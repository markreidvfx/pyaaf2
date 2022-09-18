from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
import sys
from PySide2 import QtCore
from PySide2 import QtWidgets

import aaf2

class TreeItem(object):

    def __init__(self, item, parent=None, index = 0):
        self.parentItem = parent
        self.item = item
        self.children = {}
        self.children_count = 0
        self.properties = {}
        self.loaded = False
        self.index = index
        self.references = []
        #self.getData()
    def columnCount(self):
        return 1

    def childCount(self):
        self.setup()
        return self.children_count

    def child(self,row):
        self.setup()
        if row in self.children:
            return self.children[row]

        if isinstance(self.item, aaf2.properties.StrongRefSetProperty):
            key = self.references[row]
            item = self.item.get(key)
            t = TreeItem(item ,self, row)

        elif isinstance(self.item, aaf2.properties.StrongRefVectorProperty):
            item = self.item.get(row)
            t = TreeItem(item ,self, row)
        else:
            return None
        print(row, item)
        self.children[row] = t
        return t

    def childNumber(self):
        self.setup()
        return self.index

    def parent(self):
        self.setup()
        return self.parentItem

    def extend(self, items):
        for i in items:
            index = self.children_count
            t = TreeItem(i,self, index)

            self.children[index] = t
            self.children_count += 1

    def name(self):
        item = self.item
        if hasattr(item, 'name'):
            name = item.name
            if name:
                return name
        return self.class_name()

    def class_name(self):
        item = self.item
        if isinstance(item, aaf2.core.AAFObject):
            return item.classdef.class_name

        if hasattr(item,"class_name"):
            return item.class_name
        else:
            return item.__class__.__name__

    def setup(self):
        if self.loaded:
            return

        item = self.item
        if isinstance(item, list):
            self.extend(item)

        if isinstance(item, aaf2.core.AAFObject):
            self.extend(list(item.properties()))

        elif isinstance(item, aaf2.properties.StrongRefProperty):
            self.extend([item.value])

        elif isinstance(item, aaf2.properties.StrongRefVectorProperty):
            self.children_count = len(item)

        elif isinstance(item, aaf2.properties.StrongRefSetProperty):
            self.children_count = len(item)
            self.references = list(item.references.keys())
            self.references.sort()

        elif isinstance(item, (aaf2.properties.Property)):
            try:
                v = str(item.value)
            except:
                v = "Error"

            self.properties['Value'] = v

        # add slot and mob references as children for convenience
        if isinstance(item, aaf2.components.SourceClip):
            mob = item.mob
            if mob:
                self.extend([mob])
            slot = item.slot
            if slot:
                self.extend([slot])


        self.properties['Name'] = self.name()
        self.properties['Class'] = self.class_name()

        self.loaded = True

class AAFModel(QtCore.QAbstractItemModel):

    def __init__(self, root ,parent=None):
        super(AAFModel,self).__init__(parent)

        self.rootItem = TreeItem(root)

        self.headers = ['Name', 'Value', 'Class']

    def headerData(self, column, orientation,role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.headers[column]
        return None

    def columnCount(self,index):
        #item = self.getItem(index)

        return len(self.headers)

    def rowCount(self,parent=QtCore.QModelIndex()):
        parentItem = self.getItem(parent)
        return parentItem.childCount()

    def data(self, index, role):

        if not index.isValid():
            return 0

        if role != QtCore.Qt.DisplayRole:
            return None

        item = self.getItem(index)

        header_key = self.headers[index.column()]

        return str(item.properties.get(header_key,''))

    def parent(self, index):

        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = self.getItem(index)
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.childNumber(), 0, parentItem)

    def index(self, row, column, parent = QtCore.QModelIndex()):
        if parent.isValid() and parent.column() != 0:
            return QtCore.QModelIndex()

        item = self.getItem(parent)
        childItem = item.child(row)

        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()


    def getItem(self,index):

        if index.isValid():
            item = index.internalPointer()
            if item:
                return item
        return self.rootItem

class Window(QtWidgets.QTreeView):
    def __init__(self, options):
        super(Window, self).__init__()

        self.options = options

        self.resize(700,600)
        self.setAlternatingRowColors(True)
        self.setUniformRowHeights(True)

    def setFilePath(self, path):
        print(path)
        f = aaf2.open(file_path)

        root = f.content
        if options.toplevel:
            root = list(f.content.toplevel())
        if options.compmobs:
            root = list(f.content.compositionmobs())

        if options.mastermobs:
            root = list(f.content.mastermobs())

        if options.sourcemobs:
           root = list(f.content.GetSourceMobs())

        if options.dictionary:
            root = f.dictionary

        if options.metadict:
            root = f.metadict

        if options.root:
            root = f.root

        model = AAFModel(root)

        self.setModel(model)

        self.setWindowTitle(file_path)
        self.expandToDepth(1)
        self.resizeColumnToContents(0)
        self.resizeColumnToContents(1)

if __name__ == "__main__":

    from PySide2 import QtWidgets
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option('-t','--toplevel',action="store_true", default=False)
    parser.add_option('-c','--compmobs',action="store_true", default=False)
    parser.add_option('-m','--mastermobs',action="store_true", default=False)
    parser.add_option('-s','--sourcemobs',action="store_true", default=False)
    parser.add_option('-d','--dictionary',action="store_true", default=False)
    parser.add_option('--metadict',action="store_true", default=False)
    parser.add_option('-r','--root',action="store_true", default=False)

    (options, args) = parser.parse_args()

    if not args:
        parser.error("not enough arguments")

    file_path = args[0]

    app = QtWidgets.QApplication(sys.argv)

    tree = QtWidgets.QTreeView()

    window = Window(options)

    window.setFilePath(file_path)

    window.show()

    fs_watcher = QtCore.QFileSystemWatcher([file_path])
    fs_watcher.fileChanged.connect(window.setFilePath)

    sys.exit(app.exec_())
