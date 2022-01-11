import cv2
import numpy as np
import os
import logging

class Trainer():
    def __init__(self):
        self.output_yml = "trainer.yml"
        self.trainer_pwd = os.path.dirname(os.path.realpath(__file__))
        self.output_config_path = os.path.join(self.trainer_pwd, self.output_yml)


    def train(self, faces, ids):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.train(faces, np.array([ids]))
        recognizer.write(self.output_config_path)
        logging.info(f"{len(np.unique(ids))} faces trained")