#!/usr/bin/python3.5

# Author  : Y.Lemiere
# Date    : 2020/01
# Contact : lemiere@lpccaen.in2p3.fr
# Object  : SuperNEMO OM commissioning


from datetime import date, datetime
import time
import sys
import os
import subprocess
import configparser
import subprocess
#import scp

def usage():
    print("\nHow to use it :\n")
    print("DEMO mode for local test :")
    print("   |-> ./init.py -d  (--demo or --debug)")
    print("RECOVERY mode for production getting data from ccage :")
    print("   |-> ./init.py -r")
    print("HELP to display this help :")
    print("   |-> ./init.py -h")
    


    
def recover_data():

    function_name = "recover_data"
    snemo_cfg = configparser.ConfigParser()
    snemo_cfg.read('conf/snemo.cfg')
    distant_path =  snemo_cfg.get('FILE_CFG','ccage_path')+"/"+snemo_cfg.get('FILE_CFG','tgz_file')
    local_path =  snemo_cfg.get('FILE_CFG','local_path')
    try:

        if os.path.isdir(local_path) == True:
            print("ERROR : [%s] : %s exist, don't overwrite it! or do it yourself"%(function_name,local_path))
            sys.exit(1)
        else:
            os.makedirs(local_path)
    except:
        print("\033[91mERROR\033[00m : [%s] : Can not create directories on %s  "%(function_name,local_path))
        sys.exit(1)

            
    print("INFO : [%s] : You will pull Calorimeter status data from CCAGE"%(function_name))
    id_name = input("REQUEST : [%s] :  Please, enter your cclyon id : "%(function_name))
    print("scp -r %s@%s:%s %s"%(id_name,snemo_cfg.get('FILE_CFG','server_name'),distant_path,local_path))
    #os.system('scp -r %s@%s %s %s'%(id_name,snemo_cfg.get('FILE_CFG','server_name'),distant_path,local_path))
    from_ = id_name+"@"+snemo_cfg.get('FILE_CFG','server_name')+":"+distant_path
    to_   = local_path
    #print(from_)
    #print(to_)
    
    try:
        p = subprocess.Popen(["scp", from_, to_])
        sts = os.waitpid(p.pid, 0)
        os.system('tar -xvzf %s/%s -C %s'%(to_,snemo_cfg.get('FILE_CFG','tgz_file'),to_))
        os.system('rm -f $(pwd)/data/files')
        os.system('ln -s $(pwd)/%s/last_version $(pwd)/data/files'%(to_))

    except:
        print("\033[91mERROR\033[00m : [%s] : Can not transfer data from %s  "%(function_name,distant_path))
        sys.exit(1)
    
    
def produce_files(side_nb, column_nb, row_nb, el, path):

    if el == None:
        OM_ID = "OM_"+str(side_nb)+"."+str(column_nb)+"."+str(row_nb)
    else:
        OM_ID = "OM_"+str(side_nb)+"."+str(column_nb)+"."+str(row_nb)+"."+str(el)

    fiber_log_filename =  path+"/"+OM_ID+"_fiber.log"
    fiber_log = open(fiber_log_filename,'w')
    fiber_log.write('[OM_ID]\n\n')
    fiber_log.write('id = %s\n'%(OM_ID))
    fiber_log.write('\n')
    
    fiber_log.write('[STATUS]\n\n')
    fiber_log.write('fiber0_CHECK = 0\n')
    fiber_log.write('fiber0_OK = 0\n')
    fiber_log.write('fiber0_BAD = 0\n')
    fiber_log.write('fiber0_HS = 0\n')
    fiber_log.write('\n')
    fiber_log.write('fiber1_CHECK = 0\n')
    fiber_log.write('fiber1_OK = 0\n')
    fiber_log.write('fiber1_BAD = 0\n')
    fiber_log.write('fiber1_HS = 0\n')
    fiber_log.write('\n')
    fiber_log.write('[COMMENT]\n\n')
    fiber_log.write('fiber0_comment = \n')
    fiber_log.write('fiber1_comment = \n')
    
    HV_log_filename =  path+"/"+OM_ID+"_HV.log"
    HV_log = open(HV_log_filename,'w')
    HV_log.write('[OM_ID]\n\n')
    HV_log.write('id = %s\n'%(OM_ID))
    HV_log.write('\n')
    
    HV_log.write('[STATUS]\n\n')
    HV_log.write('HV_CHECK = 0\n')
    HV_log.write('HV_OK = 0\n')
    HV_log.write('HV_BAD = 0\n')
    HV_log.write('HV_HS = 0\n')
    HV_log.write('\n')
    HV_log.write('[COMMENT]\n\n')
    HV_log.write('HV_comment = \n')
    
    signal_log_filename =  path+"/"+OM_ID+"_signal.log"
    signal_log = open(signal_log_filename,'w')
    signal_log.write('[OM_ID]\n\n')
    signal_log.write('id = %s\n'%(OM_ID))
    signal_log.write('\n')
    
    
    signal_log.write('[STATUS]\n\n')
    signal_log.write('signal_CHECK = 0\n')
    signal_log.write('signal_OK = 0\n')
    signal_log.write('signal_BAD = 0\n')
    signal_log.write('signal_HS = 0\n')
    signal_log.write('\n')
    signal_log.write('[COMMENT]\n\n')
    signal_log.write('signal_comment = \n')
    
    
    
    leak_log_filename =  path+"/"+OM_ID+"_leak.log"
    leak_log = open(leak_log_filename,'w')
    leak_log.write('[OM_ID]\n\n')
    leak_log.write('id = %s\n'%(OM_ID))
    leak_log.write('\n')
    
    
    leak_log.write('[STATUS]\n\n')
    leak_log.write('leak_CHECK = 0\n')
    leak_log.write('leak_OK = 0\n')
    leak_log.write('leak_BAD = 0\n')
    leak_log.write('leak_HS = 0\n')
    leak_log.write('\n')
    leak_log.write('[COMMENT]\n\n')
    leak_log.write('leak_comment = \n')
      
    

if __name__ == '__main__':
    start_time= datetime.now()
    debug=True
    app_name = sys.argv[0]
    dummy_mode = False
    recovery_mode = False
    
    i=0
    for arg in sys.argv[1:]:
        i=i+1
        if arg == "-d" or arg == "--debug" or arg == "--demo":
            dummy_mode    = True
            recovery_mode = False
        if arg == "-r" or arg == "--recovery":
            dummy_mode    = False
            recovery_mode = True
        elif arg == "-h" or arg == "--help":
            usage()
            sys.exit(0)
    
    intro_file = open("images/img.txt",'r')
    print(intro_file.read())
    
    

    
    
    snemo_cfg = configparser.ConfigParser()
    snemo_cfg.read('conf/snemo.cfg')


    if dummy_mode == True:

        if debug:
            print("INFO : [%s] enter in dummy mode")
        
        data_path =  snemo_cfg.get('FILE_CFG','data_path')
        
        context = ["main_wall","x_wall","gamma_veto"]
        nb_of_side = snemo_cfg.get('GEO_CFG','number_of_side')
        nb_of_column_per_mw = snemo_cfg.get('GEO_CFG','number_of_column_per_main_wall')
        nb_of_row_per_mw    = snemo_cfg.get('GEO_CFG','number_of_row_per_main_wall')
        
        nb_of_wall_per_x_wall = snemo_cfg.get('GEO_CFG','number_of_wall_per_x_wall')
        nb_of_row_per_x_wall    = snemo_cfg.get('GEO_CFG','number_of_row_per_x_wall')
        nb_of_col_per_x_wall    = snemo_cfg.get('GEO_CFG','number_of_col_per_x_wall')
        
        nb_of_wall_per_g_veto = snemo_cfg.get('GEO_CFG','number_of_wall_per_g_veto')
        nb_of_col_per_g_veto    = snemo_cfg.get('GEO_CFG','number_of_col_per_g_veto')
        
        if debug:
            print("DEBUG : [%s] Create %s 'side' directories" %(app_name,nb_of_side))
            print("DEBUG : [%s] Create %s 'column' in MW directories" %(app_name,nb_of_column_per_mw))
            print("DEBUG : [%s] Create %s 'row' in MW directories" %(app_name,nb_of_row_per_mw))
            
            print("DEBUG : [%s] Create %s 'wall' in XW directories" %(app_name,nb_of_wall_per_x_wall))
            print("DEBUG : [%s] Create %s 'row' in XW directories" %(app_name,nb_of_row_per_x_wall))
            print("DEBUG : [%s] Create %s 'col' in XW directories" %(app_name,nb_of_col_per_x_wall))
            
            print("DEBUG : [%s] Create %s 'col' in GV directories" %(app_name,nb_of_col_per_g_veto))
            print("DEBUG : [%s] Create %s 'wall' in GV directories" %(app_name,nb_of_wall_per_g_veto))
            
        try:
            os.makedirs(data_path)
            os.system('rm -f $(pwd)/data/files')
            os.system('ln -s $(pwd)/%s $(pwd)/data/files'%(data_path))

            fourth_level = None
            
            for om in context:
                for side_nb in range(int(nb_of_side)):
                    full_side_path = data_path+"/"+om+"/"+'side'+str(side_nb)
                    print(full_side_path)
                    os.makedirs(full_side_path)
                    if om == "main_wall":
                        second_level = int(nb_of_column_per_mw)
                        third_level = int(nb_of_row_per_mw)
                        second_level_name = "column"
                        third_level_name = "row"
                    elif om == "x_wall":
                        second_level = int(nb_of_wall_per_x_wall)
                        third_level = int(nb_of_col_per_x_wall)
                        fourth_level = int(nb_of_row_per_x_wall)
                        second_level_name = "wall"
                        third_level_name = "column"
                        fourth_level_name = "row"
                    elif om == "gamma_veto":
                        second_level = int(nb_of_wall_per_g_veto)
                        third_level  = int(nb_of_col_per_g_veto)
                        second_level_name = "wall"
                        third_level_name = "row"
                        fourth_level=None
                    
                    for column_nb in range(second_level):
                        full_column_path = full_side_path+"/"+second_level_name+str(column_nb)
                        os.makedirs(full_column_path)
                        for row_nb in range(third_level):

                            full_row_path = full_column_path+"/"+third_level_name+str(row_nb)
                            os.makedirs(full_row_path)

                            if fourth_level != None:
                                for el in range(fourth_level):
                                    full_el_path = full_row_path+"/"+fourth_level_name+str(el)
                                    os.makedirs(full_el_path)
                                    produce_files(side_nb, column_nb, row_nb, el, full_el_path)
                            elif fourth_level == None:
                                produce_files(side_nb, column_nb, row_nb, None, full_row_path)
                                
                  
                        
        except:
            print("\033[91mERROR\033[00m : [%s] : Can not create directories on %s  "%(app_name,data_path))
            sys.exit(1)
    elif recovery_mode == True:
        print("Recovery mode")
        recover_data()
        
    else:
        print("WARNING : [%s] Please dummy or recovery mode ? "%app_name)
        usage()
        sys.exit(1)

                    
    print("INFO :  : The END!")
    sys.exit(0)
