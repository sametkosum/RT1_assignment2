#!/usr/bin/env python

import rospy
import actionlib
import actionlib.msg
import assignment_2_2022.msg
from std_srvs.srv import *
import sys
import select
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Twist
from assignment_2_2022.msg import Posxy_velxy
from colorama import Fore, Style
from colorama import init
init()

def publisher(msg): # callback function for the subscriber
    global pub
    POSITION = msg.pose.pose.position # get the position from the msg
    VELOCITY = msg.twist.twist.linear# get the twist from the msg
    posxy_velxy = Posxy_velxy() # create custom message
    # assign the parameters of the custom message
    posxy_velxy.msg_pos_x = POSITION.x
    posxy_velxy.msg_pos_y = POSITION.y
    posxy_velxy.msg_vel_x = VELOCITY.x
    posxy_velxy.msg_vel_y = VELOCITY.y
    pub.publish(posxy_velxy)# publish the custom message
def action_client():
    # create the action client
    action_client = actionlib.SimpleActionClient('/reaching_goal', assignment_2_2022.msg.PlanningAction)
    # wait for the server to be started
    action_client.wait_for_server()

    status_goal = False

    while not rospy.is_shutdown():
        # Get the keyboard inputs
        print(Fore.WHITE + " Enter position of the target or type c to cancel it ")
        #print(Fore.MAGENTA + "X position of target: ")
        INPUT_XPOS = input(Fore.BLUE + "Desired X Position : ")
        #print(Fore.MAGENTA + "Y position of target: ")
        INPUT_YPOS = input(Fore.BLUE + "Desired Y Position : ")
        
 	# If user entered 'c' and the robot is reaching the goal position, cancel the goal
        if INPUT_XPOS == "c" or INPUT_YPOS == "c":
            # Cancel the goal
            action_client.cancel_goal()
            status_goal = False
        else:
            # Convert numbers from string to float
            SEND_XPOS = float(INPUT_XPOS)
            SEND_YPOS = float(INPUT_YPOS)
            # Create the goal to send to the server
            goal = assignment_2_2022.msg.PlanningGoal()
            goal.target_pose.pose.position.x = SEND_XPOS
            goal.target_pose.pose.position.y = SEND_YPOS
            action_client.send_goal(goal) # Send the goal to the action server
            status_goal = True


def main():
    
    rospy.init_node('ACTION_CLIENT') #initialize the node
    global pub  # global publisher
    pub = rospy.Publisher("/posxy_velxy", Posxy_velxy, queue_size = 1)  # publisher: send a message which contains two parameters (velocity and position) 
    sub_from_Odom = rospy.Subscriber("/odom", Odometry, publisher)  # subscriber: get from "Odom" two parameters (velocity and position)
    action_client() # call the function client

if __name__ == '__main__':
    main()

