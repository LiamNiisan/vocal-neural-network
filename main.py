import input_data as ind
import neural_network as nn
import numpy as np


def apprentissage(nbEpoch, errorPlot, update_status_bar):
    update_status_bar("Obtention des parametres de configuration, les inputs et outputs...")
    settings = ind.get_config()
    input_data_nb = int(settings['Input'])
    output_file_nb = int(settings['Output'])


    train_voice_data = ind.get_input_data(input_data_nb)
    train_voice_data_stat = ind.get_static(train_voice_data)
    train_voice_energy_stat = ind.get_stat_energy(train_voice_data)

    output_data = ind.get_output_data(output_file_nb)

    vc_voice_data = ind.get_input_data(input_data_nb, 'vc')
    vc_voice_data_stat = ind.get_static(vc_voice_data)
    vc_voice_energy_stat = ind.get_stat_energy(vc_voice_data)

    test_voice_data = ind.get_input_data(input_data_nb, 'test')
    test_voice_data_stat = ind.get_static(test_voice_data)
    test_voice_energy_stat = ind.get_stat_energy(test_voice_data)

    update_status_bar("Creation du reseau de neuronne...")
    neural_net = nn.NeuralNetwork(settings, train_voice_data_stat, vc_voice_data_stat, test_voice_data_stat, output_data[::-1])

    neural_net.nn_learning_process(nbEpoch, update_status_bar)

    error_train = np.zeros(nbEpoch)
    error_vc = np.asarray(neural_net.vc_error_array)
    error_test = np.asarray(neural_net.test_error_array)

    update_status_bar("affichage des resultats...")
    errorPlot.fillData(error_train, error_vc, error_test, nbEpoch)

    update_status_bar("Done")