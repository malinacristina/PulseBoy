from PyQt5 import QtCore, QtGui
import pickle as pickle
import random

default_row = [[0, [], '']]


class ExperimentModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.headerdata = ['Active Valves', 'Parameters', 'Trial Name']
        self.arraydata = default_row.copy()
        self.current_trial = 0

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0])

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        elif role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        return QtCore.QVariant(str(self.arraydata[index.row()][index.column()]))

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.headerdata[col])
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return int(col)
        return QtCore.QVariant()

    def append_row(self, row):
        if self.arraydata[0] == default_row.copy()[0]:
            self.arraydata[0] = row
        else:
            self.arraydata.append(row)
        self.layoutChanged.emit()

    def update_row(self, idx, row):
        self.arraydata[idx] = row
        self.layoutChanged.emit()

    def remove_row(self, row_i):
        if len(self.arraydata) < 2:
            print(default_row)
            self.arraydata = default_row.copy()
        else:
            self.arraydata.pop(row_i)
        self.layoutChanged.emit()

    def insert_row(self, row_i, row):
        self.arraydata.insert(row_i, row)
        self.layoutChanged.emit()

    def move_trial_up(self, idx):
        try:
            if idx > 0:
                self.arraydata[idx], self.arraydata[idx-1] = self.arraydata[idx-1], self.arraydata[idx]
        except:
            pass
        self.layoutChanged.emit()

    def move_trial_down(self, idx):
        try:
            if idx < len(self.arraydata):
                self.arraydata[idx], self.arraydata[idx + 1] = self.arraydata[idx + 1], self.arraydata[idx]
        except:
            pass
        self.layoutChanged.emit()

    def append_valve(self, row, valve_params):
        self.arraydata[row][0] += 1
        self.arraydata[row][1].append(valve_params)
        self.layoutChanged.emit()

    def load_arraydata(self, file_conf):
        try:
            with open(file_conf, 'rb') as fn:
                arraydata = pickle.load(fn)

            self.arraydata = arraydata
            self.layoutChanged.emit()
        except:
            print('LOAD FAILED')
            pass

    def save_arraydata(self, file_conf):
        try:
            with open(file_conf[0] + file_conf[1], 'wb') as fn:
                pickle.dump(self.arraydata, fn)
        except:
            print("save failed")
            pass

    def advance_trial(self):
        self.current_trial += 1

    def reset_trials(self):
        self.current_trial = 0

    def total_trials(self):
        return len(self.arraydata)

    def randomise_trials(self):
        random.shuffle(self.arraydata)
