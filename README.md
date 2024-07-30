# Introduction
  This is a Geometry file and Mesh file converter based on [GMSH](https://gmsh.info/)。
### Geometry
From 
```
 Gmsh GEO (*.geo
 OpenCASCADE BREP (*.brep)
 OpenCASCADE XAO (*.xao)
 STEP (*.stp *.step)
 IGES (*.igs *.iges)
```
To
```
Gmsh Options (*.opt)
Gmsh Unrolled GEO (*.geo_unrolled)
OpenCASCADE BREP (*.brep)
OpenCASCADE XAO (*.xao)
STEP (*.step)
IGES (*.iges)
```
### Mesh
From
```
Gmsh MSH (*.msh)
Diffpack 3D (*.diff)
I-deas Universal (*.unv)
MED (*.med *.mmed)
Inria Medit (*.mesh)
Nastran Bulk Data File (*.bdf *.nas)
Gambit Neutral (*.neu)
Object File Format (*.off)
Plot3D Structured Mesh (*.p3d)
STL Surface(*.stl)
VTK (*.vtk)
VRML Surface (*.wrl *vrml)
PLY2 (*.ply)
```
To
```
Gmsh MSH (*.msh)
Abaqus INP (*.inp)
LSDYNA KEY (*.key)
RADIOSS BLOCK (*_0000.rad)
CELUM (*.celum)
CGNS(Experimental) (*.cgns)
Diffpack 3D (*.diff)
I-deas Universal (*.unv)
Iridum (*.ir3)
MED (*.med)
Inria Medit (*.mesh)
CEA Triangulation (*.mail)
Matlab (*.m)
Nastran Bulk Data File (*.bdf)
Object File Format (*.off)
Plot3D Structured Mesh (*.p3d)
STL Surface(*.stl)
VTK (*.vtk)
VRML Surface (*.wrl)
Tochnog (*.dat)
PLY2 Surface (*.ply2)
SU2 (*.su2)
GAMBIT Neutral File (*.neu)
X3D (*.x3d)
```
# Usage
  * Use Python 3.10 or lower version
  * Install gmsh and PyQt5 libraries:
```python
pip install gmsh
pip install pyqt5
```
  * Download/copy two python file here.
  * Run it
# Others
Remember to star this project!!!
