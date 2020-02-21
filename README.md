This is a project for Ntuples analysis

decorateNtuples.py: The first macro takes into standard ntuples from 0 lepton channel  (with MV2
score explicitely saved) and  add branches with PCBT for the leading and
subleading.

TMVAMulticlass.c: standard macro from TMVA for BDT or Multiclassification. With
the correct  input with PCBT it runs the training and produces the standard
output format. The most important is the xml file with training results.

Evaluate_xml.py: Reads the xml and computes the BDT or Multiclass output on the
fly. Example on how to run: python Evaluate_xml.py "/Users/francescoarmandodibello/Documents/VHbb/Ntuples/HbbSignal_decor.root" weights/TMVAClassification_BDT_250_400.weights.xml

This will output histograms file that can be used as inputs to the fit.

convert_toFit.py: WSMaker is very peaky about naming so this macro get the
histogram from the previous macro and puts them with usual nomenclature of
WSMaker.
