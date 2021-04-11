'''
    Implements model readers & docker image generator
'''
__author__ = "Martin A. Guerrero Romero (marguerom1@alum.us.es)"

import argparse

from processing.CVEfiles import getGraph, getProductVersion
from processing.scrapping import getExistingImageNames
from processing.deployment import launchImage

def checkPortInput(localPort) -> int:
    '''
        Check input port is valid. If that is not the case, 8080 will be the default port

        :param localPort: user input port
    '''
    # If user does not enter any, port 8080 will be the default port
    if localPort == '':
        localPort = int('8080')
    else:
        try:
            int(localPort)
            # ¿Deberia validar q tenga 4 digitos?
        except ValueError as ve:
            print(ve)
            localPort = int('8080')

    return localPort

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process a vulnerabily model', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('fileDirectoryName', help='input file directory name\n'
                                                'eg. models/CVE-example.fm')
    args = parser.parse_args()

    # Check if file exists
    try:
        with open(args.fileDirectoryName) as file:

            # Load description and vulnerability tree
            description, graph = getGraph(file)

            # Ask the user for filters
            filter = input('\nPlease, enter filter words (separated by commas):')
            
            if filter == '':
                filters = []
            else:
                filters = filter.replace(' ','').split(',')

            # Check if 'version' is one of the filters entered. If that is not the case, he adds it
            if 'version' not in filters:
                filters.append('version')
            
            # Get Product & Version of filtered leaves of the graph
            pv = getProductVersion(graph, filters)

            # Get list of image names if they exist in the repository
            imageName = getExistingImageNames(pv)
            
            # Check if any image was found
            if not imageName:
                print('\nThe search has been unsuccessful! No image has been found')

                # Aqui habra q montar el docker-compose para montar la imagen que queremos
                # ESTO NO ESTA HECHO -------------------------------------------------------------------------------------

            else:
                # Check if it is one or more and show number of images found
                if isinstance(imageName, list):
                    print('\nThe search has been successful! '+str(len(imageName))+' images have been found')

                    # Ask the user for local host port
                    localPort = input('\nIn which port do you want to display the image?:')
                    localPort = checkPortInput(localPort)

                    for image in imageName:

                        # Pull and run container image
                        status = launchImage(image, localPort)
                        
                        # Check if it was launched successfully
                        if(status == 'Exit'):
                            print('Image '+image+' could not be launched')
                        else:
                            print('\nImage '+image+' has been launched successfully')
                            break
                    # ¿¿ Se acabaria aqui la ejecucion??

                else:
                    print('\nThe search has been successful! 1 image has been found')

                    # Ask the user for local host port
                    localPort = input('\nIn which port do you want to display the image?:')
                    localPort = checkPortInput(localPort)

                    # Pull and run container image
                    status = launchImage(imageName, localPort)
                    
                    # Check if it was launched successfully
                    if(status == 'Exit'):
                        print('Image '+imageName+' could not be launched')
                        
                        # ¿¿Redirigir al docker-compose??

                    else:
                        print('\nImage '+imageName+' has been launched successfully')

    # Catch File Not Found Error if the file is not found
    except FileNotFoundError as e:
        print('File not accessible. Please, check directory or file name.')
        print(e)
    
    # Ensure that the file is closed even if an exception happends during the program execution
    finally:
        file.close()
