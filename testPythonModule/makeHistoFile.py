import os,sys
from ROOT import *
from bjetClasses import *


def main():

    dir = 'data/'
    filesList = []
    for ifile in os.listdir(dir):
        filesList.append(ifile)
    filesList.sort()

    h_R_bl = {}

    for ifile in filesList:
        sampleID = ifile.split('.')[1]
        
        print ifile
        file = TFile.Open(dir+ifile)
        tree = file.Get("susy")

        outf = TFile.Open("histosToCompare.PythonModule.root","RECREATE")

        h_R_bl[sampleID] = TH1F("h_R_bl_"+sampleID,"",30,0,1)

        i = 0
        for entry in tree:
            if ( i % 10000 == 0):
                print '%s / %s' % (i,tree.GetEntries())
            i+=1

            t_is2b = entry.is2b
            
            if t_is2b == 0: continue

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

            t_mc_event_weight = entry.mc_event_weight
            t_ttbar_weight = entry.ttbar_weight
            t_Wj_sherpa_weight = entry.Wj_sherpa_weight
            
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

            jets = bjetExtractor(j1,j2,j3,j4,t_jet1_MV1,t_jet2_MV1,t_jet3_MV1,t_jet4_MV1)
            bjetvars = bjetVariables(jets.bjet1,jets.bjet2,jets.jet1,jets.jet2,lep)
            
            eventWeight = t_mc_event_weight
            if t_ttbar_weight != -999:
                eventWeight *= t_ttbar_weight
            if t_Wj_sherpa_weight != -999:
                eventWeight *= t_Wj_sherpa_weight
            
            
            h_R_bl[sampleID].Fill(bjetvars.getR_bl(),eventWeight)
            
 

    #Don't know why, but have to use this method to get it written into the file
    outf.cd()
    for sampleID in list(h_R_bl.keys()):
        h_R_bl[sampleID].Write()
    

if __name__ == "__main__":
    main()

