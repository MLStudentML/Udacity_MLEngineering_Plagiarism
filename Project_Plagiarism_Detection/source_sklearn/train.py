from __future__ import print_function

import argparse
import os
import pandas as pd

# sklearn.externals.joblib is deprecated in 0.21 and will be removed in 0.23. 
# from sklearn.externals import joblib
# Import joblib package directly
import sklearn
#import joblib
from sklearn.externals import joblib
import numpy as np
import sagemaker
from sagemaker import LinearLearner

## TODO: Import any additional libraries you need to define a model


# Provided model load function
def model_fn(model_dir):
    """Load model from the model_dir. This is the same model that is saved
    in the main if statement.
    """
    print("Loading model.")
    
    # load using joblib
    #model = joblib.load(os.path.join(model_dir, "model.joblib"))
    model = np.load(os.path.join(model_dir, "model.npy"))
    print("Done loading model.")
    
    return model


## TODO: Complete the main code
if __name__ == '__main__':
    
    # All of the model parameters and training parameters are sent as arguments
    # when this script is executed, during a training job
    
    # Here we set up an argument parser to easily access the parameters
    parser = argparse.ArgumentParser()

    # SageMaker parameters, like the directories for training data and saving models; set automatically
    # Do not need to change
    parser.add_argument('--output-data-dir', type=str, default=os.environ['SM_OUTPUT_DATA_DIR'])
    parser.add_argument('--model-dir', type=str, default=os.environ['SM_MODEL_DIR'])
    parser.add_argument('--data-dir', type=str, default=os.environ['SM_CHANNEL_TRAIN'])
    
    ## TODO: Add any additional arguments that you will need to pass into your model
    
    # args holds all passed-in arguments
    args = parser.parse_args()

    # Read in csv training file
    training_dir = args.data_dir
    train_data = pd.read_csv(os.path.join(training_dir, "train.csv"), header=None, names=None)

    # Labels are in the first column
    train_y = train_data.iloc[:,0].values.reshape(-1,1)
    train_x = train_data.iloc[:,1:].values
    
    
    ## --- Your code here --- ##
    

    ## TODO: Define a model 
    model = LinearLearner(role=role,    
                          train_instance_count=1,
                          train_instance_type="ml.c4.xlarge",
                          predictor_type="binary_classifier",
                          output_path=output_path,
                          sagemaker_session=sagemaker_session,
                          epochs=15)
    
    
    ## TODO: Train the model
    model.fit(train_x, train_y)
    
    
    ## --- End of your code  --- ##
    

    # Save the trained model
    #joblib.dump(model, os.path.join(args.model_dir, "model.joblib"))
    np.save(model, os.path.join(args.model_dir, "model.npy"))
