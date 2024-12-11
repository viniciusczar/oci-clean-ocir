hi! 

<p> This repo will help you to clena oldest images in your repository (OCIR) in na OCI (oracle cloud).
</p>
<h5> Firstly, install on your environment: </h5>
    sudo apt-get update && sudo apt-get upgrade -y
    sudo apt-get install -y python3 python3-pip python3-venv
<h5> And then, execute python environment: </h5>
    python3 -m venv venv
    source venv/bin/activate
<h5> Install oci python lib for use oci sdk methods: </h5>
    pip install oci
<h5> Finally, execute: </h5>
    python3 scan_registry.py
    <p># That command will return the list of repositorys. You need copy then, paste in the repositories.txt file, remove undesire characters, like parentheses ( "()" ) and quantity number images. In the end, the list will be filled just the name.</p>
    python3 delete_oldest_images.py

