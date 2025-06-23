from machine import I2C
import struct
import time

class BMP280:
    def __init__(self, i2c, addr=0x76):
        self.i2c = i2c
        self.addr = addr
        self._load_calibration()
        self.i2c.writeto_mem(self.addr, 0xF4, b'\x27')  # normal mode
        self.i2c.writeto_mem(self.addr, 0xF5, b'\xA0')  # config

    def _read16(self, reg):
        data = self.i2c.readfrom_mem(self.addr, reg, 2)
        return struct.unpack('<H', data)[0]

    def _read16s(self, reg):
        data = self.i2c.readfrom_mem(self.addr, reg, 2)
        return struct.unpack('<h', data)[0]

    def _read24(self, reg):
        data = self.i2c.readfrom_mem(self.addr, reg, 3)
        return (data[0] << 16) | (data[1] << 8) | data[2]

    def _load_calibration(self):
        self.dig_T1 = self._read16(0x88)
        self.dig_T2 = self._read16s(0x8A)
        self.dig_T3 = self._read16s(0x8C)
        self.dig_P1 = self._read16(0x8E)
        self.dig_P2 = self._read16s(0x90)
        self.dig_P3 = self._read16s(0x92)
        self.dig_P4 = self._read16s(0x94)
        self.dig_P5 = self._read16s(0x96)
        self.dig_P6 = self._read16s(0x98)
        self.dig_P7 = self._read16s(0x9A)
        self.dig_P8 = self._read16s(0x9C)
        self.dig_P9 = self._read16s(0x9E)

    def read_raw(self):
        data = self.i2c.readfrom_mem(self.addr, 0xF7, 6)
        adc_p = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        adc_t = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
        return adc_t, adc_p

    def compensate_temperature(self, adc_T):
        var1 = (((adc_T >> 3) - (self.dig_T1 << 1)) * self.dig_T2) >> 11
        var2 = (((((adc_T >> 4) - self.dig_T1) * ((adc_T >> 4) - self.dig_T1)) >> 12) * self.dig_T3) >> 14
        self.t_fine = var1 + var2
        temp = (self.t_fine * 5 + 128) >> 8
        return temp / 100.0

    def compensate_pressure(self, adc_P):
        var1 = self.t_fine - 128000
        var2 = var1 * var1 * self.dig_P6
        var2 += ((var1 * self.dig_P5) << 17)
        var2 += (self.dig_P4 << 35)
        var1 = ((var1 * var1 * self.dig_P3) >> 8) + ((var1 * self.dig_P2) << 12)
        var1 = (((1 << 47) + var1) * self.dig_P1) >> 33

        if var1 == 0:
            return 0  # evita divisão por zero

        p = 1048576 - adc_P
        p = (((p << 31) - var2) * 3125) // var1
        var1 = (self.dig_P9 * (p >> 13) * (p >> 13)) >> 25
        var2 = (self.dig_P8 * p) >> 19
        p = ((p + var1 + var2) >> 8) + (self.dig_P7 << 4)
        return p / 256.0

    def read_compensated_data(self):
        adc_t, adc_p = self.read_raw()
        temp = self.compensate_temperature(adc_t)
        press = self.compensate_pressure(adc_p)
        return temp, press
