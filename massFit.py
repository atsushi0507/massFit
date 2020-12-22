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

# Observable
x = r.RooRealVar("x", "x", 0., 25.)

# Convert TH1 to RooFit RooDataHist
dh_massHist = r.RooDataHist("dh_massHist", "dh_massHist", x, DV_m_4track)
dh_mv4 = r.RooDataHist("dh_mv4", "dh_mv4", x, mv_4track)
dh_ax4 = r.RooDataHist("dh_ax4", "dh_ax4", x, ax_4track)
dh_hi4 = r.RooDataHist("dh_hi4", "dh_hi4", x, hi_4track)

# Get p.d.f. for each background component
mv4_pdf = r.RooHistPdf("mv4_pdf", "mv4_pdf", x, dh_mv4)
ax4_pdf = r.RooHistPdf("ax4_pdf", "ax4_pdf", x, dh_ax4)
hi4_pdf = r.RooHistPdf("hi4_pdf", "hi4_pdf", x, dh_hi4)

frame = x.frame(r.RooFit.Title("normalize"))
mv4_pdf.plotOn(frame, r.RooFit.LineColor(r.kRed))
ax4_pdf.plotOn(frame, r.RooFit.LineColor(r.kBlue))
hi4_pdf.plotOn(frame, r.RooFit.LineColor(r.kGreen))
frame.Draw()
c1.Print("{}/pdfNormalized.pdf".format(directory))

# Define normalizatin range
x.setRange("part", 6., 10.)
x.setRange("hi_part", 0., 5.)

# Fit pdf to data
r_part_mv = mv4_pdf.fitTo(dh_massHist, r.RooFit.Save(r.kTRUE), r.RooFit.Range("part"))
r_part_ax = ax4_pdf.fitTo(dh_massHist, r.RooFit.Save(r.kTRUE), r.RooFit.Range("part"))
r_part_hi = hi4_pdf.fitTo(dh_massHist, r.RooFit.Save(r.kTRUE), r.RooFit.Range("hi_part"))

# Construct a background model
frac_ax = r.RooRealVar("frac_ax", "frac_ax", 0., 1.)
frac_hi = r.RooRealVar("frac_hi", "frac_hi", 0., 1.)
bkgPdf = r.RooAddPdf("bkgPdf", "bkgPdf", r.RooArgList(ax4_pdf, hi4_pdf, mv4_pdf), r.RooArgList(frac_ax, frac_hi))

x.setRange("fitRange", 0.5, 25.)
bkgResult = bkgPdf.fitTo(dh_massHist, r.RooFit.Save(r.kTRUE), r.RooFit.Range("fitRange"))
bkgFrame = x.frame(r.RooFit.Title("bkgFit"))
dh_massHist.plotOn(bkgFrame)
bkgPdf.plotOn(bkgFrame)
# Overlay  bkg components
ras_ax4 = r.RooArgSet(ax4_pdf)
ras_hi4 = r.RooArgSet(hi4_pdf)
ras_mv4 = r.RooArgSet(mv4_pdf)
bkgPdf.plotOn(bkgFrame, r.RooFit.Components(ras_ax4), r.RooFit.LineColor(r.kRed), r.RooFit.LineStyle(r.kDashed))
bkgPdf.plotOn(bkgFrame, r.RooFit.Components(ras_hi4), r.RooFit.LineColor(r.kGreen+2), r.RooFit.LineStyle(r.kDotted))
bkgPdf.plotOn(bkgFrame, r.RooFit.Components(ras_mv4), r.RooFit.LineColor(r.kMagenta), r.RooFit.LineStyle(r.kCircle))
bkgFrame.Draw()
c1.Print("{}/bkgFit.pdf".format(directory))

bkgResult.Print()
