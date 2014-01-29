'''
Created Dec 2012

RunIRVariantAnnotation

@author: Joe Wood

'''

import logging
from config import api_config
import IRApiUtilities
import csv
import sys

def main():
    
    #configure logging 
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d-%m-%y %H:%M',
                    stream=sys.stdout,
                    filemode='w') 
       
#     filename=api_config['log_file']
    myIRApiUtilities = IRApiUtilities.IRApiUtilities()
    
    #Read analysis.csv file
    analysis_file = sys.argv[1]
    
    try:
        analysisReader = csv.reader(open(analysis_file, 'rb'), delimiter=',')
    except IOError:
        print "Error: can\'t find file or read data"
        logging.error("Error: can\'t find file or read data")
        
    logging.debug('analysis_file %s read',api_config['analysis_file']) 
    
    #Get variome files    
    for analysis in analysisReader:
        
        analysis_id = analysis[0]
        analysis_ir_version = "ir16"
#         analysis_ir_version = analysis[1]
        
        analysis_base_url = api_config['analysis_base_url'].replace("IR_VERSION", analysis_ir_version)
        variome_base_url = api_config['variome_base_url'].replace("IR_VERSION", analysis_ir_version)
        
        get_variome = myIRApiUtilities.get_variome(analysis_id,api_config['token'],analysis_base_url,variome_base_url,api_config['output_path'], analysis_ir_version)

        try:     
            get_variome = myIRApiUtilities.get_variome(analysis_id,api_config['token'],analysis_base_url,variome_base_url,api_config['output_path'], analysis_ir_version)
        except:
            logging.error('Variome fetching failed for analysis %s',analysis_id)
        
        if(get_variome == 1):
            logging.info('Variome exported for analysis %s',analysis_id)
        elif(get_variome == 0):
            logging.error('Variome export failed for analysis %s',analysis_id)
    
    logging.info("Finished")    

if __name__ == '__main__':
    main()