Steamz
======

CS316 Team Project



RUNNING OUR WEBSITE
To run our website through a virtual machine, run ./script.sh in the home Steamz directory on the command line. Then, input IP address http://0.0.0.0:8000/steam/ into your webbrowser to see our website. (Note that in order to do this through vagrant, port forwarding must be set up: we did this by altering our vagrantfile to include an additional line:   config.vm.network :forwarded_port, guest: 8000, host: 8000, auto_correct: true). From the webbrowser, it is then possible for the user to navigate the website through this web browser.  We have put our data in demo.json.  This is in the main directory in Steamz/data.  
