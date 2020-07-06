# retrain
retrain image classifier with tensorflow hub trained module


Usage : 

trian classifier with command like : "python retrain.py --image_dir ~/retrain/flower_photos --saved_model_dir ~/retrain_jpeg/saved"

after training the classifier, cd to saved_model_dir

tensorflow serving deployment can be done with command such as : "sudo docker run -d -p 8500:8500 --name mynet --mount type=bind,source=/home/yangck/retrain_jpeg/saved,target=/models/mynet/1 -e MODEL_NAME=mynet -ti tensorflow/serving --env export TF_CPP_MIN_VLOG_LEVEL=3 -v=1"

use client.py to send inference request to server

