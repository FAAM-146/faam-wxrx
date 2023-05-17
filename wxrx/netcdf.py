import datetime
from typing import Any
import uuid

from netCDF4 import Dataset
from faam_data import get_product
from vocal.schema_types import type_from_spec

from .arinc import Arinc708Message
from .converters import scan_angle_from_int, gain_from_int, range_from_int, tilt_from_int
from . import __version__ as wxrx_version


ENUM_OPERATING_MODE = {
    'Standby': 0,
    'Weather (only)': 1,
    'Map': 2,
    'Contour': 3,
    'Test': 4,
    'Turbulence (only)': 5,
    'Turbulence and Weather': 6,
    'Reserved (calibration annunciation)': 7
}

ENUM_CONTROL_ACCEPT = {
    'Do not accept control': 0,
    'IND1 accept control': 1,
    'IND2 accept control': 2,
    'All INDs accept control': 3
}

ENUM_DATA_ACCEPT = {
    'Do not accept': 0,
    'Accept data 1': 1,
    'Accept data 2': 2,
    'Accept any data': 3
}

ENUM_DATA = {
    'No Precipitation (<Z2)': 0,
    'Light Precipitation (Z2 to Z3)': 1,
    'Moderate Precipitation (Z3 to Z4)': 2, 
    'Heavy Precipitation (Z4 to Z5)': 3,
    'Very Heavy Precipitation (>Z5)': 4,
    'Reserved (out of cal. indication)': 5,
    'Medium Turbulence': 6,
    'Severe Turbulence': 7
}

def get_duration(start_time: datetime.datetime, end_time: datetime.datetime) -> str:
    """
    Get the duration of the flight in ISO8601 format

    Args:
        start_time (datetime.datetime): Start time of the flight
        end_time (datetime.datetime): End time of the flight

    Returns:
        str: Duration of the flight in ISO8601 format
    """
    duration = end_time - start_time
    hours = duration.seconds // 3600
    minutes = (duration.seconds % 3600) // 60
    seconds = duration.seconds % 60
    return f'PT{hours}H{minutes}M{seconds}S'


def GLOBAL_OVERWRITES(writer: 'NetCDFWriter') -> dict[str, Any]:
    """
    Get the global attributes for the netCDF file which are not defined in the product definition
    or in the core file.
    """
    start_time = datetime.datetime.utcfromtimestamp(int(writer.nc['time'][0]))
    end_time = datetime.datetime.utcfromtimestamp(int(writer.nc['time'][-1]))
    duration = get_duration(start_time, end_time)
    return {
        'comment': ('This file is a netCDF representation of the weather radar data from '
                    'the ARINC708 databus.'),
        'constants_file': None,
        'date_created': f'{datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")}Z',
        'processing_software_version': wxrx_version,
        'processing_software_doi': '10.5281/zenodo.7944619',
        'processing_software_url': 'https://www.github.com/FAAM-146/faam-wxrx',
        'processing_software_commit': None,
        'references': 'https://doi.org/10.5281/zenodo.7944511',
        'source': ('Captured from the ARINC708 databus on the FAAM WxRx computer, '
                   'using Copilot v3 and a Ballard Technology LP708-1 interface card.'),
        'revision_number': 0,
        'revision_date': datetime.date.today().strftime('%Y-%m-%d'),
        'uuid': str(uuid.uuid4()),
        'time_coverage_duration': duration,
        'time_coverage_end': end_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'time_coverage_start': start_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'title': f'FAAM Weather Radar Data for flight {writer.flight_number} on {start_time.strftime("%Y-%m-%d")}',
        'summary': f'This file contains the weather radar data from the FAAM aircraft, captured during flight {writer.flight_number}',
        'id': writer.filename.replace('.nc', ''),
}

class NetCDFWriter:
    """
    A class to write a netCDF file from the ARINC708 databus weather radar data.
    """

    def __init__(self, corefile: str) -> None:
        """
        Create a new NetCDFWriter object.

        Args:
            corefile (str): Path to the core file to use for the metadata
        """
        self.corefile = corefile
        self.filename: str = ''
        self.flight_date: datetime.datetime = datetime.datetime.min
        self.flight_number: str = ''

    def _get_filename(self, corefile: str) -> str:
        """
        Get the filename for the netCDF file from the core file.

        Args:
            corefile (str): Path to the core file to use for the metadata

        Returns:
            str: Filename for the netCDF file
        """
        with Dataset(corefile, 'r') as nc:
            self.flight_number = nc.getncattr('flight_number')
            self.flight_date = datetime.datetime.strptime(nc.getncattr('flight_date'), '%Y-%m-%d')
            return f'faam-wxrx_{self.flight_date.strftime("%Y%m%d")}_r0_{self.flight_number}_l0.nc'
        

    def init_file(self) -> None:
        """
        Initialise the netCDF file, creating the dimensions and variables from the
        product definition.
        """
        product = get_product('wxrx-raw')
        for dimension in product.dimensions:
            self.nc.createDimension(dimension.name, dimension.size)

        for variable in product.variables:

            ncvar = self.nc.createVariable(
                variable.meta.name,
                type_from_spec(variable.meta.datatype),
                variable.dimensions,
                fill_value=variable.attributes.FillValue
            )
            setattr(self, variable.meta.name, ncvar)

            for key, value in variable.attributes:
                if value is None or key == 'FillValue' or 'derived_from_file' in key:
                    continue
                setattr(ncvar, key, value)
        


    def write_message(self, time: float, message: Arinc708Message) -> None:
        """
        Write a single ARINC708 message to the netCDF file.

        Args:
            time (float): Time of the message, in seconds since the epoch
            message (Arinc708Message): The ARINC708 message to write
        """
        i = len(self.time)
        try:
            self.time[i] = time
            self.control_accept[i] = message.control_accept
            self.slave[i] = message.slave
            self.mode_annunciation[i] = message.mode_annunciation
            self.faults[i] = message.faults
            self.stabilization[i] = message.stabilization
            self.operating_mode[i] = message.operating_mode
            self.tilt[i] = tilt_from_int(message.tilt)
            self.gain[i] = gain_from_int(message.gain)
            self.range[i] = range_from_int(message.range)
            self.data_accept[i] = message.data_accept
            self.scan_angle[i] = scan_angle_from_int(message.scan_angle)
            self.reflectivity[i, :] = message.data[::-1]
        except Exception as e:
            pass

    def __enter__(self) -> 'NetCDFWriter':
        """
        Context manager entry point. On entry, the netCDF file is opened and initialised.
        """
        self.filename = self._get_filename(self.corefile)
        self.nc = Dataset(self.filename, 'w')
        self.init_file()
        return self
    
    def __exit__(self, exc_type: type, exc_value: Exception, traceback: object) -> None:
        """
        Context manager exit point. On exit, the netCDF file is closed and the global
        attributes are written. Though not in that order.

        Args:
            exc_type (type): Exception type
            exc_value (Exception): Exception value
            traceback (object): Traceback object
        """
        overwrites = GLOBAL_OVERWRITES(self)
        
        with Dataset(self.corefile, 'r') as nc:
            for attr in nc.ncattrs():
                value = nc.getncattr(attr)
                
                if attr in overwrites:
                    value = overwrites[attr]

                    while callable(value):
                        value = value()

                if value is not None:
                    self.nc.setncattr(attr, value)
        self.nc.close()

        



