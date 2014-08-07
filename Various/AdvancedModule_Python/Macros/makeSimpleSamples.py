import os,sys

def getFilesList(dirName):
    filesList = []
    for ifile in os.listdir(dirName):
        if 'WimpPair' in ifile: continue
        if '_NONE_' in ifile:
            filesList.append(ifile)
    filesList.sort()
    return filesList

    
def main():
    dir = '/glusterfs/atlas6/users/stopTeam/outputs-p15xx/outputs-p15xx-Aug17/mc-forTMVA/lepton-signal/'

    filesList = getFilesList(dir)

    
    outf = open('ID2NameSamples.py','w')

    outf.write('ID2Name = {\n')
    for ifile in filesList:
        sampleID = ifile.split('.')[1]
        stopmass = ifile.split('_')[4]
        charmass = ifile.split('_')[5]
        neutmass = ifile.split('_')[6]
        outf.write('\'%s\' : \'%s_%s_%s\',\n' % (sampleID,stopmass,charmass,neutmass))
    outf.write('}')
    
if __name__ == "__main__":
    main()
