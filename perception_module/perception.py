# Lint as: python3
# ==============================================================================
"""Run to start the perception module.
Usage: 
python perception.py -m <model> 
python perception.py --model=<model>
Arguments: 'o' or 'outdoor' for outdoor model, 'i' or 'indoor' for indoor model.
if not specified, runs on default arguments.
"""
import sys
import rospy
import os 
import numpy as np
from nav_msgs.msg import Path
from geometry_msgs.msg import Twist,Vector3
from std_msgs.msg import String
from sensor_msgs.msg import Image
import time
from cv_bridge import CvBridge, CvBridgeError
sys.path.append('utils')
import get_dataset_colormap
try:
    sys.path.remove("/opt/ros/kinetic/lib/python2.7/dist-packages")
    print('ok')
except:
    print('error remove path')
import cv2
import inference
import tensorflow as tf 
from PIL import Image as Image_pil
import virtual_guide

sys.path.append('/opt/ros/kinetic/lib/python2.7/dist-packages')
class image_converter:
    def __init__(self, model):
		#configurations for tensorflow
		config = tf.ConfigProto(log_device_placement=False, allow_soft_placement=True)
		config.gpu_options.allow_growth = True
		#publisher
		self.pub = rospy.Publisher("chatter",Image, queue_size=1)
		self.bridge = CvBridge()
		#planner subscriber
		self.vector_sub = rospy.Subscriber("/fake_cmd_vel", Twist, self.vector_callback)
		#camera subscriber
		self.image_sub = rospy.Subscriber("/zed/left/raw_image", Image, self.image_callback)

    	#choose indoor or outdoor model
		if(model=='i' or model=='indoor'):
			self.model = 'i'
		elif(model=='o' or model=='outdoor'):
			self.model = 'o'
		else:
			print('Please choose model "indoor" or "outdoor". Outdoor is chosen on defalt.')
		if(self.model == 'i'):
			self.MODEL = inference.DeepLabModel('models/mobilev2indoor_stride16_90000.tar.gz')
		else:
			self.MODEL = inference.DeepLabModel('models/mobilev2_stride16add153_100000.tar.gz')
		self.first = True
		self.vector = 2
		self.ADD_BALL = virtual_guide.Add_Guide()
    def receive_image(self):
		"""Callback function for receiving data.
		All data recieved in this function."""
		self.rpi_name, self.package = self.image_hub.recv_image()
		self.image_hub.send_reply(b'OK')

		#check the package name of data
		if self.rpi_name=="zed_image":
			self.image = self.package
			self.image_callback()
		elif self.rpi_name=="direction":
			self.angular = self.package
			self.vector_callback()
		else:
			print("Not receive image or vector.")
    def vector_callback(self,data):
        """Vector callback function for directional data from the Planner module"""
        #straight
        if data.angular.z == 0.0:
            self.vector = 2
        #right
        elif data.angular.z < 0 and data.angular.z > -5:
            self.vector = 3
        #left
        elif data.angular.z > 0:
            self.vector = 1
        #no direction specified
        elif data.angular.z <= -5:
            self.vector = 0

    def image_callback(self,data):
		try:
			cv_image = self.bridge.imgmsg_to_cv2(data, "passthrough")
		except CvBridgeError as e:
			print(e)
        
        #run the segmentation model
		image = Image_pil.fromarray(cv_image)
		resized_im, seg_map = self.MODEL.run(image)
		resized_im = np.array(resized_im)

        #get colormap for specified model
		if(self.model =='o'):
			seg_image = get_dataset_colormap.label_to_color_image_rl(seg_map,'cityscapes').astype(np.uint8)
		else:
			seg_image = get_dataset_colormap.label_to_color_image_rl(seg_map,'ade20k').astype(np.uint8)

		#get size and initialize
		if self.first==True:
			self.ADD_BALL.initialize(seg_image)
			self.first = False

		#for keyboard input
		key = cv2.waitKey(33)
		if key == 119:# or self.vector == 2:
			print("up")
			self.vector = 2
		elif key == 97:# or self.vector == 1:
		 	print("left")
		 	self.vector = 1
		elif key == 100:# or self.vector == 3:
		 	print("right")
			self.vector = 3
		elif key == 27:# or self.vector == 0:
			self.vector = 0
		else :
			pass
        
        #resize
		dim = (120, 80)
		seg_image = cv2.resize(seg_image, dim, interpolation=cv2.INTER_AREA)
		resized_im = cv2.resize(resized_im, dim, interpolation=cv2.INTER_AREA)

		#add virtual guide
		seg_image = self.ADD_BALL.add_check(self.vector,seg_image)
		
		#for visualization 
		resized_im = cv2.cvtColor(resized_im, cv2.COLOR_BGR2RGB) #change to brg color space
		color_and_mask = cv2.addWeighted(resized_im, 0.3, seg_image, 0.7, 0.0) #overlayed image
		color_and_mask = cv2.resize(color_and_mask, (360,240), interpolation=cv2.INTER_AREA) #make larger
		cv2.imshow('frame', color_and_mask)

		#send processed image
		to_send = seg_image
		image_message = self.bridge.cv2_to_imgmsg(to_send, encoding="passthrough")
		#rospy.loginfo(image_message)
		self.pub.publish(image_message)

def main(argv):
    model = "indoor"
    try:
        opts, args = getopt.getopt(argv,"-h-m:",["help","model="])
    except getopt.GetoptError:
        print('GetoptError, usage: perception.py --m <model>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h','--help'):
            print("Run to start the perception module.\n\
            Usage: perception.py -m <model>\n\
            or perception.py --model=<model>\n\
            Arguments: o for outdoor model, i for indoor model.")
            sys.exit()
        elif opt in ('-m','--model'):
            if opt in ('o','i','outdoor','indoor'):
                model = arg
            else:
				print('Please chose model "indoor" or "outdoor". Indoor is chosen on defalt.')
				sys.exit()
    print("model: ",model)
    
    ic = image_converter(model)
    rospy.init_node('image_converter', anonymous=True)

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv[1:])