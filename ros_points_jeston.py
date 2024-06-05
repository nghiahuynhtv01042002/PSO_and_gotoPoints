#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import serial
import rospy
from geometry_msgs.msg import Pose2D

ser = serial.Serial('/dev/ttyUSB0', 115200)



def decoder_frame_data(data_received):

    split_index_CMD_start = data_received.index(':')
    split_index_CMD_stop = data_received.index('#', split_index_CMD_start + 1)

    split_index_X_start = data_received.index(':', split_index_CMD_stop + 1)
    split_index_X_stop = data_received.index('#', split_index_X_start + 1)

    split_index_Y_start = data_received.index(':', split_index_X_stop + 1)
    split_index_Y_stop = data_received.index('#', split_index_Y_start + 1)

    split_index_Theta_start = data_received.index(':', split_index_Y_stop + 1)
    split_index_Theta_stop = data_received.index('#', split_index_Theta_start + 1)

    cmd = data_received[split_index_CMD_start + 1:split_index_CMD_stop]
    X = float(data_received[split_index_X_start + 1:split_index_X_stop])
    Y = float(data_received[split_index_Y_start + 1:split_index_Y_stop])
    Theta = float(data_received[split_index_Theta_start + 1:split_index_Theta_stop])   
    return cmd, X, Y, Theta

def odom_publisher(path):
    rospy.init_node('odom_publisher', anonymous=True)
    odom_pub = rospy.Publisher('odom1', Pose2D, queue_size=10)
    rate = rospy.Rate(100)  # Thay đổi tần số nếu cần thiết
#     data_send ="!cmd:RUN#x:0.1#y:0.1#theta:45.00#" 
#     data_send +="\n"
#     ser.write(data_send.encode())
#     add path 
   

    while not rospy.is_shutdown():
        data_received = ser.readline().decode('utf-8').strip()
        #if data_received:
        cmd, X, Y, Theta = decoder_frame_data(data_received)
        print("cmd: {}\nx: {}\ny: {}\ntheta: {}\n".format(cmd, X, Y, Theta))

		
        if cmd is not None:
        	# Tạo message Pose2D mới
       		odom_msg = Pose2D()
        	odom_msg.x = X
        	odom_msg.y = Y
        	odom_msg.theta = Theta
		

       		# Publish Pose2D message
        	odom_pub.publish(odom_msg)
	
        rate.sleep()

if __name__ == '__main__':
	try:
                path = []
                path.append([0.4,-0.4])
                path.append([0.8,-0.4])
                path.append([1.2,0.0])
                # my_list.append([0.8,0.4])
                # my_list.append([0.4,0.4])
                # my_list.append([0.0,0.0])
                path.append([1.4,0.0])
                path.append([1.8,0.4])
                path.append([2.2,0.0])
                # print(path)
		# print("sss")
	        odom_publisher(path)
		
	except rospy.ROSInterruptException:
        	pass
	except KeyboardInterrupt:
		ser.close()
	


