import os, sys

from ROOT import *

def getFilesList(dirName):
    filesList = []
    for ifile in os.listdir(dirName):
        filesList.append(ifile)
    filesList.sort()
    return filesList

def getMax(h1,h2):
    if h1.GetMaximum() > h2.GetMaximum():
        return h1.GetMaximum()
    else:
        return h2.GetMaximum()
        

def main():

    gROOT.SetStyle("Plain")
    gStyle.SetOptStat(0)
    gROOT.SetBatch(True)

    dir = 'rootFiles/'
    filesList = getFilesList(dir)
    
    ssample = ['166434','166454']
    bsample = ['105861']
    

    for ifile in filesList:
        print 'Processing %s' % ifile
        histoFile = TFile.Open(dir+ifile)
        method = ifile.split('.')[1]

        hname = 'h_R_bl_'
        
        hbkg = histoFile.Get(hname+bsample[0])
        hsig = []
        for sampleID in ssample:
            hsig.append(histoFile.Get(hname+sampleID))
            
        #all normalize to 1
        if not hbkg.Integral() == 0:
            hbkg.Scale(1/hbkg.Integral())
        for histo in hsig:
            if not histo.Integral == 0:
                histo.Scale(1/histo.Integral())
                
        #Only make the overlap plots

        for histo in hsig:
            max = getMax(histo,hbkg)
            hOverlap = hbkg.Clone()
            hOverlap.SetMaximum(1.1*max)
            hSepar = hOverlap.Clone()

            Nbins = hbkg.GetNbinsX()
            
            
            for ibin in range(Nbins):
                obin = 0
                sbin = 0
                sigbin = histo.GetBinContent(ibin)
                bkgbin = hbkg.GetBinContent(ibin)
                if sigbin != 0 and bkgbin != 0:
                    if sigbin > bkgbin:
                        obin = bkgbin
                    else:
                        obin = sigbin
                    sbin = (sigbin - bkgbin) * (sigbin - bkgbin) / (sigbin + bkgbin)
                hOverlap.SetBinContent(ibin,obin)
                hSepar.SetBinContent(ibin,sbin)

            c = TCanvas('c_'+method+'_'+histo.GetName().split('_')[-1],'Histogram R_bl for method %s and signal %s'%(method,histo.GetName().split('_')[-1]),800,600)
            hbkg.SetLineWidth(2)
            hbkg.SetLineColor(1)

            histo.SetLineWidth(2)
            histo.SetLineColor(2)
            
            hOverlap.SetLineWidth(2)
            hOverlap.SetLineColor(kAzure+3)
            hOverlap.SetFillColor(kAzure+4)
            hOverlap.SetFillStyle(3001)
            hOverlap.SetTitle("R_bl")
            hOverlap.GetXaxis().SetTitle("R_bl")
            hOverlap.GetXaxis().SetTitleSize(0.035)

            hOverlap.Draw()
            hbkg.Draw('same')
            histo.Draw('same')

            leg = TLegend(0.7,0.8,0.9,0.9)
            leg.AddEntry(hbkg,'ttbar','l')
            leg.AddEntry(histo,sampleID,'l')
            leg.AddEntry(hOverlap,'overlap','f')
            leg.Draw()

            tex = TLatex()
            tex.SetTextSize(0.025)
            tex.SetTextColor(kAzure+4)
            tex.SetNDC()
            tex.DrawLatex(0.7,0.75,'overlap = %s'%hOverlap.Integral())
            tex.DrawLatex(0.7,0.7 ,'separation = %s'%(0.5*hSepar.Integral()))

            c.SaveAs('plots/overlap_'+method+'_'+histo.GetName().split('_')[-1]+'.png')
            

if __name__ == "__main__":
    main()
            
            

                
                        
    
