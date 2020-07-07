from __future__ import print_function
import base64
import requests
from PIL import Image
import numpy as np
import json
import glob
import os
import random as rand
import time
import cv2

SERVER_URL = 'http://172.17.0.2:8501/v1/models/mynet:predict'

TEST_AMOUNT = 1000
BASE_DIR = '/home/yangck/retrain/flower_photos'

def main():
    walk = list(os.walk(BASE_DIR))
    class_list = sorted(walk[0][1])
    correct_pred = 0
    total_time = 0
    lowest_time = 10000
    highest_time = 0
    for i in range(TEST_AMOUNT):
        randnum = rand.randint(0,100000)
        folder = BASE_DIR + '/' + class_list[randnum % len(class_list)]
        filelist = glob.glob(folder + '/*.jpg')
        image = filelist[randnum % len(filelist)]
        with open(image,"rb") as image_file:
            start = time.time()
            i = image_file.read()
            i = np.frombuffer(i, dtype=np.byte)
            i = cv2.imdecode(i, cv2.IMREAD_COLOR)
            # cv2.imshow('win',i)
            # cv2.waitKey(0)
            i = cv2.resize(i, (299, 299))
            i = np.expand_dims(i, 0)
            i = i / 255
            i = i.astype(np.float32)
            predict_request = {"inputs": {"image": i.tolist()}}
            tosend = json.dumps(predict_request)
            response = requests.post(SERVER_URL, data=tosend)
            response.raise_for_status()
            end = time.time()
            # print('elapsed time :',end-start)
            elapsed_time = end-start
            total_time += elapsed_time
            if elapsed_time < lowest_time:
                lowest_time = elapsed_time
            if elapsed_time > highest_time:
                highest_time = elapsed_time
            res = np.asarray(response.json()['outputs'])
            if np.argmax(res,axis=1).item() == randnum % len(class_list):
                # print('correct!')
                correct_pred += 1
            # else:
                # print('incorrect!','pred =',class_list[np.argmax(res,axis=1).item()],'answer =',class_list[randnum % len(class_list)])
    print('percentage of correct prediction :',correct_pred/TEST_AMOUNT)
    print('avg inference time :',total_time/TEST_AMOUNT)
    print('lowest :',lowest_time)
    print('highest :',highest_time)



if __name__ == '__main__':
  main()
