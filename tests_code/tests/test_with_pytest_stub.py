from unittest.mock import Mock

import pytest

from tests_code.my_alarm import MyAlarm, Sensor
from tests_code.my_code import MyCode


class StubSensor:
    def get_pressure(self):
        return 1.0


def test_low_threshold():
    alarm = MyAlarm(StubSensor())
    assert alarm.check_sensor()


def test_high_threshold():
    stub = Mock(Sensor)
    stub.get_pressure.return_value = 10.0
    alarm = MyAlarm(stub)
    assert alarm.check_sensor()
