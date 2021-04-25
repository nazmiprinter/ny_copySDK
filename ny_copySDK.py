from PySide2 import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance
from maya import cmds
import maya.OpenMayaUI as omui
import maya.OpenMaya as om

#AUTHOR = Nazmi Yazici
#EMAIL = nazmiprinter@gmail.com
#WEBSITE = nazmiprinter.com
#DATE = 29/08/2019

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class NYcopySDK(QtWidgets.QMainWindow):
    def __init__(self, parent=maya_main_window()):
        self.window_name = 'ny_copySDK_window'
        if cmds.window(self.window_name, exists=True):
            cmds.deleteUI(self.window_name)
        super(NYcopySDK, self).__init__(parent)
        self.setupUi( self )
        self.connectSignals()

    def get_selected(self):
        senderObj = self.sender()
        senderName = senderObj.objectName()
        driver = cmds.ls(sl=True)[0]
        driverAttr = cmds.channelBox('mainChannelBox', q=True, sma=True)
        driverSum = [driver + '.' + x for x in driverAttr][0]
        if senderName.startswith("s"):
            self.source_TB.setText(driverSum)
        else:
            self.destination_TB.setText(driverSum)

    def copy_sdk(self):
        obj_s4 = str(self.obj_s4_TB.text())
        obj_rw = str(self.obj_rw_TB.text())
        attr_s4 = str(self.attr_s4_TB.text())
        attr_rw = str(self.attr_rw_TB.text())
        driverJJ = str(self.source_TB.text())
        newDriv = str(self.destination_TB.text())
        if not driverJJ :
            om.MGlobal.displayWarning('Please select your source driver attribute')
        elif not newDriv:
            om.MGlobal.displayWarning('Please select your destination driver attribute')
        elif not obj_s4:
            om.MGlobal.displayWarning('Please enter a string to search')  
        elif not obj_rw:
            om.MGlobal.displayWarning('Please enter a string to replace')
        else:  
            drivenAttr = []
            ogOuts = []
            dupNews = []
            dupFins = []
            mirrorFirst = []
            newOuts = []

            #INPUT CONNECTIONS OF OG SET DRIVEN KEY CURVES
            connection = cmds.listConnections(driverJJ, scn=True, p=True, s=False, d=True)
            if not connection:
                om.MGlobal.displayWarning("Source driver doesn't have any SDK setup")
            else:

                #GETTING NODE NAMES FROM INPUT DATA
                for div in connection:
                    gel = div.split('.')
                    gel2 = gel[0]
                    drivenAttr.append(gel2)

                #GETTING OUTPUT DATA FROM SOURCE SDK NODES
                for getOut in drivenAttr:
                        ogOut = cmds.listConnections(getOut, scn=True, p=True, s=False, d=True)[0]
                        ogOuts.append(ogOut)
                        
                #DUPLICATING NODES AND RENAMING THEM
                duplicatedNodes = cmds.duplicate(drivenAttr, st=True)
                for delOne in duplicatedNodes:
                    if drivenAttr[-1].isdigit():
                        del2 = delOne.replace(obj_s4, obj_rw)
                        dupRename = cmds.rename(delOne, del2)
                        dupNews.append(dupRename)
                    else:
                        del1 = delOne[:-1]
                        del2 = del1.replace(obj_s4, obj_rw)
                        dupRename = cmds.rename(delOne, del2)
                        dupNews.append(dupRename)

                #REPLACING INPUT DATA FROM OG
                for mf in connection:
                    mfv = mf.replace(obj_s4, obj_rw)
                    mirrorFirst.append(mfv)

                #REPLACING OUTPUT DATA FROM OG
                for ll in ogOuts:
                    newout = ll.replace(obj_s4, obj_rw)
                    newOuts.append(newout)

                for fin in dupNews:
                    dupFin = fin + '.output'
                    dupFins.append(dupFin)

                #CONNECTION FROM NEW DRIVER TO NEW SDK NODES
                for cnn in mirrorFirst:
                    cmds.connectAttr(newDriv, cnn, f=True)

                #IF ATTRIBUTE IS GONNA BE REPLACED, CHANGE THE OUTPUT NAMES
                if attr_s4:
                    newOuts = [mj.replace(attr_s4, attr_rw) for mj in newOuts]

                #CONNECTION TO THE NEW DRIVEN ATTRIBUTES
                for cnn2 in range(len(dupFins)):
                    cmds.connectAttr(dupFins[cnn2], newOuts[cnn2], f=True)

                #IF ATTRIBUTE IS REPLACED, CHANGE THE NODE NAMES
                if attr_s4:
                    renameLast = cmds.listConnections(newOuts, scn=True, p=False, s=True, d=False)
                    for rn in renameLast:
                        nodeRn = rn.replace(attr_s4, attr_rw)
                        cmds.rename(rn, nodeRn)
                om.MGlobal.displayInfo('Job Done!')
    
    def connectSignals(self):
        self.connect(self.source_BTN, QtCore.SIGNAL('released()'), self.get_selected)
        self.connect(self.destination_BTN, QtCore.SIGNAL('released()'), self.get_selected)
        self.connect(self.copy_BTN, QtCore.SIGNAL('released()'), self.copy_sdk)

    def setupUi(self, ny_copySDK_window):
        ny_copySDK_window.setObjectName("ny_copySDK_window")
        ny_copySDK_window.setWindowModality(QtCore.Qt.NonModal)
        ny_copySDK_window.resize(424, 233)
        ny_copySDK_window.setMinimumSize(QtCore.QSize(424, 233))
        ny_copySDK_window.setMaximumSize(QtCore.QSize(424, 233))
        self.centralwidget = QtWidgets.QWidget(ny_copySDK_window)
        self.centralwidget.setMinimumSize(QtCore.QSize(424, 108))
        self.centralwidget.setMaximumSize(QtCore.QSize(424, 16777215))
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(14, 10, 132, 51))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.attrText_LYT = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.attrText_LYT.setContentsMargins(0, 0, 0, 0)
        self.attrText_LYT.setObjectName("attrText_LYT")
        self.source_TXT = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.source_TXT.setObjectName("source_TXT")
        self.attrText_LYT.addWidget(self.source_TXT)
        self.destination_TXT = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.destination_TXT.setObjectName("destination_TXT")
        self.attrText_LYT.addWidget(self.destination_TXT)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(144, 10, 221, 51))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.textBox_LYT = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.textBox_LYT.setContentsMargins(0, 0, 0, 0)
        self.textBox_LYT.setObjectName("textBox_LYT")
        self.source_TB = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.source_TB.setEnabled(True)
        self.source_TB.setReadOnly(True)
        self.source_TB.setObjectName("source_TB")
        self.textBox_LYT.addWidget(self.source_TB)
        self.destination_TB = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.destination_TB.setReadOnly(True)
        self.destination_TB.setObjectName("destination_TB")
        self.textBox_LYT.addWidget(self.destination_TB)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(370, 10, 41, 51))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.setBtn_LYT = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.setBtn_LYT.setContentsMargins(0, 0, 0, 0)
        self.setBtn_LYT.setObjectName("setBtn_LYT")
        self.source_BTN = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.source_BTN.setObjectName("source_BTN")
        self.setBtn_LYT.addWidget(self.source_BTN)
        self.destination_BTN = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.destination_BTN.setEnabled(True)
        self.destination_BTN.setObjectName("destination_BTN")
        self.setBtn_LYT.addWidget(self.destination_BTN)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(40, 190, 351, 25))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.copyButton_LYT = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.copyButton_LYT.setContentsMargins(0, 0, 0, 0)
        self.copyButton_LYT.setObjectName("copyButton_LYT")
        self.copy_BTN = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.copy_BTN.setObjectName("copy_BTN")
        self.copyButton_LYT.addWidget(self.copy_BTN)
        self.drvnObj_LBL = QtWidgets.QLabel(self.centralwidget)
        self.drvnObj_LBL.setGeometry(QtCore.QRect(140, 70, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.drvnObj_LBL.setFont(font)
        self.drvnObj_LBL.setAlignment(QtCore.Qt.AlignCenter)
        self.drvnObj_LBL.setObjectName("drvnObj_LBL")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 90, 401, 41))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.drvnObj_LYT = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.drvnObj_LYT.setContentsMargins(0, 0, 0, 0)
        self.drvnObj_LYT.setObjectName("drvnObj_LYT")
        self.obj_s4_LBL = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.obj_s4_LBL.setObjectName("obj_s4_LBL")
        self.drvnObj_LYT.addWidget(self.obj_s4_LBL)
        self.obj_s4_TB = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.obj_s4_TB.setObjectName("obj_s4_TB")
        self.drvnObj_LYT.addWidget(self.obj_s4_TB)
        self.obj_rw_LBL = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.obj_rw_LBL.setObjectName("obj_rw_LBL")
        self.drvnObj_LYT.addWidget(self.obj_rw_LBL)
        self.obj_rw_TB = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.obj_rw_TB.setObjectName("obj_rw_TB")
        self.drvnObj_LYT.addWidget(self.obj_rw_TB)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(10, 150, 401, 41))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.drvnAttr_LYT = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.drvnAttr_LYT.setContentsMargins(0, 0, 0, 0)
        self.drvnAttr_LYT.setObjectName("drvnAttr_LYT")
        self.attr_s4_LBL = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.attr_s4_LBL.setObjectName("attr_s4_LBL")
        self.drvnAttr_LYT.addWidget(self.attr_s4_LBL)
        self.attr_s4_TB = QtWidgets.QLineEdit(self.horizontalLayoutWidget_3)
        self.attr_s4_TB.setObjectName("attr_s4_TB")
        self.drvnAttr_LYT.addWidget(self.attr_s4_TB)
        self.attr_rw_LBL = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.attr_rw_LBL.setObjectName("attr_rw_LBL")
        self.drvnAttr_LYT.addWidget(self.attr_rw_LBL)
        self.attr_rw_TB = QtWidgets.QLineEdit(self.horizontalLayoutWidget_3)
        self.attr_rw_TB.setObjectName("attr_rw_TB")
        self.drvnAttr_LYT.addWidget(self.attr_rw_TB)
        self.drvnAtr_LBL = QtWidgets.QLabel(self.centralwidget)
        self.drvnAtr_LBL.setGeometry(QtCore.QRect(110, 130, 211, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.drvnAtr_LBL.setFont(font)
        self.drvnAtr_LBL.setAlignment(QtCore.Qt.AlignCenter)
        self.drvnAtr_LBL.setObjectName("drvnAtr_LBL")
        ny_copySDK_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ny_copySDK_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 424, 21))
        self.menubar.setObjectName("menubar")
        ny_copySDK_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ny_copySDK_window)
        self.statusbar.setObjectName("statusbar")
        ny_copySDK_window.setStatusBar(self.statusbar)
        self.retranslateUi(ny_copySDK_window)
        QtCore.QMetaObject.connectSlotsByName(ny_copySDK_window)

    def retranslateUi(self, ny_copySDK_window):
        ny_copySDK_window.setWindowTitle(QtWidgets.QApplication.translate("ny_copySDK_window", "ny_copySDK", None, -1))
        self.source_TXT.setText(QtWidgets.QApplication.translate("ny_copySDK_window", "Source Driver Attribute:", None, -1))
        self.destination_TXT.setText(QtWidgets.QApplication.translate("ny_copySDK_window", "New Driver Attribute:", None, -1))
        self.source_BTN.setText(QtWidgets.QApplication.translate("ny_copySDK_window", "Set", None, -1))
        self.destination_BTN.setText(QtWidgets.QApplication.translate("ny_copySDK_window", "Set", None, -1))
        self.copy_BTN.setText(QtWidgets.QApplication.translate("ny_copySDK_window", "COPY!", None, -1))
        self.drvnObj_LBL.setText(QtWidgets.QApplication.translate("ny_copySDK_window", "Driven Object", None, -1))
        self.obj_s4_LBL.setText(QtWidgets.QApplication.translate("ny_copySDK_window", "Search For:", None, -1))
        self.obj_rw_LBL.setText(QtWidgets.QApplication.translate("ny_copySDK_window", "Replace With:", None, -1))
        self.attr_s4_LBL.setText(QtWidgets.QApplication.translate("ny_copySDK_window", "Search For:", None, -1))
        self.attr_rw_LBL.setText(QtWidgets.QApplication.translate("ny_copySDK_window", "Replace With:", None, -1))
        self.drvnAtr_LBL.setText(QtWidgets.QApplication.translate("ny_copySDK_window", "Driven Attribute (Optional)", None, -1))

def runUI():
    global win
    win = NYcopySDK()
    win.show()

runUI()
