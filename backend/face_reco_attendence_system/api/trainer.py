import cv2
import numpy as np
import os


class Trainer():
    def __init__(self):
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.output_yml = "trainer.yml"
        self.trainer_pwd = os.path.dirname(os.path.realpath(__file__))
        self.output_config_path = os.path.join(
            self.trainer_pwd, self.output_yml)

    def train(self, faces, ids):

        self.recognizer.train(faces, np.array([ids]))
        self.recognizer.write(self.output_config_path)
