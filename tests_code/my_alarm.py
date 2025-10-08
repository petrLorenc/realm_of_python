class Sensor:
    def __init__(self):
        self.pressure = 0

    def increase_pressure(self, value):
        self.pressure += value

    def decrease_pressure(self, value):
        self.pressure -= value

    def get_pressure(self):
        return self.pressure


class SystemWrapper:
    def notify(self, message):
        print(message)


class MyAlarm:

    def __init__(self, sensor, system):
        self.high_threshold = 10.0
        self.low_threshold = 1.0
        self.sensor = sensor or Sensor()
        self.system = system or SystemWrapper()

    def check_sensor(self):
        pressure = self.sensor.get_pressure()
        if pressure >= self.high_threshold:
            self.system.notify("High pressure")
            return True
        elif pressure <= self.low_threshold:
            self.system.notify("Low pressure")
            return True
        self.system.notify("Normal pressure")
        return False
