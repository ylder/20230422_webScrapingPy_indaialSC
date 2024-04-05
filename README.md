# Extração e armazenamento de proposições (indicações) da Câmara legislativa de Indaial-SC


## 1 Descrição do projeto

	Sistema de Coleta, armazenamento e atualizações incrementais de dados das
	proposições de vereadores da prefeitura de Indaial-SC, diretamente de seu
	site oficial, em um banco de dados sqlite.

	Projeto foi inspirado pelo que foi desenvolvido por Joviano, na sua "Maratona
	Python com Power BI". A estrutura do projeto não seguiu o que foi costruído
 	nessa maratona, pois se desenvolveu uma estrutura de sistema, com a modularização
  	dos códigos.

## 2 Ferramentas e técnicas utilizadas
	
	VS Code
	Jupyter Notebook
	Python 3.9.10
	SQLite3

## 3 Objetivos do autor

	• Aplicar programação orientada a objetos;

	• Ter 1º contato com webscraping;

	• aprimorar conhecimento e aumentar complexidade ao utilizar loops;

	• lidar melhor com erros de execução, tornando-os parte integrante da mecânica
	do código;

	• explorar o uso da solução Sqlite3, integrada ao Python.

## 4 Funcionamento do projeto

	O projeto foi construído de maneira modularizada, com arquivos (e classes)
 	que são responsáveis pelas 3 principais atividades para executar o objetivo
  	do projeto: construção e conexão com banco de dados, WebScraping dos dados
   	do site da cidade e ingestão dos dados no banco.

	Feito isto, a lógica do algorítmo é a apresentada no fluxograma a seguir:

![Imagem1](https://github.com/ylder/20230422_webScrapingPy_indaialSC/assets/126031404/9a3750fb-03d1-4b6e-beaf-18363749a3de)

	Para poder executar o código com sucesso, é necessário configurar o arquivo
	'src/.env'. Nele contém 3 variáveis:
		
		USER_AGENT = 'Seu User-Agent' (Seu User-Agent do seu navegador)
		BASE_DADOS = 'SeuBancoDados_SQLite3.db' (Nome do banco de dados)
		TABELA_PROJETO = 'sua_tabela' (Nome da tabela a armezar os dados)

	O arquivo 'src/main.py' ativa a execução do algoritmo mencionado, sendo
	necessário informar o período desejado em anos.

## 5 Considerações

	O código possui comentários e explicações sobre seu próprio funcionamento.
	Necessário esse aprofundamento para que haja completa compreensão do projeto.
