import pandas as pd

class Timer:
    def __init__(self, logfile: str, tmpfile: str = '') -> None:
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
    def date(self) -> str:
        return self.df.index[0].date()
    
    def includes(self, tempfile: str) -> bool:
        return tempfile in self.df.tmpfile.unique()
    
    def time_at_size(self, size: int, tmpfile: str='') -> pd.Timestamp:
        
        # get the index of self.df where the size is closest to the requested size
        if tmpfile:
            return self.df[self.df.tmpfile == tmpfile]['size'].sub(size).abs().idxmin()
        return self.df['size'].sub(size).abs().idxmin()
            
        

        

