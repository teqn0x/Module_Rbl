#ifndef _BJETEXTRACTOR_H_
#define _BJETEXTRACTOR_H_

#include <iostream>
#include "TLorentzVector.h"

class bjetExtractor{

 public:
  bjetExtractor(TLorentzVector j1, TLorentzVector j2, TLorentzVector j3, TLorentzVector j4, float mv11, float mv12, float mv13, float mv14);

  ~bjetExtractor();

  void sortByMV1(TLorentzVector *v, float*mv);
  void swap(float &a, float &b);
  void swap(TLorentzVector &a, TLorentzVector &b);
  
  void setJets(TLorentzVector *v);

  TLorentzVector bjet1;
  TLorentzVector bjet2;
  TLorentzVector jet1;
  TLorentzVector jet2;

 private:
  float mv1[4];
  TLorentzVector lv[4];
  
};

#endif
