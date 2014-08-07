#include <iostream>
#include "TTree.h"
#include "TFile.h"
#include "TRandom3.h"


int makeTree(int nEvents=100,TString subTitle=""){

  std::cout << "Code making dummy.root containing the following branches:" << std::endl;
  std::cout << "--------------------" << std::endl;
  std::cout << "Total number of events" << std::endl;
  std::cout << "generated: " << nEvents << std::endl;
  
  if(subTitle != ""){
    TFile f("dummy."+subTitle+".root","RECREATE");
  } else {
    TFile f("dummy.root","RECREATE");
  }
  TTree tree("susy","Dummy TTree");

  int is2b;
  float lep1_pT, jet1_pT, jet2_pT, jet3_pT, jet4_pT;
  float lep_eta, jet1_eta, jet2_eta, jet3_eta, jet4_eta;
  float lep_phi, jet1_phi, jet2_phi, jet3_phi, jet4_phi;
  float lep_E, jet1_E, jet2_E, jet3_E, jet4_E;
  float jet1_MV1, jet2_MV1, jet3_MV1, jet4_MV1;
  
  float r;
  
  //Setting branches:
  tree.Branch("is2b",&is2b,"is2b/I");

  tree.Branch("lep1_pT",&lep1_pT,"lep1_pT/F");
  tree.Branch("jet1_pT",&jet1_pT,"jet1_pT/F");
  tree.Branch("jet2_pT",&jet2_pT,"jet2_pT/F");
  tree.Branch("jet3_pT",&jet3_pT,"jet3_pT/F");
  tree.Branch("jet4_pT",&jet4_pT,"jet4_pT/F");

  tree.Branch("lep_eta",&lep_eta,"lep_eta/F");
  tree.Branch("jet1_eta",&jet1_eta,"jet1_eta/F");
  tree.Branch("jet2_eta",&jet2_eta,"jet2_eta/F");
  tree.Branch("jet3_eta",&jet3_eta,"jet3_eta/F");
  tree.Branch("jet4_eta",&jet4_eta,"jet4_eta/F");
  
  tree.Branch("lep_phi",&lep_phi,"lep_phi/F");
  tree.Branch("jet1_phi",&jet1_phi,"jet1_phi/F");
  tree.Branch("jet2_phi",&jet2_phi,"jet2_phi/F");
  tree.Branch("jet3_phi",&jet3_phi,"jet3_phi/F");
  tree.Branch("jet4_phi",&jet4_phi,"jet4_phi/F");

  tree.Branch("lep_E",&lep_E,"lep_E/F");
  tree.Branch("jet1_E",&jet1_E,"jet1_E/F");
  tree.Branch("jet2_E",&jet2_E,"jet2_E/F");
  tree.Branch("jet3_E",&jet3_E,"jet3_E/F");
  tree.Branch("jet4_E",&jet4_E,"jet4_E/F");

  tree.Branch("jet1_MV1",&jet1_MV1,"jet1_MV1/F");
  tree.Branch("jet2_MV1",&jet2_MV1,"jet2_MV1/F");
  tree.Branch("jet3_MV1",&jet3_MV1,"jet3_MV1/F");
  tree.Branch("jet4_MV1",&jet4_MV1,"jet4_MV1/F");

  
  
  gRandom = new TRandom3(); //gRandom->Rndm() for random number

  for(int i = 0; i < nEvents; i++){
    
    if (i % 1000 == 0){
      std::cout << "Generating event " << i << std::endl;
    }
    
    r = gRandom->Rndm();
    if(r < 0.5){ is2b = 0; } else { is2b = 1; }
    
    gRandom->Rannor(lep1_pT,lep_E);
    gRandom->Rannor(jet1_pT,jet1_E);
    gRandom->Rannor(jet2_pT,jet2_E);
    gRandom->Rannor(jet3_pT,jet3_E);
    gRandom->Rannor(jet4_pT,jet4_E);
    
    lep1_pT *= lep1_pT;  lep_E *= lep_E;
    jet1_pT *= jet1_pT;  jet1_E *= jet1_E;
    jet2_pT *= jet2_pT;  jet2_E *= jet2_E;
    jet3_pT *= jet3_pT;  jet3_E *= jet3_E;
    jet4_pT *= jet4_pT;  jet4_E *= jet4_E;

    lep_eta = ( gRandom->Rndm()-0.5 ) * 5;
    jet1_eta = ( gRandom->Rndm()-0.5 ) * 5;
    jet2_eta = ( gRandom->Rndm()-0.5 ) * 5;
    jet3_eta = ( gRandom->Rndm()-0.5 ) * 5;
    jet4_eta = ( gRandom->Rndm()-0.5 ) * 5;
    
    lep_phi = (gRandom->Rndm()-0.5 ) * TMath::Pi();
    jet1_phi = (gRandom->Rndm()-0.5 ) * TMath::Pi();
    jet2_phi = (gRandom->Rndm()-0.5 ) * TMath::Pi();
    jet3_phi = (gRandom->Rndm()-0.5 ) * TMath::Pi();
    jet4_phi = (gRandom->Rndm()-0.5 ) * TMath::Pi();
    
    jet1_MV1 = gRandom->Rndm();
    jet2_MV1 = gRandom->Rndm();
    jet3_MV1 = gRandom->Rndm();
    jet4_MV1 = gRandom->Rndm();
    
    tree.Fill();
  }

  tree.Write();
  
  std::cout << "TTree " << tree.GetName() << " created and written on " << f.GetName() << std::endl;

  return 0;

}
  
  


