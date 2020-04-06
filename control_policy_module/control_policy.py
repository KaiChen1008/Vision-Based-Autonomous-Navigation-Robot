#!/usr/bin/env python2
# Software License Agreement (BSD License)
from __future__ import print_function

import sys
import os 
import numpy as np
import tensorflow as tf 
import rospy
from geometry_msgs.msg import Twist, Point
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import time
try:
   sys.path.remove("/opt/ros/melodic/lib/python2.7/dist-packages")
   print('ok')
except:
   print('error remove path')
import cv2
# SPEED
speed_ratio_l = 0   # To slow down linear velocity smoothly
speed_ratio_a = 0   # To slow down angular velocity smoothly
pre_linear_v = 0    # Record previous motion
pre_angular_v = 0   # Record previous motion
full_speed = 0.3   # Highest speed

pose_x = 0
pose_y = 0

# ----------------------------Best Models-------------------------------
meta_path = './Unitedmap_0906_reload-0/RobotBrain/model-12063494.cptk.meta'
ckpt_path = './Unitedmap_0906_reload-0/RobotBrain/'
# ----------------------------------------------------------------------
# goal vector
# meta_path = './models/goal_vector_0218-0/RobotBrain/model-8049273.cptk.meta'
# ckpt_path = './models/goal_vector_0218-0/RobotBrain/'

#meta_path = './models/Unitedmap_0907_LW-0/RobotBrain/model-4757563.cptk.meta'
#ckpt_path = './models/Unitedmap_0907_LW-0/RobotBrain/'


# meta_path = './0227_LW-0/RobotBrain/model-7306821.cptk.meta'
# ckpt_path = './0227_LW-0/RobotBrain/'



config = tf.ConfigProto(log_device_placement=False, allow_soft_placement=True)
config.gpu_options.allow_growth = True

def create_speed(angular_v):
    global speed_ratio_a, pre_angular_v, full_speed
    if angular_v:
        if pre_angular_v * angular_v == -1: # Suddenly change of direction leads to speed drop to 0.
            speed_ratio_a = 0
        pre_angular_v = angular_v
        speed_ratio_a = speed_ratio_a + 0.05 if speed_ratio_a < 1 else 1
        return speed_ratio_a * full_speed * angular_v
    else:
        speed_ratio_a = speed_ratio_a - 0.1 if speed_ratio_a >= 0.1 else 0
        return speed_ratio_a * full_speed * pre_angular_v

class RL_Model:
	def __init__(self, path):
		tf.reset_default_graph()
		self.sess = tf.Session()
		self.saver = tf.train.import_meta_graph(path)
		graph = tf.get_default_graph()
		self.visual_in = graph.get_tensor_by_name('visual_observation_0:0')
		# self.vector_in = graph.get_tensor_by_name('vector_observation:0')
		self.conv = graph.get_tensor_by_name('main_graph_0_encoder0/conv_2/Conv2D:0')
		self.action = graph.get_tensor_by_name('action:0')
		self.action_mask = graph.get_tensor_by_name('action_masks:0') 
		self.queue_val = 0	
		self.action_pub = rospy.Publisher('twitch', Twist, queue_size=1)
		self.linear_speed = 0.2
		self.angular_speed = 0.3#0.4186
		self.move_command = Twist()
		self.count = 3
		self.mask = np.array([[1, 1, 1]])
		#self.last_time = 0
		self.saver.restore(self.sess, tf.train.latest_checkpoint(ckpt_path))
		self.right_count = 0
		self.left_count = 0
		
	def restore_and_test(self, img_test):

		self.move_command.linear.x = self.linear_speed
		#elf.count = (self.count + 1) % 5
		#self.saver.restore(self.sess, tf.train.latest_checkpoint(ckpt_path))
		#act = tf.multinomial(self.action, 1)
		# prob = self.sess.run([self.action], feed_dict = {self.visual_in:img_test, self.vector_in:[[pose_x,pose_y]], self.action_mask:self.mask})
		prob = self.sess.run([self.action], feed_dict = {self.visual_in:img_test, self.action_mask:self.mask})

		direction = np.argmax(prob)
		print(direction)
		# print(self.left_count, self.right_count)
		self.move_command.angular.z = 0
		# 2-Action
		# Turn Right
		# if direction == 0 :
		# 	self.move_command.angular.z = -self.angular_speed
		# # Turn Left
		# elif direction == 1:
		# 	self.move_command.angular.z = self.angular_speed

		# 3-Action
		if direction == 0 :
			self.move_command.angular.z = create_speed(0)
			#self.move_command.angular.z = 0
			#self.queue_val += 0
		# Turn Left
		elif direction == 1:
			self.move_command.angular.z = create_speed(1)
			#self.move_command.angular.z = self.angular_speed
			#self.left_count += 1
			#self.queue_val += 1
		# Turn Right
		elif direction == 2:
			self.move_command.angular.z = create_speed(-1)
			#self.move_command.angular.z = -self.angular_speed
			#self.right_count += 1
			#self.queue_val += -1 
		self.action_pub.publish(self.move_command)
class image_converter:

	def __init__(self):	
		self.bridge = CvBridge()
		self.image_sub = rospy.Subscriber("chatter", Image, self.callback)
		#self.pose_sub = rospy.Subscriber("goal_vector", Point, self.pose_callback)
		self.RLmodel = RL_Model(meta_path)
		self.last_time = time.time()

	def callback(self,data):
		try:
			cv_image = self.bridge.imgmsg_to_cv2(data, "passthrough")
		except CvBridgeError as e:
			print(e)

		width = 120
		height = 80
		dim = (width, height)
		resize_image = cv2.resize(cv_image, dim, interpolation=cv2.INTER_AREA)
		cv2.imshow("Resize_image data", cv_image)
		#resize_image = resize_image.reshape((1, 80, 120, 3))
		resize_image = [resize_image]
		#print(time.time() - self.last_time)
		self.RLmodel.restore_and_test(resize_image)
		self.last_time = time.time()

		cv2.waitKey(1)
	
	def pose_callback(self, data):
		global pose_x, pose_y
		pose_x = data.x 
		pose_y = data.y 
		print(pose_x)
		print(pose_y)

	def callback2(self, position):
		self.RLmodel.x = position.linear.x
		self.RLmodel.y = position.linear.y
		
	def test(self):
		for i in range(100):
			fake_image = np.zeros((1, 80, 120, 3))
			self.RLmodel.restore_and_test(fake_image)
def main(args):
	rospy.init_node('image_converter', anonymous=True)
	ic = image_converter()
	ic.test()
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting down")
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main(sys.argv)
