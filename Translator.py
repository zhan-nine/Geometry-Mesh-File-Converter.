import gmsh

# C. Geuzaine and J.-F. Remacle. Gmsh: a three-dimensional finite element mesh generator with built-in pre- and post-processing facilities. International Journal for Numerical Methods in Engineering 79(11), pp. 1309-1331, 2009.
import sys
import os


class MyTranslator:
    def __init__(self):
        self.nodeTags = []
        self.nodeCoords = []
        self.nodeParams = []
        self.edgeNodes = []
        self.edgeTags = []
        self.faceNodes = []
        self.faceTags = []
        self.volumes = []
        pass

    def Get_Mesh_Dim_Elements(self, file_path):
        #  本函数实现可以从Gmsh Python extended tutorial 7找指令
        gmsh.initialize()
        gmsh.model.add("model")
        gmsh.open(file_path)
        # 获取网格中体的个数
        self.volumes = gmsh.model.getEntities(3)
        # 获取网格中点的个数
        for dim, tag in self.volumes:
            nodeTags, nodeCoords, nodeParams = gmsh.model.mesh.getNodes(dim, tag)
            self.nodeTags += nodeTags
            self.nodeCoords += nodeCoords
            self.nodeParams += nodeParams
        print(len(self.nodeTags))
        # 获取网格中边的个数
        gmsh.model.mesh.createEdges()
        # edgeNodes是edgeTags的两倍，每个边有两个节点
        self.edgeTags, self.edgeNodes = gmsh.model.mesh.getAllEdges()
        print(len(self.edgeTags), " ", len(self.edgeNodes))
        # print(self.edgeTags)
        # 获取网格中面的个数
        gmsh.model.mesh.createFaces()
        # faceNodes是faceTags的三倍，每个面有三个节点
        self.faceTags, self.faceNodes = gmsh.model.mesh.getAllFaces(3)
        print(gmsh.model.mesh.getElements(2))
        print(len(self.faceTags), " ", len(self.faceNodes))
        # print(self.faceTags)
        gmsh.clear()
        gmsh.finalize()
        pass

    def Trans_Geometry(file_paths, output_path, output_format):
        for file_path in file_paths:
            out_last_name = output_format.split("*")[1][:-1]
            # print(out_last_name)
            # print(file_path)
            # print(os.path.split(file_path))
            # print(output_format)
            gmsh.initialize()
            gmsh.model.add("model")
            gmsh.open(file_path)
            out_name = os.path.splitext(os.path.split(file_path)[1])
            print(os.path.join(output_path, out_name[0]) + out_last_name)
            # pause=input("Press Enter to continue...")
            gmsh.write(os.path.join(output_path, out_name[0]) + out_last_name)
            gmsh.clear()
            gmsh.finalize()

    def Trans_Mesh(file_paths, output_path, output_format):
        for file_path in file_paths:
            out_last_name = output_format.split("*")[1][:-1]
            # print(out_last_name)
            # print(file_path)
            # print(os.path.split(file_path))
            # print(output_format)
            gmsh.initialize()
            gmsh.model.add("model")
            gmsh.open(file_path)
            out_name = os.path.splitext(os.path.split(file_path)[1])
            print(os.path.join(output_path, out_name[0]) + out_last_name)
            # pause=input("Press Enter to continue...")
            gmsh.write(os.path.join(output_path, out_name[0]) + out_last_name)
            gmsh.clear()
            gmsh.finalize()
        pass


# 以下用于测试
# if __name__ == "__main__":
#     MyMesh = MyTranslator()
#     MyMesh.Get_Mesh_Dim_Elements("files/output.mesh")
