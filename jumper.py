#!/usr/bin/env python
# -*- coding:utf-8 -*-
# jumper will stand in the left of right side of screen , we can culculate the distence of jumper with middle line, then get the duration(ms)
# send devices :  input swipe <x1> <y1> <x2> <y2> [duration(ms)]
# adb shell /system/bin/screencap -p /sdcard/screenshot.png
# adb pull /sdcard/screenshot.png .
# (or not delete)adb shell rm /sdcard/screenshot.png
# load jumper
# jumper = img.open("jumper.png")

import PIL.Image as img
from math import *
class jumper(object):
	"""docstring for jumper"""
	def __init__(self, jumper_file_name, confige=None):
		self.jimg = img.open(jumper_file_name).convert('RGB')
		self.confige = confige
		# key point(random select on jumpper)
		self.kp = [(39,5),(19,47),(59,49),(40,86),(40,140),(7,190),(73,193)]

	"""pixel is familier, differ judge by threshold(default 5)

	return boolean
	"""
	def _isfamilier(self, rgb1,rgb2,threshold = 5):
		return abs(rgb1[0]-rgb2[0]) < threshold and abs(rgb1[1]-rgb2[1]) < threshold and abs(rgb1[2]-rgb2[2]) < threshold
	
	"""main func in jumper

	@param _tim target img
	@return x,y of jumper foot
	"""
	def _find_jumper(self, _tim):
		def _jumper_foot(x,y):
			return x+self.jimg.width//2,y+self.jimg.height*9//10

		# h: 1/4 to 3/4
		for _y in range(_tim.height//4,_tim.height*3//4):
			for _x in range(_tim.width - self.jimg.width):
				__count = 0
				for _xy in self.kp:
					if self._isfamilier(_tim.getpixel((_x+_xy[0],_y+_xy[1])), self.jimg.getpixel(_xy)):
						__count += 1
						# fit
						if __count > len(self.kp)-2:
							if _x <= _tim.width//2:
								print("----> left side")
							else:
								print("----> right side")
							print(_x,_y)
							return _jumper_foot(_x,_y)
						continue
					break
		print("not found")

	"""current get by mirror centen line
	
	@param	jxy	after _find_jumper get the jumper position, then use this position to find target
	"""
	def _find_target(self, _target_img, jxy):
		# slope set 40'
		x,y = jxy
		_slope = pi*40/180
		_tx = (_target_img.width//2+1-x)*2+x
		_ty = y-2*sin(_slope)*abs(_target_img.width//2+1-x)
		return _tx,int(_ty)


	"""mark position
	"""
	def _mark(self, img, xy, radius=5,color=(255,0,0)):
		print("set mark :",xy)
		x,y = xy
		_min_x = x - radius if x >= radius else 0
		_min_y = y - radius if y >= radius else 0
		_max_x = x + radius if x + radius < img.width else img.width
		_max_y = y + radius if y + radius < img.height else img.height
		for _y in range(_min_y,_max_y):
			for _x in range(_min_x,_max_x):
				img.putpixel((_x,_y),color)
		return img

	"""draw grid
	"""
	def _grid(self, _tim,w_d=2,h_d=2,bar=1,color=(255,0,0)):
		if w_d > 1:
			for y in range(_tim.height):
				for x in range(_tim.width//w_d, _tim.width, _tim.width//w_d):
					for _b in range(bar):
						_tim.putpixel((x+_b,y),color)
						_tim.putpixel((x-_b,y),color)
		if h_d > 1:
			for x in range(_tim.width):
				for y in range(_tim.height//h_d, _tim.height, _tim.height//h_d):
					for _b in range(bar):
						_tim.putpixel((x,y+_b),color)
						_tim.putpixel((x,y-_b),color)
		return _tim

for i in range(1,9):

	j = jumper("jumper.png")
	tim = img.open(str(i)+".png").convert('RGB')
	_pos = j._find_jumper(tim)
	if _pos:
		_target = j._find_target(tim, _pos)
		j._mark(tim, _pos)
		j._mark(tim, _target)
		j._grid(tim, w_d=4, h_d=4)
		tim.save(str(i)+"_test.png")




"""
@param _tim target img
@param jumper jumper
@return x,y of jumper foot
# """
# def find_jumper(_tim, jumper):
# 	# get by green channel(not now)
# 	# key point
# 	# (14,32),(66,32),(40,5),(40,57),
# 	# init jumper info
# 	jw,jh = jumper.size
# 	key_point = [(39,5),(19,47),(59,49),(40,86),(40,140),(7,190),(73,193)]
# 	key_point_v = []
# 	_jumper_rgbs = list(jumper.getdata())
# 	for _v in key_point:
# 		key_point_v.append(_jumper_rgbs[_v[0]+_v[1]*jw])
	
# 	w,h = _tim.size
# 	rgbs = list(_tim.getdata())

# 	for _y in range(h//4,h*3//4):
# 		for _x in range(w//2 - jw):
# 			__count = 0
# 			# left side
# 			_lx = _x
# 			for _k in range(len(key_point)):
# 				_cx,_cy = key_point[_k][0] + _lx,key_point[_k][1] + _y
# 				if isfamilier( rgbs[_cx+_cy*w], key_point_v[_k]):
# 					__count += 1
# 					if __count == len(key_point):
# 						print("----> left side")
# 						print(_lx,_y)
# 						return _lx+jw//2,_y+jh*9//10
# 					continue
# 				break

# 			# right side
# 			_rx = _x + w//2 - jw
# 			for _k in range(len(key_point)):
# 				_cx,_cy = key_point[_k][0] + _rx,key_point[_k][1] + _y
# 				if isfamilier( rgbs[_cx+_cy*w], key_point_v[_k]):
# 					__count += 1
# 					if __count == len(key_point):
# 						print("----> right side")
# 						print(_rx,_y)
# 						return _rx+jw//2,_y+jh*9//10
# 					continue
# 				break
# 	print("not found")
# 	pass

# # for visual test, mark x,y position
# def _t_mark_position(im,xy,radius=6,color=(255,0,0)):
# 	print("set mark :",xy)
# 	x,y = xy
# 	w,h = im.size
# 	# n = 46
# 	# for i in range(1,n):
# 	# 	im.putpixel((int(x+radius*cos(2*pi/i)), int(y+radius*sin(2*pi/i))), (255,0,0))
# 	_min_x = x - radius if x >= radius else 0
# 	_min_y = y - radius if y >= radius else 0
# 	_max_x = x + radius if x + radius < w else w
# 	_max_y = y + radius if y + radius < h else h
# 	for _y in range(_min_y,_max_y):
# 		for _x in range(_min_x,_max_x):
# 			im.putpixel((_x,_y),color)
# 	return im

# # pixel is familier
# def isfamilier(rgb1,rgb2,Threshold = 5):
# 	return abs(rgb1[0]-rgb2[0]) < Threshold and abs(rgb1[1]-rgb2[1]) < Threshold and abs(rgb1[2]-rgb2[2]) < Threshold

# #@param jxy jumper x,y
# def _get_target(im,jxy):
# 	x,y = jxy
# 	w,h = im.size
# 	# slope set 40'
# 	_slope = pi*40/180
# 	_tx = (w//2+1-x)*2+x
# 	_ty = y-2*sin(_slope)*abs(w//2+1-x)
# 	return _tx,int(_ty)

# def _draw_mid_line(im,bar=1,color=(255,0,0)):
# 	w,h = im.size
# 	for y in range(h):
# 		for _b in range((bar+1)//2):
# 			im.putpixel((w//2+_b,y),color)
# 			im.putpixel((w//2-_b,y),color)
# 	for x in range(w):
# 		for _b in range((bar+1)//2):
# 			im.putpixel((x,h//2+_b),color)
# 			im.putpixel((x,h//2-_b),color)
# 	return im

# # _t_mark_position(img.open("3.png"),(330, 1047)).save("mark.png")
# _tim = img.open("4.png")
# point = find_jumper(_tim,jumper)
# if point:
# 	_target = _get_target(_tim,point)
# 	_marked_img = _t_mark_position(_tim, point)
# 	_marked_img = _t_mark_position(_marked_img, _target)
# 	_marked_img = _draw_mid_line(_marked_img)
# 	_marked_img.save("4_marked_img.png")
