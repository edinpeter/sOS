import rospy
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
#Declare state

class ApproachGateState:
	#Class variables will get 
	image = None
	isActive = False
	bridge = CvBridge()
	taskComplete = False
	#Update class image variable 
	def isComplete(self):
		return self.taskComplete

	def imageCallback(self,image_data):
		if not isActive:
			return
		rospy.loginfo("ApproachGate: Received image message")
		try:
			cv_image = bridge.imgmsg_to_cv2(image_data, "bgr8")
			ApproachGate.image = cv2_img
		except CvBridgeError, e:
			print e

	def Update(self):
		rospy.loginfo("Approaching gate")

		#Some condition marks this task as complete
		if 0:
			rospy.loginfo("Approach Gate Task complete, terminating.")
			taskComplete = True

			
	def __init__(self):
		rospy.loginfo("ApproachGate state created")
		self.subscriber = rospy.Subscriber("/stereo/left/image_rect_color", Image, self.imageCallback,  queue_size = 1)
	