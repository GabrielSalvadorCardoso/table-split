from readcsv import readcsv
from connection_factory import get_connection
import psycopg2

CSV_PATH = 'controle_codigo/codigo_contribuidor.csv' # localização do arquivo a ser convertido para banco de dados
TABLE_NAME = 'codigo_contribuidor'

def treat_value(value):
    """
    Esta função tem a função de tratar cada dado a ser inserido no comando insert
    para que estejam no formato adequado para execução do comando pelo banco de dados
    :param value:
    :return:
    """

    if value.isnumeric() == False: # se não for numerico...
        if value.capitalize() == "True" or value.capitalize() == "False": # ..e se a string representar um boolean...
            value = value.capitalize()
        elif value == '': # ...ou se a string for vazia...
            value = "null"
        else:
            # se não for numerico, não representar um booleano ou não for uma string vazia,
            # apenas coloque o valor entre aspas simples
            value = "'" + value + "'"

    return value


def construct_insert_list(dict_list, table_name):
    """
    Recebe uma lista de dicionários contendo os dados
    originados a partir do arquivo .csv e faz o devido
    tratamento de tipos para a construção do comando insert
    :param dict_list:
    :return:
    """
    insert_list = []

    for dicionario in dict_list: # Processando o dicionario atual
        # A cada dicionário de 'dict_list', 'key_list' e 'values_list' são refitos
        keys_list = []
        values_list = []

        for chave in dicionario.keys(): # Peocessando a lista de chaves e valores do dicionário atual
            keys_list.append(chave)

            # Trata cada valor separadamente antes de adicioná-lo na lista de valores
            dicionario[chave] = treat_value( dicionario[chave] )

            values_list.append(dicionario[chave])

        # concatena a lista de chaves no formato(chave1, chave2, ...). O mesmo para a lista de valores
        concat_keys = ", ".join(keys_list)
        concat_values = ", ".join(values_list)

        insert_list.append("insert into public." + table_name + " (" + concat_keys + ") values(" + concat_values + ");" )

    # DEBUG
    # for insert in insert_list:
    #    print(insert)

    return insert_list


def execute_insert_list(insert_list):
    with get_connection() as connection:
        cursor = connection.cursor() # Gera um cursor

        for sql_insert in insert_list:

            try:

                cursor.execute(sql_insert) # Devemos executar o comando pelo cursor
                print("Registro inserido com sucesso!")

            except psycopg2.IntegrityError as ViolacaoPK:

                print("--------------------------------------------------------------------------------------------------------------------------------")
                print("Chave primaria já existe: " + str(ViolacaoPK), end='')
                print("Comando excluido da lista:\n" + sql_insert)

                # Retira o comando problematico da lista e reexecuta a função
                insert_list.remove(sql_insert)
                execute_insert_list(insert_list)

            except psycopg2.InternalError as ErroInterno:
                print("Erro interno: " + str(ErroInterno))

        print("--------------------------------------------------------------------------------------------------------------------------------")

# Recupera uma lista de dicionários com os dados a serem inseridos no banco...
insert_list = construct_insert_list( readcsv(CSV_PATH), TABLE_NAME) # ...e constroi uma lista de inserts com esta lista
execute_insert_list(insert_list)


"""
TIPOS DE DADOS A SEREM TRATADOS
    - Com aspas
        1. string
        2. date
    - Sem aspas
        1. Numericos
        2. boolean
        
OBS: Dados do CSV que tenham alguma função dentro dos comandos do banco de dados(como aspas) devem ser tratados, por exemplo:
- Tratar aspas simple substituindo-as por aspas duplas
"""