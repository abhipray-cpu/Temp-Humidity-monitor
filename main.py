from PyQt5 import QtWidgets, uic
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
from threading import Thread
import time
from datetime import datetime
try:
    print(os.environ['DATABASE_URI'])
    # Fetch the service account key JSON file contents
    cred = credentials.Certificate('./configKey.json')
    # Initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(cred, {
        'databaseURL': f"{os.environ['DATABASE_URI']}"
    })
    # declaring the collection objects
    values = db.reference('/values')
    humdityStore = db.reference('/humidity')
    tempcStore = db.reference('/tempC')
    tempfStore = db.reference('/tempF')
    hicStore = db.reference('/hiC')
    hifStore = db.reference('/hiF')
    dewpointStore = db.reference('/dewPoint')
except Exception as e:
    print(e)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        #Load the UI Page
        uic.loadUi('controller.ui', self)
        self.stopThreads=False
        self.setWindowTitle('Room Conditions')
        self.humidityarr = []
        self.temperaturearr = []
        self.heatIndexarr = []
        self.dewPointarr = []
        self.normalStyle = "color:white;font:75 12pt MS Shell Dlg 2;"
        self.underStyle="color:orange;font:75 12pt MS Shell Dlg 2;"
        self.overStyle="color:red;font:75 12pt MS Shell Dlg 2;"




    def updateChart1(self):
        y_axis=[]
        x_axis=[]
        for i in range(1,len(self.humidityarr)+1):
            x_axis.append(i)
        for val in self.humidityarr:
            y_axis.append(val)
        self.humidityPlot.plot(x_axis,y_axis,pen=pg.mkPen('r', width=1))
    def updateChart2(self):
        y_axis = []
        x_axis = []
        for i in range(1,len(self.temperaturearr)+1):
            x_axis.append(i)
        for val in self.temperaturearr:
            y_axis.append(val)
        self.tempPlot.plot(x_axis,y_axis,pen=pg.mkPen('g', width=1))
    def updateChart3(self):
        y_axis = []
        x_axis = []
        for i in range(1,len(self.heatIndexarr)+1):
            x_axis.append(i)
        for val in self.heatIndexarr:
            y_axis.append(val)
        self.hiPlot.plot(x_axis,y_axis,pen=pg.mkPen('b', width=1))
    def updateChart4(self):
        y_axis = []
        x_axis = []
        for i in range(1,len(self.dewPointarr)+1):
            x_axis.append(i)
        for val in self.dewPointarr:
            y_axis.append(val)
        self.dpPlot.plot(x_axis,y_axis,pen=pg.mkPen('m', width=1))


    def updateChart1Util(self):
        while 1 == 1:
            self.updateChart1()
            time.sleep(1)
            if self.stopThreads:
                break
    def updateChart2Util(self):
        while 1 == 1:
            self.updateChart2()
            time.sleep(1)
            if self.stopThreads:
                break
    def updateChart3Util(self):
        while 1 == 1:
            self.updateChart3()
            time.sleep(1)
            if self.stopThreads:
                break
    def updateChart4Util(self):
        while 1 == 1:
            self.updateChart4()
            time.sleep(1)
            if self.stopThreads:
                break

    #this function will add data to the array [{value,timeStamp}] in this format
    def addData(self):
        readings=values.get()
        humVal=readings['humidity']
        tempcVal=readings['tempC']
        tempfVal=readings['tempF']
        hifVal=readings['heatIndexF']
        dpVal=readings['dewPoint']

        #setting style
        if humVal>=50 and humVal<=65:
            self.humidity.setStyleSheet(self.normalStyle)
        elif humVal<50:
            self.humidity.setStyleSheet(self.underStyle)
        else:
            self.humidity.setStyleSheet(self.overStyle)

        if tempcVal>=15 and tempcVal<=35:
            self.tempC.setStyleSheet(self.normalStyle)
        elif tempcVal<15:
            self.tempC.setStyleSheet(self.underStyle)
        else:
            self.tempC.setStyleSheet(self.overStyle)

        if tempfVal>=50 and tempfVal<=100:
            self.tempF.setStyleSheet(self.normalStyle)
        elif tempfVal<50:
            self.tempF.setStyleSheet(self.underStyle)
        else:
            self.tempF.setStyleSheet(self.overStyle)

        if hifVal>=90 and hifVal<=100:
            self.hiF.setStyleSheet(self.normalStyle)
        elif hifVal>100:
            self.hiF.setStyleSheet(self.overStyle)
        elif hifVal<90 and hifVal>80:
            self.hiF.setStyleSheet("color:yellow;font:75 12pt MS Shell Dlg 2;")
        else:
            self.hiF.setStyleSheet(self.underStyle)

        if dpVal>=10 and dpVal<=15:
            self.dp.setStyleSheet(self.normalStyle)
        elif dpVal<10:
            self.dp.setStyleSheet(self.underStyle)
        else:
            self.dp.setStyleSheet(self.overStyle)

        self.humidity.setText(f"{readings['humidity']}")
        self.tempC.setText(f"{readings['tempC']}")
        self.tempF.setText(f"{readings['tempF']}")
        self.hiC.setText(f"{readings['heatIndexC']}")
        self.hiF.setText(f"{readings['heatIndexF']}")
        self.dp.setText(f"{readings['dewPoint']}")
        self.humidityarr.append(readings['humidity'])
        self.temperaturearr.append(readings['tempC'])
        self.heatIndexarr.append(readings['heatIndexC'])
        self.dewPointarr.append(readings['dewPoint'])

    def appendData(self):
        while 1 == 1:
            self.addData()
            time.sleep(1)
            if self.stopThreads:
                break

    #make a seprate thread that will update the data even when the gui is closed

    def createHistory(self):
        while 1 == 1:
            self.createHistoryUtil()
            time.sleep(1)

    def createHistoryUtil(self):
        readings = values.get()
        humVal = readings['humidity']
        tempcVal = readings['tempC']
        tempfVal = readings['tempF']
        hicVal = readings['heatIndexC']
        hifVal = readings['heatIndexF']
        dpVal = readings['dewPoint']

        try:
            humdityStore.push({"value":humVal,'time':f'{datetime.now()}'})
        except Exception as e:
            print(e)
            print('failed to push humidity value')

        try:
            tempcStore.push({"value":tempcVal,'time':f'{datetime.now()}'})
        except Exception as e:
            print(e)
            print('failed to push temperature(C) value')

        try:
            tempfStore.push({"value":tempfVal,'time':f'{datetime.now()}'})
        except Exception as e:
            print(e)
            print('failed to push temperature(F) value')

        try:
            hicStore.push({"value": hicVal, 'time': f'{datetime.now()}'})
        except Exception as e:
            print(e)
            print('failed to push heat index(c) value')

        try:
            hifStore.push({"value": hifVal, 'time': f'{datetime.now()}'})
        except Exception as e:
            print(e)
            print('failed to push heat index(F) value')

        try:
            dewpointStore.push({"value": dpVal, 'time': f'{datetime.now()}'})
        except Exception as e:
            print(e)
            print('failed to push dew point value')








def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.stopThreads=False
    Thread(target=main.appendData).start()
    Thread(target=main.updateChart1Util).start()
    Thread(target=main.updateChart2Util).start()
    Thread(target=main.updateChart3Util).start()
    Thread(target=main.updateChart4Util).start()
    Thread(target=main.show()).start()
    Thread(target=main.createHistory).start()

    sys.exit(exitApp())

def exitApp():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.stopThreads = True
    app.exec_()



if __name__ == '__main__':
    main()