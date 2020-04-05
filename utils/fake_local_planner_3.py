#!/usr/bin/env python
import rospy
from nav_msgs.msg import Path
from std_msgs.msg import Bool
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist, PoseWithCovarianceStamped
from math import atan2

#x = 0.0
#y = 0.0 
#theta = 0.0
pose_x = 0.0
pose_y = 0.0
theta  = 0.0
REST_PATH_POINT_TO_END = 5
REST_PATH_POINT = 10
THRESHOLD = 0.15
LEFT    = 1
RIGHT   =-1
STRAIGHT= 0
path_goal_y = 0.0
path_goal_x = 0.0
def pose_callback(msg):
    global pose_x
    global pose_y
    global theta

    pose_x = msg.pose.pose.position.x
    pose_y = msg.pose.pose.position.y

    rot_q = msg.pose.pose.orientation
    (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])

def path_callback(msg):
    global path_goal_x
    global path_goal_y
    global REST_PATH_POINT
    if len(msg.poses) > 3:
        REST_PATH_POINT = len(msg.poses)
        path_goal_y = msg.poses[5].pose.position.y
        path_goal_x = msg.poses[5].pose.position.x
        print('rest path point = ' + str(REST_PATH_POINT))

    


def create_twist(direction):
    pub_twist = Twist()

    pub_twist.linear.x = 0.0
    pub_twist.linear.y = 0.0
    pub_twist.linear.z = 0.0

    pub_twist.angular.x= 0.0
    pub_twist.angular.y= 0.0
    pub_twist.angular.z= direction # -6 : means no ball

    return pub_twist

def create_goal():
    pub_goal = Bool()
    if REST_PATH_POINT < REST_PATH_POINT_TO_END:
        print(REST_PATH_POINT, REST_PATH_POINT_TO_END )
        pub_goal = True
    else:
        pub_goal = False

    return pub_goal

def ball_generator():
    rospy.init_node("fake_local_planner")
    path_sub = rospy.Subscriber("/move_base/GlobalPlanner/plan", Path, path_callback)
    pose_sub = rospy.Subscriber("/slam_pose", PoseWithCovarianceStamped, pose_callback)
    twist_pub = rospy.Publisher("/fake_cmd_vel", Twist, queue_size = 1)
    goal_pub  = rospy.Publisher("/if_goal", Bool, queue_size=10)
    position_pub =rospy.Publisher('/position', Twist, queue_size=1)

    rate = rospy.Rate(4)

    print('started')

    while not rospy.is_shutdown():
        inc_x = path_goal_x - pose_x
        inc_y = path_goal_y - pose_y

        angle_to_goal = atan2(inc_y, inc_x)

        delta_theta = angle_to_goal - theta
        print('--------------------------')
        delta_x =-(path_goal_x - pose_x) 
        delta_y = (path_goal_y - pose_y) 
        tw = Twist()
        tw.linear.x = delta_x
        tw.linear.y = delta_y
        position_pub.publish(tw)

        if delta_theta > THRESHOLD:
            if delta_theta > 3.14:
                speed = create_twist(RIGHT)
                print('right')
            else:
                speed = create_twist(LEFT)
                print('left')
        elif delta_theta < -THRESHOLD:
            if delta_theta < -3.14:
                speed = create_twist(LEFT)
                print('left')
            else:
                speed = create_twist(RIGHT)
                print('right')
        else:
            speed = create_twist(STRAIGHT)
            speed = create_twist(-6) # do not put a ball when the target is in front of husky
            print('go straight')
        print(delta_theta)
        #print('--------------------------')


        
        goal_pub.publish(create_goal())
        twist_pub.publish(speed)  
        rate.sleep()

    print('fake_local_planner shutdown')



if __name__ == '__main__':
    try:
        print('starting local planner publisher ................')
        ball_generator()

    except rospy.ROSInterruptException:
        print('ROS error')
        pass
