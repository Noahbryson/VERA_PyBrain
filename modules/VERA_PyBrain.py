from pathlib import Path
import scipy.io as scio
import numpy as np
import csv
import matplotlib.pyplot as plt
import pyvista as pv
from functions import functions as f
from VERA_utils import loadVERA, VERA_component, VERA_rosamap
# from pyvista import plotting

class VERA_PyBrain(loadVERA):
    """module housing all of the parameters from the VERA .mat file as well as visualization and analysis tools."""
    def __init__(self,fp:str,subject:str=''):
        self.path=Path(fp)
        if subject != '':
            self.subject = subject
        else:
            self.subject = None
        super().__init__(self.path)
        # self._loadMat(path)
        self.mapping = VERA_rosamap(self.path.parent.parent / 'channel_rosa_map.csv')
        for i,entry in enumerate(self.mapping):
            entry[1] = entry[1][1:-1]
            if entry[0][-1] == 'X':
                entry[0] == 'IDX'
            if entry[1].find("''")>-1:
                entry[1]=entry[1].replace("''","'")
            # self.mapping
        self.funcs = f()

    
    def alignBCI2kChannels(self):
        x = {a:b for a,b in zip(self.electrodeNames,self.electrodeDefinition.Label)}
        labels = {x[1]:x[2] for x in self.mapping}
        output = {labels[k]:v for k,v in x.items()}
        return output
    
    def get_ROI_map(self):
        channels = self.alignBCI2kChannels()
        output = {k:list() for k in channels.values()}
        for k,v in channels.items():
            output[v].append(k)    
        return output
    def export_ROI_map(self):
        data = self.get_ROI_map()
        savePath = self.path.parent
        writeFormat = []
        for k,v in data.items():
            writeFormat.append([k,v])
        with open(savePath/'channel_locations.csv','w') as fp:
            writer = csv.writer(fp)
            writer.writerow(['Closest Region','Channels'])
            for w in writeFormat:
                writer.writerow(w)
        print(f'file written to {savePath}')
            
    
    def listAttributes(self):
        for i in self.attrNames:
            print(f'name: {i}, type {type(self.__getattribute__(i))}')

    def generateAxis(self,figname:str='VERA_PyBrain basic fig',engine:str='matplotlib'):
        """For Generation of a standalone figure and axis for plotting one thing. More advanced plotting should use user defined axes.
            This function is designed for simple vizualizations and testing"""
        if engine == 'pyvista':
            ax = pv.Plotter(shape=(1,1))
        else:
            "default matplotlib engine"
            ax = plt.figure(figname).add_subplot(111,projection='3d')
        return  ax,engine

    def plotAllVolumes(self, ax:plt.axes,engine:str='matplotlib'):
        if engine == 'pyvista':
            # faces = np.concatenate((3*np.ones([len(self.cortex.tri), 1]), self.cortex.tri), axis=1)
            # faces = faces.astype(np.int32).flatten()
            # vertices = self.cortex.vert
            # cloud = pv.PolyData(vertices, faces)
            # # cloud.plot(show_edges=True, color=True)
            # plotter = pv.Plotter()
            # plotter.add_mesh(cloud, smooth_shading=False)
            # plotter.show()
            tris = self.cortex.tri
            tris.sort(axis=0)
            verts = self.cortex.vert
            faces = np.hstack((np.full((len(tris),1),3, dtype=np.int32),tris))
            # tris = tris[0:int(len(tris)/2)]
            testFace = self.funcs.flattenCells(tris)
            # testFace = [3,1,2,3]
            cloud = pv.PolyData(verts,testFace)
            mesh = pv.PolyData(verts)
            cloud = pv.PolyData.from_regular_faces(verts,tris)
            # mesh.plot(show_edges=True, color=True)
            # subdiv = cloud.subdivide(nsub=1, subfilter='linear')
            # subdiv.compute_normals(cell_normals=True, inplace=True)
            # subdiv.plot(smooth_shading=True)

            # cloud = cloud.subdivide(nsub=1, subfilter='linear')
            # cloud.compute_normals(inplace=True)
            cloud.plot(smooth_shading=False)


            print('setup')



            return cloud
        else:
            "default matplotlib engine"
            x = self.cortex.vert[:,0]
            y = self.cortex.vert[:,1]
            z = self.cortex.vert[:,2]
            ax.plot_trisurf(x,y,z,triangles =self.cortex.tri.astype(np.uint16))
            return ax
        # breakpoint()
        
    def show(self, engine = 'pyvista',**kwargs):
        if engine == 'pyvista':
            pass
        else:
            "default matplotlib engine"
            plt.show()


                

if __name__ == '__main__':
    # loc = r'C:\Users\nbrys\Box\Brunner Lab\DATA\SCAN_Mayo\BJH041\brain\brain_MNI.mat'
    loc = r'/Users/nkb/Library/CloudStorage/Box-Box/Brunner Lab/DATA/SCAN_Mayo/BJH046/brain/brain_MNI.mat'
    vera = VERA_PyBrain(loc)
    vera.listAttributes()
    # ax,engine = vera.generateAxis(engine='pyvista')
    ax,engine = vera.generateAxis()

    # ax,engine = vera.generateAxis()
    vera.plotAllVolumes(ax,engine)
    vera.show(engine=engine)