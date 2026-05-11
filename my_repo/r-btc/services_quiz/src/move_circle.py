#! /usr/bin/env python3

import rospy
from math import sqrt
import time
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from services_pkg.srv import CustomServMess, CustomServMessResponse

def my_callback(request):
    response = CustomServMessResponse()
    make_circle()
    response.success = True
    return response


def make_circle():
        vel.angular.z = 0.3
        vel.linear.x = 0.1
        
        pub.publish(vel)
        rospy.sleep(20.9)
        
        vel.angular.z = 0.0
        vel.linear.x = 0.0
        pub.publish(vel)




vel = Twist()  

rospy.init_node('diffbot_make_circle')
my_service = rospy.Service('/move_in_circle', CustomServMess, my_callback)
# creeaza un publisher pentru topicul /cmd_vel
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

rospy.spin()
