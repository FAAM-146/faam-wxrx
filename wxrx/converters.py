from .arinc import SCAN_ANGLES


def scan_angle_from_int(i: int) -> float:
    """
    Returns the scan angle from the integer representation.

    Args:
        i (int): The integer representation of the scan angle.

    Returns:
        float: The scan angle in degrees.
    """
    return i * SCAN_ANGLES[-1]


def tilt_from_int(i: int) -> float:
    """
    Returns the tilt angle in degrees.

    Args:
        i (int): The encoded tilt value.

    Returns:
        float: The tilt angle in degrees.
    """
    return (i & 0x40) * (-16) + (i & 0x3f) * .25


def range_from_int(i: int) -> int:
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


def gain_from_int(i: int) -> int:
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
