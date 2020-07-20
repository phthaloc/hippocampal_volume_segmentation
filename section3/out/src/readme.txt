ATTENTION: in udacity workspace it could be that scripts in deploy_scripts directory are not executable directly.
You have to copy the bash commands and run them by hand in terminal.
1. upload weight file (from section2/out/src/runs/<selected_weight_file> rename file and copy to section3/out/parameters/weights.weights)
1. Launch the Orthanc in terminal window: bash launch_orthanc.sh
   you can verfy that it is working: echoscu 127.0.0.1 4242 -v
2. Launch OHIF image viewer in seperate terminal and do not close them:
   bash launch_OHIF.sh 
3. Start AI server by running bash script start_listener.sh
4. Simulate an exam via the send_volume.sh script
5. run the inference_dcm.py to create the report report.dcm
6. send the report to the OHIF image viewer using the send_result.sh script
