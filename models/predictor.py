# make a prediction for a new image.
from keras.models import load_model
import cv2 as cv


class Predictor:

  def __init__(self, image, model):
    self.model = load_model(model)
    self.prediction = self.predict_number(image)
    
  # load and prepare the image
  def load_image(self, image):
    # load the image
    img = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

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
    if self.model.predict(img)[0][0] > self.model.predict(img)[0][1]:
      return 0
    else: return 1



"""
Test scripts
"""
if __name__ == "__main__":
  image = '../images/bin1.jpg'
  model = 'model.h5'
  predictor = Predictor(image, model)

