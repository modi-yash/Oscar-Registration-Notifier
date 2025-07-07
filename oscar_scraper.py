# First, install Python
# In your terminal, type "python -m  pip", press enter
# then type "pip install -r requirements.txt", press enter
# Pushover API Key - IF YOU ARE USING THIS, YOU NEED A PUSHOVER API KEY
from sensitive_info import API_KEY
# Required libraries
import requests
from bs4 import BeautifulSoup # type: ignore
import time
from typing import Optional

class Course:
    def __init__(self, crn: int, session: Optional[requests.Session] = None):
        self.course_crn = crn
        if session is None:
            self.session = requests.Session()
            self.session.headers.update({'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})
        else:
            self.session = session
        self.course_title = ""
        self.course_department = ""
        self.course_number = ""
        self.course_section = ""
        self.url = f"https://oscar.gatech.edu/pls/bprod/bwckschd.p_disp_detail_sched?term_in=202508&crn_in={self.course_crn}"
        self.num_registered = 0
        # Fetch course data when the object is created
        self.fetch_course_data()

    def fetch_course_data(self):
        # Make a GET request to the URL
        try:
            response = self.session.get(self.url)
            # Check if the request was successful
            # If the request was successful, parse the HTML content
            if response.status_code == 200:
                # self.update_num_registered()
                html = response.content
                soup = BeautifulSoup(html, 'html.parser')
                course_information = soup.find(class_='ddlabel', scope="row")
                if course_information:
                    course_information = course_information.get_text(strip=True)
                    if " - " in course_information:
                        course_information = course_information.split(" - ")
                        print(course_information)
                        # Assuming the course title is the first part, department and number are the second, and section is the third
                        self.course_title = course_information[0]
                        self.course_department, self.course_number = course_information[2].split(" ")
                        self.course_section = course_information[3]
                    else:
                        print("Course not found.")
            # Response not found
            elif response.status_code == 404:
                print("Page not found (404). Please check the URL.")
            # Other response errors
            else:
                print(f"Failed to retrieve the page. Status code: {response.status_code}")
        # Error handling for connection issues
        except requests.exceptions.ConnectionError as e:
            print("Connection error. Please check your internet connection,", e)
        except requests.exceptions.Timeout as e:
            print("Connection timed out. Please check your internet connection,", e)
        except requests.exceptions.RequestException as e:
            print("An error occurred while making the request:", e)

    def update_num_registered(self):
        try:
            response = self.session.get(self.url)
            # Check if the request was successful
            # If the request was successful, parse the HTML content
            if response.status_code == 200:
                pass
            # Response not found
            elif response.status_code == 404:
                print("Page not found (404). Please check the URL.")
            # Other response errors
            else:
                print(f"Failed to retrieve the page. Status code: {response.status_code}")
        except requests.exceptions.ConnectionError as e:
            print("Connection error. Please check your internet connection,", e)
        except requests.exceptions.Timeout as e:
            print("Connection timed out. Please check your internet connection,", e)
        except requests.exceptions.RequestException as e:
            print("An error occurred while making the request:", e)

    def __repr__(self):
        return f"Course({self.course_crn}, {self.course_title}, {self.course_department}, {self.course_number}, {self.course_section})"
    
    def __str__(self):
        return f"CRN: {self.course_crn}, Title: {self.course_title}, Department: {self.course_department}, Number: {self.course_number}, Section: {self.course_section}"

crn_nums = [83543, 82855, 86793, 81192, 88149, 83431, 93239, 91697, 86193, 92480, 91142, 85530, 83169]
courses = []
with requests.Session() as session:
    session.headers.update({'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})
    
    # Creates couses
    for crn in crn_nums:
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