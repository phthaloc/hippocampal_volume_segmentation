"""
Contains class that runs inferencing
"""
import torch
import numpy as np

from networks.RecursiveUNet import UNet

from utils.utils import med_reshape

class UNetInferenceAgent:
    """
    Stores model and parameters and some methods to handle inferencing
    """
    def __init__(self, parameter_file_path='', model=None, device='cpu', patch_size=64):

        self.model = model
        self.patch_size = patch_size
        self.device = device

        if model is None:
            self.model = UNet(num_classes=3)

        if parameter_file_path:
            self.model.load_state_dict(torch.load(parameter_file_path, map_location=self.device))

        self.model.to(self.device)

    def single_volume_inference_unpadded(self, volume):
        """
        Runs inference on a single volume of arbitrary patch size,
        padding it to the conformant size first

        Arguments:
            volume {Numpy array} -- 3D array representing the volume

        Returns:
            3D NumPy array with prediction mask
        """
        
        raise NotImplementedError

    def single_volume_inference(self, volume):
        """
        Runs inference on a single volume of conformant patch size
        Requirements: 
        - volume is already normalized to range [0, 1]
        - volume has the correct path size (64, 64

        Steps this function applies:
        - slice input image (volume)  accross the x/0th dimension.
        - each slice is fed into the trained model (self.model)
        - the model outputs a (label/segmentation) mask (label for each pixel)
        - all masks are concatenated accross dimension x/0 (mask is put back together)

        Arguments:
            volume {Numpy array} -- 3D array representing the volume

        Returns:
            3D NumPy array with prediction mask
        """
        self.model.eval()

        # Assuming volume is a numpy array of shape [X,Y,Z] and we need to slice X axis
        slices = []

        # TASK: Write code that will create mask for each slice across the X (0th) dimension. After 
        # that, put all slices into a 3D Numpy array. You can verify if your method is 
        # correct by running it on one of the volumes in your training set and comparing 
        # with the label in 3D Slicer.
        with torch.no_grad():
            for idx0 in range(volume.shape[0]):
                ## get a slice of the volume:
                slc = volume[idx0, :, :]
                ## transform shape to [batch_size=1, channels=1, patch_size, patch_size]:
                slc = slc[None, None, :]
                ## to pytorch tensor:
                slc_ts = torch.from_numpy(slc)
                ## bring data to same device like model:
                slc_ts = slc_ts.to(self.device, dtype=torch.float)
                ## run inference
                prediction = self.model(slc_ts)
                ## during training we used a cross entropy loss function.
                ## Technically we would have to apply a softmax function
                ## for the prediction, because we do not get the probability for
                ## each class, but only the votes for each class. However, 
                ## since the softmax function is a monotonic increasing function
                ## it is sufficient to use the votes and use the majority vote for
                ## a channel/class (axis=1, -> argmux function) to select the predicted class:
                msk = prediction.argmax(axis=1).cpu().numpy()
                slices += [msk]
        return np.concatenate(slices, axis=0)
