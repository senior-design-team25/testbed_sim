#!/usr/bin/env python
#########################################################################
## CAN Bus Arbiter Node
#
## Kevin Gilbert
#  2 November 2014
#  vulCAN
##
#  Controller Area Networks utilize a hardware arbiter implementation
#       where each node writes concurrently to the bus through logic
#       gates. Signals driven high (logic low) will stay high when a
#       logic high (low voltage) signal is trying to drive the bus.
#       Since lower valued message IDs are higher priority, this lets
#       high priority signals assume control of the bus. This is 
#       difficult to implement in directly within the ROS framework,
#       so to emulate the basic functionality of CAN an arbiter node will
#       query each control node for their message ID and provide the bus
#       grant signal to the highest priority node.
#########################################################################

import sys
import can_lib

import rospy
import random
from std_msgs.msg import String
from frame_msg.msg import frame

TOPIC = "CAN_BUS"

id_responses = []
keys = [
    0x7FF
]

def callback(data, pub):
    print data 
    if (keys.count(data.msg_id) > 0):
        id_responses.append(data)  
    else:
        print 'Received message not marked for arbiter'

def transmit(pub, msg):
    pub.publish(msg.msg_id, msg.remote_request, msg.DLC, msg.data, msg.CRC_seq, msg.ACK)

def bus_grant(pub, node):
    pub.publish(0x001, 1, 1, [0x22], 0, 0)

def talker():
    pub = rospy.Publisher(TOPIC, frame)
    rospy.Subscriber('CAN_BUS_RX', frame, callback, pub)
    rospy.init_node('arbiter', anonymous=True)
    r = rospy.Rate(0.5) # 10hz

#########################################################
#   State Machine Logic
#   Cycle through each node and grant bus
#       to device with highest priority
#########################################################
    state = 0
    next_state = 0
    node_index = 0
    msg0 = frame(0x001,1,2,[0x11,0xFF],0x1234,0)
    msg1 = frame()
    NUM_NODES = 1    
    
    nodes = [
        msg0,
        msg1
    ]

    while not rospy.is_shutdown():
        state = next_state
        if state == 0:
            message = nodes[node_index]
            node_index += 1
            if (node_index == NUM_NODES):
                #bus_grant(id_responses.index(min(id_responses)))
                next_state = 2
            else:
                next_state = 1
            transmit(pub, message) 
            
        elif state == 1:
            next_state = 0    

        elif state == 2:
            bus_grant(pub, 0)
            next_state = 4
        
        #transmit(pub, message) 
        r.sleep()
        
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException: pass
