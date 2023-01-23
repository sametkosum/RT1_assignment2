#! /usr/bin/env python

import rospy # Import the ROS python library
from assignment_2_2022.srv import goal_rc, goal_rcResponse # Import the service and service response messages
import actionlib   # Import the actionlib library
import actionlib.msg  # Import the actionlib message library
import assignment_2_2022.msg  # Import the package message library

class Service:
    def __init__(self):
        # Initialize the counters for goals reached and cancelled
        self.TARGET_CANCELLED = 0
        self.TARGET_REACHED   = 0
        # Create the service
        self.srv = rospy.Service('TARGETSERVICE', goal_rc, self.data) 
        # Subscribe to the result topic
        self.sub_result = rospy.Subscriber('/reaching_goal/result', assignment_2_2022.msg.PlanningActionResult, self.result_callback)
    def result_callback(self, msg):
        # Get the status of the result from the msg
        status = msg.status.status
        # Goal cancelled (status = 2)
        if status == 2:
            self.TARGET_CANCELLED += 1
        # Goal reached (status = 3)
        elif status == 3:
            self.TARGET_REACHED += 1
    def data(self, req):
        # Return the response containing the current values of TARGET_CANCELLED and TARGET_REACHED
        return goal_rcResponse(self.TARGET_REACHED, self.TARGET_CANCELLED)
def main():
    # Initialize the node
    rospy.init_node('TARGETSERVICE')
    # Create an instance of the Service class
    TARGETSERVICE = Service()
    # Wait for messages
    rospy.spin()
if __name__ == "__main__":
    main()

