===================
Dataset Description
===================

The FAAM provided weather radar data are provided in a netCDF file. The
file is essentially a low-level represention of the raw ARINC708 data, with
the exception of the following:

* Range (nm)
* Tilt (deg)
* Gain (dB)
* Scan angle (deg)

which are all converted from their packed binary representation to
floating point or integer values.

A full description of the data format is provided in the 
`FAAM Data Github repository <https://github.com/FAAM-146/faam-data>`_. For 
convenience, a summary of the data format is provided below.

WxRx NetCDF Specification
==========================

.. include:: _dynamic/wxrx.rst