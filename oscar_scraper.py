# First, install Python
# In your terminal, type "python -m  pip", press enter
# then type "pip install -r requirements.txt", press enter
# Pushover API Key - IF YOU ARE USING THIS, YOU NEED A PUSHOVER API KEY

# Required libraries
import requests, time
from log import log
from Course import *
from sensitive_info import *

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
                log(f"Attempt {num_tries} for CRN {crn} failed: {e}")
                if num_tries == 3:
                    log(f"Giving up on CRN {crn} after 3 failed attempts.")
                else:
                    time.sleep(5)  # Wait before retrying
            except Exception as e:
                log(f"Error fetching data for CRN {crn}: {e}")
                break
        time.sleep(1)  # Sleep for 1 second to avoid overwhelming the server
    print("Finished fetching data for all CRNs. Starting looping.")

while(True):
    for course in courses:
        if(course.num_registered<course.update_num_registered() and course.registration_info[0]!=course.registration_info[1]
            and course.num_registered!=-404 and not course.has_notified): # checks if the registration seats have changed
                r = requests.post("https://api.pushover.net/1/messages.json", data = {
                "token": API_KEY,
                "user": USER_KEY,
                "message": f"Registration for {course.course_title} has changed and IS NOT full."
                })
                course.has_notified = True
                log(f"Notification provided: \"Registration for {course.course_title} has changed and IS NOT full.\"")
                raise Exception("It works.")
        time.sleep(1)
    time.sleep(5)