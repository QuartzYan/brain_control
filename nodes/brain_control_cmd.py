#!/usr/bin/env python
import time
import rospy
import socket
import threading
from geometry_msgs.msg import Twist

from brain_control.msg import brain_control_msg

cmd_pub = None

def pubCmdMsg(msg, duration):
  i = 0
  r = rospy.Rate(5)
  while(i < 5*duration):
    cmd_pub.publish(msg)
    r.sleep()
    i = i+1

def CallBack(msg):
  cmd = Twist()
  if msg.con_num == 3:
    if msg.con_key == 3:
      #w: move forward
      cmd.linear.x = 0.5
      cmd.angular.z = 0
    elif msg.con_key == 4:
      #s: move backward
      cmd.linear.x = -0.5
      cmd.angular.z = 0
    elif msg.con_key == 5:
      #a: turn left
      cmd.linear.x = 0
      cmd.angular.z = 1.0
    elif msg.con_key == 6:
      #d: turn right
      cmd.linear.x = 0
      cmd.angular.z = -1.0
    else:
      #stop
      cmd.linear.x = 0
      cmd.angular.z = 0
    
    pubCmdMsg(cmd, 2)

def main():
  global cmd_pub

  rospy.init_node('brain_control_cmd')
  rospy.Subscriber('brain_control_msg', brain_control_msg, CallBack)
  cmd_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)

  rospy.spin()

if __name__ == "__main__":
  try:
    main()
  except rospy.ROSInterruptException:
    pass
