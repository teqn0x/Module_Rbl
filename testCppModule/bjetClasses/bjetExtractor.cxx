#include <iostream>
#include "TLorentzVector.h"
#include "bjetExtractor.h"

bjetExtractor::bjetExtractor(TLorentzVector j1, TLorentzVector j2, TLorentzVector j3, TLorentzVector j4, float mv11, float mv12, float mv13, float mv14){
  lv[0] = j1; lv[1] = j2; lv[2] = j3; lv[3] = j4;
  mv1[0] = mv11; mv1[1] = mv12; mv1[2] = mv13; mv1[3] = mv14;
  sortByMV1(lv,mv1);
  setJets(lv);
}

bjetExtractor::~bjetExtractor() {}

void bjetExtractor::sortByMV1(TLorentzVector *v, float *mv){
  for(int i = 0; i < 4; i++){
    for(int j = 0; j < 4-1-i; j++){
      if(mv[j+1] < mv[j]){
	swap(mv[j+1],mv[j]);
	swap(v[j+1],v[j]);
      }
    }
  }
}

void bjetExtractor::swap(float &a, float &b){
    float tmp = a;
    a = b;
    b = tmp;
}

void bjetExtractor::swap(TLorentzVector &a, TLorentzVector &b){
  TLorentzVector tmp = a;
  a = b;
  b = tmp;
}
 
void bjetExtractor::setJets(TLorentzVector *v){
  if(v[0].Pt() > v[1].Pt()){
    jet1 = v[0];
    jet2 = v[1];
  } else {
    jet1 = v[1];
    jet2 = v[0];
  }
  if (v[2].Pt() > v[3].Pt()){
    bjet1 = v[2];
    bjet2 = v[3];
  } else {
    bjet1 = v[3];
    bjet2 = v[2];
  }
}



