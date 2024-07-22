import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QDragEnterEvent, QDropEvent

class DropWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    
    # window title and window size
    self.setWindowTitle("Drag and Drop File Here")
    self.setGeometry(300, 300, 400, 400)

    # label inside the window
    self.label = QLabel("Drop a file here", self)
    self.label.setAlignment(Qt.AlignCenter)


    layout = QVBoxLayout()
    layout.addWidget(self.label)

    container = QWidget()
    container.setLayout(layout)
    self.setCentralWidget(container)

    self.setAcceptDrops(True)  # Enable drag-and-drop for this window

  def dragEnterEvent(self, event: QDragEnterEvent):
    if event.mimeData().hasUrls(): event.accept()
    else:                          event.ignore()


  def dropEvent(self, event: QDropEvent):
    urls = event.mimeData().urls()
    self.file_paths = [url.toLocalFile() for url in urls]
    
  
  def getFileList(self):
    return self.file_paths
        



app = QApplication(sys.argv)
window = DropWindow()


class dragdrop:
  
  def __init__(self) -> None:
    window.show()
    exit(app.exec())
  
  def getFileList(self):
    return window.file_paths

  