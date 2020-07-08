# retrain
retrain image classifier with tensorflow hub trained module


### Usage : 

1. trian classifier with command like : 

 `python retrain.py --image_dir ~/retrain/flower_photos --saved_model_dir ~/retrain_jpeg/saved`

1. after training the classifier, cd to "saved_model_dir" provided in args above

1. tensorflow serving deployment can be done with command such as : "sudo docker run -d -p 8500:8500 --name mynet --mount type=bind,source=/home/yangck/retrain_jpeg/saved,target=/models/mynet/1 -e MODEL_NAME=mynet -ti tensorflow/serving"

1. use client.py to send inference request to server



### Edit :

Did some testing with models trained by "vanilla" retrain.py and my implemenation of retrian.py (trained with same set of data)
I used two slightly different "client_autotest.py" to test performance of both of them, and the resluts are listed below:

  For "vanilla" retrained model : (input is decoded JPEG, so we need to decode JPEG first in order to send it to server for inference)
  
    percentage of correct prediction : 0.882
    avg inference time : 0.2736836004257202
    lowest : 0.18077421188354492
    highest : 0.6768004894256592
    
  For my implementation of retrained model : (input is undecoded JPEG string, decoding is done within the served model)
  
    percentage of correct prediction : 0.86
    avg inference time : 0.06731470036506652
    lowest : 0.053359031677246094
    highest : 0.12958669662475586

  **In theory, two models should have same performance in terms of correctly predicting the class, further experimenting should easily prove this**
  
To avoid confusion, I've added postfix to two different client_autotest.py, they are now "client_autotest_vanilla.py" and "client_autotest_my.py".
As their names suggest, the first is automated test for model trained by vanilla retrain.py, second is for otherwise.
