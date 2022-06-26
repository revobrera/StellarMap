from PyQt5.QtCore import (  # PyQt5 libraries and sub-libaries
    QAbstractTableModel, Qt)


class PandasModel(QAbstractTableModel):

    def __init__(self, data):
        """
        This function initializes table model.
        It is a constuctor so it gets called when object is created in line ..
        """

        QAbstractTableModel.__init__(self)
        self._data = data


    def rowCount(self, parent=None):
        """
        Simply returns the number of rows of table when called
        """

        return self._data.shape[0]


    def columnCount(self, parnet=None):
        """
        This piece of code returns number of columns when called
        """

        return self._data.shape[1]


    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        """
        This function returns the alignment of any object that gets passed in it
        """

        #Checking if passed object is valid
        if index.isValid():
            
            
            #If object is set to display role it returns the location of data in it
            if role == Qt.ItemDataRole.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])


            #Otherwise it goes to desired column and returns its alignment
            column_count = self.columnCount()

            for column in range(0, column_count):

                if (index.column() == column and role == Qt.ItemDataRole.TextAlignmentRole):
                    return Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter



        #If object is invalid  or desired column does not exist it returns None
        return None


    def headerData(self, col, orientation, role):
        """
        This function returns the location of header
        """

        #Return location if layout is horizontal and role is on display only mode
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self._data.columns[col]
        return None


    def setData(self, index, value, role):
        """
        This function sets value to a field
        """

        #Checker to see if given index location is valid
        if not index.isValid():
            return False

        #Checker to see if desired field is set on edit mode
        if role != Qt.ItemDataRole.EditRole:
            return False


        #Check if row number for desired index is valid
        row = index.row()
        if row < 0 or row >= len(self._data.values):
            return False


        #Check if column number for desired index is valid
        column = index.column()
        if column < 0 or column >= self._data.columns.size:
            return False

        
        #If all above conditions are true only then set value at given index
        self._data.iloc[row][column] = value
        self.dataChanged.emit(index, index)

        return True

    def flags(self, index):
        """
        This function basically sets the default windows button bar
        """

        flags = super(self.__class__, self).flags(index)
        flags |= Qt.ItemFlag.ItemIsEditable
        flags |= Qt.ItemFlag.ItemIsSelectable
        flags |= Qt.ItemFlag.ItemIsEnabled
        flags |= Qt.ItemFlag.ItemIsDragEnabled
        flags |= Qt.ItemFlag.ItemIsDropEnabled

        return flags
