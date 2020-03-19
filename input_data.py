import os, sys
import json
import neural_voice_class as nvc

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

data_filename = __location__ + '/data_60/data_'
nn_config_filename = __location__ + '/nn_config.txt'
output_filename = __location__ + '/output'

def get_config():

    settings = {}
    with open(nn_config_filename, 'r') as file:
        for line in file:
            name, setting = line.strip().split(" ")
            settings[name] = setting
    
    return settings


def get_input_data(nb=60, name='train'):

    filename = data_filename + name + '.txt'
    all_voice_data = []
    with open(filename, 'r') as file:
        for line in file:
            dest, voice_string = line.strip().split(":")
            voice_array = voice_string.split(" ")
            voice_data = nvc.InputData(dest, voice_array)
            all_voice_data.append(voice_data)

    return all_voice_data[0:nb]


def get_output_data(file_nb=1):

    filename = output_filename + str(file_nb) + '.txt'
    output = []
    with open(filename, 'r') as file:
        for line in file:
            nb, value = line.strip().split(" ")
            output.append(value)

    output_list = []
    for item in output:

        string_output = list(item)
        int_output = [ int(x) for x in string_output ]

        output_list.append(int_output)
    
    return output_list



def get_static(all_voice_data):
    
    all_voice_data_stat = []
    for data in all_voice_data:
        stat_voice_data = nvc.InputData(data.des_out, get_stat_data(data.voice_data))
        all_voice_data_stat.append(stat_voice_data)

    return all_voice_data_stat



def get_stat_data(data, nb=26):

    data_stat = []
    for i in range(1, len(data), nb):
        start = i
        end = i + int(nb/2) - 1
        data_stat = data_stat + (data[start:end])

    return data_stat


def get_stat_energy(list_data, nb=26):

    energy_stat = []
    for item in list_data:
        data = item.voice_data
        item_energy_stat = []
        for i in range(1, len(data), nb):
            pos = i + int(nb/2)
            item_energy_stat.append(data[pos])
        energy_stat.append(item_energy_stat)

    return energy_stat