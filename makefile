DIR = ""

run: atividade_2

atividade_1:
	@echo "=================[ ATIVIDADE 1 ]=================="
	@make -s run_atividade_1 DIR="atividade1" IN="lena" TYPE="tif"
	@make -s run_atividade_1 DIR="atividade1" IN="DSC_0048" TYPE="jpg"
	@make -s run_atividade_1 DIR="atividade1" IN="DSC_0050" TYPE="jpg"

run_atividade_1:
	@echo "------[ INICIANDO PROCESSAMENTO DE IMAGENS ]------"
	@echo "---------[ IMAGEM : $(IN).$(TYPE) ]---------"
	@./$(DIR)/main.py images/$(IN).$(TYPE)                     -s $(DIR)/cinza/$(IN)_gray.png			# Gerar imagem em tons de cinza
	@./$(DIR)/main.py $(DIR)/cinza/$(IN)_gray.png -g -hist     -s $(DIR)/histograma/$(IN)_hist.png			# Gerar histograma
	@./$(DIR)/main.py $(DIR)/cinza/$(IN)_gray.png -g -a        -s $(DIR)/histograma/$(IN)_hist_acumulado.png		# Gerar histograma acumulado
	@./$(DIR)/main.py $(DIR)/cinza/$(IN)_gray.png -g -n        -s $(DIR)/negativo/$(IN)_neg.png			# Gerar negativo
	@./$(DIR)/main.py $(DIR)/cinza/$(IN)_gray.png -g -c 0 90   -s $(DIR)/contraste/$(IN)_cont.png			# ajuste de contraste
	@./$(DIR)/main.py $(DIR)/cinza/$(IN)_gray.png -g -log      -s $(DIR)/logaritmo/$(IN)_log.png			# operador logaritmico
	@./$(DIR)/main.py $(DIR)/cinza/$(IN)_gray.png -g -p 2 0.5  -s $(DIR)/potencia/$(IN)_pot.png			# operador de potência
	@./$(DIR)/main.py $(DIR)/cinza/$(IN)_gray.png -g -O        -s $(DIR)/otsu/$(IN)_otsu.png			# limiarização de otsu
	@./$(DIR)/main.py $(DIR)/cinza/$(IN)_gray.png -g -e        -s $(DIR)/equalizacao/$(IN)_hist_eq.png		# equalização de histograma

atividade_2:
	@echo "=================[ ATIVIDADE 2 ]=================="