import os,sys
from array import array

from ROOT import *

import ID2NameSamples as samples

DEFsbin = {"t125":1, "t150":2,"t180":3,"t200":4,"t225":5,"t250":6, "t275":7, "t300":8, "t350":9,"t400":10,"t450":11,"t500":12,"t550":13,"t600":14, "t650":15, "t700":16, "t750":17, "t800":18}
DEFnbin = {"n050":1,"n060":2, "n070":3, "n075":4,"n095":5,"n100":6,"n120":7, "n125":8, "n145":9, "n150":10,"n170":11, "n195":12, "n200":13, "n220": 14, "n245":15,"n250":16,"n270":17,"n295":18,"n300":19,"n320":20, "n345":21, "n350":22, "n370":23, "n395":24} 

CH150sbin = {'t160':1, 't180':2, 't200':3, 't225':3, 't250':4, 't275':5, 't300':6,'t350':7, 't400':8, 't500':9, 't600':10, 't800':11}
CH150nbin = {'n001':1, 'n025':2, 'n050':3, 'n075':4, 'n100':5, 'n140':6}

sbin    = {}
nbin    = {}

#Or settin a default here:
#sbin = DEFsbin
#nbin = DEFnbin
#????



#Would be even more general if you have clear names in DEFsbin, DEFCH150sbin etc. and use throughout the rest of the code xbin and ybin instead of sbin and nbin, same reason why I made function getBins

def getSbin(stopMass):
    for mass in sbin:
        if mass == stopMass:
            return sbin[mass]
def getNbin(neutMass):
    for mass in nbin:
        if mass == neutMass:
            return nbin[mass]

#Need this function to keep it general, certain grids don't have a stopmass / neutralino mass grid, the n001 has a stopmass / chargino grid
def getBins(gridType,sampleID):
    masses = samples.ID2Name[sampleID]
    mstop = masses.split('_')[0]
    mchar = masses.split('_')[1]
    mneut = masses.split('_')[2]

    if gridType == 0 or gridType == 1:
        return [getSbin(mstop),getNbin(mneut)]

    else:
        print '##    GRID NUMBER OPTION DOES NOT EXISTS        ##'
        print '##  IN getBins(gridType,sampleID),  EXITING NOW ##'
        sys.exit()
        

def setMassGrid(gridType):
    #Use the global variables sbin and nbin
    global sbin
    global nbin
    if gridType == 0:
        sbin = DEFsbin
        nbin = DEFnbin
    elif gridType == 1:
        sbin = CH150sbin
        nbin = CH150nbin
    else:
        print '## GRID NUMBER OPTION DOES NOT EXISTS, EXITING NOW ##'
        sys.exit()
        #or, gives a error stream instead of standard output stream:
        #raise SystemExit('Incorrect input!')

def getSampleList(dirName):
    sampleList = []
    for ifile in os.listdir(dirName):
        if '_NONE_' in ifile and not 'WimpPair' in ifile:
            sampleList.append(ifile.split('.')[1])

    return sampleList

def getGridSamples(gridType,sampleList):
    gridSamples = []
    for sampleID in sampleList:
        name = samples.ID2Name[sampleID]
        #Must be in the grids, there are to many samples in between to get a nice grid if we use all the samples:
        if gridType == 0 or gridType == 1:
            if name.split('_')[0] not in sbin: continue
            if name.split('_')[2] not in nbin: continue
        
        mstop = int(name.split('_')[0][1:])
        mchar = int(name.split('_')[1][1:])
        mneut = int(name.split('_')[2][1:])

        if gridType == 0 and mchar == 2*mneut:
            gridSamples.append(sampleID)
        if gridType ==1 and mchar == 150:
            gridSamples.append(sampleID)
 
    return gridSamples
    
def getOverlapSeparation(hsig,hbkg):
    if not hsig.Integral() == 0:
        hsig.Scale(1/hsig.Integral())
    if not hbkg.Integral == 0:
        hbkg.Scale(1/hbkg.Integral())

    if hbkg.GetMaximum() > hsig.GetMaximum():
        hOverlap = hbkg.Clone()
    else:
        hOverlap = hsig.Clone()
    hOverlap.Reset()
    hSepar = hOverlap.Clone()

    N = hOverlap.GetNbinsX()


    for ibin in range(1,N+1):
        overlapbin = 0
        sepbin = 0

        sigbin = hsig.GetBinContent(ibin)
        bkgbin = hbkg.GetBinContent(ibin)

        if not sigbin == 0 and not bkgbin == 0:
            if sigbin > bkgbin:
                overlapbin = sigbin
            else:
                overlapbin = bkgbin
            sepbin = (sigbin-bkgbin)*(sigbin-bkgbin) / (sigbin+bkgbin)

        hOverlap.SetBinContent(ibin,overlapbin)
        hSepar.SetBinContent(ibin,sepbin)

    overlap = hOverlap.Integral()
    separation = 0.5*hSepar.Integral()

    return [overlap,separation]
        
        
        

def getRatio(A,B):
    print A,B,(A-B)/(A+B)
    return (A-B)/(A+B)

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

    ##################################################
    ###
    ### DRAWING GRIDS
    ###
    ##################################################


    histoFile = TFile('Histos.root')
    plotdir = 'gridplots/'
    if not os.path.exists(plotdir):
        os.makedirs(plotdir)
        print 'Created directory: %s' % plotdir


    topologies = ['is1b','is2b','pure1b']

    #Get samplesList:
    dirName = '/glusterfs/atlas6/users/stopTeam/outputs-p15xx/outputs-p15xx-Aug17/mc-forTMVA/lepton-signal/'
    print 'Getting all sampleIDs from directory: %s' % dirName
    samplesList = getSampleList(dirName)
    

    listGrids = [0,1]
    nameGrids = {0:'mc2mn',1:'mc150'}
    titleGrids = {0:'M_{#chi^{#pm}} = 2 M_{#chi^{0}}',1:'M_{#chi^{#pm}} = 150 GeV'}
    xtitle = {0:'stop mass [GeV]',1 : 'stop mass [GeV]'}
    ytitle = {0:'neutralino mass [GeV]', 1:'neutralino mass [GeV]'}

    for gridType in listGrids:
        print 'Going through gridType: %s' % nameGrids[gridType]
        setMassGrid(gridType)

        Nsbin = len(sbin)
        Nnbin = len(nbin)

        #So the first thing I want to get of
        plotName = 'R_bl_vs_asymm_bl_grid_'+nameGrids[gridType]

        R_bl_name1 = 'h_R_bl_orig_'
        R_bl_name2 = 'h_R_bl_new_'
        R_bl_name3 = 'h_R_bl_new2b_'

        asymm_bl_name = 'h_asymm_bl_'

        h_txt = {}
        h_clr = {}

        for topo in topologies:
            #The grid histos, one for color, one for text and canvas:
            h_txt[topo] = TH2D("h_grid_txt_"+topo+"_"+nameGrids[gridType],titleGrids[gridType],Nsbin,0,Nsbin+1,Nnbin,0,Nnbin-1)
            h_clr[topo] = TH2D("h_grid_clr_"+topo+"_"+nameGrids[gridType],titleGrids[gridType],Nsbin,0,Nsbin+1,Nnbin,0,Nnbin-1)
            

        gridSamples = getGridSamples(gridType, samplesList)
        
        #Need to split this in 4 different parts, the 3 combo's in R_bl and R_bl_orig vs asymm_bl, lets just start with the R_bl_orig vs asymm_bl and test that

        #get bkg:

        listOverlapSepar_R_bl_orig = {}
        listOverlapSepar_R_bl_new = {}
        listOverlapSepar_R_bl_new2b = {}
        listOverlapSepar_asymm_bl = {}
        
        for topo in topologies:
            hbkg = histoFile.Get(R_bl_name1+topo+'_117050')
            for sampleID in gridSamples:
                hsig1 = histoFile.Get(R_bl_name1+topo+'_'+sampleID)
                hsig2 = histoFile.Get(R_bl_name2+topo+'_'+sampleID)
                hsig3 = histoFile.Get(R_bl_name3+topo+'_'+sampleID)
                hsig4 = histoFile.Get(asymm_bl_name+topo+'_'+sampleID)

                listOverlapSepar_R_bl_orig[sampleID] = getOverlapSeparation(hsig1,hbkg)
                listOverlapSepar_R_bl_new[sampleID] = getOverlapSeparation(hsig2,hbkg)
                listOverlapSepar_R_bl_new2b[sampleID] = getOverlapSeparation(hsig3,hbkg)
                listOverlapSepar_asymm_bl[sampleID] = getOverlapSeparation(hsig4,hbkg)

        for topo in topologies:
            #Now Set the bin contents of the color one to -999:
            for ibin in range(Nsbin):
                for jbin in range(Nnbin):
                    h_clr[topo].SetBinContent(ibin+1,jbin+1,-999)

            #Set bin contents for clr and txt correctly and save the mininmum and maximum for the color grid:
            maxbin = -10
            minbin =  10

            
            for sampleID in gridSamples:
                bins = getBins(gridType,sampleID)
                bincon = getRatio(listOverlapSepar_R_bl_orig[sampleID][1],listOverlapSepar_asymm_bl[sampleID][1])
                if bincon > maxbin:
                    maxbin = bincon
                if bincon < minbin:
                    minbin = bincon
                    
                h_txt[topo].SetBinContent(bins[0],bins[1],bincon)
                h_clr[topo].SetBinContent(bins[0],bins[1],bincon)


            if minbin < 0:
                h_clr[topo].SetMinimum(1.1*minbin)
            else:
                h_clr[topo].SetMinimum(0.9*minbin)
            if maxbin > 0:
                h_clr[topo].SetMaximum(1.1*maxbin)
            else:
                h_clr[topo].SetMaximum(0.9*maxbin)

            #label settings:
            for stopmass in sbin:
                h_clr[topo].GetXaxis().SetBinLabel(getSbin(stopmass),stopmass[1:])
            for neutmass in nbin:
                h_clr[topo].GetYaxis().SetBinLabel(getNbin(neutmass),neutmass[1:])

            
            h_clr[topo].GetXaxis().SetTitle(xtitle[gridType])
            h_clr[topo].GetYaxis().SetTitle(ytitle[gridType])

            c = TCanvas("c_"+topo+"_"+nameGrids[gridType],titleGrids[gridType],800,600)
            
            h_clr[topo].Draw("COLZ")
            h_txt[topo].Draw("textsames")

            c.SaveAs(plotdir+'R_bl_vs_asymm_bl_grid_'+topo+'_'+nameGrids[gridType]+'.png')
            

if __name__ == "__main__":
    main()
            
            
                
                                                                                         

        

        
