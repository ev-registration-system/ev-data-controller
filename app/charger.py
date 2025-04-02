import threading
import time

class Charger:
    def __init__(self, id):
        self.id = id
        self.state = 'off'
        self.session_energy = 0.0
        self.stop_event = threading.Event()
        self.thread = None

    def get_state(self):
        return self.state

    def turn_on(self):
        self.state = 'on'
        if not self.thread or not self.thread.is_alive():
            self.stop_event.clear()
            self.thread = threading.Thread(target=self.charge, daemon=True)
            self.thread.start()

    def turn_off(self):
        self.state = 'off'
        self.stop_event.set() # signals the charge() thrrad to stop

    def charge(self):
        while not self.stop_event.is_set():
            if self.state == 'on':
                # treating 1 minute as 1 hour at 10kWh for demonstration purposes
                self.session_energy += 10.0 / 60
            time.sleep(1)  # Wait 1 minute (really 1 second)
