# -*- coding: utf-8 -*-
"""
Created on Fri May  3 11:08:33 2019

@author: jhrut
"""
import math,datetime
import numpy as np
from fractions import Fraction   # code for fractional input, and finish the parameters
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
from tkinter import scrolledtext as scrt

#-------------------------------------------------------------------------------
''' build first tab '''
class rdmeTab():
    def __init__(self,tabControl):
        self.tab = ttk.Frame(tabControl)
        self.canvas = tk.Canvas(self.tab,width=400,height=300)
        self.canvas.delete('all')
        edge = 20
        self.canvas.create_text(edge,edge,anchor='nw',text='Table Diagram:')
        midx = 200
        midy = 150
        leny = 2*(midx-edge)
        wid = leny/3
        # draw table
        x1 = midx-(leny/2)
        y1 = midy-(wid/2)
        x2 = midx+(leny/2)
        y2 = midy+(wid/2)
        self.canvas.create_line(x1,y1,x2,y1)
        self.canvas.create_line(x2,y1,x2,y2)
        self.canvas.create_line(x2,y2,x1,y2)
        self.canvas.create_line(x1,y2,x1,y1)
        # draw axes
        lin = wid/2
        self.canvas.create_line(x2-15,y2-15,x2-15-lin,y2-15)
        self.canvas.create_line(x2-15,y2-15,x2-15,y2-15-lin)
        x1 = x2-15-lin
        y1 = y2-15-lin
        x2 = x2-15
        y2 = y2-15
        self.canvas.create_line(x1,y2,x1+5,y2+5)
        self.canvas.create_line(x1,y2,x1+5,y2-5)
        self.canvas.create_text(x1-5,y2,anchor='e',text='Y')
        self.canvas.create_line(x2,y1,x2+5,y1+5)
        self.canvas.create_line(x2,y1,x2-5,y1+5)
        self.canvas.create_text(x2,y1-5,anchor='s',text='X')
        # directions
        dire = ' 1. Use the jog buttons to move the torch to the desired start point \n 2. Set the local zero coordinates \n 3. Run the output file in the program \n '
        self.canvas.create_text(midx,midy+lin+15,anchor='n',text=dire)
        self.canvas.pack()

#-------------------------------------------------------------------------------
''' tabs for shape makers '''
class shapeTab():
    ''' initialize tab '''
    def __init__(self,tabControl,mod):
        # use setup to select build model
        self.tab = ttk.Frame(tabControl)
        self.type = mod
        self.inputs = np.array([])
        inbox = np.array([])
        self.frame = ttk.LabelFrame(self.tab,text='Build '+self.type)
        self.frame.grid(column=0,row=0,rowspan=4,padx=8,pady=4)
        if self.type[0] == 'R': # rectangle
            # description
            desc = ' Rectangle corner starts at (0,0) \n Enter all values. \n selection for entry cut distance, output for speeds \t '
            # labels
            self.labels = ['X-width','Y-height','Thickness','Entry Cut','X-copies','Y-copies','Filename']
        elif self.type[0]=='C': # circle
            # description
            desc = ' Pierce starts at (0,0), cuts in to circle edge \n Extends along direction axis \n Enter all values and direction to extend (x or y). \t '
            # labels
            self.labels = ['Diameter','Direction','Thickness','Entry Cut','X-copies','Y-copies','Filename']
        elif self.type[0]=='D': # donut
            # description
            desc = ' Cuts inner diameter circle first \n Shape and offset extends along direction axis \n Enter all values and direction to extend (x or y). \t '
            # labels
            self.labels = ['Outside Diameter','Inside Diameter','Direction','Offset','Thickness','Entry Cut','X-copies','Y-copies','Filename']
        elif self.type[0]=='L': # line
            # description
            desc = ' Line starts at (0,0) Extends along direction axis \n (recommend turning off THC) \t \n Enter all values and direction to extend (x or y). \t '
            # labels
            self.labels = ['Length','Direction','Thickness','Filename']
            
        # description
        ttk.Label(self.frame,text=desc).grid(column=1,row=0,columnspan=5,pady=3)
        # build inputs
        for i in range(0,len(self.labels)):
            if self.labels[i]!='Y-copies':
                ttk.Label(self.frame,text=self.labels[i]+':').grid(column=2,row=i+2,pady=5)
            self.inputs = np.append(self.inputs,tk.StringVar())
            inbox = np.append(inbox,ttk.Entry(self.frame,width=22,textvariable=self.inputs[i]))
            if self.labels[i] not in ['Entry Cut','X-copies','Y-copies']: # input boxes
                inbox[i].grid(column=3,row=i+2,columnspan=4,pady=5)
                if self.type[0]=='L' and self.labels[i]=='Filename':
                    # build button
                    ttk.Button(self.frame,text='Build',command=self.update_build).grid(column=3,row=i+3,columnspan=4,pady=5)
            elif self.labels[i]=='Entry Cut': # entry cut radio buttons
                if self.type[0]=='R' or self.type[0]=='C':
                    rad1 = tk.Radiobutton(self.frame,text='None',variable=self.inputs[i],value='None')
                    rad1.grid(column=3,row=i+2,pady=5,sticky='E')
                    rad2 = tk.Radiobutton(self.frame,text='Inside',variable=self.inputs[i],value='Inside')
                    rad2.grid(column=4,row=i+2,pady=5)
                    rad3 = tk.Radiobutton(self.frame,text='Outside',variable=self.inputs[i],value='Outisde')
                    rad3.grid(column=5,row=i+2,pady=5,sticky='W')
                    self.inputs[i].set('None')
                elif self.type[0]=='D':
                    rad1 = tk.Radiobutton(self.frame,text='None',variable=self.inputs[i],value='None')
                    rad1.grid(column=3,row=i+2,pady=5,sticky='E')
                    rad3 = tk.Radiobutton(self.frame,text='Outside',variable=self.inputs[i],value='Outside')
                    rad3.grid(column=5,row=i+2,pady=5,sticky='W')
                    self.inputs[i].set('None')
            elif self.labels[i]=='X-copies': # copies number spinboxes
                spinX = tk.Spinbox(self.frame,from_=1,to=25,width=4,textvariable=self.inputs[i])
                spinX.grid(column=3,row=i+2,pady=5)
            elif self.labels[i]=='Y-copies':
                ttk.Label(self.frame,text='Y-copies:').grid(column=4,row=i+1,padx=2,pady=5)
                spinY = tk.Spinbox(self.frame,from_=1,to=25,width=4,textvariable=self.inputs[i])
                spinY.grid(column=5,row=i+1,pady=5)
                # build button
                ttk.Button(self.frame,text='Build',command=self.update_build).grid(column=3,row=i+4,columnspan=4,pady=5)
                
        # parameters
        ttk.Label(self.tab,text='Cutting Parameters:').grid(column=1,row=0,padx=8,pady=4,sticky='W')
        self.parameters = scrt.ScrolledText(self.tab,width=25,height=25,wrap=tk.WORD,state='disabled')
        self.parameters.grid(column=1,row=1,rowspan=6,padx=8,pady=4)
        # add tab to main
        tabControl.add(self.tab,text=' '+self.type+' ')
        
    ''' test inputs when Build is pressed '''
    def update_build(self):
        # empty input value list
        invals = []
        # input test
        for i in range(0,len(self.inputs)):
            if self.inputs[i].get(): # not empty
                invals = invals+[self.inputs[i].get()]
                
                if self.labels[i] not in ['Direction','Entry Cut','Filename']: # then numbers inputs
                    try: # check if number
                        invals[i] = float(Fraction(invals[i]))
                    except:
                        invals[i] = False
                    if invals[i] < 0: # check if negative
                        invals[i] = False
                    
                elif self.labels[i] == 'Direction':
                    if len(invals[i])>1 or invals[i] not in ['x','X','y','Y']: # too long or not right
                        invals[i] = False
                    
            else: # empty
                invals = invals+[True]
                if self.labels[i]!='Filename': # file name is optional
                    invals[i] = False
        
        # test for bad input
        for i in range(0,len(invals)):
            if invals[i] is False:
                self.errorMsg()
                return
            # else: good input
        # pull first values
        if self.type[0] in ['R','C','L']: # rectangle, circle, line
            thick = invals[2]
        elif self.type[0] == 'D': # donut
            thick = invals[4]
        # calculate kerf
        try:
            kerf = getKerf(thick)
        except:
            self.errorMsg()
            return
        kerf = round(kerf,4)
        self.fileWrite(invals,kerf,thick)
        self.update_par(thick,kerf)


    ''' write g code to file '''
    def fileWrite(self,invals,kerf,thick):
        # get time stamp
        curtim = datetime.datetime.now()
        start = "[Creation Date: "+curtim.strftime('%x')+" - "+curtim.strftime('%X')+"]\nG92 X0 Y0 Z0\nG90\nM65\n"
        middle = "\n"
        end = "\nM66\n"
        # update params and get ptd
        rec_ptd = self.update_par(thick,kerf)
        # replicators
        xcop = 0
        ycop = 0
        xoff = 0
        yoff = 0
        # define shape specific values then build g-code
        if self.type[0]=='R':
            xlen = round(invals[0],4)
            ylen = round(invals[1],4)
            ent = invals[3]
            xcop = int(invals[4])
            ycop = int(invals[5])
            xoff = xlen+0.75
            yoff = ylen+0.75
            filename = 'rectangle.tap'
            if invals[6]!=True:
                filename = invals[6] + '-' + filename
            midpart = middleRectangle(xlen,ylen,kerf,ent,rec_ptd)
#            middle = middle + middleRectangle(xlen,ylen,kerf,ent)
            
        elif self.type[0]=='C':
            diam = round(invals[0],4)
            direc = invals[1]
            ent = invals[3]
            if ent[0]=='I':
                r1 = round((diam-kerf)/2,4)
            else:
                r1 = round((diam+kerf)/2,4)
            # set repetition values
            xcop = int(invals[4])
            ycop = int(invals[5])
            xoff = diam+0.75
            yoff = diam+0.75
            # set file name
            filename = 'circle.tap'
            if invals[6]!=True:
                filename = invals[6] + '-' + filename
            midpart = middleCircle(r1,direc,ent,rec_ptd)
#            middle = middle + middleCircle(r1,direc,ent)
                
        elif self.type[0]=='D':
            odiam = invals[0]
            idiam = invals[1]
            direc = invals[2]
            offs = round(invals[3],4)
            ent = invals[5]
            xcop = int(invals[6])
            ycop = int(invals[7])
            xoff = round(odiam+0.75,4)
            yoff = round(odiam+0.75,4)
            filename = 'donut.tap'
            if invals[7]!=True:
                filename = invals[8] + '-' + filename
            r1 = round((odiam+kerf)/2,4) # outer radius
            r2 = round((idiam-kerf)/2,4) # inner radius
            midpart = middleDonut(r1,r2,direc,offs,ent,rec_ptd)
#            middle = middle + middleDonut(r1,r2,direc,offs,ent)
            
        for i in range(0,xcop): # repeat x columns
            if i>0: # offset on 2nd step
                middle = middle+'\nG00 X'+str(round(xoff,4))+' Y0.0\nG92 X0 Y0\n'
            for j in range(0,ycop): # do y repeat first
                if j>0: # offset on 2nd step
                    if i % 2 != 0: # offset down on odd steps
                        middle = middle+'\nG00 X0.0 Y'+str(round(-yoff,4))+'\nG92 X0 Y0\n'
                    else: # offset up on even steps
                        middle = middle+'\nG00 X0.0 Y'+str(round(yoff,4))+'\nG92 X0 Y0\n'
                # add shape cutting to middle
                middle = middle + midpart
        
        if self.type[0]=='L':
            leng = round(invals[0],4)
            direc = invals[1]
            filename = 'line.tap'
            middle = middle + middleLine(leng,direc,rec_ptd)
        
        # open file and write
        file = open(filename,'w')
        file.write(start)
        file.write(middle)
        file.write(end)
        file.close()
        self.finalMsg(filename)
        
    ''' update parameters text box '''
    def update_par(self,thick,kerf):
        # calculate recomended amperage
        thicks =   [ 1/4,  3/8,   1/2,  3/4,     1,  1.5,    2,  2.5,    3,    4]
        
        ii_high = False
        ii_match = False
        ii_low = False
        # Find index
        if thick<thicks[0]: # thickness lower
            ii_high = 0
            ii_match = 0
            ii_low = 0
        elif thick>thicks[len(thicks)-1]: # thickness higher
            ii_high = len(thicks)-1
            ii_match = len(thicks)-1
            ii_low = len(thicks)-1
        else: # thickness within range
            for i in range(0,len(thicks)): # test exact match
                if thick==thicks[i]:
                    ii_match = i
                    break
            ii_high = 0
            for i in range(0,len(thicks)): # find higher point
                if thick<thicks[i]:
                    ii_high = i
                    break
            ii_low = len(thicks)-1
            for i in range(len(thicks)-1,0,-1): # find lower point
                if thick>thicks[i]:
                    ii_low = i
                    break
        
        rec_ts = [0,0]
        # [thicks]0,[propPreslow]1,[propPreshigh]2,[oxyPreslow]3,[oxyPreshigh]4,[cutspeedlow]5,[cutspeedhigh]6,[piercetime]7,[tipsize]8
        if ii_match is False: # no match so interpolate between low and high
            m = (Oxy[1][ii_high]-Oxy[1][ii_low])/(thicks[ii_high]-thicks[ii_low])
            rec_ppl = round(m*(thick-thicks[ii_low]) + Oxy[1][ii_low],4)
            m = (Oxy[2][ii_high]-Oxy[2][ii_low])/(thicks[ii_high]-thicks[ii_low])
            rec_pph = round(m*(thick-thicks[ii_low]) + Oxy[2][ii_low],4)
            m = (Oxy[3][ii_high]-Oxy[3][ii_low])/(thicks[ii_high]-thicks[ii_low])
            rec_opl = round(m*(thick-thicks[ii_low]) + Oxy[3][ii_low],4)
            m = (Oxy[4][ii_high]-Oxy[4][ii_low])/(thicks[ii_high]-thicks[ii_low])
            rec_oph = round(m*(thick-thicks[ii_low]) + Oxy[4][ii_low],4)
            m = (Oxy[5][ii_high]-Oxy[5][ii_low])/(thicks[ii_high]-thicks[ii_low])
            rec_csl = round(m*(thick-thicks[ii_low]) + Oxy[5][ii_low],4)
            m = (Oxy[6][ii_high]-Oxy[6][ii_low])/(thicks[ii_high]-thicks[ii_low])
            rec_csh = round(m*(thick-thicks[ii_low]) + Oxy[6][ii_low],4)
            m = (Oxy[7][ii_high]-Oxy[7][ii_low])/(thicks[ii_high]-thicks[ii_low])
            rec_ptd = round(m*(thick-thicks[ii_low]) + Oxy[7][ii_low],4)
            rec_ts = [ Oxy[8][ii_low] , Oxy[8][ii_high] ]
        else: # at bounds so use ii_match
            rec_ppl = Oxy[1][ii_match]
            rec_pph = Oxy[2][ii_match]
            rec_opl = Oxy[3][ii_match]
            rec_oph = Oxy[4][ii_match]
            rec_csl = Oxy[5][ii_match]
            rec_csh = Oxy[6][ii_match]
            rec_ptd = Oxy[7][ii_match]
            rec_ts[0] = Oxy[8][ii_match]
        
        # print to paramters
        self.parameters.config(state='normal')
        # clear panel
        self.parameters.delete(0.0,tk.END)
        # material thickness input
        self.parameters.insert(tk.END,str(round(thick,5))+'in Steel\n')
        # kerf for input parameters
        self.parameters.insert(tk.END,'Predicted Kerf: '+str(kerf)+' in\n\n')
        if rec_ts[1]==0: # match
            self.parameters.insert(tk.END,'Tip Size: '+str(rec_ts[0])+' \n\n')
        else: # two tips
            self.parameters.insert(tk.END,'Tip Size: '+str(rec_ts[0])+'-'+str(rec_ts[1])+' \n\n')
        self.parameters.insert(tk.END,'Propylene Pressure: '+str(rec_ppl)+'-'+str(rec_pph)+' psi\n\n')
        self.parameters.insert(tk.END,'Oxygen Pressure: '+str(rec_opl)+'-'+str(rec_oph)+' psi\n\n')
        self.parameters.insert(tk.END,'Cut Speed: '+str(rec_csl)+'-'+str(rec_csh)+' IPM\n\n')
        self.parameters.insert(tk.END,'Pierce Delay: '+str(rec_ptd)+' sec\n\n')
        self.parameters.config(state='disabled')
        
        return rec_ptd
    
    ''' error message '''
    def errorMsg(self):
        errtit = 'Failed Build'
        errmes = 'Wrong inputs provided, provide proper \ninputs before pressing *Build*.'
        msg.showerror(title=errtit, message=errmes)
        
    ''' completed message '''
    def finalMsg(self,filename):
        inftit = 'TAP file Created'
        infmes1 = 'File Successfully created. \n*'
        infmes2 = '* located in local directory.'
        msg.showinfo(title=inftit,message=infmes1+filename+infmes2)
#        if self.type[0]=='R':
#            msg.showinfo(title=inftit, message=infmes1 + 'rectangle' + infmes2)
#        elif self.type[0]=='C':
#            msg.showinfo(title=inftit, message=infmes1 + 'circle' + infmes2)
#        elif self.type[0]=='D':
#            msg.showinfo(title=inftit, message=infmes1 + 'donut' + infmes2)
#        elif self.type[0]=='L':
#            msg.showinfo(title=inftit, message=infmes1 + 'line' + infmes2)
            
#-------------------------------------------------------------------------------
        # [thicks]0,[propPreslow]1,[propPreshigh]2,[oxyPreslow]3,[oxyPreshigh]4,[cutspeedlow]5,[cutspeedhigh]6,[piercetime]7,[tipsize]8
Oxy =    [[1/4, 3/8, 1/2, 3/4,  1, 1.5,  2, 2.5,  3,   4],
          [  4,   4,   4,   5,  5,   5,  5,   6,  6,   8], [ 6, 6, 6, 9, 9, 9, 9,11,11,12],
          [ 60,  60,  60,  60, 60,  60, 60,  70, 70,  75], [70,70,70,70,70,70,70,80,80,100],
          [ 23,  23,  21,  20, 18,  13, 12,  10,  9,   8], [33,33,31,29,28,20,18,16,15,14],
          [ .1, .25,  .5, .75,  1, 1.5,  2, 2.5,  3, 3.5],
          ['4/0','000','00','0','1','2','2','3','3','4']]

# phased out params and get params

#-------------------------------------------------------------------------------
''' calculate kerf from inputs, return kerf'''
def getKerf(thick):
    # range of thicknesses
    thicks =   [ 1/4,  3/8,   1/2,  3/4,     1,  1.5,    2,  2.5,    3,    4]
    # range of kerfs
    kerfs =    [0.06, 0.07, 0.075, 0.08, 0.085, 0.09, 0.10, 0.11, 0.12, 0.13]
    # test supplied thickness
    if thick<thicks[0]: # thickness lower
        kerf = kerfs[0]
    elif thick>thicks[len(thicks)-1]: # thickness higher
        kerf = kerfs[len(kerfs)-1]
    else: # thickness within range
        for i in range(0,len(thicks)): # test exact match
            if thick==thicks[i]:
                kerf = kerfs[i]
                return kerf
        ii_high = 0
        for i in range(0,len(thicks)): # find higher point
            if thick<thicks[i]:
                ii_high = i
                break
        ii_low = len(thicks)-1
        for i in range(len(thicks)-1,0,-1): # find lower point
            if thick>thicks[i]:
                ii_low = i
                break
        # interpolate kerf from points
        m = (kerfs[ii_high]-kerfs[ii_low])/(thicks[ii_high]-thicks[ii_low])
        kerf = m*(thick-thicks[ii_low]) + kerfs[ii_low]
    return kerf
    
''' build middle g-code for rectangle '''
def middleRectangle(xlen,ylen,kerf,ent,rec_ptd):
    part1 = '\nG04 [adjust torch to cut height, wait for pre-heat]\nG00 Z0.6 [raise torch up 0.6in]\nM11C4 [trigger solenoid]\nG04 X'+str(rec_ptd)+' [wait x time for pierce]\n'
    middle = "G00 X0.0 Y0.0" #(0,0)
    # no entry cut
    if ent[0]=='N': # None
        part2 = 'G01 Z-0.05 [drive into cut]\n'
        # 0 kerf+len , no curves
        x1 = round(xlen+kerf,4)
        y1 = round(ylen+kerf,4)
        middle = middle+part1+part2+"G01 X0.0 Y"+str(y1)
        middle = middle+"\nG01 X"+str(x1)
        middle = middle+"\nG01 Y0.0"
        middle = middle+"\nG01 X0.0 Y0.0\nM62\n"
        
    # entry cut inside part, offset kerf to inner
    elif ent[0]=='I':
        # 0 ent len-kerf , only curves on entry
        # ent = 0.5
        x1 = round(0.5,4)
        x2 = round(xlen-kerf,4)
        y1 = round(0.5,4)
        y2 = round(ylen-kerf,4)
        middle = middle+"\nG00 X"+str(x1)+" Y"+str(y1)
        middle = middle+part1+"G03 X0.0 Y0.0 Z-0.05 J-"+str(y1)
        middle = middle+"\nG01 X"+str(x2)+" Y0.0"
        middle = middle+"\nG01 Y"+str(y2)
        middle = middle+"\nG01 X0.0"
        middle = middle+"\nG01 Y0.0"
        middle = middle+"\nG03 X"+str(x1)+" Y"+str(y1)+" J"+str(y1)+"\nM62\n"
        
    # entry cut outside part, offset kerf outer
    elif ent[0]=='O':
        # 0 ent ent+1/2kerf ent+1/2kerf+len ent+kerf+len , straight entry with curved corners
        # ent = 0.2
        x1 = round(0.2,4)
        x2 = round(0.2+(kerf/2),4)
        x3 = round(0.2+(kerf/2)+xlen,4)
        x4 = round(0.2+kerf+xlen,4)
        y1 = round(0.2,4)
        y2 = round(0.2+(kerf/2),4)
        y3 = round(0.2+(kerf/2)+ylen,4)
        y4 = round(0.2+kerf+ylen,4)
        cr1 = round(kerf/2,4)
        middle = middle+"\nG00 X"+str(x1)+" Y0.0"
        middle = middle+part1+"G01 Y"+str(y3)+' Z-0.05'
        middle = middle+"\nG02 X"+str(x2)+" Y"+str(y4)+" I"+str(cr1)
        middle = middle+"\nG01 X"+str(x3)
        middle = middle+"\nG02 X"+str(x4)+" Y"+str(y3)+" J-"+str(cr1)
        middle = middle+"\nG01 Y"+str(y2)
        middle = middle+"\nG02 X"+str(x3)+" Y"+str(y1)+" I-"+str(cr1)
        middle = middle+"\nG01 X0.0\nM62\n"
        
    return middle
        
''' build middle g-code for circle '''
def middleCircle(r1,direc,ent,rec_ptd):
    part1 = '\nG04 [adjust torch to cut height, wait for pre-heat]\nG00 Z0.6 [raise torch up 0.6in]\nM11C4 [trigger solenoid]\nG04 X'+str(rec_ptd)+' [wait x time for pierce]\n'
    middle = "G00 X0.0 Y0.0" #(0,0)
    if ent[0]=='N': # None
        part2 = 'G01 Z-0.05 [drive into cut]\n'
        if direc in ['x','X']:
            middle = middle+part1+part2+"G02 I"+str(r1)+"\nM62\n"
        elif direc in ['y','Y']:
            middle = middle+part1+part2+"G02 J"+str(r1)+"\nM62\n"
    # inside entry cut
    elif ent[0]=='I':
        # part2 is added to entry cut
        if direc in ['x','X']:
            if r1 <= 1: # for small holes start cut in center
                middle = middle+"\nG00 X"+str(r1)+"\n"
                middle = middle+part1+"G01 X0.0 Z-0.05"
                middle = middle+"\nG03 I"+str(r1)
                middle = middle+"\nG01 X"+str(r1)+" Y0.0\nM62\n"
            elif 1 < r1 <= 6: # use between .25 and .5 radius for entry radius
                er1 = round((0.25*(r1-1)/5) + 0.25,4)
                middle = middle+"\nG00 X"+str(er1)+" Y"+str(er1)+"\n"
                middle = middle+part1+"G03 X0.0 Y0.0 Z-0.05 J-"+str(er1)
                middle = middle+"\nG03 I"+str(r1)
                middle = middle+"\nG03 X"+str(er1)+" Y-"+str(er1)+" I"+str(er1)+"\nM62\n"
            else: # otherwise cut entry on 0.5 radius arc
                middle = middle+"\nG00 X0.5 Y0.5\n"
                middle = middle+part1+"G03 X0.0 Y0.0 Z-0.05 J-0.5"
                middle = middle+"\nG03 I"+str(r1)
                middle = middle+"\nG03 X0.5 Y-0.5 I0.5\nM62\n"
        elif direc in ['y','Y']:
            if r1 <= 1:
                middle = middle+"\nG00 Y"+str(r1)+"\n"
                middle = middle+part1+"G01 Y0.0 Z-0.05"
                middle = middle+"\nG03 J"+str(r1)
                middle = middle+"\nG01 X0.0 Y"+str(r1)+"\nM62\n"
            elif 1 < r1 <= 6:
                er1 = round((0.25*(r1-1)/5) + 0.25,4)
                middle = middle+"\nG00 X-"+str(er1)+" Y"+str(er1)+"\n"
                middle = middle+part1+"G03 X0.0 Y0.0 Z-0.05 I"+str(er1)
                middle = middle+"\nG03 J"+str(r1)
                middle = middle+"\nG03 X"+str(er1)+" Y"+str(er1)+" J"+str(er1)+"\nM62\n"
            else:
                middle = middle+"\nG00 X-0.5 Y0.5\n"
                middle = middle+part1+"G03 X0.0 Y0.0 Z-0.05 I0.5"
                middle = middle+"\nG03 J"+str(r1)
                middle = middle+"\nG03 X0.5 Y0.5 J0.5\nM62\n"
    # outside entry cut
    elif ent[0]=='O':
        er1 = 0.4 # calc entry cut radius
        if r1 <= 1:
            er1 = 0.25
        elif 1 < r1 <= 6:
            er1 = round((0.15*(r1-1)/5) + 0.25,4)
        
        if direc in ['x','X']:
            middle = middle+"\nG00 Y-"+str(er1)+"\n"
            middle = middle+part1+"G03 X"+str(er1)+" Y0.0 Z-0.05 J"+str(er1)+""
            middle = middle+"\nG02 I"+str(r1)
            middle = middle+"\nG03 X0.0 Y"+str(er1)+" I-"+str(er1)+"\nM62\n"
        elif direc in ['y','Y']:
            middle = middle+"\nG00 X"+str(er1)+"\n"
            middle = middle+part1+"G03 X0.0 Y"+str(er1)+" Z-0.05 I-"+str(er1)
            middle = middle+"\nG02 J"+str(r1)
            middle = middle+"\nG03 X-"+str(er1)+" Y0.0 J-"+str(er1)+"\nM62\n"
    # return the code
    return middle

''' build middle g-code for donut '''
def middleDonut(r1,r2,direc,offs,ent,rec_ptd):
    # r1 = outer radius
    # r2 = inner radius
    # d1 = distance between circles
    # outer start at 0
    # offset outer by 0.25 for start, go up to 0.4
    # inner start at 0.5 + d1 + r2 (or 0.5)
    # offset inner start by 0.5 + r2 (or 0.5)
    part1 = '\nG04 [adjust torch to cut height, wait for pre-heat]\nG00 Z0.6 [raise torch up 0.6in]\nM11C4 [trigger solenoid]\nG04 X'+str(rec_ptd)+' [wait x time for pierce]\n'
    middle = "G00 X0.0 Y0.0" #(0,0)
    d1 = round(r1-r2+offs,4)
    if ent[0]=='N':
        part2 = 'G01 Z-0.05 [drive into cut]\n'
        if direc in ['x','X']:
            middle = middle+"\nG00 X"+str(d1)
            middle = middle+part1+part2+"G03 I"+str(r2)+"\nM62\n" # interior hole CCW
            middle = middle+"\nG00 X0.0 Y0.0"
            middle = middle+part1+part2+"G02 I"+str(r1)+"\nM62\n"
        elif direc in ['y','Y']:
            middle = middle+"\nG00 Y"+str(d1)
            middle = middle+part1+part2+"G03 J"+str(r2)+"\nM62\n" # interior hole CCW
            middle = middle+"\nG00 X0.0 Y0.0"
            middle = middle+part1+part2+"G02 J"+str(r1)+"\nM62\n"
    # entry cut
    else:
        # outer circle entry cut radius
        er1 = 0.5
        if r1 <= 1:
            er1 = 0.25
        elif 1 < r1 <= 6:
            er1 = round((0.25*(r1-1)/5) + 0.25,4)
        # inner circle entry cut adius
        er2 = 0.4
        if r2 <= 1:
            er2 = 0.25
        elif 1 < r2 <= 6:
            er2 = round((0.15*(r2-1)/5) + 0.25,4)
        in1a = round(er1+d1+r2,4) # inner circle start a
        in1b = round(er1+d1+er2,4) # inner circle start b
        in2 = round(er1+d1,4) # inner circle edge
        if direc in ['x','X']:
            if r2 <= 1: # for small center holes start cut in center
                # inner circle
                middle = middle+"\nG00 X"+str(in1a)
                middle = middle+part1+"G01 X"+str(in2)+' Z-0.05'
                middle = middle+"\nG03 I"+str(r2) # interior hole CCW
                middle = middle+"\nG01 X"+str(in1a)+" Y0.0\nM62\n"
            else: # otherwise arc entry for inside and out
                # inner circle
                middle = middle+"\nG00 X"+str(in1b)+" Y"+str(er2)
                middle = middle+part1+"G03 X"+str(in2)+" Y0.0 Z-0.05 J-"+str(er2)
                middle = middle+"\nG03 I"+str(r2)
                middle = middle+"\nG03 X"+str(in1b)+" Y-"+str(er2)+" I"+str(er2)+"\nM62\n"
            # outer circle (the same)
            middle = middle+"\nG00 X0.0 Y-"+str(er1)
            middle = middle+part1+"G03 X"+str(er1)+" Y0.0 Z-0.05 J"+str(er1)
            middle = middle+"\nG02 I"+str(r1)
            middle = middle+"\nG03 X0.0 Y"+str(er1)+" I-"+str(er1)+"\nM62\n"
        elif direc in ['y','Y']:
            if r2 <= 1:
                # inner circle
                middle = middle+"\nG00 Y"+str(in1a)
                middle = middle+part1+"G01 Y"+str(in2)+' Z-0.05'
                middle = middle+"\nG03 J"+str(r2)
                middle = middle+"\nG01 X0.0 Y"+str(in1a)+"\nM62\n"
            else:
                # inner circle
                middle = middle+"\nG00 X-"+str(er2)+" Y"+str(in1b)
                middle = middle+part1+"G03 X0.0 Y"+str(in2)+" Z-0.05 I"+str(er2)
                middle = middle+"\nG03 J"+str(r2)
                middle = middle+"\nG03 X"+str(er2)+" Y"+str(in1b)+" J"+str(er2)+"\nM62\n"
            # outer circle (the same)
            middle = middle+"\nG00 X"+str(er1)+" Y0.0"
            middle = middle+part1+"G03 X0.0 Y"+str(er1)+" Z-0.05 I-"+str(er1)
            middle = middle+"\nG02 J"+str(r1)
            middle = middle+"\nG03 X-"+str(er1)+" Y0.0 J-"+str(er1)+"\nM62\n"
    return middle

''' build middle g-code for line '''
def middleLine(leng,direc,rec_ptd):
    part1 = '\nG04 [adjust torch to cut height, wait for pre-heat]\nG00 Z0.6 [raise torch up 0.6in]\nM11C4 [trigger solenoid]\nG04 X'+str(rec_ptd)+' [wait x time for pierce]\nG01 Z-0.05 [drive into cut]\n'
    middle = "G00 X0.0 Y0.0" #(0,0)
    if direc=='x':
        middle = middle+part1+"G01 X"+str(leng)+"\nM62\n"
    elif direc=='y':
        middle = middle+part1+"G01 Y"+str(leng)+"\nM62\n"
    return middle
    
#-------------------------------------------------------------------------------
''' main functions '''
master = tk.Tk()
master.title('Oxy Gcode Maker')
tabControl = ttk.Notebook(master)

# outline
rdme = rdmeTab(tabControl)
tabControl.add(rdme.tab,text=' Directions ')

# rectangle
rect = shapeTab(tabControl,'Rectangle')

# circle
circ = shapeTab(tabControl,'Circle')

# donut
dnut = shapeTab(tabControl,'Donut')

# line
line = shapeTab(tabControl,'Line')

tabControl.pack()

master.mainloop()