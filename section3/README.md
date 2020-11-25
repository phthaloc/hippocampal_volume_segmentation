### Section 3: Integration into a clinical network

In this final section we use some of the work from Section 2 to create an AI product that can be integrated into a clinical network and provide the auto-computed information on the hippocampal volume to the clinicians. While hospital integrations are typically handled by hospital IT staff, it will help tremendously if a Data Scientist can talk the same language with the people who will operate the model, and will have a feel for how clinical radiological software works.

Specifically, we have the following software in this setup:

* MRI scanner is represented by a script `section3/src/deploy_scripts/send_volume.sh`. When you run this script it will simulate what happens after a radiological exam is complete, and send a volume to the clinical PACS. Note that scanners typically send entire studies to archives.
* PACS server is represented by [Orthanc](http://orthanc-server.com/) deployment that is listening to DICOM DIMSE requests on port 4242. Orthanc also has a DicomWeb interface that is exposed at port 8042, prefix /dicom-web. There is no authentication. Our PACS server is also running an auto-routing module that sends a copy of everything it receives to an AI server.
* Viewer system is represented by [OHIF](http://ohif.org/). It is connecting to the Orthanc server using DicomWeb and is serving a web application on port 3000. 
* AI server is represented by a couple of scripts. `section3/src/deploy_scripts/start_listener.sh` brings up a DCMTK's `storescp` and configures it to just copy everything it receives into a directory that you will need to specify by editing this script, organizing studies as one folder per study. HippoVolume.AI is the AI module that you will create in this section.

The complete system pipeline is illustrated in the figure below:
<img src="../readme.img/network_setup.png" width=400em>

The code for this section is located in `section3/src`.

`inference_dcm.py` contains code that will analyze the directory of the AI server that contains the routed studies, find the right series to run the algorithm on, will generate report, and push it back to the PACS.

Note that in real system you would architect things a bit differently. Probably, AI server would be a separate piece of software that would monitor the output of the listener, and would manage multiple AI modules, deciding which one to run, automatically. In our case, for the sake of simplicity, all code sits in one Python script that has to be run manually after an exam is simulateed via the `send_volume.sh` script - `inference_dcm.py`. It combines the functions of processing of the listener output and executing the model (it does not do any proper error handling).

Running the script 
> `deploy_scripts/send_volume.sh`
will simulate a completion of MRI study and send patient data to the PACS. After that run `inference_dcm.py`.

The `send_volume.sh` script needs to be run from directory `section3/src` (because it relies on relative paths). An MRI scan will be sent to the PACS and to the module which will compute the volume, prepare the report and push it back to the PACS so that it could be inspected in the clinical viewer.

At this point, go to *[YOUR IP ADDRESS]*:3000 which brings up the OHIF viewer. Inspect the report in the context of a radiological study presented to a radiologist in a clinical viewer.

The study that `send_result.sh` sends, and a few other sample studies are located in `/data/TestVolumes`. Feel free to modify the script to try out the algorithm with other volumes.

> Note, that the DICOM studies used for inferencing this section have been created artificially, and while full-brain series belong to the same original study, this is not the study from which the hippocampus crop is taken.

#### Requirements
In this 3rd section we will be working with three software products for emulating the clinical network. You would need to install and configure:
* [Orthanc server](https://www.orthanc-server.com/download.php) for PACS emulation
* [OHIF zero-footprint web viewer](https://docs.ohif.org/development/getting-started.html) for viewing images. Note that if you deploy OHIF from its github repository, at the moment of writing the repo includes a yarn script (`orthanc:up`) where it downloads and runs the Orthanc server from a Docker container. If that works for you, you won't need to install Orthanc separately.
* If you are using Orthanc (or other DICOMWeb server), you will need to configure OHIF to read data from your server. OHIF has instructions for this: https://docs.ohif.org/configuring/data-source.html
* You will also need to configure Orthanc for auto-routing of studies to automatically direct them to your AI algorithm. For this you will need to take the script that you can find at `section3/src/deploy_scripts/route_dicoms.lua` and install it to Orthanc as explained on this page: https://book.orthanc-server.com/users/lua.html
* [DCMTK tools](https://dcmtk.org/) for testing and emulating a modality. Note that if you are running a Linux distribution, you might be able to install dcmtk directly from the package manager (e.g. `apt-get install dcmtk` in Ubuntu)
