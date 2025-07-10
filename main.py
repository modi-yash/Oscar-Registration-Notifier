from oscar_scraper import *
from sensitive_info import CRNS
import random
debug_mode = True
# CRNS variable imported from sensitive_info.py
sleep_time_between_course_initialization = [5, 7]
courses = make_courses(CRNS,
                       sleep_time_between_course_initialization,
                       debug_mode)
sleep_time_between_courses = [5, 7]
sleep_time_between_each_ping = [250, 350]
sleep_time_between_error = [250, 350]
loop_check_courses(courses,
                   sleep_time_between_courses,
                   sleep_time_between_each_ping,
                   sleep_time_between_error,
                   debug_mode)