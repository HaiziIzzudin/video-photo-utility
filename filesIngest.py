from PySide6.QtWidgets import ( QApplication, QFileDialog, QWidget, QVBoxLayout, QTextEdit, )

app = QApplication([]) # QApplication must be initialized before QWidget

class filesIngest:
  def select_files(self, kind):
    """
    Def for open dialog Select multiple image file
    """
    file_dialog = QFileDialog()
    file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)

    if kind == 'images':
      file_dialog.setNameFilter("Images (*.png *.xpm *.jpg *.jpeg *.gif)")
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