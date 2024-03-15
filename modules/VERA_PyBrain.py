from pathlib import Path
import scipy.io as scio

class VERA_PyBrain:
    def __init__(self,path2file:str):
        path=Path(path2file)
        self.brain=self._loadMat(path)

    def _loadMat(self,fp:Path):
        temp = scio.loadmat(fp,mat_dtype=True,simplify_cells=True)
        self.brain = 0


if __name__ == '__main__':
    loc = r'C:\Users\nbrys\Box\Brunner Lab\DATA\SCAN_Mayo\BJH041\brain\brain_MNI.mat'
    vera = VERA_PyBrain(loc)