import sys

from PySide2.QtCore import Qt, QFile, QIODevice
from PySide2 import QtWidgets
from PySide2.QtUiTools import QUiLoader

from factories import ErasureFactory
from utils import Utils
from verify import Verify


class PyRaseController:
    DEFAULT_METHODS = [
        'Zero Overwrite',
        'One Overwrite',
        'Random Overwrite',
        'DOD Overwrite',
    ]

    def __init__(self):
        loader = QUiLoader()
        self.ui = loader.load('pyrase.ui')
        self.overwrite = None
        self.verify = None
        self.device = None
        self.method = None
        self.devices = Utils.get_block_devices()
        self._add_default_methods_to_method_box()
        self._add_devices_to_device_box()

        self.ui.device_box.currentIndexChanged.connect(self._set_device)
        self.ui.close_button.clicked.connect(self.ui.close)
        self.ui.erase_button.clicked.connect(self._erase)

    def _add_default_methods_to_method_box(self):
        self.ui.method_box.clear()
        for method in self.DEFAULT_METHODS:
            self.ui.method_box.addItem(method)

    def _add_devices_to_device_box(self):
        for device in self.devices:
            self.ui.device_box.addItem(device)

    def _erase(self):
        self.method = self.ui.method_box.currentText()
        self.ui.erase_button.setEnabled(False)
        self.ui.close_button.setEnabled(False)

        if self.method == 'Zero Overwrite':
            self.overwrite = ErasureFactory.zero_overwrite(self.device)
            self.overwrite.finished.connect(self._verify)
            self.overwrite.start()
            self.overwrite.CURRENT_DATA.connect(self.ui.erase_progress.setValue)
            self.overwrite.CURRENT_TIME.connect(self.ui.erase_duration_label.setText)
            self.overwrite.CURRENT_PASS.connect(self.ui.pass_value_label.setText)

        elif self.method == 'One Overwrite':
            self.overwrite = ErasureFactory.one_overwrite(self.device)
            self.overwrite.finished.connect(self._verify)
            self.overwrite.start()
            self.overwrite.CURRENT_DATA.connect(self.ui.erase_progress.setValue)
            self.overwrite.CURRENT_TIME.connect(self.ui.erase_duration_label.setText)
            self.overwrite.CURRENT_PASS.connect(self.ui.pass_value_label.setText)

        elif self.method == 'Random Overwrite':
            self.overwrite = ErasureFactory.random_overwrite(self.device)
            self.overwrite.finished.connect(self._verify)
            self.overwrite.start()
            self.overwrite.CURRENT_DATA.connect(self.ui.erase_progress.setValue)
            self.overwrite.CURRENT_TIME.connect(self.ui.erase_duration_label.setText)
            self.overwrite.CURRENT_PASS.connect(self.ui.pass_value_label.setText)

        elif self.method == 'DOD Overwrite':
            self.overwrite = ErasureFactory.dod_overwrite(self.device)
            self.overwrite.finished.connect(self._verify)
            self.overwrite.start()
            self.overwrite.CURRENT_DATA.connect(self.ui.erase_progress.setValue)
            self.overwrite.CURRENT_TIME.connect(self.ui.erase_duration_label.setText)
            self.overwrite.CURRENT_PASS.connect(self.ui.pass_value_label.setText)

    def _verify(self):
        if self.method == 'Zero Overwrite':
            pattern = b'\0x00'
        elif self.method == 'One Overwrite':
            pattern = b'\0xff'
        else:
            pattern = 'random'

        self.ui.erase_progress.setValue(100)
        self.verify = Verify(self.device, pattern, self.ui.verify_percent.value())
        self.verify.finished.connect(self._finished)
        self.verify.start()
        self.verify.CURRENT_DATA.connect(self.ui.verify_progress.setValue)
        self.verify.CURRENT_TIME.connect(self.ui.verify_duration_label.setText)

    def _finished(self):
        self.ui.verify_progress.setValue(100)

        if self.verify.success:
            erasure_status = 'Passed'
        else:
            erasure_status = 'Failed'

        self.ui.close_button.setEnabled(True)

    def _set_device(self):
        if '/dev/sd' in self.ui.device_box.currentText():
            self.device = self.ui.device_box.currentText()[:8]
        elif '/dev/nvm' in self.ui.device_box.currentText():
            self.device = self.ui.device_box.currentText()[:12]

