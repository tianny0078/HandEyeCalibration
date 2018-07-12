#!/usr/bin/env python

import argparse
import rospy
import externaldevice
#from std_msgs.msg import String
from geometry_msgs.msg import Pose, Twist, Wrench
from intera_core_msgs.msg import EndpointState
from recorder import EndeffectorRecorder

class HandEyeCalibrationHelper(object):
    def __init__(self, filename):
        self._recorder = EndeffectorRecorder(filename)

    def callback(self, data):
        #rospy.loginfo(rospy.get_caller_id() + 'I heard %f %f %f', data.pose.position.x, 
        #data.pose.position.y, data.pose.position.z)
        c = externaldevice.getch()
        if c:
            if c in ['\x1b', '\x03']:
                rospy.signal_shutdown("finished")
            else:
                print("Save EndEffector Position and Orientation!")
                self._recorder.record(data)
    def stop(self):
        self._recorder.stop()

    def listener(self):

        # In ROS, nodes are uniquely named. If two nodes with the same
        # name are launched, the previous one is kicked off. The
        # anonymous=True flag means that rospy will choose a unique
        # name for our 'listener' node so that multiple listeners can
        # run simultaneously.
        rospy.init_node('listener', anonymous=True)

        rospy.Subscriber('/robot/limb/right/endpoint_state', EndpointState, self.callback)

        # spin() simply keeps python from exiting until this node is stopped
        rospy.spin()

if __name__ == '__main__':
    epilog = """
    """
    arg_fmt = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=arg_fmt,
                                     description='recorder format',
                                     epilog=epilog)
    required = parser.add_argument_group('required arguments')
    required.add_argument(
        '-f', '--file', dest='filename', required=True,
        help='the file name to record to'
    )
    args = parser.parse_args(rospy.myargv()[1:])

    helper = HandEyeCalibrationHelper(args.filename)
    helper.listener()
    rospy.on_shutdown(helper.stop)
    #externaldevice.getch()
    print 'Done'

