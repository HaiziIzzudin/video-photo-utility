import sys
import re
import os
import subprocess
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QLineEdit, 
    QFileDialog, QWidget, QTextEdit, QMessageBox, QListWidget, QHBoxLayout, QMenu, QCheckBox
)
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QDragMoveEvent

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("FFmpeg Date Setter")
        self.setGeometry(200, 200, 800, 600)

        self.layout = QVBoxLayout()

        # Widgets
        self.file_list = QListWidget(self)
        self.file_list.setSelectionMode(QListWidget.SingleSelection)
        self.file_list.itemSelectionChanged.connect(self.on_selection_changed)
        self.file_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.file_list.customContextMenuRequested.connect(self.show_context_menu)

        self.file_input = QLineEdit(self)
        self.file_input.setPlaceholderText("Drag and drop files here or click to open")
        self.file_input.setReadOnly(True)
        self.file_input.setAcceptDrops(True)
        self.file_input.dragEnterEvent = self.dragEnterEvent
        self.file_input.dropEvent = self.dropEvent

        self.open_file_button = QPushButton("Open Files", self)
        self.open_file_button.clicked.connect(self.open_file_dialog)

        self.clear_file_list_button = QPushButton("Clear File List", self)
        self.clear_file_list_button.clicked.connect(self.clear_file_list)

        self.date_input = QLineEdit(self)
        self.date_input.setPlaceholderText("YYYY-MM-DD")
        self.date_input.textChanged.connect(self.update_ffmpeg_command)

        self.overwrite_checkbox = QCheckBox("Overwrite Original Files", self)
        self.overwrite_checkbox.setChecked(False)

        self.command_output = QTextEdit(self)
        self.command_output.setReadOnly(True)

        self.execute_current_command_button = QPushButton("Execute FFmpeg Command for Selected File", self)
        self.execute_current_command_button.clicked.connect(self.execute_current_ffmpeg_command)

        self.execute_all_command_button = QPushButton("Execute FFmpeg Command for All Files", self)
        self.execute_all_command_button.clicked.connect(self.execute_all_ffmpeg_commands)

        # Layout
        self.layout.addWidget(self.file_input)
        self.layout.addWidget(self.open_file_button)
        self.layout.addWidget(self.file_list)
        self.layout.addWidget(self.clear_file_list_button)
        self.layout.addWidget(self.date_input)
        self.layout.addWidget(self.overwrite_checkbox)  # Checkbox for overwriting
        self.layout.addWidget(self.command_output)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.execute_current_command_button)
        button_layout.addWidget(self.execute_all_command_button)
        self.layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.files = []
        self.ffmpeg_commands = {}

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dragMoveEvent(self, event: QDragMoveEvent):
        event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path not in self.files:
                    self.files.append(file_path)
                    self.file_list.addItem(file_path)
            self.process_files()

    def open_file_dialog(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        if file_dialog.exec_():
            new_files = file_dialog.selectedFiles()
            for file in new_files:
                if file not in self.files:
                    self.files.append(file)
                    self.file_list.addItem(file)
            self.process_files()

    def clear_file_list(self):
        self.files.clear()
        self.file_list.clear()
        self.ffmpeg_commands.clear()
        self.command_output.clear()
        self.date_input.clear()

    def show_context_menu(self, position: QPoint):
        menu = QMenu(self)
        remove_action = menu.addAction("Remove File")
        remove_action.triggered.connect(self.remove_selected_file)
        menu.exec(self.file_list.mapToGlobal(position))

    def remove_selected_file(self):
        selected_items = self.file_list.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            file_path = selected_item.text()
            self.files.remove(file_path)
            self.file_list.takeItem(self.file_list.row(selected_item))
            self.ffmpeg_commands.pop(file_path, None)
            self.command_output.clear()
            self.date_input.clear()
            self.on_selection_changed()  # Update command display

    def on_selection_changed(self):
        selected_items = self.file_list.selectedItems()
        if selected_items:
            selected_file = selected_items[0].text()
            self.extract_date_from_filename(selected_file)
            self.generate_ffmpeg_command(selected_file)

    def process_files(self):
        self.ffmpeg_commands.clear()
        for file in self.files:
            self.extract_date_from_filename(file)
            self.generate_ffmpeg_command(file)

    def extract_date_from_filename(self, file):
        match = re.search(r'(\d{4})(\d{2})(\d{2})', file)
        if match:
            year, month, day = match.groups()
            date_string = f"{year}-{month}-{day}"
            self.date_input.setText(date_string)

    def update_ffmpeg_command(self):
        selected_items = self.file_list.selectedItems()
        if selected_items:
            selected_file = selected_items[0].text()
            self.generate_ffmpeg_command(selected_file)

    def generate_ffmpeg_command(self, file):
        if not file:
            self.command_output.setText("No file selected.")
            return

        date_string = self.date_input.text()
        if not re.match(r'\d{4}-\d{2}-\d{2}', date_string):
            self.command_output.setText("Invalid date format. Use YYYY-MM-DD.")
            return

        date_time_string = f"{date_string} 00:00:00"  # Time is set to 00:00:00

        tmp_output_file = f"{file.rsplit('.', 1)[0]}_tmp.mp4"
        command = f'ffmpeg -i "{file}" -c copy -metadata creation_time="{date_time_string}" "{tmp_output_file}"'
        self.ffmpeg_commands[file] = command
        if self.file_list.selectedItems() and self.file_list.selectedItems()[0].text() == file:
            self.command_output.setText(command)

    def execute_ffmpeg_command(self, file):
        if file in self.ffmpeg_commands:
            command = self.ffmpeg_commands[file]
            tmp_output_file = f"{file.rsplit('.', 1)[0]}_tmp.mp4"
            try:
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    if self.overwrite_checkbox.isChecked():
                        try:
                            os.remove(file)
                            os.rename(tmp_output_file, file)
                            return f"File '{file}' processed and overwritten successfully."
                        except Exception as e:
                            return f"Error handling file overwrite for '{file}':\n{e}"
                    else:
                        return f"File '{file}' processed successfully. Temporary file created."
                else:
                    return f"Error executing FFmpeg command for '{file}':\n{result.stderr}"
            except Exception as e:
                return f"Exception occurred while processing '{file}':\n{e}"
            finally:
                # Cleanup temp file if not checked to overwrite original
                if not self.overwrite_checkbox.isChecked() and os.path.exists(tmp_output_file):
                    os.remove(tmp_output_file)
        return f"No command found for file '{file}'."

    def execute_current_ffmpeg_command(self):
        selected_items = self.file_list.selectedItems()
        if selected_items:
            selected_file = selected_items[0].text()
            confirmation = QMessageBox.question(self, "Confirm Execution", f"Do you want to execute the FFmpeg command for the selected file '{selected_file}'?", QMessageBox.Yes | QMessageBox.No)
            if confirmation == QMessageBox.Yes:
                message = self.execute_ffmpeg_command(selected_file)
                self.show_info_dialog("FFmpeg Process", message)

    def execute_all_ffmpeg_commands(self):
        confirmation = QMessageBox.question(self, "Confirm Execution", "Do you want to execute the FFmpeg command for all files?", QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            for file in self.files:
                self.execute_ffmpeg_command(file)
            self.show_info_dialog("FFmpeg Process", "All files have been processed successfully.")

    def show_info_dialog(self, title, message):
        QMessageBox.information(self, title, message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
