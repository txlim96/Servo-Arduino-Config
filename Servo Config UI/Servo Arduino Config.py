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
        changePin = False
        servoState = 'normal'
        angleState = 'disabled'

        self.spinner = []           # list of servo spinners (0-3) and angle spinners (4-7)
        self.btnServoTest = []      # list of test buttons
        self.btnSetHome = []        # list of set home buttons

        self.frame = []

        for i in range(5):
            frame = Frame(self.master, bg='black')
            self.frame.append(frame)
            self.frame[i].pack(side=TOP, fill=X)
        
        self.frameTop0()
        self.frameTop12()
        self.frameTop34()

        self.strReturnHomeText = StringVar()
        self.strReturnHomeText.set("Return home")
        self.btnReturnHome = Button(self.master, highlightbackground='black', fg='white', textvariable=self.strReturnHomeText, command=self.execHome)
        self.btnReturnHome.pack(fill=BOTH, padx=10, pady=10)

    def exit(self, event):
        com.closeSerial()
        self.master.quit()

    def frameTop0(self):

        self.labelCom = Label(self.frame[0], text="COM:")
        self.labelCom.config(bg='black', fg='white')
        self.labelCom.pack(side=LEFT)

        self.comString = StringVar()
        self.refresh()
        self.popUpMenu = OptionMenu(self.frame[0], self.comString, *self.comPort, command=self.refresh)
        self.popUpMenu.config(bg='black', fg='white')
        self.popUpMenu.pack(side=LEFT)

        self.frameTopSub1()

        self.strServoPin = StringVar()
        self.strServoPin.set("Confirm pins")
        self.changePin = Button(self.frame[0], wraplength=70, highlightbackground='black', fg='white', textvariable=self.strServoPin, command=self.changeServoPin)
        self.changePin.pack(side=LEFT, fill=BOTH)
        
        self.frame[0].pack(padx=150, pady=5)

    def frameTopSub1(self):
        self.subFrame1 = Frame(self.frame[0])
        
        self.strConnectText = StringVar()
        self.strConnectText.set("Connect")
        self.btnConnect = Button(self.subFrame1, highlightbackground='black', fg='white', textvariable=self.strConnectText, command=self.connect)
        self.btnConnect.pack(side=TOP, fill=X)

        self.btnRefresh = Button(self.subFrame1, highlightbackground='black', fg='white', text='Refresh', command=self.refresh)
        self.btnRefresh.pack(side=TOP, fill=X)

        self.subFrame1.pack(side=LEFT)
        
    def frameTop12(self):
        global servoState, angleState
        string = ['SERVO', 'ANGLE']

        for f in range(1, 3):
            for i in range(4):
                self.labelSpinner = Label(self.frame[f], text=string[f-1]+ ' '+str(i), bg='black', fg='white')
                self.labelSpinner.pack(side=LEFT, fill=X, expand=True)

                spinbox = Spinbox(self.frame[f], width=3, bg='black', fg='white')
                
                if f == 1:
                    spinbox.config(values=[3,5,6,9,10,11], state=servoState, command=lambda idx=i:com.sendData('S', str(idx), self.spinner[idx].get()))
                elif f == 2:
                    spinbox.config(from_=0, to=180, state=angleState, command=lambda idx=i:com.sendData('', str(idx), self.spinner[idx+4].get()))
                    
                self.spinner.append(spinbox)
                self.spinner[i+(f-1)*4].pack(side=LEFT)
            self.frame[f].pack(pady=5)

    def frameTop34(self):
        for i in range(4):
            btn = Button(self.frame[3], highlightbackground='black', fg='white', text='Test', command=lambda idx=i:com.sendData(mode='T', val=str(idx)))
            self.btnServoTest.append(btn)
            self.btnServoTest[i].pack(side=LEFT, fill=X, expand=True, padx=20)

        for i in range(4):
            btn = Button(self.frame[4], highlightbackground='black', fg='white', text='Set home', command=lambda idx=i:self.setHome(str(idx), self.spinner[idx+4].get()))
            self.btnSetHome.append(btn)
            self.btnSetHome[i].pack(side=LEFT, fill=X, expand=True, padx=20)

        self.frame[3].pack(pady=10)

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
                self.strServoPin.set("Confirm pins")
            else:
                servoState = 'disabled'
                angleState = 'normal'
                self.strServoPin.set("Change servo pins")
                
            changePin = not changePin
            for i in range(8):
                st = servoState if i > 3 else angleState
                self.spinner[i].config(state=st)
                
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
                    self.strConnectText.set('Disconnect')
                    self.master.title('Servo Arduino Configuration-Connected to '+port)
                    com.sendData()
                    time.sleep(1)       # buffer period

                    for i in range(4):
                        com.sendData('S', str(i), self.spinner[i].get())
                        time.sleep(1)
                        
                else:
                    print('Disconnected')
                    com.closeSerial()
                    connected = False
                    self.strConnectText.set('Connect')
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
