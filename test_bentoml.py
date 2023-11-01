import pytest
import requests
from keras.datasets import cifar100
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

# one-hot encoding 및 스케일링
x_train = (x_train/255.).astype("float32")
x_test = (x_test/255.).astype("float32")

BASE_URL = "http://localhost:8000"

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


def test_predict_endpoint():
    test_array = {"array":np.expand_dims(x_test[0],axis=0)}
    sample_input = json.dumps(test_array,cls=NumpyArrayEncoder)

    response = response = requests.post(
        "http://0.0.0.0:8000/classify",
        headers={
            "Content-Type": "content-type: application/json",
        },
        data=sample_input
    )

    assert response.status_code == 200, f"Expected status code 200 but received {response.status_code}. Response: {response.text}"
    result = response.json()
    assert "result" in result, f"'result' key not found in response. Response: {response.text}"
