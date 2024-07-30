import gmsh
import sys
import os

def Trans_Geometry(file_paths, output_path, output_format):
    for file_path in file_paths:
        out_last_name=output_format.split("*")[1][:-1]
        #print(out_last_name)
        #print(file_path)
        #print(os.path.split(file_path))
        #print(output_format)
        gmsh.initialize()
        gmsh.model.add("model")
        gmsh.open(file_path)
        out_name=os.path.splitext(os.path.split(file_path)[1])
        print(os.path.join(output_path,out_name[0])+out_last_name)
        #pause=input("Press Enter to continue...")
        gmsh.write(os.path.join(output_path,out_name[0])+out_last_name)
        gmsh.clear()
        gmsh.finalize()

def Trans_Mesh(file_paths, output_path, output_format):
    for file_path in file_paths:
        out_last_name=output_format.split("*")[1][:-1]
        #print(out_last_name)
        #print(file_path)
        #print(os.path.split(file_path))
        #print(output_format)
        gmsh.initialize()
        gmsh.model.add("model")
        gmsh.open(file_path)
        out_name=os.path.splitext(os.path.split(file_path)[1])
        print(os.path.join(output_path,out_name[0])+out_last_name)
        #pause=input("Press Enter to continue...")
        gmsh.write(os.path.join(output_path,out_name[0])+out_last_name)
        gmsh.clear()
        gmsh.finalize()
    pass