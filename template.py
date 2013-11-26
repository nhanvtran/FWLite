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

    files = []
    dirEos = "file:/eos/uscms/store/user/ntran/upgradeJet/files/";
    dir = "DYToMuMu_M-20_TuneZ2star_14TeV-pythia6--Summer13-UpgradePhase1Age0START_DR61SLHCx_PU140Bx25_STAR17_61_V1A-v1/"
    files.append(dirEos+dir+"00C5D08B-F1CB-E211-9AB3-003048FFD760.root");
    files.append(dirEos+dir+"00D65CEF-CCCC-E211-8034-0025905964BC.root");
    files.append(dirEos+dir+"00DD2552-90CC-E211-B67C-003048FFD732.root");
    files.append(dirEos+dir+"02FDA665-43CC-E211-B132-0026189438FC.root");
    files.append(dirEos+dir+"040F731A-36CC-E211-902F-00261894386D.root");        
        
    events = Events( files );

    # loop over events
    count = 0
    ntotal = events.size()
    print "Nevents = "+str(ntotal)
    print "Start looping"

    calojetHandle = Handle( "vector<reco::CaloJet>" );
    calojetLabel = "ak5CaloJets";

    pfjetHandle = Handle( "vector<reco::PFJet>" );
    pfjetLabel = "ak5PFJets";

    genjetHandle = Handle( "vector<reco::GenJet>" );
    genjetLabel = "ak5GenJets";
            
    #for event in events:
    ctr = 0;
    for event in events:

        if ctr == nEvents: break;
        if ctr % 500 == 0: print "ctr = ", ctr;
        ctr = ctr + 1;

        # PU info
        if ctr < 10:
            event.getByLabel( pileupLabel, pileupHandle );
            pileupInfos = pileupHandle.product();
            print "pileupInfos.size() = ",pileupInfos.size();
            for pv in pileupInfos:
                print "PU INFO: bx = ",pv.getBunchCrossing(),", nPU = ",pv.getPU_NumInteractions();      
        
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

        for calojet in calojets:
            if calojet.pt() > 15:
                print calojet.pt();
                    
        for pfjet in pfjets:
            if pfjet.pt() > 15:
                print pfjet.pt();
            
        for genjet in genjets:
            if genjet.pt() > 15:
                print genjet.pt();
                                    
    fileOut.cd();
    for i in range(len(histograms)):
        #histograms[i].Scale( 1./histograms[i].Integral() );
        histograms[i].Write();
    fileOut.Close();






