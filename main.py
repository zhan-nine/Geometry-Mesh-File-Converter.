from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QAction,
    QFileDialog,
    QTextEdit,
    QListWidget,
    QListWidgetItem,
    QHBoxLayout,
    QWidget,
    QMenuBar,
)
from PyQt5.QtWidgets import (
    QComboBox,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QSizePolicy,
    QStatusBar,
    QMessageBox,
)
import Translator
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
        # 把下面的控件垂直排列
        vbox1 = QVBoxLayout()
        self.layout().addLayout(vbox1)
        self.output_button = QPushButton("导出")

        self.label_output_format = QLabel("输出文件格式:")
        self.combobox_output_format = QComboBox()
        self.combobox_output_format.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.combobox_output_format.currentTextChanged.connect(self.ChooseOutputFormat)
        vbox1.addWidget(self.label_output_format)
        # 加入一个combobox
        vbox1.addWidget(self.combobox_output_format)
        vbox1.addWidget(self.output_button)
        # 其他条件设置良好之前，导出按钮不可用
        self.output_button.setEnabled(False)
        self.output_button.clicked.connect(self.ExportFile)
        vbox1.addStretch(2)

    def ChooseOutputFormat(self):
        self.parent().status.showMessage(
            "Output Format: " + self.combobox_output_format.currentText()
        )

    def load_data(self, file_paths):  # 参数名改为 file_paths 以反映它是一个列表
        # 清空文本框
        self.text_edit.clear()
        # 清空列表
        self.list_widget.clear()
        if not file_paths:
            return
        self.input_file_paths = file_paths
        for file_path in file_paths:  # 遍历列表中的每个文件路径
            # 清空文本编辑器应该在循环外部进行，以保留所有文件的内容

            # 为每个文件创建一个 QListWidgetItem 并添加到列表中
            item = QListWidgetItem(file_path)
            self.list_widget.addItem(item)

    def item_clicked(self, item):
        # 状态栏输出文件名
        self.parent().status.showMessage("Choose: " + item.text())
        with open(item.text(), "r") as f:
            file_data = f.readlines()
        self.text_edit.clear()
        self.text_edit.setPlainText("".join(file_data))
        # for line in file_data:
        #     self.text_edit.append(line)

    def ExportFile(self):
        file_paths = self.input_file_paths
        print(file_paths)
        output_format = self.combobox_output_format.currentText()
        output_path = self.parent().folder_path
        if self.parent().InputType == "Geometry":
            Translator.MyTranslator.Trans_Geometry(
                file_paths, output_path, output_format
            )
        elif self.parent().InputType == "Mesh":
            Translator.MyTranslator.Trans_Mesh(file_paths, output_path, output_format)

    def Show_Button(self):
        print("Show_Button")
        try:
            if self.input_file_paths and self.parent().folder_path:
                self.output_button.setEnabled(True)
        except:
            self.output_button.setEnabled(False)


class MyMainWindow(QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.initMenu()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("格式转换器")
        self.resize(1920, 1080)
        self.InputType = ""
        self.setCentralWidget(self.central)

    def initMenu(self):
        self.menu = self.menuBar()
        self.status = self.statusBar()
        self.central = MyCentralWidget(self)

        self.status.showMessage("Ready")

        self.file_menu = self.menu.addMenu("文件")
        self.file_menu_open = self.file_menu.addMenu("打开")

        self.file_menu_export = self.file_menu.addAction("导出地址")
        self.file_menu_export.triggered.connect(self.export_file)
        self.file_menu_export.triggered.connect(self.central.Show_Button)

        self.open_geometry = QAction("几何文件", self)
        self.open_geometry.triggered.connect(self.open_file_geometry)
        self.open_geometry.triggered.connect(self.central.Show_Button)
        self.file_menu_open.addAction(self.open_geometry)

        self.open_mesh = QAction("网格文件", self)
        self.open_mesh.triggered.connect(self.open_file_mesh)
        self.open_mesh.triggered.connect(self.central.Show_Button)
        self.file_menu_open.addAction(self.open_mesh)

        self.exit_action = QAction("退出", self)
        self.exit_action.triggered.connect(self.close)
        self.file_menu.addAction(self.exit_action)

        self.introduction = QAction("关于", self)
        self.menu.addAction(self.introduction)
        self.introduction.triggered.connect(self.Show_Introduction)

    def open_file_geometry(self):
        file_path, _ = QFileDialog.getOpenFileNames(
            self,
            "Open File",
            "",
            "All Files (*.*);;"
            + "Geometry - Gmsh GEO (*.geo);;"
            + "Geometry - OpenCASCADE BREP (*.brep);;"
            + "Geometry - OpenCASCADE XAO (*.xao);;"
            + "Geometry - STEP (*.stp *.step);;"
            + "Geometry - IGES (*.igs *.iges)",
        )
        if file_path:
            self.central.load_data(file_path)
            self.status.showMessage("Geometry file loaded")
            self.InputType = "Geometry"
            self.ChangeComboBox()

    def open_file_mesh(self):
        file_path, _ = QFileDialog.getOpenFileNames(
            self,
            "Open File",
            "",
            "All Files (*.*);;"
            + "Mesh - Gmsh MSH (*.msh);;"
            + "Mesh - Diffpack 3D (*.diff);;"
            + "Mesh - I-deas Universal (*.unv);;"
            + "Mesh - MED (*.med *.mmed);;"
            + "Mesh - Inria Medit (*.mesh);;"
            + "Mesh - Nastran Bulk Data File (*.bdf *.nas);;"
            + "Mesh - Gambit Neutral (*.neu);;"
            + "Mesh - Object File Format (*.off);;"
            + "Mesh - Plot3D Structured Mesh (*.p3d);;"
            + "Mesh - STL Surface(*.stl);;"
            + "Mesh - VTK (*.vtk);;"
            + "Mesh - VRML Surface (*.wrl *vrml);;"
            + "Mesh - PLY2 (*.ply)",
        )
        if file_path:
            self.central.load_data(file_path)
            self.status.showMessage("Mesh file loaded")
            self.InputType = "Mesh"
            self.ChangeComboBox()

    def export_file(self):
        self.folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹", "/")
        if self.folder_path:
            self.status.showMessage("Export to: " + self.folder_path)

    def ChangeComboBox(self):
        self.central.combobox_output_format.clear()
        if self.InputType == "Geometry":
            self.central.combobox_output_format.addItem("Gmsh Options (*.opt)")
            self.central.combobox_output_format.addItem(
                "Gmsh Unrolled GEO (*.geo_unrolled)"
            )
            self.central.combobox_output_format.addItem("OpenCASCADE BREP (*.brep)")
            self.central.combobox_output_format.addItem("OpenCASCADE XAO (*.xao)")
            self.central.combobox_output_format.addItem("STEP (*.step)")
            self.central.combobox_output_format.addItem("IGES (*.iges)")
        elif self.InputType == "Mesh":
            self.central.combobox_output_format.addItem("Gmsh MSH (*.msh)")
            self.central.combobox_output_format.addItem("Abaqus INP (*.inp)")
            self.central.combobox_output_format.addItem("LSDYNA KEY (*.key)")
            self.central.combobox_output_format.addItem("RADIOSS BLOCK (*_0000.rad)")
            self.central.combobox_output_format.addItem("CELUM (*.celum)")
            self.central.combobox_output_format.addItem("CGNS(Experimental) (*.cgns)")
            self.central.combobox_output_format.addItem("Diffpack 3D (*.diff)")
            self.central.combobox_output_format.addItem("I-deas Universal (*.unv)")
            self.central.combobox_output_format.addItem("Iridum (*.ir3)")
            self.central.combobox_output_format.addItem("MED (*.med)")
            self.central.combobox_output_format.addItem("Inria Medit (*.mesh)")
            self.central.combobox_output_format.addItem("CEA Triangulation (*.mail)")
            self.central.combobox_output_format.addItem("Matlab (*.m)")
            self.central.combobox_output_format.addItem(
                "Nastran Bulk Data File (*.bdf)"
            )
            self.central.combobox_output_format.addItem("Object File Format (*.off)")
            self.central.combobox_output_format.addItem(
                "Plot3D Structured Mesh (*.p3d)"
            )
            self.central.combobox_output_format.addItem("STL Surface(*.stl)")
            self.central.combobox_output_format.addItem("VTK (*.vtk)")
            self.central.combobox_output_format.addItem("VRML Surface (*.wrl)")
            self.central.combobox_output_format.addItem("Tochnog (*.dat)")
            self.central.combobox_output_format.addItem("PLY2 Surface (*.ply2)")
            self.central.combobox_output_format.addItem("SU2 (*.su2)")
            self.central.combobox_output_format.addItem("GAMBIT Neutral File (*.neu)")
            self.central.combobox_output_format.addItem("X3D (*.x3d)")
            pass

    def Show_Introduction(self):
        QMessageBox.about(
            self,
            "关于",
            "这是一个格式转换器，可以将几何文件和网格文件转换为不同的格式。请先选择文件，再选择输出地址，再选择输出格式，然后可以导出。",
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()

    sys.exit(app.exec_())
