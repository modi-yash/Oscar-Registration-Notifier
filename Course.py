from sensitive_info import *

import requests
from bs4 import BeautifulSoup, Tag # type: ignore
from typing import Optional

class Course:
    def __init__(self, crn: int, session: Optional[requests.Session] = None):
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
        self.nums_registered = self.update_nums_registered()
        # Fetch course data when the object is created
        self.fetch_course_data()

    def fetch_course_data(self):
        # Make a GET request to the URL
        try:
            response = self.session.get(self.url)
            # Check if the request was successful
            # If the request was successful, parse the HTML content
            if response.status_code == 200:
                html = response.content
                self.update_nums_registered(html)
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

    def update_nums_registered(self, html=None) -> int:
        try:
            # Finds html code if it is not inputted
            if html is None:
                response = self.session.get(self.url)
                if response.status_code == 200:
                    html = response.content
                # Error handling for response
                elif response.status_code == 404:
                    print("Page not found (404). Please check the URL.")
                    return -2
                else:
                    print(f"Failed to retrieve the page. Status code: {response.status_code}")
                    return -2
            soup = BeautifulSoup(html, 'html.parser')
            # Example: Find the number of registered students (update selector as needed)
            table = soup.find('table', class_='datadisplaytable', summary='This layout table is used to present the seating numbers.')
            if isinstance(table, Tag):
                self.nums_registered = list(map(lambda item: item.get_text(), (table.find_all('td', class_='dddefault'))))
                return self.nums_registered[1]
            else:
                print("Could not find the seating numbers table.")
            return -1
        except requests.exceptions.ConnectionError as e:
            print("Connection error. Please check your internet connection,", e)
            return -1
        except requests.exceptions.Timeout as e:
            print("Connection timed out. Please check your internet connection,", e)
            return -1
        except requests.exceptions.RequestException as e:
            print("An error occurred while making the request:", e)
            return -1
        except Exception as e:
            print("An error occurred while parsing the HTML:", e)
            return -1

    def __repr__(self):
        return f"Course({self.course_crn}, {self.course_title}, {self.course_department}, {self.course_number}, {self.course_section})"
    
    def __str__(self):
        return f"CRN: {self.course_crn}, Title: {self.course_title}, Department: {self.course_department}, Number: {self.course_number}, Section: {self.course_section}"