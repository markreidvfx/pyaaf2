import sys
from PyQt4 import QtCore

import aaf2

class TreeItem(object):

    def __init__(self, item, parent=None):
        self.parentItem = parent
        self.item = item
        self.childItems = []
        self.properties = {}
        self.loaded = False
        #self.getData()
    def columnCount(self):
        return 1

    def childCount(self):
        self.setup()
        return len(self.childItems)

    def child(self,row):
        self.setup()
        return self.childItems[row]

    def childNumber(self):
        self.setup()
        if self.parentItem != None:
            return self.parentItem.childItems.index(self)
        return 0

    def parent(self):
        self.setup()
        return self.parentItem

    def extendChildItems(self, items):
        for i in items:
            t = TreeItem(i,self)
            self.childItems.append(t)

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
            self.extendChildItems(item)

        if isinstance(item, aaf2.core.AAFObject):
            self.extendChildItems(list(item.properties()))

        elif isinstance(item, aaf2.properties.StrongRefProperty):
            self.extendChildItems([item.value])

        elif isinstance(item, (aaf2.properties.StrongRefSetProperty,
                               aaf2.properties.StrongRefVectorProperty)):
            self.extendChildItems(list(item))

        elif isinstance(item, (aaf2.properties.Property)):
            self.properties['Value'] = str(item.value)


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
            return QtCore.QVariant(self.headers[column])
        return QtCore.QVariant()

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


if __name__ == "__main__":

    from PyQt4 import QtGui
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

    app = QtGui.QApplication(sys.argv)

    model = AAFModel(root)

    tree = QtGui.QTreeView()

    tree.setModel(model)

    tree.resize(700,600)
    tree.expandToDepth(1)
    tree.resizeColumnToContents(0)
    tree.resizeColumnToContents(1)
    tree.show()

    sys.exit(app.exec_())
