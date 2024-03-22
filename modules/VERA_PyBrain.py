from pathlib import Path
import scipy.io as scio
import matplotlib.pyplot as plt
import pyvista as pv

# from pyvista import plotting

class VERA_PyBrain():
    """module housing all of the parameters from the VERA .mat file as well as visualization and analysis tools."""
    def __init__(self,path2file:str,subject:str=''):
        path=Path(path2file)
        if subject != '':
            self.subject = subject
        else:
            self.subject = None
        self._loadMat(path)
    def _loadMat(self,fp:Path):
        self.brainType = fp.name.split('.')[0]
        attrNames = []
        try:
            temp = scio.loadmat(fp,mat_dtype=True,simplify_cells=True)
            for k,v in sorted(temp.items()):
                if not isinstance(v,dict):
                    self.__setattr__(k,v)
                    attrNames.append(k)
                else:
                    self.__setattr__(k,VERA_component(v))
                    attrNames.append(k)
        except:
            print('error loading brain :(')
        else:
            print('brain loaded successfully yay')
        finally:
            self.attrNames = attrNames
            print('module complete, attributes stored')

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
            cloud = pv.PolyData(self.cortex.vert)
            brain = cloud.delaunay_3d(progress_bar=True)
            brain.plot()
            return brain
        else:
            "default matplotlib engine"
            x = self.cortex.vert[:,0]
            y = self.cortex.vert[:,1]
            z = self.cortex.vert[:,2]
            ax.plot_trisurf(x,y,z)
            return ax
        # breakpoint()
        
    def show(self, engine = 'pyvista',**kwargs):
        if engine == 'pyvista':
            pass
        else:
            "default matplotlib engine"
            plt.show()

class VERA_component():
    """class that recurses through dictionaries to make them into object variables rather than string keys for continuity with MATLAB struct interface"""
    def __init__(self,input:dict):
        for k,v in input.items():
            if isinstance(v,dict):
                self.__setattr__(k,VERA_component(v))
            else:
                self.__setattr__(k,v)
                

if __name__ == '__main__':
    loc = r'C:\Users\nbrys\Box\Brunner Lab\DATA\SCAN_Mayo\BJH041\brain\brain_MNI.mat'
    vera = VERA_PyBrain(loc)
    vera.listAttributes()
    ax,engine = vera.generateAxis(engine='pyvista')
    vera.plotAllVolumes(ax,engine)
    vera.show(engine=engine)