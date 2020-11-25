How to run the clinical application simulation:
    - if scripts in the deploy_scripts directory are not executable directly because of error "storescu: command not found", copy the bash commands within these scripts and run them (in correct order) by hand in terminal.

Steps for running the production environment:
1. copy model weights file from section2/results/<specific_run_directory>/model.path to directory section3/src/

2. Launch the Orthanc in terminal window (run from directory where script is located): bash launch_orthanc.sh
   you can verfy that it is working: echoscu 127.0.0.1 4242 -v

3. open new terminal window and launch OHIF image viewer in seperate terminal (run from directory where script is located) and do not close it: bash launch_OHIF.sh 

4. Open new terminal window and start AI server by running bash script start_listener.sh or by entering into terminal (the following commands have to be executed from directory deplay_scripts):
	curl -X POST http://localhost:8042/tools/execute-script --data-binary @route_dicoms.lua -v
	storescp 106 -v -aet HIPPOAI -od /home/workspace/src/routed/ --sort-on-study-uid st

5. Open new terminal window and simulate an exam by running the send_volume.sh script or by entering command:
	storescu 127.0.0.1 4242 -v -aec HIPPOAI +r +sd /data/TestVolumes/Study1
available test volumes: Study1, Study2, Study3

6. run the inference_dcm.py from src directory to create the report report.dcm:
	python inference_dcm.py routed/

(7.) this step is not necessary because the script inference_dcm.py already sends the report.dcm file to the OHIF image viewer.
send the report (report.dcm file) to the OHIF image viewer using the send_result.sh script or by running the following command from "src" directory:
	storescu 127.0.0.1 4242 -v -aec HIPPOAI report.dcm
