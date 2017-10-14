#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os, inspect, thread, time
from detect import *
from testing import *
from recogn import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


fd = 0
#only for writing to file
frame_arr = []
seq_arr = []

class SampleListener(Leap.Listener):

	temp_hand = Leap.Hand()
	hand_arr = []
	start_frame = Leap.Frame()
	_id = 0

	def on_init(self, controller):
		print "Initialized"

	def on_connect(self, controller):
		print "Connected"

	def on_frame(self, controller):

		frame = controller.frame()
		prev_frame = controller.frame(1)

		if len(frame.hands) == 1 and len(prev_frame.hands) == 1:
			self._id = self._id + 1
			#for testing
			#print "Frame id = %d" %(self._id)	
			prev_hand = prev_frame.hands.rightmost
			hand = frame.hands.rightmost
			self._check(hand,prev_hand)

	def _check(self,hand,prev_hand):		

		if self.temp_hand.is_valid:
			if not check_hands(hand,self.temp_hand,40,40):
				self.temp_hand = Leap.Hand()

		elif check_hands(hand,prev_hand,0.1,2):
			self._exit()
			self.temp_hand = prev_hand
			#print "Frame" 
			#recognition_part
			res = recognition([hand])
			if res:
				print res
			#print recognition([hand])
			#print recognition([hand])
			#only for writing to file
			#frame_for_hand = hand.frame
			#frame_arr.append(frame_for_hand)

		elif dynamic_check(hand,prev_hand,40):
			if not check_hands(hand,prev_hand,1,2):
				if len(self.hand_arr) == 0:
					self.hand_arr.append(prev_hand)
				self.hand_arr.append(hand)
			else:
				self._exit()

	def _exit(self):
		lst_frame = []	
		if len(self.hand_arr) > 0:
			first_hand = self.hand_arr[0]
			last_hand = self.hand_arr[(len(self.hand_arr)-1)]
		
			if long_way(first_hand,last_hand,50):
				#print "Got sequence"
				#recognition_part
				self.hand_arr.insert(0,1)
				res = recognition(self.hand_arr)
				if res:			
					print res
				#print recognition(self.hand_arr)
				#only for writing to file
				'''for h in self.hand_arr:
					frame = h.frame
					lst_frame.append(frame)
				seq_arr.append(lst_frame)	
				'''
			elif rotates(first_hand,last_hand):
				#print  "Got rotation sequence"	
				#recognition_part
				self.hand_arr.insert(0,2)
				res = recognition(self.hand_arr)
				if res:			
					print res
				#print recognition(self.hand_arr)				
				#only for writing to file	
				'''for h in self.hand_arr:
					frame = h.frame
					lst_frame.append(frame)
				seq_arr.append(lst_frame)'''

			elif turn(first_hand,last_hand):
				#print "Got turn sequence"
				#recognition_part
				self.hand_arr.insert(0,3)
				res = recognition(self.hand_arr)
				if res:			
					print res				
				#print recognition(self.hand_arr)	

		self.hand_arr = [] 														
	
def main():
	#only for writing to file
	#global fd
	#s = raw_input("")
    		
	#fd = open("15/" + s + ".data","wb")
	
	listener = SampleListener()
	controller = Leap.Controller()
	controller.add_listener(listener)


	print "Press Enter to quit..."
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass
	'''if s == 'д' or s == 'з' or s == 'щ' or s == 'ц' or s == 'ё' or s == 'й' or s == 'ъ' or s == 'ь':
		arr = seq_arr[-1]
		for frame in arr:
			save_frame(frame,fd)
	else:
		frame = frame_arr[-1]
		save_frame(frame,fd)	'''


	controller.remove_listener(listener)


if __name__ == "__main__":
    main()