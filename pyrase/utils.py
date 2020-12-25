import subprocess
import re
import os
from PySide2.QtCore import Qt


class Utils:
    @classmethod
    def get_device_size(cls, device):
        f = open(device, 'rb')
        f.seek(0, os.SEEK_END)
        size = f.tell()
        f.close()
        return int(size)

    @classmethod
    def get_block_devices(cls):
        devices = []
        device_list = os.popen('lsblk -o NAME,MODEL,SIZE -np --nodeps').read().split('\n')
        for device in device_list:
            if '/dev/sd' in device or '/dev/nvm' in device:
                devices.append(device)
        return devices

