#! /usr/bin/env python
# -*- coding: utf-8 -*-
from detect import *
from neuro import *
import itertools
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

letters = ['а','у','ы','х','я','б','г','п','л','в','ж','е','ф','ч','э','ю','с','и','н','о','р','м','т','ш']



def recognition(res):
	if len(res) == 1:
		return static(res[0])
		#static(res[0])
	else:
		return dynamic(res)
		#dynamic(res)

def predict2(name,hand):
	clf = joblib.load('networks/'+name+'.pkl') 
	x = coord(hand)
	
	letter = clf.predict([x]).tolist()[0]
	return letter

def predict(name,hand):
	clf = joblib.load('networks/'+name+'.pkl') 
	x = coord(hand)
	
	letter = clf.predict([x]).tolist()[0]
	num = max(clf.predict_proba([x]).tolist()[0])
	if letter == 'в' or letter == 'и' or letter == 'у' or letter == 'н':
		if num >= 1:
			return letter
	if letter == 'б':
		if num >= 0.92:
			return letter
	elif letter == 'п':
		if num >= 0.91:
			return letter
	elif letter == 'ж':
		if num >= 0.95:
			return letter
	elif letter == 'т' or letter == 'ш':
		if num >= 0.97:
			return letter	
	elif letter == 'ф':
		if num >= 0.95:
			return letter	
	elif letter == 'ч':
		if num >= 0.75:
			return letter	
	elif letter == 'х':
		if num >= 0.75:
			return letter
	else:
		if num >= 0.99:
			return letter		

	#print max(clf.predict_proba([x]).tolist()[0])

def static(hand):

	return predict('lol',hand)

	#_arr = list(itertools.chain.from_iterable(arr))
	#check the probbability >= ?? 0.8?


def dynamic(hands):
	n = hands.pop(0)
	res = predict2('lol2',hands[0])
	first_hand = hands[0]
	last_hand = hands[-1]

	if n == 1:
		#sequense
		if res == 'п':
			if goes_down(first_hand,last_hand):
				return 'ц'
			else:
				return 'д'	
		elif res == 'ш':
			return 'щ'
		else:
			if res == 'з':
				if goes_down(first_hand,last_hand):
					return 'з'	
	elif n == 2:
		#rotate
		if res == 'и':
			return 'й'
		elif res == 'е':
			return 'ё'
		elif res == 'г':
			if check_dir(first_hand,last_hand):
				return 'ь'
			else:
				return 'ъ'	
	elif n==3:
		if res == 'п':
			return 'к'



