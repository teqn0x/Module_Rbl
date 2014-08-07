import os,sys

from array import array
from ROOT import *
from samples import ID2Name

DEFsbin = {"t125":1, "t150":2,"t180":3,"t200":4,"t225":5,"t250":6, "t275":7, "t300":8, "t350":9,"t400":10,"t450":11,"t500":12,"t550":13,"t600":14, "t650":15, "t700":16, "t750":17, "t800":18}
DEFnbin = {"n050":1,"n060":2, "n070":3, "n075":4,"n095":5,"n100":6,"n120":7, "n125":8, "n145":9, "n150":10,"n170":11, "n195":12, "n200":13, "n220": 14, "n245":15,"n250":16,"n270":17,"n295":18,"n300":19,"n320":20, "n345":21, "n350":22, "n370":23, "n395":24} 

CH150sbin = {'t160':1, 't180':2, 't200':3, 't225':3, 't250':4, 't275':5, 't300':6,'t350':7, 't400':8, 't500':9, 't600':10, 't800':11}
CH150nbin = {'n001':1, 'n025':2, 'n050':3, 'n075':4, 'n100':5, 'n140':6} #Maybe add a few bins here, just to create space to print text

xbin    = {}
ybin    = {}

#setting the mass grid:
def setMassGrid(gridType):
    global xbin
    global ybin
    if gridType == 0:
        xbin = DEFsbin
        ybin = DEFnbin
    elif gridType == 1:
        xbin = CH150sbin
        ybin = CH150nbin
    else:
        sys.exit('Wrong grid type given in setMassGrid(gridType)')



#Getting the bin numbers by mass:

def getXbin(stopMass):
    for mass in xbin:
        if mass == stopMass:
            return xbin[mass]
def getYbin(neutMass):
    for mass in ybin:
        if mass == neutMass:
            return ybin[mass]

def getXmass(ibin):
    for x in xbin:
        if xbin[x] == ibin:
            return x

def getYmass(ibin):
    for y in ybin:
        if ybin[y] == ibin:
            return y

def getBins(gridType,sampleID):
    masses = ID2Name[sampleID]
    mstop = masses.split('_')[0]
    mchar = masses.split('_')[1]
    mneut = masses.split('_')[2]
    if gridType == 0 or gridType == 1:
        return [getXbin(mstop),getYbin(mneut)]

    else:
        sys.exit('Wrong grid type given in getBins(gridType,sampleID)')

        
def getGridSamples(gridType,sampleList):
    gridSamples = []

        
    for sampleID in sampleList:
        masses = ID2Name[sampleID]
        if masses.split('_')[0] not in xbin: continue
        if masses.split('_')[2] not in ybin: continue


        mstop = int(masses.split('_')[0][1:])
        mchar = int(masses.split('_')[1][1:])
        mneut = int(masses.split('_')[2][1:])

        if gridType == 0 and mchar == 2*mneut:
            gridSamples.append(sampleID)
        if gridType == 1 and mchar == 150:
            gridSamples.append(sampleID)

    return gridSamples


def optParser():
    from optparse import OptionParser
    parser = OptionParser()

    parser.add_option('--grid', dest= 'grid', help='Grid type, 0: mc = 2*mn, 1: mc = 150GeV', default = 0, type = 'int')
    parser.add_option('--var1', dest= 'var1', help='First variables we want to plot', default = '')
    parser.add_option('--var2', dest= 'var2', help='Second variable, makes ratio plot', default = '')
    parser.add_option('--topo', dest= 'topo', help='Topology, 1->is1b, 2->is2b', default = 1, type = 'int')
    parser.add_option('--type', dest= 'type', help='Overlap(1) of Separation(0)?',default = 0, type = 'int')

    (config, sys.argv[1:]) = parser.parse_args(sys.argv[1:])

    return config

def main():

    ######################################################
    ###
    ###   ROOT SETTINGS
    ###
    ######################################################
    gStyle.SetOptStat(0)
    gROOT.SetBatch(True)

    icol=0
    gStyle.SetFrameBorderMode(icol)
    gStyle.SetFrameFillColor(icol)
    gStyle.SetCanvasBorderMode(icol)
    gStyle.SetCanvasColor(icol)
    gStyle.SetPadBorderMode(icol)
    gStyle.SetPadColor(icol)
    gStyle.SetStatColor(icol)
    gStyle.SetPaperSize(20,26)
    gStyle.SetPadTopMargin(0.05)
    gStyle.SetPadRightMargin(0.15)
    gStyle.SetPadBottomMargin(0.16)
    gStyle.SetPadLeftMargin(0.16)
    gStyle.SetTitleXOffset(1.4)
    gStyle.SetTitleYOffset(1.3)

    font=42
    tsize=0.05
    gStyle.SetTextFont(font)
    gStyle.SetTextSize(tsize)
    gStyle.SetLabelFont(font,"x")
    gStyle.SetTitleFont(font,"x")
    gStyle.SetLabelFont(font,"y")
    gStyle.SetTitleFont(font,"y")
    gStyle.SetLabelFont(font,"z")
    gStyle.SetTitleFont(font,"z")
    gStyle.SetLabelSize(tsize,"x")
    gStyle.SetTitleSize(tsize,"x")
    gStyle.SetLabelSize(tsize,"y")
    gStyle.SetTitleSize(tsize,"y")
    gStyle.SetLabelSize(tsize,"z")
    gStyle.SetTitleSize(tsize,"z")
    gStyle.SetMarkerStyle(20)
    gStyle.SetMarkerSize(1.2)
    gStyle.SetHistLineWidth(2)
    gStyle.SetLineStyleString(2,"[12 12]")
    gStyle.SetEndErrorSize(0.)
    gStyle.SetOptTitle(0)
    gStyle.SetOptFit(0)
    gStyle.SetPadTickX(1)
    gStyle.SetPadTickY(1)


    
    fPaletteColor = array('i', [51, 52, 53, 54, 55, 56, 57, 58, 59,
                                60, 61, 62, 63, 64, 65, 66, 67, 68, 69,
                                70, 71, 72, 73, 74, 75, 76, 77, 78, 79,
                                80, 81, 82, 83, 84, 85, 86, 87, 88, 89,
                                90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100])
    
    gStyle.SetPalette(50, fPaletteColor);
    gStyle.SetPaintTextFormat(".2f")                                                                  


    ################
    ### making the plots:
    ################

    config = optParser()
    gridType = config.grid
    variable1 = config.var1
    variable2 = config.var2
    topology = config.topo
    if topology == 1:
        topology = 'is1b'
    elif topology == 2:
        topology = 'is2b'
    else:
        topology = 'is1b' #default setting
    plotType = config.type
    getSepar = True
    getOverlap = False
    if plotType == 1:
        getSepar = False
        getOverlap = True
    else:
        getSepar = True   #default settings
        getOverlap = False
        
    if variable1 == '':
        sys.exit('Give a variable name')
    ratioPlot = True
    if variable2 == '':
        ratioPlot = False

    plotSaveName = 'massgrid_'+variable1+'_'
    if not variable2 == '':
        plotSaveName+=variable2+'_'
    plotSaveName+=topology+'_'

    if getSepar:
        plotSaveName+='Separation_'
    else:
        plotSaveName+='Overlap_'

    if gridType == 0:
        plotSaveName+='mc2mn.png'
    elif gridType == 0:
        plotSaveName+='mc150.png'
        
        
    setMassGrid(gridType)
    
    infile = open('binContents.txt')

    #histogram axis titles etc:
    xtitle = {0 : '#tilde{t} mass [GeV]', 1 : '#tilde{t} mass [GeV]'}
    ytitle = {0 : '#tilde{#chi}_{1}^{0} mass [GeV]', 1 : '#tidle{#chi}_{1}^{0} mass [Gev]'}

    varTitle = {'R_bl_orig':'R_bl(MV1)',
                'R_bl_new' :'R_bl(pT)',
                'Asymm_bl_orig':'asymm_bl(MV1)',
                'Asymm_bl_new':'asymm_bl'}


    additionalHistoTitle = ''
    if variable2 == '':
        if variable1 in varTitle:
            additionalHistoTitle = '%s %s' % (topology,varTitle[variable1])
        else:
            additionalHistoTitle = '%s %s' % (topology,variable1)
    else:
        additionalHistoTitle = '%s  ' % topology
        if variable1 in varTitle:
            additionalHistoTitle+='A = %s   ' % varTitle[variable1]
        else:
            additionalHistoTitle+='A = %s   ' % variable1

        if variable2 in varTitle:
            additionalHistoTitle+='B = %s   ' % varTitle[variable2]
        else:
            additionalHistoTitle+='B = %s   ' % variable2

        
    histoTitle = {0 : 'M_{#chi_{1}^{#pm}} = 2M_{#chi_{1}^{0}} '+additionalHistoTitle, 1 : 'M_{#chi_{1}^{#pm}} = 150 GeV '+additionalHistoTitle}

    samplesList = []
    overlap = {}
    separ = {}
    #Dict keys: sampleID+var+topo
    for line in infile:
        line = line.split()
        sampleID = line[0]
        var = line[1]
        topo = line[2]
        bin_overlap = line[3]
        bin_separ = line[4]

        samplesList.append(sampleID)
        overlap[sampleID+var+topo] = float(bin_overlap)
        separ[sampleID+var+topo] = float(bin_separ)

    gridSamples = getGridSamples(gridType,samplesList)

    #Calculation of the bincontents:
    binContent = {}
    for sampleID in gridSamples:
        if ratioPlot:
            if getOverlap:
                A = overlap[sampleID+variable1+topology]
                B = overlap[sampleID+variable2+topology]
            if getSepar:
                A = separ[sampleID+variable1+topology]
                B = separ[sampleID+variable2+topology]
            binContent[sampleID] = (A-B)/(A+B)
        else:
            if getOverlap:
                binContent[sampleID] = overlap[sampleID+variable1+topology]
            if getSepar:
                binContent[sampleID] = separ[sampleID+variable1+topology]
        

    nx = len(xbin)
    ny = len(ybin)

    histo = TH2F('massgrid','',nx,0,nx,ny,0,ny)

    ##Setting up the axis:
    for x in xbin:
        histo.GetXaxis().SetBinLabel(xbin[x],x[1:])
    for y in ybin:
        histo.GetYaxis().SetBinLabel(ybin[y],y[1:])


    colHisto = histo.Clone()
    for i in range(histo.GetNbinsX()):
        for j in range(histo.GetNbinsY()):
            colHisto.SetBinContent(i+1,j+1,-999)

    mx = -1e99
    mn = 1e99
        
    for sampleID in gridSamples:
        bins = getBins(gridType,sampleID)
        #print bins, binContent[sampleID]
        histo.SetBinContent(bins[0],bins[1],binContent[sampleID])
        colHisto.SetBinContent(bins[0],bins[1],binContent[sampleID])

        if mx < binContent[sampleID]:
            mx = binContent[sampleID]
        if mn > binContent[sampleID]:
            mn = binContent[sampleID]

    if mx > 0:
        mx = 1.05*mx
    if mx < 0:
        mx = 0.95*mx
        
    if mn < 0:
        mn = 1.05*mn
    if mn > 0:
        mn = 0.95*mn

    colHisto.SetMaximum(mx)
    colHisto.SetMinimum(mn)
        
    c = TCanvas("grid","grid",1200,800)
    

    histo.GetXaxis().SetTitle(xtitle[gridType])
    histo.GetYaxis().SetTitle(ytitle[gridType])
    histo.SetTitle(histoTitle[gridType])

    colHisto.Draw("colz")
    histo.Draw("text same")

    latex = TLatex()
    latex.SetTextColor(1)
    latex.SetTextFont(font)
    latex.SetTextSize(0.035)
    latex.SetNDC()

    latex.DrawLatex(0.2,0.85,histoTitle[gridType])
    if getSepar:
        if ratioPlot:
            latex.DrawLatex(0.2,0.8,'Ratio (A-B / A+B)with separation per signal sample')
        else:
            latex.DrawLatex(0.2,0.8,'Separation per signal sample')
    if getOverlap:
        if ratioPlot:
            latex.DrawLatex(0.2,0.8,'Ratio (A-B / A+B) with overlap per signal sample')
        else:
            latex.DrawLatex(0.2,0.8,'Overlap per signal sample')

    c.SaveAs(plotSaveName)
    
if __name__ == "__main__":
    main()
    
