import scipy.io as scio
from pathlib import Path
import csv
import os
import glob

class loadVERA():
      def __init__(self,fpath:Path,brainName:str='brain'):
            self.subjectRoot = fpath.parent
            self.brainDir = fpath
            self.brainType = brainName
            attrNames = []
            fp = self.brainDir / f'{brainName}.mat'
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
                  self.__reindex_matricies__()
            finally:
                  self.attrNames = attrNames
                  print('module complete, attributes stored')
            

      def __reindex_matricies__(self):
           self.cortex.tri = self.cortex.tri -1
                

class VERA_component():
    """class that recurses through dictionaries to make them into object variables rather than string keys for continuity with MATLAB struct interface"""
    def __init__(self,input:dict):
        for k,v in input.items():
            if isinstance(v,dict):
                self.__setattr__(k,VERA_component(v))
            else:
                self.__setattr__(k,v)
                
                
def VERA_rosamap(fp:Path|str) -> list:
      if os.path.exists(fp):
            with open(fp,'r',encoding='utf-8-sig') as file:
                  reader = csv.reader(file)
                  return [r for r in reader]
      else:
            print('ROSA Mapping does not exist')
            return []