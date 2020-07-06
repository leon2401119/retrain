from __future__ import print_function
import base64
import requests
from PIL import Image
import numpy as np
import json


SERVER_URL = 'http://172.17.0.2:8501/v1/models/mynet:predict'

# IMAGE_URL = '/home/yangck/retrain/flower_photos/daisy/107592979_aaa9cdfe78_m.jpg'
# IMAGE_URL = '/home/yangck/retrain/flower_photos/tulips/14957470_6a8c272a87_m.jpg'
IMAGE_URL = '/home/yangck/Desktop/flower.jpg'


def main():
    with open(IMAGE_URL, "rb") as image_file:
        i = image_file.read()
        i = np.frombuffer(i,dtype=np.byte)
        # i = cv2.imdecode(i,cv2.IMREAD_COLOR)
        # cv2.imshow('win',i)
        # cv2.waitKey(0)
        # i = cv2.resize(i,(299,299))
        # i = np.expand_dims(i,0)
        # i = i/255
        # i = i.astype(np.float32)
        jpeg_bytes = base64.b64encode(i)
        jpeg_bytes = jpeg_bytes.decode('utf-8')
        # predict_request = {"instances":{
        #                         "image" : [{"b64": jpeg_bytes}]
        #                     }
        # }
        # predict_request = {
        #     "signature_name": "",
        #     "instances": [
        #         {
        #             "image" : [{"b64": [jpeg_bytes]}]
        #         },
        #     ]
        # }
        predict_request = {"inputs" : {"image" : {"b64": jpeg_bytes}}}
        tosend = json.dumps(predict_request)
        response = requests.post(SERVER_URL, data = tosend)
        response.raise_for_status()
        print(response.json()['outputs'])

def main1():
    input_image = open(IMAGE_URL, "rb").read()
    image_np = cv2.imdecode(np.fromstring(input_image, dtype=np.uint8), cv2.IMREAD_COLOR)
    image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
    # cv2.imshow('im',image_np)
    # cv2.waitKey(0)
    info = np.iinfo(image_np.dtype)
    d = image_np.astype(np.float32) / info.max
    origin_data = cv2.resize(d, (224, 224), interpolation=cv2.INTER_LINEAR).reshape((-1, 224, 224, 3))
    json_request = json.dumps({"instances": origin_data.tolist()})
    json_response = requests.post(SERVER_URL, data=json_request)
    print(json_response.json())


if __name__ == '__main__':
  main()