import csv
from readcsv import readcsv

CSV_FILE_PATH = "csv_test/atividade.csv"
ATIVIDADE_DICT_LIST = readcsv(CSV_FILE_PATH) # Retorna a lista de dicionário gerado a partir de atividade.csv

def show_dicts(dict_list, showkeys=False):
    """
    Função auxiliar que mostra o estado da lista de dicionários
    passada como parâmentro. Esta função tem o objetivo apenas
    de facilitar o debug
    :param dict_list:
    :return:
    """
    for dicio in dict_list:
        print(dicio)

    if showkeys:
        print("-------------------------------------------------")
        print("KEYS LIST")
        print("[", end='')
        for key in dict_list[0].keys():
            print(key, end=' ')
        print("]")
        print("-------------------------------------------------")

def create_related_csv(filedirectory, dict_list): #['id_custeio', 'nome']
    #print(filename)
    with open(filedirectory + '.csv', 'w', newline='') as csvfile:

        # Os nomes das colunas serão as chaves do primeiro dicionario
        escritor = csv.DictWriter(csvfile, fieldnames= dict_list[0].keys())
        escritor.writeheader()

        # escrevendo cada valor do diconario no arquivo .csv
        for dicio in dict_list:
            escritor.writerow(dicio)

def create_relationship(old_dict_list): # recebe a lista de dicionarios de t_atividade
    """
    Esta função tem o objetivo de montar um relacionamento entre 't_atividade' e 'custeio'.
    Neste relacionamento deve haver o ID de ambas as partes assim como o valor referente ao relacionamento
    :param old_dict_list:
    :return:
    """

    custeio_dict_list = readcsv("csv_test/custeio.csv") # lista de dicionario do custeio

    relationship_dict_list = [] # lista de dicionarios que formará o .csv do relacionamento

    for atividade_dict in old_dict_list: # Itera sobre cada dicionario da lista de atividades
        #DEBUG
        #print(atividade_dict['nome'])

        for custeio_dict in custeio_dict_list: # Itera sobre cada dicionario da lista de custeios
            """
            Plano de implementação:
            1. Estabelecer relacionamento entre todos os elementos de t_atividade e custeio ( X )
            2. Eliminar os relacionamentos que não possuam valor ( X )
            3. Tranformar os dados restantes em uma lista de dicionário para serem inseridos no .csv (  )
                3.1. Nomear as celulas da primeira linha do .csv com os cabeçalhos (  ) 
            """

            relationship_dict = {}

            # custeio_dict['id_custeio'] + "-" + custeio_dict['nome'] =
            # 'id_custeio-nome_custeio' que forma uma chave para o dicionario
            # Assim podemos recuperar o valor do custeio relcaionado a atividade

            # Se não houver um valor relacionado a uma relação entre t_atividade e custeio esta relação não deve aparecer na tabela
            # lembrando que a chave referente a cada custeio na planilha t_atividade é formada pelo id_custeio + nome_custeio
            if atividade_dict[ custeio_dict['id_custeio'] + "-" + custeio_dict['nome'] ] != "":

                relationship_dict['id_atividade'] = atividade_dict['id_atividade']
                relationship_dict['id_custeio'] = custeio_dict['id_custeio']
                relationship_dict['valor'] = atividade_dict[ custeio_dict['id_custeio'] + "-" + custeio_dict['nome'] ]

                relationship_dict_list.append(relationship_dict)
                #print(relationship_dict)

                #DEBUG
                #print("ID Atividade: " + atividade_dict['id_atividade'] + " -> " +
                #      "ID Custeio: " + custeio_dict['id_custeio'] + " " +
                #      custeio_dict['nome'] + ": " +
                #      atividade_dict[ custeio_dict['id_custeio'] + "-" + custeio_dict['nome']])
        #print("---------------------------------------------------------------------")

    #for dicio in old_dict_list:
    #    print("A atividade ID " + dicio['id_atividade'] +
    #          " '" + dicio['nome'] + "' esta relacionada ao custeio DE VALOR:" + dicio['11-passagens'])
    return relationship_dict_list

def create_rside(source_dict_list):
    """
    Será montada uma lista de dicionários baseada na primeira linha do documento csv
    Esta lista conterá apenas os cabeçalhos com prefixo numérico
    Este prefixo será a chave primaria da entidade enquanto que o restante do nome será
    o nome do custeio associada a chave
    :param source_dict_list:
    :return:
    """

    rside_dict_list = [] # Dados que formarão o .csv do custeio

    for source_dict in source_dict_list: # Montando uma lista de dicionarios a partir de cada dicionario antigo

        for chave in source_dict.keys():

            if chave[0].isnumeric(): # Precisamos apenas dos cabeçalho numerado

                (pk, value) = chave.split('-') # Separa a parte numerica do restante do cabeçalho
                rside_dict = {}
                rside_dict['id_custeio'] = pk # Mudar para nome genéricos
                rside_dict['nome'] = value

                # O ID DEVE SER UM VALOR ASSOCIADA A CHAVE id_custeio #DEBUG
                #print("{'" + custeio_dict['id_custeio'] + "' : '" + custeio_dict['nome'] + "'}", end='')
                rside_dict_list.append(rside_dict)

        break # Usaremos apenas o primeiro dicionário da lista antiga, pois precisamos apenas dos cabeçaos numerados

    return rside_dict_list

def create_lside(source_dict_list):
    """
    Cria a primeira parte, "o lado esqueerdo" do relacionaamento, baseado na lista
    de dicionarios da funte(ariunda do arquivo csv que contem todos os dados a serem divididos)
    :param source_dict_list:
    :return:
    """

    lside_dict_list = []

    for source_dict in source_dict_list: # Iterando sobre a lista de dicionário original

        lside_dict = {} # Cria um novo dicionario para cada dicionário da lista original

        for chave in source_dict.keys(): # Iterando sobre as chaves do cionario atual

            if chave[0].isnumeric() == False: # So nos interessa as chaves não numericas
                lside_dict[chave] = source_dict[chave]

        lside_dict_list.append(lside_dict)

    return lside_dict_list


# CRIANDO O CSV REFERENTE A TABELA ATIVIDADE
#atividade_solo_list = create_lside(ATIVIDADE_DICT_LIST)
#show_dicts(atividade_solo_list)
#create_related_csv('T_atividade', atividade_solo_list)

# CRIANDO O CSV REFERENTE A TABELA CUSTEIO
#custeio_dict_list = create_rside(ATIVIDADE_DICT_LIST) # TESTE PASSO 2
#show_dicts(custeio_dict_list, showkeys=False)
#create_related_csv('custeio', custeio_dict_list) # TESTE PASSO 3

#Criando o relacionamento entre as tabelas
#atividade_custeio_dict_list = create_relationship(ATIVIDADE_DICT_LIST) # TESTE PASSO 4
#show_dicts(atividade_custeio_dict_list)
#create_related_csv('atividade_custeio', atividade_custeio_dict_list)


"""
PROCEDIMENTO DE TESTE:
1. Apague tudo que estiver dentro do diretorio 'csv_test' da aplicação mantendo apenas a pasta 'backup' e o arquivo 'atividade.csv'
2. Acione a função 'create_rside' passando a lista de dicionários oriunda do arquivo 'atividade.csv'
3. Passe a lista de dicionarios retornado para a função 'create_related_csv' juntamente com o nome do arquivo desejado
    3.1. O csv a ser relacionado com 'atividade.csv' é criado, observe que o arquivo .csv aparece no mesmo diretório de 'atividade.csv'
4. Com o arquivo criado, acione 'create_relationship' passando a lista de dicionarios oriundos de 'atividade.csv'
5. Esta função retornará uma lista de dicionários que deverá ser submetida a função 'create_realated_csv'
    5.1 Verifique o diretório 'csv_test', agora temos os arquivos 'atividade.csv', 'custeio.csv' e 'atividade_custeio.csv'
    5.2 Este arquivos representam as duas partes do relacionamento N:N e o relacionamento em si
6. Agora podemos submeter estes arquivos ao modulo 'db_handler.py' para que sejam inseridos no banco de dados
    6.1 As tabelas referentes a cada arquivo csv devem estar previamente criadas com os tipos correspondentes
7. Opicionalmente você pode criar um arquivo csv que contenha apenas os dados referentes a atividade
    7.1. Acionae a função 'create_lside' passando a lista de dicionarios advinda do arquivo 'atividade.csv'
    7.2. O dicionario retornado terá os dados especificos de atividade, agora é só enviar esta lista para 'create_related_csv'
8. No final teremos os seguintes arquivos csv: um referente a atividade outro referente ao custeio e mais um referente ao relacionamento 
"""