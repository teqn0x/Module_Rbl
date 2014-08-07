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

    varList = ['m_Wh_orig','m_Wh_new']
    topologies = ['is2b']
    samples = ['117050','166438','166442']

    xtitle = { 'm_Wh_orig' : 'M_{jj} [GeV] (MV1)',
               'm_Wh_new'  : 'M_{jj} [GeV] (p_T)'}

    htitle = { 'm_Wh_orig' : 'M_{jj} with sorting b-jets by MV1',
               'm_Wh_new'  : 'M_{jj} with sorting b-jets by p_T'}

    legEntry = {'117050' : 'ttbar',
                '166438' : 't300_c100_n050',
                '166442' : 't350_c200_n100'}

    for var in varList:
        for topo in topologies:
            for sampleID in samples:

                print var,topo,sampleID

                hname = 'h_'+var+'_'+topo+'_'+sampleID
                histo = histoFile.Get(hname)

                histo.GetXaxis().SetTitleSize(0.035)
                histo.GetXaxis().SetTitle(xtitle[var])
                histo.SetLineWidth(2)
                histo.SetLineColor(1)

                histo.SetTitle(htitle[var])

                c = TCanvas("c"+hname[1:],"c"+hname[1:],800,600)
                histo.Draw()

                leg = TLegend(0.7,0.85,0.9,0.9)
                leg.AddEntry(histo,legEntry[sampleID],'l')
                leg.Draw()

                c.SaveAs(plotdir+hname+'.png')

if __name__ == "__main__":
    main()




                
