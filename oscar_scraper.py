# Required libraries
import requests, time
from log import log
from Course import *
from sensitive_info import *
import sys

# Puts all courses into a list
def make_courses(crn_list):
    all_courses_list = []
    with requests.Session() as session:
        session.headers.update({'user-agent': USER_AGENT})
        # Creates couses
        for crn in crn_list:
            num_tries = 0
            while num_tries < 3:
                try:
                    all_courses_list.append(Course(crn, session))
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
        log("Finished fetching data for all CRNs. Starting looping.")
        return all_courses_list

def loop_check_courses(courses,
                       sleep_time_between_courses: int = 1,
                       sleep_time_between_each_ping: int = 5,
                       sleep_time_between_error: int = 30):
    while(True):
        try:
            for course in courses:
                # Checks if the open registration seats have increased and hasn't already notified
                old_num_registered = course.num_registered
                course.update_num_registered()
                if(old_num_registered>course.num_registered # Registration slot has opened
                and course.registration_info[0]!=course.registration_info[1] # Registration is not max
                and course.num_registered!=-404 # Not first time checking
                and not course.has_notified):
                        # Posts message to api
                        r = requests.post("https://api.pushover.net/1/messages.json", data = {
                        "token": API_KEY,
                        "user": USER_KEY,
                        "message": f"Registration for {course.course_title} has changed and IS NOT full."
                        })
                        course.has_notified = True
                        log(f"Notification provided: \"Registration for {course.course_title} has changed and IS NOT full.\"")
                        # Ends the process (for now)
                        raise Exception("It works.")
                time.sleep(sleep_time_between_courses)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            log(f"Connection timed out. Please check your internet connection.")
            time.sleep(sleep_time_between_error)
        except Exception as e:
            log("Fatal error occurred:", e)
            sys.exit(1)
        time.sleep(sleep_time_between_each_ping)


# CRNS variable imported from sensitive_info.py
courses = make_courses(CRNS)
# Sleep times in seconds
sleep_time_between_courses = 1
sleep_time_between_each_ping = 5
sleep_time_between_error = 30
loop_check_courses(courses,
                   sleep_time_between_courses,
                   sleep_time_between_each_ping,
                   sleep_time_between_error)