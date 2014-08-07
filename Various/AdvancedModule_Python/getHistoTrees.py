import os,sys

from bjetClasses import *

from ROOT import *



def main():

    preselCuts = True

    #Getting the proper filesList:
    dir = '/glusterfs/atlas6/users/stopTeam/outputs-p15xx/outputs-p15xx-Aug22/mc-forTMVA/'

    filesList = []
    for ifile in os.listdir(dir+'lepton-signal'):
        if 'WimpPair' in ifile or 'LQLQ2' in ifile or '_Tt_' in ifile: continue
        if '_NONE_' in ifile:
            filesList.append(ifile)

    filesList.append('mc12_8TeV.117050.PowhegPythia_P2011C_ttbar.e1727_a188_a171_r3549_p15_NONE_tmva.root')
    filesList.sort()

    h_R_bl_orig_list = {}
    h_R_bl_new_list = {}
    h_R_bl_new2b_list = {}

    h_Asymm_bl_orig_list = {}
    h_Asymm_bl_new_list = {}
    h_Asymm_bl_new2b_list = {}

    h_Bjets_pT_orig_list = {}
    h_Bjets_pT_new_list = {}
    h_Bjets_pT_new2b_list = {}

    h_m_Wh_orig_list  = {}
    h_m_Wh_new_list   = {}
    h_m_Wh_new2b_list = {}
    

    h_asymm_bl_list = {}
    h_Bjet_pTsum_list = {} #Not defined in the ntuples anymore, it seems that Bjet1_pT and Bjet2_pT are more powerfull anyway in the new grid I'm using, but lets just keep this in for the sake of completeness
    
    #A few scatterplots:
    h_bj1s_pT_orig_list = {}
    h_bj2s_pT_orig_list = {}

    h_bj1s_pT_new_list = {}
    h_bj2s_pT_new_list = {}

    h_bj1s_pT_new2b_list = {}
    h_bj2s_pT_new2b_list = {}

    h_R_bl_orignew_list = {}
    h_R_bl_orignew2b_list = {}

    h_R_bl_orignewnew2b_list = {}
    
    h_asymm_bl_orig_list = {}
    h_asymm_bl_new_list = {}

    h_R_bl_orig_asymm_bl_list = {}
    h_R_bl_new_asymm_bl_list = {}
    h_R_bl_new2b_asymm_bl_list = {}

    

    topologies = ['is1b','is2b','pure1b']

    outf = TFile('Histos.root','RECREATE')


    for ifile in filesList:
        sampleID = ifile.split('.')[1]
        print ifile

        if '117050' in ifile:
            file = TFile(dir+'lepton/'+ifile)
        else:
            file = TFile(dir+'lepton-signal/'+ifile)

        tree = file.Get('susy')

        for topo in topologies:
            h_R_bl_orig_list [topo+sampleID] = TH1F("h_R_bl_orig_"+topo+"_"+sampleID,";R_bl (original);",50,0,1)
            h_R_bl_new_list  [topo+sampleID] = TH1F("h_R_bl_new_"+topo+"_"+sampleID,";R_bl (new);",50,0,1)
            h_R_bl_new2b_list[topo+sampleID] = TH1F("h_R_bl_new2b_"+topo+"_"+sampleID,";R_bl (new,2b);",50,0,1)

            h_Asymm_bl_orig_list[topo+sampleID] = TH1F("h_Asymm_bl_orig_"+topo+"_"+sampleID,";Asymm_bl (original);",50,-1,1)
            h_Asymm_bl_new_list[topo+sampleID] = TH1F("h_Asymm_bl_new_"+topo+"_"+sampleID,";Asymm_bl (new);",50,-1,1)
            h_Asymm_bl_new2b_list[topo+sampleID] = TH1F("h_Asymm_bl_new2b_"+topo+"_"+sampleID,";Asymm_bl (new2b);",50,-1,1)
            
            h_Bjets_pT_orig_list[topo+sampleID] = TH1F("h_Bjets_pT_orig_"+topo+"_"+sampleID,";Bjets_pT(Original);",100,0,1000)
            h_Bjets_pT_new_list[topo+sampleID] = TH1F("h_Bjets_pT_new_"+topo+"_"+sampleID,";Bjets_pT(New);",100,0,1000)
            h_Bjets_pT_new2b_list[topo+sampleID] = TH1F("h_Bjets_pT_new2b_"+topo+"_"+sampleID,";Bjets_pT(New2b);",100,0,1000)
            
            h_asymm_bl_list[topo+sampleID] = TH1F("h_asymm_bl_"+topo+"_"+sampleID,";;",50,-1,1)
            h_Bjet_pTsum_list[topo+sampleID] = TH1F("h_Bjet_pTsum_"+topo+"_"+sampleID,";;",100,0,1000)


            
            h_bj1s_pT_orig_list [topo+sampleID] = TH2F("h_bj1s_pT_orig_"+topo+"_"+sampleID,";Bjet1_pT;orig_bj1_pT",100,0,300,100,0,300)
            h_bj2s_pT_orig_list [topo+sampleID] = TH2F("h_bj2s_pT_orig_"+topo+"_"+sampleID,";Bjet2_pT;orig_bj2_pT",100,0,200,100,0,200)
            
            h_bj1s_pT_new_list [topo+sampleID] = TH2F("h_bj1s_pT_new_"+topo+"_"+sampleID,";Bjet1_pT;bj1_new_pT",100,0,300,100,0,300)
            h_bj2s_pT_new_list [topo+sampleID] = TH2F("h_bj2s_pT_new_"+topo+"_"+sampleID,";Bjet2_pT;bj2_new_pT",100,0,200,100,0,200)
            
            h_bj1s_pT_new2b_list [topo+sampleID] = TH2F("h_bj1s_pT_new2b_"+topo+"_"+sampleID,";Bjet1_pT;bj1_new2b_pT",100,0,300,100,0,300)
            h_bj2s_pT_new2b_list [topo+sampleID] = TH2F("h_bj2s_pT_new2b_"+topo+"_"+sampleID,";Bjet2_pT;bj2_new2b_pT",100,0,200,100,0,200)
            
            h_R_bl_orignew_list [topo+sampleID] = TH2F("h_R_bl_orignew_"+topo+"_"+sampleID,";R_bl_orig;R_bl_new",50,0,1,50,0,1)
            h_R_bl_orignew2b_list [topo+sampleID] = TH2F("h_R_bl_orignew2b_"+topo+"_"+sampleID,";R_bl_orig;R_bl_new2b",50,0,1,50,0,1)

            h_R_bl_orignewnew2b_list [topo+sampleID] = TH3F("h_R_bl_orignewnew2b_"+topo+"_"+sampleID,";R_bl_orig;R_bl_new;R_bl_new2b",50,0,1,50,0,1,50,0,1)
            
            h_asymm_bl_orig_list [topo+sampleID] = TH2F("h_asymm_bl_orig_"+topo+"_"+sampleID,";asymm_bl;orig_asymm_bl",50,-1,1,50,-1,1)
            h_asymm_bl_new_list [topo+sampleID] = TH2F("h_asymm_bl_new_"+topo+"_"+sampleID,";asymm_bl;new_asymm_bl",50,-1,1,50,-1,1)


            h_m_Wh_orig_list[topo+sampleID] = TH1F("h_m_Wh_orig_"+topo+"_"+sampleID,";M_Wh (orig);",100,0,300)
            h_m_Wh_new_list  [topo+sampleID] = TH1F("h_m_Wh_new_"+topo+"_"+sampleID,";M_Wh (new);",100,0,300)
            h_m_Wh_new2b_list[topo+sampleID] = TH1F("h_m_Wh_new2b_"+topo+"_"+sampleID,";M_Wh (new2b);",100,0,300)

            h_R_bl_orig_asymm_bl_list[topo+sampleID] = TH2F("h_R_bl_orig_asymm_bl_"+topo+"_"+sampleID,";R_bl(orig);asymm_bl",50,0,1,50,-1,1)
            h_R_bl_new_asymm_bl_list[topo+sampleID] = TH2F("h_R_bl_new_asymm_bl_"+topo+"_"+sampleID,";R_bl(new);asymm_bl",50,0,1,50,-1,1)
            h_R_bl_new2b_asymm_bl_list[topo+sampleID] = TH2F("h_R_bl_new2b_asymm_bl_"+topo+"_"+sampleID,";R_bl(new2b);asymm_bl",50,0,1,50,-1,1)






        i = 0
        for entry in tree:
            if ( i % 100000 == 0):
                print '%s / %s' % (i,tree.GetEntries())
            i+=1

            t_is1b = entry.is1b
            t_is2b = entry.is2b

            t_Bjet1_pT = entry.Bjet1_pT
            t_Bjet2_pT = entry.Bjet2_pT

            t_asymm_bl = entry.asymm_bl
            
            t_jet1_pT = entry.jet1_pT
            t_jet2_pT = entry.jet2_pT
            t_jet3_pT = entry.jet3_pT
            t_jet4_pT = entry.jet4_pT            

            #Preselection cuts:
            if preselCuts:
                t_j1_MEt_dPhi = entry.j1_MEt_dPhi
                t_j2_MEt_dPhi = entry.j2_MEt_dPhi
                t_MEt_sig4j = entry.MEt_sig4j
                t_nIsoTrk = entry.nIsoTrk
                t_MEt = entry.MEt

                if t_jet1_pT < 80000: continue
                if t_jet2_pT < 60000: continue
                if t_jet3_pT < 40000: continue
                if t_jet4_pT < 25000: continue
                if abs(t_j1_MEt_dPhi) < 0.8: continue
                if abs(t_j2_MEt_dPhi) < 0.8: continue
                if t_nIsoTrk != 0: continue
                #if t_MEt < 150000: continue
                if t_MEt_sig4j < 5: continue



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

            jets1 = bjetExtractor(j1,j2,j3,j4,t_jet1_MV1,t_jet2_MV1,t_jet3_MV1,t_jet4_MV1,t_Bjet1_pT,t_Bjet2_pT)
            jets2 = bjetExtractorMV1(j1,j2,j3,j4,t_jet1_MV1,t_jet2_MV1,t_jet3_MV1,t_jet4_MV1)

            bjetvars1 = bjetVariables(jets1.bjet1,jets1.bjet2,jets1.jet1,jets1.jet2,lep)
            bjetvars2 = bjetVariables(jets2.bjet1,jets2.bjet2,jets2.jet1,jets2.jet2,lep)

            t_total_weight = entry.total_weight

                    
            passSel = {}
            for topo in topologies:
                passSel[topo] = 0
            if t_is1b:
                passSel['is1b'] = 1
                if not t_is2b:
                    passSel['pure1b'] = 1
            if t_is2b:
                passSel['is2b'] = 1



            for topo in topologies:
                if passSel[topo] == 1:
                    h_R_bl_orig_list[topo+sampleID].Fill(bjetvars1.getR_bl(),t_total_weight)
                    h_R_bl_new_list[topo+sampleID].Fill(bjetvars2.getR_bl(),t_total_weight)
                    h_Asymm_bl_orig_list[topo+sampleID].Fill(bjetvars1.getAsymm_bl(), t_total_weight)
                    h_Asymm_bl_new_list[topo+sampleID].Fill(bjetvars2.getAsymm_bl(), t_total_weight)
                    h_Bjets_pT_orig_list[topo+sampleID].Fill(bjetvars1.getBjets_pT()/1000.,t_total_weight)
                    h_Bjets_pT_new_list[topo+sampleID].Fill(bjetvars2.getBjets_pT()/1000.,t_total_weight)
                    h_m_Wh_orig_list[topo+sampleID].Fill( (jets1.jet1 + jets1.jet2).M() / 1000., t_total_weight)
                    h_m_Wh_new_list[topo+sampleID].Fill(  (jets2.jet1 + jets2.jet2).M() / 1000., t_total_weight)
                    

                    
                    if t_Bjet2_pT != -999:
                        h_R_bl_new2b_list[topo+sampleID].Fill(bjetvars2.getR_bl(),t_total_weight)
                        h_Asymm_bl_new2b_list[topo+sampleID].Fill(bjetvars2.getAsymm_bl(),t_total_weight)
                        h_Bjets_pT_new2b_list[topo+sampleID].Fill(bjetvars2.getBjets_pT()/1000.,t_total_weight)
                        h_Bjet_pTsum_list[topo+sampleID].Fill(t_Bjet1_pT / 1000. + t_Bjet2_pT / 1000., t_total_weight)
                        h_m_Wh_new2b_list[topo+sampleID].Fill(  (jets2.jet1 + jets2.jet2).M() / 1000., t_total_weight)
                    else:
                        h_R_bl_new2b_list[topo+sampleID].Fill(-999,t_total_weight)
                        h_Asymm_bl_new2b_list[topo+sampleID].Fill( -999 ,t_total_weight)
                        h_Bjets_pT_new2b_list[topo+sampleID].Fill( -999 ,t_total_weight)
                        h_Bjet_pTsum_list[topo+sampleID].Fill(t_Bjet1_pT / 1000., t_total_weight)
                        h_m_Wh_new2b_list[topo+sampleID].Fill(-999,t_total_weight)

                    h_asymm_bl_list[topo+sampleID].Fill(t_asymm_bl, t_total_weight)
                    

                    h_bj1s_pT_orig_list [topo+sampleID] .Fill( t_Bjet1_pT / 1000., jets2.bjet1.Pt() / 1000.  , t_total_weight)
                    h_bj2s_pT_orig_list [topo+sampleID] .Fill( t_Bjet2_pT / 1000., jets2.bjet2.Pt() / 1000.  , t_total_weight)
                    h_bj1s_pT_new_list [topo+sampleID]  .Fill( t_Bjet1_pT / 1000., jets1.bjet1.Pt() / 1000.  , t_total_weight)
                    h_bj2s_pT_new_list [topo+sampleID]  .Fill( t_Bjet2_pT / 1000., jets1.bjet2.Pt() / 1000.  , t_total_weight)
                    h_bj1s_pT_new2b_list [topo+sampleID].Fill( t_Bjet1_pT / 1000., jets1.bjet1.Pt() / 1000.  , t_total_weight)


                    h_R_bl_orig_asymm_bl_list[topo+sampleID].Fill(bjetvars1.getR_bl(),t_asymm_bl,t_total_weight)
                    h_R_bl_new_asymm_bl_list[topo+sampleID].Fill(bjetvars2.getR_bl(),t_asymm_bl,t_total_weight)
                    


                    if t_Bjet2_pT == -999:
                        h_R_bl_new2b_asymm_bl_list[topo+sampleID].Fill(-999,-999,t_total_weight)
                        h_R_bl_orignew2b_list[topo+sampleID].Fill(-999,-999,t_total_weight)
                        h_bj2s_pT_new2b_list [topo+sampleID].Fill( -999, -999 , t_total_weight) 
                    else:
                        h_R_bl_orignew2b_list[topo+sampleID].Fill(bjetvars1.getR_bl(),bjetvars2.getR_bl(),t_total_weight)
                        h_R_bl_new2b_asymm_bl_list[topo+sampleID].Fill(bjetvars2.getR_bl(),t_asymm_bl,t_total_weight)
                        h_bj2s_pT_new2b_list[topo+sampleID].Fill(t_Bjet2_pT / 1000., jets1.bjet2.Pt() / 1000., t_total_weight)
                    h_R_bl_orignew_list [topo+sampleID] .Fill( bjetvars2.getR_bl(), bjetvars1.getR_bl() , t_total_weight) 

                    h_R_bl_orignewnew2b_list[topo+sampleID].Fill(bjetvars1.getR_bl(),bjetvars2.getR_bl(),bjetvars2.getR_bl(),t_total_weight)


                    h_asymm_bl_orig_list [topo+sampleID].Fill( t_asymm_bl, bjetvars2.getAsymm_bl() , t_total_weight) 
                    h_asymm_bl_new_list [topo+sampleID] .Fill( t_asymm_bl, bjetvars1.getAsymm_bl() , t_total_weight) 





        outf.cd()
        for topo in topologies:
            h_R_bl_orig_list[topo+sampleID].Write()
            h_R_bl_new_list[topo+sampleID].Write()
            h_R_bl_new2b_list[topo+sampleID].Write()

            h_Asymm_bl_orig_list[topo+sampleID].Write()
            h_Asymm_bl_new_list[topo+sampleID].Write()
            h_Asymm_bl_new2b_list[topo+sampleID].Write()

            h_Bjets_pT_orig_list[topo+sampleID].Write()
            h_Bjets_pT_new_list[topo+sampleID].Write()
            h_Bjets_pT_new2b_list[topo+sampleID].Write()

            h_asymm_bl_list[topo+sampleID].Write()
            h_Bjet_pTsum_list[topo+sampleID].Write()

            h_bj1s_pT_orig_list [topo+sampleID] .Write()
            h_bj2s_pT_orig_list [topo+sampleID] .Write()
            h_bj1s_pT_new_list [topo+sampleID]  .Write()
            h_bj2s_pT_new_list [topo+sampleID]  .Write()
            h_bj1s_pT_new2b_list [topo+sampleID].Write()
            h_bj2s_pT_new2b_list [topo+sampleID].Write()
            h_R_bl_orignew_list [topo+sampleID] .Write()
            h_asymm_bl_orig_list [topo+sampleID].Write()
            h_asymm_bl_new_list [topo+sampleID] .Write()

            h_m_Wh_orig_list[topo+sampleID].Write()
            h_m_Wh_new_list[topo+sampleID].Write()
            h_m_Wh_new2b_list[topo+sampleID].Write()

            h_R_bl_orig_asymm_bl_list[topo+sampleID].Write()
            h_R_bl_new_asymm_bl_list[topo+sampleID].Write()
            h_R_bl_new2b_asymm_bl_list[topo+sampleID].Write()

            h_R_bl_orignew2b_list[topo+sampleID].Write()
            h_R_bl_orignewnew2b_list[topo+sampleID].Write()
            


    print 'Outfile %s written' % (outf.GetName())



if __name__ == "__main__":
    main()
