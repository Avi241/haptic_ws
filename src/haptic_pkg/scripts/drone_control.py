
from turtle import pos
import rospy,time
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from ros_falcon.msg import falconForces
import numpy as np


rospy.init_node("Falcon_control", anonymous=True) # Initialize ros node
pub_velocity = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
pub_force = rospy.Publisher("/falconForce", falconForces, queue_size=1)
position = np.array([0.0,0.0,0.0])
velocity = np.array([0.0,0.0,0.0])
msg_vel =  Twist()
msg_force = falconForces()
joy_stick_sensitivity = 30

def takeoff():
    pub = rospy.Publisher("/drone/takeoff", Empty, queue_size=1)
    rospy.sleep(0.5) # delay for ros to initalize and create a publisher otherwise it won't be able to accept the published command
    pub.publish(Empty()) # Publish empty msg to takeoff

def land():
    pub = rospy.Publisher("/drone/land", Empty, queue_size=1)
    rospy.sleep(0.5) # delay for ros to initalize and create a publisher otherwise it won't be able to accept the published command
    pub.publish(Empty()) # Publish empty msg to takeoff

def pub_vel(vel_x,vel_y):
    msg_vel.linear.x = vel_x
    msg_vel.linear.y = vel_y
    pub_velocity.publish(msg_vel)

def pub_falcon_force(force_x,force_y):
    msg_force.X=force_x
    msg_force.Y=force_y
    pub_force.publish(msg_force)

def callback_pos(data):
    global position
    position = data.axes
    button = data.buttons[0]
    if(button==2):
        land()
    elif(button==4):
        takeoff()
    else:
        pass

def callback_vel(data):
    global velocity
    velocity[0] = data.linear.x
    velocity[1] = data.linear.y
    velocity[2] = data.linear.z

rospy.Subscriber("/falcon/joystick", Joy, callback_pos,queue_size=1)
rospy.Subscriber("/drone/gt_vel",Twist,callback_vel,queue_size=1)

prev_error_x = 0
prev_error_y = 0

if __name__ == "__main__":
    try:
        program_starts = time.time()
        prev_time=0
        while not rospy.is_shutdown():
            if(time.time() - prev_time >= 0.01):
                prev_time=time.time()
                cmd_vel_x = joy_stick_sensitivity*position[0]
                cmd_vel_y = joy_stick_sensitivity*position[1]
                # print(position_y,position_x)
                pub_vel(cmd_vel_x if cmd_vel_x >= 0.05 or cmd_vel_x <= -0.05 else 0 ,cmd_vel_y if cmd_vel_y >= 0.05 or cmd_vel_y <= -0.05 else 0)
                error_x = (velocity[0]-cmd_vel_x)
                error_y = (velocity[1]-cmd_vel_y)
                error_d_x = prev_error_x - error_x
                error_d_y = prev_error_y - error_y
                pub_falcon_force(3*error_x + 1*error_d_x,3*error_y + 1*error_d_y)
                prev_error_x = error_x
                prev_error_y = error_y
    except KeyboardInterrupt:
        pass