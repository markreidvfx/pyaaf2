from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

import sys
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

import io
import random
import binascii
import aaf2
from aaf2.cfb import CompoundFileBinary


class TreeItem(object):
    def __init__(self, item, metadict=None, parent=None, index = 0):
        self.parentItem = parent
        self.item = item

        self.children = {}
        self.children_count = 0
        self.properties = {}
        self.loaded = False
        self.index = index
        self.metadict = metadict

    def columnCount(self):
        return 1

    def childCount(self):
        self.setup()
        return self.children_count

    def child(self,row):
        self.setup()
        if row in self.children:
            return self.children[row]

        return None

    def childNumber(self):
        self.setup()
        return self.index

    def parent(self):
        self.setup()
        return self.parentItem

    def extend(self, items):
        for i in items:
            index = self.children_count
            t = TreeItem(i, self.metadict, self, index)

            self.children[index] = t
            self.children_count += 1

    def name(self):
        return self.item.name

    def class_name(self):
        class_id = self.item.class_id
        if not class_id:
            return ""

        if self.metadict:
            classdef = self.metadict.lookup_classdef(class_id)
            if classdef:
                name = classdef.class_name
                if name:
                    return name
        return ""

    def setup(self):
        if self.loaded:
            return

        item = self.item

        if item.isdir():
            dirs = []
            streams = []
            for d in item.listdir():
                if d.isdir():
                    dirs.append(d)
                else:
                    streams.append(d)

            self.extend(sorted(dirs, key=lambda entry: entry.name))
            self.extend(sorted(streams, key=lambda entry: entry.name))

        self.properties['Name'] = self.name()
        self.properties['Class'] = self.class_name()
        self.properties['Class ID'] = str(item.class_id or "")
        self.properties['Type'] = "Directory" if item.isdir() else "Stream"
        self.properties['Color'] = item.color
        self.properties['Modified'] = str(item.modify_time)
        self.properties['Created'] = str(item.create_time)
        self.properties['Byte Size'] = item.byte_size
        self.properties['Path'] = item.path()

        if item.isfile() and item.sector_id is not None:
            self.properties["Sector ID"] = item.sector_id
            is_mini = item.byte_size < item.storage.min_stream_max_size
            self.properties['Stream Type'] = "MiniFat" if is_mini else "Fat"

            chain = item.storage.get_fat_chain(item.sector_id, is_mini)
            self.properties["Chain"] = ",".join([str(i) for i in chain])

        self.loaded = True


class CFBModel(QtCore.QAbstractItemModel):
    def __init__(self, root, metadict=None, parent=None):
        super(CFBModel,self).__init__(parent)

        self.rootItem = TreeItem(root, metadict)
        self.headers = ['Name', 'Type', 'Class', 'Class ID', 'Byte Size',"Stream Type", 'Chain',  "Path"]

    def headerData(self, column, orientation,role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.headers[column]
        return None

    def columnCount(self,index):
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


def display_data(data, name):
    w = QtWidgets.QTextEdit()

    font = QtGui.QFontDatabase.systemFont(QtGui.QFontDatabase.FixedFont)
    if font:
        w.setFont(font)
    w.setFontPointSize(12)
    w.setWindowTitle(name)
    w.resize(800, 800)

    if isinstance(data, list):
        w.setText(str(data))
    else:
        text = binascii.hexlify(data).decode("utf-8")
        n = 32
        chunks = [text[i:i+n] for i in range(0, len(text), n)]
        w.setText("\n".join(chunks))

    w.show()
    return w


class CFBTree(QtWidgets.QTreeView):
    def __init__(self, options, tabs, fat, minifat):
        super(CFBTree, self).__init__()

        self.options = options
        self.tabs = tabs
        self.fat = fat
        self.minifat = minifat

        self.resize(700,600)
        self.setAlternatingRowColors(True)
        self.setUniformRowHeights(True)

        self.clicked.connect(self.item_clicked)
        self.doubleClicked.connect(self.item_double_clicked)
        self.text_edits = {}

    def setFilePath(self, path):
        try:
            self.f = aaf2.open(file_path)
            self.cfb = self.f.cfb
            root = self.f.cfb.root
            model = CFBModel(root, self.f.metadict)
        except:
            print("unable to read as aaf, trying raw CFB")
            self.f = io.open(path, 'rb')
            self.cfb = CompoundFileBinary(self.f)
            model = CFBModel(self.cfb.root, None)

        self.setModel(model)
        # self.expandToDepth(1)
        self.resizeColumnToContents(0)
        self.resizeColumnToContents(1)
        self.resizeColumnToContents(2)
        self.resizeColumnToContents(3)

    def item_clicked(self, index):
        tree_item = index.internalPointer()
        if not tree_item:
            return
        if not tree_item.item:
            return

        item = tree_item.item
        if item.isfile():
            f = item.open()
            if f.is_mini_stream():
                self.minifat.set_selected(f.fat_chain, True)
                self.tabs.setCurrentIndex(1)
            else:
                self.fat.set_selected(f.fat_chain, True)
                self.tabs.setCurrentIndex(0)

    def item_double_clicked(self, index):
        tree_item = index.internalPointer()
        if not tree_item:
            return
        if not tree_item.item:
            return

        item = tree_item.item
        if item.isfile():
            path = item.path()
            if path in self.text_edits:
                self.text_edits[path].show()
                self.text_edits[path].setWindowState(QtCore.Qt.WindowActive)
                return

            f = item.open()
            data = f.read()
            self.text_edits[path] = display_data(data, path)


def get_fat_chains(cfb, minifat=False):
    chains = {}
    seen = set()
    fat = cfb.fat
    if minifat:
        fat = cfb.minifat

    for i,v in enumerate(fat):
        if v in (aaf2.cfb.DIFSECT, aaf2.cfb.FATSECT, aaf2.cfb.FREESECT):
            continue

        # if the sid has been seen it is in a existing chain
        if i in seen:
            continue

        chain = cfb.get_fat_chain(i, minifat)

        # remove all chains that start with any values in chain
        for v in chain:
            chains.pop(v, None)
            seen.add(v)
        chains[i] = chain

    result = {}
    random.seed(0)
    for start, chain in chains.items():
        color = QtGui.QColor(random.randint(0, 255),
                             random.randint(0, 255),
                             random.randint(0, 255), 128)
        for i,v in enumerate(chain):
            c = color
            # a = (i+1) / float(len(chain))
            # a = a * 0.5 + .25
            # c =  QtGui.QColor(color)
            # c.setAlphaF(a)
            result[v] = (c, chain)

    return result


class FatViewer(QtWidgets.QTableWidget):
    def __init__(self):
        super(FatViewer, self).__init__()
        self.fat_col_count = 16
        self.chains = {}
        self.minifat = False
        self.cfb = None
        self.text_edits = {}
        self.verticalHeader().hide()
        self.horizontalHeader().hide()

        self.setColumnCount(self.fat_col_count)
        for i in range(self.fat_col_count):
            self.setColumnWidth(i, 48)
            w = QtWidgets.QTableWidgetItem()
            w.setText(str(i))
            self.setHorizontalHeaderItem(i, w)

        self.cellDoubleClicked.connect(self.double_click)

        # adjust style sheet so unfocused selection is visible
        self.setStyleSheet('QTableView:item:selected {background-color: rgb(45,157,255); color: rgb(255,255,255)}')

    def set_cfb(self, cfb, minifat=False):
        self.minifat = minifat
        self.cfb = cfb
        fat = cfb.fat
        if minifat:
            fat = cfb.minifat

        self.setRowCount((len(fat) + self.fat_col_count-1) // self.fat_col_count)
        self.chains = get_fat_chains(cfb, minifat)

        for i, v in enumerate(fat):
            row, col = divmod(i, self.fat_col_count)
            w = QtWidgets.QTableWidgetItem()
            w.setFlags(w.flags() ^ QtCore.Qt.ItemIsEditable)
            w.setToolTip(str(i))

            if v == aaf2.cfb.FREESECT:
                w.setBackground(QtGui.QBrush(QtGui.QColor(0, 255, 0, 25)))
                w.setText("free")
            elif v == aaf2.cfb.FATSECT:
                w.setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 0, 25)))
                w.setText("fat")
            elif v == aaf2.cfb.DIFSECT:
                w.setBackground(QtGui.QBrush(QtGui.QColor(0, 255, 255, 25)))
                w.setText("difat")
            else:
                color, chain = self.chains.get(i, [QtGui.QColor(0, 0, 255, 255), []])
                w.setBackground(QtGui.QBrush(color))
                if v == aaf2.cfb.ENDOFCHAIN:
                    w.setText('end')
                else:
                    w.setText(str(v))

            self.setItem(row, col, w)

    def set_cfb_difat(self, cfb):
        difat = []
        for t, i, sid in cfb.iter_difat():
            difat.append(sid)

        self.setRowCount((len(difat) + self.fat_col_count - 1)  // self.fat_col_count)

        for i, v in enumerate(difat):
            row, col = divmod(i, self.fat_col_count)
            w = QtWidgets.QTableWidgetItem()
            w.setFlags(w.flags() ^ QtCore.Qt.ItemIsEditable)
            w.setToolTip(str(i))

            if v == aaf2.cfb.FREESECT:
                w.setBackground(QtGui.QBrush(QtGui.QColor(0, 255, 0, 25)))
                w.setText("free")
            else:
                w.setText(str(v))

            self.setItem(row, col, w)

    def double_click(self, row, col):
        index = (row * self.fat_col_count) + col
        chain = self.chains.get(index, None)
        if chain is None:
            return
        self.set_selected(chain[1])

    def set_selected(self, chain, scroll_to=False):
        self.clearSelection()
        for sid in chain:
            row, col = divmod(sid, self.fat_col_count)
            w = self.item(row, col)
            w.setSelected(True)
            if scroll_to:
                self.scrollToItem(w)
                scroll_to = False

    def read_minifat_sector(self, sid):
        s = aaf2.cfb.Stream(self.cfb, self.cfb.root, 'r')
        offset = sid * 64
        s.seek(offset)
        data = s.read(64)
        return data

    def show_chain(self, index):
        chain = self.chains.get(index, None)
        if chain and chain[1]:
            key = "fat chain: {}".format(chain[1][0])
            self.text_edits[key] = display_data(chain[1], key)

    def extract_sector(self, sid):
        key = "sector : {}".format(sid)
        if key in self.text_edits:
            self.text_edits[key].show()
            self.text_edits[key].setWindowState(QtCore.Qt.WindowActive)
            return

        f = io.BytesIO()
        if self.minifat:
            sector_data = self.read_minifat_sector(sid)
        else:
            sector_data = self.cfb.read_sector_data(sid)
        f.write(sector_data)

        self.text_edits[key] = display_data(f.getvalue(), key)

    def extract_chain(self, index):
        chain = self.chains.get(index, None)
        if not chain:
            return

        key = "chain : {}".format(chain[1][0])
        if key in self.text_edits:
            self.text_edits[key].show()
            self.text_edits[key].setWindowState(QtCore.Qt.WindowActive)
            return

        if chain:
            f = io.BytesIO()
            for sid in chain[1]:
                if self.minifat:
                    sector_data = self.read_minifat_sector(sid)
                else:
                    sector_data = self.cfb.read_sector_data(sid)
                f.write(sector_data)
            self.text_edits[key] = display_data(f.getvalue(), key)

    def contextMenuEvent(self, event):
        if not self.cfb:
            return

        row = self.rowAt(event.pos().y())
        col = self.columnAt(event.pos().x())
        index = (row * self.fat_col_count) + col

        self.menu = QtWidgets.QMenu(self)
        action = QtWidgets.QAction('Extract Chain Containing: %d' % index, self)
        action.triggered.connect(lambda: self.extract_chain(index))
        self.menu.addAction(action)

        action = QtWidgets.QAction('Show Chain Containing: %d' % index, self)
        action.triggered.connect(lambda: self.show_chain(index))
        self.menu.addAction(action)

        action = QtWidgets.QAction('Extract Sector: %d' % index, self)
        action.triggered.connect(lambda: self.extract_sector(index))
        self.menu.addAction(action)

        self.menu.popup(QtGui.QCursor.pos())


class Window(QtWidgets.QWidget):
    def __init__(self, options):
        super(Window, self).__init__()
        tabs = QtWidgets.QTabWidget()
        self.fat = FatViewer()
        self.minifat = FatViewer()
        self.difat = FatViewer()
        self.cfb_tree = CFBTree(options, tabs, self.fat, self.minifat)

        label_names = ["magic",
                       "class_id",
                       "minor_version",
                       "major_version",
                       "byte_order",
                       "sector_size",
                       "mini_stream_sector_size",
                       "dir_sector_count",
                       "fat_sector_count",
                       "dir_sector_start",
                       "transaction_signature",
                       "min_stream_max_size",
                       "minifat_sector_start",
                       "minifat_sector_count",
                       "difat_sector_start",
                       "difat_sector_count",
                       "ministream_sector_start",
                       "ministream_sector_size"
                       ]

        self.labels = {}
        forum = QtWidgets.QFormLayout()

        for l in label_names:
            label = QtWidgets.QLabel("")
            label.setTextInteractionFlags(QtGui.Qt.TextSelectableByMouse)
            forum.addRow(l, label)
            self.labels[l] = label

        tabs.addTab(self.fat, "Fat")
        tabs.addTab(self.minifat, "Mini Fat")
        tabs.addTab(self.difat, "DiFat")

        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addLayout(forum)
        h_layout.addWidget(tabs)
        top_widget = QtWidgets.QWidget()
        top_widget.setLayout(h_layout)

        splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        splitter.addWidget(top_widget)
        splitter.addWidget(self.cfb_tree)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(splitter)

        self.setLayout(layout)

    def setFilePath(self, path):
        self.cfb_tree.setFilePath(path)
        cfb = self.cfb_tree.cfb
        for name, label in self.labels.items():
            value = ""
            if name == "ministream_sector_start":
                value = cfb.root.sector_id
            elif name == "ministream_sector_size":
                value = cfb.root.byte_size
            else:
                if hasattr(cfb, name):
                    value = getattr(cfb, name)

            label.setText(": {}".format(value))

        self.fat.set_cfb(cfb, False)
        self.minifat.set_cfb(cfb, True)
        self.difat.set_cfb_difat(cfb)

        self.setWindowTitle(path)


if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()

    (options, args) = parser.parse_args()

    if not args:
        parser.error("not enough arguments")

    file_path = args[0]

    app = QtWidgets.QApplication(sys.argv)
    window = Window(options)
    window.setFilePath(file_path)
    window.resize(2000, 1400)
    window.show()

    sys.exit(app.exec_())
