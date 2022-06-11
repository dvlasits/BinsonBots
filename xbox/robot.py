import atexit
import RPi.GPIO as g
import time
import threading
from collections import defaultdict
from approxeng.input import CentredAxis, TriggerAxis, Button, Controller, BinaryAxis
from approxeng.input.selectbinder import ControllerResource
from approxeng.input.controllers import ControllerRequirement, print_devices, ControllerNotFoundError

class MyController():

    def listen(self):
        start = time.time()
        # Get a joystick
        while time.time() - start < 120:
            try:
                
                with ControllerResource(ControllerRequirement(require_snames = ['lx'])) as joystick:
                    # Loop until we're disconnected
                    while joystick.connected:
                        if self.dictt['stop'] == 10:
                            quit()
                        # This is an instance of approxeng.input.ButtonPresses
                        #print(str(joystick.axes) + f"sq = {joystick['square'] is not None},tri = {joystick['triangle'] is not None}, ",end = '\r', flush = True)
                        self.dictt['ly'] = -joystick['ly']
                        self.dictt['lx'] = joystick['lx']
                        self.dictt['rx'] = joystick['rx']
                        self.dictt['ry'] = -joystick['ry']
                        presses = joystick.check_presses()
                        self.dictt['square'] = joystick['square'] is not None
                        self.dictt['triangle'] = joystick['triangle'] is not None
                        self.dictt['circle'] = joystick['circle'] is not None
                        self.dictt['x'] = joystick['cross'] is not None
                        self.dictt['LB'] = joystick['l1'] is not None
                        self.dictt['RB'] = joystick['r1'] is not None
                        self.dictt['lt'] = joystick['lt']
                        self.dictt['rt'] = joystick['rt']
                        
            except ControllerNotFoundError:                    
                for i in self.dictt:
                    self.dictt[i] = 0
        for i in self.dictt:
            self.dictt[i] = 0
    def giveDict(self,dictt):
        self.dictt = dictt

class Robot:

    def __init__(self):
        self.vars = {}
        g.setmode(g.BCM)
        LRPWM = [18,15]
        self.OutDirec = [24,23]
        
        self.pwms = []
        for pwm in LRPWM:
            g.setup(pwm,g.OUT)
            self.pwms.append(g.PWM(pwm,100))
            self.pwms[-1].start(0)
        for direc in self.OutDirec:
            g.setup(direc,g.OUT)
            g.output(direc, 1)
        self.controller = MyController()
        self.dictt = defaultdict(int)
        self.controller.giveDict(self.dictt)
        self.t = threading.Thread(target = self.listen2, args = ())
        self.t.start()
    
    def listen2(self):
        self.controller.listen()
            
    def forward(self,speed1,speed2):
            if speed1 < -1:
                speed1 = -1
            if speed1 > 1:
                speed1 = 1
            if speed2 < -1:
                speed2 = -1
            if speed2 > 1:
                speed2 = 1
            DirecL = 0
            DirecR = 0
            speeds = [speed1, speed2]
            if speed1 < 0:
                DirecL = 1
            if speed2 < 0:
                DirecR = 1
            for index,direc in enumerate([DirecL, DirecR]):
                g.output(self.OutDirec[index], direc)
            for index,pwm in enumerate(self.pwms):
                pwm.ChangeDutyCycle(abs(speeds[index]) * 100)

    def turn(self,power):
        self.forward(power,-power)

    def stop(self):
        self.forward(0,0)

    def shutdown(self):
        try:
            self.stop()
        except:
            pass
        try:
            self.stop()
        except:
            pass
        print("Process stopped")
        self.dictt['stop'] = 10


robot=Robot()
remote = robot.dictt
atexit.register(robot.shutdown)
