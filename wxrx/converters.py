from .arinc import SCAN_ANGLES


def scan_angle_from_int(i):
    """
    Returns the scan angle from the integer representation.

    Args:
        i (int): The integer representation of the scan angle.

    Returns:
        float: The scan angle in degrees.
    """
    return (
        (i & 0x800 > 0) * SCAN_ANGLES[0] +
        (i & 0x400 > 0) * SCAN_ANGLES[1] +
        (i & 0x200 > 0) * SCAN_ANGLES[2] +
        (i & 0x100 > 0) * SCAN_ANGLES[3] +
        (i & 0x80 > 0) * SCAN_ANGLES[4] +
        (i & 0x40 > 0) * SCAN_ANGLES[5] +
        (i & 0x20 > 0) * SCAN_ANGLES[6] + 
        (i & 0x10 > 0) * SCAN_ANGLES[7] +
        (i & 0x8 > 0) * SCAN_ANGLES[8] +
        (i & 0x4 > 0) * SCAN_ANGLES[9] +
        (i & 0x2 > 0) * SCAN_ANGLES[10] +
        (i & 0x1 > 0) * SCAN_ANGLES[11]
    )


def tilt_from_int(i):
    """
    Returns the tilt angle in degrees.

    Args:
        i (int): The encoded tilt value.

    Returns:
        float: The tilt angle in degrees.
    """
    return (
        (i & 0x40 > 0) * 0.25 +
        (i & 0x20 > 0) * 0.5 +
        (i & 0x10 > 0) * 1 +
        (i & 0x8 > 0) * 2 +
        (i & 0x4 > 0) * 4 +
        (i & 0x2 > 0) * 8 +
        (i & 0x1 > 0) * 16
    )


def range_from_int(i):
    """
    Returns the range in nautical miles. A value of 0 indicates maximum range,
    320 nautical miles.

    May raise a KeyError if the range is not in the lookup table.

    Args:
        i (int): The encoded range value.

    Returns:
        int: The range in nautical miles.
    """
    return {
        1: 5,
        2: 10,
        4: 20,
        8: 40,
        16: 80,
        32: 160,
        63: 315,
        0: 320
    }[i]


def gain_from_int(i):
    """
    Returns the gain. A value of 0 indicates maximum gain. A value of 1 indicates calibration.

    May raise a KeyError if the gain is not in the lookup table.

    Args:
        i (int): The encoded gain value.
    
    Returns:
        int: The gain, or an indicator of calibration.
    """
    return {
        63: 1,
        0: 0,
        5: -5,
        11: -11,
        62: -62
    }[i]