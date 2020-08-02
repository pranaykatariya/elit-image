from flask import Flask
from flask_restful import reqparse,Api,Resource
from flask_cors import CORS, cross_origin
from keras.models import load_model
from PIL import Image
import numpy as np
from skimage import transform
import requests
from io import BytesIO
import warnings
warnings.filterwarnings("ignore")

parser = reqparse.RequestParser()
parser.add_argument('query')


def load(response):
    np_image = Image.open(BytesIO(response.content))
    np_image = np.array(np_image).astype('float32') / 255
    np_image = transform.resize(np_image, (224, 224, 3))
    np_image = np.expand_dims(np_image, axis=0)
    return np_image


class Spam(Resource):
    def get(self):
        args = parser.parse_args()
        print(type(args))
        print(args)
        url = ""
        url = str([args['query']])
        st=url.replace("'","")
        st = st.replace('"', "")
        st = st.replace("[", "")
        st = st.replace("]", "")

        print("inside")
        print(st)
        response = requests.get(st)
        image = load(response)
        model = load_model("Final_weights.h5")
        ans = model.predict(image)
        maping = {0: "Neutral", 1: "Porn", 2: "NFSW"}
        new_ans = np.argmax(ans[0])
        print(maping[new_ans])
        print(ans[0][new_ans])


app = Flask(__name__)
CORS(app)
api = Api(app)
api.add_resource(Spam, '/')

if __name__ == "__main__":
    app.run()