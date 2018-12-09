# The MIT License (MIT)
#
# Copyright (c) 2016 Scott Shawcroft for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
`adafruit_bus_device.i2c_device` - I2C Bus Device
====================================================
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_BusDevice.git"

class I2CDevice:
    def __init__(self, i2c, device_address):
        # Verify that a device with that address exists.
        try:
            i2c.writeto(device_address, b'')
        except OSError:
            raise ValueError("No I2C device at address: %x" % device_address)
        self.i2c = i2c
        self.device_address = device_address

    def readinto(self, buf, **kwargs):
        self.i2c.readfrom_into(self.device_address, buf, **kwargs)

    def write(self, buf, **kwargs):
        self.i2c.writeto(self.device_address, buf, **kwargs)

    def write_then_readinto(self, out_buffer, in_buffer, *,
                            out_start=0, out_end=None, in_start=0, in_end=None, stop=True):
        if out_end is None:
            out_end = len(out_buffer)
        if in_end is None:
            in_end = len(in_buffer)
        if hasattr(self.i2c, 'writeto_then_readfrom'):
            # In linux, at least, this is a special kernel function call
            self.i2c.writeto_then_readfrom(self.device_address, out_buffer, in_buffer,
                                           out_start=out_start, out_end=out_end,
                                           in_start=in_start, in_end=in_end, stop=stop)
        else:
            # If we don't have a special implementation, we can fake it with two calls
            self.write(out_buffer, start=out_start, end=out_end, stop=stop)
            self.readinto(in_buffer, start=in_start, end=in_end)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False
