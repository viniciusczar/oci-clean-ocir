hi! 

 This repo will help you to clena oldest images in your repository (OCIR) in na OCI (oracle cloud).
 Firstly, install on your environment: 
    sudo apt-get update && sudo apt-get upgrade -y
    sudo apt-get install -y python3 python3-pip python3-venv
 And then, execute python environment:
    python3 -m venv venv
    source venv/bin/activate
 Install oci python lib for use oci sdk methods:
    pip install oci
 Finally, execute: 
    python3 scan_registry.py
    # That command will return the list of repositorys. You need copy then, paste in the repositories.txt file, remove undesire characters, like parentheses ( "()" ) and quantity number images. In the end, the list will be filled just the name.
    python3 delete_oldest_images.py
