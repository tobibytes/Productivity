import requests
from canvas.semester import Semester
from canvas.secret import KeyEncryptor
class CanvasFirst:

    def __init__(self, api_key: str, email: str):
        self.api_key = api_key
        self.email = email
        self.account_id = None
        self.base_url = "https://canvas.instructure.com/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        
    def _get_courses(self):
        """
        Get a list of courses from the Canvas API.
        """
        url = f"{self.base_url}/courses"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching courses: {response.status_code} - {response.text}")
        
    def _get_cur_semester_courses(self):
        """
        Get the courses for the current semester.
        """
        courses = self._get_courses()
        current_semester_courses = []
        for course in courses:
            if len(course.keys()) < 5:
                continue
            if Semester.check_in_semester(course['created_at']):
                course = self._format_course(course)
                current_semester_courses.append(course)
        return current_semester_courses
    
    def _format_course(self, course):
        return {
            "course_id": course['id'],
            "course_account_id": self.account_id,
            "course_name": course['name'],
            "course_code": course['course_code'],
            "course_uuid": course['uuid'],
            "course_created_at": course['created_at'],
            "course_semester": Semester.get_cur_semester()
        }
    def _get_user(self):
        return {
            "email": self.email,
            "api_key": KeyEncryptor.encrypt(self.api_key),
        }
    
    def get_user_and_courses(self):
        """
        Get the user and their courses.
        """
        courses = self._get_cur_semester_courses()
        user_info = self._get_user()
        user.update({
            "courses": courses
        })
        return user_info
    