from PySide6.QtWidgets import ( QApplication, QFileDialog, QWidget, QVBoxLayout, QTextEdit, )
from colorama import Fore, Style


from colorama import Fore, Style, just_fix_windows_console
just_fix_windows_console()
MAGENTA = Fore.LIGHTMAGENTA_EX
RED = Fore.RED
RESET = Style.RESET_ALL


app = QApplication([]) # QApplication must be initialized before QWidget
exiftool_location = r"C:\Program Files\XnViewMP\AddOn"


class filesIngest:
  def select_files(self, kind):
    """
    Def for open dialog Select multiple image file
    """
    file_dialog = QFileDialog()
    file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)

    if kind.lower() == 'i':
      file_dialog.setNameFilter("Images (*.png *.xpm *.jpg *.jpeg *.gif *.heic *.heif *.webp)")
      file_dialog.setWindowTitle("Select images to modify its EXIF timestamps")
    elif kind.lower() == 'v':
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
  



  
  


if __name__ == '__main__':
  for i in range(0, 5):
    print(RED, '!!! DEBUGGING MODE !!!', RESET)

  # please input file url here
  filepath = r"E:\ChatExport_2024-09-03\photos\photo_1@03-07-2022_03-37-57.jpg"
  kind = 'images' # images | videos

  fi = filesIngest()
  dateobj = fi.getFile_EncodedDate(filepath, kind)

  print(dateobj)