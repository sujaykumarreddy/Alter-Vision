import cv2
from gtts import gTTS
import os
import time

# Pretrained classes in the model
class detect_objects(object):

    def __init__(self):
        self.classNames = {0: 'background',
                      1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle', 5: 'airplane', 6: 'bus',
                      7: 'train', 8: 'truck', 9: 'boat', 10: 'traffic light', 11: 'fire hydrant',
                      13: 'stop sign', 14: 'parking meter', 15: 'bench', 16: 'bird', 17: 'cat',
                      18: 'dog', 19: 'horse', 20: 'sheep', 21: 'cow', 22: 'elephant', 23: 'bear',
                      24: 'zebra', 25: 'giraffe', 27: 'backpack', 28: 'umbrella', 31: 'handbag',
                      32: 'tie', 33: 'suitcase', 34: 'frisbee', 35: 'skis', 36: 'snowboard',
                      37: 'sports ball', 38: 'kite', 39: 'baseball bat', 40: 'baseball glove',
                      41: 'skateboard', 42: 'surfboard', 43: 'tennis racket', 44: 'bottle',
                      46: 'wine glass', 47: 'cup', 48: 'fork', 49: 'knife', 50: 'spoon',
                      51: 'bowl', 52: 'banana', 53: 'apple', 54: 'sandwich', 55: 'orange',
                      56: 'broccoli', 57: 'carrot', 58: 'hot dog', 59: 'pizza', 60: 'donut',
                      61: 'cake', 62: 'chair', 63: 'couch', 64: 'potted plant', 65: 'bed',
                      67: 'dining table', 70: 'toilet', 72: 'tv', 73: 'laptop', 74: 'mouse',
                      75: 'remote', 76: 'keyboard', 77: 'cellphone', 78: 'microwave', 79: 'oven',
                      80: 'toaster', 81: 'sink', 82: 'refrigerator', 84: 'book', 85: 'clock',
                      86: 'vase', 87: 'scissors', 88: 'teddy bear', 89: 'hair drier', 90: 'toothbrush'}


    def id_class_name(self, class_id, classes):
        for key, value in classes.items():
            if class_id == key:
                return value

    def write_to_file(self, class_names):
        with open('test.txt', 'r+') as f:
            f.write("The objects in the scene are "+class_names)
            f.close()
        print("The objects in the scene are "+class_names)

    def run_object_detection(self, img):
    # Loading model
        model = cv2.dnn.readNetFromTensorflow('models/frozen_inference_graph.pb',
                                              'models/ssd_mobilenet_v2_coco_2018_03_29.pbtxt')
        image = img

        image_height, image_width, _ = image.shape

        model.setInput(cv2.dnn.blobFromImage(image, size=(300, 300), swapRB=True))
        output = model.forward()
        # print(output[0,0,:,:].shape)

        class_names = ''
        for detection in output[0, 0, :, :]:
            confidence = detection[2]
            if confidence > .5:
                class_id = detection[1]
                class_name=self.id_class_name(class_id,self.classNames)
                class_names += class_name + ','
                box_x = detection[3] * image_width
                box_y = detection[4] * image_height
                box_width = detection[5] * image_width
                box_height = detection[6] * image_height
                cv2.rectangle(image, (int(box_x), int(box_y)), (int(box_width), int(box_height)), (23, 230, 210), thickness=1)
                cv2.putText(image,class_name ,(int(box_x), int(box_y+.05*image_height)),cv2.FONT_HERSHEY_SIMPLEX,(.005*image_width),(0, 0, 255))


        cv2.imshow('image', image)
        time.sleep(5)

        self.write_to_file(class_names)

        with open("test.txt", 'r') as file:
            file = file.read()

        speak = gTTS(file, lang='en')
        speak.save("audio_new.mp3")

        file = "audio_new.mp3"
        os.system("mpg123 " + file)
        open('test.txt', 'w').close()


    # cv2.imwrite("image_box_text.jpg",image)
