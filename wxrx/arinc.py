from collections import namedtuple

SCAN_ANGLES = [0xb4 / 2**i for i in range(12)]

ARINC708_DELINIATOR = 0b10110100 #0o055, LSB first
ARINC708_LENGTH_BYTES = 200

Arinc708Message = namedtuple('Arinc708Message', [
    'label', 'control_accept', 'slave', 'spare1', 'mode_annunciation',
    'faults', 'stabilization', 'operating_mode', 'tilt', 'gain', 'range',
    'spare2', 'data_accept', 'scan_angle', 'data'
])
