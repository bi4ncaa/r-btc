#! /usr/bin/env python
import rospy
import actionlib
from std_msgs.msg import Empty
# Changed nameAction -> NameAction, nameFeedback -> NameFeedback, nameResult -> NameResult
from actions_pkg.msg import NameAction, NameFeedback, NameResult

class TakeOnAndOff(object):
    
  _feedback = NameFeedback()
  _result   = NameResult()

  def _init_(self):
    self._pub_takeoff = rospy.Publisher('/drone/takeoff', Empty, queue_size=1)
    self._pub_land = rospy.Publisher('/drone/land', Empty, queue_size=1)
    self._empty_msg = Empty()
    
    self._as = actionlib.SimpleActionServer("Take_on_and_off_rbt", NameAction, self.goal_callback, False)
    self._as.start()
    
  def goal_callback(self, goal):
    r = rospy.Rate(1)
    success = True
    start_time = rospy.get_time()
    
    rospy.loginfo("Pilot %s requested action: %s" % (goal.pilot_name, goal.goal))
    
    if goal.goal == 'TAKEOFF':
        self._feedback.feedback = 'take off'
        self._feedback.progress_pct = 0
        
        for i in range(4):
            if self._as.is_preempt_requested():
                self._as.set_preempted()
                success = False
                break
                
            self._feedback.progress_pct = (i + 1) * 25 
            
            self._pub_takeoff.publish(self._empty_msg)
            self._as.publish_feedback(self._feedback)
            r.sleep()
            
    elif goal.goal == 'LAND':
        self._feedback.feedback = 'landing'
        rospy.loginfo("Goal received: LAND. Drone landing...")
        
        for i in range(4):
            if self._as.is_preempt_requested():
                rospy.loginfo('The landing goal good RBTC')
                self._as.set_preempted()
                success = False
                break
                
            self._pub_land.publish(self._empty_msg)
            self._as.publish_feedback(self._feedback)
            r.sleep()
            
    else:
        rospy.logwarn("RBT Goal received: %s" % goal.goal)
        success = False

    if success:
        self._result.status_message = "Action '%s' completed for rbt%s!" % (goal.goal, goal.pilot_name)
        self._result.total_time = rospy.get_time() - start_time
        
        self._as.set_succeeded(self._result)
      
if _name_ == '_main_':
  rospy.init_node('rbtc')
  TakeOnAndOff()
  rospy.spin()
