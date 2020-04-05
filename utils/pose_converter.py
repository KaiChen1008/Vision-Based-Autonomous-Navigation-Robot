#!/usr/bin/env python
import rospy
import roslib
import time
import threading
from time import sleep
from geometry_msgs.msg import PoseWithCovarianceStamped, Quaternion
from tf.transformations import euler_from_quaternion, quaternion_from_euler


class pose_converter():
    def __init__(self):
        rospy.init_node('pose_converter')
        self.pub = rospy.Publisher('slam_pose', PoseWithCovarianceStamped, queue_size=1)
        print('node started')

        self.count = 0
        self.poseWithStamped = PoseWithCovarianceStamped()
        self.rate = rospy.Rate(10)

        rospy.Subscriber("amcl_pose", PoseWithCovarianceStamped, self.callback)
        # rospy.spin()

        while not rospy.is_shutdown():
            self.pub.publish(self.poseWithStamped)
            self.rate.sleep()

    def callback(self, poseWithStamped):
        print('receive pose...' + str(self.count))
        self.count = self.count + 1
        orientation = Quaternion()
        orientation = poseWithStamped.pose.pose.orientation
        q = [orientation.x, orientation.y, orientation.z, orientation.w]
        qx= self.convert(q)

        poseWithStamped.pose.pose.orientation.x = qx[0]
        poseWithStamped.pose.pose.orientation.y = qx[1]
        poseWithStamped.pose.pose.orientation.z = qx[2]
        poseWithStamped.pose.pose.orientation.w = qx[3]

        self.poseWithStamped = poseWithStamped
        # self.pub.publish(poseWithStamped)

    def convert(self, q):
        (roll, pitch, yaw) = euler_from_quaternion(q)

        yaw += 1.57

        qx = quaternion_from_euler (roll, pitch, yaw)
        return qx


GlobalPose = PoseWithCovarianceStamped()

class receiver(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        rospy.init_node('pose_converter_receiver')
        rospy.Subscriber("amcl_pose", PoseWithCovarianceStamped, self.callback)

        print('node started')
        self.count = 0
        rospy.spin()

    
    def callback(self, poseWithStamped):
        global GlobalPose
        print('receive pose...' + str(self.count))
        self.count = self.count + 1
        orientation = Quaternion()
        orientation = poseWithStamped.pose.pose.orientation
        q = [orientation.x, orientation.y, orientation.z, orientation.w]
        qx= self.convert(q)

        poseWithStamped.pose.pose.orientation.x = qx[0]
        poseWithStamped.pose.pose.orientation.y = qx[1]
        poseWithStamped.pose.pose.orientation.z = qx[2]
        poseWithStamped.pose.pose.orientation.w = qx[3]

        GlobalPose = poseWithStamped
        # self.pub.publish(poseWithStamped)

    def convert(self, q):
        (roll, pitch, yaw) = euler_from_quaternion(q)

        yaw += 1.57

        qx = quaternion_from_euler (roll, pitch, yaw)
        return qx



class sender(threading.Thread):
    def __init__(self):
        global GlobalPose
        threading.Thread.__init__(self)
        rospy.init_node('pose_converter_sender')
        self.pub = rospy.Publisher('slam_pose', PoseWithCovarianceStamped, queue_size=1)
        print('node started')
        self.rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            self.pub.publish(GlobalPose)
            self.rate.sleep()


if __name__ == '__main__':
    try:
        print('starting pose converter....')
        p = pose_converter()

        # threading type
        # print('creating theads')
        # s = sender()
        # r = receiver()
        # s.start()
        # r.start()
        # print('threads started')
        # s.join()
        # r.join()
        # print('all threads have done')

    except rospy.ROSInterruptException:
        print('ROS error')
        pass
