from pathlib import Path
import scipy.io as scio
import numpy as np
import csv
import matplotlib.pyplot as plt
import pyvista as pv
from VERA_utils import loadVERA, VERA_component, VERA_rosamap
from helper_functions import flattenCells, nonhomogenous_shape
import distinctipy
# from pyvista import plotting

class VERA_PyBrain(loadVERA):
    """module housing all of the parameters from the VERA .mat file as well as visualization and analysis tools."""
    def __init__(self,fp:str|Path,subject:str='',brainName: str='brain'):
        if isinstance(fp,str):
            fp = Path(fp)
        self.path=Path(fp)
        if subject != '':
            self.subject = subject
        else:
            self.subject = None
        super().__init__(fpath=self.path,brainName=brainName)
        # self._loadMat(path)
        self.mapping = self.getMapping()
        self.default_colors = self.get_annotation_cmap()
            # self.mapping
    
    def set_subject_result_dir(self,fpath: str|Path):
        if isinstance(fpath,str):
            fpath = Path(fpath)
        self.data_root = fpath
    def load_channel_results(self,fpath:str|Path):
        """
        -----------
        load_channel_results loads electrode channel names and an associated effect size from analysis script output .mat file. 
        Allows for volumetric plotting of an effect. Note this loading function will work for a single floating point value or an array, though further processing is needed to display the array as a video. 
        -----------
        Args:
            fpath (str | Path): filepath to .mat file containing channel names and channel labels.
        ----------
        Returns:
        dictionary with the channel name remapped to the VERA structure as the key, and the loaded effect as the value
        """
        labels = scio.loadmat(fpath)
    def load_channel_labels(self,fpath:str|Path):
        """
        -----------
        load_channel_labels loads electrode channel names from analysis script output .mat file, sets an index for a given channel to parse an array. 
        Most commonnly used for assigning colors to each electrode
        -----------
        Args:
            fpath (str | Path): filepath to .mat file containing channel names and channel labels. 
        ----------
        Returns:
        dictionary with the channel name remapped to the VERA structure as the key, and the loaded label as the value
        """
        labels = scio.loadmat(fpath)

    def make_color_list(self,numColors:int=1, fromFile: bool=False,filepath:str|Path='',pastel:float=0.6):
        """make_cmap _summary_

        Args:
            numColors (int): _description_
            fromFile (bool, optional): _description_. Defaults to False.
            filepath (str | Path, optional): _description_. Defaults to ''.

        Returns:
            _type_: _description_
        """
        colors = 0
        if fromFile:
            pass
        else:
            colors = distinctipy.get_colors(numColors,pastel_factor=pastel,rng=0)
        return colors
    
    
    def getMapping(self):
        mapVals = VERA_rosamap(self.path.parent / 'channel_rosa_map.csv')
        output = {}
        for i,entry in enumerate(mapVals):
            if entry[1][0] == "'":
                entry[1] = entry[1][1:-1]
            if entry[0]==entry[1] or entry[0] == 'IDX':
                pass
            else:
                if entry[1].find("''")>-1:
                    entry[1]=entry[1].replace("''","'")
                output[entry[2]] = [entry[1],int(entry[0])]
        return output
    
    def alignBCI2kChannels(self):
        x = {a:b for a,b in zip(self.electrodeNames,self.electrodeDefinition.Label)}
        labels = {x[1]:x[2] for x in self.mapping}
        output = {labels[k]:v for k,v in x.items() if k in labels.keys()}
        return output
    
    def get_ROI_map(self):
        channels = self.alignBCI2kChannels()
        output = {k:list() for k in channels.values()}
        for k,v in channels.items():
            output[v].append(k)    
        return output
    def export_ROI_map(self):
        if len(self.mapping) > 0:
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
        else:
            print('no mapping file present, please see rosa map example file.')
    
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

    def plotAllVolumes(self, ax,engine:str='matplotlib'):
        if engine == 'pyvista':

            tris = self.cortex.tri
            verts = self.cortex.vert
            faces = flattenCells(tris)
            cloud = pv.PolyData(verts,faces)
            cloud.compute_normals(cell_normals=True, inplace=True)
            cloud['colors'] = self.default_colors
            ax.add_mesh(cloud,smooth_shading=True,scalars='colors')
            # ax.add_volume(cloud)#,rgb=self.default_colors)


            print('setup')



            return ax
        else:
            "default matplotlib engine"
            x = self.cortex.vert[:,0]
            y = self.cortex.vert[:,1]
            z = self.cortex.vert[:,2]
            ax.plot_trisurf(x,y,z,triangles =self.cortex.tri.astype(np.uint16))
            return ax
        
    def plot_electrodes_on_volume(self,volume):
        
        return volume
        
        # breakpoint()
    
    def show(self, engine = 'pyvista',**kwargs):
        if engine == 'pyvista':
            # ax.export_obj('pv.obj')
            ax.show()
        else:
            "default matplotlib engine"
            plt.show()

    def get_annotation_cmap(self):
        data = self.annotation
        output = np.zeros([len(data.Annotation),4],np.ndarray)
        value_map = {}
        test_map = {}
        test_colors = []
        region_map = {}
        region_colors = distinctipy.get_colors(len(data.AnnotationLabel))
        region_colors.reverse()
        for i,region in enumerate(data.AnnotationLabel):
            test_map[region['Identifier']]=region['PreferredColor']
            test_colors.append(region['PreferredColor'])
            value_map[region['Identifier']]=distinctipy.get_rgb256(region_colors[i])
            region_map[region['Name']]=region['PreferredColor']
        # fig = plt.figure()
        # ax1 = fig.add_subplot(1,2,1)
        # ax2 = fig.add_subplot(1,2,2)
        
        
        
        # distinctipy.color_swatch(region_colors, ax=ax1, title="distinctipy")
        # distinctipy.color_swatch(test_colors, ax=ax2, title="default")
        # plt.show()
        for i in range(len(output)):
            try:
                output[i][0:3] = value_map[data.Annotation[i]]#*255
                output[i][3] = 0.5*255
            except KeyError:
                output[i][:] = np.array([1,1,1,0.5]).reshape(1,4)*255
        if isinstance(output,list):
            color_array = np.array(output)
        color_array = np.asarray(np.vstack(output),dtype=np.uint8)
        return color_array
        
                

if __name__ == '__main__':
    # loc = r'C:\Users\nbrys\Box\Brunner Lab\DATA\SCAN_Mayo\BJH041\brain\brain_MNI.mat'
    rootDir = Path(r'/Users/nkb/Library/CloudStorage/Box-Box/Brunner Lab/DATA/SCAN_Mayo/BJH041')
    brain_name = 'brain_MNI'
    vera = VERA_PyBrain(rootDir/'brain',brainName=brain_name)
    vera.set_subject_result_dir(rootDir)
    vera.listAttributes()
    ax,engine = vera.generateAxis(engine='pyvista')
    # ax,engine = vera.generateAxis()

    # ax,engine = vera.generateAxis()
    vera.plotAllVolumes(ax,engine)
    vera.show(engine=engine,ax=ax)