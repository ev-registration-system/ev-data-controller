import firebase_admin
from firebase_admin import credentials, firestore

details = credentials.Certificate("ev-registration-system-firebase-admin.json") 
firebase_admin.initialize_app(details)
db = firestore.client()

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

        # Write data to Firestore
        data = {
            "ir_sensor": ir_sensor,
            "charger_power": charger_power,
            "ev_charger_value": ev_value,
        }
        db.collection("chargers").document(str(charger_id)).set(data)
        print(f"Data successfully written for Charger ID: {charger_id}")

    # Catching and printing errors
    except ValueError as e:
        print(f"Value Error: {e}")
    except Exception as e:
        print(f"An error occurred while writing to Firestore: {e}")

if __name__ == "__main__":
    controller()
