import pandas as pd
from datetime import datetime

class IRSensor:
    def __init__(self, csv_file='app/ir_sensor_data.csv'):
        self.csv_file = csv_file
        self.data = self.load_csv_data()
        
    def load_csv_data(self):
        try:
            df = pd.read_csv(self.csv_file)
            current_date = datetime.now().date()
            # current_hour = datetime.now().hour # dev only
            
            df['timestamp'] = df.apply(
                lambda row: datetime(current_date.year, current_date.month, current_date.day, int(row['hour']), int(row['minute']), 0, 0),
                # lambda row: datetime(current_date.year, current_date.month, current_date.day, current_hour, int(row['hour']), int(row['minute']), 0), # dev only
                axis=1
            )
            return df
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return pd.DataFrame()

    def get_system_time(self):
        now = datetime.now()
        return now.replace(minute=(now.minute // 30) * 30, second=0, microsecond=0)

    def detect_vehicle(self):
        if self.data.empty:
            print("IRSensor: No CSV data loaded or file is empty.")
            return False

        current_slot = self.get_system_time()
        row = self.data[self.data['timestamp'] == current_slot]

        if row.empty:
            print(f"IRSensor: No IR data for time slot: {current_slot}")
            return False

        ir_value = row.iloc[0]['ir_value']
        vehicle_present = ir_value >= 0.6
        print(f"IRSensor: [{current_slot}] IR Value={ir_value}, Vehicle Present={vehicle_present}")
        return vehicle_present
