from PySide2.QtCore import QThread, Signal
from time import time
from datetime import timedelta
from math import trunc
import fastrand
import os
from utils import Utils


class Verify(QThread):
    CURRENT_DATA = Signal(int)
    CURRENT_TIME = Signal(str)

    def __init__(self, device, pattern, percent):
        super(Verify, self).__init__()
        self.device = device
        self.size = trunc(Utils.get_device_size(self.device) / 512)
        self.percent = percent
        self.bytes_needed = trunc(self.size * 512 * self.percent)
        self.bytes_read = 0
        self.success = True

    def run(self):
        drive = open(self.device, 'rb')
        timer = time()

        while self.bytes_read < self.bytes_needed:
            rand = fastrand.pcg32bounded(self.size)
            drive.seek(rand, 0)
            data = drive.read(512)

            if data != pattern * 512:
                print('Non-zero data has been failed. Erasure has failed.')
                self.success = False
                break

            self.CURRENT_DATA.emit((self.bytes_read / self.bytes_needed) * 100)
            self.CURRENT_TIME.emit(str(timedelta(seconds=(time() - timer))))
            self.bytes_read += 512

        drive.close()

