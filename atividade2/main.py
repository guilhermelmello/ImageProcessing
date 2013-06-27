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
	# define o tamanho da máscara (m x m)
	mask = [[1 for i in range(m)] for j in range(m)]
	r_i = len(mask)/2			# indice inicial para a linha
	c_i = len(mask[0])/2		# indice inicial para a coluna
	
	s_im = np.zeros(shape=(len(image),len(image[0])))
	
	for i,lin in enumerate(im[r_i:-r_i],r_i):			# percorre as linhas  desconsiderando as bordas
		for j, p in enumerate(lin[c_i:-c_i],c_i):		# percorre as colunas desconsiderando as bordas
			med = 0
			for i_m in range(i-r_i, i+r_i+1):			# percorre as linhas da imagem que estão contidas na máscara
				for j_m in range(j-c_i, j+c_i+1):		# percorre as colunas da imagem que estão contidas na máscara
					med += im[i_m][j_m]
			med = med/float(len(mask)*len(mask[0]))		# faz a média
			s_im[i][j] = med
	
	return s_im


def suavizacao_kvizinhos(im,m,k):
	# define o tamanho da máscara (m x m)
	mask = [[1 for i in range(m)] for j in range(m)]
	r_i = len(mask)/2			# indice inicial para a linha
	c_i = len(mask[0])/2		# indice inicial para a coluna
	
	s_im = np.zeros(shape=(len(image),len(image[0])))
	
	for i,lin in enumerate(im[r_i:-r_i],r_i):			# percorre as linhas  desconsiderando as bordas
		print i,"/",len(im)
		for j, p in enumerate(lin[c_i:-c_i],c_i):		# percorre as colunas desconsiderando as bordas
			med = []
			for i_m in range(i-r_i, i+r_i+1):			# percorre as linhas da imagem que estão contidas na máscara
				for j_m in range(j-c_i, j+c_i+1):		# percorre as colunas da imagem que estão contidas na máscara
					med.append(im[i_m][j_m])			# adiciona o pixel atual em uma lista
			s_im[i][j] = media_kvizinhos(med,im[i][j],k)# faz a média dos k vizinhos e retorna o valor para o pixel 
	return s_im



def media_kvizinhos(v,pix,k):
	v.sort()					# ordena o vetor de entrada
	p_ind = v.index(pix)		# armazena a posição do pixel no vetor
	v_res = []					# inicializa um vetor resultante (para armazenar os k vizinhos)
	e = p_ind-1					# inicializa as posições dos vizinhos (na lista) a ser computado
	d = p_ind+1
	while len(v_res) < k:
		d_e = 300				# inicializa a distancia a esquerda
		d_d = 300				# inicializa a distancia a direita
		
		if e >= 0:				# calcula a distancia do elemento a esquerda
			d_e = v[p_ind] - v[e]
		if d < len(v):			# calcula a distancia do elemento a direita
			d_d = v[d] - v[p_ind]
		
		if d_e <= d_d:
			v_res.append(v[e])
			e -= 1
		else:
			v_res.append(v[d])
			d += 1
	
	return sum(v_res)/float(k)



def suavizacao_mediana(im,m):
	# define o tamanho da máscara (m x m)
	mask = [[1 for i in range(m)] for j in range(m)]
	r_i = len(mask)/2			# indice inicial para a linha
	c_i = len(mask[0])/2		# indice inicial para a coluna
	
	s_im = np.zeros(shape=(len(image),len(image[0])))
	
	for i,lin in enumerate(im[r_i:-r_i],r_i):			# percorre as linhas  desconsiderando as bordas
		print i,"/",len(im)
		for j, p in enumerate(lin[c_i:-c_i],c_i):		# percorre as colunas desconsiderando as bordas
			med = []
			for i_m in range(i-r_i, i+r_i+1):			# percorre as linhas da imagem que estão contidas na máscara
				for j_m in range(j-c_i, j+c_i+1):		# percorre as colunas da imagem que estão contidas na máscara
					med.append(im[i_m][j_m])			# adiciona o pixel atual em uma lista
			med.sort()
			s_im[i][j] = med[len(med)/2]				# atribui o valor mediano do vetor
	return s_im


def operador_laplaciano(im):
	mask = [[ 0,-1, 0],
		    [-1, 4,-1],
		    [ 0,-1, 0]]
	
	s_im = np.zeros(shape=(len(im),len(im[0])))
	
	for i,lin in enumerate(im[1:-1]):
		for j,pixel in enumerate(lin[1:-1]):
			s  = im[i-1][j-1] * mask[0][0]
			s += im[i-1][ j ] * mask[0][1]
			s += im[i-1][j+1] * mask[0][2]
			s += im[ i ][j-1] * mask[1][0]
			s += im[ i ][ j ] * mask[1][1]
			s += im[ i ][j+1] * mask[1][2]
			s += im[i+1][j-1] * mask[2][0]
			s += im[i+1][ j ] * mask[2][1]
			s += im[i+1][j+1] * mask[2][2]
			s_im[i][j] = s
	return s_im


def bordas_robert(im):
	h1 = [[ 1, 0],
	      [ 0,-1]]
	h2 = [[ 0, 1],
	      [-1, 0]]
	
	s_im = np.zeros(shape=(len(im),len(im[0])))
	
	for i,lin in enumerate(im[1:-1]):
		for j,pixel in enumerate(lin[1:-1]):
			h  = im[i-1][j-1] * h1[0][0]
			h += im[i-1][ j ] * h1[0][1]
			h += im[ i ][j-1] * h1[1][0]
			h += im[ i ][ j ] * h1[1][1]
			
			v  = im[i-1][j-1] * h2[0][0]
			v += im[i-1][ j ] * h2[0][1]
			v += im[ i ][j-1] * h2[1][0]
			v += im[ i ][ j ] * h2[1][1]
			
			s_im[i][j] = h+v
	return s_im

def bordas_prewitt(im):
	mask1 = [[-1,-1,-1],
		     [ 0, 0, 0],
		     [ 1, 1, 1]]
	mask2 = [[-1, 0, 1],
		     [-1, 0, 1],
		     [-1, 0, 1]]
	
	s_im = np.zeros(shape=(len(im),len(im[0])))
	
	for i,lin in enumerate(im[1:-1]):
		for j,pixel in enumerate(lin[1:-1]):
			h  = im[i-1][j-1] * mask1[0][0]
			h += im[i-1][ j ] * mask1[0][1]
			h += im[i-1][j+1] * mask1[0][2]
			h += im[ i ][j-1] * mask1[1][0]
			h += im[ i ][ j ] * mask1[1][1]
			h += im[ i ][j+1] * mask1[1][2]
			h += im[i+1][j-1] * mask1[2][0]
			h += im[i+1][ j ] * mask1[2][1]
			h += im[i+1][j+1] * mask1[2][2]
			
			v  = im[i-1][j-1] * mask2[0][0]
			v += im[i-1][ j ] * mask2[0][1]
			v += im[i-1][j+1] * mask2[0][2]
			v += im[ i ][j-1] * mask2[1][0]
			v += im[ i ][ j ] * mask2[1][1]
			v += im[ i ][j+1] * mask2[1][2]
			v += im[i+1][j-1] * mask2[2][0]
			v += im[i+1][ j ] * mask2[2][1]
			v += im[i+1][j+1] * mask2[2][2]
			
			s_im[i][j] = h+v
	return s_im


def bordas_sobel(im):
	mask1 = [[-1,-2,-1],
		     [ 0, 0, 0],
		     [ 1, 2, 1]]
	mask2 = [[-1, 0, 1],
		     [-2, 0, 2],
		     [-1, 0, 1]]
	
	s_im = np.zeros(shape=(len(im),len(im[0])))
	
	for i,lin in enumerate(im[1:-1]):
		for j,pixel in enumerate(lin[1:-1]):
			h  = im[i-1][j-1] * mask1[0][0]
			h += im[i-1][ j ] * mask1[0][1]
			h += im[i-1][j+1] * mask1[0][2]
			h += im[ i ][j-1] * mask1[1][0]
			h += im[ i ][ j ] * mask1[1][1]
			h += im[ i ][j+1] * mask1[1][2]
			h += im[i+1][j-1] * mask1[2][0]
			h += im[i+1][ j ] * mask1[2][1]
			h += im[i+1][j+1] * mask1[2][2]
			
			v  = im[i-1][j-1] * mask2[0][0]
			v += im[i-1][ j ] * mask2[0][1]
			v += im[i-1][j+1] * mask2[0][2]
			v += im[ i ][j-1] * mask2[1][0]
			v += im[ i ][ j ] * mask2[1][1]
			v += im[ i ][j+1] * mask2[1][2]
			v += im[i+1][j-1] * mask2[2][0]
			v += im[i+1][ j ] * mask2[2][1]
			v += im[i+1][j+1] * mask2[2][2]
			
			s_im[i][j] = h+v
	return s_im



if __name__ == "__main__":
	#image = misc.imread("../images/lena.tif")
	image = misc.imread("image.png")
	#image = [[i+j for i in range(10)] for j in range(10)]
	
	#print "gerando imagem em tons de cinza"
	#image = gray(image)
	#print len(image),len(image[0])
	
	#plt.imshow(image,cmap=plt.cm.gray)
	#plt.show()
	
	print "suavizando imagem"
	
	s_im = bordas_sobel(image)
	
	plt.subplot(211)
	plt.imshow(image,cmap=plt.cm.gray)
	#plt.show()
	plt.subplot(212)
	plt.imshow(s_im,cmap=plt.cm.gray)
	
	plt.show()
	
	#---------------
	
	
	
	
	
	
	
	
	
	
	