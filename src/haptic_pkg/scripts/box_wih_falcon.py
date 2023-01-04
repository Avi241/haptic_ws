#!/usr/bin/env python3

import rospy
import time
from geometry_msgs.msg import Wrench,WrenchStamped
from sensor_msgs.msg import Joy
from ros_falcon.msg import falconForces
from gazebo_msgs.msg import LinkStates
import numpy as np

rospy.init_node("Box_control", anonymous=True) # Initialize ros node

pub_left_force_box = rospy.Publisher("/force_left", Wrench, queue_size=1)
pub_left_force_falcon = rospy.Publisher("/falconForce", falconForces, queue_size=1)
pub_right_force_box = rospy.Publisher("/force_right", Wrench, queue_size=1)
pub_right_force_falcon = rospy.Publisher("/falconForce1", falconForces, queue_size=1)

pos_falcon_left = np.array([0.0,0.0,0.0])
pos_falcon_right = np.array([0.0,0.0,0.0])

pos_box_left = np.array([0.0,0.0,0.0])
pos_box_right = np.array([0.0,0.0,0.0])

force_box_left = np.array([0.0,0.0,0.0])
force_box_right = np.array([0.0,0.0,0.0])

msg_box_force_left =  Wrench()
msg_falcon_force_left = falconForces()

msg_box_force_right =  Wrench()
msg_falcon_force_right = falconForces()

joy_stick_sensitivity = 30

def pub_box_force_left(force_x,force_y):
    msg_box_force_left.force.x = force_x
    msg_box_force_left.force.y = force_y
    pub_left_force_box.publish(msg_box_force_left)


def pub_box_force_right(force_x,force_y):
    msg_box_force_right.force.x = force_x
    msg_box_force_right.force.y = force_y
    pub_right_force_box.publish(msg_box_force_right)

def pub_falcon_force_left(force_x,force_y):
    msg_falcon_force_left.X=force_x
    msg_falcon_force_left.Y=force_y
    pub_left_force_falcon.publish(msg_falcon_force_left)

def pub_falcon_force_right(force_x,force_y):
    msg_falcon_force_right.X=force_x
    msg_falcon_force_right.Y=force_y
    pub_right_force_falcon.publish(msg_falcon_force_right)

def callback_pos_falcon_left(data):
    global pos_falcon_left
    pos_falcon_left = data.axes
    

def callback_pos_falcon_right(data):
    global pos_falcon_right
    pos_falcon_right = data.axes
    

def callback_force_box_left(data):
    global force_box_left
    force_box_left = [data.wrench.force.x,data.wrench.force.y,data.wrench.force.z]
    

def callback_force_box_right(data):
    global force_box_right
    force_box_right = [data.wrench.force.x,data.wrench.force.y,data.wrench.force.z]
    
def box_pos_cb(data):
    global pos_box_left,pos_box_right
    box_pos = [data.pose[3].position.x,data.pose[3].position.y,data.pose[3].position.z]
    pos_box_left = [box_pos[0],box_pos[1]-0.25,box_pos[2]]
    pos_box_right = [box_pos[0],box_pos[1]+0.25,box_pos[2]]


rospy.Subscriber("/falcon/joystick", Joy, callback_pos_falcon_left,queue_size=1)
rospy.Subscriber("/left/force_feedback",WrenchStamped,callback_force_box_left,queue_size=1)
rospy.Subscriber("/falcon/joystick1", Joy, callback_pos_falcon_right,queue_size=1)
rospy.Subscriber("/right/force_feedback",WrenchStamped,callback_force_box_right,queue_size=1)
rospy.Subscriber("/gazebo/link_states",LinkStates,box_pos_cb,queue_size=1)
prev_error_x = 0
prev_error_y = 0

if __name__ == "__main__":
    try:
        program_starts = time.time()
        prev_time=0
        while not rospy.is_shutdown():
            if(time.time() - prev_time >= 0.01):
                prev_time=time.time()

                ############ States ########################################
                """
                pos_box_left  # give the positon of left box
                pos_box_right  # gives the position of right box

                pos_falcon_left # gives the position of left falcon
                pos_falcon_right # gives the position of right falocon

                force_box_left # gives the force acting on left box
                force_box_right # gives the force acting on right box
                
                """
                ############################## 
                

                ## Write your code here ######33

                ######## Publish force to box and falcon ########
                """
                pub_box_force_left(force_box_x,force_box_y) 
                pub_box_force_right(force_box_x,force_box_y)
                pub_falcon_force_left(force_falcon_x,force_falcon_y)
                pub_falcon_force_right(force_falcon_x,force_falcon_y)
                
                """


                
    except KeyboardInterrupt:
        pass
    # rospy.spin()
