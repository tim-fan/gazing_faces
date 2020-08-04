#!/usr/bin/env python

import rospy
import message_filters
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from gaze_tracking_ros.msg import GazeState

class ImageSaver():
    def __init__(self):
        self._bridge = CvBridge()
    
    def save(self, image, gaze_state):
        """
        Save given image associated with given gaze state
        """
        print("callback")
        print(rospy.Time.now())
        print(gaze_state)

        # convert gaze state ratios (0 to 1) to int (-100 to 100)
        x = int(gaze_state.horizontal_ratio * 200 - 100)
        y = int(gaze_state.vertical_ratio * 200 - 100)

        outname = "/tmp/x{x}y{y}.png".format(x=x,y=y)

        print(outname)

        cv_img = self._bridge.imgmsg_to_cv2(image, desired_encoding='passthrough')
        cv2.imwrite(outname,cv_img)


def recorder():
    print("start")

    rospy.init_node("image_recorder")
    print(rospy.Time.now())

    image_saver = ImageSaver()

    image_sub = message_filters.Subscriber('face_detection/face_image', Image)
    gaze_sub = message_filters.Subscriber('gaze_state', GazeState)

    ts = message_filters.TimeSynchronizer([image_sub, gaze_sub], 10)
    ts.registerCallback(image_saver.save)
    rospy.spin()



if __name__ == '__main__':
    try:
        recorder()
    except rospy.ROSInterruptException:
        pass