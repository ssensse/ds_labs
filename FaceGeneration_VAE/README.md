Variational AutoEncoder consists of **encoder** and **decoder** parts. \
To use the API you must have the relevant libraries: 
  * <code>tensorflow - 2.17.0</code>
  * <code>numpy - 1.26.4 </code>
  * <code>flask - 3.1.0 </code>

And other libraries: <code>pillow</code> <code>io</code> \
Launch **api.py** with cmd or conda. Then open your browser on **127.0.0.1:5000**

#########################################

FILES:
* ***api.py*** - the web application that uses VAE
* ***model_class.py*** - the VAE architecture code and the corresponding functions for its building.
* ***encoder.weights.h5*** - the encoder weights. Encoder encodes an entire image to a small latent space.
* ***decoder.weights.h5*** - the decoder weights. Decoder reconstructs an image using the latent space (sequence of 1024 numbers).
* *face_generation.ipynb* - my researching of celeba dataset and VAE parameters, building an architecture. API can work without this file.
* *train_celeba* - callbacks that were uploaded during VAE training
* *graphs* - graphs of VAE parameter analysis

<image width=200 src='https://github.com/ssensse/ds_labs/blob/main/FaceGeneration_VAE/graphs/screamer.jpg'>
