import sys
from pathlib import Path

from ebooklib import epub
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QSplitter,
    QTextEdit,
    QToolBar,
    QWidget,
)


class Peebook(QMainWindow):
    def __init__(self):
        super().__init__()

        # sets main window config
        self.setWindowTitle("Peebook")
        self.setGeometry(100, 100, 800, 600)

        # sets main widget config
        widget = QWidget()
        self.setCentralWidget(widget)

        # sets vertical layout config
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        widget.setLayout(layout)

        # creates the toolbar
        toolbar = QToolBar("Toolbar")
        toolbar.setMovable(False)  # makes tollbar fixed
        self.addToolBar(toolbar)

        # ceates the actions
        openFile = QAction("Open", self)
        openFile.setStatusTip("Opens ebook file")
        openFile.triggered.connect(self.open_file)

        up_sync = QAction("Upload", self)
        up_sync.setStatusTip("Sync up with dropbox")

        down_sync = QAction("Download", self)
        down_sync.setStatusTip("Sync down from dropbox ")

        exit_action = QAction("Exit", self)
        exit_action.setStatusTip("Exit the application")
        exit_action.triggered.connect(QApplication.instance().quit)

        # add actions to toolbar
        toolbar.addAction(openFile)
        toolbar.addAction(up_sync)
        toolbar.addAction(down_sync)
        toolbar.addAction(exit_action)

        # creates the QListWidget
        self.lista = QListWidget()
        # self.lista.setStyleSheet(
        #    """
        # background-color: #262626;
        # color: #FFFFFF;
        # """
        # )
        self.lista.setMinimumWidth(60)

        # lista.currentItemChanged.connect(lambda item: texto.setText(item.text()))
        self.lista.itemClicked.connect(lambda item: self.texto.setText(item.text()))
        # layout.addWidget(lista)

        # creates the QTextEdit
        self.texto = QTextEdit()
        self.texto.setText("<html><body><h1>Welcome to Peebook!</h1></body></html>")
        # layout.addWidget(texto)

        # Cria o Splitter
        mySplitter = QSplitter()
        mySplitter.addWidget(self.lista)
        mySplitter.addWidget(self.texto)
        mySplitter.setStretchFactor(0, 2)
        mySplitter.setStretchFactor(1, 8)
        mySplitter.setHandleWidth(1)
        layout.addWidget(mySplitter)

        # creates the status bar
        self.statusbar = self.statusBar()
        self.statusbar.showMessage("Peebook 0.1")

    def open_file(self):
        home_dir = str(Path.home())
        fname = QFileDialog.getOpenFileName(
            self,
            "Open file...",
            home_dir,
            "ePub files (*.epub);;Amazon Kindle files (*.azw);;PDF files (*.pdf)",
        )
        if fname[0]:
            with open(fname[0], "r") as f:
                book = epub.read_epub(f.name)
            self.statusbar.showMessage(f.name)
            self.lista.clear()
            print(dir(book))
            for item in book.toc:
                if item.title:
                    list_item = QListWidgetItem(item.title)
                    self.lista.addItem(list_item)
                print(f"Book chapter UID: {item.title}")
                print(f"Book chapter title: {item.uid}")
                # self.lista.addItem(title)


if __name__ == "__main__":
    # creates application
    app = QApplication(sys.argv)

    # creates the window
    peebookwindow = Peebook()

    # shows the window
    peebookwindow.show()

    # executes the application
    sys.exit(app.exec())
