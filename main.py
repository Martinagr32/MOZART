'''
    Implements model readers & docker image generator
'''
__author__ = "Martin A. Guerrero Romero (marguerom1@alum.us.es)"

import argparse
from datetime import datetime

from processing.CVEfiles import getGraph, getProductVersion
from processing.scrapping import getExistingImageNames
from processing.deployment import launchPulledImage, launchCreatedImage

def checkPortInput(localPort) -> int:
    '''
        Check input port is valid. If that is not the case, 8080 will be the default port

        :param localPort: user input port
    '''
    # If user does not enter any or its not a number , port 8080 will be the default port
    if localPort == '':
        localPort = int('8080')
    else:
        try:
            int(localPort)
            if not (0 < int(localPort) and 65535 > int(localPort)):
                localPort = int('8080')
        except ValueError as ve:
            print('You must enter a number between 0 and 65535')
            print(ve)
            localPort = int('8080')

    return localPort

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process a vulnerabily feature model', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('fileDirectoryName', help='input file directory name\n'
                                                'eg. models/CVE-example.fm')
    args = parser.parse_args()

    print('\n       -----  MOZART  -----')

    # Check if file exists
    try:
        with open(args.fileDirectoryName) as file:

            # Append execution to general log
            with open('log/inputsLog.txt','a+') as logFile:

                # Create file with log of specific execution
                now = datetime.now().strftime('%d-%m-%Y %H.%M.%S') # Get current date and time without / and :
                newFile = 'log/inputsLog('+now+').txt'

                with open(newFile, 'w+') as eLogFile:
                    
                    # Introducing in general log
                    now = datetime.now().strftime('%d/%m/%Y %H:%M:%S') # Get current date and time
                    logFile.write('\n--- Starting execution (' + now + ') ---')
                    logFile.write('\n\nCVE file: '+args.fileDirectoryName)

                    # Introducing in specific log
                    eLogFile.write('--- Starting execution ---')
                    eLogFile.write('\n\nCVE file: '+args.fileDirectoryName)

                    # Load description and vulnerability tree
                    description, graph = getGraph(file)

                    # Ask the user for filters
                    filter = input('\nPlease, enter filter words (separated by commas):')

                    logFile.write('\n\nUser-entered filters: ' + filter)
                    eLogFile.write('\n\nUser-entered filters: ' + filter)
                    
                    if filter == '':
                        filters = []
                    else:
                        filters = filter.replace(' ','').split(',')

                    # Check if 'version' is one of the filters entered. If that is not the case, he adds it
                    if 'version' not in filters:
                        filters.append('version')
                    
                    # Get Product & Version of filtered leaves of the graph
                    pv = getProductVersion(graph, filters)

                    for product in pv.keys():
                        if product != '':

                            # Get list of image names if they exist in the repository
                            imageName = getExistingImageNames(pv)
                            
                            # Check if any image was found
                            if not imageName:
                                print('\nThe search has been unsuccessful! No image has been found')

                                # Ask the user for local host port
                                localPort = input('\nIn which port do you want to display the image?:')
                                    
                                logFile.write('\nUser-entered port: ' + localPort)
                                eLogFile.write('\nUser-entered port: ' + localPort)

                                localPort = checkPortInput(localPort)

                                # ASk the user for container name
                                containerName = input('\nPlease, enter container name (without spaces -> preferable use camelCase):')

                                logFile.write('\nUser-entered container name: ' + containerName)
                                eLogFile.write('\nUser-entered container name: ' + containerName)
                                            
                                if containerName == '' or len(containerName.split()) > 1:
                                    containerName = 'defaultName' # Autogenerate default name

                                # Build and run container image
                                status = launchCreatedImage(pv, localPort, containerName)

                                # Check if it was launched successfully
                                if(status == 'Exit'):
                                    print('Image could not be launched')
                                else:
                                    print('\nImage has been launched successfully')

                                now = datetime.now().strftime('%d/%m/%Y %H:%M:%S') # Get current date and time
                                logFile.write('\n\n--- End of execution (' + now + ') ---')
                                eLogFile.write('\n\n--- End of execution ---')

                            else:
                                # Check if it is one or more and show number of images found
                                if isinstance(imageName, list):
                                    print('\nThe search has been successful! '+str(len(imageName))+' images have been found')

                                    # Ask the user for local host port
                                    localPort = input('\nIn which port do you want to display the image?:')
                                    
                                    logFile.write('\nUser-entered port: ' + localPort)
                                    eLogFile.write('\nUser-entered port: ' + localPort)

                                    localPort = checkPortInput(localPort)

                                    # ASk the user for container name
                                    containerName = input('\nPlease, enter container name (without spaces -> preferable use camelCase):')

                                    logFile.write('\nUser-entered container name: ' + containerName)
                                    eLogFile.write('\nUser-entered container name: ' + containerName)
                                            
                                    if containerName == '' or len(containerName.split()) > 1:
                                        containerName = 'defaultName' # Autogenerate default name

                                    for image in imageName:

                                        # Pull and run container image
                                        status = launchPulledImage(image, localPort, containerName)
                                        
                                        # Check if it was launched successfully
                                        if(status == 'Exit'):
                                            print('Image '+image+' could not be launched')
                                        else:
                                            print('\nImage '+image+' has been launched successfully')
                                            break
                                    
                                    now = datetime.now().strftime('%d/%m/%Y %H:%M:%S') # Get current date and time
                                    logFile.write('\n\n--- End of execution (' + now + ') ---')
                                    eLogFile.write('\n\n--- End of execution ---')

                                else:
                                    print('\nThe search has been successful! 1 image has been found')

                                    # Ask the user for local host port
                                    localPort = input('\nIn which port do you want to display the image?:')

                                    logFile.write('\nUser-entered port: ' + localPort)
                                    eLogFile.write('\nUser-entered port: ' + localPort)

                                    localPort = checkPortInput(localPort)

                                    # ASk the user for container name
                                    containerName = input('\nPlease, enter container name (without spaces -> preferable use camelCase):')

                                    logFile.write('\nUser-entered container name: ' + containerName)
                                    eLogFile.write('\nUser-entered container name: ' + containerName)
                                            
                                    if containerName == '' or len(containerName.split()) > 1:
                                        containerName = 'defaultName' # Autogenerate default name

                                    # Pull and run container image
                                    status = launchPulledImage(imageName, localPort, containerName)
                                    
                                    # Check if it was launched successfully
                                    if(status == 'Exit'):
                                        print('Image '+imageName+' could not be launched')
                                        
                                        # Build and run container image
                                        newStatus = launchCreatedImage(pv, localPort, containerName)

                                        # Check if it was launched successfully
                                        if(newStatus == 'Exit'):
                                            print('Image could not be launched')
                                        else:
                                            print('\nImage has been launched successfully')

                                        now = datetime.now().strftime('%d/%m/%Y %H:%M:%S') # Get current date and time
                                        logFile.write('\n\n--- End of execution (' + now + ') ---')
                                        eLogFile.write('\n\n--- End of execution ---')

                                    else:
                                        print('\nImage '+imageName+' has been launched successfully')

                                        now = datetime.now().strftime('%d/%m/%Y %H:%M:%S') # Get current date and time
                                        logFile.write('\n\n--- End of execution (' + now + ') ---')
                                        eLogFile.write('\n\n--- End of execution ---')
                        else:
                            print('Empty product')

    # Catch File Not Found Error if the file is not found
    except FileNotFoundError as e:
        print('File not accessible. Please, check directory or file name.')
        print(e)
    
    # Ensure that the file is closed even if an exception happends during the program execution
    finally:
        eLogFile.close()
        logFile.close()
        file.close()
