import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, Conv2D, Conv2DTranspose, BatchNormalization, Flatten, Dropout
from tensorflow.keras.layers import Rescaling, Reshape, Lambda, LeakyReLU, ReLU
from tensorflow.keras.models import Model
import tensorflow.keras.backend as K

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def sampling(args):
    mean, log_var = args
    epsilon = K.random_normal(shape=K.shape(mean), mean=0, stddev=1)
    return mean + K.exp(log_var * 0.5) * epsilon

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def set_encoder_decoder(input_shape = (128,128,3), 
                        latent_dim = 1024, 
                        is_leakyrelu = True, 
                        is_batchnorm = False, 
                        is_dropout = False,
                        lrelu_slope = 0.1):
    #ENCODER
    encoder_input = Input(input_shape, name='encoder_input')
    x = encoder_input

    size = input_shape[0]
    count = 0
    while size != 8:
        x = Conv2D(64, 3, strides=2, padding='same', name=f'encoder_conv_{count}')(x)
        if is_batchnorm:
            x = BatchNormalization(name=f'encoder_bn_{count}')(x)
        if is_leakyrelu:
            x = LeakyReLU(lrelu_slope, name=f'encoder_LReLU_{count}')(x)
        else:
            x = ReLU(name=f'encoder_ReLU_{count}')(x)
        if is_dropout:
            x = Dropout(0.3, name=f'encoder_dropout_{count}')(x)
        count += 1
        size = int(size / 2)

    x = Flatten(name=f'encoder_flatten')(x)
    
    mean = Dense(latent_dim, name='mean')(x)
    log_var = Dense(latent_dim, name='log_var')(x)
    z = Lambda(sampling, name='encoder_output')([mean, log_var])

    encoder = Model(encoder_input, [mean, log_var, z], name='encoder')
    
    #DECODER
    decoder_input = Input((latent_dim,), name='decoder_input')
    x= Dense(size * size * 64, name='decoder_hidden')(decoder_input)
    x = Reshape((size, size, 64))(x)

    count = 0
    while size != input_shape[0]:
        x = Conv2DTranspose(64, 3, strides=2, padding='same', name=f'decoder_convTrans_{count}')(x)
        if is_batchnorm:
            x = BatchNormalization(name=f'decoder_bn_{count}')(x)
        if is_leakyrelu:
            x = LeakyReLU(lrelu_slope, name=f'decoder_LReLU_{count}')(x)
        else:
            x = ReLU(name=f'decoder_ReLU_{count}')(x)
        if is_dropout:
            x = Dropout(0.3, name=f'decoder_dropout_{count}')(x)
        count += 1
        size *= 2

    x = Conv2DTranspose(64, 3, padding='same', name=f'decoder_convTrans_{count}')(x)
    decoder_output = Conv2DTranspose(3, 3, activation='sigmoid', padding = 'same', name='decoder_output')(x)

    decoder = Model(decoder_input, decoder_output, name='decoder')
    
    mean,log_var,z = encoder(encoder.inputs)
    rec = decoder(z)
    
    return encoder, decoder

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class VAE(tf.keras.Model):
    def __init__(self, encoder, decoder):
        super(VAE, self).__init__()

        self.encoder_input = encoder.inputs
        self.encoder = encoder
        self.decoder = decoder
        self.latent_dim = self.encoder.output[0].shape[1]

    def call(self, inputs):
        mean, log_var, z = self.encoder(inputs)
        reconstruction = self.decoder(z)
        return mean, log_var, reconstruction

    def compile(self, optimizer, loss_factor):
        self.optimizer = optimizer
        self.loss_factor = loss_factor
        
    def predict(self, x):
        x = tf.convert_to_tensor(x)
        mean, log_var, z = self.encoder.predict(x, verbose=0)
        return self.decoder.predict(z, verbose=0)                
        
    def fit(self, x, epochs, init_epoch=1, callbacks=[]): 
        def reconstruction_loss(batch, reconstructed):
            rec_loss = tf.reduce_mean(tf.square(batch - reconstructed))
            return rec_loss
        def KL_div(mean, log_var):
            kl_loss =  -0.5 * tf.reduce_mean(1 + log_var - tf.square(mean) - tf.exp(log_var))
            return kl_loss
        def compute_loss(self, batch):
            mean, log_var, reconstructed = self(batch)
            rec_loss = reconstruction_loss(batch, reconstructed)
            kl_loss = KL_div(mean, log_var)
            loss = self.loss_factor * rec_loss + kl_loss
            return loss, rec_loss, kl_loss
            
        callback_list = tf.keras.callbacks.CallbackList(
            callbacks, model=self)
        hist = {'VAE_loss': [], 'rec_loss': [], 'KL_loss': []}
        logs = {}

        callback_list.on_train_begin(logs=logs)
        for epoch in range(init_epoch , epochs+1):
            callback_list.on_epoch_begin(epoch, logs=logs)
            
            progress_bar = tqdm(enumerate(x), total=len(x))
            for step, training_batch in progress_bar:
                with tf.GradientTape() as tape:
                    loss, rec_loss, kl_loss = compute_loss(self, training_batch)\
                    
                hist['VAE_loss'].append(loss.numpy())
                hist['rec_loss'].append(rec_loss.numpy())
                hist['KL_loss'].append(kl_loss.numpy())
                logs['VAE_loss'] = loss.numpy()
                logs['rec_loss'] = rec_loss.numpy()
                logs['KL_loss'] = kl_loss.numpy()

                gradients = tape.gradient(loss, self.trainable_variables)
                self.optimizer.apply_gradients(zip(gradients, self.trainable_variables))
                progress_bar.set_description(
                    'Epoch: {} - Loss: {:.3f} - rec_loss: {:.5f} - KL_loss: {:.3f}'\
                    .format(epoch, loss.numpy(), rec_loss.numpy(), kl_loss.numpy()))

                
                
                callback_list.on_train_batch_end(step, logs=logs)
            callback_list.on_epoch_end(epoch, logs=logs) 

        return hist