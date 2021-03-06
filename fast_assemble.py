##
## This is the powerhouse file that opens the files, stacks the
## respective data from the files (its attributes), then calls for
## histogram fits, pulls the fits and statistics, and then packages
## it into readable and small files.
##
## Running as of 08/19/2015
##


import ROOT as rt
import sys, random, math
import time
import os
import numpy as np

import stackNfit as snf

#opens the files for the barrel
def openEB(filename, fileList, runinfo, startfilepos, endfilepos, entries, histList1, histList2, transList1, transList2):
    rTree = rt.TChain("Tree_Optim")
    for k in range(startfilepos, endfilepos):
        if filename in fileList[k]:
            rTree.Add(fileList[k])
            print "successfully cut branch from " + fileList[k]
            #Saving run info in tuple list
            runinfo = np.vstack((runinfo, [fileList[k]]))

    #fills the histogram with data
    if isinstance(histList1[0],list) == True: #Individual barrel crystals
        if histList2 !=0:
            histList1, histList2, transList1, transList2 = snf.stackTime(rTree, entries, histList1, histList2, 1, 0, transList1,transList2, 0, 0)
        else:
            histList1, transList1 = snf.stackTime(rTree, entries, histList1, 0, 0, 0, transList1, 0, 0, 0)
        
    else: #eta baby eta
        if histList2!=0:
            histList1, histList2, transList1, transList2 = snf.stackTimeEta(rTree, entries, histList1, histList2, transList1, transList2)
        else:
            histList1, transList1 = snf.stackTimeEta(rTree, entries, histList1, 0, transList1, 0)
    return runinfo

#opens the files for the barrel
def openEE(filename, fileList, runinfo, startfilepos, endfilepos, entries, histListp1, histListm1, histListp2, histListm2, transListp1, transListm1, transListp2, transListm2):
    rTree = rt.TChain("Tree_Optim")
    for k in range(startfilepos, endfilepos):
        if filename in fileList[k]:
            rTree.Add(fileList[k])
            print "successfully cut branch from " + fileList[k]
            #Saving run info in tuple list
            runinfo = np.vstack((runinfo, [fileList[k]]))

    #fills the histogram with data
    if histListm2 != 0: #Differentiating photon 1 and 2
        histListp1, histListm1, histListp2, histListm2, transListp1, transListm1, transListp2, transListm2 = snf.stackTime(rTree, entries, histListp1, histListm1, histListp2, histListm2, transListp1, transListm1, transListp2, transListm2)
    else:   #Combine photon 1 and 2
        histListp1, histListm1, transListp1, transListm1 = snf.stackTime(rTree, entries, histListp1, histListm1, 0, 0, transListp1, transListm1, 0, 0)
    return runinfo


#opens the files for the barrel
def openMass(filename, fileList, runinfo, startfilepos, endfilepos, entries, histList, histRun):
    rTree = rt.TChain("Tree_Optim")
    for k in range(startfilepos, endfilepos):
        if filename in fileList[k]:
            rTree.Add(fileList[k])
            print "successfully cut branch from " + fileList[k]
            #Saving run info in tuple list
            runinfo = np.vstack((runinfo, [fileList[k]]))

            #makes the histogram for pi0 mass
            histname = "Average Pi0 mass in Barrel for time instance (%s)" %(fileList[k])
            histtitle = "Pi0 mass (GeV) for ROOT file cluster (%s)" %(fileList[k])
            histmass = rt.TH1F(histname,histtitle,1000,0,1)
            
            #fills the mass histogram list with ROOT files oriented folder
            histmass = snf.stackMass(rTree,histmass)
            histList.append(copy.copy(histmass))
            
            #Fills large histogram for the entire run's dataset
            histRun = snf.stackMass(rTree,histRun)
    
    return runinfo, histList, histrun



#saves the histograms, fits, and others for the barrel
def saveEB(runNumber, dataList1, dataList2, histList1, histList2, transList1, transList2, htime1, htime2, hlaser1, hlaser2, fitdata1, fitdata2, seedmap1, seedmap2):
    if isinstance(histList1[0],list) == True: #Individual barrel crystals
        if histList2 !=0:
            f = rt.TFile("IndivTimeEB_p1_" + runNumber + ".root","new")
            for eta in range(0,len(histList1)):
                for phi in range(0, len(histList1[0])):
                    histList1[eta][phi].Write()
                    transList1[eta][phi].Write()
                    #Saving value of data in tuple list
                    dataList1 = np.append(dataList1, [0, eta-85, phi, fitdata1[eta][phi][0],fitdata1[eta][phi][1],fitdata1[eta][phi][2],fitdata1[eta][phi][3],fitdata1[eta][phi][4],fitdata1[eta][phi][5],fitdata1[eta][phi][6]])
            htime1.Write()
            hlaser1.Write()
            if seedmap1 != 0:
                seedmap1.Write()
            f.Close()

            f2 = rt.TFile("IndivTimeEB_p2_" + runNumber + ".root","new")
            for eta in range(0,len(histList2)):
                for phi in range(0, len(histList2[0])):
                    histList2[eta][phi].Write()
                    transList2[eta][phi].Write()
                    #Saving value of data in tuple list
                    dataList2 = np.append(dataList2, [0, eta-85, phi, fitdata2[eta][phi][0],fitdata2[eta][phi][1],fitdata2[eta][phi][2],fitdata2[eta][phi][3],fitdata2[eta][phi][4],fitdata2[eta][phi][5],fitdata1[eta][phi][6]])
            htime2.Write()
            hlaser2.Write()
            if seedmap1 != 0:
                seedmap2.Write()
            f2.Close()
    
            dataList1.shape = (171,361,10)
            dataList2.shape = (171,361,10)
            np.save("dataEB_p1_" + runNumber + ".npy", dataList1)
            np.save("dataEB_p2_" + runNumber + ".npy", dataList2)
        else:
            #saving all 1D histograms in tree
            f = rt.TFile("IndivTimeEB_c_" + runNumber + ".root","new")
            for eta in range(0,len(histList1)):
                for phi in range(0, len(histList1[0])):
                    histList1[eta][phi].Write()
                    transList1[eta][phi].Write()
                    #Saving value of data in tuple list
                    dataList1 = np.append(dataList1, [0, eta-85, phi, fitdata1[eta][phi][0],fitdata1[eta][phi][1],fitdata1[eta][phi][2],fitdata1[eta][phi][3],fitdata1[eta][phi][4],fitdata1[eta][phi][5],fitdata1[eta][phi][6]])
            htime1.Write()
            hlaser1.Write()
            if seedmap1 != 0:
                seedmap1.Write()
            f.Close()

            dataList1.shape = (171,361,10)
            np.save("dataEB_c_" + runNumber + ".npy", dataList1)
    else: #clustertimeEB
        if histList2 !=0:
            f = rt.TFile("ClusterTimeEB_p1_" + runNumber + ".root","new")
            for eta in range(0,len(histList1)):
                histList1[eta].Write()
                transList1[eta].Write()
                #Saving value of data in tuple list
                dataList1 = np.append(dataList1, [0, eta-85, fitdata1[eta][0],fitdata1[eta][1],fitdata1[eta][2],fitdata1[eta][3],fitdata1[eta][4],fitdata1[eta][5],fitdata1[eta][6]])
            htime1.Write()
            hlaser1.Write()
            if seedmap1 != 0:
                seedmap1.Write()
            f.Close()
        
            f2 = rt.TFile("ClusterTimeEB_p2_" + runNumber + ".root","new")
            for eta in range(0,len(histList2)):
                histList2[eta].Write()
                transList2[eta].Write()
                #Saving value of data in tuple list
                dataList2 = np.append(dataList2, [0, eta-85, fitdata2[eta][0],fitdata2[eta][1],fitdata2[eta][2],fitdata2[eta][3],fitdata2[eta][4],fitdata2[eta][5],fitdata1[eta][6]])
            htime2.Write()
            hlaser2.Write()
            if seedmap1 != 0:
                seedmap2.Write()
            f2.Close()
            
            #formatting and saving all data into a numpy file for analyzing later
            dataList1.shape = (171,9)
            dataList2.shape = (171,9)
            np.save("EtadataEB_p1_" + runNumber + ".npy", dataList1)
            np.save("EtadataEB_p2_" + runNumber + ".npy", dataList2)
        else:
            f = rt.TFile("ClusterTimeEB_c_" + runNumber + ".root","new")
            for eta in range(0,len(histList1)):
                histList1[eta].Write()
                #Saving value of data in tuple list
                dataList1 = np.append(dataList1, [0, eta-85, fitdata1[eta][0],fitdata1[eta][1],fitdata1[eta][2],fitdata1[eta][3],fitdata1[eta][4],fitdata1[eta][5],fitdata1[eta][6]])
            htime1.Write()
            hlaser1.Write()
            if seedmap1 != 0:
                seedmap1.Write()
            f.Close()
            
            #formatting and saving all data into a numpy file for analyzing later
            dataList1.shape = (171,9)
            np.save("EtadataEB_c_" + runNumber + ".npy", dataList1)


#saves the histograms, fits, and others for the barrel
def saveEE(runNumber,dataListp,dataListm,histListp1,histListp2,histListm1,histListm2,transListp1,transListp2,transListm1,transListm2,htimep1,htimep2,htimem1,htimem2,hlaserp1,hlaserp2,hlaserm1,hlaserm2,fitdatap1,fitdatap2,fitdatam1,fitdatam2,seedmapp1,seedmapp2,seedmapm1,seedmapm2):
    if histListp2 != 0: #2 photons
        f = rt.TFile("IndivTimeEEp_p1p2_" + runNumber + ".root","new")
        for x in range(0,len(histListp1)):
            for y in range(0, len(histListp1[0])):
                histListp1[x][y].Write()
                histListp2[x][y].Write()
                transListp1[x][y].Write()
                transListp2[x][y].Write()
                #Saving value of data in tuple list
                dataListp = np.append(dataListp, [0, "p1", x, y, fitdatap1[x][y][0],fitdatap1[x][y][1],fitdatap1[x][y][2],fitdatap1[x][y][3],fitdatap1[x][y][4],fitdatap1[x][y][5],fitdatap1[x][y][6]])
                dataListp = np.append(dataListp, [0, "p2", x, y, fitdatap2[x][y][0],fitdatap2[x][y][1],fitdatap2[x][y][2],fitdatap2[x][y][3],fitdatap2[x][y][4],fitdatap2[x][y][5],fitdatap2[x][y][6]])
        htimep1.Write()
        htimep2.Write()
        hlaserp1.Write()
        hlaserp2.Write()
        if seedmapp1 != 0:
            seedmapp1.Write()
        if seedmapp2 !=0:
            seedmapp2.Write()
        f.Close()
            
        f2 = rt.TFile("IndivTimeEEm_p1p2_" + runNumber + ".root","new")
        for x in range(0,len(histListm1)):
            for y in range(0, len(histListm1[0])):
                histListm1[x][y].Write()
                histListm2[x][y].Write()
                transListm1[x][y].Write()
                transListm2[x][y].Write()
                #Saving value of data in tuple list
                dataListm = np.append(dataListm, [0, "m1", x, y, fitdatam1[x][y][0],fitdatam1[x][y][1],fitdatam1[x][y][2],fitdatam1[x][y][3],fitdatam1[x][y][4],fitdatam1[x][y][5],fitdatam1[x][y][6]])
                dataListm = np.append(dataListm, [0, "m2", x, y, fitdatam2[x][y][0],fitdatam2[x][y][1],fitdatam2[x][y][2],fitdatam2[x][y][3],fitdatam2[x][y][4],fitdatam2[x][y][5],fitdatam2[x][y][6]])
        htimem1.Write()
        htimem2.Write()
        hlaserm1.Write()
        hlaserm2.Write()
        if seedmapm1 != 0:
            seedmapm1.Write()
        if seedmapm2 !=0:
            seedmapm2.Write()
        f2.Close()
        
        dataListp.shape = (101,101,2,11)
        dataListm.shape = (101,101,2,11)
        np.save("dataEEp_p1p2_" + runNumber + ".npy", dataListp)
        np.save("dataEEm_p1p2_" + runNumber + ".npy", dataListm)
    else:
        f = rt.TFile("IndivTimeEEp_c_" + runNumber + ".root","new")
        for x in range(0,len(histListp1)):
            for y in range(0, len(histListp1[0])):
                histListp1[x][y].Write()
                transListp1[x][y].Write()
                dataListp = np.append(dataListp, [0, "p", x, y, fitdatap1[x][y][0],fitdatap1[x][y][1],fitdatap1[x][y][2],fitdatap1[x][y][3],fitdatap1[x][y][4],fitdatap1[x][y][5],fitdatap1[x][y][6]])
        htimep1.Write()
        hlaserp1.Write()
        if seedmapp1 != 0:
            seedmapp1.Write()
        f.Close()
        
        f2 = rt.TFile("IndivTimeEEm_c_" + runNumber + ".root","new")
        for x in range(0,len(histListm1)):
            for y in range(0, len(histListm1[0])):
                histListm1[x][y].Write()
                transListm1[x][y].Write()
                dataListm = np.append(dataListm, [0, "m", x, y, fitdatam1[x][y][0],fitdatam1[x][y][1],fitdatam1[x][y][2],fitdatam1[x][y][3],fitdatam1[x][y][4],fitdatam1[x][y][5],fitdatam1[x][y][6]])
        htimem1.Write()
        hlaserm1.Write()
        if seedmapm1 != 0:
            seedmapm1.Write()
        f2.Close()

        #formatting and saving all data into a numpy file for analyzing later
        dataListp.shape = (101,101,11)
        dataListm.shape = (101,101,11)
        np.save("dataEEp_c_" + runNumber + ".npy", dataListp)
        np.save("dataEEm_c_" + runNumber + ".npy", dataListm)


#draws the graphs you want to see and saves them as .png in respective folders
def printPrettyPictureEB(runNumber,htime1,htime2,hlaser1,hlaser2,seedmap1,seedmap2):
    #Gets rid of legend
    rt.gStyle.SetOptStat(0)
    
    #creates permanent background canvas
    rt.gROOT.LoadMacro('setstyle.c')
    rt.gROOT.Macro('setstyle.c')
    c = rt.TCanvas("c","c",900,600)
    c.cd()
    
    if type(htime1) != rt.TH1F: #Individual crystals
        if htime2 != 0:
            htime1.SetAxisRange(-5., 5.,"Z")
            htime1.Draw("colz")
            htime1.GetYaxis().SetTitleOffset(1.15)
            htime1.GetZaxis().SetTitleOffset(0.8)
            c.Print("IndivTimeResponseEB_p1_" + runNumber + ".png")
            hlaser1.SetAxisRange(0., 1.,"Z")
            hlaser1.Draw("colz")
            hlaser1.GetYaxis().SetTitleOffset(1.15)
            hlaser1.GetZaxis().SetTitleOffset(1.1)
            c.Print("IndivLaserTransparencyEB_p1_" + runNumber + ".png")

            htime2.SetAxisRange(-5., 5.,"Z")
            htime2.Draw("colz")
            htime2.GetYaxis().SetTitleOffset(1.15)
            htime2.GetZaxis().SetTitleOffset(0.8)
            c.Print("IndivTimeResponseEB_p2_" + runNumber + ".png")
            hlaser2.SetAxisRange(0., 1.,"Z")
            hlaser2.Draw("colz")
            hlaser2.GetYaxis().SetTitleOffset(1.15)
            hlaser2.GetZaxis().SetTitleOffset(1.1)
            c.Print("IndivLaserTransparencyEB_p2_" + runNumber + ".png")
        else:
            htime1.SetAxisRange(-5., 5.,"Z")
            htime1.Draw("colz")
            htime1.GetYaxis().SetTitleOffset(1.15)
            htime1.GetZaxis().SetTitleOffset(0.8)
            c.Print("IndivTimeResponseEB_c_" + runNumber + ".png")
            hlaser1.SetAxisRange(0., 1.,"Z")
            hlaser1.Draw("colz")
            hlaser1.GetYaxis().SetTitleOffset(1.15)
            hlaser1.GetZaxis().SetTitleOffset(1.1)
            c.Print("IndivLaserTransparencyEB_c_" + runNumber + ".png")
    else:
        if htime2 != 0:
            htime1.SetAxisRange(-85,85,"X")
            htime1.Draw("E1")
            c.Print("EtaTimeResponseEB_p1_" + runNumber + ".png")
            hlaser1.SetAxisRange(0., 1.,"Y")
            hlaser1.Draw("colz")
            hlaser1.GetYaxis().SetTitleOffset(1.15)
            hlaser1.GetZaxis().SetTitleOffset(1.1)
            c.Print("EtaLaserTransparencyEB_p1_" + runNumber + ".png")
            
            htime2.SetAxisRange(-85,85,"X")
            htime2.Draw("E1")
            c.Print("EtaTimeResponseEB_p2_" + runNumber + ".png")
            hlaser2.SetAxisRange(0., 1.,"X")
            hlaser2.Draw("colz")
            hlaser2.GetYaxis().SetTitleOffset(1.15)
            hlaser2.GetZaxis().SetTitleOffset(1.1)
            c.Print("EtaLaserTransparencyEB_p2_" + runNumber + ".png")

        else:
            htime1.SetAxisRange(-85,85,"X")
            htime1.Draw("E1")
            c.Print("EtaTimeResponseEB_c_" + runNumber + ".png")
            hlaser1.SetAxisRange(0., 1.,"X")
            hlaser1.Draw("colz")
            hlaser1.GetYaxis().SetTitleOffset(1.15)
            hlaser1.GetZaxis().SetTitleOffset(1.1)
            c.Print("EtaLaserTransparencyEB_c_" + runNumber + ".png")

    if seedmap1 != 0: #print 1 seed map
        if type(htime1) != rt.TH1F: #individual crystal
            seedmap1.SetMinimum(0.)
            seedmap1.Draw("colz")
            seedmap1.GetYaxis().SetTitleOffset(1.15)
        else:
            seedmap1.SetMinimum(0.)
            seedmap1.SetAxisRange(-85,85,"X")
            seedmap1.Draw()
        c.Print("SeedDensityEB_" + runNumber + ".png")
        if seedmap2 != 0: #print both seed maps
            if type(htime1) != rt.TH1F: #individual crystal
                seedmap2.SetMinimum(0.)
                seedmap2.Draw("colz")
                seedmap2.GetYaxis().SetTitleOffset(1.15)
            else:
                seedmap2.SetMinimum(0.)
                seedmap2.SetAxisRange(-85,85,"X")
                seedmap2.Draw()
            c.Print("SeedDensityEB_p2_" + runNumber + ".png")

    #close the canvas
    c.Close()


#draws the graphs you want to see and saves them as .png in respective folders
def printPrettyPictureEE(runNumber,htimep1,htimep2,htimem1,htimem2,hlaserp1,hlaserp2,hlaserm1,hlaserm2,seedmapp1,seedmapm1,seedmapp2,seedmapm2):
    #Gets rid of legend
    rt.gStyle.SetOptStat(0)
    
    #creates permanent background canvas
    rt.gROOT.LoadMacro('setstyle.c')
    rt.gROOT.Macro('setstyle.c')
    c = rt.TCanvas("c","c",600,500)
    c.cd()
    
    if type(htimep2) == rt.TH2F:
        htimep1.SetAxisRange(-5., 5.,"Z")
        htimep1.Draw("colz")
        htimep1.GetYaxis().SetTitleOffset(1.1)
        htimep1.GetZaxis().SetTitleOffset(0.8)
        c.Print("IndivTimeResponseEEp_p1_" + runNumber + ".png")
        hlaserp1.SetAxisRange(0., 1.,"Z")
        hlaserp1.Draw("colz")
        hlaserp1.GetYaxis().SetTitleOffset(1.1)
        hlaserp1.GetZaxis().SetTitleOffset(1.1)
        c.Print("IndivLaserTransparencyEEp_p1_" + runNumber + ".png")
        
        htimep2.SetAxisRange(-5., 5.,"Z")
        htimep2.Draw("colz")
        htimep2.GetYaxis().SetTitleOffset(1.1)
        htimep2.GetZaxis().SetTitleOffset(0.8)
        c.Print("IndivTimeResponseEEp_p2_" + runNumber + ".png")
        hlaserp2.SetAxisRange(0., 1.,"Z")
        hlaserp2.Draw("colz")
        hlaserp2.GetYaxis().SetTitleOffset(1.1)
        hlaserp2.GetZaxis().SetTitleOffset(1.1)
        c.Print("IndivLaserTransparencyEEp_p2_" + runNumber + ".png")
    
        htimem1.SetAxisRange(-5., 5.,"Z")
        htimem1.Draw("colz")
        htimem1.GetYaxis().SetTitleOffset(1.1)
        htimem1.GetZaxis().SetTitleOffset(0.8)
        c.Print("IndivTimeResponseEEm_p1_" + runNumber + ".png")
        hlaserm1.SetAxisRange(0., 1.,"Z")
        hlaserm1.Draw("colz")
        hlaserm1.GetYaxis().SetTitleOffset(1.1)
        hlaserm1.GetZaxis().SetTitleOffset(1.1)
        c.Print("IndivLaserTransparencyEEm_p1_" + runNumber + ".png")
        
        htimem2.SetAxisRange(-5., 5.,"Z")
        htimem2.Draw("colz")
        htimem2.GetYaxis().SetTitleOffset(1.1)
        htimem2.GetZaxis().SetTitleOffset(0.8)
        c.Print("IndivTimeResponseEEm_p2_" + runNumber + ".png")
        hlaserm2.SetAxisRange(0., 1.,"Z")
        hlaserm2.Draw("colz")
        hlaserm2.GetYaxis().SetTitleOffset(1.1)
        hlaserm2.GetZaxis().SetTitleOffset(1.1)
        c.Print("IndivLaserTransparencyEEm_p2_" + runNumber + ".png")
    else:
        htimep1.SetAxisRange(-5., 5.,"Z")
        htimep1.Draw("colz")
        htimep1.GetYaxis().SetTitleOffset(1.1)
        htimep1.GetZaxis().SetTitleOffset(0.8)
        c.Print("IndivTimeResponseEEp_c_" + runNumber + ".png")
        hlaserp1.SetAxisRange(0., 1.,"Z")
        hlaserp1.Draw("colz")
        hlaserp1.GetYaxis().SetTitleOffset(1.1)
        hlaserp1.GetZaxis().SetTitleOffset(1.1)
        c.Print("IndivLaserTransparencyEEp_c_" + runNumber + ".png")

        htimem1.SetAxisRange(-5., 5.,"Z")
        htimem1.Draw("colz")
        htimem1.GetYaxis().SetTitleOffset(1.1)
        htimem1.GetZaxis().SetTitleOffset(0.8)
        c.Print("IndivTimeResponseEEm_c_" + runNumber + ".png")
        hlaserm1.SetAxisRange(0., 1.,"Z")
        hlaserm1.Draw("colz")
        hlaserm1.GetYaxis().SetTitleOffset(1.1)
        hlaserm1.GetZaxis().SetTitleOffset(1.1)
        c.Print("IndivLaserTransparencyEEm_c_" + runNumber + ".png")

    if seedmapp1 != 0: #print 1 seed map
        seedmapp1.SetMinimum(0.)
        seedmapp1.Draw("colz")
        seedmapp1.GetYaxis().SetTitleOffset(1.1)
        c.Print("SeedDensityEEp_" + runNumber + ".png")

        seedmapm1.SetMinimum(0.)
        seedmapm1.Draw("colz")
        seedmapm1.GetYaxis().SetTitleOffset(1.1)
        c.Print("SeedDensityEEm_" + runNumber + ".png")
        if seedmapp2 != 0: #print both seed maps
            seedmapp2.SetMinimum(0.)
            seedmapp2.Draw("colz")
            seedmapp2.GetYaxis().SetTitleOffset(1.1)
            c.Print("SeedDensityEEp_p2_" + runNumber + ".png")
            
            seedmapm2.SetMinimum(0.)
            seedmapm2.Draw("colz")
            seedmapm2.GetYaxis().SetTitleOffset(1.1)
            c.Print("SeedDensityEEm_p2_" + runNumber + ".png")

    #close the canvas
    c.Close()
