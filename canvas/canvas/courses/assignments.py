import requests
class Assignments:
    def __init__(self, course_id, api_key):
        self.course_id = course_id
        self.api_key = api_key
        self.base_url = f"https://morganstate.instructure.com/api/v1/courses/{course_id}/assignments"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
    def _get_assignments(self):
        """
        Fetches all assignments for the course.
        """
        response = requests.get(self.base_url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching assignments: {response.status_code} - {response.text}")
        
        
    def _parse_assignment(self, assignment):
        """
        Parses a single assignment and returns relevant details.
        """
        return {
            "assignment_course_id": str(self.course_id),
            "assignment_id": str(assignment.get("id")),
            "assignment_description": assignment.get("description"),
            "assignment_due_at": assignment.get("due_at"),
            "assignment_unlock_at": assignment.get("unlock_at"),
            "assignment_points_possible": assignment.get("points_possible"),
            "assignment_grading_type": assignment.get("grading_type"),
            "assignment_name": assignment.get("name"),
            "assignment_submission_types": assignment.get("submission_types"),
            "assignment_has_submitted_submissions": assignment.get("has_submitted_submissions"),
            "assignment_updated_at": assignment.get("updated_at")
        }
        
    def get_assignments(self):
        """
        Fetches and parses all assignments for the course.
        """
        assignments = self._get_assignments()
        parsed_assignments = [self._parse_assignment(assignment) for assignment in assignments]
        return parsed_assignments
    