### Explanation:
1. **`DropWindow` Class**: 
   - Inherits from `QMainWindow`.
   - Sets up a label and a layout to display drag-and-drop information.
   - Implements `dragEnterEvent` and `dropEvent` to handle drag-and-drop operations.

2. **`dragEnterEvent` Method**:
   - Called when a drag operation enters the window.
   - Accepts the event if the dragged data contains URLs (files).

3. **`dropEvent` Method**:
   - Called when a drop occurs.
   - Extracts the file path from the dropped URL and updates the label and prints the file path.

4. **`main` Function**:
   - Initializes the `QApplication`.
   - Creates and shows the main window.
   - Starts the event loop.