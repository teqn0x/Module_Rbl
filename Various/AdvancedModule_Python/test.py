import os,sys

from ROOT import *

from bjetClassesv2 import bjetExtractor

def getFilesList(dirName):
    filesList = []
    for ifile in os.listdir(dirName):
        if '.root' in ifile:
            filesList.append(ifile)

    filesList.sort()
    return filesList


def main():
    dir = 'inputs/'
    filesList = getFilesList(dir)

    for ifile in filesList:
        print ifile

        file = TFile(dir+ifile)
        tree = file.Get("susy")

        i = 0
        for entry in tree:

            if (i% 100000 == 0):
                print '%s / %s' % (i,tree.GetEntries())
            i+=1

            t_is1b = entry.is1b
            t_is2b = entry.is2b

            t_Bjet1_pT = entry.Bjet1_pT
            t_Bjet2_pT = entry.Bjet2_pT

            t_nJet = entry.nJet
            
            t_asymm_bl = entry.asymm_bl
            
            t_jet1_pT = entry.jet1_pT
            t_jet2_pT = entry.jet2_pT
            t_jet3_pT = entry.jet3_pT
            t_jet4_pT = entry.jet4_pT            

            t_jet1_eta = entry.jet1_eta
            t_jet2_eta = entry.jet2_eta
            t_jet3_eta = entry.jet3_eta
            t_jet4_eta = entry.jet4_eta            

            t_jet1_phi = entry.jet1_phi
            t_jet2_phi = entry.jet2_phi
            t_jet3_phi = entry.jet3_phi
            t_jet4_phi = entry.jet4_phi

            t_jet1_E = entry.jet1_E
            t_jet2_E = entry.jet2_E
            t_jet3_E = entry.jet3_E
            t_jet4_E = entry.jet4_E
            
            t_jet1_MV1 = entry.jet1_MV1
            t_jet2_MV1 = entry.jet2_MV1
            t_jet3_MV1 = entry.jet3_MV1
            t_jet4_MV1 = entry.jet4_MV1

            t_lep1_pT = entry.lep1_pT
            t_lep_eta = entry.lep_eta
            t_lep_phi = entry.lep_phi
            t_lep_E = entry.lep_E
            
            j1 = TLorentzVector()
            j2 = TLorentzVector()
            j3 = TLorentzVector()
            j4 = TLorentzVector()
            lep = TLorentzVector()

            j1.SetPtEtaPhiE(t_jet1_pT,t_jet1_eta,t_jet1_phi,t_jet1_E)
            j2.SetPtEtaPhiE(t_jet2_pT,t_jet2_eta,t_jet2_phi,t_jet2_E)
            j3.SetPtEtaPhiE(t_jet3_pT,t_jet3_eta,t_jet3_phi,t_jet3_E)
            j4.SetPtEtaPhiE(t_jet4_pT,t_jet4_eta,t_jet4_phi,t_jet4_E)          
            lep.SetPtEtaPhiE(t_lep1_pT,t_lep_eta,t_lep_phi,t_lep_E)

            jets = bjetExtractor(j1,j2,j3,j4,t_jet1_MV1,t_jet2_MV1,t_jet3_MV1,t_jet4_MV1,t_Bjet1_pT,t_Bjet2_pT)


if __name__ == "__main__":
    main()
