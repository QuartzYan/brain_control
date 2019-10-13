#!/usr/bin/env python
import time
import rospy
import socket
import threading

from brain_control.msg import brain_control_msg

class BrainControlInterface:
  def __init__(self):
    self._pub = rospy.Publisher('brain_control_msg', brain_control_msg, queue_size=1)
    try:
      self._udpSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
      self._udpSocket.bind(("", 8848))
      print 'Bind UDP on 8848...'
    except:
      print 'Build UDP socket error!! exit~'
      exit(-1)
      
  def UDPLinstenLoop(self):
    rospy.loginfo("start udp linster..")
    while not rospy.is_shutdown():
      data, addr = self._udpSocket.recvfrom(1024)
      con_num = -1
      con_key = -1
      print data
      if len(data) < 3:
        continue

      if data[0] == 'c':
        con_num = 1
      elif data[0] == 'b':
        con_num = 2
      elif data[0] == 'w':
        con_num = 3
      else:
        con_num = 0

      if data[2] == 't':
        con_key = 1
      elif data[2] == 'k':
        con_key = 2
      elif data[2] == 'w':
        con_key = 3
      elif data[2] == 's':
        con_key = 4        
      elif data[2] == 'a':
        con_key = 5
      elif data[2] == 'd':
        con_key = 6
      else:
        con_key = 0
      self.pubMsg(con_num, con_key)

  def pubMsg(self, con_num, con_key):
    msg = brain_control_msg()
    msg.header.frame_id = ''
    msg.header.stamp = rospy.Time.now()
    msg.con_num = con_num
    msg.con_key = con_key
    rospy.loginfo("%s, %s", str(con_num), str(con_key))
    self._pub.publish(msg)

def main():
  rospy.init_node('brain_control_interface')
  BCI = BrainControlInterface()
  BCI.UDPLinstenLoop()

if __name__ == "__main__":
  try:
    main()
  except rospy.ROSInterruptException:
    pass
