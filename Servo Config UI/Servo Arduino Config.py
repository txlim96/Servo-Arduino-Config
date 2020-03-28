from tkinter import *
import arduinoComms as com
import time

class ServoArduinoUI(object):
    def __init__(self):
        global connected, changePin, servoState, angleState
        self.master = Tk()
        self.master.bind("<Control-q>", self.exit)
        self.master.minsize(width=700, height=350)
        self.master.config(bg='black')
        self.master.title("Servo Arduino Configuration")
        self.comPort = []
        self.home= {'0': '0', '1':'0', '2':'0', '3':'0'}
        connected = False
        changePin = True
        servoState = 'normal'
        angleState = 'disabled'
        self.frameTop1()
        self.frameTop2()
        self.frameTop3()
        self.frameTop4()
        self.frameTop5()

        self.strReturnHomeText = StringVar()
        self.strReturnHomeText.set("Return home")
        self.btnReturnHome = Button(self.master, highlightbackground='black', fg='white', textvariable=self.strReturnHomeText, command=self.execHome)
        self.btnReturnHome.pack(fill=BOTH, pady=10)

    def exit(self, event):
        com.closeSerial()
        self.master.quit()

    def frameTop1(self):
        self.frame1 = Frame(self.master)
        self.frame1.config(bg='black')

        self.labelCom = Label(self.frame1, text="COM:")
        self.labelCom.config(bg='black', fg='white')
        self.labelCom.pack(side=LEFT)

        self.comString = StringVar()
        self.refresh()
        self.popUpMenu = OptionMenu(self.frame1, self.comString, *self.comPort, command=self.refresh)
        self.popUpMenu.config(bg='black', fg='white')
        self.popUpMenu.pack(side=LEFT)

        self.frameTopSub1()

        self.btnServoPin = StringVar()
        self.btnServoPin.set("Confirm pins")
        self.changePin = Button(self.frame1, wraplength=70, highlightbackground='black', fg='white', textvariable=self.btnServoPin, command=self.changeServoPin)
        self.changePin.pack(side=LEFT, fill=BOTH)
        
        self.frame1.pack(side=TOP, fill=X, padx=150, pady=5)

    def frameTopSub1(self):
        self.subFrame1 = Frame(self.frame1)
        
        self.btnConnectText = StringVar()
        self.btnConnectText.set("Connect")
        self.btnConnect = Button(self.subFrame1, highlightbackground='black', fg='white', textvariable=self.btnConnectText, command=self.connect)
        self.btnConnect.pack(side=TOP, fill=X)

        self.btnRefreshText = StringVar()
        self.btnRefreshText.set("Refresh")
        self.btnRefresh = Button(self.subFrame1, highlightbackground='black', fg='white', textvariable=self.btnRefreshText, command=self.refresh)
        self.btnRefresh.pack(side=TOP, fill=X)

        self.subFrame1.pack(side=LEFT)
        
    def frameTop2(self):
        global servoState
        self.frame2 = Frame(self.master)
        self.frame2.config(bg='black')

        self.frameSpinner(self.frame2, "SERVO", 1)
        self.spinbox1 = Spinbox(self.frame2, values=[3,5,6,9,10,11], width=3, bg='black', fg='white', state=servoState, command=lambda:com.sendData('S', '0', self.spinbox1.get()))
        self.spinbox1.pack(side=LEFT)
        self.frameSpinner(self.frame2, "SERVO", 2)
        self.spinbox2 = Spinbox(self.frame2, values=[3,5,6,9,10,11], width=3, bg='black', fg='white', state=servoState, command=lambda:com.sendData('S', '1', self.spinbox2.get()))
        self.spinbox2.pack(side=LEFT)
        self.frameSpinner(self.frame2, "SERVO", 3)
        self.spinbox3 = Spinbox(self.frame2, values=[3,5,6,9,10,11], width=3, bg='black', fg='white', state=servoState, command=lambda:com.sendData('S', '2', self.spinbox3.get()))
        self.spinbox3.pack(side=LEFT)
        self.frameSpinner(self.frame2, "SERVO", 4)
        self.spinbox4 = Spinbox(self.frame2, values=[3,5,6,9,10,11], width=3, bg='black', fg='white', state=servoState, command=lambda:com.sendData('S', '3', self.spinbox4.get()))
        self.spinbox4.pack(side=LEFT)
        
        self.frame2.pack(side=TOP, fill=X, pady=5)

    def frameTop3(self):
        global angleState
        self.frame3 = Frame(self.master)
        self.frame3.config(bg='black')

        self.frameSpinner(self.frame3, "ANGLE", 1)
        self.spinbox5 = Spinbox(self.frame3, from_=0, to=180, width=3, bg='black', fg='white', state=angleState, command=lambda:com.sendData('', '0', self.spinbox5.get()))
        self.spinbox5.pack(side=LEFT)
        self.frameSpinner(self.frame3, "ANGLE", 2)
        self.spinbox6 = Spinbox(self.frame3, from_=0, to=180, width=3, bg='black', fg='white', state=angleState, command=lambda:com.sendData('', '1', self.spinbox6.get()))
        self.spinbox6.pack(side=LEFT)
        self.frameSpinner(self.frame3, "ANGLE", 3)
        self.spinbox7 = Spinbox(self.frame3, from_=0, to=180, width=3, bg='black', fg='white', state=angleState, command=lambda:com.sendData('', '2', self.spinbox7.get()))
        self.spinbox7.pack(side=LEFT)
        self.frameSpinner(self.frame3, "ANGLE", 4)
        self.spinbox8 = Spinbox(self.frame3, from_=0, to=180, width=3, bg='black', fg='white', state=angleState, command=lambda:com.sendData('', '3', self.spinbox8.get()))
        self.spinbox8.pack(side=LEFT)

        self.frame3.pack(side=TOP, fill=X, pady=5)

    def frameTop4(self):
        self.frame4 = Frame(self.master)
        self.frame4.config(bg='black')

        self.btnServoText = StringVar()
        self.btnServoText.set("Test")
        self.btnServoTest1 = Button(self.frame4, highlightbackground='black', fg='white', textvariable=self.btnServoText, command=lambda:com.sendData(mode='T', val='0'))
        self.btnServoTest1.pack(side=LEFT, fill=X, expand=True, padx=20)
        self.btnServoTest2 = Button(self.frame4, highlightbackground='black', fg='white', textvariable=self.btnServoText, command=lambda:com.sendData(mode='T', val='1'))
        self.btnServoTest2.pack(side=LEFT, fill=X, expand=True, padx=20)
        self.btnServoTest3 = Button(self.frame4, highlightbackground='black', fg='white', textvariable=self.btnServoText, command=lambda:com.sendData(mode='T', val='2'))
        self.btnServoTest3.pack(side=LEFT, fill=X, expand=True, padx=20)
        self.btnServoTest4 = Button(self.frame4, highlightbackground='black', fg='white', textvariable=self.btnServoText, command=lambda:com.sendData(mode='T', val='3'))
        self.btnServoTest4.pack(side=LEFT, fill=X, expand=True, padx=20)
        
        self.frame4.pack(side=TOP, fill=X, pady=10)

    def frameTop5(self):
        self.frame5 = Frame(self.master)
        self.frame5.config(bg='black')

        self.strSetHomeText = StringVar()
        self.strSetHomeText.set("Set home")
        self.btnSetHome1 = Button(self.frame5, highlightbackground='black', fg='white', textvariable=self.strSetHomeText, command=lambda:self.setHome('0', self.spinbox5.get()))
        self.btnSetHome1.pack(side=LEFT, fill=X, expand=True, padx=20)
        self.btnSetHome2 = Button(self.frame5, highlightbackground='black', fg='white', textvariable=self.strSetHomeText, command=lambda:self.setHome('1', self.spinbox6.get()))
        self.btnSetHome2.pack(side=LEFT, fill=X, expand=True, padx=20)
        self.btnSetHome3 = Button(self.frame5, highlightbackground='black', fg='white', textvariable=self.strSetHomeText, command=lambda:self.setHome('2', self.spinbox7.get()))
        self.btnSetHome3.pack(side=LEFT, fill=X, expand=True, padx=20)
        self.btnSetHome4 = Button(self.frame5, highlightbackground='black', fg='white', textvariable=self.strSetHomeText, command=lambda:self.setHome('3', self.spinbox8.get()))
        self.btnSetHome4.pack(side=LEFT, fill=X, expand=True, padx=20)
        
        self.frame5.pack(side=TOP, fill=X)

    def frameSpinner(self, frame, string, idx):
        self.labelSpinner = Label(frame, text=string+' '+str(idx))
        self.labelSpinner.config(bg='black', fg='white')
        self.labelSpinner.pack(side=LEFT, fill=X, expand=True)

    def setHome(self, num, v):
        self.home[num] = str(v)
        com.sendData(idx=num, val=str(v));

    def execHome(self):
        for i in range(4):
            com.sendData(idx=str(i), val=self.home[str(i)])
            time.sleep(1)

    def changeServoPin(self):
        global connected, changePin, servoState, angleState
        try:
            if changePin is False:
                servoState = 'normal'
                angleState = 'disabled'
                self.btnServoPin.set("Confirm pins")
            else:
                servoState = 'disabled'
                angleState = 'normal'
                self.btnServoPin.set("Change servo pins")
                
            changePin = not changePin
            self.spinbox1.config(state=servoState)
            self.spinbox2.config(state=servoState)
            self.spinbox3.config(state=servoState)
            self.spinbox4.config(state=servoState)
            self.spinbox5.config(state=angleState)
            self.spinbox6.config(state=angleState)
            self.spinbox7.config(state=angleState)
            self.spinbox8.config(state=angleState)
            
        except Exception as e:
            print(e)
            pass

    def connect(self):
        global connected
        try:
            if self.comPort != []:
                if connected is False:
                    print('Connected')
                    port = self.comString.get()
                    com.setupSerial(port)
                    connected = True        # send pin attach code here
                    self.btnConnectText.set('Disconnect')
                    self.master.title('Servo Arduino Configuration-Connected to '+port)
                    com.sendData()
                    time.sleep(1)       # buffer period
                    com.sendData('S', '0', self.spinbox1.get())
                    time.sleep(1)
                    com.sendData('S', '1', self.spinbox2.get())
                    time.sleep(1)
                    com.sendData('S', '2', self.spinbox3.get())
                    time.sleep(1)
                    com.sendData('S', '3', self.spinbox4.get())
                else:
                    print('Disconnected')
                    com.closeSerial()
                    connected = False
                    self.btnConnectText.set('Connect')
                    self.master.title('Servo Arduino Configuration')
        except Exception as e:
            print(e)
            print('Port unavailable. Please refresh!')
            pass
        
    def refresh(self):
        self.comPort = com.listSerialPorts()
##        print(self.comPort)
        try:
            self.btnConnect.config(state=NORMAL)
            if self.comPort == []:
                self.btnConnect.config(state=DISABLED)
        except:
            pass
        if self.comPort == []:
            self.comPort = [""]
        self.comString.set(self.comPort[0])
        try:
            menu = self.popUpMenu["menu"]
            menu.delete(0, "end")
            for option in self.comPort:
                menu.add_command(label=option, command=lambda val=option:self.comString.set(val))
        except:
            pass

if __name__ == "__main__":
    servoUI = ServoArduinoUI()
    servoUI.master.mainloop()
