import sys
import PyQt6.QtCore as qtCore
import PyQt6.QtWidgets as qtWidgets
import PyQt6.QtGui as qtGui
import cleaner as cl


class App(qtWidgets.QMainWindow):

    def __init__(self):
        
        super().__init__()

        centralWidget = qtWidgets.QWidget()
        self.setCentralWidget(centralWidget)

        self.setWindowTitle("Cleaner")
        self.setGeometry(100,100,800,400)

        self.setAcceptDrops(True)
        self.files = []

        self.dropLabel = qtWidgets.QLabel()
        self.dropLabel.setWordWrap(True)
        self.dropLabel.setAlignment(qtCore.Qt.AlignmentFlag.AlignCenter)

        font = qtGui.QFont()
        font.setPointSize(18)
        self.dropLabel.setFont(font)

        self.cleanButton = qtWidgets.QPushButton("Clean", self)
        self.cleanButton.clicked.connect(self.cleaning)

        self.mergeButton = qtWidgets.QPushButton("Merge", self)
        self.mergeButton.clicked.connect(self.merging)
        self.mergeButton.setEnabled(False)

        self.deteleEmptyRow = qtWidgets.QPushButton("Detele Empty Row", self)
        self.deteleEmptyRow.clicked.connect(self.deleting)

        principalLayout = qtWidgets.QVBoxLayout()
        principalLayout.addWidget(self.dropLabel)
        principalLayout.addStretch()

        bottomLayout = qtWidgets.QHBoxLayout()
        bottomLayout.addWidget(self.cleanButton)
        bottomLayout.addWidget(self.mergeButton)
        bottomLayout.addWidget(self.deteleEmptyRow)

        principalLayout.addLayout(bottomLayout)
        centralWidget.setLayout(principalLayout)

        self.createTopMenu()
        self.set_idle_style()  

    def createTopMenu(self):

        fileActions, helpActions = [], []

        menuBar = self.menuBar()
        menuFile = menuBar.addMenu("File")

        cleanAction = qtGui.QAction("Clean", self)
        cleanAction.triggered.connect(self.cleaning)
        fileActions.append(cleanAction)

        mergeAction = qtGui.QAction("Merge", self)
        mergeAction.triggered.connect(self.merging)
        fileActions.append(mergeAction)

        deleteRowAction = qtGui.QAction("Delete Row", self)
        deleteRowAction.triggered.connect(self.deleting)
        fileActions.append(deleteRowAction)

        quitAction = qtGui.QAction("Quit", self)
        quitAction.setShortcut("Ctrl+Q")
        quitAction.triggered.connect(self.close)
        fileActions.append(quitAction)

        for action in fileActions:
            menuFile.addAction(action)

        helpMenu = menuBar.addMenu("Help")

        cleanAbout = qtGui.QAction("About Clean", self)
        cleanAbout.triggered.connect(self.aboutClean)
        helpActions.append(cleanAbout)

        mergeAbout = qtGui.QAction("About Merge", self)
        mergeAbout.triggered.connect(self.aboutMerge)
        helpActions.append(mergeAbout)

        deleteRowAbout = qtGui.QAction("About Detele Row", self)
        deleteRowAbout.triggered.connect(self.aboutDeleteRow)
        helpActions.append(deleteRowAbout)

        for action in helpActions:
            helpMenu.addAction(action)

    def set_idle_style(self):
        
        self.dropLabel.setText("Drop files here (CSV, XLSX)")
        self.dropLabel.setStyleSheet("""
        QLabel {
            border: 1px dashed palette(mid);
            border-radius: 6px;
            color: palette(text);
            background-color: palette(base);
        }
    """)

    def set_drag_style(self):

        self.dropLabel.setStyleSheet("""
        QLabel {
            border: 1px solid palette(highlight);
            border-radius: 6px;
            color: palette(highlight);
            background-color: palette(base);
        }
    """)

    def set_filled_style(self):

        self.dropLabel.setStyleSheet("""
        QLabel {
            border: none;
            color: palette(text);
            background-color: palette(base);
        }
    """)

    def aboutClean(self):

        qtWidgets.QMessageBox.information(
            self,
            "Clean",
            "Cleans and standardizes a data file (CSV or Excel)."
        )

    def aboutDeleteRow(self):

        qtWidgets.QMessageBox.information(
            self,
            "Delete Row",
            ""
        )

    def aboutMerge(self):

        qtWidgets.QMessageBox.information(
            self,
            "Merge",
            "Merges two data files into a single dataset."
        )

    def cleaning(self):

        if not self.files:
            self.dropLabel.setText("Drop files here (CSV, XLSX)")
            return
        
        for file in self.files :
            file_path = file
            cl.clean(file_path)

        self.dropLabel.setText(f"Cleaning:\n{self.files[0]}")

    def merging(self):

        self.dropLabel.setText(
            "Merging files:\n" + "\n".join(self.files)
        )

        cl.merge(self.files[0],self.files[1])

    def deleting(self):
        self.dropLabel.setText("Deleting empty rows")

    def dragEnterEvent(self, event):

        if event.mimeData().hasUrls():
            self.set_drag_style()
            event.acceptProposedAction()

    def dragLeaveEvent(self, event):

        if not self.files:
            self.set_idle_style()

    def dropEvent(self, event):

        self.files = [
            url.toLocalFile()
            for url in event.mimeData().urls()
            if url.toLocalFile().lower().endswith((".csv", ".xlsx"))

        ]

        if not self.files:
            self.set_idle_style()
            return

        self.set_filled_style()
        self.dropLabel.setText("\n".join(self.files))
        self.mergeButton.setEnabled(len(self.files) >= 2)
        self.cleanButton.setEnabled(not(len(self.files) >= 2))
    


if __name__ == "__main__":
    app = qtWidgets.QApplication(sys.argv)
    fenetre = App()
    fenetre.show()
    sys.exit(app.exec())