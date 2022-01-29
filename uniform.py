import ROOT as r
import numpy as np
from glob import glob
import array
from ROOT import TGraph2D
meanX=[]
meanY=[]
rmsX=[]
rmsY=[]
points=0
hundred=np.linspace(0,1,100)
for percent in hundred:
    ArPer=100-percent
    XePer=percent
    file='lyAr'+str(ArPer)+'Xe'+str(XePer)+'.root'
    f=r.TFile(file,"READ")
    meanX.append(f.Phztotal.GetMean(1))
    meanY.append(f.Phztotal.GetMean(2))
    rmsX.append(f.Phztotal.GetRMS(1))
    rmsY.append(f.Phztotal.GetRMS(2))
    points+=1


MeanXCan=r.TCanvas("MeanX","Mean_X_canvas")
MeanXCan.cd()
XMean=r.TGraph(int(points),array.array('d',hundred),array.array('d',meanX))
XMean.SetTitle("Mean X vs. Xe Percent; Percent of Xe; Mean x (m)")
XMean.SetLineColor(4)
XMean.Draw()
MeanXCan.SaveAs('MeanX.png')

MeanYCan=r.TCanvas("MeanY","Mean_Y_canvas")
MeanYCan.cd()
YMean=r.TGraph(int(points),array.array('d',hundred),array.array('d',meanY))
YMean.SetTitle("Mean Y vs. Xe Percent; Percent of Xe; Mean Y (m)")
YMean.SetLineColor(2)
YMean.Draw()
MeanYCan.SaveAs('MeanY.png')

Mean2DCan=r.TCanvas("Mean2D","Mean_2D_canvas")
Mean2DCan.cd()
Mean2D=TGraph2D(int(points),array.array('d',hundred),array.array('d',meanX),array.array('d',meanY))
Mean2D.GetXaxis().SetTitle("Percent of Xe")
Mean2D.GetYaxis().SetTitle("Mean X (m)")
Mean2D.GetZaxis().SetTitle("Mean Y (m)")
Mean2D.Draw()
Mean2DCan.SaveAs('Mean2D.png')

Mean2DErrorCan=r.TCanvas("Mean2D","Mean_2D_Error_canvas")
Mean2DErrorCan.cd()
Mean2DError=r.TGraph2DErrors(int(points),array.array('d',hundred),array.array('d',meanX),array.array('d',meanY),array.array('d',rmsX),array.array('d',rmsY))
Mean2DError.GetXaxis().SetTitle("Percent of Xe")
Mean2DError.GetYaxis().SetTitle("Mean X (m)")
Mean2DError.GetZaxis().SetTitle("Mean Y (m)")
Mean2DError.Draw()
Mean2DErrorCan.SaveAs('Mean2DError.png')

RMSXCan=r.TCanvas("RMSX","RMS_X_canvas")
RMSXCan.cd()
XRMS=r.TGraph(int(points),array.array('d',hundred),array.array('d',rmsX))
XRMS.SetTitle("RMS X vs. Xe Percent; Percent of Xe; RMS x (m)")
XRMS.SetLineColor(38)
XRMS.Draw()
RMSXCan.SaveAs('RMSX.png')

RMSYCan=r.TCanvas("RMSY","RMS_Y_canvas")
RMSYCan.cd()
YRMS=r.TGraph(int(points),array.array('d',hundred),array.array('d',rmsY))
YRMS.SetTitle("RMS Y vs. Xe Percent; Percent of Xe; RMS y (m)")
YRMS.SetLineColor(46)
YRMS.Draw()
RMSYCan.SaveAs('RMSY.png')

RMS2DCan=r.TCanvas("RMS2D","RMS_2D_canvas")
RMS2DCan.cd()
RMS2D=TGraph2D(int(points),array.array('d',hundred),array.array('d',rmsX),array.array('d',rmsY))
RMS2D.GetXaxis().SetTitle("Percent of Xe")
RMS2D.GetYaxis().SetTitle("RMS X (m)")
RMS2D.GetZaxis().SetTitle("RMS Y (m)")
RMS2D.Draw()
RMS2DCan.SaveAs('RMS2D.png')
