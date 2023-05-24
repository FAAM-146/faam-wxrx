class Metadata:
    def __init__(self):
        self._metadata = {}

    def add_global(self, key, value):
        self._metadata[key] = value

    def write_to_nc(self, nc):
        for key, value in self._metadata.items():
            try:
                value = value()
            except TypeError:
                pass
            
            nc.setncattr(key, value)