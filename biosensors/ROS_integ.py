#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import Float32MultiArray
import signal
import sys
import serial

#-----------------------------------------------------------------
#SIGINT handler
def sigint_handler(signal, frame):
    sys.exit(0)
    if(ser is not None):
        ser.close()
ser = serial.Serial('/dev/due',9600)  # open serial port
pub = rospy.Publisher('Sensor_Values', Float32MultiArray, queue_size=10)
signal.signal(signal.SIGINT, sigint_handler)
rospy.init_node('BioSensors', anonymous=True)
rate = rospy.Rate(1)
while not rospy.is_shutdown():
    line=ser.readline()
    pos1=line.find('[')
    pos2=line.find(',')
    pos3=line.find(';')
    pos4=line.find(']')
    if(pos1!=-1 and pos2!=-1 and pos3!=-1 and pos4!=-1):
        temp_reading=float(line[pos1+1:pos2])
        meth_reading=float(line[pos2+1:pos3])
        humid_reading=float(line[pos3+1:pos4])
        Sensor_Values=Float32MultiArray(data=[temp_reading,meth_reading,humid_reading])
    else:
        Sensor_Values=Float32MultiArray(data=[-1,-1,-1])

    pub.publish(Sensor_Values)
    rate.sleep()
ser.close() 