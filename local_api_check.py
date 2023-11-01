from keras.datasets import cifar100
from tensorflow.python.keras.utils import np_utils
from itertools import chain
import bentoml
import numpy as np

import json
from json import JSONEncoder

def get_cifar100():
    # 데이터 다운로드
    (x_train, y_train), (x_test, y_test) = cifar100.load_data()
    return x_train, y_train, x_test, y_test

x_train, y_train,x_test,y_test = get_cifar100()

input_shape = (32,32,3)
num_classes = len(set(list(chain(*y_train))))

# one-hot encoding 및 스케일링
x_train = (x_train/255.).astype("float32")
x_test = (x_test/255.).astype("float32")

y_train = np_utils.to_categorical(y_train, num_classes)
y_test = np_utils.to_categorical(y_test, num_classes)

import requests

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

test = {"array":np.expand_dims(x_test[0],axis=0)}

data = json.dumps(test,cls=NumpyArrayEncoder)
response = requests.post(
   "http://0.0.0.0:8000/classify",
   headers={
      "Content-Type": "content-type: application/json",
   },
   data=data
)

print(response.text)