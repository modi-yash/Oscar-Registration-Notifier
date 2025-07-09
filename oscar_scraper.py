# Required libraries
import requests, time
from log import log
from Course import *
from sensitive_info import *
import sys

# Puts all courses into a list
def make_courses(crn_list, sleep_time_between_course_initialization = 1.0, debug: bool = False):
    all_courses_list = []
    with requests.Session() as session:
        session.headers.update({'user-agent': USER_AGENT})
        # Creates couses
        if debug: log("[Seats capacity, Seats taken, Seats available, Waitlist capacity, Waitlist taken, Waitlist remaining]")
        for crn in crn_list:
            num_tries = 0
            while num_tries < 3:
                try:
                    course = Course(crn, session)
                    all_courses_list.append(course)
                    # Prints all seats
                    if debug: log(f"{course.__str__()} - {course.registration_info}")
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
            time.sleep(sleep_time_between_course_initialization)  # Sleep for 1 second to avoid overwhelming the server
        print("Finished fetching data for all CRNs. Starting looping.")
        return all_courses_list

def loop_check_courses(courses,
                       sleep_time_between_courses = 1.0,
                       sleep_time_between_each_ping = 5.0,
                       sleep_time_between_error = 30.0,
                       debug: bool = False):
    while(True):
        try:
            for course in courses:
                # Checks if the open registration seats have increased and hasn't already notified
                old_num_available = course.num_available
                course.update_num_available()
                if(old_num_available<course.num_available # Registration slot has opened
                and course.num_available!=-404 # Not first time checking
                and not course.has_notified):
                        # Posts message to api
                        r = requests.post("https://api.pushover.net/1/messages.json", data = {
                        "token": API_KEY,
                        "user": USER_KEY,
                        "message": f"Registration for {course.course_title} has changed and IS NOT full."
                        })
                        course.has_notified = True
                        log(f"Notification provided: \"Registration for {course.course_title} has changed and IS NOT full.\" From {old_num_available} available to {course.num_available}")
                time.sleep(sleep_time_between_courses)
            time.sleep(sleep_time_between_each_ping)
        except KeyboardInterrupt as e:
            # Exiting the program
            if debug:
                log("[Seats capacity, Seats taken, Seats available, Waitlist capacity, Waitlist taken, Waitlist remaining]")
                for course in courses:
                    log(f"{course.__str__()} - {course.registration_info}")
            raise KeyboardInterrupt()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            # Internet connection or timeout error
            log(f"Connection timed out. Please check your internet connection.")
            time.sleep(sleep_time_between_error)
        except Exception as e:
            # Other errors
            log("Fatal error occurred:", e)
            sys.exit(1)