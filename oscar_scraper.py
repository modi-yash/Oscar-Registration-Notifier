# First, install Python
# In your terminal, type "python -m  pip", press enter
# then type "pip install -r requirements.txt", press enter
# Pushover API Key - IF YOU ARE USING THIS, YOU NEED A PUSHOVER API KEY

# Required libraries
import time
from Course import *
from sensitive_info import *
import requests

# r = requests.post("https://api.pushover.net/1/messages.json", data = {
#   "token": API_KEY,
#   "user": USER_KEY,
#   "message": f"Test"
# })
courses = []
with requests.Session() as session:
    session.headers.update({'user-agent': USER_AGENT})
    
    # Creates couses
    for crn in CRNS:
        num_tries = 0
        while num_tries < 3:
            try:
                course = Course(crn, session)
                courses.append(course)
                break  # Success, exit retry loop
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                num_tries += 1
                print(f"Attempt {num_tries} for CRN {crn} failed: {e}")
                if num_tries == 3:
                    print(f"Giving up on CRN {crn} after 3 failed attempts.")
                else:
                    time.sleep(5)  # Wait before retrying
            except Exception as e:
                print(f"Error fetching data for CRN {crn}: {e}")
                break
        time.sleep(1)  # Sleep for 1 second to avoid overwhelming the server
    print("Finished fetching data for all CRNs.")

# while(True):
#     pass