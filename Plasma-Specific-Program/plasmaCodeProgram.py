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
            self.labels = ['X-width','Y-height','Material','Thickness','Amperage','Entry Cut','X-copies','Y-copies','Filename']
        elif self.type[0]=='C': # circle
            # description
            desc = ' Pierce starts at (0,0), cuts in to circle edge \n Extends along direction axis \n Enter all values and direction to extend (x or y). \t '
            # labels
            self.labels = ['Diameter','Direction','Material','Thickness','Amperage','Entry Cut','X-copies','Y-copies','Filename']
        elif self.type[0]=='D': # donut
            # description
            desc = ' Cuts inner diameter circle first \n Shape and offset extends along direction axis \n Enter all values and direction to extend (x or y). \t '
            # labels
            self.labels = ['Outside Diameter','Inside Diameter','Direction','Offset','Material','Thickness','Amperage','Entry Cut','X-copies','Y-copies','Filename']
        elif self.type[0]=='L': # line
            # description
            desc = ' Line starts at (0,0) Extends along direction axis \n (recommend turning off THC) \t \n Enter all values and direction to extend (x or y). \t '
            # labels
            self.labels = ['Length','Direction','Material','Thickness','Amperage']
            
        # description
        ttk.Label(self.frame,text=desc).grid(column=1,row=0,columnspan=5,pady=3)
        # build inputs
        for i in range(0,len(self.labels)):
            if self.labels[i]!='Y-copies':
                ttk.Label(self.frame,text=self.labels[i]+':').grid(column=2,row=i+2,pady=5)
            self.inputs = np.append(self.inputs,tk.StringVar())
            inbox = np.append(inbox,ttk.Entry(self.frame,width=22,textvariable=self.inputs[i]))
            if self.labels[i] not in ['Material','Amperage','Entry Cut','X-copies','Y-copies']: # input boxes
                inbox[i].grid(column=3,row=i+2,columnspan=4,pady=5)
            elif self.labels[i]=='Material': # material selection drop down
                m_drop = ttk.Combobox(self.frame,width=19,textvariable=self.inputs[i],state='readonly')
                m_drop['values'] = ('Mild Steel','Stainless Steel','Aluminum')
                m_drop.grid(column=3,row=i+2,columnspan=4,pady=5,padx=10)
                m_drop.current(0)
            elif self.labels[i]=='Amperage': # amperage selection drop down
                a_drop = ttk.Combobox(self.frame,width=19,textvariable=self.inputs[i],state='readonly')
                a_drop['values'] = ('85A','65A','45A','FineCut')
                a_drop.grid(column=3,row=i+2,columnspan=4,pady=5)
                a_drop.current(0)
                if self.type[0]=='L':
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
                
                if self.labels[i] not in ['Direction','Material','Amperage','Entry Cut','Filename']: # then numbers inputs
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
                    invals = invals+[False]
        
        # test for bad input
        for i in range(0,len(invals)):
            if invals[i] is False:
                self.errorMsg()
                return
        
        # else: good input
        # pull first values
        if self.type[0] in ['R','C','L']: # rectangle, circle, line
            mat = invals[2]
            thick = invals[3]
            amp = invals[4]
        elif self.type[0] == 'D': # donut
            mat = invals[4]
            thick = invals[5]
            amp = invals[6]
        # calculate kerf
        try:
            kerf = getKerf(mat,thick,amp)
        except:
            self.errorMsg()
            return
        kerf = round(kerf,4)
        self.fileWrite(invals,kerf)
        self.update_par(mat,thick,amp,kerf)
        
            
    ''' write g code to file '''
    def fileWrite(self,invals,kerf):
        # get time stamp
        curtim = datetime.datetime.now()
        start = "[Creation Date: "+curtim.strftime('%x')+" - "+curtim.strftime('%X')+"]\nG92 X0 Y0 Z0\nG90\nM65\n"
        middle = "\n"
        end = "\nM66\n"
        xcop = 0
        ycop = 0
        xoff = 0
        yoff = 0
        # define specific values then build g-code
        if self.type[0]=='R':
            xlen = round(invals[0],4)
            ylen = round(invals[1],4)
            ent = invals[5]
            xcop = int(invals[6])
            ycop = int(invals[7])
            xoff = xlen+0.75
            yoff = ylen+0.75
            filename = 'rectangle.tap'
            if invals[8]!=True:
                filename = invals[8] + '-' + filename
            midpart = middleRectangle(xlen,ylen,kerf,ent)
#            middle = middle + middleRectangle(xlen,ylen,kerf,ent)
            
        elif self.type[0]=='C':
            diam = round(invals[0],4)
            direc = invals[1]
            ent = invals[5]
            if ent[0]=='I':
                r1 = round((diam-kerf)/2,4)
            else:
                r1 = round((diam+kerf)/2,4)
            # set repetition values
            xcop = int(invals[6])
            ycop = int(invals[7])
            xoff = diam+0.75
            yoff = diam+0.75
            # set file name
            filename = 'circle.tap'
            if invals[8]!=True:
                filename = invals[8] + '-' + filename
            midpart = middleCircle(r1,direc,ent)
#            middle = middle + middleCircle(r1,direc,ent)
                
        elif self.type[0]=='D':
            odiam = round(invals[0],4) 
            idiam = round(invals[1],4)
            direc = invals[2]
            offs = round(invals[3],4)
            ent = invals[7]
            xcop = int(invals[8])
            ycop = int(invals[9])
            xoff = odiam+0.75
            yoff = odiam+0.75
            filename = 'donut.tap'
            if invals[10]!=True:
                filename = invals[10] + '-' + filename
            r1 = round((odiam+kerf)/2,4) # outer radius
            r2 = round((idiam-kerf)/2,4) # inner radius
            midpart = middleDonut(r1,r2,direc,offs,ent)
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
            middle = middle + middleLine(leng,direc)
        
        # open file and write
        file = open(filename,'w')
        file.write(start)
        file.write(middle)
        file.write(end)
        file.close()
        self.finalMsg(filename)
        
    ''' update parameters text box '''
    def update_par(self,mat,thick,amp,kerf):
        # calculate recomended amperage
        steel_th = [.0299, .0478, .0747, .1345, 3/16, 1/4, 3/8, 1/2, 5/8, 3/4]
        al_th = [1/32, 1/16, 1/8, 3/16, 1/4, 3/8, 1/2, 5/8, 3/4]
        rec_amp = 0
        if mat[0]=='M':
            if steel_th[3] <= thick <= steel_th[9]: # test 85A
                rec_amp = '85A'
            elif steel_th[2] <= thick <= steel_th[9]: # test 65A
                rec_amp = '65A'
            elif steel_th[0] <= thick <= steel_th[5]: # test 45A
                rec_amp = '45A'
            else:
                rec_amp = 'xx'
        elif mat[0]=='S':
            if steel_th[3] <= thick <= steel_th[9]: # test 85A
                rec_amp = '85A'
            elif steel_th[2] <= thick <= steel_th[9]: # test 65A
                rec_amp = '65A'
            elif steel_th[0] <= thick <= steel_th[5]: # test 45A
                rec_amp = '45A'
            else:
                rec_amp = 'xx'
        elif mat[0]=='A':
            if al_th[2] <= thick <= al_th[8]: # test 85A
                rec_amp = '85A'
            elif al_th[1] <= thick <= al_th[7]: # test 65A
                rec_amp = '65A'
            elif al_th[0] <= thick <= al_th[4]: # test 45A
                rec_amp = '45A'
            else:
                rec_amp = 'xx'
        
        # print to paramters
        self.parameters.config(state='normal')
        # clear panel
        self.parameters.delete(0.0,tk.END)
        # material thickness input
        self.parameters.insert(tk.END,str(round(thick,5))+' in '+mat+'\n')
        # recomended amperage
        self.parameters.insert(tk.END,'Recommended Amperage: '+rec_amp+'\n') 
        # kerf for input parameters
        self.parameters.insert(tk.END,'Predicted Kerf: '+str(kerf)+' in\n\n')
        # get the parameters
        pset = [[0,0],[0,0],0,0,0,0] # [volt,speed,cutheight,pierceheight,piercedelay,rec_amp]
        if amp[0]=='8':
            if mat[0]=='M':
                pset = get_params(Mild85,thick)
            elif mat[0]=='S':
                pset = get_params(Stain85,thick)
            elif mat[0]=='A':
                pset = get_params(Alum85,thick)
        elif amp[0]=='6':
            if mat[0]=='M':
                pset = get_params(Mild65,thick)
            elif mat[0]=='S':
                pset = get_params(Stain65,thick)
            elif mat[0]=='A':
                pset = get_params(Alum65,thick)
        elif amp[0]=='4':
            if mat[0]=='M':
                pset = get_params(Mild45,thick)
            elif mat[0]=='S':
                pset = get_params(Stain45,thick)
            elif mat[0]=='A':
                pset = get_params(Alum45,thick)
        elif amp[0]=='F':
            if mat[0]=='M':
                pset = get_params(MildFC,thick)
            elif mat[0]=='S':
                pset = get_params(StainFC,thick)
        else:
            self.parameters.insert(tk.END,'Thickness is outside possible values\n')
            return
        self.parameters.insert(tk.END,'Voltage: '+str(pset[0][0])+'-'+str(pset[0][1])+' Volts\n\n')
        self.parameters.insert(tk.END,'Cutting Speed: '+str(pset[1][0])+'-'+str(pset[1][1])+' IPM\n\n')
        self.parameters.insert(tk.END,'Cut Height: '+str(pset[2])+' in\n\n')
        self.parameters.insert(tk.END,'Pierce Height: '+str(pset[3])+' in\n\n')
        self.parameters.insert(tk.END,'Pierce Delay: '+str(pset[4])+' sec\n\n')
        self.parameters.insert(tk.END,'Amperage: '+str(pset[5])+' Amps\n\n')
        self.parameters.config(state='disabled')
    
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
        # [thicks 0; voltage range 12; cut speed range 34; torch height 5; pierce height 6; pierce delay 7; amperage 8]
Mild85 = [[.1345, 3/16, 1/4, 3/8, 1/2, 5/8, 3/4],
          [122, 123, 123, 126, 131, 134, 136], [121, 123, 126, 127, 131, 133, 135],
          [250, 185, 130, 70, 45, 35, 24], [336, 220, 160, 86, 56, 37, 29],
          [.06, .06, .06, .06, .06, .06, .06],
          [.15, .15, .15, .15, .18, .18, .24],
          [.2, .2, .5, .5, .5, 1, 1.5],
          [85, 85, 85, 85, 85, 85, 85]]
Stain85 = [[.1345, 3/16, 1/4, 3/8, 1/2, 5/8],
           [122, 122, 122, 126, 132, 135], [120, 121, 122, 125, 131, 134],
           [275, 200, 130, 65, 36, 28], [336, 240, 164, 80, 48, 30],
           [.06, .06, .06, .06, .06, .06],
           [0.15, 0.15, 0.15, 0.15, .18, .18],
           [.2, .2, .5, .5, .5, 1],
           [85, 85, 85, 85, 85, 85]]
Alum85 = [[1/8, 1/4, 3/8, 1/2, 5/8],
          [122, 127, 132, 135, 139], [121, 127, 131, 133, 137],
          [300, 130, 80, 50, 38], [360, 172, 104, 68, 48],
          [.06, .06, .06, .06, .06],
          [.15, .15, .15, .18, .18],
          [.2, .5, .5, .5, 1],
          [85, 85, 85, 85, 85]]
Mild65 = [[.1345, 3/16, 1/4, 3/8, 1/2, 5/8],
          [125, 126, 127, 130, 135, 138], [123, 125, 127,  129, 132, 136],
          [190, 140, 90, 45, 30, 23], [224, 168, 116, 62, 40, 26],
          [.06, .06, .06, .06, .06, .06],
          [.15, .15, .15, .15, .18, .24],
          [.1, .2, .5, .7, 1.2, 2],
          [65, 65, 65, 65, 65, 65]]
Stain65 = [[.1345, 3/16, 1/4, 3/8, 1/2],
           [125, 126, 126, 131, 136], [123, 125, 126, 131, 135],
           [240, 155, 80, 40, 26], [296, 168, 96, 52, 32],
           [.06, .06, .06, .06, .06],
           [.15, .15, .15, .15, .18],
           [.1, .2, .5, .7, 1.2],
           [65, 65, 65, 65, 65]]
Alum65 = [[1/16, 1/8, 1/4, 3/8, 1/2],
          [121, 124, 131, 135, 139], [121, 124, 128, 131, 138],
          [365, 280, 105, 50, 35], [428, 336, 152, 68, 48],
          [.06, .06, .06, .06, .06],
          [.15, .15, .15, .15, .18],
          [.1, .1, .5, .7, 1.2],
          [65, 65, 65, 65, 65]]
Mild45 = [[.0179, .0299, .0478, .0598, .0747, .1046, .1345, 3/16, 1/4],
          [128, 128, 129, 130, 130, 133, 134, 135, 137], [128, 128, 128, 129, 129, 131, 131, 132, 132],
          [350, 350, 350, 350, 270, 190, 100, 70, 48], [500, 450, 400, 400, 320, 216, 164, 108, 73],
          [.06, .06, .06, .06, .06, .06, .06, .06, .06],
          [.15, .15, .15, .15, .15, .15, .15, .15, .15],
          [.01, .01, .1, .1, .2, .4, .4, .5, .6],
          [45, 45, 45, 45, 45, 45, 45, 45, 45]]
Stain45 = [[.0179, .0299, .0478, .0598, .0747, .1046, .1345, 3/16, 1/4],
           [130, 130, 130, 130, 132, 132, 133, 135, 141], [129, 129, 130, 130, 131, 131, 134, 135, 140],
           [350, 350, 350, 350, 250, 140, 100, 52, 30], [500, 450, 400, 400, 360, 206, 134, 58, 35],
           [.06, .06, .06, .06, .06, .06, .06, .06, .06],
           [.15, .15, .15, .15, .15, .15, .15, .15, .15],
           [.01, .01, .1, .1, .2, .4, .4, .5, .6],
           [45, 45, 45, 45, 45, 45, 45, 45, 45]]
Alum45 = [[1/32, 1/16, 3/32, 1/8, 1/4],
          [136, 136, 136, 140, 142], [136, 136, 134, 134, 137],
          [325, 325, 200, 100, 54], [450, 400, 328, 224, 96],
          [.06, .06, .06, .06, .06],
          [.15, .15, .15, .15, .15],
          [.01, .1, .2, .4, .5],
          [45, 45, 45, 45, 45]]
MildFC = [[.0179, .0239, .0299, .0359, .0478, .0598, .0747, .1046, .1345],
          [78, 78, 78, 78, 78, 78, 78, 78, 78], [78, 78, 78, 78, 78, 78, 78, 78, 78],
          [325, 325, 325, 325, 325, 250, 200, 120, 95], [325, 325, 325, 325, 325, 250, 200, 120, 95],
          [.06, .06, .06, .06, .06, .06, .06, .06, .06],
          [.15, .15, .15, .15, .15, .15, .15, .15, .15],
          [.01, .01, .1, .1, .2, .4, .4, .5, .5],
          [40, 40, 40, 40, 45, 45, 45, 45, 45]]
StainFC = [[.0179, .0239, .0299, .0359, .0478, .0598, .0747, .1046, .1345],
           [68, 68, 68, 68, 68, 70, 70, 80, 80], [68, 68, 68, 68, 68, 70, 70, 80, 80],
           [325, 325, 325, 325, 325, 240, 200, 120, 75], [325, 325, 325, 325, 325, 240, 200, 120, 75],
           [.02, .02, .02, .02, .02, .02, .02, .02, .02],
           [.08, .08, .08, .08, .08, .08, .08, .08, .08],
           [.01, .01, .1, .1, .2, .4, .4, .5, .6],
           [40, 40, 40, 40, 45, 45, 45, 45, 45]]
    # if thick>Mild85[len(Mild85)-1]: edge start

''' define paramters from thickness and defined set, return set '''
def get_params(matnums,thick):
    ii_low = 0
    ii_high = len(matnums[0])-1
    for i in range(0,len(matnums[0])):
        if thick<=matnums[0][i]:
            ii_low = i
            break
    for i in range(len(matnums[0])-1,0,-1):
        if thick>=matnums[0][i]:
            ii_high = i
            break
    # [thicks 0; voltage range 12; cut speed range 34; torch height 5; pierce height 6; pierce delay 7; amperage 8]
    outs = [[0,0],[0,0],0,0,0,0] # [volt,speed,cutheight,pierceheight,piercedelay,rec_amp]
    if ii_low!=ii_high:
        # voltage
        x1 = (matnums[1][ii_low] + matnums[1][ii_high])/2
        x2 = (matnums[2][ii_low] + matnums[2][ii_high])/2
        outs[0] = [x1,x2]
        # cutting speed
        x1 = (matnums[3][ii_low] + matnums[3][ii_high])/2
        x2 = (matnums[4][ii_low] + matnums[4][ii_high])/2
        outs[1] = [x1,x2]
        # cut height
        x1 = (matnums[5][ii_low] + matnums[5][ii_high])/2
        outs[2] = x1
        # pierce height
        x1 = (matnums[6][ii_low] + matnums[6][ii_high])/2
        outs[3] = x1
        # pierce delay
        x1 = (matnums[7][ii_low] + matnums[7][ii_high])/2
        outs[4] = x1
        # amperage
        x1 = (matnums[8][ii_low] + matnums[8][ii_high])/2
        outs[5] = x1
    else:
        outs[0] = [matnums[1][ii_high],matnums[2][ii_high]]
        outs[1] = [matnums[3][ii_high],matnums[4][ii_high]]
        outs[2] = matnums[5][ii_high]
        outs[3] = matnums[6][ii_high]
        outs[4] = matnums[7][ii_high]
        outs[5] = matnums[8][ii_high]
    return outs

#-------------------------------------------------------------------------------
''' calculate kerf from inputs, return kerf'''
def getKerf(mat,thick,amp):
    # range of thicknesses
    steel_th = [.0299, .0478, .0747, .1345, 3/16, 1/4, 3/8, 1/2, 5/8, 3/4]
    al_th = [1/32, 1/16, 1/8, 3/16, 1/4, 3/8, 1/2, 5/8, 3/4]
    # define min and max thicknesses based on material and amperage
    if mat[0]=='M': # mild steel
        thicks = steel_th
        if amp[0]=='8':
            thicks = steel_th[3:10]
            kerfs = [.068, .071, .073, .078, .090, .095, .1]
        elif amp[0]=='6':
            thicks = steel_th[2:10]
            kerfs = [.062, .065, .068, .07, .076, .088, .09, .091]
        elif amp[0]=='4':
            thicks = steel_th[0:6]
            kerfs = [.035, .054, .055, .061, .065, .066]
        elif amp[0]=='F':
            thicks = steel_th[0:4]
            kerfs = [.024, .043, .049, .053]
        else: # outside range
            raise Exception()
            return
    elif mat[0]=='S': # stainless
        thicks = steel_th
        if amp[0]=='8':
            thicks = steel_th[3:10]
            kerfs = [.065, .068, .07, .08, .094, .095, .096]
        elif amp[0]=='6':
            thicks = steel_th[2:10]
            kerfs = [.056, .062, .068, .073, .076, .090, .093, .096]
        elif amp[0]=='4':
            thicks = steel_th[0:6]
            kerfs = [.032, .055, .058, .067, .069, .069]
        elif amp[0]=='F':
            thicks = steel_th[0:4]
            kerfs = [.018, .036, .040, .055]
        else: # outside range
            raise Exception()
            return
    elif mat[0]=='A': # aluminum
        thicks = al_th
        if amp[0]=='8':
            thicks = al_th[2:9]
            kerfs = [.08, .078, .075, .08, .09, .095, .1]
        elif amp[0]=='6':
            thicks = al_th[1:8]
            kerfs = [.073, .074, .075, .076, .083, .091, .1]
        elif amp[0]=='4':
            thicks = al_th[0:5]
            kerfs = [.059, .061, .065, .063, .060]
        # no finecut for aluminum
        else: # outside range
            raise Exception()
            return
    else: # outside range
        raise Exception()
        return
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
def middleRectangle(xlen,ylen,kerf,ent):
    middle = "G00 X0.0 Y0.0" #(0,0)
    # no entry cut
    if ent[0]=='N': # None
        # 0 kerf+len , no curves
        x1 = round(xlen+kerf,4)
        y1 = round(ylen+kerf,4)
        middle = middle+"\nM61\nG01 X0.0 Y"+str(y1)
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
        middle = middle+"\nM61\nG03 X0.0 Y0.0 J-"+str(y1)
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
        middle = middle+"\nM61\nG01 Y"+str(y3)
        middle = middle+"\nG02 X"+str(x2)+" Y"+str(y4)+" I"+str(cr1)
        middle = middle+"\nG01 X"+str(x3)
        middle = middle+"\nG02 X"+str(x4)+" Y"+str(y3)+" J-"+str(cr1)
        middle = middle+"\nG01 Y"+str(y2)
        middle = middle+"\nG02 X"+str(x3)+" Y"+str(y1)+" I-"+str(cr1)
        middle = middle+"\nG01 X0.0\nM62\n"
        
    return middle
        
''' build middle g-code for circle '''
def middleCircle(r1,direc,ent):
    middle = "G00 X0.0 Y0.0" #(0,0)
    if ent[0]=='N': # None
        if direc in ['x','X']:
            middle = middle+"\nM61\nG02 I"+str(r1)+"\nM62\n"
        elif direc in ['y','Y']:
            middle = middle+"\nM61\nG02 J"+str(r1)+"\nM62\n"
    # inside entry cut
    elif ent[0]=='I':
        if direc in ['x','X']:
            if r1 <= 1: # for small holes start cut in center
                middle = middle+"\nG00 X"+str(r1)+"\n"
                middle = middle+"\nM61\nG01 X0.0"
                middle = middle+"\nG03 I"+str(r1)
                middle = middle+"\nG01 X"+str(r1)+" Y0.0\nM62\n"
            elif 1 < r1 <= 6: # use between .25 and .5 radius for entry radius
                er1 = round((0.25*(r1-1)/5) + 0.25,4)
                middle = middle+"\nG00 X"+str(er1)+" Y"+str(er1)+"\n"
                middle = middle+"\nM61\nG03 X0.0 Y0.0 J-"+str(er1)
                middle = middle+"\nG03 I"+str(r1)
                middle = middle+"\nG03 X"+str(er1)+" Y-"+str(er1)+" I"+str(er1)+"\nM62\n"
            else: # otherwise cut entry on 0.5 radius arc
                middle = middle+"\nG00 X0.5 Y0.5\n"
                middle = middle+"\nM61\nG03 X0.0 Y0.0 J-0.5"
                middle = middle+"\nG03 I"+str(r1)
                middle = middle+"\nG03 X0.5 Y-0.5 I0.5\nM62\n"
        elif direc in ['y','Y']:
            if r1 <= 1:
                middle = middle+"\nG00 Y"+str(r1)+"\n"
                middle = middle+"\nM61\nG01 Y0.0"
                middle = middle+"\nG03 J"+str(r1)
                middle = middle+"\nG01 X0.0 Y"+str(r1)+"\nM62\n"
            elif 1 < r1 <= 6:
                er1 = round((0.25*(r1-1)/5) + 0.25,4)
                middle = middle+"\nG00 X-"+str(er1)+" Y"+str(er1)+"\n"
                middle = middle+"\nM61\nG03 X0.0 Y0.0 I"+str(er1)
                middle = middle+"\nG03 J"+str(r1)
                middle = middle+"\nG03 X"+str(er1)+" Y"+str(er1)+" J"+str(er1)+"\nM62\n"
            else:
                middle = middle+"\nG00 X-0.5 Y0.5\n"
                middle = middle+"\nM61\nG03 X0.0 Y0.0 I0.5"
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
            middle = middle+"\nM61\nG03 X"+str(er1)+" Y0.0 J"+str(er1)+""
            middle = middle+"\nG02 I"+str(r1)
            middle = middle+"\nG03 X0.0 Y"+str(er1)+" I-"+str(er1)+"\nM62\n"
        elif direc in ['y','Y']:
            middle = middle+"\nG00 X"+str(er1)+"\n"
            middle = middle+"\nM61\nG03 X0.0 Y"+str(er1)+" I-"+str(er1)
            middle = middle+"\nG02 J"+str(r1)
            middle = middle+"\nG03 X-"+str(er1)+" Y0.0 J-"+str(er1)+"\nM62\n"
    # return the code
    return middle

''' build middle g-code for donut '''
def middleDonut(r1,r2,direc,offs,ent):
    # r1 = outer radius
    # r2 = inner radius
    # d1 = distance between circles
    # outer start at 0
    # offset outer by 0.25 for start, go up to 0.4
    # inner start at 0.5 + d1 + r2 (or 0.5)
    # offset inner start by 0.5 + r2 (or 0.5)
    middle = "G00 X0.0 Y0.0" #(0,0)
    d1 = round(r1-r2+offs,4)
    if ent[0]=='N':
        if direc in ['x','X']:
            middle = middle+"\nG00 X"+str(d1)
            middle = middle+"\nM61\nG03 I"+str(r2)+"\nM62\n" # interior hole CCW
            middle = middle+"\nG00 X0.0 Y0.0"
            middle = middle+"\nM61\nG02 I"+str(r1)+"\nM62\n"
        elif direc in ['y','Y']:
            middle = middle+"\nG00 Y"+str(d1)
            middle = middle+"\nM61\nG03 J"+str(r2)+"\nM62\n" # interior hole CCW
            middle = middle+"\nG00 X0.0 Y0.0"
            middle = middle+"\nM61\nG02 J"+str(r1)+"\nM62\n"
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
                middle = middle+"\nM61\nG01 X"+str(in2)
                middle = middle+"\nG03 I"+str(r2) # interior hole CCW
                middle = middle+"\nG01 X"+str(in1a)+" Y0.0\nM62\n"
            else: # otherwise arc entry for inside and out
                # inner circle
                middle = middle+"\nG00 X"+str(in1b)+" Y"+str(er2)
                middle = middle+"\nM61\nG03 X"+str(in2)+" Y0.0 J-"+str(er2)
                middle = middle+"\nG03 I"+str(r2)
                middle = middle+"\nG03 X"+str(in1b)+" Y-"+str(er2)+" I"+str(er2)+"\nM62\n"
            # outer circle (the same)
            middle = middle+"\nG00 X0.0 Y-"+str(er1)
            middle = middle+"\nM61\nG03 X"+str(er1)+" Y0.0 J"+str(er1)
            middle = middle+"\nG02 I"+str(r1)
            middle = middle+"\nG03 X0.0 Y"+str(er1)+" I-"+str(er1)+"\nM62\n"
        elif direc in ['y','Y']:
            if r2 <= 1:
                # inner circle
                middle = middle+"\nG00 Y"+str(in1a)
                middle = middle+"\nM61\nG01 Y"+str(in2)
                middle = middle+"\nG03 J"+str(r2)
                middle = middle+"\nG01 X0.0 Y"+str(in1a)+"\nM62\n"
            else:
                # inner circle
                middle = middle+"\nG00 X-"+str(er2)+" Y"+str(in1b)
                middle = middle+"\nM61\nG03 X0.0 Y"+str(in2)+" I"+str(er2)
                middle = middle+"\nG03 J"+str(r2)
                middle = middle+"\nG03 X"+str(er2)+" Y"+str(in1b)+" J"+str(er2)+"\nM62\n"
            # outer circle (the same)
            middle = middle+"\nG00 X"+str(er1)+" Y0.0"
            middle = middle+"\nM61\nG03 X0.0 Y"+str(er1)+" I-"+str(er1)
            middle = middle+"\nG02 J"+str(r1)
            middle = middle+"\nG03 X-"+str(er1)+" Y0.0 J-"+str(er1)+"\nM62\n"
    return middle

''' build middle g-code for line '''
def middleLine(leng,direc):
    middle = "G00 X0.0 Y0.0" #(0,0)
    if direc=='x':
        middle = middle+"\nM61\nG01 X"+str(leng)+"\nM62\n"
    elif direc=='y':
        middle = middle+"\nM61\nG01 Y"+str(leng)+"\nM62\n"
    return middle
    
#-------------------------------------------------------------------------------
''' main functions '''
master = tk.Tk()
master.title('Plasma Gcode Maker')
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