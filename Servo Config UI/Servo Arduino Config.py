from tkinter import *
import arduinoComms as com
import time

class ServoArduinoUI(object):
    def __init__(self):
        global connected
        self.master = Tk()
        self.master.bind("<Control-q>", self.exit)
        self.master.minsize(width=600, height=350)
        self.master.config(bg='black')
        self.master.title("Servo Arduino Configuration")
        self.comPort = []
        self.spinbox = []
        connected = False
        self.frameTop1()
        self.frameTop2()
        self.frameTop3()
        self.frameTop4()

    def exit(self, event):
        com.closeSerial()
        self.master.quit()

    def frameTop1(self):
        self.frame1 = Frame(self.master)
        self.frame1.config(width=20, height=1, bg='black')

        self.labelCom = Label(self.frame1, text="COM:")
        self.labelCom.config(bg='black', fg='white')
        self.labelCom.pack(side=LEFT)

        self.comString = StringVar()
        self.refresh()
        self.popUpMenu = OptionMenu(self.frame1, self.comString, *self.comPort, command=self.refresh)
        self.popUpMenu.config(bg='black', fg='white')
        self.popUpMenu.pack(side=LEFT)

        self.btnConnectText = StringVar()
        self.btnConnectText.set("Connect")
        self.connect = Button(self.frame1, width=10, highlightbackground='black', fg='white', textvariable=self.btnConnectText, command=self.connect)
        self.connect.pack(side=TOP)

        self.btnRefreshText = StringVar()
        self.btnRefreshText.set("Refresh")
        self.refresh = Button(self.frame1, width=10, highlightbackground='black', fg='white', textvariable=self.btnRefreshText, command=self.refresh)
        self.refresh.pack(side=TOP)
        
        self.frame1.pack(side=TOP, pady=5)

    def frameTop2(self):
        self.frame2 = Frame(self.master)
        self.frame2.config(bg='black')

        self.frameSpinner(self.frame2, "SERVO", 1)
        self.spinbox1 = Spinbox(self.frame2, values=[3,5,6,9,10,11], bg='black', fg='white', width=5, command=lambda:com.sendData('0', '0'))
        self.spinbox1.pack(side=LEFT)
        self.frameSpinner(self.frame2, "SERVO", 2)
        self.spinbox2 = Spinbox(self.frame2, values=[3,5,6,9,10,11], bg='black', fg='white', width=5, command=lambda:com.sendData('2', '0'))
        self.spinbox2.pack(side=LEFT)
        self.frameSpinner(self.frame2, "SERVO", 3)
        self.spinbox3 = Spinbox(self.frame2, values=[3,5,6,9,10,11], bg='black', fg='white', width=5, command=lambda:com.sendData('3', '0'))
        self.spinbox3.pack(side=LEFT)
        self.frameSpinner(self.frame2, "SERVO", 4)
        self.spinbox4 = Spinbox(self.frame2, values=[3,5,6,9,10,11], bg='black', fg='white', width=5, command=lambda:com.sendData('4', '0'))
        self.spinbox4.pack(side=LEFT)
        
        self.frame2.pack(side=TOP, fill=X, pady=5)

    def frameTop3(self):
        self.frame3 = Frame(self.master)
        self.frame3.config(bg='black')

        self.frameSpinner(self.frame3, "ANGLE", 1)
        self.spinbox5 = Spinbox(self.frame3, from_=0, to=180, bg='black', fg='white', width=5, command=lambda:com.sendData('0', self.spinbox5.get()))
        self.spinbox5.pack(side=LEFT)
        self.frameSpinner(self.frame3, "ANGLE", 2)
        self.spinbox6 = Spinbox(self.frame3, from_=0, to=180, bg='black', fg='white', width=5, command=lambda:com.sendData('1', self.spinbox6.get()))
        self.spinbox6.pack(side=LEFT)
        self.frameSpinner(self.frame3, "ANGLE", 3)
        self.spinbox7 = Spinbox(self.frame3, from_=0, to=180, bg='black', fg='white', width=5, command=lambda:com.sendData('2', self.spinbox7.get()))
        self.spinbox7.pack(side=LEFT)
        self.frameSpinner(self.frame3, "ANGLE", 4)
        self.spinbox8 = Spinbox(self.frame3, from_=0, to=180, bg='black', fg='white', width=5, command=lambda:com.sendData('3', self.spinbox8.get()))
        self.spinbox8.pack(side=LEFT)

        self.frame3.pack(side=TOP, fill=X)

    def frameTop4(self):
        self.frame4 = Frame(self.master)
        self.frame4.config(bg='black')

        self.btnServoText = StringVar()
        self.btnServoText.set("Test")
        self.btnServoTest1 = Button(self.frame4, width=10, highlightbackground='black', fg='white', textvariable=self.btnServoText, command=lambda:com.testServo('0'))
        self.btnServoTest1.pack(side=LEFT, fill=X, expand=True, padx=20)
        self.btnServoTest2 = Button(self.frame4, width=10, highlightbackground='black', fg='white', textvariable=self.btnServoText, command=lambda:com.testServo('1'))
        self.btnServoTest2.pack(side=LEFT, fill=X, expand=True, padx=20)
        self.btnServoTest3 = Button(self.frame4, width=10, highlightbackground='black', fg='white', textvariable=self.btnServoText, command=lambda:com.testServo('2'))
        self.btnServoTest3.pack(side=LEFT, fill=X, expand=True, padx=20)
        self.btnServoTest4 = Button(self.frame4, width=10, highlightbackground='black', fg='white', textvariable=self.btnServoText, command=lambda:com.testServo('3'))
        self.btnServoTest4.pack(side=LEFT, fill=X, expand=True, padx=20)
        
        self.frame4.pack(side=TOP, fill=X, pady=10)

    def frameSpinner(self, frame, string, idx):
        self.labelSpinner = Label(frame, text=string+' '+str(idx))
        self.labelSpinner.config(bg='black', fg='white')
        self.labelSpinner.pack(side=LEFT, fill=X, expand=True)

    def connect(self):
        global connected
        try:
            if self.comPort != []:
                if connected is False:
                    print('Connected')
                    port = self.comString.get()
                    com.setupSerial(port)
                    connected = True
                    self.btnConnectText.set('Disconnect')
                    self.master.title('Servo Arduino Configuration-Connected to '+port)
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
            self.connect.config(state=NORMAL)
            if self.comPort == []:
                self.connect.config(state=DISABLED)
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
