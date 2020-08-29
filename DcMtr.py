#!/usr/bin/env python3
#
# (c) Yoichi Tanibayashi
#
import pigpio
import time
from MyLogger import get_logger


class DcMtr:
    PWM_FREQ = 50
    PWM_RANGE = 100

    _log = get_logger(__name__, False)

    def __init__(self, pi, pin, debug=False):
        self._dbg = debug
        __class__._log = get_logger(__class__.__name__, self._dbg)
        self._pi = pi
        self._pin = pin

        self._n = len(pin)
        self._pwm_freq = list(range(self._n))
        self._pwm_range = list(range(self._n))

        for i in range(self._n):
            self._pi.set_mode(self._pin[i], pigpio.OUTPUT)
            self._pwm_freq[i] = pi.set_PWM_frequency(
                self._pin[i], DcMtr.PWM_FREQ)
            self._pwm_range[i] = pi.set_PWM_range(
                self._pin[i], DcMtr.PWM_RANGE)
            self._pi.set_PWM_dutycycle(pin[i], 0)

    def set(self, in1, in2):
        if in1 < 0:
            in1 = 0
        if in1 > DcMtr.PWM_RANGE:
            in1 = DcMtr.PWM_RANGE
        if in2 < 0:
            in2 = 0
        if in2 > DcMtr.PWM_RANGE:
            in2 = DcMtr.PWM_RANGE

        self._log.debug('in=(%s, %s)', in1, in2)

        self._pi.set_PWM_dutycycle(self._pin[0], in1)
        self._pi.set_PWM_dutycycle(self._pin[1], in2)

    def set_speed(self, speed, sec=0):
        if speed < -DcMtr.PWM_RANGE:
            speed = -DcMtr.PWM_RANGE
        if speed > DcMtr.PWM_RANGE:
            speed = DcMtr.PWM_RANGE

        if speed >= 0:
            self.set(speed, 0)
        else:
            self.set(0, -speed)

        time.sleep(sec)

    def set_break(self, sec=0):
        self.set(DcMtr.PWM_RANGE, DcMtr.PWM_RANGE)
        time.sleep(sec)

    def set_stop(self, sec=0):
        self.set(0, 0)
        time.sleep(sec)


class DcMtrN:
    _log = get_logger(__name__, False)

    def __init__(self, pi, pin, debug=False):
        self._dbg = debug
        __class__._log = get_logger(__class__.__name__, self._dbg)
        self._pi = pi
        self._pin = pin

        self._n = len(self._pin)
        self._dc_mtr = list(range(self._n))

        for i in range(self._n):
            self._dc_mtr[i] = DcMtr(self._pi, self._pin[i], self._dbg)

    def get_n(self):
        return self._n

    def set_speed(self, speed, sec=0):
        for i in range(self._n):
            self._dc_mtr[i].set_speed(speed[i])
        time.sleep(sec)

    def set_break(self, sec=0):
        for i in range(self._n):
            self._dc_mtr[i].set_break()
        time.sleep(sec)

    def set_stop(self, sec=0):
        for i in range(self._n):
            self._dc_mtr[i].set_stop()
        time.sleep(sec)


#####
def main1(pi):
    pin = [[13, 12], [17, 18]]

    dc_mtr = DcMtrN(pi, pin, debug=True)
    print(dc_mtr._n)
    for i in range(dc_mtr._n):
        print(dc_mtr._dc_mtr[i]._pwm_freq)
        print(dc_mtr._dc_mtr[i]._pwm_range)

    try:
        dc_mtr.set_speed([100, 30], 1)
        dc_mtr.set_break(0.3)
        dc_mtr.set_speed([-30, -100], 1)
        dc_mtr.set_break(0.3)
    finally:
        print('dc_mtr.set_stop()')
        dc_mtr.set_stop()


if __name__ == '__main__':
    pi = pigpio.pi()
    try:
        main1(pi)
    finally:
        print('pi.stop()')
        pi.stop()

# for emacs ..
# Local Variables:
# Coding: utf-8-unix
# End:
