from maya import cmds
import maya.OpenMaya as om
from PySide2 import QtCore, QtWidgets, QtGui
import maya.cmds as cmds
import maya.mel as mel
import sys
import os
import logging
import xml.etree.ElementTree as xml
from cStringIO import StringIO
import pyside2uic as pysideuic
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance

#AUTHOR = Nazmi Yazici
#EMAIL = nazmiprinter@gmail.com
#WEBSITE = vimeo.com/nazmiprinter
#DATE = 29/08/2019


def load_ui_type(uiFile):
    parsed = xml.parse(uiFile)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text

    with open(uiFile, 'r') as f:
        o = StringIO()
        frame = {}

        pysideuic.compileUi(f, o, indent=0)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec pyc in frame

        # Fetch the base_class and form class based on their type in the xml from designer
        form_class = frame['Ui_%s' % form_class]
        base_class = getattr(QtWidgets, widget_class)
    return form_class, base_class

uiFile = '{}/ny_copySDK.ui'.format(os.path.dirname(__file__))
form_class, base_class = load_ui_type(uiFile)

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class ny_copySDKClass(form_class, base_class):
    def __init__(self, parent=maya_main_window()):
        self.window_name = 'ny_copySDK_window'
        if cmds.window(self.window_name, exists=True):
            cmds.deleteUI(self.window_name)

        super(ny_copySDKClass, self).__init__(parent)
        self.setupUi( self )
        #methods
        self.connectSignals()

    def get_selected_src(self, *arg):
        driver = cmds.ls(sl=True)[0]
        driverAttr = cmds.channelBox('mainChannelBox', q=True, sma=True)
        driverSum = [driver + '.' + x for x in driverAttr][0]
        self.source_TB.setText(driverSum)

    def get_selected_dest(self, *arg):
        driver = cmds.ls(sl=True)[0]
        driverAttr = cmds.channelBox('mainChannelBox', q=True, sma=True)
        driverSum = [driver + '.' + x for x in driverAttr][0]
        self.destination_TB.setText(driverSum)

    def copy_sdk(self, *arg):
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
        self.connect(self.source_BTN, QtCore.SIGNAL('released()'), self.get_selected_src)
        self.connect(self.destination_BTN, QtCore.SIGNAL('released()'), self.get_selected_dest)
        self.connect(self.copy_BTN, QtCore.SIGNAL('released()'), self.copy_sdk)
      
def runUI():
    global win
    win = ny_copySDKClass()
    win.show()

runUI()
