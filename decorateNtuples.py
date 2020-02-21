from ROOT import TFile, TTree
from array import array

#filename = ["Diboson"]
filename = ["HbbSignal","Diboson","Zjets_latestinDec","singleTop","ttbar_0L"]
g = 0
for fn in filename:
 g = g + 1
 File_old = TFile(fn+".root","read")
 oldtree  = File_old.Get('Nominal')

 f = TFile( fn+"_decor"+".root", 'recreate' )
 t = oldtree.CloneTree(0)
 #t = TTree( 't1', 'tree with histos' )

 n = array( 'i', [ 0 ] )
 n1 = array( 'i', [ 0 ] )
 nSam = array( 'i', [ 0 ] )
 t.Branch( 'PCLead', n, 'PCLead/I' )
 t.Branch( 'PCSLead', n1, 'PCSLead/I' )
 t.Branch( 'nSam', nSam, 'nSam' )

 for i in range(oldtree.GetEntries()):
  oldtree.GetEntry(i)
  # define here the different possibilities used to extract pseudo-continous

  MV2_1=  oldtree.MV2TrkJet1InLeadFJ
  MV2_2=  oldtree.MV2TrkJet2InLeadFJ
  nSam[0] = g
  n[0]  = -1
  n1[0] = -1

  if MV2_1 >= 0.792: n[0] = 3
  if MV2_1 < 0.792 and MV2_1 >= 0.577 : n[0] = 2
  if MV2_1 < 0.577 and MV2_1 >= 0.4814 : n[0] = 1

  if MV2_2 >= 0.792: n1[0] = 3
  if MV2_2 < 0.792 and MV2_2 >= 0.577 : n1[0] = 2
  if MV2_2 < 0.577 and MV2_2 >= 0.4814 : n1[0] = 1

  t.Fill()

 f.Write()
 f.Close()
