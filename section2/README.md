### Section 2: Training a segmentation CNN

The directory called `section2/src` contains the source code that forms the framework for your machine learning pipeline.

We use [PyTorch](https://pytorch.org/) to train the model and we use [Tensorboard](https://www.tensorflow.org/tensorboard/) to visualize the results.

With the script `run_ml_pipeline.py` (or `run_ml_pipeline.ipynb`) we kick off the training pipeline. The jupyter notebook `run_ml_pipeline.ipynb` shows a run of the pipeline with performance measurements.

The code has hooks to log progress to Tensorboard. In order to see the Tensorboard output launch Tensorboard executable from the same directory where `run_ml_pipeline.py` is located using the following command:

> `tensorboard --logdir runs --bind_all`

After that, Tensorboard will write logs into directory called `runs` and you will be able to view progress by opening the browser and navigating to default port 6006 of the machine where you are running it.

The following figure shows the tracking of the loss function during training of the ML model:
<img src="../readme.img/loss.png" width=800em>
