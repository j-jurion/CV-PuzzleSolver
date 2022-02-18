import cv2 as cv

DEV = True

class DevMessage():
  def __init__(self, msg):
    if DEV:
      print(f"DEBUG MESSAGE: {msg}")


class DevImage():
  def __init__(self,title, img):
    if DEV:
      cv.imshow(title, img)
