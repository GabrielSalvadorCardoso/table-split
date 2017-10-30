import csv

CSV_COPY_PATH = 'csv_test/codigo.csv'

"""
def writecsv(lines_list):
    with open(CSV_COPY_PATH, 'w') as csvcopy:
        csvwriter = csv.writer(csvcopy)
        for line in lines_list:
            csvwriter.writerow(line)


with open(CSV_PATH, 'r') as csvfile:
    lines_list = csv.reader(csvfile)

    writecsv(lines_list)
    #for line in lines_list:
        #print(line)
"""
def readcsv(csv_path):
    """
    Esta função apenas lê o documento .csv e retorna uma lista de dicionários.
    Cada dicionário desta lista contém os dados de cada linha do .csv indexado
    pelas chaves da primeira linha do documento
    :param csv_path:
    :return:
    """

    with open(csv_path, 'r') as csvfile:

        # DictReader retorna um conjunto(iterável) de dicionarios no qual é possivel,
        # em cada dicionario, recuperar um valor específico a partir de uma chave.
        # Estas chaves estão presentes em uma lista de chaves(objeto_dict.keys()) de
        # cada dicionario do conjunto presente em DictReader. A lista de chaves é montada
        # a partir da primeira linha do arquivo .csv

        dict_reader = csv.DictReader(csvfile)
        dict_list = []

        for dicionario in dict_reader:
            dict_list.append(dicionario)

        return dict_list


#DEBUG
#codigo_dict_list = readcsv(CSV_COPY_PATH)
#for dicio in codigo_dict_list:
#    print(dicio)
#import splitter
#splitter.show_dicts(codigo_dict_list)