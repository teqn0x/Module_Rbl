#include <iostream>
#include "TLorentzVector.h"
#include "TH1.h"
#include "TFile.h"
#include "TTree.h"

int makeHistoFile(TString fileName, TString sampleID){

  gSystem->Load("bjetExtractor_cxx.so");
  gSystem->Load("bjetVariables_cxx.so");

  TFile *f = TFile::Open(fileName);
  TTree *tree = f->Get("susy");

  TFile *outf = TFile::Open("histosToCompare_"+sampleID+".root","RECREATE");

  int is2b;
  float lep1_pT,jet1_pT,jet2_pT,jet3_pT,jet4_pT;
  float lep_eta,jet1_eta,jet2_eta,jet3_eta,jet4_eta;
  float lep_phi,jet1_phi,jet2_phi,jet3_phi,jet4_phi;
  float lep_E,jet1_E,jet2_E,jet3_E,jet4_E;
  float jet1_MV1,jet2_MV1,jet3_MV1,jet4_MV1;

  double mc_event_weight;
  float ttbar_weight,Wj_sherpa_weight;
  
  tree->SetBranchAddress("lep1_pT",&lep1_pT);
  tree->SetBranchAddress("jet1_pT",&jet1_pT);
  tree->SetBranchAddress("jet2_pT",&jet2_pT);
  tree->SetBranchAddress("jet3_pT",&jet3_pT);
  tree->SetBranchAddress("jet4_pT",&jet4_pT);

  tree->SetBranchAddress("lep_eta",&lep_eta);
  tree->SetBranchAddress("jet1_eta",&jet1_eta);
  tree->SetBranchAddress("jet2_eta",&jet2_eta);
  tree->SetBranchAddress("jet3_eta",&jet3_eta);
  tree->SetBranchAddress("jet4_eta",&jet4_eta);

  tree->SetBranchAddress("lep_phi",&lep_phi);
  tree->SetBranchAddress("jet1_phi",&jet1_phi);
  tree->SetBranchAddress("jet2_phi",&jet2_phi);
  tree->SetBranchAddress("jet3_phi",&jet3_phi);
  tree->SetBranchAddress("jet4_phi",&jet4_phi);

  tree->SetBranchAddress("lep_E",&lep_E);
  tree->SetBranchAddress("jet1_E",&jet1_E);
  tree->SetBranchAddress("jet2_E",&jet2_E);
  tree->SetBranchAddress("jet3_E",&jet3_E);
  tree->SetBranchAddress("jet4_E",&jet4_E);

  tree->SetBranchAddress("jet1_MV1",&jet1_MV1);
  tree->SetBranchAddress("jet2_MV1",&jet2_MV1);
  tree->SetBranchAddress("jet3_MV1",&jet3_MV1);
  tree->SetBranchAddress("jet4_MV1",&jet4_MV1);

  tree->SetBranchAddress("is2b",&is2b);
  
  tree->SetBranchAddress("mc_event_weight",&mc_event_weight);
  tree->SetBranchAddress("ttbar_weight",&ttbar_weight);
  tree->SetBranchAddress("Wj_sherpa_weight",&Wj_sherpa_weight);


  int N = tree->GetEntries();
  TH1F *h_R_bl = new TH1F("h_R_bl_"+sampleID,"R_bl;R_bl;",30,0,1);
  
  std::cout << "Looping over file " << f->GetName() << " and TTree " << tree->GetName() << std::endl;
  std::cout << "Total number of events: " << N << std::endl;

  int step;
  if( N < 1000 ){ step = 100; }
  else if( N < 10000){ step = 1000;}
  else if( N < 100000) { step = 10000; }
  else { step = 100000; }

  for(int i = 0; i < N; i++){
    if (i % step == 0){
      if(i != 0){
	std::cout << "Event " << i << " / " << N << std::endl;
      }
    }
    
    tree->GetEntry(i);
    
    if (is2b == 0) continue;

    TLorentzVector j1,j2,j3,j4,lep;
    j1.SetPtEtaPhiE(jet1_pT,jet1_eta,jet1_phi,jet1_E);
    j2.SetPtEtaPhiE(jet2_pT,jet2_eta,jet2_phi,jet2_E);
    j3.SetPtEtaPhiE(jet3_pT,jet3_eta,jet3_phi,jet3_E);
    j4.SetPtEtaPhiE(jet4_pT,jet4_eta,jet4_phi,jet4_E);
    lep.SetPtEtaPhiE(lep1_pT,lep_eta,lep_phi,lep_E);

    bjetExtractor jets(j1,j2,j3,j4,jet1_MV1,jet2_MV1,jet3_MV1,jet4_MV1);
    bjetVariables bjetvars(jets.bjet1,jets.bjet2,jets.jet1,jets.jet2,lep);
    
    float eventWeight = mc_event_weight;
    if(ttbar_weight != -999){
      eventWeight*=ttbar_weight;
    }
    if(Wj_sherpa_weight != -999){
      eventWeight*=Wj_Sherpa_weight;
    }
    
    h_R_bl->Fill(bjetvars.getR_bl(),eventWeight);
    
  }

  outf->cd();
  h_R_bl->Write();
  
  h_R_bl->Draw();
  
  return 0;
}

