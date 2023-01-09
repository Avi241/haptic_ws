#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Pose
from gazebo_msgs.msg import ModelState

# Global variable to store the model's pose
model_pose_left = Pose()
model_pose_right = Pose()

pub = rospy.Publisher('/gazebo/set_model_state', ModelState, queue_size=10)

def joy_callback_left(msg):
    global model_pose_left

    # Update the x position of the model based on the joystick input
    model_pose_left.position.x = msg.axes[0] - 0.2

    # Update the y position of the model based on the joystick input
    model_pose_left.position.y = msg.axes[1] 
    model_pose_left.position.z = msg.axes[2] 

    # Publish the updated model pose
    model_state = ModelState()
    model_state.model_name = "falcon_cursor_left"
    model_state.reference_frame = "world"
    model_state.pose = model_pose_left
    pub.publish(model_state)

def joy_callback_right(msg):
    global model_pose_right

    # Update the x position of the model based on the joystick input
    model_pose_right.position.x = msg.axes[0] + 0.2

    # Update the y position of the model based on the joystick input
    model_pose_right.position.y = msg.axes[1] 
    model_pose_right.position.z = msg.axes[2] 

    # Publish the updated model pose
    pub = rospy.Publisher('/gazebo/set_model_state', ModelState, queue_size=10)
    model_state = ModelState()
    model_state.model_name = "falcon_cursor_right"
    model_state.reference_frame = "world"
    model_state.pose = model_pose_right
    pub.publish(model_state)

def control_model():
    rospy.init_node('control_model')
    rospy.Subscriber("/falcon/joystick", Joy, joy_callback_left)
    rospy.Subscriber("/falcon/joystick1", Joy, joy_callback_right)
    rospy.spin()

if __name__ == '__main__':
    control_model()
