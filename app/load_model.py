from tensorflow import keras
import tensorflow as tf
from tensorflow.keras import layers
# from vit_keras import vit, utils
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, BatchNormalization, Flatten, Dropout, Activation, Input
import bentoml


def create_model():
    # set input layer
    inputs = layers.Input(shape=input_shape)
    x = tf.keras.layers.Lambda(lambda image: tf.image.resize(image, (image_size, image_size)))(inputs)
    
    # base_model = vit.vit_b16(
    #     image_size=image_size, 
    #     activation="sigmoid", 
    #     pretrained=True,
    #     include_top=False, 
    #     pretrained_top=False
    # )

    # base_model.trainable = False
    # x = base_model(x)
    x = Flatten()(x)
    x = BatchNormalization()(x)
    x = Dense(32, activation=tf.nn.gelu)(x)
    x = BatchNormalization()(x)
    outputs = Dense(num_classes, activation="softmax")(x)
    
    # create model
    model = keras.Model(inputs=inputs, outputs=outputs)
    
    return model

input_shape = (32, 32, 3) 
image_size = 256
num_classes = 100

#모델 로드
print("Loading Model")
model = create_model()
model.load_weights("check_point/check_point")
model.compile(loss='categorical_crossentropy',
  optimizer='adam',
  metrics=['accuracy']
)

# image_size = 256
# model = tf.keras.models.load_model("my_model.h5")

bentoml.tensorflow.save_model(
    "my_model_service",
    model,
    signatures={
        "__call__": {
            "batchable": True,
            "batch_dim": 0,
        },
    }
)