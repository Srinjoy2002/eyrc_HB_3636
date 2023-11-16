import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
import cv2
import numpy as np
from sensor_msgs.msg import Image
from geometry_msgs.msg import Pose2D

class ArUcoDetector(Node):

    def __init__(self):
        super().__init__('ar_uco_detector')
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',  # Adjust the topic name according to your setup
            self.image_callback,
            10
        )
        self.publisher = self.create_publisher(
            Pose2D,
            '/detected_aruco',
            10
        )
        self.cv_bridge = CvBridge()

    def image_callback(self, msg):
        # Convert ROS Image to OpenCV image
        cv_image = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        # Define your custom ArUco marker pattern
        aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

        parameters = cv2.aruco.DetectorParameters()
        corners, ids, _ = cv2.aruco.detectMarkers(cv_image, aruco_dict, parameters=parameters)

        if ids is not None and len(ids) > 0:
            for i in range(len(ids)):
                marker_id = ids[i]
                marker_corners = corners[i][0]
                marker_center = np.mean(marker_corners, axis=0)
                x = marker_center[0]
                y = marker_center[1]
                # You need to calculate the orientation (theta) based on the ArUco marker's orientation.

                # Transform goal poses from center-based to top-left reference
                x_goal = response.x_goal - 250
                y_goal = 250 - response.y_goal  # Invert y-axis for top-left reference
                theta_goal = response.theta_goal
                hb_controller.flag = response.end_of_list

                # Create a Pose2D message and publish it
                pose_msg = Pose2D()
                pose_msg.x = x
                pose_msg.y = y
                pose_msg.theta = theta
                self.publisher.publish(pose_msg)

def main(args=None):
    rclpy.init(args=args)

    aruco_detector = ArUcoDetector()

    rclpy.spin(aruco_detector)

    aruco_detector.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

