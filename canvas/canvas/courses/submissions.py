import requests


class Submissions:
    def __init__(self, course_id, assignment_id, api_key):
        self.course_id = course_id
        self.api_key = api_key
        self.assignment_id = assignment_id
        self.base_url = f"https://morganstate.instructure.com/api/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/pdf"
        }
        
    def _create_submission_step_1(self, url, filename):
        base_url = self.base_url + "/users/self/files"
        data = requests.post(base_url, headers= self.headers, data= {
            "name": filename,
            "url": url,
            
        })
        return data.json()
        
    def _create_submission_step_2(self, upload_url, target_url, upload_params, filename):
        # Upload the file to the upload_url
        # This is a placeholder for the actual upload logic
        # You would typically use a library like requests to handle the file upload
        # For example:
        upload_params['target_url'] = target_url
        upload_params['filename'] = filename
        upload_params['content_type'] = "application/pdf"  # or your real MIME type

        multipart_data = {key: (None, value) for key, value in upload_params.items()}

        response = requests.post(upload_url, files=multipart_data)
        return response.json()
    
    def create_submission(self, url, filename):
        """
        Create a submission for the assignment.
        """
        # Step 1: Create the submission
        data = self._create_submission_step_1(url, filename)
        
        # Step 2: Upload the file
        upload_url = data.get('upload_url')
        target_url = url
        upload_params = data.get('upload_params')
        
        if not upload_url or not target_url or not upload_params:
            raise Exception("Missing upload URL or parameters in the response")
        
        return self._create_submission_step_2(upload_url, target_url, upload_params, filename)
    
    def _make_submission(self, submission_file_id=None, submission_type="online_upload"):
        """
        Make a submission for the assignment using an uploaded file.
        """
        url = f"{self.base_url}/courses/{self.course_id}/assignments/{self.assignment_id}/submissions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }

        payload = {
            "submission[submission_type]": "online_upload",
            "submission[file_ids][]": submission_file_id
            # "submission[body]": submission_body,
        }

        response = requests.post(url, headers=headers, data=payload)

        if response.status_code in range(200, 300):
            return response.json()
        else:
            raise Exception(f"Error making submission: {response.status_code} - {response.text}")
        
    def make_submission(self, url=None, filename=None):
        """
        Make a submission for the assignment.
        """
        data = self.create_submission(url, filename)
        file_id = data.get('id')
        
        return self._make_submission(submission_file_id=file_id)