# make a prediction for a new image.
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import cv2 as cv
import numpy as np


class Predictor:

  def __init__(self, image, model):
    self.model = load_model(model)
    self.prediction = self.predict_number(image)
    return self.prediction
    
  # load and prepare the image
  def load_image(self, filename):
    # load the image
    img = load_img(filename, grayscale=True, target_size=(28, 28))
    # convert to array
    img = img_to_array(img)
    # reshape into a single sample with 1 channel
    img = img.reshape(1, 28, 28, 1)
    # prepare pixel data
    img = img.astype('float32')
    img = img / 255.0
    return img

  # load an image and predict the class
  def predict_number(self,image):
    # load the image
    img = self.load_image(image)
    # load model
    
    # predict the class
    predict_x=self.model.predict(img) 
    classes_x=np.argmax(predict_x,axis=1)
    print(classes_x[0])



"""
Test scripts
"""
if __name__ == "__main__":
  image = '../images/1-97.png'
  model = 'model.h5'
  predictor = Predictor(image, model)

