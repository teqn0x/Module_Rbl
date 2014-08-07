#include <iostream>
#include "TLorentzVector.h"
#include "bjetVariables.h"

bjetVariables::bjetVariables(TLorentzVector bj1, TLorentzVector bj2, TLorentzVector j1, TLorentzVector j2, TLorentzVector lep){
  _bj1 = bj1;
  _bj2 = bj2;
  _j1 = j1;
  _j2 = j2;
  _lep = lep;
}

bjetVariables::~bjetVariables() {}


float bjetVariables::getR_bl() const{
  // Values taken from PDG
  const float MW  = 80.385 * 1000;
  const float dMW = 2.1    * 1000;
  const float Mt  = 173.5  * 1000;
  const float dMt = 2.0    * 1000;
  
  float deltaM1 = ( (MW - (_j1+_j2).M()) * (MW - (_j1+_j2).M()) ) / (dMW*dMW) +  ( (Mt - (_j1+_j2+_bj1).M()) * (Mt - (_j1+_j2+_bj1).M()) ) / (dMt*dMt);
  float deltaM2 = ( (MW - (_j1+_j2).M()) * (MW - (_j1+_j2).M()) ) / (dMW*dMW) +  ( (Mt - (_j1+_j2+_bj2).M()) * (Mt - (_j1+_j2+_bj2).M()) ) / (dMt*dMt);
    
  if(deltaM1 < deltaM2){
    return (_lep.Pt() / (_lep.Pt() + _bj2.Pt()) );
  } else {
    return (_lep.Pt() / (_lep.Pt() + _bj1.Pt()) );
  }
}

float bjetVariables::getAsymm_bl() const{
  return ( (_bj1.Pt() - _lep.Pt()) / (_bj1.Pt() + _lep.Pt()) );
}

float bjetVariables::getBjets_pT() const{
  return (_bj1.Pt() + _bj2.Pt());
}

