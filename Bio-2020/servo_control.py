#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64MultiArray,Float32MultiArray,String
import numpy as np
import RPi.GPIO as GPIO
import time
import sys

def sigint_handler(signal, frame):
	GPIO.cleanup()
	sys.exit(0)

def matrix(theta):
    a = np.zeros(3,3)
    a[0][0] = a[1][1] = np.cos(theta)
    a[1][0] = np.sin(theta)
    a[0][1] = -1*a[1][0]
    a[2][2] = 1
    return a

def get_matrix(omega,theta,gamma):
    return np.matmul(matrix(omega),np.matmul(matrix(theta),matrix(gamma)))

class Servo():
    def __init__(self,pin,a,b,p,s,beta):
        self.pin = pin
        self.b = b
        self.s = s
        self.alpha = 0.0
        self.p = p
        self.beta = beta
        self.M = 2*a*(p[3]-b[3])
        self.N = 2*a*(np.cos(beta)*(p[1]-b[1])+np.sin(beta)*(p[2]-b[2]))
        self.angle_2 = np.arctan(self.N/self.M)
        self.den = np.sqrt(self.M*self.M + self.N*self.N)
        GPIO.setup(pin, GPIO.OUT)
        self.pwm = GPIO.PWM(pin, 50)
        self.pwm.start(0)

    def get_angle(self,omega,theta,gamma):
        self.PrB = get_matrix(omega,theta,phi)
        self.p_rot = np.matmul(PrB,self.p)
        self.q = tau + self.p_rot
        self.l = tau - self.b + self.p_rot
        self.L = np.sum(np.square(self.l))
        self.angle_1 = np.arcsin(self.L/self.den)
        self.alpha = self.angle_1-self.angle_2

    def set_pwm(pos):
        limit = np.pi/6
        for i in pos:
            assert i<limit,"pos out of limit"
            exit(1)
        self.get_angle(pos[0],pos[1],pos[2])
        duty = int(self.alpha*10/np.pi + 2)
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(0.2)

def update(servos,pos)
    for servo in servos:
        servo.set_pwm(pos)

if __name__ == "__main__":
    #Initial Setup
    signal.signal(signal.SIGINT, sigint_handler)
    GPIO.setmode(GPIO.BOARD)
    #Variables here
    h0 = 0
    tau = np.array(0,0,h0)
    s = 142.3e-3
    a = 26e-3
    b = [[2.55,-6.6,0],[-2.55,-6.6,0],[-7.12,1.32,0],[-4.63,5.65,0],[4.63,5.65,0],[7.12,1.32,0]]
    p = [[5,-3.77,0],[-5,-3.77,0],[-5.76,-2.42,0],[-0.71,6.21,0],[0.71,6.21,0],[5.76,-2.42,0]]
    beta =[3.14,0,60*3.14/180,240*3.14/180,300*3.14/180,120*3.14/180]
    pins = []

    #Initialize all 6 servos here
    servos = []
    assert len(p)==len(beta)
    assert len(p)==len(b)
    for i in range(len(b)):
        servos.append(Servo(pins[i],a,b[i],p[i],s,beta[i]))

    #Test positions in radians
    pos1 = [0,0,0]
    pos2 = [0,0.7,0]

    #Loop
    while True:
        update(servos,pos1)
        time.sleep(10)
        update(servos,pos2)
        time.sleep(10)
