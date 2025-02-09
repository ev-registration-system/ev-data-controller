import firebase_admin
from firebase_admin import credentials, firestore
import time

details = credentials.Certificate("ev-registration-system-firebase-admin.json") 
firebase_admin.initialize_app(details)
db = firestore.client()

# Get charger state from Firestore
def get_charger_state(charger_id):
    doc_ref = db.collection("charger_states").document(str(charger_id))
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        # Initialize new charger state if not found
        return {
            "last_power_state": 0,
            "last_timestamp": time.time(),
            "active_period_start": None,
            "current_active_time": 0.0,
            "current_power_used": 0.0,
        }
    
# Save charger state to Firestore
def save_charger_state(charger_id, state):
    doc_ref = db.collection("charger_states").document(str(charger_id))
    doc_ref.set(state)


# Process and update charger data
def process_charger_data(charger_id, charger_power_value, ev_charger_value):
    current_time = time.time()
    state = get_charger_state(charger_id)
    
    # Time passed since last updated timestamp in collection
    elapsed_time = current_time - state["last_timestamp"]

    # Transition from 0 to 1 of power state or still in 1 power state
    if charger_power_value == 1:
        if state["active_period_start"] is None:
            state["active_period_start"] = current_time
        state["current_active_time"] += elapsed_time
        # Calculate power used in this period
        state["current_power_used"] += ev_charger_value * (elapsed_time / 3600) 

    # Transition from 1 to 0 of power state or still in 0 power state
    else:
        # If there was an active period 
        if state["active_period_start"] is not None:
            active_duration = current_time - state["active_period_start"]
            state["current_active_time"] += active_duration
            state["current_power_used"] += ev_charger_value * (active_duration / 3600)
        
        # Log historical data before resetting
            history_data = {
                "charger_id": charger_id,
                "total_active_time_minutes": state["current_active_time"] / 60,
                "total_active_time_hours": state["current_active_time"] / 3600,
                "total_power_used_kwh": state["current_power_used"],
                "timestamp": firestore.SERVER_TIMESTAMP,
            }
            db.collection("charger_history").add(history_data)
            print("Historical data successfully logged.")

        # Save values before resetting 
        final_active_time_minutes = state["current_active_time"] / 60
        final_active_time_hours = state["current_active_time"] / 3600
        final_power_used = state["current_power_used"]

        # Reset the state values when charger power is off
        state["active_period_start"] = None
        state["current_active_time"] = 0.0
        state["current_power_used"] = 0.0

        # Save updated state to db
        save_charger_state(charger_id, state)

        return {
            "final_active_time_minutes": final_active_time_minutes,
            "final_active_time_hours": final_active_time_hours,
            "final_power_used": final_power_used,
        }
    
    # Update state for time and power
    state["last_power_state"] = charger_power_value
    state["last_timestamp"] = current_time

    # Save to collection
    save_charger_state(charger_id, state)
    return state

# Data manipulation controller
def controller():
    print("*** WELCOME TO THE EVANTAGE DATA CONTROLLER ***")
    print("Enter EV Charger data to store in Firestore Database:")
    
    
    try:
        # Prompt for Charger ID (Document ID)
        charger_id = input("Enter Charger ID (int): ").strip()
        if not charger_id:
            raise ValueError("Charger ID is required!")
        if not charger_id.isdigit():
            raise ValueError("Charger ID must be an integer.")
        charger_id = int(charger_id)
    
        # IR Sensor value (1/0)
        ir_sensor = int(input("Enter IR Sensor value (1 or 0): ").strip())
        if ir_sensor not in [0, 1]:
            raise ValueError("IR Sensor value must be 1 or 0.")

        # Charger Power value (1 or 0)
        charger_power = int(input("Enter Charger Power value (1 or 0): ").strip())
        if charger_power not in [0, 1]:
            raise ValueError("Charger Power value must be 1 or 0.")
        
        try:
            # EV Charger Value (float)
            ev_value = float(input("Enter EV Charger value (float): ").strip())
        except ValueError:
            # If the input is not a valid float
            raise ValueError("Invalid input! Please enter a valid float value for the EV Charger.")

        # Get time and power used 
        state = process_charger_data(charger_id, charger_power, ev_value)

        # Write data to Firestore
        data = {
            "ir_sensor": ir_sensor,
            "charger_power": charger_power,
            "ev_charger_value": ev_value,
        }
        db.collection("chargers").document(str(charger_id)).set(data)
        print(f"Data successfully written for Charger ID: {charger_id}")

        if state:
            if "final_active_time_minutes" in state:
                print(f"Total Time Active: {state['final_active_time_minutes']:.2f} minutes ({state['final_active_time_hours']:.2f} hours)")
                print(f"Total Power Used: {state['final_power_used']:.2f} kWh")
            else:
                print("Charger is currently active or waiting for active period to complete.")
        else:
            print(f"ERROR: Failed to process data for Charger ID: {charger_id}.")

        
    # Catching and printing errors
    except ValueError as e:
        print(f"Value Error: {e}")
    except Exception as e:
        print(f"An error occurred while writing to Firestore: {e}")

if __name__ == "__main__":
    controller()
