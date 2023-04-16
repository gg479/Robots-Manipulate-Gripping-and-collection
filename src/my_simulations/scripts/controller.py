#!/usr/bin/env python3

import rospy
from std_msgs.msg import String

# send message to the ur10 robot
UR10_PUB = "action/ur10"

# recieves message from the ur10 robot
UR10_SUB = "feedback/ur10"

# send message to the turtle bot
TURTLE_PUB = "action/turtle"

# receives message from turtle bo
TURTLE_SUB = "feedback/turtle"

turtle = {
    "pickup": "MOVE_TO_PICKUP_STATION",
    "load": "LOAD_PAYLOAD",
    "dropoff": "MOVE_TO_DROPOFF_STATION"
}

ur10 = {
    "wait": "AWAIT_TURTLE",
    "load": "LOAD_TURTLE",
    "completed": "LOADING_COMPLETE"
}

def turtle_handler(data):
    print("Turtle:", data.data)

    if data.data == turtle["load"]:
        ur10_pub.publish(ur10["load"])


def ur10_handler(data):
    print("UR10:", data.data)

    if data.data == ur10["completed"]:
        turtle_pub.publish(turtle["dropoff"])
   

def register_pub_sub():
    turtle_pub.publish(turtle["pickup"])
    ur10_pub.publish(ur10["wait"])


turtle_pub = rospy.Publisher(TURTLE_PUB, String, queue_size=10)
ur10_pub = rospy.Publisher(UR10_PUB, String, queue_size=10)

turtle_sub = rospy.Subscriber(TURTLE_SUB, String, turtle_handler)
ur10_sub = rospy.Subscriber(UR10_SUB, String, ur10_handler)

def start():
    rospy.init_node("controller")
    register_pub_sub()
    print("started controller")
    rospy.spin()


if __name__ == "__main__":
    start()
