import os,sys

from ROOT import *

def getFilesList(dirName):
    filesList = []
    for ifile in os.listdir(dirName):
        if '.root' in ifile:
            filesList.append(ifile)
    filesList.sort()
    return filesList

def main():
    
    filesList = getFilesList('data/')

    h_R_bl = {}
    for ifile in filesList:
        print ifile
        
        sampleID = ifile.split('.')[1]
        h_R_bl[sampleID] = TH1F("h_R_bl_"+sampleID,"",30,0,1)
        
        file = TFile.Open('data/'+ifile)
        outf = TFile.Open('histosToCompare.PythonOldMethod.root','RECREATE')
        
        tree = file.Get("susy")

        i = 0
        for entry in tree:
            if (i % 10000 == 0):
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
            
            j1lv = TLorentzVector()
            j2lv = TLorentzVector()
            j3lv = TLorentzVector()
            j4lv = TLorentzVector()
            lep = TLorentzVector()

            j1lv.SetPtEtaPhiE(t_jet1_pT,t_jet1_eta,t_jet1_phi,t_jet1_E)
            j2lv.SetPtEtaPhiE(t_jet2_pT,t_jet2_eta,t_jet2_phi,t_jet2_E)
            j3lv.SetPtEtaPhiE(t_jet3_pT,t_jet3_eta,t_jet3_phi,t_jet3_E)
            j4lv.SetPtEtaPhiE(t_jet4_pT,t_jet4_eta,t_jet4_phi,t_jet4_E)          
            lep.SetPtEtaPhiE(t_lep1_pT,t_lep_eta,t_lep_phi,t_lep_E)


            lvList = [[j1lv,t_jet1_MV1],
                     [j2lv,t_jet2_MV1],
                     [j3lv,t_jet3_MV1],
                     [j4lv,t_jet4_MV1]]

            #Sort by MV1:
            lvList.sort(key = lambda ll: ll[1])

            
            #Now get leading and subleading bjet:
            bjet1 = TLorentzVector()
            bjet2 = TLorentzVector()
            #print 'JETINFO GIVEN HERE:'
            #print 'B JETS:'
            if lvList[2][0].Pt() > lvList[3][0].Pt():
                bjet1 = lvList[2][0]
                bjet2 = lvList[3][0]
                    
            else:
                bjet1 = lvList[3][0]
                bjet2 = lvList[2][0]
                    

                
            jet1 = TLorentzVector()
            jet2 = TLorentzVector()
            
            if lvList[0][0].Pt() > lvList[1][0].Pt():
                jet1 = lvList[0][0]
                jet2 = lvList[1][0]
            else:
                jet1 = lvList[1][0]
                jet2 = lvList[0][0]
                
            Wh = TLorentzVector()
            Wh = (jet1+jet2)
            
                
            dMW = 2100 # in MeV
            dMtop = 2000 # in MeV
            
            MW =     80.385 * 1000 #MeV
            Mtop =  173.5 * 1000 # MeV again
            
            dM_Whb1 = (MW - Wh.M())**2 / (dMW**2) + (Mtop - (Wh+bjet1).M())**2 / (dMtop**2)
            dM_Whb2 = (MW - Wh.M())**2 / (dMW**2) + (Mtop - (Wh+bjet2).M())**2 / (dMtop**2)

            if dM_Whb1 < dM_Whb2:
                R_bl = lep.Pt() / (lep.Pt() + bjet2.Pt())
            else:
                R_bl = lep.Pt() / (lep.Pt() + bjet1.Pt())

            eventWeight = t_mc_event_weight
            if t_ttbar_weight != -999:
                eventWeight *= t_ttbar_weight
            if t_Wj_sherpa_weight != -999:
                eventWeight *= t_Wj_sherpa_weight
            
            
            h_R_bl[sampleID].Fill(R_bl,eventWeight)
            
    outf.cd()
    for sampleID in list(h_R_bl.keys()):
        h_R_bl[sampleID].Write()
    
if __name__ == "__main__":
    main()
