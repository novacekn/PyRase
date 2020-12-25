from overwrites import OverwriteMethod, Overwrite


class ErasureFactory:
    @staticmethod
    def zero_overwrite(device):
        return Overwrite(OverwriteMethod.ZERO_OVERWRITE, device)

    @staticmethod
    def one_overwrite(device):
        return Overwrite(OverwriteMethod.ONE_OVERWRITE, device)

    @staticmethod
    def dod_overwrite(device):
        return Overwrite(OverwriteMethod.DOD_OVERWRITE, device)

    @staticmethod
    def random_overwrite(device):
        return Overwrite(OverwriteMethod.RANDOM_OVERWRITE, device)

