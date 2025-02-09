from flask import Flask, request, send_file
from model_class import *
from PIL import Image
import io

app = Flask(__name__)
encoder, decoder = set_encoder_decoder()
encoder.load_weights('model_weights/encoder.weights.h5')
decoder.load_weights('model_weights/decoder.weights.h5')

@app.route('/')
def main_frame():
    return '''<center><h1>Variational Auto Encoder</h1>
            <form action="/gen"><button style="height:50px">Generate</button></form>
            <form action="/upload"><button style="height:50px">Reconstruct Image</button></form></center>'''

@app.route('/gen')
def gen():
    preds = decoder.predict(np.random.normal(0,1,1024).reshape((1,1024))).squeeze() * 255
    img = Image.fromarray(preds.astype('uint8'), 'RGB').resize((450,450))
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

@app.route('/upload')
def upload_file():
    return '''<h3>Upload image</h3>
            <form action="/rec" method="POST" enctype="multipart/form-data">
                <input type="file" name="file">
                <input type="Submit" value="Upload">
            </form>'''

@app.route('/rec', methods=['POST'])
def reconstruct_file():
    if request.method=='POST':
        f = request.files['file']
        img = Image.open(f).resize((128,128))
        img = np.asarray(img).reshape((1,128,128,3)) / 255.
        preds = decoder.predict(encoder.predict(img)[2]).squeeze() * 255
        img = Image.fromarray(preds.astype('uint8'), 'RGB').resize((450,450))
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)

    return send_file(img_io, mimetype='image/png')


if __name__=='__main__':
    app.run(debug=True)