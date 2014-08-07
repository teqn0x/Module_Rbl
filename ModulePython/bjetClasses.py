#Classes to calculate R_bl variable.
#
# Class bjetExtractor: get 2 bjets (or 2 jets with the highest MV1) from the 4 leading jets
# Class bjetVariables: get R_bl (or Asymm_bl or Bjets_pT)

# Example of Use:
# 4 LorentzVectors for jets (j1,j2,j3,j4)
# 4 MV1 variables (j1_MV1,j2_MV1,j3_MV1,j4_MV1)
# 1 LorentzVector for the lepton (lep)

# jets = bjetExtractor(j1,j2,j3,j4,j1_MV1,j2_MV1,j3_MV1,j4_MV1)
# bjetvars = bjetVariables(jets.bjet1,jets.bjet2,jets.jet1,jets.jet2,lep)
# R_bl = bjetvars.getR_bl()
# Bjets_pT = bjetvars.getBjets_pT()


from ROOT import TLorentzVector

class bjetVariables:
    def __init__(self,bjet1,bjet2,jet1,jet2,lep):
        self.bjet1 = bjet1
        self.bjet2 = bjet2
        self.jet1 = jet1
        self.jet2 = jet2
        self.lep = lep

    def getR_bl(self):

        #R_bl, variable to distinguish between stop and top quark
        #R_bl = lep.pT / (bjet_pT + lep_pT) where the bjet is associated with the leptonic decaying top quark

        #Assumption: two leading jets that are not bjets form the hadronic decaying W
        
        #Values taken from PDG
        MW  = 80.385 * 1000   #W Boson mass
        dMW = 2.1    * 1000   #W Boson width
        Mt  = 173.5  * 1000   #top mass
        dMt = 2.0    * 1000   #top width

        #Calculate deltaMi = (MW - (jet1+jet2).M())^2/dMW^2 + (Mt - (jet1+jet2+bjeti).M())^2 / dMt^2, where i=1,2
        # if deltaM1 < deltaM2, then jet1, jet2 and bjet1 represent the top 'better' then jet1, jet2 and bjet2, so then R_bl = lep.Pt() / (lep.Pt() + bjet2.Pt() )
        

        deltaM1 = ( (MW - (self.jet1+self.jet2).M()) * (MW - (self.jet1+self.jet2).M()) ) / (dMW*dMW) +  ( (Mt - (self.jet1+self.jet2+self.bjet1).M()) * (Mt - (self.jet1+self.jet2+self.bjet1).M()) ) / (dMt*dMt)
        deltaM2 = ( (MW - (self.jet1+self.jet2).M()) * (MW - (self.jet1+self.jet2).M()) ) / (dMW*dMW) +  ( (Mt - (self.jet1+self.jet2+self.bjet2).M()) * (Mt - (self.jet1+self.jet2+self.bjet2).M()) ) / (dMt*dMt)
        
        if deltaM1 > deltaM2:
            return self.lep.Pt() / (self.bjet1.Pt() + self.lep.Pt())
        else:
            return self.lep.Pt() / (self.bjet2.Pt() + self.lep.Pt())
        
    #Asymm_bl: 
    def getAsymm_bl(self):
        return (self.bjet1.Pt() - self.lep.Pt()) / (self.bjet1.Pt() + self.lep.Pt())

    #Bjets_pT, scalar sum of the two bjet pT's: 
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

        #Python sorts from small to large, so lv[2] and lv[3] have larger MV1's.
        #Extracting the leading and subleading jets/bjets:
        
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
