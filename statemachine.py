#!/usr/bin/python
import rospy
import sys
import ApproachGate
import signal
from std_msgs.msg import Bool

quitFlag = False
interrupted = False
#Maximum number of states
STATE_MAX = 1;

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

#After callback executes, statemachine loop will quit
def quitCallback(data):
	quitFlag = data.data;

def statemachine():
	quitFlag = False
	stateList = [ ]
	stateList.append(ApproachGate.ApproachGateState())

	#First state, parameter if you only want to test certain tasks
	statePosition = rospy.get_param('startingState', 0);

	#End state, parameter if you only want to test certain tasks
	stateCap = rospy.get_param('endingState', STATE_MAX);

	#Quit if your start state is after the end state
	if statePosition > stateCap:
		sys.exit("Invalid state range, quitting.")

	#Subscribe to a message that any node can publish that will state autonomous operation
	rospy.Subscriber("quitFlag",Bool, quitCallback)

	#Initialize node
	rospy.init_node('statemachine', anonymous=True)
	#Parameter rate, 15 if parameter isn't set
	rateHz = rospy.get_param('stateMachineLoopRate', 15)

	#Create ros rate object with the rate number
	rate = rospy.Rate(rateHz)
	while not quitFlag and not interrupted:
		stateList[statePosition].Update()

		if stateList[statePosition].isComplete():
			rospy.loginfo("Task marked as complete by State Machine, moving to next task.")
			#Delete class instance object to mark it for garbage collection, gotta think of the environment, yo
			#del stateList[statePosition]

			#Increment to the next state when the previous one completes
			statePosition = statePosition + 1
			#Quit when we run out of states
			if statePosition >= STATE_MAX:
				quitFlag = True

		#Sleep for 1/rate seconds
		rate.sleep()


	rospy.loginfo("Quit flag changed, exiting.")	

if __name__ == '__main__':
	try:
		signal.signal(signal.SIGINT, signal_handler)
		statemachine()
	except rospy.ROSInterruptException:
		pass

