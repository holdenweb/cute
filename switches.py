# Simple switch debouncer
from machine import Timer, Pin
#import utime, time

class Debounced:
    def __init__(self, pin):
        self.pin = pin
        self._state = 0
        self.value = False
        self.timer = Timer(-1)
        self.timer.init(period=8, mode=Timer.PERIODIC, callback=self.tick)
    def tick(self, _):
        bit = self.pin.value()
        self._state = ((self._state << 1) | (1 - bit)) & 0xfff
        if self._state == 0xfff:
            self.value = True
        elif self._state == 0x000:
            self.value = False
        # no action otherwise