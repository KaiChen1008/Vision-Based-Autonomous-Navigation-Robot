#!/usr/bin/env python
# 08 25 anna inverse
import rospy
import roslib
from time import sleep
from geometry_msgs.msg import PoseWithCovarianceStamped, Quaternion, Twist
from std_msgs.msg import Bool
from communication import sender

class controller():
    def __init__(self):
        rospy.init_node('controller')
        self.goal = False
        self.sendman = sender()
        self.twist = Twist()
        self.action_count = 0
        self.plus = 0
        self.minus = 0
        self.j = self.create_zero_twist()

        print('node started')

        rospy.Subscriber("twitch", Twist, self.callback)
        rospy.Subscriber("if_goal", Bool, self.is_goal)
        rospy.Subscriber("Emergency", Bool, self.is_Emergency)
        rospy.spin()
        
#        while not rospy.is_shutdown():
#            self.sendman.send(self.j)
#            sleep(1.0/20.0)
    
    def is_Emergency(self, data):
        if data.data == True:
            self.goal = True
            self.j = self.create_zero_twist()
            self.sendman.send(self.j)
            print('Emergency!!')
            a = '0'
            while a != 'y' and  a != 'Y':
                a = input('is ok???: ')
                print(a)
            self.goal = False


    def callback(self, t):
        #print('receive t...')
        if (self.goal is False):
            self.j = self.msgs2json(t)
            self.sendman.send(self.j)
            print(self.j)

    def is_goal(self, data):
        if data.data == True:
            self.j = self.create_zero_twist()
            self.sendman.send(self.j)
            self.goal = True
            print('achieve')
            # continue
            a = 'z'
            while a != 'y' or a != 'Y':
                a = input("if next goal exists:")
                
            self.goal = False

    
    def create_zero_twist(self):
        j = {
            'linear_x' : 0.0,
            'linear_y' : 0.0,
            'linear_z' : 0.0,
            'angular_x': 0.0,
            'angular_y': 0.0,
            'angular_z': 0.0,
        }

        return j
    
    def msgs2json(self, t):
        j = {
            'linear_x' : t.linear.x,
            'linear_y' : t.linear.y,
            'linear_z' : t.linear.z,
            'angular_x': t.angular.x,
            'angular_y': t.angular.y,
            'angular_z': t.angular.z
        }
        if t.angular.z > 0.0:
            self.plus = self.plus +1
        if t.angular.z < 0.0:
            self.minus = self.minus +1

        print(str(self.plus) + ',' + str(self.minus))
        return j
    
    def smooth_twist(self, t):
        
        return t




if __name__ == '__main__':
    try:
        print('starting controll husky....')
        c = controller()

    except rospy.ROSInterruptException:
        print('ROS error')
        pass
