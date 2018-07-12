import rospy
import intera_interface
from geometry_msgs.msg import Pose, Twist, Wrench
from intera_core_msgs.msg import EndpointState

class EndeffectorRecorder(object):
    def __init__(self, filename):
        """
        This recorder is to record the endeffector state
        """
        self._filename = filename
        self._done = False
        try:
            self._f = open(self._filename, 'a')
        except IOError:
            print("Could not read file:", filename)
            rospy.rospy.signal_shutdown("File cannot be read, exit!")

    def stop(self):
        """
        stop recording
        """
        self._f.close()
        self._done = True

    def done(self):
        """
        Return whether or not recording is done.
        """
        if rospy.is_shutdown():
            self.stop()
        return self._done
    
    def record(self, data):
        """
        Records the pose information (postion and orientation) of the endeffector, 
        and save it into the file in txt file
        """
        print("Test func called")
        self._f.write(str(data.pose.position.x) + ' ')
        self._f.write(str(data.pose.position.y) + ' ')
        self._f.write(str(data.pose.position.z) + ' ')
        self._f.write(str(data.pose.orientation.x) + ' ')
        self._f.write(str(data.pose.orientation.y) + ' ')
        self._f.write(str(data.pose.orientation.z) + ' ')
        self._f.write(str(data.pose.orientation.w) + '\n')
                
                