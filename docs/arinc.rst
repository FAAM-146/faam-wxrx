=====================
The ARINC708 Protocol
=====================

Weather radar data is transmitted using the ARINC708 protocol. The
ARINC708 word consists of a 64-bit header and a 512 data values of
3 bits each. The full word is thus 1600 bits long.

.. note::
    ARINC data are presented LSB first, so the first bit transmitted
    is the least significant bit of the first byte.

The Header
==========

The 64 bit header starts with a label of 8 bits, which is always 0o055
(or equivalently 0b10110100). The header contains the following fields:

.. _arinc708-header:
.. csv-table:: ARINC708 Header
    :header: "Bit(s)", "Name", "Description"

    "0-7", "Label", "Always 0o055"
    "8-9", "Control Accept", "See :numref:`arinc708_control_accept`"
    "10", "Slave", "0=Master, 1=Slave"
    "11-12", "Unused", ""
    "13-17", "Mode Annunciation", "See :numref:`arinc708_mode_annunciation`"
    "18-24", "Faults", "See :numref:`arinc708_faults`"
    "25", "Stabilization", "0=Off, 1=On"
    "26-28", "Operating Mode", "See :numref:`arinc708_operating_mode`"
    "29-35", "Tilt", "See :numref:`arinc708_tilt`"
    "36-41", "Gain", "See :numref:`arinc708_gain`"
    "42-47", "Range", "See :numref:`arinc708_range`"
    "48", "Unused",
    "49-50", "Data Accept", "See :numref:`arinc708_data_accept`"
    "51-62", "Scan angle", "See :ref:`arinc708_scan_angle`"
    "63", "Unused"

Control Accept
--------------

.. csv-table:: Control Accept
    :header: Bit 9, Bit 8, Description
    :name: arinc708_control_accept

    0, 0, Do not accept control
    0, 1, IND1 accept control
    1, 0, IND2 accept control
    1, 1, IND1 and IND2 accept control

Mode Annunciation
-----------------

.. csv-table:: Mode Annunciation
    :header: Bit, Mode annunciuation
    :name: arinc708_mode_annunciation

    13, Automatic sensing of a turbulence alert has occurred
    14, Automatic sensing of a reflectivity weather alert has occurred
    15, Clutter elimination is active
    16, Reduced sector scan is in operation
    17, Aircraft attitude and/or tilt exceeds the system's design limits

Faults
------

.. csv-table:: Faults
    :header: Bit, Fault
    :name: arinc708_faults

    18, Cooling fault
    19, Display fault
    20, Calibration fault
    21, Altitude input fault
    22, Control fault
    23, Antenna fault
    24, Transmitter/receiver fault

Operating Mode
--------------

.. csv-table:: Operating Mode
    :header: Bit 28, Bit 27, Bit 26, Operating mode
    :name: arinc708_operating_mode

    0, 0, 0, Standby
    0, 0, 1, Weather (only)
    0, 1, 0, Map
    0, 1, 1, Contour
    1, 0, 0, Test
    1, 0, 1, Turbulence (only)
    1, 1, 0, Weather and turbulence
    1, 1, 1, Reserved (Calibration annunciuation)

Tilt
----

.. csv-table:: Tilt
    :header: Bit, Tilt (degrees)
    :name: arinc708_tilt

    35, -16
    34, +8
    33, +4
    32, +2
    31, +1
    30, +0.5
    29, +0.25

Gain
----

.. csv-table:: Gain
    :header: Bit 41, Bit 40, Bit 39, Bit 38, Bit 37, Bit 36, Gain (dB)
    :name: arinc708_gain

    1, 1, 1, 1, 1, 1, Calibration
    0, 0, 0, 0, 0, 0, Max
    0, 0, 0, 0, 0, 1, -5
    0, 0, 0, 0, 1, 1, -11
    1, 1, 1, 1, 1, 0, -62


Range
-----

.. csv-table:: Range
    :header: Bit 47, Bit 46, Bit 45, Bit 44, Bit 43, Bit 42, Range (nm)
    :name: arinc708_range

    0, 0, 0, 0, 0, 1, 5
    0, 0, 0, 0, 1, 0, 10
    0, 0, 0, 1, 0, 0, 20
    0, 0, 1, 0, 0, 0, 40
    0, 1, 0, 0, 0, 0, 80
    1, 0, 0, 0, 0, 0, 160
    1, 1, 1, 1, 1, 1, 315
    0, 0, 0, 0, 0, 0, 320

Data Accept
-----------

.. csv-table:: Data Accept
    :header: Bit 50, Bit 49, Data Accept
    :name: arinc708_data_accept

    0, 0, Do not accept data
    0, 1, Accept data 1
    1, 0, Accept data 2
    1, 1, Accept any data

.. _arinc708_scan_angle:

Scan Angle
----------
The scan angle is given by bits 51-62. Bit 62 is the most significant
bit, and takes a value of 180 degrees. Each less significant bit takes
the value of half the next more significant bit. For example, bit 61
takes a value of 90 degrees, and bit 60 takes a value of 45 degrees.
The least significant bit, bit 51, takes a value of 0.087890625 degrees.

The Data
========

The data payload is 1536 bits long, divided into 512 3-bit fields. Each
field gives a categorized radar return, summarized in :numref:`arinc708_data_bins`.

.. csv-table:: Data bins
    :header: Bit 2, Bit 1, Bit 0, Category, Representative Color
    :name: arinc708_data_bins

    0, 0, 0, No precipitation (<Z2), Black
    0, 0, 1, Light precipitation (Z2 to Z3), Green
    0, 1, 0, Moderate precipitation (Z3 to Z4), Yellow
    0, 1, 1, Heavy precipitation (Z4 to Z5), Red
    1, 0, 0, Very heavy precipitation (>Z5), Magenta
    1, 0, 1, Reserved (out of cal indication), 
    1, 1, 0, Medium turbulence,
    1, 1, 1, Heavy turbulence,