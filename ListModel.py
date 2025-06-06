"""
ListModel.py
Abstract List Model class for displaying loaded templates to select.
"""
from pathlib import Path
from PyQt5.QtCore import QAbstractListModel, Qt
class ListModel(QAbstractListModel):
    '''Model for Qt View that displays list of selectable text items'''
    def __init__(self, template_folder: str):
        '''Initilizes list of template paths given the path location of the
        Templates folder'''
        super().__init__()
        self.template_folder = template_folder
        self.update_data()
    
    def data(self, index, role):
        '''The Qt View will call this and provide an index number of the data
        it is requesting. The role is role the Qt View is asking for.'''
        if role == Qt.DisplayRole:
            # index has .row() and .column() contain the index numbers
            # using row for list.
            # Display only the folder name, but stores absolute pathlib path object in list.
            pathlib_path = self.items[index.row()] 
            display_text = pathlib_path.name
            return display_text
    
    def rowCount(self, index):
        '''Qt View calls this to get the number of rows in the list,
        it is called so the Qt View knows the maximum index it can request
        from the data store.'''
        return len(self.items)
    
    def _get_templates(self, template_folder_path: str):
        """Takes in location of the source folder and returns list
        of all the files & dirs in that path, as Pathlib path objects.
        This is logical input output function only, independent of class wide varialbes."""
        templates = [folder for folder in Path(template_folder_path).iterdir()]
        return templates
    
    def update_data(self):
        """sets paths list (stored in self.items), using the tempaltes folder
        of this class instance, then emmits layout changed.
        This can be called after class has been initilized to refresh the
        list of paths, or can be called after self.template_folder has been
        changed to chagne the source folder to use."""
        self.items = self._get_templates(self.template_folder)
        self.layoutChanged.emit()