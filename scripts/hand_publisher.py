#!/usr/bin/env python

import rospy
import yaml

from sensor_msgs.msg import JointState
from std_msgs.msg import Float64

hand_positions = None
hand_joints = {}

def remap_cfg(data):

	cfg = {}

	for i, name in enumerate( data.name ):
		cfg[ name ] = float(data.position[i])

	return cfg

def set_angle(to, angle):
	global hand_joints

	hand_joints[to].publish( Float64( angle ) )

def callback(data):

	config = remap_cfg(data)

	if ( hand_to_grip != None ):
		set_angle("hand_to_grip", -config["hand_to_grip"])

	if ( bone_to_hand1 != None and bone_to_hand2 != None ):

		set_angle("bone_to_hand1", config["bone_to_hand"])
		set_angle("bone_to_hand2", -config["bone_to_hand"])

def listener():

	global hand_positions
	global hand_joints

	rospy.init_node("hand_publisher")
	rospy.Subscriber("joint_states", JointState, callback)

	hand_joints["hand_to_grip"] = rospy.Publisher("/hand_to_grip/command", Float64)
	hand_joints["bone_to_hand1"] = rospy.Publisher("/bone_to_hand1/command", Float64)
	hand_joints["bone_to_hand2"] = rospy.Publisher("/bone_to_hand2/command", Float64)

	hand_positions = rospy.get_param("~hand_positions")

	rospy.spin()

if __name__ == '__main__':
	listener()
