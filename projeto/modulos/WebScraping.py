from os import getenv
from requests import get
from bs4 import BeautifulSoup
from pandas import DataFrame, concat, to_datetime


class WebScrapping:
    """Classe para realizar coleta dos dados do site de interesse."""
    
    def __init__(self, ano: int = None, num_proposicao: int = None, tipo_proposicao: int = 1, decode: str = 'latin1'):
        """
        Inicializa a classe de Web Scraping.

        Argumentos:
            ano (int): Ano em que as proposições foram realizadas.
            num_proposicao (int): Número da proposição.
            tipo_proposicao (int): Tipo da proposição (indicação, requerimento, moção).
            decode (str): Decodificação para transformar bytes do HTML em texto do site.
        """
        super().__init__()
        self._headers = {'User-Agent': getenv('USER_AGENT')}
        self._ano = ano
        self._num_proposicao = num_proposicao
        self._tipo_proposicao = tipo_proposicao
        self._decode = decode

    def html_site(self, url: str) -> BeautifulSoup:
        """
        Obtém o conteúdo HTML de uma URL e retorna um objeto BeautifulSoup.

        Argumentos:
            url (str): A URL do site.

        Retorna:
            BeautifulSoup: Objeto contendo a estrutura HTML parseada.
        """
        try:
            # Faz a requisição para acessar o HTML do link.
            requisicao = get(url, headers=self._headers, timeout=4)
            
            # Converte o conteúdo do site de bytes para texto.
            resposta_bytes = requisicao.content
            html_pagina = resposta_bytes.decode(self._decode)
            
            # Parseia o HTML e retorna um objeto BeautifulSoup.
            return BeautifulSoup(html_pagina, 'html.parser')
        
        except:
            pass

    def _existencia_proposicao(self) -> BeautifulSoup:
        """
        Verifica a existência de uma proposição e retorna o HTML correspondente.

        Retorna:
            BeautifulSoup: Objeto contendo a estrutura HTML parseada da proposição.

        Lança:
            ValueError: Se a proposição não existir.
        """
        # Constrói a URL com base nos parâmetros fornecidos.
        site = f'https://www.legislador.com.br//LegisladorWEB.ASP?WCI=ProposicaoTexto&ID=3&TPProposicao={self._tipo_proposicao}&nrProposicao={self._num_proposicao}&aaProposicao={self._ano}'
        
        # Obtém o HTML do site.
        html = self.html_site(site)

        # Condições para verificar a existência da proposição.
        condicoes = (
            (html.find_all('dt') == []) or
            ('Proposição não existente' in str(html))
        )

        # Se as condições são atendidas, lança um ValueError informando que a proposição não existe.
        if condicoes:
            raise ValueError("A proposição não existe.")
        else:
            # Se a proposição existe, retorna o HTML correspondente.
            return html

    def dados_proposicao(self) -> DataFrame:
        """
        Extrai dados da proposição do HTML e retorna um DataFrame estruturado.

        Retorna:
            DataFrame: DataFrame contendo os dados da proposição.
        """
        # Obtém o HTML da proposição verificando a existência.
        html = self._existencia_proposicao()

        # Define as colunas do DataFrame.
        cols = ['Reunião', 'Deliberação', 'Situação', 'Assunto', 'Autor', 'Proposição', 'Ano', 'Texto']
        df_estrutural = DataFrame(columns=cols)

        # Obtém as tags HTML relevantes.
        html_colunas = html.find_all('dt')
        html_linha = html.find_all('dd')

        # Cria um DataFrame temporário com os dados extraídos das tags.
        dados = DataFrame(
            columns=[i.get_text() for i in html_colunas],
            data=[[i.get_text() for i in html_linha]]
        )

        # Adiciona informações adicionais que não estão nas tags consultadas.
        dados['Proposição'] = self._num_proposicao
        dados['Ano'] = self._ano
        dados['Texto'] = html.p.get_text()

        # Concatena os DataFrames temporários.
        df = concat([df_estrutural, dados])

        # Ajusta os tipos de dados das colunas.
        for i in ['Reunião', 'Deliberação']:
            df[i] = to_datetime(df[i], dayfirst=True, errors='coerce')

        return df.astype(
            {
                'Reunião': str,
                'Deliberação': str,
                'Situação': str,
                'Assunto': str,
                'Autor': str,
                'Proposição': int,
                'Ano': int,
                'Texto': str
            }
        )


if __name__ == '__main__':
    # Exemplo de uso da classe
    ws = WebScrapping(2007, 3)
    ws.html_site('https://www.legislador.com.br//LegisladorWEB.ASP?WCI=ProposicaoTexto&ID=3&TPProposicao=1&nrProposicao=300&aaProposicao=2007')
    ws.dados_proposicao()