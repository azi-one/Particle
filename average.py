import ROOT as r
import numpy as np
from glob import glob
from array import array
from ROOT import TGraph2D

average=[]
min=[]

hundred=np.arange(0,101,1)
points=0
for percent in hundred:
    ArPer=100-percent
    XePer=percent
    file='lyAr'+str(ArPer)+'Xe'+str(XePer)+'.root'
    f=r.TFile(file,"READ")
    t=f.Get("Phztotal")
    average.append((t.Integral())/(t.GetEntries()))
    min.append(t.GetBinContent(t.GetMinimumBin()))
    points+=1

global light, Min
c1=r.TCanvas("c1","Total_Light_Yield")
c1.cd()
light=r.TGraph(int(points),array("d",hundred),array("d",average))
light.SetTitle("Average Light Yield vs Xe Light Percent; Percent of Xe Light; Average Light Yield")
light.SetLineColor(4)
light.Draw()
c1.Draw()
c1.SaveAs("averageLY.png")

c2=r.TCanvas("c2","Miminum")
c2.cd()
Min=r.TGraph(int(points),array("d",hundred),array("d",min))
Min.SetTitle("Minimum light Yield ; Percent of Xe light; Minimum  light Yield")
Min.SetLineColor(4)
Min.Draw()
c2.Draw()
c2.SaveAs("MinLY.png")


