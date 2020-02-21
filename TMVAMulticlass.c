/**********************************************************************************
 * Project   : TMVA - a Root-integrated toolkit for multivariate data analysis    *
 * Package   : TMVA                                                               *
 * Root Macro: TMVAMulticlass                                                     *
 *                                                                                *
 * This macro provides a simple example for the training and testing of the TMVA  *
 * multiclass classification                                                      *
 **********************************************************************************/

#include <cstdlib>
#include <iostream>
#include <map>
#include <string>

#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TSystem.h"
#include "TROOT.h"
#include "TMath.h"

#include "TMVA/Tools.h"
#include "TMVA/Factory.h"
#include "TMVA/TMVAMultiClassGui.h"

using namespace TMVA;

void TMVAMulticlass( TString myMethodList = "" )
{

   // This loads the library
   TMVA::Tools::Instance();

   // to get access to the GUI and all tmva macros
   // TString tmva_dir(TString(gRootDir) + "/tmva");
   // if(gSystem->Getenv("TMVASYS"))
   //    tmva_dir = TString(gSystem->Getenv("TMVASYS"));
   // gROOT->SetMacroPath(tmva_dir + "/test/:" + gROOT->GetMacroPath() );
   // gROOT->ProcessLine(".L TMVAMultiClassGui.C");

   //---------------------------------------------------------------
   // default MVA methods to be trained + tested
   std::map<std::string,int> Use;
   Use["MLP"]             = 0;
   Use["BDTG"]            = 1;
   Use["FDA_GA"]          = 0;
   Use["PDEFoam"]         = 0;
   //---------------------------------------------------------------

   std::cout << std::endl;
   std::cout << "==> Start TMVAMulticlass" << std::endl;

   if (myMethodList != "") {
      for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) it->second = 0;

      std::vector<TString> mlist = TMVA::gTools().SplitString( myMethodList, ',' );
      for (UInt_t i=0; i<mlist.size(); i++) {
         std::string regMethod(mlist[i]);

         if (Use.find(regMethod) == Use.end()) {
            std::cout << "Method \"" << regMethod << "\" not known in TMVA under this name. Choose among the following:" << std::endl;
            for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) std::cout << it->first << " ";
            std::cout << std::endl;
            return;
         }
         Use[regMethod] = 1;
      }
   }

   // Create a new root output file.
   TString outfileName = "test_boostedVhbb_TMVAMulticlass.root";
   TFile* outputFile = TFile::Open( outfileName, "RECREATE" );

 //  TMVA::Factory *factory = new TMVA::Factory( "TMVAMulticlass", outputFile,
 //                                               "!V:!Silent:Color:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=multiclass" );

   TMVA::Factory *factory = new TMVA::Factory( "TMVAClassification", outputFile,
                                                                "!V:!Silent:Color:DrawProgressBar:AnalysisType=Classification" );

   factory->AddSpectator("EventWeight",   'F');

   factory->AddVariable( "MET", 'F' );
   factory->AddVariable( "PCLead", 'I' );
   factory->AddVariable( "PCSLead", 'I' );
//   factory->AddVariable( "MV2TrkJet1InLeadFJ","MV2_leading","", 'F' );
//   factory->AddVariable( "MV2TrkJet2InLeadFJ","MV2_Sleading","", 'F' );
//   factory->AddSpectator( "MV2TrkJet1InLeadFJ","MV2_leading","", 'F' );
//   factory->AddSpectator( "MV2TrkJet2InLeadFJ","MV2_Sleading","", 'F' );
//   factory->AddVariable( "TMath::Floor((MV2TrkJet1InLeadFJ/2.+0.5)/(0.792/2.+0.5))","PCbin1","", 'F' );
   //factory->AddVariable( "(MV2TrkJet1InLeadFJ>0.577 && MV2TrkJet1InLeadFJ<0.792  )","PCbin2","", 'F' );
   //factory->AddVariable( "(MV2TrkJet1InLeadFJ<0.577 && MV2TrkJet1InLeadFJ>0.4814)","PCbin3","", 'F' );
   //factory->AddVariable( "(MV2TrkJet2InLeadFJ>0.792)","PCbinS1","", 'F' );
   //factory->AddVariable( "(MV2TrkJet2InLeadFJ>0.577 && MV2TrkJet2InLeadFJ<0.792  )","PCbinS2","", 'F' );
   //factory->AddVariable( "(MV2TrkJet2InLeadFJ<0.577 && MV2TrkJet2InLeadFJ>0.4814)","PCbinS3","", 'F' );
//try
   factory->AddVariable( "mJ", "mass", "", 'F' );
   factory->AddVariable( "sqrt((acos(cos(PhiTrkJet1InLeadFJ*3.14/180.-PhiTrkJet2InLeadFJ*3.14/180.)) * (acos(cos(PhiTrkJet1InLeadFJ*3.14/180.-PhiTrkJet2InLeadFJ*3.14/180.)))) + (EtaTrkJet1InLeadFJ-EtaTrkJet2InLeadFJ)*(EtaTrkJet1InLeadFJ-EtaTrkJet2InLeadFJ) )", "DeltaR", "", 'F' );
//   factory->AddVariable( "var3", "Variable 3", "units", 'F' );
//   factory->AddVariable( "var4", "Variable 4", "units", 'F' );

   TFile *input(0);
   TFile *input_ZZ(0);
   TFile *input_Zj(0);
   TFile *input_ttbar(0);
   TFile *input_singletop(0);
   TString fname = "/Users/francescoarmandodibello/Documents/VHbb/Ntuples/HbbSignal_decor.root";
   //TString fname = "./test_VHbb_tmva_example_multiple_background.root";
   if (!gSystem->AccessPathName( fname )) {
      // first we try to find the file in the local directory
      std::cout << "--- TMVAMulticlass   : Accessing " << fname << std::endl;
      input = TFile::Open( fname );
      input_ZZ = TFile::Open( "/Users/francescoarmandodibello/Documents/VHbb/Ntuples/Diboson_decor.root" );
      input_Zj = TFile::Open( "/Users/francescoarmandodibello/Documents/VHbb/Ntuples/Zjets_latestinDec_decor.root" );
      input_ttbar = TFile::Open( "/Users/francescoarmandodibello/Documents/VHbb/Ntuples/ttbar_0L_decor.root" );
      input_singletop = TFile::Open( "/Users/francescoarmandodibello/Documents/VHbb/Ntuples/singleTop_decor.root" );
   }
   else {
      std::cout << "Creating testdata...." << std::endl;
      gROOT->ProcessLine(".L createData.C");
      gROOT->ProcessLine("create_MultipleBackground(2000)");
      std::cout << " created tmva_example_multiple_background.root for tests of the multiclass features"<<std::endl;
      input = TFile::Open( fname );
   }
   if (!input) {
      std::cout << "ERROR: could not open data file" << std::endl;
      exit(1);
   }

   TTree *signal      = (TTree*)input->Get(   "Nominal");
   TTree *background0 = (TTree*)input_ZZ->Get("Nominal");
   TTree *background1 = (TTree*)input_Zj->Get("Nominal");
   TTree *background2 = (TTree*)input_ttbar->Get("Nominal");
   TTree *background3 = (TTree*)input_singletop->Get("Nominal");

   gROOT->cd( outfileName+TString(":/") );
   factory->AddSignalTree(signal,1.);
   factory->AddBackgroundTree(background0,1.);
   factory->AddBackgroundTree(background1,1.);
   factory->AddBackgroundTree(background2,1.);
   factory->AddBackgroundTree(background3,1.);
   factory->SetWeightExpression( "EventWeight" );

   factory->PrepareTrainingAndTestTree( "MET < 1000 && MET > 600   && MV2TrkJet1InLeadFJ>0.4814 && MV2TrkJet2InLeadFJ>0.4814  && (mJ>50) && PtTrkJet1InLeadFJ > 10 && PtTrkJet2InLeadFJ > 10 && NAdditionalCaloJets == 0","SplitMode=random:!V");
//   factory->PrepareTrainingAndTestTree( "EventWeight > -2 && MET < 400 && MET > 250 && IsTaggedTrkJet1InLeadFJ && IsTaggedTrkJet2InLeadFJ && (mJ>50) && PtTrkJet1InLeadFJ > 10 && PtTrkJet2InLeadFJ > 10 && NAdditionalCaloJets == 0","SplitMode=random:!V");
   //factory->PrepareTrainingAndTestTree( "MET > 250 && IsTaggedTrkJet1InLeadFJ && IsTaggedTrkJet2InLeadFJ && (mJ>50) && PtTrkJet1InLeadFJ > 8 && PtTrkJet2InLeadFJ > 8","nTest_Signal=1000000:nTest_Background=1000000:nTrain_Signal=1000000:nTrain_Background=1000000");

   if (Use["BDTG"]) // gradient boosted decision trees
      //factory->BookMethod( TMVA::Types::kBDT, "BDTG", "!H:!V:NTrees=1000:BoostType=Grad:Shrinkage=0.10:UseBaggedBoost:BaggedSampleFraction=0.50:nCuts=20:MaxDepth=2");
         factory->BookMethod(TMVA::Types::kBDT, "BDT",
                                         "!H:!V:NTrees=200:MaxDepth=4:BoostType=AdaBoost:AdaBoostBeta=0.15:SeparationType=GiniIndex:nCuts=100:NEventsMin=100:PruneMethod=NoPruning");
   if (Use["MLP"]) // neural network
      factory->BookMethod( TMVA::Types::kMLP, "MLP", "!H:!V:NeuronType=tanh:NCycles=1000:HiddenLayers=N+5,5:TestRate=5:EstimatorType=MSE");
   if (Use["FDA_GA"]) // functional discriminant with GA minimizer
      factory->BookMethod( TMVA::Types::kFDA, "FDA_GA", "H:!V:Formula=(0)+(1)*x0+(2)*x1+(3)*x2+(4)*x3:ParRanges=(-1,1);(-10,10);(-10,10);(-10,10);(-10,10):FitMethod=GA:PopSize=300:Cycles=3:Steps=20:Trim=True:SaveBestGen=1" );
   if (Use["PDEFoam"]) // PDE-Foam approach
      factory->BookMethod( TMVA::Types::kPDEFoam, "PDEFoam", "!H:!V:TailCut=0.001:VolFrac=0.0666:nActiveCells=500:nSampl=2000:nBin=5:Nmin=100:Kernel=None:Compress=T" );

  // Train MVAs using the set of training events
   factory->TrainAllMethods();

   // ---- Evaluate all MVAs using the set of test events
   factory->TestAllMethods();

   // ----- Evaluate and compare performance of all configured MVAs
   factory->EvaluateAllMethods();

   // --------------------------------------------------------------

   // Save the output
   outputFile->Close();

   std::cout << "==> Wrote root file: " << outputFile->GetName() << std::endl;
   std::cout << "==> TMVAClassification is done!" << std::endl;

   delete factory;

   // Launch the GUI for the root macros
   if (!gROOT->IsBatch()) TMVAMultiClassGui( outfileName );

}

int main( int argc, char** argv )
{
   // Select methods (don't look at this code - not of interest)
   TString methodList;
   for (int i=1; i<argc; i++) {
      TString regMethod(argv[i]);
      if(regMethod=="-b" || regMethod=="--batch") continue;
      if (!methodList.IsNull()) methodList += TString(",");
      methodList += regMethod;
   }
   TMVAMulticlass(methodList);
   return 0;
}
