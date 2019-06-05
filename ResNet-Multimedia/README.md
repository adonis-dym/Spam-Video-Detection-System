ResNet implementation of cover image spam detection.  
## Files  
* **getdataset.py**: Use requests.get() method to get dataset pictures from source CSV file.
* **write_to_tfrecord.py**: Zip samples into *tfrecord* format file to simplify and accelerate file reading process. Samples consist &#8195;&#8195;of aid(avid), binary stream expression of cover picture and their corresponding labels.
* **train.py**: Read *tfrecord* file, train ResNet model, and save checkpoint.   
* **test.py**: Use trained and saved model to test performance.  
&#8195;&#8195;Parameters: Number of batchs (here not global epoch) trained in model.  
&#8195;&#8195;Usage: ``` python3 test.py -1000 ```  Means test the model after 1000 batchs of training.
* **testset_pic.rar**: 1000 pictures we used in test case.
* **draw_validation/test_result.py**: Visualization validation/test result.
