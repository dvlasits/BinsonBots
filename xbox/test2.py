from robot import *
import time
import math

def get_angle(x,y):
    if y==0:
        if x > 0:
            return math.pi*0.5
        else:
            return math.pi*1.5
        
    angle = math.atan(x/y)
    if y < 0:
        angle += math.pi
    return angle
    

while True:
    
    velocity = math.sqrt(remote['rx']**2 + remote['ry']**2)
    angle = get_angle(remote['rx'], remote['ry'])

    if angle < math.pi/2:
        angle = angle/math.pi*2
        v_left = 1
        v_right = 1-2*angle
    elif angle < math.pi:
        angle = (angle-math.pi/2) / math.pi*2
        v_left = 1-angle*2
        v_right = -1
    elif angle < 1.5*math.pi:
        angle = (angle-math.pi) / math.pi*2
        v_left = -1
        v_right = -1 + angle*2
    else:
        angle = (angle-1.5*math.pi) / math.pi*2
        v_left = -1 + angle*2
        v_right = 1
    
    print(angle)
        

    robot.forward(v_left*velocity, v_right*velocity)
    if remote['square']:
        break

robot.shutdown()