import sys
import PyQt6.QtCore as qtCore
import PyQt6.QtWidgets as qtWidgets
import PyQt6.QtGui as qtGui
import cleaner as cl


class ProcessWorker(qtCore.QThread):
    """
    Worker thread used to run long processes
    and update the progress bar without freezing the UI.
    """

    progress = qtCore.pyqtSignal(int)
    finished = qtCore.pyqtSignal(str)

    def __init__(self, mode, files, savePath):

        super().__init__()
        self.mode = mode
        self.files = files
        self.savePath = savePath

    def run(self):
        """
        Executes the selected processing mode.
        """

        if self.mode == "clean":
            total = len(self.files)

            for i, filePath in enumerate(self.files, start=1):
                cl.clean(filePath, self.savePath)

                percent = int((i / total) * 100)
                self.progress.emit(percent)

            self.finished.emit("Cleaning finished !")

        elif self.mode == "merge":
            self.progress.emit(10)

            cl.merge(self.files[0], self.files[1], self.savePath)

            self.progress.emit(100)
            self.finished.emit("Merge finished !")

class App(qtWidgets.QMainWindow):

    def __init__(self):
        
        super().__init__()

        # Main window setup
        centralWidget = qtWidgets.QWidget()
        self.setCentralWidget(centralWidget)

        self.setWindowTitle("Cleaner")
        self.setGeometry(100,100,800,400)

        # Main window setup
        self.setAcceptDrops(True)
        self.files = []

        # Drag & drop label
        self.dropLabel = qtWidgets.QLabel()
        self.dropLabel.setWordWrap(True)
        self.dropLabel.setAlignment(qtCore.Qt.AlignmentFlag.AlignCenter)

        font = qtGui.QFont()
        font.setPointSize(18)
        self.dropLabel.setFont(font)

        # Buttons
        self.cleanButton = qtWidgets.QPushButton("Clean", self)
        self.cleanButton.clicked.connect(self.cleaning)

        self.mergeButton = qtWidgets.QPushButton("Merge", self)
        self.mergeButton.clicked.connect(self.merging)
        self.mergeButton.setEnabled(False)

        # Buttons
        principalLayout = qtWidgets.QVBoxLayout()
        principalLayout.addWidget(self.dropLabel)
        principalLayout.addStretch()

        # Progress bar
        self.progressBar = qtWidgets.QProgressBar()
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)
        self.progressBar.setVisible(False)

        principalLayout.addWidget(self.progressBar)

        bottomLayout = qtWidgets.QHBoxLayout()
        bottomLayout.addWidget(self.cleanButton)
        bottomLayout.addWidget(self.mergeButton)

        principalLayout.addLayout(bottomLayout)
        centralWidget.setLayout(principalLayout)

        # Menu and initial UI state
        self.createTopMenu()
        self.setIdleStyle()  

    def createTopMenu(self):
        """
        Creates the top menu bar.
        """

        fileActions = []

        menuBar = self.menuBar()
        menuFile = menuBar.addMenu("File")

        cleanAction = qtGui.QAction("Clean", self)
        cleanAction.triggered.connect(self.cleaning)
        fileActions.append(cleanAction)

        mergeAction = qtGui.QAction("Merge", self)
        mergeAction.triggered.connect(self.merging)
        fileActions.append(mergeAction)


        quitAction = qtGui.QAction("Quit", self)
        quitAction.setShortcut("Ctrl+Q")
        quitAction.triggered.connect(self.close)
        fileActions.append(quitAction)

        for action in fileActions:
            menuFile.addAction(action)

    def setIdleStyle(self):
        """
        Style applied when no files are loaded.
        """
        
        self.dropLabel.setText("Drop files here (CSV, XLSX)")
        self.dropLabel.setStyleSheet("""
        QLabel {
            border: 1px dashed palette(mid);
            border-radius: 6px;
            color: palette(text);
            background-color: palette(base);
        }
    """)

    def setDragStyle(self):
        """
        Style applied when dragging files over the window.
        """

        self.dropLabel.setStyleSheet("""
        QLabel {
            border: 1px solid palette(highlight);
            border-radius: 6px;
            color: palette(highlight);
            background-color: palette(base);
        }
    """)

    def setFilledStyle(self):
        """
        Style applied when files have been dropped.
        """

        self.dropLabel.setStyleSheet("""
        QLabel {
            border: none;
            color: palette(text);
            background-color: palette(base);
        }
    """)

    def cleaning(self):
        """
        Starts the cleaning process.
        """

        if not self.files:
            return

        savePath, _ = qtWidgets.QFileDialog.getSaveFileName(
            self,
            "Exporter le fichier nettoyé",
            "cleaned_file.csv",
            "CSV (*.csv);;Excel (*.xlsx)"
        )

        if not savePath:
            return

        self.startWorker("clean", savePath)

    def merging(self):
        """
        Starts the merge process.
        """

        if len(self.files) < 2:
            return

        savePath, _ = qtWidgets.QFileDialog.getSaveFileName(
        self,
        "Exporter le fichier fusionné",
        "merged_file.csv",
        "CSV (*.csv);;Excel (*.xlsx)"
        )

        if not savePath:
            return

        self.startWorker("merge", savePath)

    def dragEnterEvent(self, event):
        """
        Triggered when files are dragged into the window.
        """

        if event.mimeData().hasUrls():
            self.setDragStyle()
            event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        """
        Triggered when dragged files leave the window.
        """

        if not self.files:
            self.setIdleStyle()

    def dropEvent(self, event):
        """
        Triggered when files are dropped into the window.
        """

        new_files = [
            url.toLocalFile()
            for url in event.mimeData().urls()
            if url.toLocalFile().lower().endswith((".csv", ".xlsx"))
        ]

        for f in new_files:
            if f not in self.files:
                self.files.append(f)

        if not self.files:
            self.setIdleStyle()
            return

        self.updateFileDisplay()
    
    def processFinished(self, message):
        """
        Called when the worker thread finishes.
        """

        self.progressBar.setVisible(False)
        self.cleanButton.setEnabled(True)
        self.mergeButton.setEnabled(len(self.files) >= 2)
        self.dropLabel.setText(message)
    
    def startWorker(self, mode, savePath):
        """
        Starts the background worker thread.
        """

        self.progressBar.setValue(0)
        self.progressBar.setVisible(True)
        self.cleanButton.setEnabled(False)
        self.mergeButton.setEnabled(False)

        self.worker = ProcessWorker(mode, self.files, savePath)
        self.worker.progress.connect(self.progressBar.setValue)
        self.worker.finished.connect(self.processFinished)
        self.worker.start()

    def updateFileDisplay(self):
        """
        Updates the label with the list of loaded files.
        """

        self.setFilledStyle()
        self.dropLabel.setText("\n".join(self.files))
        self.mergeButton.setEnabled(len(self.files) >= 2)
    
def launchApp():
    app = qtWidgets.QApplication(sys.argv)
    fenetre = App()
    fenetre.show()
    sys.exit(app.exec())