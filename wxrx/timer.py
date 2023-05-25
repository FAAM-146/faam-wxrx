import datetime
import os

import pandas as pd

class Timer:
    """
    Provides a timer for a given logfile and tmpfile. This allows the time at which
    a given size was reached to be calculated. This is used to add a timestamp to
    the ARINC708 data, which is not timestamped.
    """

    def __init__(self, logfile: str, tmpfile: str = '') -> None:
        """
        Create a new Timer object.

        Args:
            logfile (str): Path to the logfile to use for the timer
            tmpfile (str): The tmpfile to use for the timer.
        """
        self.df = pd.read_csv(
            logfile,
            parse_dates=[0],
            names=['time', 'size', 'tmpfile'],
            header=3,
            index_col=0
        )

        if not tmpfile and self.df.tmpfile.nunique() != 1:
            raise ValueError(f'No tmpfile specified and logfile contains multiple tmpfiles')

        if tmpfile:
            self.df = self.df[self.df.tmpfile == tmpfile]

        self.df = self.df.asfreq('1s').interpolate()
        self.df.tmpfile.fillna(method='ffill', inplace=True)

        if len(self.df) == 0:
            raise ValueError(f'No data for {tmpfile}')

    
    @property
    def date(self) -> datetime.date:
        """
        Returns the date of the first entry in the logfile.

        Returns:
            datetime.date: The date of the first entry in the logfile
        """
        return self.df.index[0].date()
    
    def includes(self, tempfile: str) -> bool:
        """
        Indicates whether the timer includes a reference to the given tempfile.

        Args:
            tempfile (str): The tempfile to check for

        Returns:
            bool: True if the timer includes the tempfile, False otherwise
        """
        return tempfile in self.df.tmpfile.unique()
    
    @classmethod
    def get_tempfiles(cls, logfile: str) -> list[str]:
        """
        Returns a list of tempfiles in the given logfile.

        Args:
            logfile (str): The logfile to check

        Returns:
            list[str]: A list of tempfiles in the given logfile
        """
        data = pd.read_csv(
            logfile,
            parse_dates=[0],
            names=['time', 'size', 'tmpfile'],
            header=3,
            index_col=0
        )
        return data.tmpfile.unique().tolist()
    
    def time_at_size(self, size: int, tmpfile: str='') -> pd.Timestamp:
        """
        Returns the time at which the given size was reached.

        Args:
            size (int): The size to check for
            tmpfile (str): The tempfile to check for

        Returns:
            pd.Timestamp: The nearest time to which the given size was reached.
        """
        
        # get the index of self.df where the size is closest to the requested size
        if tmpfile:
            tmpfile = os.path.basename(tmpfile)
            return self.df[self.df.tmpfile == tmpfile]['size'].sub(size).abs().idxmin()
        return self.df['size'].sub(size).abs().idxmin()
            
        

        

