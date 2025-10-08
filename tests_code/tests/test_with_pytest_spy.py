from unittest.mock import Mock, call

import pytest

from tests_code.my_alarm import MyAlarm, Sensor
from tests_code.my_code import MyCode


def test_it_was_called():
    stub = Mock(Sensor)
    stub.get_pressure.return_value = 10.0
    spy = Mock()
    alarm = MyAlarm(sensor=stub, system=spy)
    alarm.check_sensor()

    expected_calls = [
        call("High pressure")
    ]
    spy.notify.assert_has_calls(expected_calls)
