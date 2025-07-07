from oscar_scraper import *

debug_mode = False
# CRNS variable imported from sensitive_info.py
sleep_time_between_course_initialization = 1.0 # Must be float value, "*.***"
courses = make_courses(CRNS,
                       sleep_time_between_course_initialization,
                       debug_mode)
# Sleep times in seconds (same as above, must be floats)
sleep_time_between_courses = 1.0
sleep_time_between_each_ping = 5.0
sleep_time_between_error = 30.0
loop_check_courses(courses,
                   sleep_time_between_courses,
                   sleep_time_between_each_ping,
                   sleep_time_between_error,
                   debug_mode)