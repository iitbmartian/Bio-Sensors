#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import Float64MultiArray,Float32MultiArray,String
import numpy as np
import signal
import sys
import time
import RPi.GPIO as GPIO
#-----------------------------------------------------------------
#SIGINT handler

def sigint_handler(signal, frame):
	GPIO.cleanup()
	sys.exit(0)

def update():
	global motor1 , motor2
	if(motor1==1):
		GPIO.output(17, GPIO.HIGH) # Set AIN1
		GPIO.output(27, GPIO.LOW) # Set AIN2
		motor1vel.ChangeDutyCycle(0.8*100)
		print("motor1")
	elif(motor1==-1):
		GPIO.output(27, GPIO.HIGH) # Set AIN1
		GPIO.output(17, GPIO.LOW) # Set AIN2
		motor1vel.ChangeDutyCycle(0.8*100)
		print("motor1 reverse")
	else:
		GPIO.output(17, GPIO.LOW) # Set AIN1
		GPIO.output(27, GPIO.LOW) # Set AIN2
		motor1vel.ChangeDutyCycle(0)
		print("motor1 stop")	
	if(motor2==1):
		GPIO.output(6, GPIO.HIGH) # Set AIN1
		GPIO.output(5, GPIO.LOW) # Set AIN2
		motor2vel.ChangeDutyCycle(0.8*100)
		print("motor2")
	elif(motor2==-1):
		GPIO.output(5, GPIO.HIGH) # Set AIN1
		GPIO.output(6, GPIO.LOW) # Set AIN2
		motor2vel.ChangeDutyCycle(0.8*100)
		print("motor2 reverse")
	else:
		GPIO.output(6, GPIO.LOW) # Set AIN1
		GPIO.output(5, GPIO.LOW) # Set AIN2	
		motor2vel.ChangeDutyCycle(0)
		print("motor2 stop")



def bio_callback(inp):
	global motor1 , motor2
	#print("callback\n")
	#print(inp)
	#print(inp.data)
	motor1 = inp.data[6]
	motor2 = inp.data[3]
	#print(inp.data[6])
	#print(inp.data[3])


if __name__ == '__main__':

	signal.signal(signal.SIGINT, sigint_handler)
	GPIO.setmode(GPIO.BCM)

	GPIO.setup(17, GPIO.OUT) # Connected to motor1IN1
	GPIO.setup(27, GPIO.OUT) # Connected to motor1IN2
	GPIO.setup(18, GPIO.OUT)
	GPIO.setup(6, GPIO.OUT) # Connected to motor2IN1
	GPIO.setup(5, GPIO.OUT) # Connected to motor2IN2
	GPIO.setup(12, GPIO.OUT)
	
	motor1vel=GPIO.PWM(18,100)
	motor2vel=GPIO.PWM(12,100)

	motor1=0
	motor2=0
	motor1vel.start(0)
	motor2vel.start(0)
	
	rospy.init_node('bio', anonymous=True)
	rospy.Subscriber("/rover/control_directives", Float64MultiArray, bio_callback)
	
	while(True):
		update()
