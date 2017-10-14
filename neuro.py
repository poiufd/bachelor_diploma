#! /usr/bin/env python
# -*- coding: utf-8 -*-
from sklearn.neural_network import MLPClassifier
import numpy as np
from sklearn.externals import joblib
import Leap
from testing import *
import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)


def read_file(f,l):
	#hand = []
	fd = open(str(f)+"/"+l+".data","rb")

	next_block_size = fd.read(4)
	size = struct.unpack('i', next_block_size)[0]
	data = fd.read(size)
	leap_byte_array = Leap.byte_array(size)
	address = leap_byte_array.cast().__long__()
	ctypes.memmove(address, data, size)

	frame = Leap.Frame()
	frame.deserialize((leap_byte_array, size))
	#hand.append(frame.hands.rightmost)
	#return hand
	return frame.hands.rightmost	

def _read(letters):
	res = []
	for i in range(1,30):
		for l in letters:
			res.append(read_file(i,l))
		#res.append(read_file(i,letters[1]))
	return res

def coord(hand):
	coord_arr = []
	wrist = hand.wrist_position
	for finger in hand.pointables:
		dif = finger.tip_position - wrist
		coord_arr.append(dif.x)
		coord_arr.append(dif.y)
		coord_arr.append(dif.z)

	return coord_arr

def teach(letters,fname,net,i):
	hands = _read(letters)
	x = map(coord,hands)
	n = len(x)
	#y = letters*6 
	y = letters*i
	#y = [1,2,3,4]*i
	net.fit(x[:n], y[:n])
	#print y

	joblib.dump(net,"networks/"+fname + ".pkl")
	'''print net.predict(x[12]) 
	print net.predict(x[13])
	print net.predict(x[14])
	print net.predict(x[15])

	print net.predict_proba(x[12]) 
	print net.predict_proba(x[13])
	print net.predict_proba(x[14])
	print net.predict_proba(x[15])'''




def main():
	controller = Leap.Controller()

	#hands1 = read_file([3,4,5,6,7,8],'а')
	#hands2 = read_file([3,4,5,6,7,8],'б')
	#hands = hands1 + hands2
	#hands = _read(['а','б'])

	#x = map(coord,hands)
	#temp = np.array(x).reshape((1, -1))
	#y = ['a','b']*6
	clf = MLPClassifier(solver='lbfgs',alpha=1e-5)
	clf1 = MLPClassifier(solver='lbfgs',alpha=1e-5)
	clf2 = MLPClassifier(solver='lbfgs',alpha=1e-5)
	clf3 = MLPClassifier(solver='lbfgs',alpha=1e-5)
	clf4 = MLPClassifier(solver='lbfgs',alpha=1e-5)
	clf5 = MLPClassifier(solver='lbfgs',alpha=1e-5)
	#n = len(x)
	#print n
	#clf.fit(x[:12], y[:12])
	#joblib.dump(clf, 'first_try.pkl') 
	#clf = joblib.load('first_try.pkl') 

	#print x[-1:]
	#print clf.predict(x[11]) 
	# a = 1, y = 21, ы = 28, х = 23
	clf6 = MLPClassifier(solver='lbfgs',alpha=1e-5)

	#teach(['а','у','ы','х'],'1st',clf,29)
	#teach(['я','б','г','п','л'],'2nd',clf1,29)
	#teach(['в','ж'],'3rd',clf2,29)
	#teach(['е','ф','ч','э','ю','с'],'4th',clf3,29)
	#teach(['и','н','о','р'],'5th',clf4,29)
	#teach(['м','т','ш'],'6th',clf5,29)
	teach(['а','у','ы','х','я','б','г','п','л','в','ж','е','ф','ч','э','ю','с','и','н','о','р','м','т','ш','з'],'lol2',clf6,29)
	#print clf.predict(x[11])[0] 
	#print x

if __name__ == "__main__":
    main()