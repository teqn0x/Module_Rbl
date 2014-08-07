from ROOT import TLorentzVector

class bjetVariables:
    def __init__(self,bjet1,bjet2,jet1,jet2,lep):
        self.bjet1 = bjet1
        self.bjet2 = bjet2
        self.jet1 = jet1
        self.jet2 = jet2
        self.lep = lep

    def getR_bl(self):
        MW  = 80.385 * 1000
        dMW = 2.1    * 1000
        Mt  = 173.5  * 1000
        dMt = 2.0    * 1000
        

        deltaM1 = ( (MW - (self.jet1+self.jet2).M()) * (MW - (self.jet1+self.jet2).M()) ) / (dMW*dMW) +  ( (Mt - (self.jet1+self.jet2+self.bjet1).M()) * (Mt - (self.jet1+self.jet2+self.bjet1).M()) ) / (dMt*dMt)
        deltaM2 = ( (MW - (self.jet1+self.jet2).M()) * (MW - (self.jet1+self.jet2).M()) ) / (dMW*dMW) +  ( (Mt - (self.jet1+self.jet2+self.bjet2).M()) * (Mt - (self.jet1+self.jet2+self.bjet2).M()) ) / (dMt*dMt)
        
        if deltaM1 > deltaM2:
            return self.lep.Pt() / (self.bjet1.Pt() + self.lep.Pt())
        else:
            return self.lep.Pt() / (self.bjet2.Pt() + self.lep.Pt())
        
    #Asymm_bl: (even defined for a 0b case)
    def getAsymm_bl(self):
        return (self.bjet1.Pt() - self.lep.Pt()) / (self.bjet1.Pt() + self.lep.Pt())

    #Bjets_pT: (even defined for a 0b and 1b case)
    def getBjets_pT(self):
        return self.bjet1.Pt() + self.bjet2.Pt()
    
class bjetExtractor:
    #Give it the LorentzVectors of the 4 leading jets and their mv1 variables.
    def __init__(self, j1, j2, j3, j4, j1_mv1, j2_mv1, j3_mv1, j4_mv1):
      
        lv = [[j1,j1_mv1],
              [j2,j2_mv1],
              [j3,j3_mv1],
              [j4,j4_mv1]]
        
        
        self.bjet1 = TLorentzVector()
        self.bjet2 = TLorentzVector()
        self.jet1  = TLorentzVector()
        self.jet2  = TLorentzVector()
        
        #Sort by second index (mv1 variable)
        lv.sort(key = lambda ll : ll[1])
        
        if lv[0][0].Pt() > lv[1][0].Pt():
            self.jet1 = lv[0][0]
            self.jet2 = lv[1][0]
        else:
            self.jet1 = lv[1][0]
            self.jet2 = lv[0][0]

        if lv[2][0].Pt() > lv[3][0].Pt():
            self.bjet1 = lv[2][0]
            self.bjet2 = lv[3][0]
        else:
            self.bjet1 = lv[3][0]
            self.bjet2 = lv[2][0]
