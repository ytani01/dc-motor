#!/usr/bin/env python3
#
# (c) Yoichi Tanibayashi
#
"""
"""
__author__ = 'Yoichi Tanibayashi'
__date__   = '2020/08'

import pigpio
from DcMtr import DcMtrN
from MyLogger import get_logger


class App:
    _log = get_logger(__name__, False)

    def __init__(self, pi, pin, debug=False):
        self._dbg = debug
        __class__._log = get_logger(__class__.__name__, self._dbg)
        self._log.debug('pin=%s', pin)

        self._pi = pi

        if len(pin) % 2 != 0:
            msg = 'invalid pin number: %s' % list(pin)
            raise RuntimeError(msg)

        self._pin = []
        for p in list(range(0, len(pin), 2)):
            self._log.debug('p=%s', p)
            self._pin.append([pin[p], pin[p+1]])

        self._dc_mtr = DcMtrN(self._pi, self._pin, debug=self._dbg)

        self._active = True

    def main(self):
        self._log.debug('')

        while self._active:
            line = input('-100..0..100|b=break> ')
            if len(line) == 0:
                self._active = False

            speed = []
            for s in line.split():
                try:
                    num = int(s)
                    speed += [num]

                except ValueError:
                    self._log.info('break!')
                    self._dc_mtr.set_break(1)
                    speed = []
                    break

            if len(speed) == 0:
                continue

            if len(speed) != self._dc_mtr.get_n():
                self._log.error('num of motors = %s', self._dc_mtr.get_n())
                continue

            self._dc_mtr.set_speed(speed)

    def end(self):
        self._dc_mtr.set_stop(1)


import click
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('pin', type=int, nargs=-1)
@click.option('--debug', '-d', 'debug', is_flag=True, default=False,
              help='debug option')
def main(pin, debug):
    _log = get_logger(__name__, debug)
    _log.debug('pin=%s', pin)

    pi = pigpio.pi()

    app = App(pi, pin, debug=debug)
    try:
        app.main()
    finally:
        _log.debug('end')
        app.end()
        pi.stop()


if __name__ == '__main__':
    main()

# for emacs
# Local Variables:
# Coding: utf-8-unix
# End:
