from sensitive_info import USER_AGENT
from log import log
import requests
from bs4 import BeautifulSoup, Tag # type: ignore
from typing import Optional

class Course:
    def __init__(self, crn: int, session: Optional[requests.Session] = None):
        self.has_notified = False
        self.course_crn = crn
        if session is None:
            self.session = requests.Session()
            self.session.headers.update({'user-agent': USER_AGENT})
        else:
            self.session = session
        self.course_title = ""
        self.course_department = ""
        self.course_number = ""
        self.course_section = ""
        self.url = f"https://oscar.gatech.edu/pls/bprod/bwckschd.p_disp_detail_sched?term_in=202508&crn_in={self.course_crn}"
        self.num_available = -404 # will change in update_num_available call in fetch_course_data
        self.registration_info = [] # same as above variable
        # Fetch course data when the object is created
        self.fetch_course_data()

    def fetch_course_data(self):
        # Make a GET request to the URL
        try:
            response = self.session.get(self.url, timeout=10)
            # Check if the request was successful
            # If the request was successful, parse the HTML content
            if response.status_code == 200:
                html = response.content
                self.update_num_available(html)
                soup = BeautifulSoup(html, 'html.parser')
                course_information = soup.find(class_='ddlabel', scope="row")
                if course_information:
                    course_information = course_information.get_text(strip=True)
                    if " - " in course_information:
                        course_information = course_information.split(" - ")
                        # print(course_information)
                        # Assuming the course title is the first part, department and number are the second, and section is the third
                        self.course_title = course_information[0]
                        self.course_department, self.course_number = course_information[2].split(" ")
                        self.course_section = course_information[3]
                    else:
                        log("Error in parsing course information.")
            # Response not found
            elif response.status_code == 404:
                log("Page not found (404). Please check the URL.")
            # Other response errors
            else:
                log(f"Failed to retrieve the page. Status code: {response.status_code}")
        # Error handling for connection issues
        except requests.exceptions.ConnectionError as e:
            log("Connection error. Please check your internet connection,", e)
            return
        except requests.exceptions.Timeout as e:
            log("Connection timed out. Please check your internet connection,", e)
            return
        except requests.exceptions.RequestException as e:
            log("An error occurred while making the request:", e)
            return

    def update_num_available(self, html=None) -> int:
        try:
            # Finds html code if it is not inputted
            if html is None:
                response = self.session.get(self.url, timeout=10)
                if response.status_code == 200:
                    html = response.content
                # Error handling for response
                elif response.status_code == 404:
                    log("Page not found (404). Please check the URL.")
                    return -2
                else:
                    log(f"Failed to retrieve the page. Status code: {response.status_code}")
                    return -2
            soup = BeautifulSoup(html, 'html.parser')
            # Example: Find the number of registered students (update selector as needed)
            table = soup.find('table', class_='datadisplaytable', summary='This layout table is used to present the seating numbers.')
            if isinstance(table, Tag):
                self.registration_info = [item.get_text() for item in table.find_all('td', class_='dddefault')]
                self.num_available = int(self.registration_info[0]) - int(self.registration_info[1])
                return self.num_available
            else:
                log("Could not find the seating numbers table.")
            return -1
        except requests.exceptions.ConnectionError as e:
            log("Connection error. Please check your internet connection,", e)
            return -1
        except requests.exceptions.Timeout as e:
            log("Connection timed out. Please check your internet connection,", e)
            return -1
        except requests.exceptions.RequestException as e:
            log("An error occurred while making the request:", e)
            return -1
        except Exception as e:
            log("An error occurred while parsing the HTML:", e)
            return -1

    def __repr__(self):
        return f"Course({self.course_crn}, {self.course_title}, {self.course_department}, {self.course_number}, {self.course_section})"
    
    def __str__(self):
        return f"CRN: {self.course_crn}, Title: {self.course_title}, Department: {self.course_department}, Number: {self.course_number}, Section: {self.course_section}"