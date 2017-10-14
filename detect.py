import math
import Leap

def check_hands(n,p,hand_n,finger_n):
	pos = n.palm_position
	prev_pos = p.palm_position

	pointables = n.pointables
	prev_pointables = p.pointables
	if pos.distance_to(prev_pos) <= hand_n:
		flag = True	
		for finger,prev_finger in zip(pointables,prev_pointables):
			tip = finger.tip_position
			prev_tip = prev_finger.tip_position
			if not tip.distance_to(prev_tip) <= finger_n:
				flag = False
		return flag

def get_dist(fs):
	res = []
	for i in range(0,len(fs)-1):
		res.append(fs[i].tip_position.distance_to(fs[i+1].tip_position))			
	return res	

def dynamic_check(n,p,finger_n):
	pointables = n.pointables
	arr = get_dist(pointables)
	prev_pointables = p.pointables
	prev_arr = get_dist(prev_pointables)
	
	return filter(lambda x: abs(x[0] - x[1]) > finger_n, zip(arr,prev_arr)) == []

def long_way(n,p,eps):
	vect = p.palm_position - n.palm_position
	return abs(vect.z) > eps

def goes_down(n,p):
	vect = p.palm_position - n.palm_position
	return vect.z > 0	

def rotates(n,p):
	last = n.palm_normal
	first = p.palm_normal	
	return (0.2*math.pi <= last.angle_to(first) <= 0.7*math.pi)	

def turn(n,p):
	last = n.direction
	first = p.direction
	return (0.2*math.pi <= last.angle_to(first) <= 0.7*math.pi)	


def check_dir(n,p):
	first = n.palm_normal
	last = p.palm_normal
	vec = first.cross(last)
	return (vec.dot(Leap.Vector.z_axis) >= 0)
