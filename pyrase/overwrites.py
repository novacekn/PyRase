from binascii import unhexlify
from time import time
import os
from PySide2.QtCore import QThread, Signal
from datetime import timedelta
import subprocess
from utils import Utils

_MEGABYTE = 1048576

class OverwriteMethod:
    ZERO_OVERWRITE = ('00000000',)
    ONE_OVERWRITE = ('11111111',)
    RANDOM_OVERWRITE = ('random',)
    DOD_OVERWRITE = ('random', 'FFFFFFFF', '00000000')


class Overwrite(QThread):
    CURRENT_DATA = Signal(int)
    CURRENT_TIME = Signal(str)
    CURRENT_PASS = Signal(str)

    def __init__(self, method, device):
        super(Overwrite, self).__init__()
        self.method = method
        self.device = device
        self.size = Utils.get_device_size(self.device)

    def run(self):
        stat = 0
        limit = int(self.size / _MEGABYTE) * _MEGABYTE
        rest = int(self.size - limit)
        timer = time()
        self.CURRENT_PASS.emit(str(stat) + '/' + str(len(self.method)))

        with open(self.device, 'w+b') as drive:
            for item in self.method:
                if item == 'random':
                    data = os.urandom(_MEGABYTE)
                    rest_data = os.urandom(rest)
                else:
                    data = unhexlify(item) * 262144
                    rest_data = unhexlify(item) * int(rest / 4)

                for total_bytes_written in range(0, self.size, _MEGABYTE):
                    if total_bytes_written == limit and rest != 0:
                        drive.write(rest_data)
                    else:
                        drive.write(data)
                    drive.flush()
                    os.fsync(drive.fileno())

                    self.CURRENT_TIME.emit(str(timedelta(seconds=(time() - timer))))
                    self.CURRENT_DATA.emit(int((total_bytes_written / self.size) * 100))

                drive.seek(0)
                stat += 1
                self.CURRENT_PASS.emit(str(stat) + '/' + str(len(self.method)))

