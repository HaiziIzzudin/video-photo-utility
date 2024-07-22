from PySide6.QtWidgets import ( QApplication, QFileDialog, )

app = QApplication([]) # QApplication must be initialized before QWidget

class filesIngest:
  def select_image_file(self):
    """
    Def for open dialog Select multiple image file
    """
    file_dialog = QFileDialog()
    file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
    file_dialog.setNameFilter("Images (*.png *.xpm *.jpg *.jpeg *.gif)")
    file_dialog.setDirectory("/")
    file_dialog.setWindowTitle("Select images to modify its EXIF timestamps")

    if file_dialog.exec():
      self.files = file_dialog.selectedFiles()

  
  def getFileList(self):
    """
    Def for get file list
    """
    return self.files