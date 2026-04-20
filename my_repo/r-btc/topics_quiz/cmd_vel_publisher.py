#!usr/bin/env python3
import rospy

from geometry_msgs.msg import Twist

from sensor_msgs.msg import LaserScan

class ObstacleAvoidance:

    def _init_(self):

        rospy.init_node('obstacle_avoidance')

        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

        rospy.Subscriber('/scan', LaserScan, self.callback)

        self.msg = Twist()

    def callback(self, data):


        front = data.ranges[0]

        right = data.ranges[270]

        left  = data.ranges[90]

        if front == float('inf'): front = 10

        if right == float('inf'): right = 10

        if left  == float('inf'): left  = 10

        if front < 1.0:

            self.msg.linear.x = 0.0

            self.msg.angular.z = 0.5   



        elif right < 1.0:

            self.msg.linear.x = 0.0

            self.msg.angular.z = 0.5  

        elif left < 1.0:

            self.msg.linear.x = 0.0

            self.msg.angular.z = -0.5  

        else:

            self.msg.linear.x = 0.5   

            self.msg.angular.z = 0.0

        self.pub.publish(self.msg)

if _name_ == '_main_':

    node = ObstacleAvoidance()

    rospy.spin()
