import csv
from readcsv import readcsv

CSV_FILE_PATH = "csv_test/t_atividade.csv"
OLD_DICT_LIST = readcsv(CSV_FILE_PATH) # Retorna a lista de dicionário gerado a partir do csv

#DEBUG
#for dicio in OLD_DICT_LIST:
    #print(dicio)

def create_relationship(old_dict_list): # recebe a lista de dicionarios de t_atividade
    """
    Esta função tem o objetivo de montar um relacionamento entre 't_atividade' e 'custeio'.
    Neste relacionamento deve haver o ID de ambas as partes assim como o valor referente ao relacionamento
    :param old_dict_list:
    :return:
    """

    custeio_dict_list = readcsv("csv_test/testando.csv") # lista de dicionario do custeio

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

                #relationship_dict_list.append(relationship_dict)
                print(relationship_dict)

                #DEBUG
                #print("ID Atividade: " + atividade_dict['id_atividade'] + " -> " +
                #      "ID Custeio: " + custeio_dict['id_custeio'] + " " +
                #      custeio_dict['nome'] + ": " +
                #      atividade_dict[ custeio_dict['id_custeio'] + "-" + custeio_dict['nome']])
        #print("---------------------------------------------------------------------")

    #DEBUG
    for dicio in relationship_dict_list:
        print(dicio)

    #for dicio in old_dict_list:
    #    print("A atividade ID " + dicio['id_atividade'] +
    #          " '" + dicio['nome'] + "' esta relacionada ao custeio DE VALOR:" + dicio['11-passagens'])



def create_rside(old_dict_list):
    """
    Será montada uma lista de dicionários baseada na primeira linha do documento csv
    Esta lista conterá apenas os cabeçalhos com prefixo numérico
    Este prefixo será a chave primaria do custeio enquanto que o restante do nome será
    o nome do custeio associada a chave
    :return:
    """

    custeio_dict_list = [] # Dados que formarão o .csv do custeio

    for old_dicio in old_dict_list:
        """
        Montando uma lista de dicionarios a partir de cada dicionario antigo
        """

        for chave in old_dicio.keys():

            if chave[0].isnumeric(): # Precisamos apenas dos cabeçalho numerado

                (pk, value) = chave.split('-') # Separa a parte numerica do restante do cabeçalho
                custeio_dict = {}
                custeio_dict['id_custeio'] = pk # Mudar para nome genéricos
                custeio_dict['nome'] = value

                # O ID DEVE SER UM VALOR ASSOCIADA A CHAVE id_custeio #DEBUG
                #print("{'" + custeio_dict['id_custeio'] + "' : '" + custeio_dict['nome'] + "'}", end='')
                custeio_dict_list.append(custeio_dict)

        break # Usaremos apenas o primeiro dicionário da lista antiga, pois precisamos apenas dos cabeçaos numerados

    return custeio_dict_list









"""
    for dicionario in dict_list: # Manipulando o dicionario atual(da antiga lista de dicionarios)
        # Geraremos um novo dicionário para cada dicionário antigo
        new_dict = {}
        new_dict['pk'] = "" # Coluna da chave primaria
        new_dict['<attribute>'] = "" # Colunas dos atributos

        for chave in dicionario.keys(): # Iterando pelas chaves do dicionario atual

            if chave[0].isnumeric(): # Verifica se o primeiro caracter da chave atual é numérico

                # Se for numérico, pegamos a parte numérica para ser o id,
                # e o restante para ser a instância relacionada ao id
                ( new_dict['pk'] , new_dict['<attribute>'] ) = chave.split('-')

                #DEBUG
                #print( new_dict['pk'] + " : " + new_dict['<attribute>'])

                new_dict_list.append(new_dict)

        #print(new_dict_list)
        #print("----------------------------------------")
"""

"""
# Criando a tabela relacionada
custeio_dict_list = create_rside(OLD_DICT_LIST)
for custeio in custeio_dict_list:
    print(custeio)

with open('csv_test/testando.csv', 'w') as csvfile:
    escritor = csv.DictWriter(csvfile, fieldnames=['id_custeio', 'nome'])
    escritor.writeheader()

    for custeio in custeio_dict_list:
        escritor.writerow(custeio)
"""

#Criando o relacionamento entre as tabelas
create_relationship(OLD_DICT_LIST)