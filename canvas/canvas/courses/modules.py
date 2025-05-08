"""

"""
import requests
class Modules:
    """
    This class is used to manage the modules in a course.
    """
    
    def __init__(self, course_id, api_key: str):
        self.base_url = "https://morganstate.instructure.com/api/v1"
        self.course_id = course_id
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
    
    def _get_modules(self):
        """
        Get the modules for a course.
        """
        url = f"{self.base_url}/courses/{self.course_id}/modules"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching modules: {response.status_code} - {response.text}")
        
    def _get_module_items_general(self, module_id):
        """
        Get the items for a module.
        """
        url = f"{self.base_url}/courses/{self.course_id}/modules/{module_id}/items"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching module items: {response.status_code} - {response.text}")
    
    def _get_module_items(self, module_general):
        """ 
        Get the specific items for a module.
        """
        url = module_general['url']
        response = requests.get(url, headers = self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching module items: {response.status_code} - {response.text}")
    
    
    def _parse_module_item(self, module_item, module_parent_id=None):
        """
        Parse the module item.
        """
        return {
            "module_item_module_id": module_parent_id,
            "module_item_id": module_item['id'],
            "module_item_title": module_item['display_name'],
            "module_item_filename": module_item['filename'],
            "module_item_uuid": module_item['uuid'],
            "module_item_type": module_item['mime_class'],
            "module_item_content_type": module_item['content-type'],
            "module_item_download_url": module_item['url'],
            "module_item_size": module_item['size'],
            "module_item_created_at": module_item['created_at'],
        }
        
    def _parse_module(self, module):
        """
        Parse the module.
        """
        return {
            "module_course_id": self.course_id,
            "module_id": module['id'],
            "module_name": module['name'],
            "module_completed_at": module['completed_at'],
            "module_state": module['state'],
            "module_prerequisite_ids": module['prerequisite_module_ids'],
        }
        
    def get_modules(self):
        """ 
        Get the modules for a course.
        """
        modules = self._get_modules()
        parsed_modules = []
        for module in modules:
            parsed_module = self._parse_module(module)
            module_items_general = self._get_module_items_general(module['id'])
            parsed_module['module_items'] = []
            for module_item_general in module_items_general:
                parsed_module['module_items'].append(self._parse_module_item(self._get_module_items(module_item_general), module['id']))
            parsed_modules.append(parsed_module)
        return parsed_modules