# retrain
retrain image classifier with tensorflow hub trained module


### Usage : 

1. train classifier with command like : <p>`python retrain.py --image_dir ~/retrain/flower_photos --saved_model_dir ~/retrain_jpeg/saved`


1. after training the classifier, cd to **"saved_model_dir"** provided in args above

1. tensorflow serving deployment can be done with command such as : <p>`sudo docker run -d -p 8500:8500 --name mynet --mount type=bind,source=/home/yangck/retrain_jpeg/saved,target=/models/mynet/1 -e MODEL_NAME=mynet -ti tensorflow/serving`

1. use **client.py** to send inference request to server

<br>
<br>
<br>

### Edit :

Did some testing with models trained by "vanilla" retrain.py and my implemenation of retrain.py (trained with same set of data).<p>
I used two slightly different "client_autotest.py" to test performance of both of them. Results are calculated by randoming sampling 1000 test images (`TEST_AMOUNT = 1000`), sending them to their respective model for inference, and averaging the numbers. All files used can be found in this repository, and the results are listed below:

  For "vanilla" retrained model : (input is **decoded JPEG**, so we need to decode JPEG first in order to send it to server for inference)
  
    percentage of correct prediction : 0.885
    average image preprocess time : 0.18765224123001098
    average inference time : 0.081202321767807
    avg total time : 0.268854562997818
    lowest total time : 0.18206572532653809
    highest total time : 0.29784584045410156
    average request packet size (MB) : 5.2418908548355105
    
  For my implementation of retrained model : (input is **undecoded JPEG** string, decoding is done **within** the served model)
  
    percentage of correct prediction : 0.892
    average image preprocess time : 0.0006006615161895752
    average inference time : 0.06417909717559814
    avg total time : 0.06477975869178772
    lowest total time : 0.054444313049316406
    highest total time : 0.08815765380859375
    average request packet size (MB) : 0.08179362106323242
    
    
  Note : Propagation time for request/response packets are included in "average inference time" since after call to `requests.post(SERVER_URL, data = tosend)` everything is handled by tensorflow serving API, thus impossible to be timed seperately.


**_In theory, two models should have same performance in terms of correctly predicting the class, further experimenting should easily prove this_**
  
To avoid confusion, I've added postfix to two different "client_autotest.py", they are now "**client_autotest_vanilla.py**" and "**client_autotest_my.py**".
As their names suggest, the first is automated test for model trained by vanilla retrain.py, second is for otherwise.


### Edit2 :
When we want to make an inference request to the tensorflow serving api, we can either use
1. RESTful API
1. gRPC API <br>

A well documented experiment shows that **sending string with gRPC** can acheive the best performance amongst sending string with REST or sending nparray with gRPC/REST.
<br>proof : <https://miro.medium.com/max/696/1*pb3j1x-JitaAwDgm2HmP_w.png><br>
As a consequence, I made a client with gRPC formatted request "clinet_grpc.py" and here are the results:

    percentage of correct prediction : 0.895
    average image preprocess time : 0.00015198373794555664
    average inference time : 0.0628689262866974
    avg total time : 0.06302091002464294
    lowest total time : 0.051235198974609375
    highest total time : 0.1358652114868164

As it turned out, no significant increase in both avg. inference time and avg. total time can be spotted.
