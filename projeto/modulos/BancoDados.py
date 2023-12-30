from os import getenv, getcwd
from dotenv import load_dotenv
from sqlite3 import Connection, Cursor, connect


class BancoDados:
    """Classe para manipular banco de dados."""
    
    def __init__(self):
        # Diretório do projeto
        diretorio = getcwd() + '/projeto/'
        # Carrega as variáveis de ambiente a partir do arquivo .env
        load_dotenv(diretorio + 'modulos/.env')
        # Caminho completo para o banco de dados
        self._base_dados = diretorio + getenv('BASE_DADOS')
        # Conexão com o banco de dados SQLite
        self._con = connect(self._base_dados)
        # Nome da tabela no banco de dados
        self._tabela = getenv('TABELA_PROJETO')
        # Cursor para executar comandos SQL no banco de dados
        self._cursor = self._con.cursor()

    def obter_conexao(self) -> Connection:
        '''
        Retorna o objeto de conexão com o banco de dados.
        '''
        return self._con

    def obter_banco_dados(self) -> str:
        '''
        Retorna o caminho completo do banco de dados.
        '''
        return self._base_dados
    
    def obter_nome_tabela(self) -> str:
        '''
        Retorna o nome da tabela.
        '''
        return self._tabela
    
    def obter_cursor(self) -> Cursor:
        '''
        Retorna o objeto cursor para interação com o banco de dados.
        '''
        return self._cursor

    def existencia_tabela(self):
        '''
        Verifica a existência da tabela no banco de dados e a cria se não existir.
        '''
        # Query para verificar se a tabela existe
        query = f'SELECT name FROM sqlite_master WHERE type="table" AND name="{self._tabela}"'
        # Executa a query e verifica o resultado
        verificacao = self._cursor.execute(query).fetchone()

        if verificacao is None:
            # Criação da tabela se não existir
            criacao = (
                f'''CREATE TABLE {self._tabela}(
                    dt_reuniao     DATETIME,
                    dt_deliberacao DATETIME,
                    situacao       TEXT,
                    assunto        TEXT,
                    autor          TEXT,
                    proposicao     INTEGER,
                    ano            INTEGER,
                    texto          TEXT
                )'''
            )
            self._cursor.execute(criacao)
            self._con.commit()
            print('Tabela não existia e foi criada.')
        else:
            print('Tabela já existe.')

    def limpar_tabela(self):
        '''
        Limpa todos os dados da tabela.
        '''
        try:
            # Query para apagar todos os dados da tabela
            self._cursor.execute(f'TRUNCATE TABLE {self._tabela}')
            # Confirmar a alteração
            self._con.commit()
            print('Todos os dados foram removidos da tabela.')
        
        except Exception as e:
            print(f'Erro ao limpar a tabela: {e}')


if __name__ == '__main__':
    # Exemplo de uso da classe
    db = BancoDados()
    db.obter_conexao()
    db.obter_banco_dados()
    db.existencia_tabela()
    db.obter_nome_tabela()