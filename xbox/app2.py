from robot import *
import time
while True:
    robot.forward(remote['ly'],remote['ry'])
    if remote['square']:
        break

robot.shutdown()