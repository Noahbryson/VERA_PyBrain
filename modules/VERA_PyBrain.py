from pathlib import Path
import scipy.io as scio

class VERA_PyBrain():
    def __init__(self,path2file:str,subject:str=''):
        path=Path(path2file)
        if subject != '':
            self.subject = subject
        else:
            self.subject = None
        self._loadMat(path)
    def _loadMat(self,fp:Path):
        self.brainType = fp.name.split('.')[0]
        try:
            temp = scio.loadmat(fp,mat_dtype=True,simplify_cells=True)
            for k,v in sorted(temp.items()):
                if not isinstance(v,dict):
                    self.__setattr__(k,v)
                else:
                    self.__setattr__(k,VERA_component(v))
        except:
            print('error loading brain :(')
        else:
            print('brain loaded successfully yay')
        finally:
            print('module complete')

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