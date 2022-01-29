import ROOT as r
import numpy as np
from glob import glob
			
def Load(number,channel,LineColor):
	import ROOT as r
	import numpy as np
	from glob import glob
	file='processed/Run'+str(number)+'*.root'
	filename=glob(file)
	globals()['f'+str(number)]=r.TFile(filename[0],'READ')
	globals()['t'+str(number)]=globals()['f'+str(number)].Get('Events')
	#return globals()['f'+str(number)], globals()['t'+str(number)] 
	histname='h'+str(number)
	channelname='vMax_2881_'+str(channel)
	globals()[histname]=r.TH1D('h{}'.format(number),'Run{} channel{};Pulse Height [mV]; Number of Pulses'.format(number,channel),100,0,500)
	for i in globals()['t'+str(number)]:
		globals()[histname].Fill(i.vMax_2881_1)
 	globals()[histname].SetLineColor(LineColor)
	
def overlay(number1,channel=1):
	import os
	overlayCan=r.TCanvas("overlayCan","overlay_plot_canvas")
	overlayCan.cd()
	LineColor=1
	for i in number1:
		Load(i,channel,LineColor)
        	#first=os.popen("cat processed/Run{}*.txt | grep waveform | head -1".format(i)).read()
                #Voltage=first.split()[3]
                histname='h'+str(i)
		globals()[histname].SetTitle('Run{}'.format(i))
		globals()[histname].SetLineColor(LineColor)
		globals()[histname].Draw("same")
		LineColor+=1
        leg=r.TLegend()
        leg=overlayCan.BuildLegend(0.55,0.7,0.9,0.9)
        r.gStyle.SetOptStat(0)
        overlayCan.SetGrid()
        overlayCan.SetLogy()
        overlayCan.Draw()

def scale(number1,number2,channel=1):
	import os
	scaleCan=r.TCanvas("scaleCan","scale_plot_canvas")
	scaleCan.cd()
	LineColor=1
	Load(number2,channel,LineColor)
	first2=os.popen("cat processed/Run{}*.txt | grep waveform | head -1".format(number2)).read()
	last2=os.popen("cat processed/Run{}*.txt | grep waveform | tail -1".format(number2)).read()
	firsttime2=first2.split()[4]
	lasttime2=last2.split()[4]
	Voltage2=first2.split()[3]
	TotalTime2=float(lasttime2)-float(firsttime2)
	histname2='h'+str(number2)
	globals()[histname2].SetTitle('Run{} {}V channel {}; Pulse Height [mV]; Number of Pulses'.format(number2,Voltage2,channel))
	globals()[histname2].Draw()
	for i in number1:
		LineColor+=1
		Load(i,channel,LineColor)
		first1=os.popen("cat processed/Run{}*.txt | grep waveform | head -1".format(i)).read()
		last1=os.popen("cat processed/Run{}*.txt | grep waveform | tail -1".format(i)).read()
		firsttime1=first1.split()[4]
		lasttime1=last1.split()[4]
		Voltage1=first1.split()[3]
		TotalTime1=float(lasttime1)-float(firsttime1)
		ScaleFactor=TotalTime2/TotalTime1
		histname1='h'+str(i)
		scalehistname='sh'+str(i)+'_'+str(number2)
		globals()[scalehistname]=globals()[histname1].Clone()
		globals()[scalehistname].Scale(ScaleFactor)
		globals()[scalehistname].SetTitle('Scaled Run{} {}V'.format(i, Voltage1))
		globals()[scalehistname].Draw("same")
	leg=r.TLegend()
	leg=scaleCan.BuildLegend(0.55,0.7,0.9,0.9)
	r.gStyle.SetOptStat(0)
	scaleCan.SetGrid()
	scaleCan.SetLogy()
	scaleCan.Draw()

	
def scan(number,voltage,channel=1):
	import ROOT as r
        import numpy as np
        from glob import glob
	scanCan=r.TCanvas('scanCan','scan_canvas')
        scanCan.cd()
	color=1
	for Run in number:
	        file='processed/Run'+str(Run)+'*.root'
	        filename=glob(file)
	        globals()['f'+str(Run)]=r.TFile(filename[0],'READ')
	        globals()['t'+str(Run)]=globals()['f'+str(Run)].Get('Events')
		for i in voltage:
			channelname='vMax_2881_'+str(channel)
			histname='h'+str(Run)+'_'+str(i)
			globals()[histname]=r.TH1D('h{}_{}'.format(Run,i),'Run{} {}V Channel {}; Pulse Height [mV]; Number of Pulses'.format(Run,i,channel),100,0,500)
			globals()[histname].SetLineColor(color)
			color+=1
			globals()['t'+str(Run)].Draw('{}>>{}'.format(channelname,histname),'bias_voltage=={}'.format(i),'same')
	leg=r.TLegend()
	leg=scanCan.BuildLegend(0.55,0.7,0.9,0.9)
	r.gStyle.SetOptStat(0)
 	scanCan.SetGrid()
	scanCan.SetLogy()
	scanCan.Draw()

def scan2(number,voltage,channel=1):
        import ROOT as r
        import numpy as np
        from glob import glob
        scanCan=r.TCanvas('scanCan','scan_canvas_2880')
        scanCan.cd()
        color=1
        for Run in number:
                file='processed/Run'+str(Run)+'*.root'
                filename=glob(file)
                globals()['f'+str(Run)]=r.TFile(filename[0],'READ')
                globals()['t'+str(Run)]=globals()['f'+str(Run)].Get('Events')
                for i in voltage:
                        channelname='vMax_2880_'+str(channel)
                        histname='h'+str(Run)+'_'+str(i)
                        globals()[histname]=r.TH1D('h{}_{}'.format(Run,i),'Run{} {}V Channel {}; Pulse Height [mV]; Number of Pulses'.format(Run,i,channel),100,0,500)
                        globals()[histname].SetLineColor(color)
                        color+=1
                        globals()['t'+str(Run)].Draw('{}>>{}'.format(channelname,histname),'bias_voltage=={}'.format(i),'same')
        leg=r.TLegend()
        leg=scanCan.BuildLegend(0.55,0.7,0.9,0.9)
        r.gStyle.SetOptStat(0)
        scanCan.SetGrid()
        scanCan.SetLogy()
        scanCan.Draw()

def scanchannel(number,voltage,low=50,high=480,DRS=2881):
	import ROOT as r
	import numpy as np
	from glob import glob
	file='processed/Run'+str(number)+'*.root'
	filename=glob(file)
	globals()['f'+str(number)]=r.TFile(filename[0],'READ')
	globals()['t'+str(number)]=globals()['f'+str(number)].Get('Events')
	scanchannelCan=r.TCanvas('scanchannelCan','scan_channel_DRS{}'.format(DRS))
	scanchannelCan.cd()
	color=1
	channel=[1,2,3,4]
	print(filename[0],'DRS'+str(DRS))
	for i in channel:
		channelname='vMax_{}_'.format(DRS)+str(i)
		histname='h'+str(number)+'_'+str(i)
		globals()[histname]=r.TH1D('h{}_{}'.format(number,i),'Run{} {}V Channel {}; Pulse Height [mV]; Number of Pulses'.format(number,voltage,i),100,0,1000)
		globals()[histname].SetLineColor(color)
		color+=1
		globals()['t'+str(number)].Draw('{}>>{}'.format(channelname,histname),'bias_voltage=={}'.format(voltage),'same')
		lowbin=globals()[histname].FindBin(low)
		highbin=globals()[histname].FindBin(high)
		totalbin=globals()[histname].Integral(lowbin,highbin)
		print("Total number of entries within range [{},{}] in channel {} is {}".format(low,high,i,totalbin)) 
	leg=r.TLegend()
	leg=scanchannelCan.BuildLegend(0.55,0.7,0.9,0.9)
	r.gStyle.SetOptStat(0)
	scanchannelCan.SetGrid()
	scanchannelCan.SetLogy()
	scanchannelCan.Draw()
	

def scanchannel2(number,channel=[1,2,3,4],DRS=2988,lowend=0,highend=1000,low=0,high=1000):
        import ROOT as r
        import numpy as np
        from glob import glob
        file='processed/Run'+str(number)+'*.root'
        filename=glob(file)
        globals()['f'+str(number)]=r.TFile(filename[0],'READ')
        globals()['t'+str(number)]=globals()['f'+str(number)].Get('Events')
        scanchannelCan=r.TCanvas('scanchannelCan','scan_channel_canvas_{}'.format(DRS))
        scanchannelCan.cd()
        color=1
	print(filename[0],"DRS {}".format(DRS))
        for i in channel:
                channelname='vMax_{}_{}'.format(DRS,i)
                histname='h'+str(number)+'_'+str(i)
                globals()[histname]=r.TH1D('h{}_{}'.format(number,i),'Run{} Channel {}; Pulse Height [mV]; Number of Pulses'.format(number,i),100,lowend,highend)
                globals()[histname].SetLineColor(color)
                color+=1
                globals()['t'+str(number)].Draw('{}>>{}'.format(channelname,histname),"",'same')
                lowbin=globals()[histname].FindBin(low)
                highbin=globals()[histname].FindBin(high)
                totalbin=globals()[histname].Integral(lowbin,highbin)
                print("Total number of entries within range [{},{}] in channel {} is {}".format(low,high,i,totalbin))
        leg=r.TLegend()
        leg=scanchannelCan.BuildLegend(0.55,0.7,0.9,0.9)
        r.gStyle.SetOptStat(0)
        scanchannelCan.SetGrid()
        scanchannelCan.SetLogy()
        scanchannelCan.Draw()

def singlescan(number,voltage,channel=1):
	import ROOT as r
	import numpy as np
	from glob import glob
	for i in number:
		file='processed/Run'+str(number)+'*.root'
		filename=glob(file)
		globals()['f'+str(number)]=r.TFile(filename[0],'READ')
		globals()['t'+str(number)]=globals()['f'+str(number)].Get('Events')
	

def entry(number,voltage,channel=1,vMaxcut=20):
	import ROOT as r
	import numpy as np
	from glob import glob
	file='processed/Run'+str(number)+'*.root'
	filename=glob(file)
	globals()['f'+str(number)]=r.TFile(filename[0],'READ')
	globals()['t'+str(number)]=globals()['f'+str(number)].Get('Events')
	entryCan=r.TCanvas('entryCan','vMax_Entry_canvas')
	entryCan.cd()
	channelname='vMax_2881_'+str(channel)
	globals()['t'+str(number)].Draw("{}:Entry$>>h1".format(channelname),"{}>{}&&bias_voltage=={}".format(channelname,vMaxcut,voltage),"COLZ")
	entryCan.Draw()		

def current(csv,voltage):
	import ROOT as r
	import numpy as np
	import array
	from ROOT import TGraph
	with open(csv,'r')as f:
		lines=f.readlines()
		Voltage=[]
		Current=[]
		Time=[]
		for i in range(len(lines)-1):
			first=abs(float(lines[i+1].split(',')[0]))
			if first==voltage:
				Voltage.append(abs(float(lines[i+1].split(',')[0])))
        			Current.append(abs(float(lines[i+1].split(',')[1])))
        			Time.append(abs(float(lines[i+1].split(',')[2])))
	timeCan=r.TCanvas('timeCan','Current Stability')
	timeCan.cd()
	global graph
	graph=TGraph(len(Time),array.array('d',np.array(Time)-Time[0]),array.array('d',Current))
	graph.SetMarkerColor(4)
	graph.SetLineColor(4)
	graph.SetTitle('KeithleyCurrentMonitor {}V;Time(s);Current(A) '.format(Voltage[0]))
	graph.Draw()
	timeCan.Draw()


def heightarea(number,channel=1):
	import ROOT as r
	import numpy as np
	from glob import glob
        

def timediff(number,channel=1):
	import ROOT as r
	import numpy as np
	from glob import glob
	import os
	import array
	channelname="2881_"+str(channel)
	waveform=os.popen("cat processed/Run{}*.txt | grep {}".format(number,channelname)).read().split("\n")
	vMax=[]
	Time=[]
	for i in range(len(waveform)-1):
		if waveform[i].split()[2]==channelname:
			vMax.append(float(waveform[i].split()[6]))
			Time.append(float(waveform[i].split()[4]))
	Timediff=Time-np.roll(Time,1)
	Timediff[0]=0
	Timediff=array.array("d",Timediff)
	vMax=array.array("d",vMax)
	#f=r.TFile("vMaxTimeDiff.root","RECREATE")
	#t=r.TTree("Events","Events")
	#t.Branch("timediff",Timediff,"TimeDiff/D")
	#t.Branch("vMax",vMax,"vMax/D")
	#t.Fill()
	#t.Write()
	#f.Close()
	#timeCan=r.TCanvas("timeCan","time_canvas")
	#timeCan.cd()
	#global graph
	#graph=r.TGraph(len(Time),array.array("d",Time),array.array("d",vMax))
	#graph.Draw()
	#timeCan.Draw()	
#	timediffCan=r.TCanvas("timediffCan","time_diff_canvas")
#	timediffCan.Divide(1,2)
	#obj=t.Get("Events")
	#obj.Draw("vMax:timediff")
	#timediffCan.Draw()
	#for i in range(len(vMax)):
	#for j in range(len(Timeiff)):
	global histvMax,histTimeDiff,hist2D
	histvMax=r.TH1D("vMax","vMax_Historgram",100,0,500)
	histTimeDiff=r.TH1D("TimeDiff","Time_Diff_Histogram; Time Difference(s)",100,0,2)
	#for i in vMax:
	#	histvMax.Fill(i)
	for j in Timediff:
		histTimeDiff.Fill(j)
	#histTimeDiff.Draw()
	#timediffCan.Draw()
	#vMaxCan=r.TCanvas("vMaxCan","vMax_Canvas")
	#vMaxCan.cd()
	#histvMax.Draw()
	#vMaxCan.Draw()
	#hist2D=r.TH2D("hist2d","vMax_Time_Histogram;Time Difference(s); Pulse Height [mV]; Number of Pulses",100,0,500,100,0,2)
	#for i in Timediff:
	#	for j in vMax:
	#		hist2D.Fill(i,j)
	#timediffCan.cd(1)
	#hist2D.Draw("Lego2")
	#timediffCan.cd(2)
	#hist2D.Draw("Colz")
	#timediffCan.cd(1)
	#hist2D.Draw("Cont1")
	#hist2D.ProjectionX().Draw()
	#timediffCan.cd(2)
	#timediffCan.SetLogz()
	#hist2D.Draw("Surf3")
	#timediffCan.Draw()
	c2=r.TCanvas("Can2","vMax_Time_Canvas")
	c2.cd()
	histTimeDiff.Draw()
	#c2.Divide(2,2)
	#c2.cd(1)
	#hist2D.ProjectionX().Draw()
	#c2.cd(2)
	#hist2D.ProjectionY().Draw()
	#c2.cd(3)
	#hist2D.Draw("Cont1")
	#c2.cd(4)
	#hist2D.Draw("Surf3")
	#hist2D.ProjectionY().Draw("same")
	#timediffCan.Draw()
	c2.Draw()

def scale2(number1,number2,channel=1,DRS=2984,lowend=0,highend=1000):
	import ROOT as r 
	import numpy as np
	from glob import glob
	import os
	allnumber=[]
	allnumber.append(number2)
	c1=r.TCanvas("overlayCan","Overlay_plot_Canvas")
	c1.cd()
	for k in number1:
		allnumber.append(k)
	LineColor=1
	for i in allnumber:
		file='processed/Run'+str(i)+'*.root'
		filename=glob(file)
		globals()['f'+str(i)]=r.TFile(filename[0],'READ')
		globals()['t'+str(i)]=globals()['f'+str(i)].Get('Events')
		histname='h'+str(i)
		channelname='vMax_{}_{}'.format(DRS,channel)
		globals()[histname]=r.TH1D('h{}'.format(i),'Run{} channel{}; Pulse Height [mV]; Number of Pulses'.format(i,channel),100,lowend,highend)
		globals()['t'+str(i)].Draw("{}>>{}".format(channelname,histname),"","same")
		globals()[histname].SetLineColor(LineColor)
		LineColor+=1
	leg1=r.TLegend()
	leg1=c1.BuildLegend(0.55,0.7,0.9,0.9)
	r.gStyle.SetOptStat(0)
	c1.SetGrid()
	c1.SetLogy()
	c1.Draw()
	scaleCan=r.TCanvas("scaleCan","scale_plot_canvas2")
        scaleCan.cd()	
        first2=os.popen("cat processed/Run{}*.txt* | grep waveform | head -1".format(number2)).read()
        last2=os.popen("cat processed/Run{}*.txt* | grep waveform | tail -1".format(number2)).read()
        firsttime2=first2.split()[4]
        lasttime2=last2.split()[4]
        Voltage2=first2.split()[3]
        TotalTime2=float(lasttime2)-float(firsttime2)
        histname2='h'+str(number2)
        globals()[histname2].SetTitle('Run{} {}V channel {}; Pulse Height [mV]; Number of Pulses'.format(number2,Voltage2,channel))
        globals()[histname2].Draw()
	for j in number1:
		first1=os.popen("cat processed/Run{}*.txt* | grep waveform | head -1".format(j)).read()
                last1=os.popen("cat processed/Run{}*.txt* | grep waveform | tail -1".format(j)).read()
                firsttime1=first1.split()[4]
                lasttime1=last1.split()[4]
                Voltage1=first1.split()[3]
                TotalTime1=float(lasttime1)-float(firsttime1)
                ScaleFactor=TotalTime2/TotalTime1
                histname1='h'+str(j)
                scalehistname='sh'+str(j)+'_'+str(number2)
                globals()[scalehistname]=globals()[histname1].Clone()
                globals()[scalehistname].Scale(ScaleFactor)
                globals()[scalehistname].SetTitle('Scaled Run{} {}V'.format(j, Voltage1))
                globals()[scalehistname].Draw("same")
        leg=r.TLegend()
        leg=scaleCan.BuildLegend(0.55,0.7,0.9,0.9)
	r.gStyle.SetOptStat(0)
        scaleCan.SetGrid()
        scaleCan.SetLogy()
        scaleCan.Draw()

def sub(number1,number2,channel=1):
	import ROOT as r
        import numpy as np
        from glob import glob
        import os
        allnumber=[]
        allnumber.append(number2)
        for k in number1:
                allnumber.append(k)
        LineColor=1
	OriCan=r.TCanvas("OriCan","Original_Canvas")
	OriCan.cd()
        for i in allnumber:
                file='processed/Run'+str(i)+'*.root'
                filename=glob(file)
                globals()['f'+str(i)]=r.TFile(filename[0],'READ')
                globals()['t'+str(i)]=globals()['f'+str(i)].Get('Events')
                histname='h'+str(i)
		channelname='area_2984_'+str(channel)
		globals()[histname]=r.TH1D('h{}'.format(i),'Run{} channel{}; Pulse Area [nVs]; Number of Pulses'.format(i,channel),100,0,350000)
                globals()['t'+str(i)].Draw("{}>>{}".format(channelname,histname),"","same")
                globals()[histname].SetLineColor(LineColor)
                LineColor+=1
	leg1=r.TLegend()
	leg1=OriCan.BuildLegend(0.55,0.7,0.9,0.9)
	r.gStyle.SetOptStat(0)
	OriCan.SetGrid()
	OriCan.SetLogy()
	OriCan.Draw()
	subCan=r.TCanvas("subCan","scaled_subtraction_Canvas")
	subCan.cd()
	first2=os.popen("cat processed/Run{}*.txt | grep waveform | head -1".format(number2)).read()
        last2=os.popen("cat processed/Run{}*.txt | grep waveform | tail -1".format(number2)).read()
        firsttime2=first2.split()[4]
        lasttime2=last2.split()[4]
        Voltage2=first2.split()[3]
        TotalTime2=float(lasttime2)-float(firsttime2)
        histname2='h'+str(number2)
	#globals()[histname2].SetTitle('Background Run{} {}V channel {}; Pulse Area [nVs]; Number of Pulses'.format(number2,Voltage2,channel))
        #globals()[histname2].Draw()
	for j in number1:
		first1=os.popen("cat processed/Run{}*.txt | grep waveform | head -1".format(j)).read()
                last1=os.popen("cat processed/Run{}*.txt | grep waveform | tail -1".format(j)).read()
                firsttime1=first1.split()[4]
                lasttime1=last1.split()[4]
                Voltage1=first1.split()[3]
                TotalTime1=float(lasttime1)-float(firsttime1)
                ScaleFactor=TotalTime2/TotalTime1
                histname1='h'+str(j)
                scalehistname='sh'+str(j)+'_'+str(number2)
                globals()[scalehistname]=globals()[histname1].Clone()
                globals()[scalehistname].Scale(ScaleFactor)
		globals()[scalehistname].Add(globals()[histname2],-1)
		globals()[scalehistname].SetTitle('Substracted Run{} {}V'.format(j, Voltage1))
		globals()[scalehistname].Draw("same")
	leg=r.TLegend()
        leg=subCan.BuildLegend(0.55,0.7,0.9,0.9)
        r.gStyle.SetOptStat(0)
        subCan.SetGrid()
        subCan.SetLogy()
        subCan.Draw()

def maximum(hist):
	import numpy as np
	import ROOT as r
	max_count=np.where(hist[0]==np.max(hist[0]))
	return hist[1][max_count]	

def gain(number,voltage,channel=1,lowend=20,highend=500):
	import numpy as np
	import ROOT as r
	from glob import glob
	import array
	FitCan=r.TCanvas("FitCan","Fit_Canvas")
	FitCan.cd()
	color=1
	max_height=[]
	sigma=[]
	channelname='vMax_2881_'+str(channel)
	for Run in number:
		file='processed/Run'+str(Run)+'*.root'
	        filename=glob(file)
	        globals()['f'+str(Run)]=r.TFile(filename[0],'READ')
	        globals()['t'+str(Run)]=globals()['f'+str(Run)].Get('Events')
		for i in voltage:
			histname='h'+str(Run)+'_'+str(i)
			globals()[histname]=r.TH1D('h{}_{}'.format(Run,i),'Run{} {}V Channel {}; Pulse Height [mV]; Number of Pulses'.format(Run,i,channel),100,lowend,highend)
                        globals()[histname].SetLineColor(color)
			color+=1
                        globals()['t'+str(Run)].Draw('{}>>{}'.format(channelname,histname),'bias_voltage=={}'.format(i),'same')
			#globals()[histname].GetXaxis().SetRange(lowend,highend)
			maxbin=globals()[histname].GetXaxis().GetBinCenter(globals()[histname].GetMaximumBin())
			low=maxbin-10
			high=maxbin+10
			gname='g'+str(Run)+'_'+str(i)
			globals()[gname]=r.TF1("g{}_{}".format(Run,i),"gaus",low,high)
			globals()[histname].Fit(globals()[gname],"","",low,high)
			max_height.append(globals()[gname].GetParameter("Mean"))
			sigma.append(globals()[gname].GetParameter("Sigma"))
	leg=r.TLegend()
	leg=FitCan.BuildLegend(0.55,0.7,0.9,0.9)
	r.gStyle.SetOptStat(0)
	FitCan.SetGrid()
	FitCan.SetLogy()
	FitCan.Draw()
	c2=r.TCanvas("c2","gain_canvas")
	c2.cd()
	xerror=np.zeros(len(sigma))
	print(max_height)
	print(sigma)
	global graph
	graph=r.TGraphErrors(len(voltage),array.array('d',np.array(voltage)),array.array('d',np.array(max_height)),xerror,array.array('d',sigma))
	graph.SetMarkerStyle(r.kOpenCircle)
	graph.SetMarkerColor(4)
	graph.SetLineColor(r.kBlue)
	graph.SetFillColor(0)
	graph.SetTitle("Run{} channel{} Gain Curve; Bias Voltage [V]; Pulse Height [mV]".format(number,channel))
	graph.Draw()
	c2.Draw()
	
def coin(number,voltage=160,DRS=2881):
	import ROOT as r
	import numpy as np
	from glob import glob
	coinCan=r.TCanvas('coinCan','Run{}_{}V_DRS{}_Coincidence'.format(number,voltage,DRS))
	coinCan.Divide(2,3)
	file='processed/Run'+str(number)+'*.root'
        filename=glob(file)
        globals()['f'+str(number)]=r.TFile(filename[0],'READ')
        globals()['t'+str(number)]=globals()['f'+str(number)].Get('Events')
	channels=['vMax_{}_1'.format(DRS),'vMax_{}_2'.format(DRS),'vMax_{}_3'.format(DRS),'vMax_{}_4'.format(DRS)]
	coinCan.cd(1)
	globals()['t'+str(number)].Draw('{}:{}'.format(channels[0],channels[1]),'bias_voltage=={}'.format(voltage))
	coinCan.cd(2)
	globals()['t'+str(number)].Draw('{}:{}'.format(channels[0],channels[2]),'bias_voltage=={}'.format(voltage))
        coinCan.cd(3)
        globals()['t'+str(number)].Draw('{}:{}'.format(channels[0],channels[3]),'bias_voltage=={}'.format(voltage))
	coinCan.cd(4)
        globals()['t'+str(number)].Draw('{}:{}'.format(channels[1],channels[2]),'bias_voltage=={}'.format(voltage))
	coinCan.cd(5)
        globals()['t'+str(number)].Draw('{}:{}'.format(channels[1],channels[3]),'bias_voltage=={}'.format(voltage))
	coinCan.cd(6)
        globals()['t'+str(number)].Draw('{}:{}'.format(channels[2],channels[3]),'bias_voltage=={}'.format(voltage))
	coinCan.Draw()
	coinCan.SaveAs("plots/Run{}_{}V_{}_Coin.png".format(number,voltage,DRS))

def coin2(number,voltage=160,channel=1,DRS1=2881,DRS2=2880):
        import ROOT as r
        import numpy as np
        from glob import glob
        coinCan2=r.TCanvas('coinCan','Run{}_{}V_DRS{}and{}_Coincidence{}'.format(number,voltage,DRS1,DRS2,channel))
        coinCan2.Divide(2,2)
        file='processed/Run'+str(number)+'*.root'
        filename=glob(file)
        globals()['f'+str(number)]=r.TFile(filename[0],'READ')
        globals()['t'+str(number)]=globals()['f'+str(number)].Get('Events')
        channels=['vMax_{}_{}'.format(DRS1,channel),'vMax_{}_1'.format(DRS2),'vMax_{}_2'.format(DRS2),'vMax_{}_3'.format(DRS2),'vMax_{}_4'.format(DRS2)]
        coinCan2.cd(1)
        globals()['t'+str(number)].Draw('{}:{}'.format(channels[0],channels[1]),'bias_voltage=={}'.format(voltage))
        coinCan2.cd(2)
        globals()['t'+str(number)].Draw('{}:{}'.format(channels[0],channels[2]),'bias_voltage=={}'.format(voltage))
        coinCan2.cd(3)
        globals()['t'+str(number)].Draw('{}:{}'.format(channels[0],channels[3]),'bias_voltage=={}'.format(voltage))
        coinCan2.cd(4)
        globals()['t'+str(number)].Draw('{}:{}'.format(channels[0],channels[4]),'bias_voltage=={}'.format(voltage))
        coinCan2.Draw()
        coinCan2.SaveAs("plots/Run{}_{}V_{}and{}_Coin{}.png".format(number,voltage,DRS1,DRS2,channel))

def coinall(number):
        import ROOT as r
        import numpy as np
        from glob import glob
        coinCan=r.TCanvas('coinCan','Run{}_Coincidence_Canvas'.format(number))
        coinCan.Divide(2,3)
        file='processed/Run'+str(number)+'*.root'
        filename=glob(file)
        globals()['f'+str(number)]=r.TFile(filename[0],'READ')
        globals()['t'+str(number)]=globals()['f'+str(number)].Get('Events')
        channels=['vMax_2881_1','vMax_2881_2','vMax_2881_3','vMax_2881_4']
        coinCan.cd(1)
        globals()['t'+str(number)].Draw('{}:{}'.format(channels[0],channels[1]))
        coinCan.cd(2)
        globals()['t'+str(number)].Draw('{}:{}'.format(channels[0],channels[2]))
        coinCan.cd(3)
        globals()['t'+str(number)].Draw('{}:{}'.format(channels[0],channels[3]))
        coinCan.cd(4)
        globals()['t'+str(number)].Draw('{}:{}'.format(channels[1],channels[2]))
        coinCan.cd(5)
        globals()['t'+str(number)].Draw('{}:{}'.format(channels[1],channels[3]))
        coinCan.cd(6)
        globals()['t'+str(number)].Draw('{}:{}'.format(channels[2],channels[3]))
        coinCan.Draw()
        coinCan.SaveAs("plots/Run{}_Coin.png".format(number))	

def plotRun(number,color,channel=1,voltage=160):
	file='processed/Run'+str(number)+'*.root'
        filename=glob(file)
        globals()['f'+str(number)]=r.TFile(filename[0],'READ')
        globals()['t'+str(number)]=globals()['f'+str(number)].Get('Events')
        histname='h'+str(number)
        channelname='vMax_2881_'+str(channel)
        globals()[histname]=r.TH1D('h{}'.format(number),'Run{} channel{};Pulse Height [mV]; Number of Pulses'.format(number,channel),100,0,500)
        globals()[histname].SetLineColor(color)
        globals()['t'+str(number)].Draw('{}>>{}'.format(channelname,histname),'bias_voltage=={}'.format(voltage),'same')


def cali(channel=1,voltage=160,DRS=2881):
	import ROOT as r
	import numpy as np
	from glob import glob
	import array
	#c1=r.TCanvas("c1","Overlay_Canvas")
	#c1.cd()
	gnumber=1
	color=1
	old=[]
	new=[]
	#calican=r.TCanvas("calican","calibration_canvas")
	#calican.cd()
	while True:
		number=int(input('Please specify the run number you want to use for calibration: '))
		#plotRun(number,color,channel,voltage)
		file='processed/Run'+str(number)+'*.root'
        	filename=glob(file)
        	globals()['f'+str(number)]=r.TFile(filename[0],'READ')
        	globals()['t'+str(number)]=globals()['f'+str(number)].Get('Events')
        	histname='h'+str(number)
        	channelname='vMax_2881_'+str(channel)
        	globals()[histname]=r.TH1D('h{}'.format(number),'Run{} channel{};Pulse Height [mV]; Number of Pulses'.format(number,channel),100,0,500)
        	globals()[histname].SetLineColor(color)
       		globals()['t'+str(number)].Draw('{}>>{}'.format(channelname,histname),'bias_voltage=={}'.format(voltage),"same")
		#calican.SetLogy()
                #calican.SetGrid()
                #calican.Draw()
                color+=1
		while True:
			lowend=float(input('Input the lowend for finding the peak: '))
			highend=float(input('Input the highend for finding the peak: '))
			#points=Range.split(',')
			#lowend=float(points[0])
			#highend=float(points[1])
			globals()['g'+str(gnumber)]=r.TF1("g{}".format(gnumber),"gaus",lowend,highend)
			globals()[histname].Fit(globals()['g'+str(gnumber)],"","",lowend,highend)
			old.append(globals()['g'+str(gnumber)].GetParameter("Mean"))
			cali_value=float(input('Please input the value you want to calibrate to: '))
			new.append(cali_value)
			gnumber+=1
			another=int(input('Do you want to calibrate another points in this run? (1/0): '))
			if another==1:
				continue
			else:
				ask=int(input('Do you want to use another run for calibration (1/0): '))
				if ask==1:
					try:
						number=int(input('Please specify the run number you want to use for calibration: '))
						#plotRun(number,color)
						file='processed/Run'+str(number)+'*.root'
        					filename=glob(file)
        					globals()['f'+str(number)]=r.TFile(filename[0],'READ')
        					globals()['t'+str(number)]=globals()['f'+str(number)].Get('Events')
        					histname='h'+str(number)
        					channelname='vMax_2881_'+str(channel)
        					globals()[histname]=r.TH1D('h{}'.format(number),'Run{} channel{};Pulse Height [mV]; Number of Pulses'.format(number,channel),100,0,500)
        					globals()[histname].SetLineColor(color)
        					globals()['t'+str(number)].Draw('{}>>{}'.format(channelname,histname),'bias_voltage=={}'.format(voltage),"same")
						color+=1
						gnumber+=1
					except ValueError:
						print('The file does not exist. Try again.')
				else:
					break
		break
	outfile=str(input('Please input the file name that store the calibration data: '))
	with open('{}'.format(outfile),'w') as f:
		for i in range(len(old)):
			f.write('{} {} \n'.format(old[i],new[i]))
	f.close()
	
def cali2(channel=1,DRS=2984,lowend=0,highend=1000):
        import ROOT as r
        import numpy as np
        from glob import glob
        import array
        #c1=r.TCanvas("c1","Overlay_Canvas")
        #c1.cd()
        gnumber=1
        color=1
        old=[]
        new=[]
	global c1      
	#c1=r.TCanvas("calican","calibration_canvas")
        #c1.cd()
        while True:
		#c1.cd()
                number=int(input('Please specify the run number you want to use for calibration: '))
                #plotRun(number,color,channel,voltage)
                file='processed/Run'+str(number)+'*.root'
                filename=glob(file)
                globals()['f'+str(number)]=r.TFile(filename[0],'READ')
                globals()['t'+str(number)]=globals()['f'+str(number)].Get('Events')
                histname='h'+str(number)
                channelname='vMax_{}_{}'.format(DRS,channel)
                globals()[histname]=r.TH1D('h{}'.format(number),'Run{} channel{};Pulse Height [mV]; Number of Pulses'.format(number,channel),100,lowend,highend)
                globals()[histname].SetLineColor(color)
                globals()['t'+str(number)].Draw('{}>>{}'.format(channelname,histname),"","same")
		#globals()[histname].Draw("same")
		#c1.SetLogy()
                #c1.SetGrid()
                #c1.Draw()
                color+=1
                while True:
                        lowend=float(input('Input the lowend for finding the peak: '))
                        highend=float(input('Input the highend for finding the peak: '))
                        #points=Range.split(',')
                        #lowend=float(points[0])
                        #highend=float(points[1])
                        globals()['g'+str(gnumber)]=r.TF1("g{}".format(gnumber),"gaus",lowend,highend)
                        globals()[histname].Fit(globals()['g'+str(gnumber)],"","",lowend,highend)
                        old.append(globals()['g'+str(gnumber)].GetParameter("Mean"))
                        cali_value=float(input('Please input the value you want to calibrate to: '))
                        new.append(cali_value)
                        gnumber+=1
                        another=int(input('Do you want to calibrate another points in this run? (1/0): '))
                        if another==1:
                                continue
                        else:
                                ask=int(input('Do you want to use another run for calibration (1/0): '))
                                if ask==1:
                                        try:
                                                number=int(input('Please specify the run number you want to use for calibration: '))
                                                #plotRun(number,color)
                                                file='processed/Run'+str(number)+'*.root'
                                                filename=glob(file)
                                                globals()['f'+str(number)]=r.TFile(filename[0],'READ')
                                                globals()['t'+str(number)]=globals()['f'+str(number)].Get('Events')
                                                histname='h'+str(number)
                                                channelname='vMax_{}_{}'.format(DRS,channel)
                                                globals()[histname]=r.TH1D('h{}'.format(number),'Run{} channel{};Pulse Height [mV]; Number of Pulses'.format(number,channel),100,lowend,highend)
                                                globals()[histname].SetLineColor(color)
                                                globals()['t'+str(number)].Draw('{}>>{}'.format(channelname,histname),"","same")
						#globals()[histname].Draw("same")
						#c1.Draw()
                                                color+=1
                                                gnumber+=1
                                        except ValueError:
                                                print('The file does not exist. Try again.')
                                else:
                                        break
                break
        outfile=str(input('Please input the file name that store the calibration data: '))
        with open('{}'.format(outfile),'w') as f:
                for i in range(len(old)):
                        f.write('{} {} \n'.format(old[i],new[i]))
        f.close()
	calicurve(outfile)

def calicurve(filename):
	import ROOT as r
	import numpy as np
	from array import array
	with open(filename,'r') as f:
		lines=f.readlines()
		old=[]
		new=[]
		for i in range(len(lines)):
			old.append(float(lines[i].split()[0]))
			new.append(float(lines[i].split()[1]))
	global graph,p0,p1
	c2=r.TCanvas("c2","calibration_curve_canvas")
	c2.cd()
	graph=r.TGraph(len(old),array("d",old),array("d",new))
	graph.SetMarkerStyle(r.kOpenCircle)
	graph.SetMarkerColor(4)
	graph.Draw("AP")
	pol=r.TF1("pol","pol1")
	graph.Fit(pol)
	p0=pol.GetParameter(0)
	p1=pol.GetParameter(1)
	print(p0,'\n',p1)
	c2.Draw()

def caliplot(number,a,b):
	import ROOT as r
	import numpy as np
	from array import array
	file='processed/Run'+str(number)+'*.root'
	filename=glob(file)
	f=r.TFile(filename[0],'READ')
	t=f.Get("Events")
	global old, new
	old=r.TH1D("old","Before Calibration; Pulse Height [mV]; Number of Pulses",100,0,500)
        new=r.TH1D("new","After Calibration; Energy [keV]; Number of Pulses",100,0,100)
	for i in t:
		ori=i.vMax_2881_1
		y=a+(b*ori)
		old.Fill(ori)
		new.Fill(y)
	c1=r.TCanvas("c1","old_unit_canvas")	
	c1.cd()
	old.Draw()
	c1.SetGrid()
	c1.SetLogy()
	c1.Draw()
        c2=r.TCanvas("c2","new_unit_canvas")
        c2.cd()
        new.Draw()
        c2.SetGrid()
        c2.SetLogy()
        c2.Draw()

def tsuball(number,cut=50):
        import ROOT as r
        import numpy as np
        from glob import glob
        tsubCan=r.TCanvas('tsubCan','Run{}_tMax_Subtraction_Canvas'.format(number))
        tsubCan.Divide(2,3)
        file='processed/Run'+str(number)+'*.root'
        filename=glob(file)
        globals()['f'+str(number)]=r.TFile(filename[0],'READ')
        globals()['t'+str(number)]=globals()['f'+str(number)].Get('Events')
        channels=['vMax_2881_1','vMax_2881_2','vMax_2881_3','vMax_2881_4']
	one=channels[0]
	two=channels[1]
	three=channels[2]
	four=channels[3]
	tone='tMax_2881_1'
	ttwo='tMax_2881_2'
	tthree='tMax_2881_3'
	tfour='tMax_2881_4'
        tsubCan.cd(1)
	titles=["t1-t2","t1-t3","t1-t4","t2-t3","t2-t4","t3-t4"]
	for i in [1,2,3,4,5,6]:
		globals()['h'+str(i)]=r.TH1D("h{}".format(i),"{} vMax>{}".format(titles[i-1],cut),100,-2,2)
	
        globals()['t'+str(number)].Draw('{}-{}>>h1'.format(tone,ttwo),'{}>{}&&{}>{}'.format(one,cut,two,cut))
        h1.Fit("gaus")
	#h1.Draw()
	tsubCan.cd(2)
        globals()['t'+str(number)].Draw('{}-{}>>h2'.format(tone,tthree),'{}>{}&&{}>{}'.format(one,cut,three,cut))
        h2.Fit("gaus")
	#h2.Draw()
	tsubCan.cd(3)
        globals()['t'+str(number)].Draw('{}-{}>>h3'.format(tone,tfour),'{}>{}&&{}>{}'.format(one,cut,four,cut))
        h3.Fit("gaus")
	#h3.Draw()
	tsubCan.cd(4)
        globals()['t'+str(number)].Draw('{}-{}>>h4'.format(ttwo,tthree),'{}>{}&&{}>{}'.format(two,cut,three,cut))
        h4.Fit("gaus")
	#h4.Draw()
	tsubCan.cd(5)
        globals()['t'+str(number)].Draw('{}-{}>>h5'.format(ttwo,tfour),'{}>{}&&{}>{}'.format(two,cut,four,cut))
        h5.Fit("gaus")
	#h5.Draw()
	tsubCan.cd(6)
        globals()['t'+str(number)].Draw('{}-{}>>h6'.format(tthree,tfour),'{}>{}&&{}>{}'.format(three,cut,four,cut))
        h6.Fit("gaus")
	#h6.Draw()
	r.gStyle.SetOptFit(1)
	tsubCan.Draw()
        tsubCan.SaveAs("plots/Run{}_tMaxsub.png".format(number))

def tsub(number,voltage=160,DRS=2881,lowcut=50,highcut=480,low=-2,high=2):
        import ROOT as r
        import numpy as np
        from glob import glob
        tsubCan=r.TCanvas('tsubCan','Run{}_{}V_DRS{}_tMax_Subtraction'.format(number,voltage,DRS))
        tsubCan.Divide(2,3)
        file='processed/Run'+str(number)+'*.root'
        filename=glob(file)
        globals()['f'+str(number)]=r.TFile(filename[0],'READ')
        globals()['t'+str(number)]=globals()['f'+str(number)].Get('Events')
        channels=['vMax_{}_1'.format(DRS),'vMax_{}_2'.format(DRS),'vMax_{}_3'.format(DRS),'vMax_{}_4'.format(DRS)]
        one=channels[0]
        two=channels[1]
        three=channels[2]
        four=channels[3]
        tone='tMax_{}_1'.format(DRS)
        ttwo='tMax_{}_2'.format(DRS)
        tthree='tMax_{}_3'.format(DRS)
        tfour='tMax_{}_4'.format(DRS)
        tsubCan.cd(1)
        titles=["t1-t2","t1-t3","t1-t4","t2-t3","t2-t4","t3-t4"]
        for i in [1,2,3,4,5,6]:
                globals()['h'+str(i)]=r.TH1D("h{}".format(i),"{} {}<vMax<{} {}V".format(titles[i-1],lowcut,highcut,voltage),100,low,high)

        globals()['t'+str(number)].Draw('{}-{}>>h1'.format(tone,ttwo),'{}>{}&&{}>{}&&{}<{}&&{}<{}&&bias_voltage=={}'.format(one,lowcut,two,lowcut,one,highcut,two,highcut,voltage))
        h1.Fit("gaus")
        #h1.Draw()
        tsubCan.cd(2)
        globals()['t'+str(number)].Draw('{}-{}>>h2'.format(tone,tthree),'{}>{}&&{}>{}&&{}<{}&&{}<{}&&bias_voltage=={}'.format(one,lowcut,three,lowcut,one,highcut,three,highcut,voltage))
        h2.Fit("gaus")
        #h2.Draw()
        tsubCan.cd(3)
        globals()['t'+str(number)].Draw('{}-{}>>h3'.format(tone,tfour),'{}>{}&&{}>{}&&{}<{}&&{}<{}&&bias_voltage=={}'.format(one,lowcut,four,lowcut,one,highcut,four,highcut,voltage))
        h3.Fit("gaus")
        #h3.Draw()
        tsubCan.cd(4)
        globals()['t'+str(number)].Draw('{}-{}>>h4'.format(ttwo,tthree),'{}>{}&&{}>{}&&{}<{}&&{}<{}&&bias_voltage=={}'.format(two,lowcut,three,lowcut,two,highcut,three,highcut,voltage))
        h4.Fit("gaus")
        #h4.Draw()
        tsubCan.cd(5)
        globals()['t'+str(number)].Draw('{}-{}>>h5'.format(ttwo,tfour),'{}>{}&&{}>{}&&{}<{}&&{}<{}&&bias_voltage=={}'.format(two,lowcut,four,lowcut,two,highcut,four,highcut,voltage))
        h5.Fit("gaus")
        #h5.Draw()
        tsubCan.cd(6)
        globals()['t'+str(number)].Draw('{}-{}>>h6'.format(tthree,tfour),'{}>{}&&{}>{}&&{}<{}&&{}<{}&&bias_voltage=={}'.format(three,lowcut,four,lowcut,three,highcut,four,highcut,voltage))
        h6.Fit("gaus")
        #h6.Draw()
        r.gStyle.SetOptFit(1)
        tsubCan.Draw()
        tsubCan.SaveAs("plots/Run{}_{}V_{}_tMaxsub.png".format(number,voltage,DRS))

def tsub2(number,voltage=160,channel=1,DRS1=2881,DRS2=2880,lowcut=50,highcut=480,low=-2,high=2):
        import ROOT as r
        import numpy as np
        from glob import glob
        tsubCan2=r.TCanvas('tsubCan','Run{}_{}V_DRS{}and{}_tMax_Subtraction{}'.format(number,voltage,DRS1,DRS2,channel))
        tsubCan2.Divide(2,2)
        file='processed/Run'+str(number)+'*.root'
        filename=glob(file)
        globals()['f'+str(number)]=r.TFile(filename[0],'READ')
        globals()['t'+str(number)]=globals()['f'+str(number)].Get('Events')
        channels=['vMax_{}_1'.format(DRS2),'vMax_{}_2'.format(DRS2),'vMax_{}_3'.format(DRS2),'vMax_{}_4'.format(DRS2)]
        one=channels[0]
        two=channels[1]
        three=channels[2]
        four=channels[3]
	zero='vMax_{}_{}'.format(DRS1,channel)
	tzero='tMax_{}_{}'.format(DRS1,channel)
        tone='tMax_{}_1'.format(DRS2)
        ttwo='tMax_{}_2'.format(DRS2)
        tthree='tMax_{}_3'.format(DRS2)
        tfour='tMax_{}_4'.format(DRS2)
        tsubCan2.cd(1)
        titles=["{}-{}".format(tzero,tone),"{}-{}".format(tzero,ttwo),"{}-{}".format(tzero,tthree),"{}-{}".format(tzero,tfour)]
        for i in [1,2,3,4]:
                globals()['h'+str(i)]=r.TH1D("h{}".format(i),"{} {}<vMax<{} {}V".format(titles[i-1],lowcut,highcut,voltage),100,low,high)

        globals()['t'+str(number)].Draw('{}-{}>>h1'.format(tzero,tone),'{}>{}&&{}>{}&&{}<{}&&{}<{}&&bias_voltage=={}'.format(zero,lowcut,one,lowcut,zero,highcut,one,highcut,voltage))
        h1.Fit("gaus")
        #h1.Draw()
        tsubCan2.cd(2)
        globals()['t'+str(number)].Draw('{}-{}>>h2'.format(tzero,ttwo),'{}>{}&&{}>{}&&{}<{}&&{}<{}&&bias_voltage=={}'.format(zero,lowcut,two,lowcut,zero,highcut,two,highcut,voltage))
        h2.Fit("gaus")
        #h2.Draw()
        tsubCan2.cd(3)
        globals()['t'+str(number)].Draw('{}-{}>>h3'.format(tzero,tthree),'{}>{}&&{}>{}&&{}<{}&&{}<{}&&bias_voltage=={}'.format(zero,lowcut,three,lowcut,zero,highcut,three,highcut,voltage))
        h3.Fit("gaus")
        #h3.Draw()
        tsubCan2.cd(4)
        globals()['t'+str(number)].Draw('{}-{}>>h4'.format(tzero,tfour),'{}>{}&&{}>{}&&{}<{}&&{}<{}&&bias_voltage=={}'.format(zero,lowcut,four,lowcut,zero,highcut,four,highcut,voltage))
        h4.Fit("gaus")
        r.gStyle.SetOptFit(1)
        tsubCan2.Draw()
        tsubCan2.SaveAs("plots/Run{}_{}V_{}and{}_tMaxsub{}.png".format(number,voltage,DRS1,DRS2,channel))

def timesub(number,low=-50,high=50,channel=4,data='LGAD'):
	import ROOT as r
	import numpy as np
	from glob import glob
	filename='/net/cms1/cms1r0/stuart/{}/Run{}/Run{}_time.ant'.format(data,number,number)
	with open(filename,'r') as f:
		lines=f.readlines()
		evt=[]
		t1=[]
		fitt1=[]
		fitprob1=[]
		t2=[]
                fitt2=[]
                fitprob2=[]
                t3=[]
                fitt3=[]
		fitprob3=[]    
		t4=[]
		fitt4=[]
		fitprob4=[]
		for i in range(len(lines)):
			evt.append(float(lines[i].split()[2]))
        		t1.append(float(lines[i].split()[6]))
        		fitt1.append(float(lines[i].split()[7]))
        		fitprob1.append(float(lines[i].split()[11]))
        		t2.append(float(lines[i].split()[15]))
        		fitt2.append(float(lines[i].split()[16]))
        		fitprob2.append(float(lines[i].split()[20]))
        		t3.append(float(lines[i].split()[24]))
        		fitt3.append(float(lines[i].split()[25]))
			fitprob3.append(float(lines[i].split()[28]))
        		t4.append(float(lines[i].split()[33]))
        		fitt4.append(float(lines[i].split()[34]))
			fitprob4.append(float(lines[i].split()[38]))
	evt=np.array(evt)
	t1=np.array(t1)
	fitt1=np.array(fitt1)
	fitprob1=np.array(fitprob1)
	t2=np.array(t2)
	fitt2=np.array(fitt2)
	fitprob2=np.array(fitprob2)
	t3=np.array(t3)
	fitt3=np.array(fitt3)
	t4=np.array(t4)
	fitt4=np.array(fitt4)
	fitprob4=np.array(fitprob4)	
	sub12=t1-t2
	sub13=t1-t3
	sub14=t1-t4
	sub23=t2-t3
	sub24=t2-t4
	sub34=t3-t4
        subfit12=fitt1-fitt2
        subfit13=fitt1-fitt3
        subfit14=fitt1-fitt3
        subfit23=fitt2-fitt3
        subfit24=fitt2-fitt4
        subfit34=fitt3-fitt4	
	subs=[sub12,sub13,sub14,sub23,sub24,sub34,subfit12,subfit13,subfit14,subfit23,subfit24,subfit34]
	subname=['t1-t2','t1-t3','t1-t4','t2-t3','t2-t4','t3-t4','fit1-fit2','fit1-fit3','fit1-fit4','fit2-fit3','fit2-fit4','fit3-fit4']
	two=[0,6]
	if channel==4:
		c1=r.TCanvas("c1","{}_Run{}_time_subtraction_canvas".format(data,number))
       		c1.Divide(2,3)
		c2=r.TCanvas("c2","{}_Run{}_fittime_subtrction_canvas".format(data,number))
		c2.Divide(2,3)
		for i in range(len(subs)):
			globals()['h'+str(i)]=r.TH1D("h{}".format(i),"{}".format(subname[i]),100,low,high)
			for j in range(len(subs[i])):	
				globals()['h'+str(i)].Fill(subs[i][j])
			if i<6:
				c1.cd(i+1)
			else:	
				c2.cd(i-5)
			globals()['h'+str(i)].Draw()
			globals()['h'+str(i)].Fit("gaus")
			r.gStyle.SetOptFit(1)
		c1.Draw()
		c1.SaveAs("/net/cms27/cms27r0/jyang/Time/plots/Run{}_Time_{}.png".format(number,data))
		c2.Draw()
		c2.SaveAs("/net/cms27/cms27r0/jyang/Time/plots/Run{}_fitTime_{}.png".format(number,data))
	if channel==2:
		c3=r.TCanvas("c3","{}_Run{}_two_channels_time_canvas".format(data,number))
		c3.Divide(1,2)
		for i in range(2):
			globals()['h'+str(i)]=r.TH1D("h{}".format(i),"{}".format(subname[two[i]]),100,low,high)
			for j in range(len(subs[two[i]])):
				globals()['h'+str(i)].Fill(subs[two[i]][j])
			c3.cd(i+1)
                        globals()['h'+str(i)].Draw()
                        globals()['h'+str(i)].Fit("gaus")
                        r.gStyle.SetOptFit(1)
		c3.Draw()
		c3.SaveAs("/net/cms27/cms27r0/jyang/Time/plots/Run{}_twoTime_{}.png".format(number,data))

def convert(number):
	import ROOT as r
	import numpy as np
	from array import array
	from glob import glob
	Tree=r.TTree("Events","Tree to store waveforms")

	EVTNUM=array('i',[0])
	#BOARD_CHAN=np.array([0])
	bias_voltage=array('f',[0])
	vMax_1=array('f',[0])
	vMax_2=array('f',[0])
	vMax_3=array('f',[0])
	vMax_4=array('f',[0])
	height_1=array('f',np.zeros(1024))
	time_1=array('f',np.zeros(1024))
        height_2=array('f',np.zeros(1024))
        time_2=array('f',np.zeros(1024))
        height_3=array('f',np.zeros(1024))
        time_3=array('f',np.zeros(1024))
        height_4=array('f',np.zeros(1024))
        time_4=array('f',np.zeros(1024))
	#wavetime=array('f',np.zeros(1024))
	#waveheight=array('f',np.zeros(1024))

	Tree.Branch("EVTNUM",EVTNUM,"EVTNUM/I")
	Tree.Branch("bias_voltage",bias_voltage,"bias_voltage/F")
	Tree.Branch("vMax_1",vMax_1,"vMax_1/F")
	Tree.Branch("vMax_2",vMax_2,"vMax_2/F")	
	Tree.Branch("vMax_3",vMax_3,"vMax_3/F")
	Tree.Branch("vMax_4",vMax_4,"vMax_4/F")
	Tree.Branch("height_1",height_1,"height_1[1024]/F")
	Tree.Branch("time_1",time_1,"time_1[1024]/F")
        Tree.Branch("height_2",height_2,"height_2[1024]/F")
        Tree.Branch("time_2",time_2,"time_2[1024]/F")
        Tree.Branch("height_3",height_3,"height_3[1024]/F")
        Tree.Branch("time_3",time_3,"time_3[1024]/F")
        Tree.Branch("height_4",height_4,"height_4[1024]/F")
        Tree.Branch("time_4",time_4,"time_4[1024]/F")

	wavenum=1024
	outFile=r.TFile('waveform/Run{}_waveform.root'.format(number),'RECREATE')
	file='processed/Run'+str(number)+'*.txt'
	filename=glob(file)[0]
	with open(filename,'r') as f:
		lines=f.readlines()
		events=0
		for i in range(len(lines)):
			if str(lines[i].split()[0])=='waveform:':
				events+=1
				#EVTNUM[0]=int(lines[i].split()[1])
				BOARD_CHAN=str(lines[i].split()[2])
				vMax=float(lines[i].split()[6])
				EVTNUM[0]=int(lines[i].split()[1])
				bias_voltage[0]=float(lines[i].split()[3])
				
		#I am sure why half of this code got deleted

def event(number,channels=[1,2,3,4],cuts=[0,0,0,0]):
	import ROOT as r
	import numpy as np
	from glob import glob
	import os
	from array import array
	file='processed/Run'+str(number)+'*.txt'
	filename=glob(file)[0]
	lines=[]
	single=[1,1025,2049,3073]
	end=4100
	for i in channels:
		globals()['time'+str(i)]=array('d',np.zeros(1024))
		globals()['height'+str(i)]=array('d',np.zeros(1024))
		globals()['wave'+str(i)]=os.popen("cat {} | grep -n 2881_{}".format(file,i)).read().split('\n')
		globals()['vMax'+str(i)]=[]
	        for j in range(len(globals()['wave'+str(i)])-1):
			globals()['vMax'+str(i)].append(float((globals()['wave'+str(i)])[j].split()[6]))
	for k in range(len(globals()['vMax'+str(1)])):	
		if globals()['vMax'+str(1)][k]>cuts[0] and globals()['vMax'+str(2)][k]>cuts[1] and globals()['vMax'+str(3)][k]>cuts[2] and globals()['vMax'+str(4)][k]>cuts[3]:
			lines.append(int(globals()['wave'+str(1)][k].split(':')[0]))
	

	heads=lines[0]+4099
	tails=4100
	waveform=os.popen("cat {} | head -{} | tail -{}".format(file,heads,tails)).read().split('\n')
	globals()['waveform1']=waveform[1:1024]
	globals()['waveform2']=waveform[1026:1026+1023]
	globals()['waveform3']=waveform[1026+1025:1026+1025+1023]
	globals()['waveform4']=waveform[1026+1025+1025:1026+1025+1025+1023]
	color=1
	c1=r.TCanvas("c1","Events_Display_Canvas")
	c1.Divide(2,2)
	for i in channels:
		for j in range(1023):
			globals()['time'+str(i)][j]=float(globals()['waveform'+str(i)][j].split()[0])
			globals()['height'+str(i)][j]=float(globals()['waveform'+str(i)][j].split()[1])
		c1.cd(i)
		globals()['graph'+str(i)]=r.TGraph(len(globals()['time'+str(i)]),globals()['time'+str(i)],globals()['height'+str(i)])
		globals()['graph'+str(i)].SetTitle('Channel{} Cuts={}; Time position [ns]; Pulse Height [mV]'.format(i,cuts))
		globals()['graph'+str(i)].SetFillColor(color)
		globals()['graph'+str(i)].SetLineColor(color)
		globals()['graph'+str(i)].Draw()
		color+=1
	c1.Draw()
	c1.SaveAs('waveform/Run{}.png'.format(number))

def calibrate(number,p0,p1,channel=1,DRS=2988):
	import ROOT as r
	for i in number:
		df=r.RDataFrame("Events","processed/Run{}.root".format(i))
		def1=df.Define("cali_{}_{}".format(DRS,channel),"vMax_{}_{}*{}+{}".format(DRS,channel,p1,p0))
		def1.Snapshot("Events","cali/Run{}_cali{}.root".format(i,channel),["cali_{}_{}".format(DRS,channel)])


def calibrate2(number,filename,channel=1,DRS=2988):
        import ROOT as r
	calicurve(filename)
        for i in number:
                df=r.RDataFrame("Events","processed/Run{}.root".format(i))
                def1=df.Define("cali_{}_{}".format(DRS,channel),"vMax_{}_{}*{}+{}".format(DRS,channel,p1,p0))
                def1.Snapshot("Events","cali/Run{}_cali{}.root".format(i,channel),["cali_{}_{}".format(DRS,channel)])


def overcali(number,channel=1,DRS=2984,lowend=0,highend=150):
	import ROOT as r
	import numpy as np
	from glob import glob
        c1=r.TCanvas("overlayCan","Overlay_plot_Canvas")
        c1.cd() 
	LineColor=1
	for i in number:
		filename='cali/Run{}_cali{}.root'.format(i,channel)
		globals()['f'+str(i)]=r.TFile(filename,'READ')
                globals()['t'+str(i)]=globals()['f'+str(i)].Get('Events')
                histname='h'+str(i)
                channelname='cali_{}_{}'.format(DRS,channel)
                globals()[histname]=r.TH1D('h{}'.format(i),'Run{} channel{}; Pulse Height [keV]; Number of Pulses'.format(i,channel),100,lowend,highend)
                globals()['t'+str(i)].Draw("{}>>{}".format(channelname,histname),"","same")
                globals()[histname].SetLineColor(LineColor)
                LineColor+=1
        leg1=r.TLegend()
        leg1=c1.BuildLegend(0.55,0.7,0.9,0.9)
        r.gStyle.SetOptStat(0)
        c1.SetGrid()
        c1.SetLogy()
        c1.Draw()

def scancali(number,channel=[1,2,3,4],DRS=2988,lowend=0,highend=150):
	import ROOT as r
	color=1
	c1=r.TCanvas("c1","scan_cali_canvas_{}".format(DRS))
        c1.cd()
	for i in channel:
		filename='cali/Run{}_cali{}.root'.format(number,i)
		globals()['f'+str(i)]=r.TFile(filename,'READ')
		globals()['t'+str(i)]=globals()['f'+str(i)].Get("Events")
		#print(filename,"DRS {}".format(DRS))
		histname='h'+str(i)
		channelname='cali_{}_{}'.format(DRS,i)
		globals()[histname]=r.TH1D("h{}".format(i),"Run{} channel{}; Pulse Height [keV]; Number of Pulses".format(number,i),100,lowend,highend)
		globals()[histname].SetLineColor(color)
		color+=1
		globals()['t'+str(i)].Draw("{}>>{}".format(channelname,histname),"","same")
	leg=r.TLegend()
	leg=c1.BuildLegend(0.55,0.7,0.9,0.9)
	r.gStyle.SetOptStat(0)
	c1.SetGrid()
	c1.SetLogy()
	c1.Draw()		

def position(number,pos,channel=1,DRS=2984,lowend=60,highend=100):
	import numpy as np
        import ROOT as r
        from glob import glob
        import array
        FitCan=r.TCanvas("FitCan","Fit_Canvas")
        FitCan.cd()
        color=1
        max_height=[]
        sigma=[]
        channelname='cali_{}_{}'.format(DRS,channel)
        for Run in number:
                filename='cali/Run{}_cali{}.root'.format(Run,channel)
                globals()['f'+str(Run)]=r.TFile(filename,'READ')
                globals()['t'+str(Run)]=globals()['f'+str(Run)].Get('Events')
                histname='h'+str(Run)
                globals()[histname]=r.TH1D('h{}'.format(Run),'Run{} Channel {}; Pulse Height [keV]; Number of Pulses'.format(Run,channel),100,lowend,highend)
                globals()[histname].SetLineColor(color)
                color+=1
                globals()['t'+str(Run)].Draw('{}>>{}'.format(channelname,histname),"",'same')
                        #globals()[histname].GetXaxis().SetRange(lowend,highend)

                maxbin=globals()[histname].GetXaxis().GetBinCenter(globals()[histname].GetMaximumBin())
                low=maxbin-10
                high=maxbin+10
                gname='g'+str(Run)
                globals()[gname]=r.TF1("g{}".format(Run),"gaus",low,high)
                globals()[histname].Fit(globals()[gname],"","",low,high)
                max_height.append(globals()[gname].GetParameter("Mean"))
                sigma.append(globals()[gname].GetParameter("Sigma"))
        leg=r.TLegend()
        leg=FitCan.BuildLegend(0.55,0.7,0.9,0.9)
        r.gStyle.SetOptStat(0)
        FitCan.SetGrid()
        FitCan.SetLogy()
        FitCan.Draw()
        c2=r.TCanvas("c2","position_canvas")
        c2.cd()
        xerror=np.zeros(len(sigma))
        print(max_height)
        print(sigma)
        global graph
        graph=r.TGraphErrors(len(pos),array.array('d',np.array(pos)),array.array('d',np.array(max_height)),xerror,array.array('d',sigma))
        graph.SetMarkerStyle(r.kOpenCircle)
        graph.SetMarkerColor(4)
        graph.SetLineColor(r.kBlue)
        graph.SetFillColor(0)
        graph.SetTitle("Run{} channel{} Position Curve; x positions; Pulse Height [keV]".format(number,channel))
        graph.Draw()
        c2.Draw()
