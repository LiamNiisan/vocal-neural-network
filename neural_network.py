import random
import math
import numpy as np
import json
import os


class NeuralNetwork:

    def __init__(self, settings, train_data, vc_data, test_data, output):

        self.settings = settings
        self.train_data = train_data
        self.vc_data = vc_data
        self.test_data = test_data
        self.all_desired_output = output
        self.desired_output = np.array
        self.nb_input = len(train_data[0].voice_data)
        self.nb_output = len(output[0])
        self.h_layers = int(settings['Layers'])
        self.func = settings['Funct']
        self.learn_rate = float(settings['Corr_fact'])
        self.momentum = float(settings['Momentum'])
        self.last_corr = []
        self.weights = np.array
        self.previous_weights = []
        self.current_value = np.array
        self.current_output = np.array
        self.i_value = np.array
        self.a_value = np.array
        self.epoch = 0
        self.test_error = []
        self.vc_error = []
        self.train_error = []
        self.save_folder = 'data/'
        self.adapt = int(settings['Adapt'])

    def set_weights(self, nb_source_layer, nb_destination_layer, layer):

        # Cette fonction permet d'initialiser les poids aléatoirement

        # Faire un seed pour pouvoir obtenir le même nombre aléatoire à chaque fois
        random.seed(66+layer)

        weights_array = []

        for ns in range(nb_destination_layer):

            single_n_array = []
            for nd in range(nb_source_layer):

                # Les poids sont inialisé entre -0.1 et 0.1
                weight = random.uniform(-0.1, 0.1)
                single_n_array.append(weight)

            weights_array.append(np.array(single_n_array))

        return np.array(weights_array)

        return np.array(weights_array)

    def set_tanh_output(self):

        tanh_output = []

        # Changer tous les 0 pour des -1 pour chaque sortie
        for o in self.all_desired_output:

            n_o = [-1 if (x == 0) else 1 for x in o]
            tanh_output.append(n_o)

        self.all_desired_output = tanh_output

    def average(self, data):

        return sum(data) / len(data)

    def set_weights_all_layers(self):

        nb_source_layer_last = self.nb_input
        weights_array = []

        for i in range(self.h_layers):
            if (i == 0):
                nb_destination_layer = int(self.settings['N_layer_1'])
            else:
                nb_destination_layer = int(self.settings['N_layer_2'])

            weights = self.set_weights(
                nb_source_layer_last, nb_destination_layer, i)
            weights_array.append(weights)

            nb_source_layer_last = nb_destination_layer

        weights = self.set_weights(
            nb_source_layer_last, self.nb_output, self.h_layers + 1)
        weights_array.append(weights)

        self.weights = weights_array

    def calculate_i(self, source_layer, weight_array, b=0):

        i_array = []

        for dest_n in weight_array:

            i = 0
            for in_data, weight in zip(source_layer, dest_n):

                i += float(in_data) * weight + b

            i_array.append(i)

        return np.array(i_array)

    def calculate_a(self, i_array):

        a_array = []

        if self.func == 'sig':

            a_array = self.sig_func(i_array)

        elif self.func == 'tanh':

            a_array = self.tanh_func(i_array)

        return np.array(a_array)

    def sig_func(self, i_array):

        a_array = []

        for i in i_array:

            try:
                a = 1/(1 + math.exp(-i))
            except OverflowError:
                a = 0

            a_array.append(a)

        return a_array

    def der_sig_func(self, a_array):

        # Cette fonction permet de calculer la dérivée de sig

        der_array = []

        for a in a_array:

            der_array.append(a * (1 - a))

        return der_array

    def der_tanh_func(self, i_array):

        # Cet fonction permet de calculer la dérivée de tanh

        return 1 - ((self.tanh_func(i_array)) ** 2)

    def tanh_func(self, i):

        return np.tanh(i)

    def activation_stage(self, b=0):

        i_array_all = []
        a_array_all = []

        # Phase 1, calculer i et a à partir de l'entrée du réseau
        i_array = self.calculate_i(self.current_value, self.weights[0], b)
        i_array_all.append(i_array)

        a_array = self.calculate_a(i_array)
        a_array_all.append(a_array)

        # Continuer à calculer pour chaque couche
        for n in range(1, len(self.weights)):

            i_array = self.calculate_i(a_array, self.weights[n], b)
            i_array_all.append(i_array)

            a_array = self.calculate_a(i_array)
            a_array_all.append(i_array)

        exit_data = a_array

        self.current_output, self.i_value, self.a_value = np.array(
            exit_data), np.array(i_array_all), np.array(a_array_all)

    def get_signal_error(self):

        error_1 = 0

        # Calculer l'erreur a partir de la sortie
        if (self.func == 'sig'):
            error_1 = (self.desired_output - self.current_output) * \
                self.der_sig_func(self.current_output)
        elif (self.func == 'tanh'):
            error_1 = (self.desired_output - self.current_output) * \
                self.der_tanh_func(self.i_value[self.h_layers])

        # Se rappeler de la derniere couche d'erreur calculee
        last_layer_error = error_1

        all_error_array = []
        all_error_array.append(error_1)

        # On passe par chaque couche a partir de la sortie, -1 pour ne pas inclue la sortie
        for layer in range(self.h_layers-1, -1, -1):

            der_func = 0

            if (self.func == 'sig'):
                der_func = (self.der_sig_func(self.a_value[layer]))
            elif (self.func == 'tanh'):
                der_func = (self.der_tanh_func(self.i_value[layer]))

            # zip permet de transposer la matrice des poids
            error_calc_weight = []
            for w in zip(*(self.weights[layer+1])):
                n_weight = w * last_layer_error
                error_calc_weight.append(sum(n_weight))

            error = np.array(der_func) * np.array(error_calc_weight)
            last_layer_error = error
            all_error_array.append(error)

        return all_error_array[::-1]

    def calculate_corr(self, n_input, error, last_corr):

        corr = []
        i = 0
        j = 0

        for n in n_input:

            c = []
            for err in error:

                # l'apprentissage en prenant compte du momentum
                if(last_corr == 0):
                    c.append((float(n) * err * self.learn_rate))
                else:
                    c.append((float(n) * err * self.learn_rate) +
                             (self.momentum * last_corr[i][j]))

            corr.append(c)

            j += 1

        i += 1

        return corr

    def adjust_weights(self, error):

        new_weights = []
        t_new_weights = []
        correction = []
        t_correction = []

        # Phase 3, calcul du facteur de correction
        # Premierement le facteur est calculé à partir de l'entrée
        if(self.epoch == 0):
            corr = self.calculate_corr(self.current_value, error[0], 0)
        else:
            corr = self.calculate_corr(
                self.current_value, error[0], self.last_corr[0])

        correction.append(corr)

        # Le reste du facteur est calculé
        for i in range(1, len(error)):

            if(self.epoch == 0):
                corr = self.calculate_corr(self.a_value[i-1], error[i], 0)
            else:
                corr = self.calculate_corr(
                    self.a_value[i-1], error[i], self.last_corr[i])

            correction.append(corr)

        # Phase 4, le facteur est additionné au poids
        for i in range(0, len(correction)):

            w = list(zip(*self.weights[i]))
            new_weights.append(np.add(w, correction[i]))

        # Les matrices des poids sont remises en format standard après avoir été transposée
        for w in new_weights:

            t_new_weights.append(list(zip(*w)))

        for c in correction:

            t_correction.append(list(zip(*c)))

        # On sauvegarde le facteur de correction pour la prochaine epoch
        self.last_corr = t_correction

        return t_new_weights

    def learning_phase(self):

        for v in self.train_data:

            if v.des_out == 'o':

                v.des_out = 0

            current_d_output = int(v.des_out)
            self.current_value = np.array(v.voice_data)
            self.desired_output = np.array(
                self.all_desired_output[current_d_output])

            # Phase 1: Activation et fonction d'activation
            self.activation_stage()

            # Phase 2-3: Calcul du signal d'erreur et facteur de correction
            error = self.get_signal_error()
            self.previous_weights.append(self.weights)

            # Phase 4: Mise a jour
            self.weights = self.adjust_weights(error)

    def testing_phase(self, data='test'):

        test_data = []
        error_array = []

        if data == 'test':

            test_data = self.test_data

        elif data == 'vc':

            test_data = self.vc_data

        elif data == 'train':

            test_data = self.train_data

        for v in test_data:

            if v.des_out == 'o':

                v.des_out = 0

            # Test de chanque données dans le test
            current_d_output = int(v.des_out)
            self.current_value = np.array(v.voice_data)
            self.desired_output = np.array(
                self.all_desired_output[current_d_output])

            # Test des données avec le réseau actuel
            self.activation_stage()

            # Calcul de l'erreur
            delta = self.desired_output - self.current_output
            s_delta = self.average(np.abs(delta))
            error = s_delta * 100

            # Puisque tanh va de -1 a 1, l'equart est 2 fois plus grand que sig, donc division par 2
            if self.func == 'tanh':

                error /= 2

            error_array.append(error)

        return self.average(error_array)

    def np_to_list(self, x_array):

        # Cet fonction sert a transformer les tableaux numpy en list() standard de Python
        # Cela permet de simplifier la serialization vers json

        list_x = []

        if type(x_array) == np.ndarray:

            for x in x_array:

                l_x = x.tolist()

                list_x.append(l_x)

        else:

            list_x = list(x_array)

        return list_x

    def save_nn_status(self):

        #weights_json_str = json.dumps(self.previous_weights)
        current_weights_json_str = json.dumps(self.np_to_list(self.weights))
        a_json_str = json.dumps(self.np_to_list(self.a_value))

        train_error_json_str = json.dumps(self.train_error)
        vc_error_json_str = json.dumps(self.vc_error)
        test_error_json_str = json.dumps(self.test_error)

        current_train_error_json_str = json.dumps(self.train_error[self.epoch])
        current_vc_error_json_str = json.dumps(self.vc_error[self.epoch])
        current_test_error_json_str = json.dumps(self.test_error[self.epoch])

        # with open(self.save_folder + "NN_weights.json", "w") as text_file:
        #    print(weights_json_str, file=text_file)

        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)

        with open(self.save_folder + "NN_weights_current.json", "w+") as text_file:
            print(current_weights_json_str, file=text_file)

        with open(self.save_folder + "NN_a.json", "w+") as text_file:
            print(a_json_str, file=text_file)

        with open(self.save_folder + "Train_error.json", "w+") as text_file:
            print(train_error_json_str, file=text_file)

        with open(self.save_folder + "VC_error.json", "w+") as text_file:
            print(vc_error_json_str, file=text_file)

        with open(self.save_folder + "Test_error.json", "w+") as text_file:
            print(test_error_json_str, file=text_file)

        with open(self.save_folder + "Train_error_current.json", "w+") as text_file:
            print(current_train_error_json_str, file=text_file)

        with open(self.save_folder + "VC_error_current.json", "w+") as text_file:
            print(current_vc_error_json_str, file=text_file)

        with open(self.save_folder + "Test_error_current.json", "w+") as text_file:
            print(current_test_error_json_str, file=text_file)

    def nn_learning_process(self, update_status_bar):

        # Reordonner les donnees aleatroirement
        random.seed(66)
        random.shuffle(self.train_data)

        # La fonction d'activation tanh va de -1 a 1, donc on change les sorties desirées pour -1 au lieu de 0
        if(self.func == 'tanh'):

            self.set_tanh_output()

        # Assinger une valeur aleatoire au poids
        self.set_weights_all_layers()

        # corr_change change a quel pourcentage le taux adaptatif commence
        train_error, test_error, vc_error, corr_change = 50, 50, 50, 4

        while vc_error > 1 and self.epoch <= int(self.settings['Epochs']):

            # Phase 1 a 4
            self.learning_phase()

            # Tester l'apprentissage pour cet epoch
            train_error = self.testing_phase('train')
            self.train_error.append(train_error)

            vc_error = self.testing_phase('vc')
            self.vc_error.append(vc_error)

            update_status_bar(
                "Test en cours (epoch #" + str(self.epoch+1) + ") ...")
            test_error = self.testing_phase()
            self.test_error.append(test_error)

            # Sensibiliser le facteur de correction pour mieur trouver le minimum local
            if(train_error < corr_change and self.adapt == 1):

                self.learn_rate /= 2
                corr_change = - 1

            # Sauvegarder les donnees pour y avoir un acces externe dans le dossier /data
            self.save_nn_status()
            self.epoch += 1
