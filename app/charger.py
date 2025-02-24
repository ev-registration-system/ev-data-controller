class Charger:
    def __init__(self):
        self.state = 'off'
    
    def get_state(self):
        return self.state
    
    def turn_on(self):
        self.state = 'on'
    
    def turn_off(self):
        self.state = ''
    
    def toggle(self):
        self.state = 'on' if self.state == 'off' else 'off'