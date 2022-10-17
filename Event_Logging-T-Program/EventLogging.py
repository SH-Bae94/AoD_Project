from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtTest import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from vars import *
from pyproj import Proj
import os
import sys
import socket 
import datetime
import openpyxl

dirName = os.path.dirname(os.path.realpath(__file__))
form_class = uic.loadUiType(os.path.join(dirName,"eventLogging.ui"))[0]

recvSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recvSock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
recvSock.bind(("",60880))

sockToAI = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

class WindowClass(QMainWindow,QWidget, form_class):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)

        self.AI_ip = '192.168.0.103'
        self.AI_port = 9999

        self.NaviFlag = True

        NaviData.RawDataBrowser = self.rawDataBrowser
        NaviData.TimeBrowser = self.timelineEdit
        NaviData.LatBrowser = self.latlineEdit
        NaviData.LonBrowser = self.lonlineEdit
        NaviData.DepthBrowser = self.depthlineEdit
        NaviData.AltiBrowser = self.altilineEdit
        NaviData.EventInputEdit = self.eventInputEdit

        self.eventInputButton.clicked.connect(self.eventSave)
        NaviData.EventInputEdit.editingFinished.connect(self.eventSave)

        RecvThread = RECVTHREAD(parent = self)
        RecvThread.start()

    def run(self):
        pass

    def eventSave(self):
        now = datetime.datetime.now()
        NaviData.ListNaviData[5] = NaviData.EventData
        self.OutputData_Time     = NaviData.ListNaviData[0]
        self.OutputData_Lat      = NaviData.ListNaviData[1]
        self.OutputData_Lon      = NaviData.ListNaviData[2]
        self.OutputData_Depth    = NaviData.ListNaviData[3]
        self.OutputData_Alti     = NaviData.ListNaviData[4]
        self.OutputData_Event     = NaviData.ListNaviData[5]
        
        if len(self.OutputData_Event) != 0:
            self.eventOutput()
            self.saveText()
            self.saveExcel()
            data = now.strftime('%Y_%m_%d %H_%M_%S')
            data = sockToAI.sendto(data.encode(),(self.AI_ip, self.AI_port))
            NaviData.EventInputEdit.clear()
    
    def eventOutput(self):
        self.OutputList = NaviData.ListNaviData
        self.OutputData = ("Time : {}   Lat : {}    Lon : {}    Depth : {}  Alti : {}   Event : {}".format(self.OutputData_Time, round(float(self.OutputData_Lat), 5), round(float(self.OutputData_Lon), 5),
                                                                                                     self.OutputData_Depth, self.OutputData_Alti, self.OutputData_Event))
        self.eventOutputBrowser.append(self.OutputData)

    def saveText(self):
        now = datetime.datetime.now()
        file = os.path.join(dirName, "Log","{}.txt".format(now.strftime('%Y_%m_%d_%H')))
        head = ("{},{},{},{},{},{}".format("Time", "Latitude", "Longitude", "Depth", "Altitude", "Event"))
        data = ("{},{},{},{},{},{}".format(self.OutputList[0], self.OutputList[1], self.OutputList[2],
                                           self.OutputList[3], self.OutputList[4], self.OutputList[5]))
        if os.path.isfile(file):
            self.textfilecheckFlag = True
        else :
            self.textfilecheckFlag = False

        with open(os.path.join(dirName, "Log","{}.txt".format(now.strftime('%Y_%m_%d_%H'))), "a") as f:
            if self.textfilecheckFlag == False:
                f.write(head+"\n")
            f.write(data+"\n")
    
    def saveExcel(self):
        now = datetime.datetime.now()
        file = os.path.join(dirName, "Log","{}.xlsx".format(now.strftime('%Y_%m_%d_%H')))
        head = ["Time", "Latitude", "Longitude", "Depth", "Altitude", "Event"]

        if os.path.isfile(file):
            self.excelfilecheckFlag = True
        else :
            self.excelfilecheckFlag = False
        
        if self.excelfilecheckFlag == False:
            wb = openpyxl.Workbook()
            sheet = wb.active
            sheet.append(head)
        else:
            wb = openpyxl.load_workbook(file)
            sheet = wb.active
        sheet.append(self.OutputList)
        wb.save(file)

class RECVTHREAD(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        while True:
            NaviData.TmpData, addr =  recvSock.recvfrom(4096)
            self.USBL_data = NaviData.TmpData.decode()
            self.CapturedData(self.USBL_data)
            self.setNaviData()
            self.setEvent()
            NaviData.RawDataBrowser.append(self.USBL_data)
            QTest.qWait(50)

    def CapturedData(self, USBL_data):
        captureData = USBL_data
        self.ParsingUSBLRedoneOP(captureData)
        
    def ParsingUSBLRedoneOP(self, msg):
        myProj = Proj(proj='utm', zone=R1_OP.Zone, ellps='WGS84', preserve_units=False)
        msgList = msg.split(" ")

        INGLL.rov_UTM_X        = float(msgList[98])
        INGLL.rov_UTM_Y        = float(msgList[99])
        INGLL.rov_lonDeg, INGLL.rov_latDeg = myProj(INGLL.rov_UTM_X, INGLL.rov_UTM_Y, inverse = True)
        PSIMSSB.rov_depth      = float(msgList[100])
        PSIMSNS.rov_Heading    = float(msgList[101])
        PSIMSNS.rov_Pitch      = float(msgList[102])
        PSIMSNS.rov_Roll       = float(msgList[103])

    def setNaviData(self):
        # self.clearNaviData()
        now = datetime.datetime.now()
        NaviData.TimeBrowser.setText(now.strftime('%Y-%m-%d %H:%M:%S'))
        NaviData.LatBrowser.setText(str(INGLL.rov_latDeg))
        NaviData.LonBrowser.setText(str(INGLL.rov_lonDeg))
        NaviData.DepthBrowser.setText(str(PSIMSSB.rov_depth))
        # self.altiBrowser.append()
        NaviData.ListNaviData[0] = now.strftime('%Y-%m-%d %H:%M:%S')
        NaviData.ListNaviData[1] = str(INGLL.rov_latDeg)
        NaviData.ListNaviData[2] = str(INGLL.rov_lonDeg)
        NaviData.ListNaviData[3] = str(PSIMSSB.rov_depth)
        # NaviData.ListNaviData[4] = 

    def clearNaviData(self):
        NaviData.TimeBrowser.clear()
        NaviData.LatBrowser.clear()
        NaviData.LonBrowser.clear()
        NaviData.DepthBrowser.clear()

    def setEvent(self):
        NaviData.EventData = NaviData.EventInputEdit.text()

# Main 함수
if __name__ =='__main__':
    app = 0
    app = QApplication(sys.argv)
    mywindows = WindowClass()
    mywindows.show()
    app.exec_()        