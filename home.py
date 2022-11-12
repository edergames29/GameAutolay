from traceback import print_tb
from zipfile import ZipFile
import os
from datetime import datetime
import configparser
import logging
import platform
logging.basicConfig(filename='app.log', filemode='w', level=logging.INFO,format='%(asctime)s - %(message)s')

logging.info(f'{os.name}')
#logging.info(f'{os.getlogin()}')
logging.info(f'{platform.platform()},{platform.release()},{platform.version()}')
if not os.path.exists('Backups'):
    os.mkdir('Backups')

#import loadui

backing_up = False
config = configparser.ConfigParser()

#Puxar asctime
def getdatestring():
    now = datetime.now()
    current_time = now.strftime("%H-%M-%S_") #%S
    d4 = now.strftime("%b-%d-%Y")

    return str(current_time+d4)

#caso o arquivo de configuracao não exista ele cria um.
if config.read('home.ini'):
    print('arquivos de configuracoes lidos')
else:
    print('home.ini não existe')
    config['DEFAULT'] = {'BackupName':'Unknown',
                        'Delay': '180',
                        'PathSaveFile': r'',
                        'PathBackupFile': 'Backups/'}
    with open('home.ini', 'w') as configfile:
        #realterado
        config.write(configfile)

#pode ser chamado para rebuildar as configuracoes e aplicar no arquivo diretamente.
def update_configfile( BackupName, Delay, PathSaveFile, PathBackupFile):
    config['DEFAULT'] = {'BackupName':BackupName,
                        'Delay': Delay,
                        'PathSaveFile': str(PathSaveFile),
                        'PathBackupFile': PathBackupFile}
    with open('home.ini', 'w') as configfile:
        config.write(configfile)

#pega todos os arquivos na pasta escolhida para criar o zip
def get_all_file_paths(directory):
    logging.info('Searching paths...')
    # initializing empty file paths list
    file_paths = []
  
    # crawling through directory and subdirectories
    for root, directories, files in os.walk(directory):
        for filename in files:
            # join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
  
    # returning all file paths
    logging.info(f'Preparing to compress {len(file_paths)} files')
    return file_paths        
  
def main(overwriteold=False):
    
    backing_up=True #quando iniciar os processos de backup liga a variavel
    
    # path to folder which needs to be zipped
    directory = str(config['DEFAULT']['pathsavefile'])
  
    # calling function to get all file paths in the directory
    file_paths = get_all_file_paths(directory)
  
    # printing the list of all files to be zipped
    logging.info('Following files will be zipped:')
    for file_name in file_paths:
        logging.info(file_name)
  
    # writing files to a zipfile
    #myZipFile.write("test.py", "dir\\test.py", zipfile.ZIP_DEFLATED )
    if overwriteold:
        path=config['DEFAULT']['PathBackupFile']+config['DEFAULT']['backupname']+'.zip'
        logging.info("Criando arquivo de sobreposicao")

        #test if an old zip exists
        if os.path.exists(path):
            logging.info("file already exists")
            os.remove(path)
            logging.info("old file removed")
            
        with ZipFile(path,'x') as zip:
            # writing each file one by one

            for file in file_paths:
                zip.write(file)
            zip.close()
    else:
        logging.info("Criando arquivo de criacao")
        with ZipFile(config['DEFAULT']['PathBackupFile']+config['DEFAULT']['backupname']+'_'+getdatestring()+'.zip','w') as zip:
            # writing each file one by one
            for file in file_paths:
                zip.write(file)
            zip.close()
            
    

    print('All files zipped successfully!, CTRL+C to stop') 
    logging.info('All files zipped successfully!')
    backing_up=False




'''
if __name__ == "__main__":
    main()
'''