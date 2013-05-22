#! /usr/bin/env python
# -*- coding:utf-8 -*-

import argparse
import copy
import matplotlib.pyplot as plt
import numpy as np
import scipy
import scipy.misc as misc
import sys

def save_img(image=None):
	"""
		Salva uma imagem recebida ou a plotagem
		contida no buffer, além de mostrar a
		imagem ou o buffer.
	"""
	if args.save:
		if image == None:
			plt.savefig(args.save[0])
		else: 
			misc.imsave(args.save[0],image)
		print "Imagem salva como:",args.save[0]
	
	if args.show:
		if image != None:
			plt.imshow(image,cmap=plt.cm.gray)
		plt.show()


def gray(image, negative = False):
	"""
		Gera uma imagem em tons de cinza
		ou o negativo da imagem recebida
	"""
	_im = copy.deepcopy(image)
	for row, l in enumerate(image):
		for col, pixel in enumerate(l):
			if negative:
				_im[row][col] = 255 - sum(pixel)/ 3
			else:
				_im[row][col] = np.sum(pixel) / 3
	return _im


def histogram(im):
	"""
		Gera o histograma de uma imagem
	"""
	hist = [0.0 for i in range(256)]
	
	for row, l in enumerate(im):
		for col, pixel in enumerate(l):
			hist[pixel[0]] += 1
	return hist


def histograma_acumulado(im):
	"""
		Gera o histograma acumulado	a partir
		do histograma normal de uma imagem
	"""
	hist = histogram(im)
	for i in range(1,len(hist)):
		hist[i] += hist[i-1]
	return hist


def normalize(im, hist):
	"""
		Faz a normalização de um histograma
		com base nas dimensões de uma imagem
	"""
	n = float(len(im[0]) * len(im))
	for i, h in enumerate(hist):
		hist[i] /= n
	return hist


def gen_img_hist(img, acumulated=False):
	"""
		Faz a plotagem de uma imagem e
		seus respectiovos histogramas, em
		suas formas comum e normalizada
	"""
	if acumulated: h = histograma_acumulado(img)
	else: h = histogram(img)
	
	plt.subplot(311)
	plt.imshow(img)
	
	plt.subplot(312)
	x = [i for i in range(len(h))]
	plt.bar(x,h)
	
	plt.subplot(313)
	hn = normalize(img,h)
	plt.bar(x,hn)

def contraste(image,c,d):
	c_im = copy.deepcopy(image)
	a = image.min()
	b = image.max()
	
	for row,l in enumerate(image):
		for col, pixel in enumerate(l):
			c_im[row][col] = ( (pixel[0] - a) * ( (d - c) / float(b - a) ) ) + c
	
	return c_im

def operador_logaritmico(image):
	lg = copy.deepcopy(image)
	R = image.max()
	c = 255 / float(np.log10( 1 + R ))
	
	for row, line in enumerate(image):
		for col, pixel in enumerate(line):
			lg[row][col] = c * np.log10( 1 + pixel[0])
	return lg

def operador_potencia(image,c,gama):
	pt = copy.deepcopy(image)
	
	for row, line in enumerate(image):
		for col, pixel in enumerate(line):
			pt[row][col] = c * ( pixel[0] ** gama )
	return pt


def gen_parser():
	parser = argparse.ArgumentParser(description = "Processamento de Imagens - Atividade 1")
	
	parser.add_argument("input_file",  help="nome do arquivo de entrada")
	
	parser.add_argument("-s","--save",      metavar = "FILE",          nargs = 1, help="salva a imagem resultante com o nome 'FILE'")
	parser.add_argument("-c","--contraste", metavar = "N", type=int,   nargs = 2, help="contraste")
	parser.add_argument("-p","--potencia",  metavar = "N", type=float, nargs = 2, help="potência")
	
	parser.add_argument("-g","--gray",         action='store_true', help="imagem carregada em tons de cinza")
	parser.add_argument("-hist","--histogram", action='store_true', help="histograma")
	parser.add_argument("-a","--acumulated",   action='store_true', help="histograma acumulado")
	parser.add_argument("-n","--negative",     action='store_true', help="negativo")
	parser.add_argument("-log","--logaritmo",  action='store_true', help="logaritmo")
	parser.add_argument("-O","--otsu",         action='store_true', help="Otsu")
	parser.add_argument("-e","--equalization", action='store_true', help="Equalização")
	parser.add_argument("-S","--show",         action='store_true', help="mostra a imagem final")
	
	return parser.parse_args()


if __name__ == "__main__" :
	
	args = gen_parser()
	
	image = misc.imread(args.input_file)
	
	if not args.gray:
		print "Gerando imagem",args.input_file,"em tons de cinza"
		image = gray(image)
		print "Imagem gerada em tons de cinza"
		save_img(image=image)
	
	
	if args.histogram:
		print "Gerando Histograma."
		gen_img_hist(image)
		print "Histograma Concluido."
		save_img()
	
	
	if args.acumulated:
		print "Gerando Histograma Acumulado."
		gen_img_hist(image,acumulated=True)
		print "Histograma Acumulado Concluido."
		save_img()
	
	
	if args.negative:
		print "Gerando Imagem Negativa."
		neg = gray(image,negative=True)
		print "Imagem Negativa Concluida."
		save_img(image=neg)
	
	
	if args.contraste:
		print "Ajustando Contraste Para Intervalo Entre",args.contraste[0],"e",args.contraste[1]
		cont = contraste(image,args.contraste[0],args.contraste[1])
		print "Ajuste de Contraste Concluido"
		save_img(image=cont)
	
	if args.logaritmo:
		print "Aplicando Operador Logaritmico"
		l = operador_logaritmico(image)
		print "Operador Logaritmico Concluido"
		save_img(image=l)
	
	if args.potencia:
		print "Aplicando Operador de Potência"
		print "C =",args.potencia[0]
		print "gama =",args.potencia[1]
		pt = operador_potencia(image,args.potencia[0],args.potencia[1])
		print "Operador de Potência Concluido"
		save_img(image=pt)
	
	if args.otsu:
		print "Limiarização de Otsu\n\tNÃO IMPLEMENTADO"
	
	if args.equalization:
		print "Histograma Equalizado\n\tNÃO IMPLEMENTADO"
