import ROOT as r
import os, datetime
import sys
sys.path.append("/Users/amizukam/DVJets/atlasstyle")
from AtlasStyle import *
from AtlasLabel import *

SetAtlasStyle()
r.gROOT.SetBatch()

label = "Work in Progress"

date = str(datetime.date.today())
directory = os.getcwd() + "/plots/" + date + "/massFit"
if (not os.path.isdir(directory)):
    os.makedirs(directory)

c1 = r.TCanvas("c1", "c1", 800, 600)
r.gPad.SetLogy()

path = "/Users/amizukam/DVJets/"
massFile = r.TFile(path+"mergedVertices/run2_full_weighted.root", "READ")
hiFile = r.TFile(path +"hadronicInteractions/HI_Templates/HI_Templates_Small_Bins.root", "READ")
ax4File_region = r.TFile(path+"accidentalCrossings/massTemplates.f.14122020.4trk.root", "READ")
ax4File = r.TFile(path+"accidentalCrossings/massTemplates.f.14122020.4trkcomb.root", "READ")

binning = 5
DV_m_4track = massFile.Get("DV_m_4track").Rebin(binning)
ax_4track = ax4File.Get("h_comb")

bin6 = DV_m_4track.FindBin(6.)
bin10 = DV_m_4track.FindBin(10.)
bin20 = DV_m_4track.FindBin(20.)

DV_m_4track.GetXaxis().SetRange(1, bin20)

DV_m_4track.Draw("hist e")
ax_4track.SetLineColor(r.kRed)
ax_4track.SetMarkerColor(r.kRed)
ax_4track.Draw("same hist e")
c1.Print("{}/{}.pdf".format(directory, "ax_and_DV"))

nData = DV_m_4track.Integral(bin10+1, bin20-1)
nAX = ax_4track.Integral(bin10+1, bin20-1)
print(nData, nAX)
