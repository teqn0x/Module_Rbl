import os,sys

from ROOT import *

def main():

    gROOT.SetStyle("Plain")
    gStyle.SetOptStat(0)
    gROOT.SetBatch(True)

    savePlots = True
    
    histoFile = TFile('Histos.root')
    plotdir = 'plots_tmp/'
    if not os.path.exists(plotdir):
        os.makedirs(plotdir)

    outfile = open('tmp.txt','w')
        
    #varList = ['R_bl_orig','R_bl_new','R_bl_new2b','Asymm_bl_orig','Asymm_bl_new','Asymm_bl_new2b','Bjets_pT_orig','Bjets_pT_new','Bjets_pT_new2b','asymm_bl','Bjet_pTsum','m_Wh_new','m_Wh_orig','m_Wh_new2b']
    #topologies = ['is1b','is2b','pure1b']

    varList = ['m_Wh_orig','m_Wh_new']
    topologies = ['is2b']


    bsample = ['117050']
    ssample = ['166418','166419','166420','166421','166422','166423','166424','166425','166426','166427','166428','166429','166430','166431','166432','166433','166434','166435','166436','166437','166438','166439','166440','166441','166442','166443','166444','166445','166446','166447','166448','166449','166450','166451','166452','166453','166454','166455','166456','166457','166458','166459','166460','166461','166462','166463','166464','166465','166466','166467','166468','166469','166470','166471','166472','166473','166474','166475','166476','166477','166478','166479','166480','166481','166482','166483','166484','166485','166486','166487','166488','166489','166490','166491','166492','166493','166494','166495','166496','166497','166498','166499','166500']


    for var in varList:
        for topo in topologies:
            print var,topo
            
            hname = 'h_'+var+'_'+topo+'_'

            hbkg = histoFile.Get(hname+bsample[0])
            
            if hbkg.Integral() > 0:
                hbkg.Scale(1/hbkg.Integral())
            
            for sgn in ssample:
                sampleID = sgn
                
                hsgn = histoFile.Get(hname+sgn)
                if hsgn.Integral() > 0:
                    hsgn.Scale(1/hsgn.Integral())
                    
                mx = 0
                if mx < hsgn.GetMaximum():
                    mx = hsgn.GetMaximum()
                if mx < hbkg.GetMaximum():
                    mx = hbkg.GetMaximum()
                    
                hOverlap = hsgn.Clone()
                hOverlap.SetMaximum(1.1*mx)
                hOverlap.Reset()
                hSepar = hOverlap.Clone()
                hSepar.Reset()

                obin = 0
                sbin = 0
                sgnbin = 0
                bkgbin = 0

                for ibin in range(hsgn.GetNbinsX()):
                    sgnbin = hsgn.GetBinContent(ibin)
                    bkgbin = hbkg.GetBinContent(ibin)
                    if (sgnbin != 0) and (bkgbin != 0):
                        if sgnbin < bkgbin:
                            obin = sgnbin
                        else:
                            obin = bkgbin
                        sbin = (sgnbin - bkgbin)*(sgnbin - bkgbin) / (sgnbin + bkgbin)
                        hOverlap.SetBinContent(ibin,obin)
                        hSepar.SetBinContent(ibin,sbin)
                
                #plot settings:
                hsgn.SetLineWidth(2)
                hbkg.SetLineWidth(2)
                hOverlap.SetLineWidth(2)
                
                hsgn.SetLineColor(2)
                hbkg.SetLineColor(1)
                hOverlap.SetLineColor(kAzure+4)
                hOverlap.SetFillColor(kAzure+3)
                hOverlap.SetFillStyle(3001)
                
                hbkg.SetMaximum(1.1*mx)

                c = TCanvas('c_'+hsgn.GetName(),'c',800,600)
                hbkg.Draw()
                hsgn.Draw('same')
                hOverlap.Draw('same')

                leg = TLegend (0.7,0.8,0.9,0.9)
                leg.AddEntry(hbkg,'ttbar','l')
                leg.AddEntry(hsgn,'signal %s' % (hsgn.GetName().split('_')[-1]),'l')
                leg.AddEntry(hOverlap,'Overlap','f')
                leg.Draw()
                
                tex = TLatex()
                tex.SetTextSize(0.04)
                tex.SetTextColor(kAzure+4)
                tex.SetNDC()
                tex.DrawLatex(0.4,0.91,'overlap %s, separation %s' % (hOverlap.Integral(),0.5*hSepar.Integral()) )

                #outfile.write('%s %s\n' % (sampleID,0.5*hSepar.Integral()))
                #
                # The only thing we essentially need to plot is the sampleID, variable, topology, overlap en separation, the gridPlotter macro can calculate the other variables (A-B/A+b)
                outfile.write('%s %s %s %s %s\n' % (sampleID,var,topo,hOverlap.Integral(),0.5*hSepar.Integral()))
                

                if savePlots:
                    c.SaveAs(plotdir+hsgn.GetName()+'.png')

if __name__ == "__main__":
    main()

                



                
