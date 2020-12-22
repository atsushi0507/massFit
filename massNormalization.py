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
mv_4track = massFile.Get("mergedMass4_sigWeight").Rebin(binning)
hi_4track = hiFile.Get("4trk")

bin6 = DV_m_4track.FindBin(6.)
bin10 = DV_m_4track.FindBin(10.)
bin20 = DV_m_4track.FindBin(20.)

DV_m_4track.GetXaxis().SetRange(1, bin20)
hi_4track.GetXaxis().SetRange(1, bin20)

leg = r.TLegend(0.65, 0.70, 0.88, 0.85)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.SetTextSize(0.03)
leg.AddEntry(DV_m_4track, "Data", "p")
leg.AddEntry(ax_4track, "Accidental Crossings", "l")
leg.AddEntry(mv_4track, "Merged Vertices", "l")
leg.AddEntry(hi_4track, "Hadronic Interactions", "l")

DV_m_4track.DrawNormalized("hist e")
ax_4track.SetLineColor(r.kRed)
ax_4track.SetMarkerColor(r.kRed)
ax_4track.DrawNormalized("same hist e")
mv_4track.SetLineColor(r.kBlue)
mv_4track.SetMarkerColor(r.kBlue)
mv_4track.DrawNormalized("same hist e")
hi_4track.SetLineColor(r.kGreen)
hi_4track.SetMarkerColor(r.kGreen)
hi_4track.DrawNormalized("same hist e")
ATLASLabel(0.55, 0.88, label)
leg.Draw()
c1.Print("{}/{}.pdf".format(directory, "DV_and_BGtemplate"))

nData = DV_m_4track.Integral(bin10+1, bin20-1)
nAX = ax_4track.Integral(bin10+1, bin20-1)
print(nData, nAX)

# RooFit
x = r.RooRealVar("x", "x", 0., 25.)
DVmass_hist = r.RooDataHist("DVmass_hist", "DVmass_hist", x, DV_m_4track)
ax4Hist = r.RooDataHist("ax4Hist", "ax4Hist", x, ax_4track)
mv4Hist = r.RooDataHist("mv4Hist", "mv4Hist", x, mv_4track)
hi4Hist = r.RooDataHist("hi4Hist", "hi4Hist", x, hi_4track)

# Get PDF
ax4_pdf = r.RooHistPdf("ax4_pdf", "ax4_pdf", x, ax4Hist)
mv4_pdf = r.RooHistPdf("mv4_pdf", "mv4_pdf", x, mv4Hist)
hi4_pdf = r.RooHistPdf("hi4_pdf", "hi4_pdf", x, hi4Hist)

# Fit full range
r_full_ax = ax4_pdf.fitTo(DVmass_hist, r.RooFit.Save(r.kTRUE))
r_full_mv = mv4_pdf.fitTo(DVmass_hist, r.RooFit.Save(r.kTRUE))
r_full_hi = mv4_pdf.fitTo(DVmass_hist, r.RooFit.Save(r.kTRUE))

x.setRange("part", 6., 10.)
x.setRange("hi_part", 1., 5.)

# Fit pdf only to data in "[6,10]"
r_part_ax = ax4_pdf.fitTo(DVmass_hist, r.RooFit.Save(r.kTRUE), r.RooFit.Range("part"))
r_part_mv = mv4_pdf.fitTo(DVmass_hist, r.RooFit.Save(r.kTRUE), r.RooFit.Range("part"))
r_part_hi = hi4_pdf.fitTo(DVmass_hist, r.RooFit.Save(r.kTRUE), r.RooFit.Range("hi_part"))

# Plot and print results

leg2 = r.TLegend(0.65, 0.65, 0.85, 0.85)
leg2.SetBorderSize(0)
leg2.SetFillStyle(0)
leg2.SetTextSize(0.03)

frame = x.frame(r.RooFit.Title("4-track"))
DVmass_hist.plotOn(frame)
ax4_pdf.plotOn(frame, r.RooFit.Range("full"), r.RooFit.LineStyle(r.kDashed), r.RooFit.LineColor(r.kBlue))
ax4_pdf.plotOn(frame, r.RooFit.Range("part"), r.RooFit.LineColor(r.kBlue))
mv4_pdf.plotOn(frame, r.RooFit.Range("full"), r.RooFit.LineStyle(r.kDashed), r.RooFit.LineColor(r.kRed))
mv4_pdf.plotOn(frame, r.RooFit.Range("part"), r.RooFit.LineColor(r.kRed))
hi4_pdf.plotOn(frame, r.RooFit.Range("full"), r.RooFit.LineStyle(r.kDashed), r.RooFit.LineColor(r.kGreen))
hi4_pdf.plotOn(frame, r.RooFit.Range("hi_part"), r.RooFit.LineColor(r.kGreen))
frame.Draw()
ATLASLabel(0.55, 0.88, label)
leg2.AddEntry(DVmass_hist, "Data", "p")
leg2.AddEntry(ax4Hist, "Accidental Crossings", "l")
leg2.AddEntry(mv4Hist, "Merged Vertices", "l")
leg2.AddEntry(hi4Hist, "Hadronic Interactions", "l")
leg2.Draw()
c1.Print("{}/DV_4track.pdf".format(directory))
