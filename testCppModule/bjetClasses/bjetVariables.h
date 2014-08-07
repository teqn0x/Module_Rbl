#ifndef _BJETVARIABLES_H_
#define _BJETVARIABLES_H_

#include <iostream>
#include "TLorentzVector.h"

class bjetVariables{
 public:
  bjetVariables(TLorentzVector bj1, TLorentzVector bj2, TLorentzVector j1, TLorentzVector j2, TLorentzVector lep);
  ~bjetVariables();

  float getR_bl() const;
  float getAsymm_bl() const;
  float getBjets_pT() const;
  
 private:
  TLorentzVector _bj1;
  TLorentzVector _bj2;
  TLorentzVector _j1;
  TLorentzVector _j2;
  TLorentzVector _lep;
};

#endif
