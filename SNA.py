import pandas as pd

def note_counter():
    f_input = open('raw_data_60.csv', 'r', encoding='utf8')
    lines = f_input.readlines()

    note_list = []
    for line in lines:
        line = line.strip()
        line = line.lower()
        notes = line.split(',')[2]
        notes_split = notes.split(';')
        for note in notes_split:
            note = note.split('_')[0]
            note_list.append(note.strip())

    note_set = set(note_list)
    note_list = list(note_set)
    note_list.sort()



    f_output = open('note_list_60.txt', 'w', encoding='utf8')
    for element in note_list:
        f_output.write(element + '\n')




def note_matrix_uci():
    f_input = open('raw_data.csv', 'r', encoding='utf8')
    lines = f_input.readlines()

    note_cooccur_counter = {}

    for line in lines:
        line = line.split(',')[2]
        line = line.strip().lower()
        note_lists = line.split(';')
        note_list = []
        for note in note_lists:
            note_list.append(note.split('_')[0])
        for i in range(len(note_list)):
            for j in range(i+1, len(note_list)):
                if note_list[i] > note_list[j]:
                    pair = (note_list[j], note_list[i])
                else:
                    pair = (note_list[i], note_list[j])
                if pair not in note_cooccur_counter:
                    note_cooccur_counter[pair] = 0
                note_cooccur_counter[pair] += 1

    note = note_counter()

    df = pd.DataFrame(index=note, columns=note)

    print(note_cooccur_counter.keys())

    for k in note_cooccur_counter.keys():
        df.loc[k[1]][k[0]] = note_cooccur_counter[k]

    df.to_csv('note_pair_uci.csv', encoding='utf8')



def note_matrix_gephi():
    f_input = open('raw_data_60.csv', 'r', encoding='utf8')
    lines = f_input.readlines()

    note_cooccur_counter = {}

    for line in lines:
        line = line.split(',')[2]
        line = line.strip().lower()
        note_lists = line.split(';')
        note_list = []
        for note in note_lists:
            note_list.append(note.split('_')[0])
        for i in range(len(note_list)):
            for j in range(i+1, len(note_list)):
                if note_list[i] > note_list[j]:
                    pair = (note_list[j], note_list[i])
                else:
                    pair = (note_list[i], note_list[j])
                if pair not in note_cooccur_counter:
                    note_cooccur_counter[pair] = 0
                note_cooccur_counter[pair] += 1
    count_list = []
    for k in note_cooccur_counter.keys():
        count_list.append([k[0], k[1], note_cooccur_counter[k]])

    df = pd.DataFrame(count_list, columns=['Source', 'Target', 'freq'])
    df.to_csv('note_pair_60_gephi.csv', encoding='utf8', index=False)


def group_network():
    data_1 = 'note_list_60_attr_name.csv'
    data_2 = 'note_pair_60_gephi.csv'

    df_1 = pd.read_csv(data_1)
    df_2 = pd.read_csv(data_2)
    note_group_dic ={}

    for index, row in df_1.iterrows():
        print(row)
        if row['ID'] in note_group_dic:
            pass
        else:
            if row['GROUP'][-1] == ' ':
                note_group_dic[row['ID']] = row['GROUP'][:-1]
            else:
                note_group_dic[row['ID']] = row['GROUP']

    output_list=[]
    for index, row_2 in df_2.iterrows():
        output_list.append([note_group_dic[row_2['Source']], note_group_dic[row_2['Target']], row_2['freq']])

    final_dic = {}
    for row_3 in output_list:
        if row_3[0] > row[1]:
            pair = (row_3[1], row_3[0])
        else:
            pair = (row_3[0], row_3[1])

        if pair not in final_dic:
            final_dic[pair] = row_3[2]
        final_dic[pair] += row_3[2]

    final_list = []
    for k in final_dic:
        final_list.append([k[0], k[1], final_dic[k]])


    df = pd.DataFrame(final_list, columns=['Source', 'Target', 'Weight'])
    df.to_csv('group_pair_60_gephi.csv',  encoding='utf8', index=False)





if __name__ == '__main__':
    group_network()