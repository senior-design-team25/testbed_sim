#!/usr/bin/env python
import rospy
from std_msgs.msg import String
   
from frame_msg.msg import frame

TOPIC = "CAN_BUS"

def callback(data):
    rospy.loginfo(rospy.get_caller_id()+"I heard %s",data)
       
def listener():
   
    # in ROS, nodes are unique named. If two nodes with the same
    # node are launched, the previous one is kicked off. The 
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaenously.
    rospy.init_node('mc_0', anonymous=True)
   
    rospy.Subscriber(TOPIC, frame, callback)
   
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
           
if __name__ == '__main__':
    listener()
