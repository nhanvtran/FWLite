import ROOT
import copy
import sys
from math import *
from array import array
from operator import itemgetter, attrgetter

ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()

from DataFormats.FWLite import Events, Handle

ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.gROOT.ProcessLine("namespace edm {typedef edm::Wrapper<vector<float> > Wrapper<vector<float,allocator<float> > >; }");
ROOT.gROOT.ProcessLine("namespace edm {typedef edm::Wrapper<vector<double> > Wrapper<vector<double,allocator<double> > >; }");

############################################################
############################################
#            Job steering                  #
############################################
from optparse import OptionParser

parser = OptionParser()

parser.add_option('-b', action='store_true', dest='noX', default=False,
                  help='no X11 windows')

#parser.add_option('--makeCards', action='store_true', dest='makeCards', default=False,
#                  help='no X11 windows')
#
#parser.add_option('--channel',action="store",type="string",dest="channel",default="mu")
parser.add_option('--nPU',action="store",type="int",dest="nPU",default=50)
parser.add_option('--nBx',action="store",type="int",dest="nBx",default=50)
parser.add_option('--nEv',action="store",type="int",dest="nEv",default=500)
parser.add_option('--index',action="store",type="int",dest="index",default=1)



(options, args) = parser.parse_args()
############################################################
############################################################


if __name__ == '__main__':

    nEvents = options.nEv;
    nPU = options.nPU; 
    nBx = options.nBx;
    index = options.index;
    ofilename = "hists/fileOut_PU"+str(nPU)+"bx"+str(nBx)+"_"+str(options.index)+".root";

    files = []
    dirEos = "file:/eos/uscms/store/user/ntran/upgradeJet/files/";
    if nPU == 140 and nBx == 25: 
        dir = "DYToMuMu_M-20_TuneZ2star_14TeV-pythia6--Summer13-UpgradePhase1Age0START_DR61SLHCx_PU140Bx25_STAR17_61_V1A-v1/"
        files.append(dirEos+dir+"00C5D08B-F1CB-E211-9AB3-003048FFD760.root");
        files.append(dirEos+dir+"00D65CEF-CCCC-E211-8034-0025905964BC.root");
        files.append(dirEos+dir+"00DD2552-90CC-E211-B67C-003048FFD732.root");
        files.append(dirEos+dir+"02FDA665-43CC-E211-B132-0026189438FC.root");
        files.append(dirEos+dir+"040F731A-36CC-E211-902F-00261894386D.root");        
    elif nPU == 50 and nBx == 50: 
        dir = "DYToLL_M_20_TuneZ2star_14TeV_pythia6--Summer12-PU50_POSTLS161_V12-v1/"
        files.append(dirEos+dir+"0C5E2225-0C4A-E211-8C32-003048D462DA.root");
    elif nPU == 50 and nBx == 25: 
        dir = "DYToLL_M_20_TuneZ2star_14TeV_pythia6--Summer12-PU50bx25_POSTLS161_V12-v1/"
        files.append(dirEos+dir+"0017DAB9-C14A-E211-B2CF-0030487E0A2D.root");
    elif nPU == 20 and nBx == 50: 
        dir = "DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball--Summer12_DR53X-PU_S10_START53_V7A-v1/"
        files.append(dirEos+dir+"00037C53-AAD1-E111-B1BE-003048D45F38.root");
    elif nPU == 70 and nBx == 25:
        dir = "GJet_Pt40_doubleEMEnriched_TuneZ2star_14TeV-pythia6--UpgradePhase1Age0DES_DR61SLHCx_PU70bx25_DES17_61_V5-v1/"
        files.append(dirEos+dir+"0204D05E-F6EF-E211-B304-002354EF3BE1.root");
        files.append(dirEos+dir+"047BA908-4AF0-E211-B9B4-002618943852.root"); 
        files.append(dirEos+dir+"04C4DEEF-2FF0-E211-9C7A-00261894395C.root");         
        files.append(dirEos+dir+"04DB1901-3BF0-E211-9DCA-00248C55CC3C.root");                 
    else:
        print "invalid file settings...";
        sys.exit();
        
    events = Events( files );

    # loop over events
    count = 0
    ntotal = events.size()
    print "Nevents = "+str(ntotal)
    print "Start looping"

    photonHandle = Handle( "vector<reco::Photon>" );
    photonLabel = "photons";

    calojetHandle = Handle( "vector<reco::CaloJet>" );
    calojetLabel = "ak5CaloJets";

    pfjetHandle = Handle( "vector<reco::PFJet>" );
    pfjetLabel = "ak5PFJets";

    genjetHandle = Handle( "vector<reco::GenJet>" );
    genjetLabel = "ak5GenJets";
    
    rechitHandle_hbhe = Handle( "edm::SortedCollection<HBHERecHit,edm::StrictWeakOrdering<HBHERecHit> >" );
    rechitHandle_hf = Handle( "edm::SortedCollection<HFRecHit,edm::StrictWeakOrdering<HFRecHit> >" );    
    rechitLabel = "reducedHcalRecHits";
    rechitLabel2_hbhe = "hbhereco";
    rechitLabel2_hf = "hfreco";    

    calotowerHandle = Handle( "edm::SortedCollection<CaloTower,edm::StrictWeakOrdering<CaloTower> >" );
    calotowerLabel = "towerMaker";

    ## some pileup information
    pileupHandle = Handle( "vector<PileupSummaryInfo>" );
    pileupLabel = "addPileupInfo";
    
    ##output
    fileOut = ROOT.TFile(ofilename,"RECREATE");
    histograms = [];
    histograms.append( ROOT.TH1F("h_calojet_pt","; pT; N",40,0,100) );                   # 0th
    histograms.append( ROOT.TH1F("h_calojet_eta","; eta; N",100,-5,5) );
    histograms.append( ROOT.TH1F("h_pfjet_pt","; pT; N",40,0,100) );
    histograms.append( ROOT.TH1F("h_pfjet_eta","; eta; N",100,-5,5) );
    histograms.append( ROOT.TH1F("h_genjet_pt","; pT; N",40,0,100) );
    histograms.append( ROOT.TH1F("h_genjet_eta","; eta; N",100,-5,5) );                  # 5th

    histograms.append( ROOT.TH1F("h_n_rechits","; N hbhe rechits; N",100,0,1000) );
    histograms.append( ROOT.TH1F("h_rechits_e","; energy; N",40,0,20) );        
    histograms.append( ROOT.TH1F("h_rechits_ieta","; ieta; N",100,-50,50) );
    histograms.append( ROOT.TH1F("h_rechits_time","; time; N",50,-50,50) );
        
    histograms.append( ROOT.TH1F("h_n_hfrechits","; N hf rechits; N",100,0,1000) );      #10th
    histograms.append( ROOT.TH1F("h_hfrechits_e","; energy; N",50,0,100) );        
    histograms.append( ROOT.TH1F("h_hfrechits_ieta","; ieta; N",100,-50,50) );
    histograms.append( ROOT.TH1F("h_hfrechits_time","; time; N",50,-50,50) );
        
    histograms.append( ROOT.TH1F("h_n_calotowers","; N calotowers; N",100,0,5000) );
    histograms.append( ROOT.TH1F("h_calotowers_pt","; pT; N",50,0,100) );                 #15th
    histograms.append( ROOT.TH1F("h_calotowers_eta","; eta; N",100,-5,5) );

    histograms.append( ROOT.TH2F("h_calotowers_etaVe","; eta; e",100,-5,5,50,0,200) );
    histograms.append( ROOT.TH2F("h_rechits_timeVe","; time; e",50,-50,50,50,0,100) );
    histograms.append( ROOT.TH2F("h_rechits_ietaVe","; ieta; e",100,-50,50,50,0,100) );
    histograms.append( ROOT.TH2F("h_hfrechits_timeVe","; time; e",50,-50,50,50,0,100) );    #20th
    histograms.append( ROOT.TH2F("h_hfrechits_ietaVe","; ieta; e",100,-50,50,50,0,100) );
    histograms.append( ROOT.TH2F("h_calotowers_ietaViphi","; ieta; iphi",100,-50,50,80,0,80) );
    histograms.append( ROOT.TH2F("h_calotowers_ietaVhadEm","; ieta; hadronic energy",100,-50,50,50,0,200) );    
    histograms.append( ROOT.TH2F("h_rechits_ietaVdepth","; ieta; depth",100,-50,50,5,0,5) );    
    histograms.append( ROOT.TH2F("h_hfrechits_ietaVdepth","; ieta; depth",100,-50,50,5,0,5) ); #25th   
    histograms.append( ROOT.TH1F("h_calotowers_etaVsume","; eta; sum e",100,-5,5) );
    histograms.append( ROOT.TH1F("h_calotowers_etaVsumEt","; eta; sum et",100,-5,5) );
    histograms.append( ROOT.TH1F("h_calotowers_etaVsumEMEt","; eta; sum EM et",100,-5,5) );
    histograms.append( ROOT.TH1F("h_calotowers_etaVsumHCEt","; eta; sum HC et",100,-5,5) );
    
    for i in range(1,101):
        histograms[26].SetBinContent(i,0.);
    
    #for event in events:
    ctr = 0;
    for event in events:

        if ctr == nEvents: break;
        if ctr % 500 == 0: print "ctr = ", ctr;
        ctr = ctr + 1;

        if ctr < 10:
            event.getByLabel( pileupLabel, pileupHandle );
            pileupInfos = pileupHandle.product();
            print "pileupInfos.size() = ",pileupInfos.size();
            for pv in pileupInfos:
                print "PU INFO: bx = ",pv.getBunchCrossing(),", nPU = ",pv.getPU_NumInteractions();      
        
        # photons
        #print "photons..."
        event.getByLabel( photonLabel, photonHandle );
        photons = photonHandle.product();

        # calo jets
        #print "calo jets..."    
        event.getByLabel( calojetLabel, calojetHandle );
        calojets = calojetHandle.product();

        # pf jets
        #print "pf jets..."    
        event.getByLabel( pfjetLabel, pfjetHandle );
        pfjets = pfjetHandle.product();

        # gen jets
        event.getByLabel( genjetLabel, genjetHandle );
        genjets = genjetHandle.product();

        # calo towers
        #print "calo towers..."             
        event.getByLabel( calotowerLabel, calotowerHandle );
        calotowers = calotowerHandle.product();
        
        # hbhe rechits
        #print "rechits..."    
        event.getByLabel( rechitLabel, rechitLabel2_hbhe, rechitHandle_hbhe );
        hbherechits = rechitHandle_hbhe.product();        
        event.getByLabel( rechitLabel, rechitLabel2_hf, rechitHandle_hf );        
        hfrechits = rechitHandle_hf.product();   
             
#        print "-----------------------------------"
#        print "photon size = ",photons.size();
#        print "calojets size = ",calojets.size(); 
#        print "pfjets size = ",pfjets.size();           
#        print "hbherechits size = ",hbherechits.size();           
#        print "calo tower size = ",calotowers.size();           

        for calojet in calojets:
            if calojet.pt() > 15:
                histograms[0].Fill( calojet.pt() );
                histograms[1].Fill( calojet.eta() );
                    
        for pfjet in pfjets:
            if pfjet.pt() > 15:
                histograms[2].Fill( pfjet.pt() );
                histograms[3].Fill( pfjet.eta() );
            
        for genjet in genjets:
            if genjet.pt() > 15:
                histograms[4].Fill( genjet.pt() );
                histograms[5].Fill( genjet.eta() );

#        print "n rechits = ", hbherechits.size();
        histograms[6].Fill( hbherechits.size() );
        for hbherechit in hbherechits:
                histograms[7].Fill( hbherechit.energy() );
                histograms[8].Fill( hbherechit.id().ieta() );
                histograms[9].Fill( hbherechit.time() );
                histograms[18].Fill( hbherechit.time(), hbherechit.energy() );
                histograms[19].Fill( hbherechit.id().ieta(), hbherechit.energy() );
                histograms[24].Fill( hbherechit.id().ieta(), hbherechit.id().depth() );

        histograms[10].Fill( hfrechits.size() );
        for hfrechit in hfrechits:
                histograms[11].Fill( hfrechit.energy() );
                histograms[12].Fill( hfrechit.id().ieta() );
                histograms[13].Fill( hfrechit.time() );
                histograms[20].Fill( hfrechit.time(), hfrechit.energy() );
                histograms[21].Fill( hfrechit.id().ieta(), hfrechit.energy() );
                histograms[25].Fill( hfrechit.id().ieta(), hfrechit.id().depth() );
                

#        print "n calotowers = ", calotowers.size();    
        histograms[14].Fill( calotowers.size() );
        for calotower in calotowers:
                histograms[15].Fill( calotower.pt() );
                histograms[16].Fill( calotower.eta() );
                histograms[17].Fill( calotower.eta(), calotower.energy() );
                histograms[22].Fill( calotower.ieta(), calotower.iphi() );                                
                histograms[23].Fill( calotower.ieta(), calotower.hadEnergy() ); 
                
                if calotower.eta() < 5 and calotower.eta() > -5:
                    curBin = histograms[26].FindBin(calotower.eta());
                    histograms[26].SetBinContent( curBin, histograms[26].GetBinContent(curBin) + calotower.energy() );
                    histograms[27].SetBinContent( curBin, histograms[27].GetBinContent(curBin) + calotower.et(0) );
                    histograms[28].SetBinContent( curBin, histograms[28].GetBinContent(curBin) + calotower.emEt() );
                    histograms[29].SetBinContent( curBin, histograms[29].GetBinContent(curBin) + calotower.hadEt() );
                        
    fileOut.cd();
    for i in range(len(histograms)):
        #histograms[i].Scale( 1./histograms[i].Integral() );
        histograms[i].Write();
    fileOut.Close();






