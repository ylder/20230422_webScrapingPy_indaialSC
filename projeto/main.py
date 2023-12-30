from projeto.modulos.BancoDados import BancoDados
from projeto.modulos.CargaIngestao import Ingestao

def main(anos):
    """
    Função principal para executar a carga de proposições nos anos fornecidos.

    Argumentos:
        anos (range): Anos para os quais a carga de proposições será executada.
    """
    
    # Cria uma instância do Banco de Dados.
    db = BancoDados()

    # Obtém a conexão com o banco de dados.
    db.obter_conexao()

    # Verifica a existência da tabela no banco de dados.
    db.existencia_tabela()

    # Loop sobre os anos fornecidos para realizar a carga de proposições.
    for ano in anos:
        
        # Cria uma instância da classe de Ingestão para o ano atual.
        ing = Ingestao(ano)

        # Insere proposições no banco de dados.
        ing.inserir_proposicao()

# Define uma faixa de anos para executar a carga de proposições.
anos = range(1996, 2024, 1)

# Chama a função principal para realizar a carga de proposições nos anos fornecidos.
main(anos)