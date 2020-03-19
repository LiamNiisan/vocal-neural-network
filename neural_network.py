import random
import math
import numpy as np

class NeuralNetwork:

    def __init__(self, settings, train_data, vc_data, test_data, output):

        self.settings = settings
        self.train_data = train_data
        self.vc_data = vc_data
        self.test_data = test_data
        self.all_desired_output = output
        self.desired_output = []
        self.nb_input = len(train_data[0].voice_data)
        self.nb_output = len(output[0])
        self.h_layers = int(settings['Layers'])
        self.func = settings['Funct']
        self.corr_fact = float(settings['Corr_fact'])
        self.weights = []
        self.current_value = []
        self.current_output = []
        self.i_value = []
        self.a_value = []
        self.epoch = 0


    def set_weights(self, nb_source_layer, nb_destination_layer, layer):
    
        random.seed(66+layer)

        weights_array = []
        for ns in range(nb_destination_layer):

            single_n_array = []
            for nd in range(nb_source_layer):

                weight = random.uniform(-0.1,0.1)
                single_n_array.append(weight)

            weights_array.append(single_n_array)


        return weights_array

    
    def average(self, data):

        return sum(data) / len(data)


    def set_weights_all_layers(self):

        nb_source_layer_last = self.nb_input
        weights_array = []

        for i in range(self.h_layers):

           nb_destination_layer = int(self.settings['N_layer_'+str(i+1)])
           weights = self.set_weights(nb_source_layer_last, nb_destination_layer, i)
           weights_array.append(weights)

           nb_source_layer_last = nb_destination_layer

        weights = self.set_weights(nb_source_layer_last, self.nb_output, self.h_layers + 1)
        weights_array.append(weights)

        self.weights = weights_array

    def weight_sum(self, weight_array):

        sum_weight_array = []
        for weight in weight_array:

            sum_weight = sum(weight)
            sum_weight_array.append(sum_weight)

        return sum_weight_array


    def calculate_i(self, source_layer, weight_array, b=0):

        i_array = []
        for dest_n in weight_array:

            i = 0
            for in_data, weight in zip(source_layer, dest_n):

                i += float(in_data) * weight + b

            i_array.append(i)

        return i_array


    def calculate_a(self, i_array):

        a_array = []
        if self.func == 'sig' :

            a_array = self.sig_func(i_array)

        elif self.func == 'tanh' :

            a_array = self.tanh_func(i_array)

        return a_array


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

        der_array = []
        for a in a_array:

            der_array.append( a * (1 -a))

        return der_array


    def der_tanh_func(self, i_array):

        return 1 - ((self.tanh_func(i_array)) ** 2)


    def tanh_func(self, i):

        return np.tanh(i)


    def activation_stage(self, b=0):

        i_array_all = []
        a_array_all = []

        i_array = self.calculate_i(self.current_value, self.weights[0], b)
        i_array_all.append(i_array)

        a_array = self.calculate_a(i_array)
        a_array_all.append(a_array)

        for n in range(1, len(self.weights)):

            i_array = self.calculate_i(a_array, self.weights[n], b)
            i_array_all.append(i_array)

            a_array = self.calculate_a(i_array)
            a_array_all.append(i_array)

        exit_data = a_array

        self.current_output, self.i_value, self.a_value = exit_data, i_array_all, a_array_all


    def get_signal_error(self):

        error_1 = 0 

        if (self.func == 'sig'):
            error_1 = (self.desired_output - self.current_output) * self.der_sig_func(self.current_output)
        elif (self.func == 'tanh'):
            error_1 = (self.desired_output - self.current_output) * self.der_tanh_func(self.current_output)


        last_layer_error = error_1

        all_error_array = []
        all_error_array.append(error_1)

        for layer in range(0, self.h_layers):

            der_func = 0

            if (self.func == 'sig'):
                der_func = (self.der_sig_func(self.a_value[1-layer]))
            elif (self.func == 'tanh'):
                der_func = (self.der_tanh_func(self.i_value[1-layer]))

            error_calc_weight = []
            for w in zip(*(self.weights[2-layer])):
                n_weight = w * last_layer_error
                error_calc_weight.append(sum(n_weight))
            error = der_func * error_calc_weight
            last_layer_error = error
            all_error_array.append(error)

        return all_error_array[::-1]

    
    def calculate_corr(self, n_input, error):

        corr = []

        for n in n_input:

            c = []
            for err in error:
                
                c.append(float(n) * err * self.corr_fact)

            corr.append(c)

        return corr

    
    def adjust_weights(self, error):

        new_weights = []
        correction = []

        corr = self.calculate_corr(self.current_value, error[0])
        correction.append(corr)

        for i in range(1, len(error)):
            
            corr = self.calculate_corr(self.a_value[i-1], error[i])
            correction.append(corr)

        for i in range(0, len(correction)):

            w = list(zip(*self.weights[i]))
            new_weights.append(np.add(w, correction[i]))

        i_new_weights = []
        for w in new_weights:
            
            i_new_weights.append(list(zip(*w)))

        return i_new_weights

    
    def learning_phase(self):

        for v in self.train_data:

            if v.des_out == 'o':
                
                v.des_out = 0

            current_d_output = int(v.des_out)
            self.current_value = v.voice_data
            self.desired_output = self.all_desired_output[current_d_output]
            
            self.activation_stage()

            error = self.get_signal_error()
            self.weights = self.adjust_weights(error)

    
    def testing_phase(self, data='test'):

        test_data = []
        error_array = []
        
        if data == 'test':
        
            test_data = self.test_data
        
        elif data == 'vc':

            test_data = self.vc_data

        for v in test_data:

            if v.des_out == 'o':
                
                v.des_out = 0

            current_d_output = int(v.des_out)
            self.current_value = v.voice_data
            self.desired_output = self.all_desired_output[current_d_output]
            
            self.activation_stage()

            error = self.get_signal_error()

            error_array.append(self.average(error[-1]) * 100)

        return self.average(error_array)



    def nn_learning_process(self):

        random.seed(66)
        random.shuffle(self.train_data)

        self.set_weights_all_layers()

        vc_error_array = []
        test_error_array = []
        
        for i in range(0,10):
            
            self.learning_phase()

            vc_error = self.testing_phase('vc')
            vc_error_array.append(vc_error)

            test_error = self.testing_phase()
            test_error_array.append(test_error)

            self.epoch += 1

        return 1














