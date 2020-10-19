"""
This file contains code that will kick off training and testing processes
"""
import os
import json
import numpy as np
from experiments.UNetExperiment import UNetExperiment
from data_prep.HippocampusDatasetLoader import LoadHippocampusData

class Config:
    """
    Holds configuration parameters
    """
    def __init__(self):
        """
        Defines important parameters:
        name: name of algorithm (neural network)
        root_dir: 
        n_epochs: number of epochs to train
        learning_rate: initial learning rate
        batch_size: size of image/label batches to feed the neural network at training at once
        patch_size:
        test_results_dir: 
        """
        self.name = 'Basic_unet'
        # self.root_dir = r'../data/TrainingSet/'
        self.root_dir = r'../../section1/data/TrainingSet/'
        self.n_epochs = 10
        self.learning_rate = 0.0002
        self.batch_size = 16
        self.patch_size = 64
        self.test_results_dir = '../results/'

if __name__ == "__main__":

    # set random seed generator:
    np.random.seed(seed=5)

    # define relative training, validation and testing size:
    train_size = 0.75
    valid_size = 0.15
    test_size = 0.1

    # Get configuration

    # TASK: Fill in parameters of the Config class and specify directory where the data is stored and 
    # directory where results will go
    c = Config()

    # Load data
    print("Loading data...")

    # TASK: LoadHippocampusData is not complete. Go to the implementation and complete it. 
    data = LoadHippocampusData(root_dir=c.root_dir, y_shape=c.patch_size,
                               z_shape=c.patch_size)


    # Create test-train-val split
    # In a real world scenario you would probably do multiple splits for 
    # multi-fold training to improve your model quality

    keys = range(len(data))

    # Here, random permutation of keys array would be useful in case if we do something like 
    # a k-fold training and combining the results. 
    keys = np.array(keys)
    np.random.shuffle(keys)

    split = dict()

    # TASK: create three keys in the dictionary: "train", "val" and "test". In each key, store
    # the array with indices of training volumes to be used for training, validation 
    # and testing respectively.
    # <YOUR CODE GOES HERE>
    split['train'] = keys[:int(train_size*len(keys))]
    split['val'] = keys[int(train_size*len(keys)):int((train_size+valid_size)*len(keys))]
    split['test'] = keys[int((train_size+valid_size)*len(keys)):]

    # Set up and run experiment
    
    # TASK: Class UNetExperiment has missing pieces. Go to the file and fill them in
    exp = UNetExperiment(config=c, split=split, dataset=data)

    # You could free up memory by deleting the dataset
    # as it has been copied into loaders
    # del dataset 

    # run training
    exp.run()

    # prep and run testing

    # TASK: Test method is not complete. Go to the method and complete it
    results_json = exp.run_test()

    results_json["config"] = vars(c)

    with open(os.path.join(exp.out_dir, 'results.json'), 'w') as out_file:
        json.dump(results_json, out_file, indent=2, separators=(',', ': '))

    print('To see results run: tensorboard --port=6006 --logdir runs --bind_all.')
