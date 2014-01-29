# Parses a runfile of the tabbed format
# bamfolder   mybam.bam parameters.json hotspot.bed [optional: hotspots.vcf.gz]
# Files can be in the current dir or /home/ionadmin/andreas/core/run_tvc/data/, else the full pathname is needed
# 
# Launches TVC on each row

import sys
import subprocess
import time
import multiprocessing as mp
import random
import os
import logging

###################################################################################

def run_process(tvc_parameters):
    
    folder = tvc_parameters["folder"]
    bam = tvc_parameters["bam"]
    parameters = tvc_parameters["parameters"] 
    bed = tvc_parameters["bed"]
    hotspot_vcf = tvc_parameters["hotspot"]  
    
    tmp_folder = "tmp" + str(random.randint(1000, 9999))
    origWD = os.getcwd() # remember our original working directory
        
    mkdir_cmd = "mkdir ../data/" + tmp_folder
    logging.info(mkdir_cmd)
    subprocess.call(mkdir_cmd, shell=True)
    
#     logging.info("TVC start for %s: %s, %s, %s, \n%s" % (tmp_folder, bed, folder, parameters, bam))
    
    ####################################################################
    # change to the TVC dir, execute TVC and change back
    os.chdir("/results/plugins/variantCaller/")
    tvc_cmd = """python /results/plugins/variantCaller/variantCaller.py -b %s -r /results/uploads/hg19.fasta \
            -i %s/%s -o %s/%s -p %s -B . """   % (bed, folder, bam, origWD, tmp_folder, parameters)
    
    if hotspot_vcf:
        tvc_cmd += "-s %s/%s" % (origWD, hotspot_vcf)
    
    logging.info(tvc_cmd)
    subprocess.call(tvc_cmd, stdout = open("tmp.txt", "wa"), shell=True)
#     subprocess.call(tvc_cmd, shell=True)

    os.chdir(origWD) 
    ####################################################################
    
    short_bam = bam.split("/")[-1].split(".")[0]
    short_params = parameters.split("/")[-1][7:].rstrip(".json")
    short_bed = bed.split("/")[-1].rstrip(".bed")
    new_name = "_%s_%s.vcf" % (short_bam, short_params)

    rename_cmd = "rename 's/.vcf/%s/' %s/*.vcf" % (new_name, tmp_folder)
    logging.info(rename_cmd)
    subprocess.call(rename_cmd, shell=True)
    
    mv_cmd = "mv %s/*.vcf %s" % (tmp_folder, folder)
    logging.info(mv_cmd)
    subprocess.call(mv_cmd, shell=True)
    rm_cmd = "rm -R %s" % (tmp_folder)
    logging.info(rm_cmd)
    subprocess.call(rm_cmd, shell=True)
    
    logging.info("TVC finished for %s" % (tmp_folder))


######################################################################################################################################################################


def main():
        
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d-%m-%y %H:%M',
                    stream=sys.stdout,
                    filemode='w') 

    ###################################################################################
    # parse the runfile
    
    analysis_spreadsheet = sys.argv[1]

    to_run = []
    with open(analysis_spreadsheet) as analyses:
        for row in analyses:
            if row[0] == "#": continue
            f = row.rstrip("\n").split("\t")
            
#             print f
            
            # verify that all files exist before starting the multiprocessing
            origWD = os.getcwd() # remember our original working directory
            os.chdir("/results/plugins/variantCaller/")

            error = False
            message = ""
            if not os.path.isfile(f[0]+"/"+f[1]): 
                message += "\nCant find bam."
            
            if not os.path.isfile(f[2]):
                if os.path.isfile("/home/ionadmin/andreas/core/run_tvc/data/"+f[2]):
                    f[2] = "/home/ionadmin/andreas/core/run_tvc/data/" + f[2]
                else: 
                    message += "\nCant find file:" + f[2]
            
            if not os.path.isfile(f[3]):
                if os.path.isfile("/home/ionadmin/andreas/core/run_tvc/data/"+f[3]):
                    f[3] = "/home/ionadmin/andreas/core/run_tvc/data/" + f[3]
                else:
                    message += "\nCant find hotspot bed."            
#             try:
#                 if not os.path.isfile(f[4]):
#                     if os.path.isfile("/home/ionadmin/andreas/core/run_tvc/data/"+f[4]):
#                         f[4] = "/home/ionadmin/andreas/core/run_tvc/data/" + f[4]
#                     else:
#                         message += "\nCant find hotspot vcf."      
#             
#             except: pass
            
            if message != "":
                print row,
                print message
                sys.exit()
            
            to_run.append(f)
            os.chdir(origWD) 

    ###################################################################################
    
    pool_run = True
    
    if pool_run: pool = mp.Pool(processes=4)
          
    for analysis in to_run:
        
        tvc_parameters = {}
        
        tvc_parameters["folder"] = analysis[0]
        tvc_parameters["bam"] = analysis[1]
        tvc_parameters["parameters"] = analysis[2]
        tvc_parameters["bed"] = analysis[3]
        
        try:
            tvc_parameters["hotspot"] = analysis[4]
        except:
            tvc_parameters["hotspot"] = None

        if not pool_run: 
          run_process(tvc_parameters)
        else: 
          pool.apply_async(run_process, args = [tvc_parameters, ])
          
    if pool_run: pool.close()
    if pool_run: pool.join()

######################################################################################################################################################################

if __name__ == '__main__':
    main()
