"""
ProjectTemplate.py
Copies template directory into destination directory using shutil copytree
raises ProjectTemplateError if shutil.copytree raises exception.
"""
import shutil

class ProjectTemplateError(Exception):
    pass

class ProjectTemplate:
    def __init__(self, template_dir, project_dir):
        self.template_dir = template_dir
        self.project_dir = project_dir
        
    def create_project(self):
        try:
            shutil.copytree(self.template_dir, self.project_dir)
            ## Debuging and Testing mode, the above line is commented out in place of the below line.
            #print(f"ProjectTemplate Test Mode:\nCopying {self.template_dir} to {self.project_dir}")
        except Exception as e:
            raise ProjectTemplateError(f'Error creating project: {str(e)}')

