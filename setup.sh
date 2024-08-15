# setup.sh

# Necessary system packages
if [ "$(uname)" == "Linux" ]; then
	sudo apt-get update
	sudo apt-get install -y python3.9-tk
fi

# Installation of Python packages
pip install -r requirements.txt