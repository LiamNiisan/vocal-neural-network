import input_data as ind
import neural_network as nn
import numpy as np


def apprentissage(errorPlot, update_status_bar):

    update_status_bar(
        "Obtention des parametres de configuration, les inputs et outputs...")

    # Commencer par obtenir les paramêtre du réseau dans les fichiers
    # Fichier de configuration
    settings = ind.get_config()
    input_data_nb = int(settings['Input'])
    output_file_nb = int(settings['Output'])

    # Fichier de données d'apprentissage
    train_voice_data = ind.get_input_data(input_data_nb)
    train_voice_data_stat = ind.get_static(train_voice_data)
    ind.get_stat_energy(train_voice_data)

    # Fichier de sortie désirée
    output_data = ind.get_output_data(output_file_nb)

    # Fichier de données de validation croisée
    vc_voice_data = ind.get_input_data(input_data_nb, 'vc')
    vc_voice_data_stat = ind.get_static(vc_voice_data)
    ind.get_stat_energy(vc_voice_data)

    # Fichier de données de test
    test_voice_data = ind.get_input_data(input_data_nb, 'test')
    test_voice_data_stat = ind.get_static(test_voice_data)
    ind.get_stat_energy(test_voice_data)

    # Création du réseau de neuronne
    update_status_bar("Creation du reseau de neuronne...")
    neural_net = nn.NeuralNetwork(settings, train_voice_data_stat,
                                  vc_voice_data_stat, test_voice_data_stat, output_data[::-1])

    neural_net.nn_learning_process(update_status_bar)

    update_status_bar("affichage des resultats...")

    train_error = np.asarray(neural_net.train_error)
    vc_error = np.asarray(neural_net.vc_error)
    test_error = np.asarray(neural_net.test_error)

    errorPlot.fillData(train_error,
                       vc_error,
                       test_error,
                       neural_net.epoch)

    update_status_bar("Done")
