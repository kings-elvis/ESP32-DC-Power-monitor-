
import time


class I2cLcd:
    def __init__(self, i2c, address, rows, cols):
        self.i2c = i2c
        self.address = address
        self.rows = rows
        self.cols = cols

        self.i2c.writeto(self.address, b'\x00')
        time.sleep_ms(20)

        self._write4(0x30)
        time.sleep_ms(5)
        self._write4(0x30)
        time.sleep_ms(1)
        self._write4(0x30)
        self._write4(0x20)

        self.command(0x28)
        self.command(0x0C)
        self.command(0x06)
        self.clear()

    def _write4(self, value):
        self.i2c.writeto(self.address, bytes([value | 0x0C]))
        self.i2c.writeto(self.address, bytes([value | 0x08]))

    def _send(self, value, mode):
        high = value & 0xF0
        low = (value << 4) & 0xF0

        self._write4(high | mode)
        self._write4(low | mode)

    def command(self, value):
        self._send(value, 0)

    def write_char(self, value):
        self._send(value, 1)

    def clear(self):
        self.command(0x01)
        time.sleep_ms(2)

    def move_to(self, col, row):
        offsets = [0x00, 0x40, 0x14, 0x54]
        self.command(0x80 | (offsets[row] + col))

    def putstr(self, text):
        for char in text:
            self.write_char(ord(char))
