from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QTextEdit, QListWidget, QListWidgetItem, QHBoxLayout, QWidget, QMenuBar
from PyQt5.QtWidgets import QComboBox

import sys

class MyClass(object):
    def __init__(self):
        pass

    def load_mesh(self, file_path):
        print("load_mesh", file_path)
        pass

    def export_mesh(self, file_path, file_type):
        print("export_mesh", file_path)
        pass


class MyCentralWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(QHBoxLayout())
        self.list_widget = QListWidget()
        self.text_edit = QTextEdit()
        self.layout().addWidget(self.list_widget)
        self.layout().addWidget(self.text_edit)
        self.text_edit.setReadOnly(True)
        self.list_widget.itemClicked.connect(self.item_clicked)
        self.layout().setStretchFactor(self.list_widget, 1)
        self.layout().setStretchFactor(self.text_edit, 3)
        #加入一个combobox
        self.layout().addWidget(QComboBox())

    def load_data(self, file_paths):  # 参数名改为 file_paths 以反映它是一个列表
        #清空文本框
        self.text_edit.clear()
        #清空列表
        self.list_widget.clear()
        if(not file_paths):
            return
        for file_path in file_paths:  # 遍历列表中的每个文件路径
            # 清空文本编辑器应该在循环外部进行，以保留所有文件的内容

            # 为每个文件创建一个 QListWidgetItem 并添加到列表中
            item = QListWidgetItem(file_path)
            self.list_widget.addItem(item)
    def item_clicked(self, item):

        with open(item.text(), "r") as f:
            file_data = f.readlines()
        self.text_edit.clear()
        self.text_edit.setPlainText("".join(file_data))
        for line in file_data:
            self.text_edit.append(line)

class MyMainWindow(QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.initUI()
        self.initMenu()

    def initUI(self):
        self.setWindowTitle("MyMainWindow")
        self.resize(1920, 1080)

        self.central = MyCentralWidget(self)
        self.setCentralWidget(self.central)

    def initMenu(self):
        self.menu = self.menuBar()
        self.status = self.statusBar()

        self.file_menu = self.menu.addMenu("文件")
        self.file_menu_open = self.file_menu.addMenu("打开")

        self.open_geometry = QAction("几何文件", self)
        self.open_geometry.triggered.connect(self.open_file_geometry)
        self.file_menu_open.addAction(self.open_geometry)

        self.open_mesh = QAction("网格文件", self)
        self.open_mesh.triggered.connect(self.open_file_mesh)
        self.file_menu_open.addAction(self.open_mesh)

        self.exit_action = QAction("退出", self)
        self.exit_action.triggered.connect(self.close)
        self.file_menu.addAction(self.exit_action)
        


    def open_file_geometry(self):
        file_path, _ = QFileDialog.getOpenFileNames(
            self, "Open File", "", 
            "All Files (*.*);;" +
            "Geometry - Gmsh GEO (*.geo);;" + 
            "Geometry - OpenCASCADE BREP (*.brep);;" + 
            "Geometry - OpenCASCADE XAO (*.xao);;" + 
            "Geometry - STEP (*.stp *.step);;" + 
            "Geometry - IGES (*.igs *.iges)"
        )
        if file_path:
            self.central.load_data(file_path)

    def open_file_mesh(self):
        file_path, _ = QFileDialog.getOpenFileNames(
            self, "Open File", "", 
            "All Files (*.*);;" +
            "Mesh - Gmsh MSH (*.msh);;" +
            "Mesh - Diffpack 3D (*.diff);;" +
            "Mesh - I-deas Universal (*.unv);;" +
            "Mesh - MED (*.med *.mmed);;" +
            "Mesh - Inria Medit (*.mesh);;" +
            "Mesh - Nastran Bulk Data File (*.bdf *.nas);;" +
            "Mesh - Gambit Neutral (*.neu);;" +
            "Mesh - Object File Format (*.off);;" +
            "Mesh - Plot3D Structured Mesh (*.p3d);;" +
            "Mesh - STL Surface(*.stl);;" +
            "Mesh - VTK (*.vtk);;" +
            "Mesh - VRML Surface (*.wrl *vrml);;" +
            "Mesh - PLY2 (*.ply)"
        )
        if file_path:
            self.central.load_data(file_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()

    sys.exit(app.exec_())