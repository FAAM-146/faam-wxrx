from collections.abc import Generator

from tqdm import tqdm

from .arinc import Arinc708Message, ARINC708_DELINIATOR, ARINC708_LENGTH_BYTES
from .netcdf import NetCDFWriter
from .timer import Timer


def parse_message(data: bytes) -> Arinc708Message:
    """
    Parse a single ARINC 708 message. See the ARINC 708 specification for details.

    Args:
        data (bytes): The data to parse

    Returns:
        Arinc708Message: The parsed message
    """

    # Each message has a 64 bit header
    header = data[0:8]
    b = int.from_bytes(header, 'little')

    # First 8 bits are the label
    label = b & 0xff
    
    # Bit 9 and 10 are the control accept
    control_accept = (b >> 8) & 0x3

    # Bit 11 is the slave bit
    slave = (b >> 10) & 0x1
    # print('slave', bin(slave))

    # Bits 12 and 13 are spare
    spare1 = (b >> 11) & 0x3

    # Bits 14 to 18 are the mode annunciation
    mode_annunciation = (b >> 13) & 0x1f

    # Bits 19 to 25 are the faults
    faults = (b >> 18) & 0x7f

    # Bit 26 is the stabilization bit
    stabilization = (b >> 25) & 0x1

    # Bits 27 to 29 are the operating mode
    operating_mode = (b >> 26) & 0x7

    # Bits 30 to 36 are the tilt
    tilt = (b >> 29) & 0x7f

    # Bits 37 to 42 are the gain
    gain = (b >> 36) & 0x3f

    # Bits 43 to 48 are the range
    range = (b >> 42) & 0x7f

    # Bit 49 is the spare
    spare2 = (b >> 48) & 0x1

    # Bits 50 and 51 are the data accept
    data_accept = (b >> 49) & 0x3

    # Bits 52 to 63 are the scan angle
    scan_angle = (b >> 51) & 0xfff

    # The rest of the message is the data. Each data point is 3 bits.
    # We convert the data to an integer and then shift it to get the data points.
    data = int.from_bytes(data[8:], 'little')

    data_buffer = []
    
    rshift = 1533 # 1533 = 1600 - 64 - 3
    while(rshift >= 0):
        data_buffer.append(data >> rshift & 0x7)
        rshift -= 3

    # Return a named tuple with the parsed data
    return Arinc708Message(
        label=label,
        control_accept=control_accept,
        slave=slave,
        spare1=spare1,
        mode_annunciation=mode_annunciation,
        faults=faults,
        stabilization=stabilization,
        operating_mode=operating_mode,
        tilt=tilt,
        gain=gain,
        range=range,
        spare2=spare2,
        data_accept=data_accept,
        scan_angle=scan_angle,
        data=data_buffer
    )


def load_tmp_file(filename: str) -> bytes:
    """
    Load a raw ARINC 708 file.

    Args:
        filename (str): The filename of the raw ARINC 708 file

    Returns:
        bytes: The raw ARINC 708 data
    """
    with open(filename, 'rb') as f:
        return f.read()


def scan_tmp_data(data: bytes) -> Generator[tuple[int, Arinc708Message], None, None]:
    """
    Scan a raw ARINC 708 file and yield each message.

    Args:
        data (bytes): The raw ARINC 708 data

    Yields:
        tuple[int, Arinc708Message]: The index of the message and the message
    """

    i = 0

    data_len = len(data)
    while i < data_len:
        d = data[i]

        if d == ARINC708_DELINIATOR:
            yield i, data[i : i + ARINC708_LENGTH_BYTES]

            i += ARINC708_LENGTH_BYTES
            continue

        i += 1


def _process_tmp_file(data: bytes, tempfile: str, t: Timer, nc: NetCDFWriter, pbar: tqdm|None=None):
    """
    Process a single raw ARINC 708 file and write the output to a NetCDF file.

    Args:
        data (bytes): The raw ARINC 708 data
        tempfile (str): The filename of the raw ARINC 708 file
        t (Timer): The timer object, used to convert the index of the message to a timestamp
        nc (NetCDFWriter): The NetCDF writer object
        pbar (tqdm|None): The progress bar object
    """
    old_index = 0
    for index, raw_message in scan_tmp_data(data):
        parsed_message = parse_message(raw_message)
        time = t.time_at_size(index, tempfile).timestamp()
        nc.write_message(time, parsed_message)
        if pbar:
            pbar.update(index - old_index)
        old_index = index


def process(tempfiles: list[str], logfile: str, corefile: str, with_progress: bool=True) -> None:
    """
    Process a list of raw ARINC 708 files and write the output to a NetCDF file.

    Args:
        tempfiles (list[str]): A list of raw ARINC 708 files
        logfile (str): The filename of the log file
        corefile (str): The filename of the core file
    """
    if with_progress:
        _tqdm = tqdm
    else:
        _tqdm = lambda x: x


    t = Timer(logfile)

    filtered_tempfiles = []
    for tempfile in tempfiles:
        if t.includes(tempfile):
            filtered_tempfiles.append(tempfile)
        else:
            print(f'Excluding {tempfile} from processing: no time data')
            
    with NetCDFWriter(corefile) as nc:

        for tempfile in _tqdm(filtered_tempfiles):

            data = load_tmp_file(tempfile)
            data_len = len(data)

            args = [data, tempfile, t, nc]

            if with_progress:
                with _tqdm(total=data_len) as pbar:
                    _process_tmp_file(*args, pbar)
            else:
                _process_tmp_file(*args)