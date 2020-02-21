import ROOT
import numpy as np

filename = ["output_newMETHbb.root","output_newMETZjet.root","output_newMETsT.root","output_newMETttbar.root","output_newMETDib.root"]
Regions  = ["250_400","400","250_400_CR","400_CR"]
New_Regions = ["13TeV_ZeroLepton_2tag1pfat0pjet_250_400ptv_SR_noaddbjetsr_mBB","13TeV_ZeroLepton_2tag1pfat0pjet_400ptv_SR_noaddbjetsr_mBB","13TeV_ZeroLepton_2tag1pfat0pjet_250_400ptv_SR_topaddbjetcr_mBB","13TeV_ZeroLepton_2tag1pfat0pjet_400ptv_SR_topaddbjetcr_mBB"]

histos = ["ttbar","Wbl","Wbb","Wbc","Wcc","Wl","Wcl","WZ","WW","ZZ","Zbl","Zbb","Zbc","Zcc","Zcl","Zl","data","ggZllH125","ggZZ","ggZvvH125","ggZvvH125cc","qqWlvH125","qqWlvH125cc","qqZllH125","qqZllH125cc","qqZvvH125","qqZvvH125cc","stopWt","stops","stopt","ggZllH125cc"]
h_histos = []

reb = 1
for h in histos:
 #ht=ROOT.TH1F(h,h,100,0,500)
 ht=ROOT.TH1F(h,h,60,-1,1)
 ht.Rebin(reb)
 h_histos.append([ht,h])

j = -1
for Reg in Regions:
 Histo_Copy = []
 print "copying: ", Reg
 j = j + 1
 histoF = []
 h = []
 f = -1
 fileO = ROOT.TFile( "FitO/"+New_Regions[j]+".root", 'recreate' )
# hAll = ROOT.TH1F("data","data",100,0,500)
 hAll = ROOT.TH1F("data","data",60,-1,1)
 hAll.Rebin(reb)
 for filen in filename:
  f = f + 1
  histoF.append(0)
  print "File:", Reg+'/'+filen
  inputF = ROOT.TFile(Reg+'/'+filen,"read")
  #histoF[f] = inputF.Get("h_mass")
  histoF[f] = inputF.Get("h_mH")
  histoF[f].Rebin(reb)
  if filen == "output_newMETHbb.root":
           fileO.cd()
           histoF[f].SetName("qqZvvH125")
           histoF[f].SetTitle("qqZvvH125")
           hAll.Add(histoF[f])
           histoF[f].Write()
           Histo_Copy.append("qqZvvH125")
  elif filen == "output_newMETZjet.root":

           histoFbb = inputF.Get("h_mZbb")
           histoFbc = inputF.Get("h_mZbc")
           histoFcc = inputF.Get("h_mZcc")
           histoFl  = inputF.Get("h_mZcl")
           histoFbl = inputF.Get("h_mZbl")
           histoFcl = inputF.Get("h_mZcl")

           histoFbb.Rebin(reb)
           histoFbc.Rebin(reb)
           histoFcc.Rebin(reb)
           histoFl.Rebin(reb)
           histoFbl.Rebin(reb)
           histoFcl.Rebin(reb)

           histoFbb.SetName("Zbb")
           histoFbb.SetTitle("Zbb")
           fileO.cd()
           histoFbb.Write()
           histoFbc.SetName("Zbc")
           histoFbc.SetTitle("Zbc")
           fileO.cd()
           histoFbc.Write()
           histoFbl.SetName("Zbl")
           histoFbl.SetTitle("Zbl")
           fileO.cd()
           histoFbl.Write()
           histoFcc.SetName("Zcc")
           histoFcc.SetTitle("Zcc")
           fileO.cd()
           histoFcc.Write()
           histoFl.SetName( "Zl")
           histoFl.SetTitle("Zl")
           fileO.cd()
           histoFl.Write()
           histoFcl.SetName("Zcl")
           histoFcl.SetTitle("Zcl")
           fileO.cd()
           histoFcl.Write()

           hAll.Add(histoFbb)
           hAll.Add(histoFbl)
           hAll.Add(histoFbc)
           hAll.Add(histoFcc)
           hAll.Add(histoFcl)
           hAll.Add(histoFl)
           Histo_Copy.append("Zbb")
           Histo_Copy.append("Zbc")
           Histo_Copy.append("Zbl")
           Histo_Copy.append("Zcl")
           Histo_Copy.append("Zcc")
           Histo_Copy.append("Zl" )

  elif filen == "output_newMETsT.root":
           fileO.cd()
           histoF[f].SetName( "stopWt")
           histoF[f].SetTitle("stopWt")
           histoF[f].Write()
           Histo_Copy.append("stopWt")
           hAll.Add(histoF[f])
  elif filen == "output_newMETttbar.root":
           fileO.cd()
           histoF[f].SetName( "ttbar")
           histoF[f].SetTitle("ttbar")
           histoF[f].Write()
           Histo_Copy.append("ttbar")
           hAll.Add(histoF[f])
  elif filen == "output_newMETDib.root":
           fileO.cd()
           histoF[f].SetName( "ZZ")
           histoF[f].SetTitle("ZZ")
           histoF[f].Write()
           Histo_Copy.append("ZZ")
           hAll.Add(histoF[f])

 print "new region: ","FitO/"+New_Regions[j]+".root"
 print "Printing ",Histo_Copy
 saved = []
 #for hh in Histo_Copy:
 #    print hh
 #    hh[0].Print("all")
 #    print "Copying:", hh[1]
 #    hh[0].SetName(hh[1])
 #    hh[0].SetTitle(hh[1])
 #    print "Copying1:", hh[1]
 #    hh[0].Write()
 #    saved.append(hh[1])
 for His in h_histos:
    if His[1] not in Histo_Copy:
         if His[1] == "data":
          for bins in range(hAll.GetXaxis().GetNbins()+1):
                  if hAll.GetBinContent(bins) > 0: hAll.SetBinError(bins,np.sqrt(hAll.GetBinContent(bins)) )
                  else:hAll.SetBinContent(bins,0)
          hAll.Write()
         else: His[0].Write()
