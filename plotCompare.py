import ROOT
import copy
from math import *
from array import array

ROOT.gROOT.ProcessLine(".L ~/tdrstyle.C");
ROOT.setTDRStyle();
ROOT.gStyle.SetPadLeftMargin(0.16);
ROOT.gStyle.SetPadRightMargin(0.16);
ROOT.gStyle.SetPalette(1);


if __name__ == '__main__':
    
    normalize = False;

    scenarios = ["PU50bx25","PU50bx50","PU140bx25","PU20bx50","PU70bx25"];

    file1 = ROOT.TFile("hists/fileOut_"+scenarios[0]+"_0.root");
    file2 = ROOT.TFile("hists/fileOut_"+scenarios[1]+"_0.root");
    file3 = ROOT.TFile("hists/fileOut_"+scenarios[2]+"_0.root");
    file4 = ROOT.TFile("hists/fileOut_"+scenarios[3]+"_0.root");
    file5 = ROOT.TFile("hists/fileOut_"+scenarios[4]+"_0.root");
        
    names = ["h_calojet_pt","h_calojet_eta","h_pfjet_pt","h_pfjet_eta","h_rechits_time","h_rechits_e","h_rechits_ieta","h_hfrechits_time","h_hfrechits_e","h_hfrechits_ieta","h_calotowers_pt","h_calotowers_eta","h_calotowers_etaVe","h_rechits_timeVe","h_rechits_ietaVe","h_hfrechits_timeVe","h_hfrechits_ietaVe","h_calotowers_ietaViphi","h_calotowers_ietaVhadEm","h_rechits_ietaVdepth","h_hfrechits_ietaVdepth","h_calotowers_etaVsume","h_calotowers_etaVsumEt","h_calotowers_etaVsumEMEt","h_calotowers_etaVsumHCEt"];
    
    for i in range(len(names)):
        
        h1 = file1.Get(names[i]);
        h2 = file2.Get(names[i]);
        h3 = file3.Get(names[i]);
        h4 = file4.Get(names[i]);
        h5 = file5.Get(names[i]);

        print "h1.GetDimension() = ", h1.GetDimension();


        if h1.GetDimension() == 1:
        
            h1.SetLineColor( 2 );
            h2.SetLineColor( 4 );
            h3.SetLineColor( 6 );
            h4.SetLineColor( 3 );
            h5.SetLineColor( 7 ); 
            
            h1.SetLineWidth( 2 ); h2.SetLineWidth( 2 ); h3.SetLineWidth( 2 ); h4.SetLineWidth( 2 ); h5.SetLineWidth( 2 );
            
            if normalize: 
                h1.Scale(1./h1.Integral());
                h2.Scale(1./h2.Integral());
                h3.Scale(1./h3.Integral());
                h4.Scale(1./h4.Integral());
                h5.Scale(1./h5.Integral());            
                h1.GetYaxis().SetTitle("normalized distribution");
                h2.GetYaxis().SetTitle("normalized distribution");
                h3.GetYaxis().SetTitle("normalized distribution");
                h4.GetYaxis().SetTitle("normalized distribution");
                h5.GetYaxis().SetTitle("normalized distribution");            
                                                                
            leg = ROOT.TLegend(0.7,0.7,0.9,0.9);
            leg.SetBorderSize(0);
            leg.SetFillStyle(0);
            leg.AddEntry(h4,"20  PU, 50 ns","l");
            leg.AddEntry(h1,"50  PU, 25 ns","l");
            leg.AddEntry(h2,"50  PU, 50 ns","l");
            leg.AddEntry(h5,"70  PU, 25 ns","l");
            leg.AddEntry(h3,"140 PU, 25 ns","l");
                            
            canTmp = ROOT.TCanvas("c_"+names[i],"c_"+names[i],1000,800);
            h3.SetMaximum( 1.2*max( h1.GetMaximum(), h2.GetMaximum(), h3.GetMaximum(), h4.GetMaximum(), h5.GetMaximum() ) );
            h3.Draw();
            h5.Draw("sames");
            h2.Draw("sames");        
            h1.Draw("sames");  
            h4.Draw("sames");        
                  
            leg.Draw();
            if normalize: canTmp.SaveAs("figs/"+names[i]+"_norm.eps");
            else: canTmp.SaveAs("figs/"+names[i]+".eps");
    
        if h1.GetDimension() == 2:
            
            can1 = ROOT.TCanvas("can1"+names[i],"can1"+names[i],1000,800);
            h1.Draw("COLZ");
            can1.SaveAs("figs/"+names[i]+"_"+scenarios[0]+".eps");
            
            can2 = ROOT.TCanvas("can2"+names[i],"can2"+names[i],1000,800);
            h2.Draw("COLZ");
            can2.SaveAs("figs/"+names[i]+"_"+scenarios[1]+".eps");
            
            can3 = ROOT.TCanvas("can3"+names[i],"can3"+names[i],1000,800);
            h3.Draw("COLZ");
            can3.SaveAs("figs/"+names[i]+"_"+scenarios[2]+".eps");
            
            can4 = ROOT.TCanvas("can4"+names[i],"can4"+names[i],1000,800);
            h4.Draw("COLZ");
            can4.SaveAs("figs/"+names[i]+"_"+scenarios[3]+".eps");
            
            can5 = ROOT.TCanvas("can5"+names[i],"can5"+names[i],1000,800);
            h5.Draw("COLZ");
            can5.SaveAs("figs/"+names[i]+"_"+scenarios[4]+".eps");                                                                                                                                                                                    
        
        del h1;
        del h2;
        del h3;
        del h4;
        del h5;
        
        
#        /DYToLL_M_20_TuneZ2star_14TeV_pythia6/Summer12-PU50bx25_POSTLS161_V12-v1/AODSIM
#        /DYToLL_M_20_TuneZ2star_14TeV_pythia6/Summer12-PU50bx25_POSTLS161_V12-v2/GEN-SIM-RAW-RECO
        
        