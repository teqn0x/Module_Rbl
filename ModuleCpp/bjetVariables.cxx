#include <iostream>
#include "TLorentzVector.h"
#include "bjetVariables.h"

// Constructor, taking 5 LorentzVectors (2 bjets, 2 jets and the lepton)
bjetVariables::bjetVariables(TLorentzVector bj1, TLorentzVector bj2, TLorentzVector j1, TLorentzVector j2, TLorentzVector lep){
  _bj1 = bj1;
  _bj2 = bj2;
  _j1 = j1;
  _j2 = j2;
  _lep = lep;
}

// Destructor
bjetVariables::~bjetVariables() {}

// R_bl, variable to distinguish between stop and top quark
// R_bl = lep.pT / (bjet_pT + lep_pT) where the bjet is associated with the leptonic decaying top quark
// 
// Assumption: two leading jets that are not bjets form the hadronic decaying W

float bjetVariables::getR_bl() const{
  // Values taken from PDG
  const float MW  = 80.385 * 1000;
  const float dMW = 2.1    * 1000;
  const float Mt  = 173.5  * 1000;
  const float dMt = 2.0    * 1000;

// Calculate deltaMi = (MW - (jet1+jet2).M())^2/dMW^2 + (Mt - (jet1+jet2+bjeti).M())^2 / dMt^2, where i=1,2
// if deltaM1 < deltaM2, then jet1, jet2 and bjet1 represent the top 'better' then jet1, jet2 and bjet2, so then R_bl = lep.Pt() / (lep.Pt() + bjet2.Pt() )
  
  float deltaM1 = ( (MW - (_j1+_j2).M()) * (MW - (_j1+_j2).M()) ) / (dMW*dMW) +  ( (Mt - (_j1+_j2+_bj1).M()) * (Mt - (_j1+_j2+_bj1).M()) ) / (dMt*dMt);
  float deltaM2 = ( (MW - (_j1+_j2).M()) * (MW - (_j1+_j2).M()) ) / (dMW*dMW) +  ( (Mt - (_j1+_j2+_bj2).M()) * (Mt - (_j1+_j2+_bj2).M()) ) / (dMt*dMt);
    
  if(deltaM1 < deltaM2){
    return (_lep.Pt() / (_lep.Pt() + _bj2.Pt()) );
  } else {
    return (_lep.Pt() / (_lep.Pt() + _bj1.Pt()) );
  }
}

//Asymm_bl:
float bjetVariables::getAsymm_bl() const{
  return ( (_bj1.Pt() - _lep.Pt()) / (_bj1.Pt() + _lep.Pt()) );
}

//Bjets_pT, the scalar sum of the two bjet pT's
float bjetVariables::getBjets_pT() const{
  return (_bj1.Pt() + _bj2.Pt());
}

