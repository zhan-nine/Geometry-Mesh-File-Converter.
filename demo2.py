from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QTextEdit, QListWidget, QListWidgetItem, QHBoxLayout, QWidget, QMenuBar
from PyQt5.QtWidgets import QComboBox, QLabel, QVBoxLayout, QPushButton, QSizePolicy
import Translator.py
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
        #把下面的控件垂直排列
        vbox1 = QVBoxLayout()
        self.layout().addLayout(vbox1)
        self.output_button = QPushButton("导出")

        self.label_output_format = QLabel("输出文件格式:")
        self.combobox_output_format = QComboBox()
        self.combobox_output_format.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.combobox_output_format.currentTextChanged.connect(self.ChooseOutputFormat)
        vbox1.addWidget(self.label_output_format)
        #加入一个combobox
        vbox1.addWidget(self.combobox_output_format)
        vbox1.addWidget(self.output_button)
        self.output_button.setEnabled(False)
        vbox1.addStretch(2)
        
    def ChooseOutputFormat(self):
        self.parent().status.showMessage("Output Format: "+self.combobox_output_format.currentText())

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
        # 状态栏输出文件名
        self.parent().status.showMessage("Choose: "+item.text())
        with open(item.text(), "r") as f:
            file_data = f.readlines()
        self.text_edit.clear()
        self.text_edit.setPlainText("".join(file_data))
        # for line in file_data:
        #     self.text_edit.append(line)

class MyMainWindow(QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.initMenu()
        self.initUI()
        

    def initUI(self):
        self.setWindowTitle("格式转换器")
        self.resize(1920, 1080)
        self.InputType = ""
        self.central = MyCentralWidget(self)
        self.setCentralWidget(self.central)

    def initMenu(self):
        self.menu = self.menuBar()
        self.status = self.statusBar()
        self.status.showMessage('Ready')

        self.file_menu = self.menu.addMenu("文件")
        self.file_menu_open = self.file_menu.addMenu("打开")

        self.file_menu_export = self.file_menu.addAction("导出地址")
        self.file_menu_export.triggered.connect(self.export_file)

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
            self.status.showMessage('Geometry file loaded')
            self.InputType="Geometry"
            self.ChangeComboBox()

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
            self.status.showMessage('Mesh file loaded')
            self.InputType="Mesh"
            self.ChangeComboBox()

    def export_file(self):
        folder_path = QFileDialog.getExistingDirectory(self, '选择文件夹', '/')
        if folder_path:
            self.status.showMessage('Export to: ' + folder_path)

    def ChangeComboBox(self):
        self.central.combobox_output_format.clear()
        if(self.InputType=="Geometry"):
            # "Geometry - Gmsh GEO (*.geo);;" + 
            # "Geometry - OpenCASCADE BREP (*.brep);;" + 
            # "Geometry - OpenCASCADE XAO (*.xao);;" + 
            # "Geometry - STEP (*.stp *.step);;" + 
            # "Geometry - IGES (*.igs *.iges)"
            self.central.combobox_output_format.addItem("Gmsh GEO (*.geo)")
            self.central.combobox_output_format.addItem("OpenCASCADE BREP (*.brep)")
            self.central.combobox_output_format.addItem("OpenCASCADE XAO (*.xao)")
            self.central.combobox_output_format.addItem("STEP (*.stp *.step)")
            self.central.combobox_output_format.addItem("IGES (*.igs *.iges)")
        elif(self.InputType=="Mesh"):
            # "Mesh - Gmsh MSH (*.msh);;" +
            # "Mesh - Diffpack 3D (*.diff);;" +
            # "Mesh - I-deas Universal (*.unv);;" +
            # "Mesh - MED (*.med *.mmed);;" +
            # "Mesh - Inria Medit (*.mesh);;" +
            # "Mesh - Nastran Bulk Data File (*.bdf *.nas);;" +
            # "Mesh - Gambit Neutral (*.neu);;" +
            # "Mesh - Object File Format (*.off);;" +
            # "Mesh - Plot3D Structured Mesh (*.p3d);;" +
            # "Mesh - STL Surface(*.stl);;" +
            # "Mesh - VTK (*.vtk);;" +
            # "Mesh - VRML Surface (*.wrl *vrml);;" +
            # "Mesh - PLY2 (*.ply)"
            self.central.combobox_output_format.addItem("Gmsh MSH (*.msh)")
            self.central.combobox_output_format.addItem("Diffpack 3D (*.diff)")
            self.central.combobox_output_format.addItem("I-deas Universal (*.unv)")
            self.central.combobox_output_format.addItem("MED (*.med *.mmed)")
            self.central.combobox_output_format.addItem("Inria Medit (*.mesh)")
            self.central.combobox_output_format.addItem("Nastran Bulk Data File (*.bdf *.nas)")
            self.central.combobox_output_format.addItem("Gambit Neutral (*.neu)")
            self.central.combobox_output_format.addItem("Object File Format (*.off)")
            self.central.combobox_output_format.addItem("Plot3D Structured Mesh (*.p3d)")
            self.central.combobox_output_format.addItem("STL Surface(*.stl)")
            self.central.combobox_output_format.addItem("VTK (*.vtk)")
            self.central.combobox_output_format.addItem("VRML Surface (*.wrl *vrml)")
            self.central.combobox_output_format.addItem("PLY2 (*.ply)")
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()

    sys.exit(app.exec_())