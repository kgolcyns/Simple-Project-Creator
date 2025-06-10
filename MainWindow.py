"""
MainWindow.py
Main Window Widget and implementation
"""
import os
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QWidget, QFileDialog
from PyQt5 import uic
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from ProjectTemplate import ProjectTemplate, ProjectTemplateError
from ListModel import ListModel
import re

from test_foldername_pattern import PATTERN # Use the regex expression defined here

base_dir = os.path.dirname(__file__)

def connect(signal,slot):
    signal.connect(slot)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        # Initilize ProjectTemplate Class
        #self.app_template_creator = ProjectTemplate(os.path.join(base_dir, 'Templates'))
        
    def initUI(self):
        uic.loadUi(os.path.join(base_dir, "MainWindow.ui"), self)
        self.setWindowTitle('Project Template Creator')
        
        # Configure templateList model and selection
        self.templateListModel = ListModel(os.path.join(base_dir, 'Templates'))
        self.templateList.setModel(self.templateListModel)
        self.templateListSelection = self.templateList.selectionModel()
        
        # Connections
        self.browseButton.clicked.connect(self.select_destination_dir)
        self.destinationFolder.textChanged.connect(self.update_create_button_state)
        connect(self.nameLineEdit.textChanged, self.update_create_button_state)
        self.templateListSelection.selectionChanged.connect(self.update_create_button_state)
        self.createButton.clicked.connect(self.create_project)
        
        # Initialize Button States
        self.update_create_button_state()
        #self.createButton.setEnabled(False)
    
    def select_destination_dir(self):
        dialog = QFileDialog(self)
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        dialog.setOption(QFileDialog.ShowDirsOnly, True)
        dialog.setWindowTitle("Select Folder to Create New Template")
        
        #Connect the finished signal to a custom slot
        dialog.finished.connect(self.handle_folder_selected)
        dialog.open()
    
    def handle_folder_selected(self, result):
        dialog = self.sender()
        if result == QFileDialog.Accepted:
            selected_folder = dialog.selectedFiles()[0]
            print(f"Selected: {selected_folder}")
            self.destinationFolder.setText(selected_folder)
        else:
            print("cancled")
        
    def update_create_button_state(self):
        """This slot sets the enabled state of the create button.
        Is enabled only when item selected in templateList and
        text is populated in destinationFolder."""
        if self.destinationFolder.text() and self.templateList.selectedIndexes() and self.nameLineEdit.text(): #TODO: have nameLineEdit go through validationregex function for the and (b/c more intuative than validating after clicking create button)
            self.createButton.setEnabled(True)
        else:
            self.createButton.setEnabled(False)
    
    def create_project(self):
        """Get:
        - values of Selected template from self.templateList ListView
        - destination dir from destinationFolder LineEdit
        
        then setup ProjectTemplate class with those source and destination,
        then run the create_project to create the project, then handle any exceptions
        or successful creation messages to user.
        """
        # check destination######################do this ## validation later TODO: THERE IS NO NAME VALIDATION!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        ##name = self.nameLineEdit.text()
        ##if not re.match('^[A-Za-z0-9][A-Za-z0-9-_.]*[A-Za-z0-9]\Z', name,flags=re.MULTILINE):
        ##    # print validation error to user that they have invalid name for Name field in project name
        ##    #TODO: verify this validaiton!!!!!!!!!!!!!
        ##    print('your dam Name is not avalid file name specifier, and the idiot programmer of this was too egotistical to give you a messagebox to say this\n+formal proving of this validation!!!')
        ##    return None
        ##else:
        ##    destination = os.path.join(self.destinationFolder.text(), name)
        ##    print('full destination since pass re:', destination)
        ##
        
        """Get provided strings, and validate name string with regx and if pass, create full path,
        then move to the try/except block to run the template maker. If not pass, then print error and msgbox to user
        giving them the error and telling them to fix it. (think of jokes also, like returning not match [raw regx pattern string],
        saying must be a valid [raw pattern string]. funny b/c its in the wording of a traditional ,well written, file error message
        but obviossly not of any use to the user (even if they are a programemr), but funny to the programmer, and the user will get the joke if they are a programmer"""
        location = self.destinationFolder.text().strip()
        folderName = self.nameLineEdit.text().strip()
        
        # check for empty strings
        if not location or not folderName:
            # bring mesaage and state that they need to fill in both fields
            # This is more serious, as they shoulden't have been able to press the button in the first place
            # (this comes before the regex validation, but if it came after, it would be a more serious error-
            # B/C that means the regex validation coulden't even catch this most basic error)
            # TODO: write msgbox (more serious) error for empty fields
            print('EMPTY Field: you need to fill in both fields')
            return None
        
        # run conclusive inputvalidation of the input folder name
        if re.match(PATTERN, folderName) is None:
            """Invalid foldername specified, so bring up msgbox to user saying that they need to fix it.
            This block is part of normal operation"""
            print(f'INVALID {folderName} specified: not a valid folder name')
            #TODO: write msgbox error for invalid folder name
            return None
        
        # concatenate full pathname
        # provide one more sanity check if the full path exists, so it can be gracefully handled here alerted here, ()
        # (shutil should be set to never overwrite,  so this should never happen, and shutil errors should be handled in the try/except block
        # as they are more sereious and unexpected errors there)
        destination = os.path.join(location, folderName)
        if os.path.exists(destination) is True:
            """Path already exists: bring up msgbox to user saying that they need to specify a different folder name
            or a different save location."""
            print(f'{destination} already exists:\nyou need to specify a different folder name or a different save location')
            #TODO: write msgbox error for path exists
            return None
        
        
        
        try:
            # get source template path that is selected
            source = self.templateListModel.items[self.templateList.selectedIndexes()[0].row()]; print('\n'+str(source))
            
            #destination = self.destinationFolder.text(); print(destination)
            #######################destination = os.path.join(self.destinationFolder.text(), self.nameLineEdit.text()); print(destination)
            #### destination = validate_name(name) + destination if validate_name was true
            
            ## DEBUG:
            print('------------')
            print('     Source:', source)
            print('Destination:', destination)
            print('------------')
            
            TemplateMaker = ProjectTemplate(source, destination)
            TemplateMaker.create_project()
        except ProjectTemplateError as err:
            print("Project Tempalte error: " + str(err))
        except Exception as err:
            print("EVEN BIGGER GENERAL Error, You better give up :(\n" + str(err))
        
        else:
            print("Template Cretated Succussfully! :)")
            # open the directory in file explorer
            showDestinationSuccessful = QDesktopServices.openUrl(QUrl.fromLocalFile(destination))
            if showDestinationSuccessful is True:
                print("Opened Destination Folder in Explorer! :)")
            else:
                print("Failed to Open Destination Folder in Explorer :(")
        
        