class ChargerController:
    def __init__(self):
        self.state = 'off'
    
    def get_state(self):
        return self.state
    
    def toggle(self):
        self.state = 'on' if self.state == 'off' else 'off'

charger = ChargerController()