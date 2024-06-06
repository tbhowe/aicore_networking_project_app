#!/bin/bash

# Update and install required packages non-interactively
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y python3-pip git


# Install python3-venv if not already installed
sudo apt-get install -y python3-venv


# Define the project directory
PROJECT_DIR="/home/ubuntu/networking_project/src"
# Clone the repository
git clone https://github.com/tbhowe/aicore_networking_project_app.git /home/ubuntu/networking_project




# Create virtual environment in the project directory
python3 -m venv $PROJECT_DIR/venv

# Activate the virtual environment
source $PROJECT_DIR/venv/bin/activate

# Install dependencies from requirements.txt
pip install -r $PROJECT_DIR/requirements.txt

# Deactivate the virtual environment
deactivate

# Provide feedback that the setup is complete
echo "Virtual environment and dependencies installed."

echo "Deployment completed successfully."