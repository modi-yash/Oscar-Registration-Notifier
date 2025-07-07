# Requirements
On Pushover (https://pushover.net):
    an API Token,
    and a User Key.

Python installed, 3.13 is what this is based on.

CRNS of your courses that you want to take. These can be found on Oscar.

# Directions
These will go into the sensitive_info.py file, formatted like "example_sensitive_info.py"

You will need a USER-AGENT, this can be any random string, but it is preferred to use your browser's user agent. If you do not know how to find this, you can search on Google "Find browser user agent," and copy and paste that into the USER-AGENT variable.

Put your CRNS into the "sensitive_info.py" file.

In your terminal, type "python -m  pip", and press enter. This will install pip, the Python installer. Then type "pip install -r requirements.txt", and press enter. This will install all the libraries you will need.

If you want to use a virtual environment, you can also use that to install the libraries. If you do not know what that is, you can safely ignore this.

After all this is done, go into your terminal and, in the directory which the "oscar_scraper.py" file is in, type "python oscar_scraper.py" in the terminal and press enter. This will activate the application. If you wish to exit the scraper, press Control + C.
