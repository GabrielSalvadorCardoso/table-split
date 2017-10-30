from readcsv import readcsv
from splitter import show_dicts, create_related_csv
import csv

CSV_FILE_PATH = "controle_codigo/controle_codigo.csv"
def split_nn(csv_file_path, left_csv=['left_side'], right_csv=['right_side'], relationship_csv=['relationship']):
    """
    Cada parâmetro recebido acima é uma lista, onde o primeiro elemento será o nome
    do CSV correspondente
    :param left_csv:
    :param right_csv:
    :param relationship_csv:
    :return:
    """

    with open(csv_file_path, 'r') as complete_csv_file:
        complete_csv_data = csv.DictReader(complete_csv_file)

        # O primeiro item de cada lista é o nome do respectivo csv a ser gerado

        left_csv_name = left_csv[0]
        left_csv.remove(left_csv[0])
        right_csv_name = right_csv[0]
        right_csv.remove(right_csv[0])
        relationship_csv_name = relationship_csv[0]
        relationship_csv.remove(relationship_csv[0])

        left_dict_list = []
        right_dict_list = []
        relationship_dict_list = []

        for registros in complete_csv_data: # Iterando sobre a lista de dicioários retornados pelo CSV
            # Um novo dicionario é criado para cada dicionario do arquivo original
            left_dict = {}
            right_dict = {}
            relationship_dict = {}

            for chave in registros.keys(): # Iterando sobre a lista de chaves de cada dicionário
                """
                Deve-se ainda eliminar as linha com id's iguais em cada lado do relacionamento,
                mas deve-se manter a repetição de id's no relacionamento
                """

                if chave in left_csv: # Mostra apenas os valores relacionados as chaves referentes a parte 'esquerda' do relacionamento
                    #registros['id_' + left_csv_name]
                    left_dict[chave] = registros[chave]
                if chave in right_csv:
                    right_dict[chave] = registros[chave]
                if chave in relationship_csv:
                    relationship_dict[chave] = registros[chave]

            # Adicionando os dicionarios recém criados as respectivas listas de dicionarioss
            #if left_dict not in left_dict_list:
            left_dict_list.append(left_dict)
            #if right_dict not in right_dict_list:
            right_dict_list.append(right_dict)
            #if relationship_dict not in relationship_dict_list:
            relationship_dict_list.append(relationship_dict)

        #DEBUG
        print("Left side of relationship")
        left_dict_list = remove_duplicated_instances(left_dict_list, 'id_' + left_csv_name.split('/')[1])
        show_dicts(left_dict_list)
        print("Right side of relationship")
        right_dict_list = remove_duplicated_instances(right_dict_list, 'id_' + right_csv_name.split('/')[1])
        show_dicts(right_dict_list)
        print("The relationship")
        show_dicts(relationship_dict_list)

        create_related_csv(left_csv_name, left_dict_list)
        create_related_csv(right_csv_name, right_dict_list)
        create_related_csv(relationship_csv_name, relationship_dict_list)

def remove_duplicated_instances(dict_list, id_column):
    """
    Função que recebe uma lista dicionario e remove os dicionários duplicados da lista.
    Isso é possível apenas se for passado 'id_column' como argumento pois a função usa
    este id como critério para determinar se cada registro esta duplicado ou não
    :param dict_list:
    :param id_column:
    :return:
    """

    id_set = set() #SE ESTIVER NA LISTA VC PODE ENTRAR
    new_dict_list = []

    for dicionario in dict_list:
        id_set.add(int(dicionario[id_column]))

    for dicionario in dict_list:
        if int(dicionario[id_column]) in id_set:
            new_dict_list.append(dicionario)
            id_set.discard( int(dicionario[id_column]) )

    return new_dict_list


split_nn(CSV_FILE_PATH, left_csv=['controle_codigo/codigo', 'id_codigo', 'titulo_codigo', 'codigo', 'descricao'],
         right_csv=['controle_codigo/contribuidor', 'id_contribuidor', 'login_contribuidor', 'nome_contribuidor', 'e-mail'],
         relationship_csv=['controle_codigo/codigo_contribuidor', 'id_codigo', 'id_contribuidor'])