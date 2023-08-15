from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
import interface
import os


class Player(QtWidgets.QMainWindow, interface.Ui_MainWindow):
    def __init__(self):
        super(Player, self).__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.play)
        self.pushButton_2.clicked.connect(self.stop)
        self.listWidget.itemDoubleClicked.connect(self.play)
        self.pushButton_3.clicked.connect(self.load)

        self.dir = ""
        self.mediaPlayer = QtMultimedia.QMediaPlayer()
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)

        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon("item.ico"))

        self.current_item_index = 0  # Индекс текущей выбранной песни

    def play(self):
        item = self.listWidget.currentItem()

        if item:
            index = self.listWidget.row(item)
            file_name = os.path.join(self.dir, item.text())
            content = QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(file_name))

            if self.mediaPlayer.state() == QtMultimedia.QMediaPlayer.PlayingState:
                self.mediaPlayer.stop()

            self.mediaPlayer.setMedia(content)
            self.mediaPlayer.play()

    def stop(self):
        self.mediaPlayer.stop()

    def load(self):
        self.listWidget.clear()

        dir = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory")

        if dir:
            for file_name in os.listdir(dir):
                if file_name.endswith(".mp3"):
                    self.listWidget.addItem(file_name)
            self.dir = dir

    def mediaStateChanged(self, state):
        if state == QtMultimedia.QMediaPlayer.StoppedState:
            self.current_item_index += 1
            if self.current_item_index < self.listWidget.count():
                self.listWidget.setCurrentRow(self.current_item_index)
                self.play()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    player = Player()
    player.show()
    app.exec_()
