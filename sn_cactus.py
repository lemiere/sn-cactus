#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

from tkinter import *
from PIL import Image, ImageTk
import datetime
import configparser




class Mapping(Frame):
    def __init__(self,master):
        Frame.__init__(self, master)
        self.master = master
        self.OM_button = []
        self.main_debug = False
        self.initUI()


    def refresh(self,arg):

        self.half_det_display.destroy()
        self.DisplayHalfDetector(arg)
        
        
    def initUI(self):

        if self.main_debug == True:
            print("INFO : Enter in initUI")

            
        self.snemo_cfg = configparser.ConfigParser()
        self.snemo_cfg.read('conf/snemo.cfg')
        
        self.context = ["main_wall","x_wall","gamma_veto"]

        self.data_path               = self.snemo_cfg.get('FILE_CFG','link_to_path')
        self.nb_of_side              = self.snemo_cfg.get('GEO_CFG','number_of_side')
        self.nb_of_column_per_mw     = self.snemo_cfg.get('GEO_CFG','number_of_column_per_main_wall')
        self.nb_of_row_per_mw        = self.snemo_cfg.get('GEO_CFG','number_of_row_per_main_wall')
        self.nb_of_wall_per_x_wall   = self.snemo_cfg.get('GEO_CFG','number_of_wall_per_x_wall')
        self.nb_of_row_per_x_wall    = self.snemo_cfg.get('GEO_CFG','number_of_row_per_x_wall')
        self.nb_of_col_per_x_wall    = self.snemo_cfg.get('GEO_CFG','number_of_col_per_x_wall')
        self.nb_of_wall_per_g_veto   = self.snemo_cfg.get('GEO_CFG','number_of_wall_per_g_veto')
        self.nb_of_col_per_g_veto    = self.snemo_cfg.get('GEO_CFG','number_of_col_per_g_veto')



        self.master.title("Optical Module Commissionning")

        ######## HEADER FRAME ############
        self.a_header_frame = LabelFrame(self.master,highlightbackground="orange", highlightcolor="orange", highlightthickness=2, bd= 2,text="Header:")
        self.a_header_frame.grid(row=0 ,column=0,columnspan=2)
        #txt = Text()
        user_name = Label(self.a_header_frame, text = "Enter your name : ", justify="center")
        user_name.grid(row=1, column=0)
        self.entry_user_name = Entry(self.a_header_frame,width=5, bg="white")
        self.entry_user_name.grid(row=2, column=0, pady=(5,5))
        
        self.photo = PhotoImage(file ="images/logo.gif")
        logo_position = Canvas(self.a_header_frame, width =100, height =100, bg ='white')
        logo_position.grid(rowspan=2,row=1 ,column=1, padx =0, pady =0)
        logo_position.create_image(50, 50, anchor=CENTER, image=self.photo)
        
        ####### DISPLAY OPTION FRAME ########
        self.a_display_frame=LabelFrame(self.master,highlightbackground="blue", highlightcolor="blue", highlightthickness=2, bd= 2,text="Display option:")
        self.a_display_frame.grid(row=2 ,column=0,columnspan=2)

        self.display_option = IntVar(None, 2)
        display_fiber0_but  = Radiobutton(self.a_display_frame, text="FIBER-0", activebackground="red",variable=self.display_option, value=0, anchor="w")
        display_fiber0_but.grid(row=14, column=0,sticky="w")
        display_fiber1_but  = Radiobutton(self.a_display_frame, text="FIBER-1", activebackground="red",variable=self.display_option, value=1, anchor="w")
        display_fiber1_but.grid(row=14, column=1,sticky="w")
        display_hv_but  = Radiobutton(self.a_display_frame, text="HV", activebackground="red",variable=self.display_option, value=2, anchor="w")
        display_hv_but.grid(row=14, column=2,sticky="w")
        display_signal_but  = Radiobutton(self.a_display_frame, text="SIGNAL", activebackground="red",variable=self.display_option, value=3, anchor="w")
        display_signal_but.grid(row=14, column=3,sticky="w")
        display_leak_but  = Radiobutton(self.a_display_frame, text="LEAK", activebackground="red",variable=self.display_option, value=4, anchor="w")
        display_leak_but.grid(row=14, column=4,sticky="w")

        ####### DETECTOR OPTION FRAME ########
        self.a_detector_frame=LabelFrame(self.master,highlightbackground="white", highlightcolor="white", highlightthickness=2, bd= 2,text="Detector view:")
        self.a_detector_frame.grid(row=3 ,column=0)
        
        for side_nb in range(2):
            side_button = Button(self.a_detector_frame, text='Side-%s' % (side_nb),command=lambda y=side_nb:self.DisplayHalfDetector(int(y)), borderwidth=1).grid(row=10, column=side_nb)

        ######## MGR BUTTON FRAME #######
        self.mgr_frame = LabelFrame(self.master,highlightbackground="black", highlightcolor="black", highlightthickness=2, bd= 2,text="GUI option:")
        self.mgr_frame.grid(row=3,column=1)
        quit_button = Button(self.mgr_frame, text="QUIT", width=10,command=self.master.quit)
        quit_button.grid(row=3, columnspan=2,column=0)
        

    def save_data(self,arg):


        if self.main_debug == True :
            print("INFO : save_data : Enter in function save_data()")
            print("INFO : File modified by : %s"%self.entry_user_name.get())

        the_date = datetime.datetime.now()
        main_comment_l0="# Modified by : "+self.entry_user_name.get()
        main_comment_l1="# Last change : "+str(the_date)
        
        debug = True
        if debug == True:
            print("Param to save for OM : %s"%arg)
            print("    |-> fiber0 state  : %s "%self.fiber0_state.get())
            if self.check0.get() == 1:
                print("    `-> DEFINED")
            else:
                print("    `-> UNDEFINED")
            print("    |-> fiber1 state  : %s "%self.fiber1_state.get())
            if self.check1.get() == 1:
                print("    `-> DEFINED")
            else:
                print("    `-> UNDEFINED")
            print("    |-> hv state      : %s "%self.hv_state.get())
            if self.check_hv.get() == 1:
                print("    `-> DEFINED")
            else:
                print("    `-> UNDEFINED")
            print("    |-> signal state  : %s "%self.signal_state.get())
            if self.check_signal.get() == 1:
                print("    `-> DEFINED")
            else:
                print("    `-> UNDEFINED")
            print("    `-> leak state  : %s "%self.leak_state.get())
            if self.check_leak.get() == 1:
                print("    `-> DEFINED")
            else:
                print("    `-> UNDEFINED")

        
        new_word=arg.split(" ")
        om_type = new_word[0]
        side=new_word[2].split("_")[0]
        l1=new_word[2].split("_")[1]
        l2=new_word[2].split("_")[2]
        pref_filename = "OM_"+str(side)+"."+str(l1)+"."+str(l2)
        
        if om_type == "GV":
            om = "gamma_veto"
            full_om_path  = self.snemo_cfg.get('FILE_CFG','link_to_path')+"/"+om+"/"+"side"+str(side)+"/"+"wall"+str(l1)+"/"+"row"+str(l2)
        elif om_type == "MW":
            om = "main_wall"
            full_om_path  = self.snemo_cfg.get('FILE_CFG','link_to_path')+"/"+om+"/"+"side"+str(side)+"/"+"column"+str(l1)+"/"+"row"+str(l2)
        else:
            om = "x_wall"
            l3=new_word[2].split("_")[3]
            full_om_path  = self.snemo_cfg.get('FILE_CFG','link_to_path')+"/"+om+"/"+"side"+str(side)+"/"+"wall"+str(l1)+"/"+"column"+str(l2)+"/"+"row"+str(l3)
            pref_filename = "OM_"+str(side)+"."+str(l1)+"."+str(l2)+"."+str(l3)
        
        om_cfg = configparser.ConfigParser()
        om_cfg.read(full_om_path+"/"+pref_filename+"_fiber.log")
        tmp_file = open(full_om_path+"/"+pref_filename+"_fiber.log","w")

        om_cfg.set('STATUS','fiber0_CHECK',str(self.check0.get()))
        om_cfg.set('STATUS','fiber1_CHECK',str(self.check1.get()))
        om_cfg.set('COMMENT','fiber0_comment',str(self.the_comment0.get()))
        om_cfg.set('COMMENT','fiber1_comment',str(self.the_comment1.get()))

        if self.check0.get() == 1 and self.fiber0_state.get() == 0:
            om_cfg.set('STATUS','fiber0_ok','1')
            om_cfg.set('STATUS','fiber0_bad','0')
            om_cfg.set('STATUS','fiber0_hs','0')
        elif self.check0.get() == 1 and self.fiber0_state.get() == 1:
            om_cfg.set('STATUS','fiber0_bad','1')
            om_cfg.set('STATUS','fiber0_hs','0')
            om_cfg.set('STATUS','fiber0_ok','0')
        elif self.check0.get() == 1 and self.fiber0_state.get() == 2:
            om_cfg.set('STATUS','fiber0_hs','1')
            om_cfg.set('STATUS','fiber0_bad','0')
            om_cfg.set('STATUS','fiber0_ok','0')
        else :
            print("WARNING : fiber#0 :  Nothing to change...")
        
        if self.check1.get() and self.fiber1_state.get() == 0:
            om_cfg.set('STATUS','fiber1_ok','1')
            om_cfg.set('STATUS','fiber1_bad','0')
            om_cfg.set('STATUS','fiber1_hs','0')
        elif self.check1.get() and self.fiber1_state.get() == 1:
            om_cfg.set('STATUS','fiber1_bad','1')
            om_cfg.set('STATUS','fiber1_ok','0')
            om_cfg.set('STATUS','fiber1_hs','0')
        elif self.check1.get() and self.fiber1_state.get() == 2:
            om_cfg.set('STATUS','fiber1_hs','1')
            om_cfg.set('STATUS','fiber1_ok','0')
            om_cfg.set('STATUS','fiber1_bad','0')
        else :
            print("WARNING : fiber#1 : Nothing to change...")

        
        tmp_file.write("%s \n"%main_comment_l0)
        tmp_file.write("%s \n"%main_comment_l1)
            
        om_cfg.write(tmp_file)
        tmp_file.close()

        hv_cfg = configparser.ConfigParser()
        hv_cfg.read(full_om_path+"/"+pref_filename+"_HV.log")
        tmp_file = open(full_om_path+"/"+pref_filename+"_HV.log","w")
        
        hv_cfg.set('STATUS','HV_CHECK',str(self.check_hv.get()))
        hv_cfg.set('COMMENT','HV_comment',str(self.the_hv_comment.get()))

        
        if self.check_hv.get() and self.hv_state.get() == 0:
            hv_cfg.set('STATUS','hv_ok','1')
            hv_cfg.set('STATUS','hv_bad','0')
            hv_cfg.set('STATUS','hv_hs','0')
        elif self.check_hv.get() and self.hv_state.get() == 1:
            hv_cfg.set('STATUS','hv_bad','1')
            hv_cfg.set('STATUS','hv_hs','0')
            hv_cfg.set('STATUS','hv_ok','0')
        elif self.check_hv.get() and self.fiber0_state.get() == 2:
            hv_cfg.set('STATUS','hv_hs','1')
            hv_cfg.set('STATUS','hv_bad','0')
            hv_cfg.set('STATUS','hv_ok','0')
        else :
            print("WARNING : hv : Nothing to change...")

        tmp_file.write("%s \n"%main_comment_l0)
        tmp_file.write("%s \n"%main_comment_l1)
            
        hv_cfg.write(tmp_file)
        tmp_file.close()


        leak_cfg = configparser.ConfigParser()
        leak_cfg.read(full_om_path+"/"+pref_filename+"_leak.log")
        tmp_file = open(full_om_path+"/"+pref_filename+"_leak.log","w")
        
        leak_cfg.set('STATUS','leak_CHECK',str(self.check_leak.get()))
        leak_cfg.set('COMMENT','leak_comment',str(self.the_leak_comment.get()))

        
        if self.check_leak.get() and self.leak_state.get() == 0:
            leak_cfg.set('STATUS','leak_ok','1')
            leak_cfg.set('STATUS','leak_bad','0')
            leak_cfg.set('STATUS','leak_hs','0')
        elif self.check_leak.get() and self.leak_state.get() == 1:
            leak_cfg.set('STATUS','leak_bad','1')
            leak_cfg.set('STATUS','leak_hs','0')
            leak_cfg.set('STATUS','leak_ok','0')
        elif self.check_leak.get() and self.leak_state.get() == 2:
            leak_cfg.set('STATUS','leak_hs','1')
            leak_cfg.set('STATUS','leak_bad','0')
            leak_cfg.set('STATUS','leak_ok','0')
        else :
            print("WARNING : leak : Nothing to change...")

        tmp_file.write("%s \n"%main_comment_l0)
        tmp_file.write("%s \n"%main_comment_l1)
            
            
        leak_cfg.write(tmp_file)
        tmp_file.close()
        
        
        signal_cfg = configparser.ConfigParser()
        signal_cfg.read(full_om_path+"/"+pref_filename+"_signal.log")
        tmp_file = open(full_om_path+"/"+pref_filename+"_signal.log","w")
        
        signal_cfg.set('STATUS','signal_CHECK',str(self.check_signal.get()))
        signal_cfg.set('COMMENT','signal_comment',str(self.the_signal_comment.get()))

        
        if self.check_signal.get() and self.signal_state.get() == 0:
            signal_cfg.set('STATUS','signal_ok','1')
            signal_cfg.set('STATUS','signal_bad','0')
            signal_cfg.set('STATUS','signal_hs','0')
        elif self.check_signal.get() and self.signal_state.get() == 1:
            signal_cfg.set('STATUS','signal_bad','1')
            signal_cfg.set('STATUS','signal_hs','0')
            signal_cfg.set('STATUS','signal_ok','0')
        elif self.check_signal.get() and self.signal_state.get() == 2:
            signal_cfg.set('STATUS','signal_hs','1')
            signal_cfg.set('STATUS','signal_bad','0')
            signal_cfg.set('STATUS','signal_ok','0')
        else :
            print("WARNING : signal : Nothing to change...")

        tmp_file.write("%s \n"%main_comment_l0)
        tmp_file.write("%s \n"%main_comment_l1)
            
            
        signal_cfg.write(tmp_file)
        tmp_file.close()

        
                
    def DisplayOM(self,arg0):

        if self.main_debug == True:
            print("INFO : DisplayOM : Enter in DisplayOM")

        
        debug = True
        new_word=arg0.split(" ")
        OM_type = new_word[0]
        Display_option = new_word[1]


        if OM_type == 'MW':
            side = new_word[2].split("_")[0]
            l1_  = new_word[2].split("_")[1]
            l2_  = new_word[2].split("_")[2]
            l3_  = "NULL"
        elif OM_type == 'XW':
            side = new_word[2].split("_")[0]
            l1_  = new_word[2].split("_")[1]
            l2_  = new_word[2].split("_")[2]
            l3_  = new_word[2].split("_")[3]
        elif OM_type == 'GV':
            side = new_word[2].split("_")[0]
            l1_  = new_word[2].split("_")[1]
            l2_  = new_word[2].split("_")[2]
            l3_  = "NULL"
        else:
            print("\033[91mERROR\033[00m : Can not parse file using %s  "%(OM_type))
            sys.exit(1)

        topic = "fiber0"
        check_f0, ok_f0, bad_f0, hs_f0, comment_f0 = self.get_data_from_file(side,l1_,l2_,l3_,OM_type,topic)
        topic = "fiber1"
        check_f1, ok_f1, bad_f1, hs_f1, comment_f1 = self.get_data_from_file(side,l1_,l2_,l3_,OM_type,topic)
        topic = "HV"
        check_HV, ok_HV, bad_HV, hs_HV, comment_HV = self.get_data_from_file(side,l1_,l2_,l3_,OM_type,topic)
        topic = "leak"
        check_leak, ok_leak, bad_leak, hs_leak, comment_leak = self.get_data_from_file(side,l1_,l2_,l3_,OM_type,topic)
        topic = "signal"
        check_the_signal, ok_signal, bad_signal, hs_signal, comment_signal = self.get_data_from_file(side,l1_,l2_,l3_,OM_type,topic)
        if self.main_debug == True:
            print("INFO : DisplayOM : OM Type : %s"%(OM_type))
            #print("INFO : DisplayOM : Option  : %s"%(Display_option))
            print("INFO : DisplayOM : Arguments (side l1 l2 l3)   : %s %s %s %s"%(side,l1_,l2_,l3_))
            print("fiber #0 : ")
            print("   |-> check : %s"%check_f0)
            print("   |-> ok    : %s"%ok_f0)
            print("   |-> bad   : %s"%bad_f0)
            print("   |-> hs    : %s"%hs_f0)
            print("   `->com    : %s"%comment_f0)
            print("fiber #1 : ")
            print("   |-> check : %s"%check_f1)
            print("   |-> ok    : %s"%ok_f1)
            print("   |-> bad   : %s"%bad_f1)
            print("   |-> hs    : %s"%hs_f1)
            print("   `-> com   : %s"%comment_f1)
            print("HighVoltage : ")
            print("   |-> check : %s"%check_HV)
            print("   |-> ok    : %s"%ok_HV)
            print("   |-> bad   : %s"%bad_HV)
            print("   |-> hs    : %s"%hs_HV)
            print("   `-> com   : %s"%comment_HV)
            print("leak")
            print("   |-> check : %s"%check_leak)
            print("   |-> ok    : %s"%ok_leak)
            print("   |-> bad   : %s"%bad_leak)
            print("   |-> hs    : %s"%hs_leak)
            print("   `-> com   : %s"%comment_leak)
            print("signal")
            print("   |-> check : %s"%check_the_signal)
            print("   |-> ok    : %s"%ok_signal)
            print("   |-> bad   : %s"%bad_signal)
            print("   |-> hs    : %s"%hs_signal)
            print("   `-> com   : %s"%comment_signal)

            
            
        OM_root = Tk()
        if OM_type == 'XW':
            OM_root.title("OM:%s.%s.%s.%s"%(side,l1_,l2_,l3_))
        else:
            OM_root.title("OM:%s.%s.%s"%(side,l1_,l2_))

            
        a_fiber0_frame=LabelFrame(OM_root,highlightbackground="blue", highlightcolor="blue", highlightthickness=2, width=100, height=100, bd= 2,text="Fiber #0:")
        a_fiber0_frame.grid(row=0,column=0)
        
        #### Fiber 0
        self.check0 = IntVar(OM_root,check_f0)

        check0_text = Label(a_fiber0_frame, text = "checked : ", justify="center")
        check0_text.grid(row=0, column=0, padx=(15,0))
        entry0_check = Checkbutton(a_fiber0_frame, variable=self.check0)
        entry0_check.grid(row=0, column=1, padx=(5,10))

        if ok_f0 == "1" and bad_f0 == "0" and hs_f0 == "0":
            self.fiber0_state = IntVar(OM_root, 0)
        elif ok_f0 == "0" and bad_f0 == "1" and hs_f0 == "0":
            self.fiber0_state = IntVar(OM_root,1)
        elif ok_f0 == "0" and bad_f0 == "0" and hs_f0 == "1":
            self.fiber0_state = IntVar(OM_root,2)
        elif ok_f0 == "0" and bad_f0 == "0" and hs_f0 == "0":
            self.fiber0_state = IntVar(OM_root,666)
        else:
            print("ERROR : Wrong fiber#0 status from file...")
            sys.exit(1)
            
        state0 =  Label(a_fiber0_frame, text="Fiber 0 status :",justify = LEFT, padx = 20)
        state0.grid(row=1, column=0,sticky="w")
        state0_ok_but  = Radiobutton(a_fiber0_frame, text="GOOD", activebackground="red",variable=self.fiber0_state, value=0, anchor="w")
        state0_ok_but.grid(row=1, column=4,sticky="w")
        state0_hs_but  = Radiobutton(a_fiber0_frame, text="HS",  activebackground="red",variable=self.fiber0_state, value=2, anchor="w")
        state0_hs_but.grid(row=2, column=4,sticky="w")
        state0_bad_but = Radiobutton(a_fiber0_frame, text="BAD",  activebackground="red",variable=self.fiber0_state, value=1, anchor="w")
        state0_bad_but.grid(row=3, column=4,sticky="w")
        comment0_label = Label(a_fiber0_frame, text="COMMENT", width=7)
        comment0_label.grid(row=4, column=0,columnspan=2,sticky="w")
        self.the_comment0 = Entry(a_fiber0_frame,bg='white')
        self.the_comment0.grid(row=5, column=0,columnspan=2,sticky="w")


        ## Fiber 1
        a_fiber1_frame=LabelFrame(OM_root,highlightbackground="green", highlightcolor="green", highlightthickness=2, width=100, height=100, bd= 2,text="Fiber #1:",relief="groove")
        a_fiber1_frame.grid(row=1,column=0)
    
        self.check1 = IntVar(OM_root,check_f1)

        check1_text = Label(a_fiber1_frame, text = "checked", justify="center")
        check1_text.grid(row=0, column=0, padx=(15,0))
        entry1_check = Checkbutton(a_fiber1_frame, variable=self.check1)
        entry1_check.grid(row=0, column=1, padx=(5,10))
        

        if ok_f1 == "1" and bad_f1 == "0" and hs_f1 == "0":
            self.fiber1_state = IntVar(OM_root, 0)
        elif ok_f1 == "0" and bad_f1 == "1" and hs_f1 == "0":
            self.fiber1_state = IntVar(OM_root,1)
        elif ok_f1 == "0" and bad_f1 == "0" and hs_f1 == "1":
            self.fiber1_state = IntVar(OM_root,2)
        elif ok_f1 == "0" and bad_f1 == "0" and hs_f1 == "0":
            self.fiber1_state = IntVar(OM_root,666)
        else:
            print("ERROR : Wrong fiber#0 status from file...")
            sys.exit(1)

        state1 =  Label(a_fiber1_frame, text="Fiber 1 status :",justify = LEFT, padx = 20)
        state1.grid(row=1, column=0,sticky="w")
        state1_ok_but  = Radiobutton(a_fiber1_frame, text="GOOD", activebackground="red",variable=self.fiber1_state, value=0, anchor="w")
        state1_ok_but.grid(row=1, column=4,sticky="w")
        state1_hs_but  = Radiobutton(a_fiber1_frame, text="HS",  activebackground="red",variable=self.fiber1_state, value=2, anchor="w")
        state1_hs_but.grid(row=2, column=4,sticky="w")
        state1_bad_but = Radiobutton(a_fiber1_frame, text="BAD",  activebackground="red",variable=self.fiber1_state, value=1, anchor="w")
        state1_bad_but.grid(row=3, column=4,sticky="w")
        comment1_label = Label(a_fiber1_frame, text="COMMENT : ", width=7)
        comment1_label.grid(row=4, column=0,columnspan=2,sticky="w")
        self.the_comment1 = Entry(a_fiber1_frame,bg='white')
        self.the_comment1.grid(row=5, column=0,columnspan=2,sticky="w")

        ########################## end of fiber 1
        
        
        ## HV
        a_hv_frame=LabelFrame(OM_root,highlightbackground="red", highlightcolor="red", highlightthickness=2, width=100, height=100, bd= 2,text="HighVoltage :",relief="ridge")
        a_hv_frame.grid(row=0,column=1)
        
        self.check_hv = IntVar(OM_root,check_HV)

        check_hv_text = Label(a_hv_frame, text = "checked", justify="center")
        check_hv_text.grid(row=0, column=0, padx=(15,0))
        entry_hv_check = Checkbutton(a_hv_frame, variable=self.check_hv)
        entry_hv_check.grid(row=0, column=1, padx=(5,10))
        

        if ok_HV == "1" and bad_HV == "0" and hs_HV == "0":
            self.hv_state = IntVar(OM_root, 0)
        elif ok_HV == "0" and bad_HV == "1" and hs_HV == "0":
            self.hv_state = IntVar(OM_root,1)
        elif ok_HV == "0" and bad_HV == "0" and hs_HV == "1":
            self.hv_state = IntVar(OM_root,2)
        elif ok_HV == "0" and bad_HV == "0" and hs_HV == "0":
            self.hv_state = IntVar(OM_root,666)
        else:
            print("ERROR : Wrong HV status from file...")
            sys.exit(1)
                        
        hv =  Label(a_hv_frame, text="HV status :",justify = LEFT, padx = 20)
        hv.grid(row=1, column=0,sticky="w")
        hv_ok_but  = Radiobutton(a_hv_frame, text="GOOD", activebackground="red",variable=self.hv_state, value=0, anchor="w")
        hv_ok_but.grid(row=1, column=4,sticky="w")
        hv_hs_but  = Radiobutton(a_hv_frame, text="HS",  activebackground="red",variable=self.hv_state, value=2, anchor="w")
        hv_hs_but.grid(row=2, column=4,sticky="w")
        hv_bad_but = Radiobutton(a_hv_frame, text="BAD",  activebackground="red",variable=self.hv_state, value=1, anchor="w")
        hv_bad_but.grid(row=3, column=4,sticky="w")
        hv_comment_label = Label(a_hv_frame, text="COMMENT", width=7)
        hv_comment_label.grid(row=4, column=0,columnspan=2,sticky="w")
        self.the_hv_comment = Entry(a_hv_frame,bg='white')
        self.the_hv_comment.grid(row=5, column=0,columnspan=2,sticky="w")
    
        ########################## end of hv
        
        ## SIGNAL
        a_signal_frame=LabelFrame(OM_root,highlightbackground="orange", highlightcolor="orange", highlightthickness=2, width=100, height=100,text="Signal :",relief="groove")
        a_signal_frame.grid(row=1,column=1)
    
        self.check_signal = IntVar(OM_root,check_the_signal)

        check_signal_text = Label(a_signal_frame, text = "checked", justify="center")
        check_signal_text.grid(row=0, column=0, padx=(15,0))
        entry_signal_check = Checkbutton(a_signal_frame, variable=self.check_signal)
        entry_signal_check.grid(row=0, column=1, padx=(5,10))
        

        if ok_signal == "1" and bad_signal == "0" and hs_signal == "0":
            self.signal_state = IntVar(OM_root, 0)
        elif ok_signal == "0" and bad_signal == "1" and hs_signal == "0":
            self.signal_state = IntVar(OM_root,1)
        elif ok_signal == "0" and bad_signal == "0" and hs_signal == "1":
            self.signal_state = IntVar(OM_root,2)
        elif ok_signal == "0" and bad_signal == "0" and hs_signal == "0":
            self.signal_state = IntVar(OM_root,666)
        else:
            print("ERROR : Wrong signal status from file...")
            sys.exit(1)

        signal =  Label(a_signal_frame, text="SIGNAL status :",justify = LEFT, padx = 20)
        signal.grid(row=1, column=0,sticky="w")
        signal_ok_but  = Radiobutton(a_signal_frame, text="GOOD", activebackground="red",variable=self.signal_state, value=0, anchor="w")
        signal_ok_but.grid(row=1, column=4,sticky="w")
        signal_hs_but  = Radiobutton(a_signal_frame, text="HS",  activebackground="red",variable=self.signal_state, value=2, anchor="w")
        signal_hs_but.grid(row=2, column=4,sticky="w")
        signal_bad_but = Radiobutton(a_signal_frame, text="BAD",  activebackground="red",variable=self.signal_state, value=1, anchor="w")
        signal_bad_but.grid(row=3, column=4,sticky="w")
        signal_comment_label = Label(a_signal_frame, text="COMMENT", width=7)
        signal_comment_label.grid(row=4, column=0,columnspan=2,sticky="w")
        self.the_signal_comment = Entry(a_signal_frame,bg='white')
        self.the_signal_comment.grid(row=5, column=0,columnspan=2,sticky="w")
        
        ########################## end of signal
        
        ## LEAK
        a_leak_frame=LabelFrame(OM_root,highlightbackground="black", highlightcolor="black", highlightthickness=2, width=100, height=100,text="Leak :",relief="groove")
        a_leak_frame.grid(row=2,column=0)
    
        self.check_leak = IntVar(OM_root,check_leak)

        check_leak_text = Label(a_leak_frame, text = "checked", justify="center")
        check_leak_text.grid(row=0, column=0, padx=(15,0))
        entry_leak_check = Checkbutton(a_leak_frame, variable=self.check_leak)
        entry_leak_check.grid(row=0, column=1, padx=(5,10))
    

        if ok_leak == "1" and bad_leak == "0" and hs_leak == "0":
            self.leak_state = IntVar(OM_root, 0)
        elif ok_leak == "0" and bad_leak == "1" and hs_leak == "0":
            self.leak_state = IntVar(OM_root,1)
        elif ok_leak == "0" and bad_leak == "0" and hs_leak == "1":
            self.leak_state = IntVar(OM_root,2)
        elif ok_leak == "0" and bad_leak == "0" and hs_leak == "0":
            self.leak_state = IntVar(OM_root,666)
        else:
            print("ERROR : Wrong leak status from file...")
            sys.exit(1)

        
        leak =  Label(a_leak_frame, text="LEAK status :",justify = LEFT, padx = 20)
        leak.grid(row=1, column=0,sticky="w")
        leak_ok_but  = Radiobutton(a_leak_frame, text="GOOD", activebackground="red",variable=self.leak_state, value=0, anchor="w")
        leak_ok_but.grid(row=1, column=4,sticky="w")
        leak_hs_but  = Radiobutton(a_leak_frame, text="HS",  activebackground="red",variable=self.leak_state, value=2, anchor="w")
        leak_hs_but.grid(row=2, column=4,sticky="w")
        leak_bad_but = Radiobutton(a_leak_frame, text="BAD",  activebackground="red",variable=self.leak_state, value=1, anchor="w")
        leak_bad_but.grid(row=3, column=4,sticky="w")
        leak_comment_label = Label(a_leak_frame, text="COMMENT", width=7)
        leak_comment_label.grid(row=4, column=0,columnspan=2,sticky="w")
        self.the_leak_comment = Entry(a_leak_frame,bg='white')
        self.the_leak_comment.grid(row=5, column=0,columnspan=2,sticky="w")
    
        ########################## end of leak
        
        
        om_id=arg0
       
        #    destroy_button = Button(another_root, text="SAVE&CLOSE", width=10,command=another_root.destroy)
        save_button = Button(OM_root, text="SAVE", width=10,command= lambda x=om_id:self.save_data(str(x)))
        save_button.grid(row=3,column=0)

        close_button = Button(OM_root, text="CLOSE", width=10,command=OM_root.destroy)
        close_button.grid(row=3,column=1)
        

        

        

    def get_data_from_file(self,side,l2,l3,l4,OM_type,topic):

        if self.main_debug == True:
            print("INFO : get_data_from_file : enter in get_data_from_file()")

        debug = False
        
        if topic == 'fiber0' or topic == 'fiber1' :
            suff_filename = "_fiber.log"
        elif topic == 'HV':
            suff_filename = "_HV.log"
        elif topic == 'signal':
            suff_filename = "_signal.log"
        elif topic == 'leak':
            suff_filename = "_leak.log"
        else:
            print("ERROR : get_status() : unknown topic...")
            sys.exit(1)

            #status_arg = topic+"_"+value.upper()  
        # Get config path and data path per OM
        if OM_type == "MW":
            full_om_path=self.snemo_cfg.get('FILE_CFG','link_to_path')+"/"+"main_wall"+"/"+"side"+str(side)+"/"+"column"+str(l2)+"/"+"row"+str(l3)
            om_filename="OM_"+str(side)+"."+str(l2)+"."+str(l3)+suff_filename
        elif OM_type == 'XW':
            full_om_path=self.snemo_cfg.get('FILE_CFG','link_to_path')+"/"+"x_wall"+"/"+"side"+str(side)+"/"+"wall"+str(l2)+"/"+"column"+str(l3)+"/"+"row"+str(l4)
            om_filename="OM_"+str(side)+"."+str(l2)+"."+str(l3)+"."+str(l4)+suff_filename
        elif OM_type == 'GV':
            full_om_path=self.snemo_cfg.get('FILE_CFG','link_to_path')+"/"+"gamma_veto"+"/"+"side"+str(side)+"/"+"wall"+str(l2)+"/"+"row"+str(l3)
            om_filename="OM_"+str(side)+"."+str(l2)+"."+str(l3)+suff_filename
        else:
            print("\033[91mERROR\033[00m : Can not parse file using %s  "%(OM_type))
            sys.exit(1)
        

        #om_file = open(full_om_path+"/"+om_filename,'r')
        om_cfg = configparser.ConfigParser()
        om_cfg.read(full_om_path+"/"+om_filename)

        if debug == True :
            print(full_om_path+"/"+om_filename)
            print(om_cfg.get('COMMENT',topic+"_comment"))
            print(om_cfg.get('STATUS',topic+"_BAD"))
        
        om_status_check = om_cfg.get('STATUS',topic+"_CHECK")
        om_comment      = om_cfg.get('COMMENT',topic+"_comment")
        om_ok           = om_cfg.get('STATUS',topic+"_OK")
        om_bad          = om_cfg.get('STATUS',topic+"_BAD")
        om_hs           = om_cfg.get('STATUS',topic+"_HS")
        if om_ok == '1' and om_bad == '1' and om_hs == '1':
            print("\033[91mERROR\033[00m : Get status from file : error in file ok/bad/hs can not be activated in a same time!")
            sys.exit(1)
        return om_status_check, om_ok, om_bad, om_hs,om_comment 
            
        
    def get_status(self,side,wall,col,row,OM_type,topic,value):
        
        debug = False
        status = False
        
        if topic == 'fiber0' or topic == 'fiber1' :
            suff_filename = "_fiber.log"
        elif topic == 'HV':
            suff_filename = "_HV.log"
        elif topic == 'signal':
            suff_filename = "_signal.log"
        elif topic == 'leak':
            suff_filename = "_leak.log"
        else:
            print("ERROR : get_status() : unknown topic...")
            sys.exit(1)

        status_arg = topic+"_"+value.upper()  
    

        
        # Get config path and data path per OM
        if OM_type == "MW":
            full_om_path=self.snemo_cfg.get('FILE_CFG','link_to_path')+"/"+"main_wall"+"/"+"side"+str(side)+"/"+"column"+str(wall)+"/"+"row"+str(col)
            om_filename="OM_"+str(side)+"."+str(wall)+"."+str(col)+suff_filename
        elif OM_type == 'XW':
            full_om_path=self.snemo_cfg.get('FILE_CFG','link_to_path')+"/"+"x_wall"+"/"+"side"+str(side)+"/"+"wall"+str(wall)+"/"+"column"+str(col)+"/"+"row"+str(row)
            om_filename="OM_"+str(side)+"."+str(wall)+"."+str(col)+"."+str(row)+suff_filename
        elif OM_type == 'GV':
            full_om_path=self.snemo_cfg.get('FILE_CFG','link_to_path')+"/"+"gamma_veto"+"/"+"side"+str(side)+"/"+"wall"+str(wall)+"/"+"row"+str(col)
            om_filename="OM_"+str(side)+"."+str(wall)+"."+str(col)+suff_filename
        else:
            print("\033[91mERROR\033[00m : Can not parse file using %s  "%(OM_type))
            sys.exit(1)
        
        

        om_file = open(full_om_path+"/"+om_filename,'r')
        om_cfg = configparser.ConfigParser()
        om_cfg.read(full_om_path+"/"+om_filename)
        ################
        
        good = False
        
        test_om_id=om_cfg.get('OM_ID','id')
        test_om_status_check_0=om_cfg.get('STATUS',status_arg)
        test_om_comment_0=om_cfg.get('COMMENT',topic+"_comment")
        
        
        if debug:
            print("om id from fiber_log : %s"%test_om_id)
            print("--> wanted status    : %s"%status_arg)
            print("--> value            : %s"%om_cfg.get('STATUS',status_arg))
            print("Comment              : %s"%test_om_comment_0)

        if om_cfg.get('STATUS',status_arg) == "1":
            status = True
        elif om_cfg.get('STATUS',status_arg) == "0":
            status = False
        else:
            print("ERROR : Get_status() : Unknow status...")
            sys.exit(1)
            
            
            #print(status)
        return status



    
    def DisplayHalfDetector(self,arg0):

        
        
        if self.main_debug == True:
            print("INFO : DisplayHalfDetector : Enter in DisplayHalfDetector")
           

        side = arg0
        OM_type = None

        self.half_det_display = Tk() 
        
        self.half_det_display.rowconfigure(0, weight=1)
        self.half_det_display.columnconfigure(0, weight=1)


        
        label = Label(self.half_det_display, text = "Please, select an Optical Module ") 
        label.grid(row = 0, column = 0, columnspan = 3) 


        topic_option = 'fiber0'
        
        if self.display_option.get() == 0:
            topic_option = 'fiber0'
        elif self.display_option.get() == 1:
            topic_option = 'fiber1'
        elif self.display_option.get() == 2:
            topic_option = 'HV'
        elif self.display_option.get() == 3:
            topic_option = 'signal'
        elif self.display_option.get() == 4:
            topic_option = 'leak'
        else:
            print("ERROR : DisplayHalfDetector() : Unknown display option")
            sys.exit(1)
            
        self.half_det_display.title("Demonstrator Side #%s -- Display : %s"%(side,topic_option))
    
        if self.main_debug == True:
            print("INFO : DisplayHalfDetector : display %s"%topic_option)    
        
    
        a_list = []
        button_list = []
        ## TOP GVETO ##
        self.a_top_gveto_frame = LabelFrame(self.half_det_display,highlightbackground="blue", highlightcolor="blue", highlightthickness=2, width=100, height=100, bd= 2,text="-- Top GVETO --")
        self.a_top_gveto_frame.grid(row=1,column=0,columnspan=3)
        
        OM_type = "GV"
        wall = 1
        row  = None
        for col in range(int(self.nb_of_col_per_g_veto)):
            it=col
            #        print(it)
            a_list = []
            #a_list[row,col]
            #a_list.insert(1,row)
            a_list.insert(1,col)
            toto=str(side)+"_"+str(wall)+"_"+str(col)
            #print("Argument for TOP GVETO : %s"%toto)
            current_om_checked = self.get_status(side,wall,col,row,OM_type,topic_option,'check')
            if current_om_checked == False:
                color='grey'
            else:
                om_current_status = self.get_status(side,wall,col,row,OM_type,topic_option,'bad')
                om_hs             = self.get_status(side,wall,col,row,OM_type,topic_option,'hs')
                if om_hs == True:
                    color='black'
                elif om_current_status == True:
                    color='red'
                else:
                    color='green'
                        
                        
            button_list.append(Button(self.a_top_gveto_frame, text = "%s.%s.%s"%(side,wall,col), command = lambda x=toto:self.DisplayOM("GV selected "+str(x))) )
            button_list[it].config(width="4")
            button_list[it].config(bg=color)
            button_list[it].grid(row=0,column=col)






        button_list = []
        ## FIRST XWALL ##
        self.a_first_xwall_frame = LabelFrame(self.half_det_display,highlightthickness=2, width=100, height=100, bd= 2,text="First XWALL")
        self.a_first_xwall_frame.grid(row=2,column=0)
        OM_type = "XW"
        wall = "0"
        
        for row in range(int(self.nb_of_row_per_x_wall)):
            for col in range (int(self.nb_of_col_per_x_wall)):
                it=(row*int(self.nb_of_col_per_x_wall))+col
                #        print(it)
                a_list = []
                #a_list[row,col]
                a_list.insert(1,row)
                a_list.insert(2,col)
                toto=str(side)+"_"+str(col)+"_"+str(row)
                toto_bis=str(side)+"_"+str(wall)+"_"+str(col)+"_"+str(row)
                
                #if debug:
                #    print("Argument for XW : %s"%toto_bis)
                    
                    
                current_om_checked = self.get_status(side,wall,col,row,OM_type,topic_option,'check')
                    
                if current_om_checked == False:
                    color='grey'
                else:
                    om_current_status = self.get_status(side,wall,col,row,OM_type,topic_option,'bad')
                    om_hs             = self.get_status(side,wall,col,row,OM_type,topic_option,'hs')
                    if om_hs == True:
                        color='black'
                    elif om_current_status == True:
                        color='red'
                    else:
                        color='green'
                        
                        
                button_list.append(Button(self.a_first_xwall_frame, text = "%s.%s.%s.%s"%(side,wall,col,row), command = lambda x=toto_bis:self.DisplayOM("XW selected "+str(x))) )
                button_list[it].config(width="3")
                button_list[it].config(bg=color)
                button_list[it].grid(row=(int(self.nb_of_row_per_x_wall)-row),column=col)



        button_list = []
        ## MAIN WALL ##
        self.a_mainwall_frame = LabelFrame(self.half_det_display,highlightbackground="blue", highlightcolor="blue", highlightthickness=2, width=100, height=100, bd= 2,text="-- Main Wall --")
        self.a_mainwall_frame.grid(row=2,column=1)
        OM_type = "MW"
        wall = None
        for row in range(int(self.nb_of_row_per_mw)):
            for col in range (int(self.nb_of_column_per_mw)):
                it=(row*int(self.nb_of_column_per_mw))+col
                #        print(it)
                a_list = []
                #a_list[row,col]
                a_list.insert(1,row)
                a_list.insert(2,col)
                toto=str(side)+"_"+str(col)+"_"+str(row)
                
                #if debug:
                #    print("Argument for MW : %s"%toto)
                
                
                current_om_checked = self.get_status(side,col,row,wall,OM_type,topic_option,'check')
                
                if current_om_checked == False:
                    color='grey'
                else:
                    om_current_status = self.get_status(side,col,row,wall,OM_type,topic_option,'bad')
                    om_hs             = self.get_status(side,col,row,wall,OM_type,topic_option,'hs')
                    if om_hs == True:
                        color='black'
                    elif om_current_status == True:
                        color='red'
                    else:
                        color='green'
                        
        
                button_list.append(Button(self.a_mainwall_frame, text = "%s.%s.%s"%(side,col,row), command = lambda x=toto:self.DisplayOM("MW selected "+str(x))) )
                button_list[it].config(width="3")
                button_list[it].config(bg=color)
                button_list[it].grid(row=(int(self.nb_of_row_per_mw)-row),column=col)

        button_list = []
        ## SECOND XWALL ##
        self.a_second_xwall_frame = LabelFrame(self.half_det_display, highlightthickness=2, width=100, height=100, bd= 2,text="Second XWALL")
        self.a_second_xwall_frame.grid(row=2,column=2)
        OM_type = "XW"
        wall = "1"
        
        for row in range(int(self.nb_of_row_per_x_wall)):
            for col in range (int(self.nb_of_col_per_x_wall)):
                it=(row*int(self.nb_of_col_per_x_wall))+col
                #        print(it)
                a_list = []
                #a_list[row,col]
                a_list.insert(1,row)
                a_list.insert(2,col)
                toto=str(side)+"_"+str(col)+"_"+str(row)
                toto_bis=str(side)+"_"+str(wall)+"_"+str(col)+"_"+str(row)
                
                #if debug:
                #    print("Argument for XW : %s"%toto_bis)
                
                current_om_checked = self.get_status(side,wall,col,row,OM_type,topic_option,'check')
                
                if current_om_checked == False:
                    color='grey'
                else:
                    om_current_status = self.get_status(side,wall,col,row,OM_type,topic_option,'bad')
                    om_hs             = self.get_status(side,wall,col,row,OM_type,topic_option,'hs')
                    if om_hs == True:
                        color='black'
                    elif om_current_status == True:
                        color='red'
                    else:
                        color='green'
                            
        
                button_list.append(Button(self.a_second_xwall_frame, text = "%s.%s.%s.%s"%(side,wall,col,row), command = lambda x=toto_bis:self.DisplayOM("XW selected "+str(x))) )
                button_list[it].config(width="3")
                button_list[it].config(bg=color)
                button_list[it].grid(row=(int(self.nb_of_row_per_x_wall)-row),column=(int(self.nb_of_col_per_x_wall)-col))



        

        button_list = []
        ## BOTTOM GVETO ##
        self.a_bottom_gveto_frame = LabelFrame(self.half_det_display,highlightbackground="blue", highlightcolor="blue", highlightthickness=2, width=100, height=100, bd= 2,text="-- Bottom GVETO --")
        self.a_bottom_gveto_frame.grid(row=3,column=0,columnspan=3)
        OM_type = "GV"
        wall = 0
        row  = None
        for col in range(int(self.nb_of_col_per_g_veto)):
            it=col
            #        print(it)
            a_list = []
            #a_list[row,col]
            #a_list.insert(1,row)
            a_list.insert(1,col)
            toto=str(side)+"_"+str(wall)+"_"+str(col)
            
            current_om_checked = self.get_status(side,wall,col,row,OM_type,topic_option,'check')
            if current_om_checked == False:
                color='grey'
            else:
                om_current_status = self.get_status(side,wall,col,row,OM_type,topic_option,'bad')
                om_hs             = self.get_status(side,wall,col,row,OM_type,topic_option,'hs')
                if om_hs == True:
                    color='black'
                elif om_current_status == True:
                    color='red'
                else:
                    color='green'
                        
                        
            button_list.append(Button(self.a_bottom_gveto_frame, text = "%s.%s.%s"%(side,wall,col), command = lambda x=toto:self.DisplayOM("GV selected "+str(x))) )
            button_list[it].config(width="4")
            button_list[it].config(bg=color)
            button_list[it].grid(row=0,column=col)


        self.button_frame = Frame(self.half_det_display)
        self.button_frame.grid(row=4 ,column=1,columnspan=3)
        
        quit_button = Button(self.button_frame, text="CLOSE", width=5,command=self.half_det_display.destroy)
        quit_button.grid(row=1,column=0)

        refresh_button = Button(self.button_frame, text="REFRESH", width=5,command=lambda x=side:self.refresh(str(x)))
        refresh_button.grid(row=1,column=1)


#        self.half_det_display.destroy
        
               
if __name__ == "__main__":
    root = Tk()
    aplicacion = Mapping(root)
    debug = True
    
    intro_file = open("images/img.txt",'r')
    print(intro_file.read())
    

    
    
    root.mainloop()
