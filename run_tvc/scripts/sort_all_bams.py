import subprocess as sp
import os
import random
import multiprocessing as mp
import sys

def index_bam(bam):
    if os.path.exists(bam+".bai"):
        print "Exists, skipping", bam + ".bai"
    else:
        index_cmd = "samtools index %s" % (bam)
        sp.call(index_cmd, shell=True)

def sort_and_reindex_bam(bam):
    
#     origWD = os.getcwd() # remember our original working directory
#     os.chdir("/home/ionadmin/CallValidation/RerunTVC/ffdna/")
#     
    view_cmd = "samtools view -H %s" % bam
#     print view_cmd
    p = sp.Popen(view_cmd, stdout = sp.PIPE, shell=True)
    output = p.stdout.read()
    
    if "SN:chr1" in output:
        print bam, "is already sorted"
        
    else:
        print bam, "needs sorting"
        hash = random.randint(100, 999)
 
        mv_cmd = "mv %s tmp%i.bam" % (bam, hash)
        #sp.call(mv_cmd, shell=True)
         
        sort_cmd = "samtools sort tmp%i.bam %s" % (hash, bam.rstrip(".bam"))
        #sp.call(sort_cmd, shell=True)
         
        rm_cmd = "rm tmp%i.bam" % (hash)
        #sp.call(rm_cmd, shell=True)
        
        # reindex the sorted bam
        rm_bai_cmd = "rm %s.bai" % (bam)
        #sp.call(rm_bai_cmd, shell=True) 
        
        index_cmd = "samtools index %s" % (bam)
        #sp.call(index_cmd, shell=True)


def main():
    
    target_folder = sys.argv[1]
    
    bams = [target_folder + x for x in os.listdir(target_folder) if x.endswith(".bam")]
    pool = mp.Pool(processes=4)    
     
    for bam in bams:
        pool.apply_async(index_bam, args = [bam,])
 
    pool.close()
    pool.join()
    
######################################################################################################################################################################

if __name__ == '__main__':
    main()
