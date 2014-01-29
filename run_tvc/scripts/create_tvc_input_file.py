import sys
import os

###########################################################################
# using a single json for all bams
#  
# bam_folder = sys.argv[1]
# json = sys.argv[2]
# bed = sys.argv[3]
# hotspot = sys.argv[4]
#  
# target_files = [x for x in os.listdir(bam_folder) if x.endswith(".bam")]
#  
# for bam in target_files:
#     print "\t".join([bam_folder, bam, json, bed, hotspot])
    
    
###########################################################################
# using many parameter files, creating all combination of bam X json

bam_folder = sys.argv[1]
json_folder = sys.argv[2]
bed = sys.argv[3]
hotspot = sys.argv[4]
 
if hotspot == "None":
    hotspot = ""
 
target_files = [x for x in os.listdir(bam_folder) if x.endswith(".bam")]
target_jsons = [x for x in os.listdir(json_folder) if x.endswith(".json")]
 
target_files = target_files[:30]

target_files.sort()
target_jsons.sort()
 
for bam in target_files:
    for json in target_jsons:
        print "\t".join([bam_folder, bam, json_folder+json, bed, hotspot])