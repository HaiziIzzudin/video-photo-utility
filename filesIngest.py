from raw import convert2raw

from PySide6.QtWidgets import ( QApplication, QFileDialog, QWidget, QVBoxLayout, QTextEdit, )
import os
from datetime import datetime
import pytz
from colorama import Fore, Style
from pymediainfo import MediaInfo

app = QApplication([]) # QApplication must be initialized before QWidget

class filesIngest:
  def select_files(self, kind):
    """
    Def for open dialog Select multiple image file
    """
    file_dialog = QFileDialog()
    file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)

    if kind == 'images':
      file_dialog.setNameFilter("Images (*.png *.xpm *.jpg *.jpeg *.gif *.heic *.heif)")
      file_dialog.setWindowTitle("Select images to modify its EXIF timestamps")
    elif kind == 'videos':
      file_dialog.setNameFilter("Videos (*.mp4 *.mov *.avi *.mkv)")
      file_dialog.setWindowTitle("Select images to modify its encoding date and other things")

    file_dialog.setDirectory("/")
    

    if file_dialog.exec():
      self.files = file_dialog.selectedFiles()

  
  def getFileList(self):
    """
    Def for get file list
    """
    return self.files
  



  def getFile_EncodedDate(self, filepath):

    media_info = MediaInfo.parse( convert2raw(filepath) )

    for track in media_info.tracks:
      if track.track_type == 'General':
        datetime_str = track.encoded_date


        # Remove UTC
        datetime_noUTCstr = datetime_str.replace(" UTC", "")
        print('DEBUG: ' + datetime_noUTCstr, end='+++\n')
        # Convert the string to a datetime object
        dtobj_utc = datetime.strptime(datetime_noUTCstr, '%Y-%m-%d %H:%M:%S')


        # Define UTC and MYT timezones
        utc_zone = pytz.utc
        myt_zone = pytz.timezone('Asia/Kuala_Lumpur')
        
        # Localize the datetime object to UTC
        dtobj_utc = utc_zone.localize(dtobj_utc)
        
        # Convert to MYT timezone
        dtobj_myt = dtobj_utc.astimezone(myt_zone)


    return dtobj_myt