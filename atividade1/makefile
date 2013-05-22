DIR = ""
lena:
	@make -s run DIR="../images" IN="lena" TYPE="tif"

run:
	@echo "Iniciando Processamento de Imagens"
	@./main.py $(DIR)/$(IN).$(TYPE)        -s $(IN)_gray.png		# Gerar imagem em tons de cinza
	@./main.py $(IN)_gray.png -g -hist     -s $(IN)_hist.png		# Gerar histograma
	@./main.py $(IN)_gray.png -g -a        -s $(IN)_hist_acumulado.png	# Gerar histograma acumulado
	@./main.py $(IN)_gray.png -g -n        -s $(IN)_neg.png			# Gerar negativo
	@./main.py $(IN)_gray.png -g -c 0 90   -s $(IN)_cont.png		# ajuste de contraste
	@./main.py $(IN)_gray.png -g -log      -s $(IN)_log.png			# operador logaritmico
	@./main.py $(IN)_gray.png -g -p 2 0.5  -s $(IN)_pot.png			# operador de potência
	@./main.py $(IN)_gray.png -g -O        -s $(IN)_otsu.png		# limiarização de otsu
	@./main.py $(IN)_gray.png -g -e        -s $(IN)_hist_eq.png		# equalização de histograma
