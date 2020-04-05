import rospy
import roslib
from geometry_msgs.msg import Twist
from klein import Klein
import json

class husListener():
    app = Klein()

    def __init__(self):
        rospy.init_node('hushus')
        self.pub = rospy.Publisher('husky_velocity_controller', Twist, queue_size=1)

    @app.route('/', methods=['POST'])
    def handle_post(self, request):
        print('receive post')
        content = json.loads(str(request.content.read(), encoding='utf-8'))
        t = self.create_twist(content)
        self.pub.publish(t)
        
    def create_twist(self, j):
        t = Twist()
        t.linear.x = j['linear_x']
        t.linear.y = j['linear_y']
        t.linear.z = j['linear_z']

        t.angular.x = j['angular_x']
        t.angular.y = j['angular_y']
        t.angular.z = j['angular_z']

        return t

if __name__ == '__main__':
    try:
        print('starting husky listener ....')
        server = husListener()
        server.app.run('localhost', 3001)

    except rospy.ROSInterruptException:
        print('ROS error')
        pass
    
