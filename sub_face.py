from distutils.command.config import config
from turtle import back
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import sys
import time
import webbrowser

import home

cancelLoopb=False


#home.update_configfile()
def backup(overwriteold=False):
    linetexttoconfigfile()
    window.lastbackup.setText(home.getdatestring())
    if overwriteold:
        window.logview.insertItem(-1,'backup created'+str(home.getdatestring()))
    else:
        window.logview.insertItem(-1,'overwritten backup'+str(home.getdatestring())
    home.main(overwriteold)

def cancel_loop():
    global cancelLoopb
    cancelLoopb=True
    window.findChild(QtWidgets.QPushButton, "cancelbutton").setEnabled(False)

def selectfolderGameSave():
    dialog = QtWidgets.QFileDialog()
    folderpath=dialog.getExistingDirectory(None, "Select the folder where the save files are.")
    window.findChild(QtWidgets.QLineEdit, "linegamesaver").setText(folderpath+'/')

def selectfolderBackupSave():
    dialog = QtWidgets.QFileDialog()
    folderpath=dialog.getExistingDirectory(None, "Select the folder where you want to save the files.")
    window.findChild(QtWidgets.QLineEdit, "linebackupsaver").setText(folderpath+'/')
def addLista():
    #window.logview.addItem('cebola'+str(home.getdatestring()),-1)
    window.logview.insertItem(-1,'cebola'+str(home.getdatestring()))
def reset():
    linebackupname = window.findChild(QtWidgets.QLineEdit, "labelbackupname")
    linebackupname.setText(home.config['DEFAULT']['backupname'])
    
    window.findChild(QtWidgets.QSpinBox, "spintimedelayset").setValue(int(home.config['DEFAULT']['delay']))

    linebackupname = window.findChild(QtWidgets.QLineEdit, "linegamesaver")
    linebackupname.setText(home.config['DEFAULT']['pathsavefile'])

    linebackupname = window.findChild(QtWidgets.QLineEdit, "linebackupsaver")
    linebackupname.setText(home.config['DEFAULT']['pathbackupfile'])
class Ui(QtWidgets.QDialog):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('base2.xml', self)
        self.show()

        #toolbutton
        self.svsearchbutton = self.findChild(QtWidgets.QToolButton, "gamesavesearch")
        self.baksearchbutton = self.findChild(QtWidgets.QToolButton, "backupsavesearch")
        self.resetbackupfolder = self.findChild(QtWidgets.QToolButton, "resetbackupfolder")
        self.resetbackupfolder.clicked.connect(addLista)

        self.svsearchbutton.clicked.connect(selectfolderGameSave)
        self.baksearchbutton.clicked.connect(selectfolderBackupSave)
        #button
        self.backupbutton = self.findChild(QtWidgets.QPushButton, "backupbutton")
        self.overwritebackupbutton = self.findChild(QtWidgets.QPushButton, "overwriteoldbackupbutton")

        self.buttonbackuploop = self.findChild(QtWidgets.QPushButton, "startloopbutton")
        self.lastbackup = self.findChild(QtWidgets.QLabel, "lastbackup")
        #label
        
        self.backupbutton.clicked.connect(backup)
        self.overwritebackupbutton.clicked.connect(lambda: backup(True))
        self.logview = self.findChild(QtWidgets.QListWidget, "logview")
        self.logview.addItem('cebola')
        #open tread
        self.buttonbackuploop.clicked.connect(self.runLongTask)


        self.findChild(QtWidgets.QPushButton, "cancelbutton").clicked.connect(cancel_loop)
        #dialog
        
        #moreinfo
        self.linkbtn = self.findChild(QtWidgets.QCommandLinkButton, "commandLinkButton")
        self.linkbtn.clicked.connect(lambda: webbrowser.open('https://github.com/edergames29'))
        # Snip...
    def runLongTask(self):
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        # Step 6: Start the thread
        self.thread.start()
        #
        #folder_path = self.dialog.getExistingDirectory(None, "Select Folder")

app = QtWidgets.QApplication(sys.argv)
window = Ui()
reset()
def linetexttoconfigfile():
    home.update_configfile(window.findChild(QtWidgets.QLineEdit, "labelbackupname").text(),
    window.findChild(QtWidgets.QSpinBox, "spintimedelayset").value(),
    window.findChild(QtWidgets.QLineEdit, "linegamesaver").text(),
    window.findChild(QtWidgets.QLineEdit, "linebackupsaver").text())

class Worker(QObject):
    print('Worker')
    finished = pyqtSignal()

    def run(self):
        global cancelLoopb
        window.findChild(QtWidgets.QProgressBar, "progressBar").setValue(100)
        window.findChild(QtWidgets.QPushButton, "backupbutton").setEnabled(False)
        window.findChild(QtWidgets.QPushButton, "startloopbutton").setEnabled(False)
        while True:
            print(cancelLoopb)
            if cancelLoopb:
                'loop cancelado'
                print('loop cancelado')
                window.logview.insertItem(-1,'Loop canceled'+str(home.getdatestring()))
                window.findChild(QtWidgets.QProgressBar, "progressBar").setValue(0)
                window.findChild(QtWidgets.QPushButton, "startloopbutton").setEnabled(True)
                window.findChild(QtWidgets.QPushButton, "backupbutton").setEnabled(True)
                window.findChild(QtWidgets.QPushButton, "cancelbutton").setEnabled(True)
                cancelLoopb=False
                break
            backup()
            time.sleep(10)
            
        self.finished.emit()

def diretoryfoldertomenu():
    pass

app.exec_()
