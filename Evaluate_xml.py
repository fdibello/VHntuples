import ROOT
from array import array
from math import isnan
import math
import sys
import numpy as np
import random

inputfileName            = sys.argv[1]
treeName                 = 'Nominal'
xmlFile                  = sys.argv[2] #'TMVAClassification_BDTG.weights.xml'
mva_method               = 'BDTG'
maxNumberOfJetsToRunOver = -1

xmlNameToBranchName = {
"MET"                     : "MET",
"PCLead"                : "PCLead",
"PCSLead"                : "PCSLead",
"mJ"                : "mJ",
"sqrt((acos(cos(PhiTrkJet1InLeadFJ*3.14/180.-PhiTrkJet2InLeadFJ*3.14/180.))*(acos(cos(PhiTrkJet1InLeadFJ*3.14/180.-PhiTrkJet2InLeadFJ*3.14/180.))))+(EtaTrkJet1InLeadFJ-EtaTrkJet2InLeadFJ)*(EtaTrkJet1InLeadFJ-EtaTrkJet2InLeadFJ))" : "PhiTrkJet1InLeadFJ",
}

# collect list of variables from XML file - they need to be declared in the
# reader in the same order
xml = ROOT.TXMLEngine()
xmldoc = xml.ParseFile(xmlFile)
mainnode = xml.DocGetRootElement(xmldoc)
child = xml.GetChild(mainnode)
while(xml.GetNodeName(child)!='Variables'):
                child = xml.GetNext(child)

attr = xml.GetFirstAttr(child)
nVars =  xml.GetAttrValue(attr)
print xml.GetAttrName(attr),' ', nVars, attr, child

varList = []

name = ''
if "Zjet" in inputfileName: name = "Zjet"
elif "sin" in inputfileName: name = "sT"
elif "Diboson" in inputfileName: name = "Dib"
elif "ttb" in inputfileName: name = "ttbar"
elif "Hbb" in inputfileName: name = "Hbb"

varnode = xml.GetChild(child)
varList.append( xml.GetAttr(varnode,'Expression') )
for i in range(1,int(nVars)):
                varnode = xml.GetNext(varnode)
                varList.append( xml.GetAttr(varnode,'Expression') )

print varList
# Found the variables from XML, now need to run the Evaluation.

reader = ROOT.TMVA.Reader()

varPointers = {}

for xmlName in varList:
        varname = xmlName
        print varname
        varPointers[varname] = array('f',[-999])
        print varname, varPointers[varname]
        reader.AddVariable(varname,varPointers[varname])
we = array('f',[-999])
reader.AddSpectator("EventWeight",   we)

reader.BookMVA(mva_method,xmlFile)

fin = ROOT.TFile(inputfileName, 'read')
tree = fin.Get(treeName)

xmlResult = array('f',[-999])

nEntries = tree.GetEntries()

fout = ROOT.TFile('validation_output_newMET'+name+'.root','recreate')
h_bdt = []
h_met = []
kfact = [0,0.2,0.5,1]
j = -1
h_METbdt = ROOT.TH2F("h_METbdt","h_METbdt",50,250,2000,10,-1.1,1.1)
h_mJbdt = ROOT.TH2F("h_mJbdt","h_mJbdt",50,50,300,10,-1.1,1.1)
h_mJMET = ROOT.TH2F("h_mJMET","h_mJMET",50,50,300,50,250,2000)
h_PCl  = ROOT.TProfile("h_PCl","h_PCl",  100,250,2000, 0,4)
h_PCsl = ROOT.TProfile("h_PCsl","h_PCls",100,250,2000, 0,4)
for k in kfact:
 j = j + 1
 h_final = ROOT.TH1F("h_final"+str(k),"h_final"+str(k),20,-1.1,1.1)
 #h_MET = ROOT.TH1F("h_MET"+str(k),"h_MET"+str(k),100,50,300)
 h_MET = ROOT.TH1F("h_MET"+str(k),"h_MET"+str(k),100,250,2000)
 h_bdt.append(h_final)
 h_met.append(h_MET)

h_mZbl = ROOT.TH1F("h_mZbl","h_mZbl",60,-1.,1.)
h_mZbb = ROOT.TH1F("h_mZbb","h_mZbb",60,-1.,1.)
h_mZbc = ROOT.TH1F("h_mZbc","h_mZbc",60,-1.,1.)
h_mZl  = ROOT.TH1F("h_mZl","h_mZl",  60,  -1.,1.)
h_mZcc = ROOT.TH1F("h_mZcc","h_mZcc",60,-1.,1.)
h_mZcl = ROOT.TH1F("h_mZcl","h_mZcl",60,-1.,1.)

h_maZbl = ROOT.TH1F("h_maZbl","h_maZbl",100,0,500)
h_maZbb = ROOT.TH1F("h_maZbb","h_maZbb",100,0,500)
h_maZbc = ROOT.TH1F("h_maZbc","h_maZbc",100,0,500)
h_maZl  = ROOT.TH1F("h_maZl","h_maZl"  ,100,0,500)
h_maZcc = ROOT.TH1F("h_maZcc","h_maZcc",100,0,500)
h_maZcl = ROOT.TH1F("h_maZcl","h_maZcl",100,0,500)

h_mttbar = ROOT.TH1F("h_mttbar","h_mttbar",60,-1.,1.)
h_mH = ROOT.TH1F("h_mH","h_mH",60,-1.,1.)
h_msT = ROOT.TH1F("h_msT","h_msT",60,-1.,1.)
h_mass = ROOT.TH1F("h_mass","h_mass",100,0,500)
h_metF  = ROOT.TH1F("h_MET","h_MET",50,400,2400)

#for i in range(1000000):
for i in range(nEntries):
  tree.GetEntry(i)
#  print "Applying now analysis cut:"
#  if tree.NBTagUnmatchedTrackJetLeadFatJet ==1 and tree.NAdditionalCaloJets == 1 and tree.MET < 400 and tree.MET > 250 and tree.MV2TrkJet1InLeadFJ>0.4814 and tree.MV2TrkJet2InLeadFJ > 0.4814 and tree.mJ > 50 and tree.PtTrkJet1InLeadFJ>10 and tree.PtTrkJet2InLeadFJ > 10:
  if tree.MET > 600 and tree.MET < 1000 and tree.MV2TrkJet1InLeadFJ>0.4814 and tree.MV2TrkJet2InLeadFJ > 0.4814 and tree.mJ > 50 and tree.PtTrkJet1InLeadFJ>10 and tree.PtTrkJet2InLeadFJ > 10 and (tree.NAdditionalCaloJets == 0) and tree.NBTagUnmatchedTrackJetLeadFatJet ==0:

   for xmlName in varList:
    varvector = getattr(tree, xmlNameToBranchName[xmlName])
    if "PhiTrkJet1InLeadFJ" in xmlNameToBranchName[xmlName]:
       varValue = np.sqrt((math.acos(math.cos(tree.PhiTrkJet1InLeadFJ*3.14/180.-tree.PhiTrkJet2InLeadFJ*3.14/180.))*(math.acos(math.cos(tree.PhiTrkJet1InLeadFJ*3.14/180.-tree.PhiTrkJet2InLeadFJ*3.14/180.))))+(tree.EtaTrkJet1InLeadFJ-tree.EtaTrkJet2InLeadFJ)*(tree.EtaTrkJet1InLeadFJ-tree.EtaTrkJet2InLeadFJ))
    #if xmlNameToBranchName[xmlName] == 'MET': varValue = tree.MET + random.gauss(0,tree.MET * k)
    else: varValue = varvector
    varPointers[xmlName][0] = varValue
#    print xmlName, varValue
# results now
   xmlResult[0] = reader.EvaluateMVA(mva_method)
#   print xmlResult[0]
   for j in range(len(kfact)):
#    print varValue, xmlNameToBranchName[xmlName],j
    if j != 0:h_bdt[j].Fill(xmlResult[0],tree.EventWeight*(1+kfact[j]*(tree.MET-800.)/400.))
    if j != 0:h_met[j].Fill(tree.MET,tree.EventWeight*(1+kfact[j]*(tree.MET-800.)/400.))
    if j == 0:h_met[j].Fill(tree.MET,tree.EventWeight)
    if j == 0:h_bdt[j].Fill(xmlResult[0],tree.EventWeight)
    #w = ((tree.mJ*tree.mJ-125*125)*(tree.mJ*tree.mJ-125*125) + 125*125)
    #if j != 0:h_met[j].Fill(tree.mJ,tree.EventWeight*w)
    #if j != 0:h_bdt[j].Fill(xmlResult[0],tree.EventWeight*w)
    #if j != 0:h_met[j].Fill(tree.mJ,tree.EventWeight*(1+kfact[j]*(tree.mJ-300.)/125. ))
    #if j != 0:h_bdt[j].Fill(xmlResult[0],tree.EventWeight*(1+kfact[j]*(tree.mJ-300.)/125.))
    #if j == 0:h_met[j].Fill(tree.mJ,tree.EventWeight)

#   print tree.mJ,xmlResult[0]
   h_METbdt.Fill(tree.MET,xmlResult[0],tree.EventWeight)
   h_mJbdt.Fill(tree.mJ,xmlResult[0],tree.EventWeight)
   h_mJMET.Fill(tree.mJ,tree.MET,tree.EventWeight)
   h_PCl.Fill(tree.MET,tree.PCLead)
   h_PCsl.Fill(tree.MET,tree.PCSLead)

   #Include all the TH1 we need
   if tree.flavB1 == 5 and tree.flavB2 == 5:   h_mZbb.Fill(xmlResult[0],tree.EventWeight)
   if tree.flavB1 == 5 and tree.flavB2 == 4:   h_mZbc.Fill(xmlResult[0],tree.EventWeight)
   if tree.flavB1 == 4 and tree.flavB2 == 5:   h_mZbc.Fill(xmlResult[0],tree.EventWeight)
   if tree.flavB1 == 4 and tree.flavB2 == 4:   h_mZcc.Fill(xmlResult[0],tree.EventWeight)
   if tree.flavB1 == 5 and tree.flavB2 == 0:   h_mZbl.Fill(xmlResult[0],tree.EventWeight)
   if tree.flavB1 == 0 and tree.flavB2 == 5:   h_mZbl.Fill(xmlResult[0],tree.EventWeight)
   if tree.flavB1 == 4 and tree.flavB2 == 0:   h_mZcl.Fill(xmlResult[0],tree.EventWeight)
   if tree.flavB1 == 0 and tree.flavB2 == 4:   h_mZcl.Fill(xmlResult[0],tree.EventWeight)
   if tree.flavB1 == 0 and tree.flavB2 == 0:   h_mZl.Fill(xmlResult[0],tree.EventWeight)
   if tree.flavB1 == 5 and tree.flavB2 == 5:   h_maZbb.Fill(tree.mJ,tree.EventWeight)
   if tree.flavB1 == 5 and tree.flavB2 == 4:   h_maZbc.Fill(tree.mJ,tree.EventWeight)
   if tree.flavB1 == 4 and tree.flavB2 == 5:   h_maZbc.Fill(tree.mJ,tree.EventWeight)
   if tree.flavB1 == 4 and tree.flavB2 == 4:   h_maZcc.Fill(tree.mJ,tree.EventWeight)
   if tree.flavB1 == 5 and tree.flavB2 == 0:   h_maZbl.Fill(tree.mJ,tree.EventWeight)
   if tree.flavB1 == 0 and tree.flavB2 == 5:   h_maZbl.Fill(tree.mJ,tree.EventWeight)
   if tree.flavB1 == 4 and tree.flavB2 == 0:   h_maZcl.Fill(tree.mJ,tree.EventWeight)
   if tree.flavB1 == 0 and tree.flavB2 == 4:   h_maZcl.Fill(tree.mJ,tree.EventWeight)
   if tree.flavB1 == 0 and tree.flavB2 == 0:   h_maZl.Fill( tree.mJ,tree.EventWeight)
#   if  tree.flavB1 == 5 and tree.flavB2 == 5: print tree.mJ, xmlResult[0]
   #if name == "ttbar": h_mttbar.Fill(xmlResult[0],tree.EventWeight)
   #if name == "Hbb": h_mH.Fill(xmlResult[0],tree.EventWeight)
   #if name == "sT": h_msT.Fill(xmlResult[0],tree.EventWeight)
   h_mH.Fill(xmlResult[0],tree.EventWeight)
   h_mass.Fill(tree.mJ,tree.EventWeight)
   h_metF.Fill(tree.MET,tree.EventWeight)
for j in range(len(kfact)):
 h_bdt[j].Write()
 h_met[j].Write()
 h_ratio_met = h_met[j].Clone("h_ratio_met"+str(j))
 h_ratio_bdt = h_bdt[j].Clone("h_ratio_bdt"+str(j))
 h_MET_ori   = h_met[0].Clone("h_met_ori")
 h_bdt_ori   = h_bdt[0].Clone("h_bdt_ori")
 h_ratio_met.Divide(h_MET_ori)
 h_ratio_bdt.Divide(h_bdt_ori)
 h_ratio_met.Write()
 h_ratio_bdt.Write()
h_METbdt.Write()
h_mJbdt.Write()
h_mJMET.Write()
h_PCl.Write()
h_PCsl.Write()
fout1 = ROOT.TFile('output_newMET'+name+'.root','recreate')
fout1.cd()
h_mZbb.Write()
h_mZbc.Write()
h_mZcc.Write()
h_mZbl.Write()
h_mZcl.Write()
h_mZl.Write()
h_maZbb.Write()
h_maZbc.Write()
h_maZcc.Write()
h_maZbl.Write()
h_maZcl.Write()
h_mttbar.Write()
h_mH.Write()
h_msT.Write()
h_mass.Write()
h_metF.Write()
fout1.Close()
fout.Close()
