from __future__ import print_function
import grpc
import numpy as np
import tensorflow as tf
from tensorflow_serving.apis import predict_pb2, prediction_service_pb2_grpc
import os
import random as rand
import time
import glob


TEST_AMOUNT = 1000
BASE_DIR = '/home/yangck/retrain/flower_photos'

# with open(IMAGE_URL, "rb") as image_file:
#     i = image_file.read()
#     # i = np.frombuffer(i, dtype=np.byte)
#
# stub = prediction_service_pb2_grpc.PredictionServiceStub(grpc.insecure_channel("172.17.0.2:8500"))
#
# request = predict_pb2.PredictRequest()
# request.model_spec.name = "mynet"
# t = tf.make_tensor_proto(i)
# request.inputs['image'].CopyFrom(t)
# result = stub.Predict(request)
# print(list(result.outputs['prediction'].float_val))



def main():
    walk = list(os.walk(BASE_DIR))
    class_list = sorted(walk[0][1])
    correct_pred = 0
    req_size = 0
    image_read_time = 0
    total_time = 0
    lowest_time = 10000
    highest_time = 0
    stub = prediction_service_pb2_grpc.PredictionServiceStub(grpc.insecure_channel("172.17.0.2:8500"))
    request = predict_pb2.PredictRequest()
    request.model_spec.name = "mynet"
    for _ in range(TEST_AMOUNT):
        randnum = rand.randint(0,100000)
        folder = BASE_DIR + '/' + class_list[randnum % len(class_list)]
        filelist = glob.glob(folder + '/*.jpg')
        image = filelist[randnum % len(filelist)]
        with open(image,"rb") as image_file:
            start = time.time()
            i = image_file.read()
            t = tf.make_tensor_proto(i)
            request.inputs['image'].CopyFrom(t)
            end = time.time()
            image_read_time += (end-start)
            result = stub.Predict(request)
            end = time.time()
            # print('elapsed time :',end-start)
            elapsed_time = end-start
            total_time += elapsed_time
            if elapsed_time < lowest_time:
                lowest_time = elapsed_time
            if elapsed_time > highest_time:
                highest_time = elapsed_time
            res = list(result.outputs['prediction'].float_val)
            if np.argmax(res).item() == randnum % len(class_list):
                # print('correct!')
                correct_pred += 1
            # else:
                # print('incorrect!','pred =',class_list[np.argmax(res,axis=1).item()],'answer =',class_list[randnum % len(class_list)])
    print('percentage of correct prediction :',correct_pred/TEST_AMOUNT)
    print('average image preprocess time :',image_read_time/TEST_AMOUNT)
    print('average inference time :',(total_time - image_read_time)/TEST_AMOUNT)
    print('avg total time :',total_time/TEST_AMOUNT)
    print('lowest total time :',lowest_time)
    print('highest total time :',highest_time)
    # print('average request packet size (MB) :', req_size / (TEST_AMOUNT * 1024 * 1024))


if __name__ == '__main__':
  main()