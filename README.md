# Hippocampal Volume Segmentation for Alzheimer's Disease detection

## Quantifying Alzheimer's Disease Progression Through Automated Measurement of Hippocampal Volume

Alzheimer's disease (AD) is a progressive neurodegenerative disorder that results in impaired neuronal (brain cell) function and eventually, cell death. AD is the most common cause of dementia. Clinically, it is characterized by memory loss, inability to learn new material, loss of language function, and other manifestations. 

For patients exhibiting early symptoms, quantifying disease progression over time can help direct therapy and disease management. 

A radiological study via MRI exam is currently one of the most advanced methods to quantify the disease. In particular, the measurement of hippocampal volume has proven useful to diagnose and track progression in several brain disorders, most notably in AD. Studies have shown reduced volume of the hippocampus in patients with AD.

The hippocampus is a critical structure of the human brain (and the brain of other vertebrates) that plays important roles in the consolidation of information from short-term memory to long-term memory. In other words, the hippocampus is thought to be responsible for memory and learning (that's why we are all here, after all!). Here is a GIF with highlighted left and right hippocampus:

![Hippocampus](./readme.img/Hippocampus_small.gif)

Humans have two hippocampi, one in each hemishpere of the brain. They are located in the medial temporal lobe of the brain. The word "hippocampus" is roughly translated from Greek as "horselike" because of the similarity to a seahorse, a peculiarity observed by one of the first anatomists to illustrate the structure.

<img src="./readme.img/Hippocampus_and_seahorse_cropped.jpg" width=200/>

According to [studies](https://www.sciencedirect.com/science/article/pii/S2213158219302542), the volume of the hippocampus varies in a population, depending on various parameters, within certain boundaries, and it is possible to identify a "normal" range when taking into account age, sex and brain hemisphere. 

<img src="./readme.img/nomogram_fem_right.svg" width=300>

There is one problem with measuring the volume of the hippocampus using MRI scans, though - namely, the process tends to be quite tedious since every slice of the 3D volume needs to be analyzed, and the shape of the structure needs to be traced. The fact that the hippocampus has a non-uniform shape only makes it more challenging. Do you think you could spot the hippocampi in this axial slice?

<img src="./readme.img/mri.jpg" width=200>

The goal is to build a piece of AI software that could help clinicians perform this task faster and more consistently.

## Repository description

We build an end-to-end AI system which features a machine learning algorithm (U-Net) that can be integrated into a clinical-grade viewer and automatically measures hippocampal volumes of new patients, as their studies are committed to the clinical imaging archive.

It is assumed that the patients brain scans are already cropped to a rectangular cube containing the hippocampus. This can be interpreted as if (fictional) radiology department runs a 'HippoCrop' tool which cuts out a rectangular portion of a brain scan from every image series and our committed radiologists have collected and annotated a dataset of relevant volumes, and converted them to NIFTI format.

We use the dataset that contains the segmentations of the right hippocampus and the U-Net architecture to build a segmentation model.

After that, we integrate the model into a working clinical PACS such that it runs on every incoming study and produces a report with volume measurements. For this task we need a working pipeline consisting of several software packages like Orthanc server, OHIF viewer, and so on. A detailed description is given is the subdirectory section3/.

## The Dataset

We are using the "Hippocampus" dataset from the [Medical Decathlon competition](http://medicaldecathlon.com/). This dataset is stored as a collection of NIFTI files, with one file per volume, and one file per corresponding segmentation mask. The original images here are T2 MRI scans of the full brain. As noted, in this dataset we are using cropped volumes where only the region around the hippocampus has been cut out. This makes the size of our dataset quite a bit smaller, our machine learning problem a bit simpler and allows us to have reasonable training times. This is not a "toy" problem, though. Algorithms that crop rectangular regions of interest are quite common in medical imaging. Segmentation is still hard.

## The Programming Environment

Recommended is a Python 3.7+ environment with the following libraries for the first two sections (see section1/ and section2/) of the project:

* nibabel
* matplotlib
* numpy
* pydicom
* PIL
* json
* torch (preferably with CUDA)
* tensorboard

For section 3 see sub-directory section3/ for more details.

## Project Instructions

### Section 1: Curating a dataset of Brain MRIs

<img src="./readme.img/Slicer.png" width=400em>

In the project directory called `section1` we will perform an exploratory data analysis (see file eda.ipynb). The goal is to inspect the dataset, understand the clinical side of the problem and get it ready for consumption by the ML algorithm in `section2`.

### Section 2: Training a segmentation CNN

<img src="./readme.img/loss.png" width=400em>

The directory called `section2/src` contains the source code that forms the framework for your machine learning pipeline.

We use [PyTorch](https://pytorch.org/) to train the model and we use [Tensorboard](https://www.tensorflow.org/tensorboard/) to visualize the results.

With the script `run_ml_pipeline.py` (or `run_ml_pipeline.ipynb`) we kick off the training pipeline. 

The code has hooks to log progress to Tensorboard. In order to see the Tensorboard output launch Tensorboard executable from the same directory where `run_ml_pipeline.py` is located using the following command:

> `tensorboard --logdir runs --bind_all`

After that, Tensorboard will write logs into directory called `runs` and you will be able to view progress by opening the browser and navigating to default port 6006 of the machine where you are running it.

### Section 3: Integrating into a clinical network

<img src="./readme.img/ohif.png" width=400em>

In this final section we use some of the work from Section 2 to create an AI product that can be integrated into a clinical network and provide the auto-computed information on the hippocampal volume to the clinicians. While hospital integrations are typically handled by hospital IT staff, it will help tremendously if you can talk the same language with the people who will operate your model, and will have a feel for how clinical radiological software works. These skills will also help you debug your model in the field.

You will perform this section in a different workspace than the previous two sections: **Workspace 2**. This workspace is a simpler hardware, with no GPU, which is more representative of a clinical environment. This workspace also has a few tools installed in it, which is replicates the following clinical network setup:

<img src="./readme.img/network_setup.png" width=400em>

Specifically, we have the following software in this setup:

* MRI scanner is represented by a script `section3/src/deploy_scripts/send_volume.sh`. When you run this script it will simulate what happens after a radiological exam is complete, and send a volume to the clinical PACS. Note that scanners typically send entire studies to archives.
* PACS server is represented by [Orthanc](http://orthanc-server.com/) deployment that is listening to DICOM DIMSE requests on port 4242. Orthanc also has a DicomWeb interface that is exposed at port 8042, prefix /dicom-web. There is no authentication and you are welcome to explore either one of the mechanisms of access using a tool like curl or Postman. Our PACS server is also running an auto-routing module that sends a copy of everything it receives to an AI server. See instructions ad the end of this page on how to launch if you are using the Udacity Workspace.  
* Viewer system is represented by [OHIF](http://ohif.org/). It is connecting to the Orthanc server using DicomWeb and is serving a web application on port 3000. Again, see instructions at the end of this page if you are using the Udacity Workspace.
* AI server is represented by a couple of scripts. `section3/src/deploy_scripts/start_listener.sh` brings up a DCMTK's `storescp` and configures it to just copy everything it receives into a directory that you will need to specify by editing this script, organizing studies as one folder per study. HippoVolume.AI is the AI module that you will create in this section.

If you want to replicate this environment on your local machine, you will find instructions in the Project Overview concept.

As with Section 2, in the directory called `section3/src` you will find the source code that forms the skeleton of the HippoVolume.AI module.

`inference_dcm.py` is the file that you will be working on. It contains code that will analyze the directory of the AI server that contains the routed studies, find the right series to run your algorithm on, will generate report, and push it back to our PACS.

Note that in real system you would architect things a bit differently. Probably, AI server would be a separate piece of software that would monitor the output of the listener, and would manage multiple AI modules, deciding which one to run, automatically. In our case, for the sake of simplicity, all code sits in one Python script that you would have to run manually after you simulate an exam via the `send_volume.sh` script - `inference_dcm.py`. It combines the functions of processing of the listener output and executing the model, and it does not do any proper error handling :)

As before, you will need to follow the instructions inside the code files to complete the section and create your AI module. Same convention is used as in Sections 1 and 2: comments that start with `# TASK` instruct you to create certain code snippets, and all other types of comments provide background or stand-out suggestions.

You will need to complete all the instructional comments in the code in order to complete this section. You can do this in any order, but it makes most sense to start with the code in `inference_dcm.py`.

Once you complete the code, you can test it by running
> `deploy_scripts/send_volume.sh`

which will simulate a completion of MRI study and sending of patient data to our PACS, and then following that by running `inference_dcm.py`

The `send_volume.sh` script needs to be run from directory `section3/src` (because it relies on relative paths). If you did everything correctly, an MRI scan will be sent to the PACS and to your module which will compute the volume, prepare the report and push it back to the PACS so that it could be inspected in our clinical viewer.

At this point, go to *[YOUR IP ADDRESS]*:3000 (can be another port if you are using Udacity Workspace) which brings up our OHIF viewer. You should be able to inspect your report in all its glory, in the context of a radiological study presented to a radiologist in a clinical viewer!

The study that `send_result.sh` sends, and a few other sample studies are located in `/data/TestVolumes`. Feel free to modify the script to try out your algorithm with other volumes.

> Note, that the DICOM studies used for inferencing this section have been created artificially, and while full-brain series belong to the same original study, this is not the study from which the hippocampus crop is taken.

Now that you have built a radiological AI system and given it to clinicians, you can start collecting data on how your model performs in the real world. If you (or the company you work for) intends to commercialize your technology, you will have to clear the regulatory bar. As we have discussed in our final lesson, an important contribution of an AI engineer to this endeavor is helping execute the clinical validation by contributing to a validation plan. Your final task in this course is to write a draft of such plan (shoot for 1-2 pages for this exercise). Remember - clinical validation is all about proving that your technology performs the way you claim it does. If you are saying that it can measure hippocampal volume, your validation needs prove that it actually does, and establish the extents to which your claim is true. Your validation plan needs to define how you would prove this, and establish these extents.

For the purpose of this exercise, assume that you have access to any clinical facility and patient cohorts you need, and that you have all the budget in the world. Assume that you know where your data came from and that you know how to label it (just come up with a good story). In your plan, touch on at least the following:

* Your algorithm relies upon certain "ground truth" - how did you define your ground truth? How will you prove that your method of collecting the ground truth is robust and represents the population that you claim this algorithm is good for?
* How do you define accuracy of your algorithm and how do you measure it with respect to real world population? Check out the [calculator and report from HippoFit](http://www.smanohar.com/biobank/calculator.html) for some inspiration.
* How do you define what data your algorithm can operate on?

There is no right answer here - think of these and other questions that would come up during validation of such algorithm. Thinking of such things early on will help you build better algorithms in the first place.

## Conclusion

This project implements a fully functional AI module for a radiological system. It requires knowledge of clinical context, data analysis, machine learning systems, and medical imaging networking. 

At the moment of writing in 2020, medical imaging AI is a very rapidly growing space, and the potential of the field is staggering. We are only starting to get access to good clinical datasets, the ImageNets of medical imaging is yet to come, clinician researchers are just starting to wrap their heads around what is possible with machine-learning-based technology and tools are becoming better every day. Information flow between data scientists and clinicians is key to unlocking the potential of medical AI and helping clinicians reduce the amount of mundane work, become more precise, efficient, and less stressed. This is just the beginning.

## License

This project is licensed under the MIT License

## Sources

[1] [www.sciencedirect.com/science/article/pii/S2213158219302542](https://www.sciencedirect.com/science/article/pii/S2213158219302542)  
[2] [en.wikipedia.org/wiki/Hippocampus](https://en.wikipedia.org/wiki/Hippocampus)  
[3] [medicaldecathlon.com/](http://medicaldecathlon.com/)
