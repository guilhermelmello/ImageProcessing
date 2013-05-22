#! /usr/bin/env python
# -*- coding:utf-8 -*-

import argparse
import copy
import matplotlib.pyplot as plt
import numpy as np
import scipy
import scipy.misc as misc
import sys

def gray(image, negative = False):
	"""
		Gera uma imagem em tons de cinza
		ou o negativo da imagem recebida
	"""
	
	#_im = np.zeros(shape=(100,200))
	#for row, l in enumerate(image[200:300]):
		#for col, pixel in enumerate(l[200:400]):
	_im = np.zeros(shape=(len(image),len(image[0])))
	for row, l in enumerate(image):
		for col, pixel in enumerate(l):
			if negative:
				_im[row][col] = 255 - sum(pixel[:3])/ 3
			else:
				_im[row][col] = np.sum(pixel) / 3
	print _im[0][0]
	return _im


def suavizacao(im,m):
	# define o tamanho da máscara (m x n)
	mask = [[1 for i in range(m)] for j in range(m)]
	r_i = len(mask)/2			# indice inicial para a linha
	c_i = len(mask[0])/2		# indice inicial para a coluna
	
	s_im = copy.deepcopy(im)	# cópia da imagem
	
	for i,lin in enumerate(im[r_i:-r_i+1],r_i):		# percorre as linhas  desconsiderando as bordas
		print i,"/",len(im)
		for j, p in enumerate(lin[c_i:-c_i],c_i):	# percorre as colunas desconsiderando as bordas
			med = 0
			for m_l in range(i-r_i, i+r_i):		# percorre as linhas da imagem que estão contidas na máscara
				med += sum(im[m_l][i-c_i:i+c_i+1])	# soma as colunas que estão dentro da máscara
			med = med/float(len(mask)*len(mask[0]))			# faz a média
			s_im[i][j] = med						
	
	return s_im


if __name__ == "__main__":
	image = misc.imread("../images/lena.tif")
	#image = [[i+j for i in range(10)] for j in range(10)]
	
	print "gerando imagem em tons de cinza"
	image = gray(image)
	
	plt.imshow(image,cmap=plt.cm.gray)
	plt.show()
	
	print "suavizando imagem"
	s_im = suavizacao(image,5)
	
	plt.imshow(s_im,cmap=plt.cm.gray)
	plt.show()
	
	
	
	
	
	
	
	
	
	
	