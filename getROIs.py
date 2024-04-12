from modules.VERA_PyBrain import VERA_PyBrain

if __name__ == '__main__':
    # loc = r'C:\Users\nbrys\Box\Brunner Lab\DATA\SCAN_Mayo\BJH041\brain\brain_MNI.mat'
    loc = r'/Users/nkb/Library/CloudStorage/Box-Box/Brunner Lab/DATA/SCAN_Mayo/BJH041/brain/brain_MNI.mat'
    vera = VERA_PyBrain(loc)
    vera.export_ROI_map()