import platform
import os
if platform.system() == 'Windows':
  import win32file
  import pywintypes

from datetime import datetime


def changeTo(datetime_obj: datetime, of_filepaths):

  timestamp = datetime_obj.timestamp()
  if platform.system() == 'Windows':
    # Convert timestamp to Windows file time
    wintime = pywintypes.Time(timestamp)
    winfile = win32file.CreateFile(
      of_filepaths, win32file.GENERIC_WRITE, win32file.FILE_SHARE_WRITE, None, win32file.OPEN_EXISTING, 0, 0
    )
    win32file.SetFileTime(winfile, wintime, wintime, wintime)
    winfile.close()
  else:
    # Set access and modification times (creation time not modifiable on Unix-like systems)
    os.utime(of_filepaths, (timestamp, timestamp))