from time import sleep
from pandas import read_sql_query
from projeto.modulos.BancoDados import *
from projeto.modulos.WebScraping import *


class Ingestao:
    """Classe para realizar a ingestão de dados no banco de dados."""

    def __init__(self, ano):
        """
        Inicializa a classe Ingestao.

        Parâmetros:
        - ano (int): O ano para o qual a ingestão será realizada.
        """
        self._ano = ano
        self._num_proposicao = self.ultima_proposicao()
        self.tabela = None
        self.con = None
        self.cursor = None

    def conectar_banco(self):
        """
        Conecta ao banco de dados e define os atributos de conexão e cursor.
        """
        db = BancoDados()
        self.tabela = db.obter_nome_tabela()
        self.con = db.obter_conexao()
        self.cursor = db.obter_cursor()

    def ultima_proposicao(self):
        """
        Obtém o número da última proposição do ano no banco de dados.

        Retorna:
        - int: O número da última proposição.
        """
        self.conectar_banco()
        query = f"SELECT MAX(proposicao) FROM {self.tabela} WHERE ano = {self._ano}"
        return read_sql_query(query, self.con).iloc[0, 0]

    def scrapper(self):
        """
        Realiza web scraping para obter dados das proposições.

        Retorna:
        - DataFrame: Um DataFrame contendo os dados das proposições.
        """
        ws = WebScrapping(self._ano, self._num_proposicao)
        return ws.dados_proposicao()

    def inserir_proposicao(self, erros_admissiveis: int = 3, seg_espera: float = 1):
        """
        Insere proposições no banco de dados.

        Parâmetros:
        - erros_admissiveis (int): Número de erros admissíveis durante a inserção.
        - seg_espera (float): Tempo de espera entre as consultas.
        """
        # Conecta ao banco de dados
        self.conectar_banco()

        # Inicializa variáveis de controle de erros e contagem de consultas
        erros_ocorridos = 0
        qtd_consultas = 1
        
        # Imprime mensagem indicando o ano selecionado
        print(f'Ano {self._ano} selecionado.')
        
        # Executa o loop enquanto erros_ocorridos for menor que erros_admissiveis
        while erros_ocorridos < erros_admissiveis:

            try:
                # Incrementa o número da proposição a ser consultada
                if self._num_proposicao is None:
                    self._num_proposicao = 1
                
                else:
                    self._num_proposicao = int(self._num_proposicao) + 1

                # Imprime informações sobre a consulta atual
                print(f'{qtd_consultas} consulta(s) realizada(s). Proposicao {self._num_proposicao}')

                # Obtém os dados da proposição usando o WebScrapping
                df = self.scrapper()

                # Itera sobre as linhas do DataFrame e insere os dados no banco de dados
                for i, linha in df.iterrows():

                    self.cursor.execute(
                        f"INSERT INTO {self.tabela} VALUES( ?, ?, ?, ?, ?, ?, ?, ? )",
                        (
                            linha['Reunião'],
                            linha['Deliberação'],
                            linha['Situação'],
                            linha['Assunto'],
                            linha['Autor'],
                            linha['Proposição'],
                            linha['Ano'],
                            linha['Texto']
                        )
                    )

                # Commita as alterações no banco de dados
                self.con.commit()

                # Reseta a contagem de erros
                erros_ocorridos = 0

            except Exception as e:
                # Trata exceções relacionadas à extração de proposições.
                erros_ocorridos += 1
                print(f'Erro ao extrair proposições: {e}')
                if erros_ocorridos == 3:
                    print('Para o respectivo ano, não há mais proposições a inserir.')
                pass

            # Incrementa a contagem de consultas e aguarda um intervalo de tempo
            qtd_consultas += 1
            sleep(seg_espera)


if __name__ == '__main__':
    bd = BancoDados()
    bd.obter_conexao()
    bd.existencia_tabela()
    
    anos = [2023]
    
    for _ in anos:
        Ingestao(_).inserir_proposicao()
    else:
        print()