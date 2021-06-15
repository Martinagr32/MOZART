'''
    Implements model readers & docker image generator
'''
__author__ = "Martin A. Guerrero Romero (marguerom1@alum.us.es)"

from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image
from datetime import datetime

from processing.CVEfiles import getGraph, getProductVersion
from processing.scrapping import getExistingImageNames
from processing.deployment import launchPulledImage, launchCreatedImage

filename = ''

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

def selectCVE():
    global filename
    filename = askopenfilename()

    buttonCVE["state"] = "disabled"

def enterFilters():


    buttonFilter["state"] = "disabled"

def enterPort():
    buttonPort["state"] = "disabled"

def enterName():
    buttonName["state"] = "disabled"

if __name__ == "__main__":

    # Main window
    root = Tk()
    root.title("MOZART")
    root.geometry('520x305')
    
    # Image and icon
    imgPath = "./img/MOZART.jpg"
    img = ImageTk.PhotoImage(Image.open(imgPath))
    panel = Label(root, image = img, anchor="center")
    panel.grid(column=0, rowspan=6, pady=10, padx=10, sticky=W+E+N+S)
    #panel.place(x=175, y=175)
    #panel.pack(side = "top", fill = "both", expand = "yes")

    iconPath = "./img/iconMOZART.jpg"
    icon = ImageTk.PhotoImage(Image.open(iconPath))
    root.wm_iconphoto(False, icon)

    # Style
    style = Style()
    style.configure('TButton', font =
               ('calibri', 10, 'bold'),
                foreground = 'black')
    
    # Buttons (inputs)
    buttonCVE = Button(root, text="Select CVE", style = 'TButton', command = selectCVE)
    buttonCVE.grid(row = 1, column = 1, padx = 70)

    buttonFilter = Button(root, text="Enter filters", style = 'TButton', command = enterFilters)
    buttonFilter.grid(row = 2, column = 1, padx = 70)

    buttonPort = Button(root, text="Enter port", style = 'TButton', command = enterPort)
    buttonPort.grid(row = 3, column = 1, padx = 70)

    buttonName = Button(root, text="Enter name", style = 'TButton', command = enterName)
    buttonName.grid(row = 4, column = 1, padx = 70)
    
    root.mainloop()

    # Check if file exists
    try:
        with open(filename, 'r') as file:

            print(file.read())

            # Append execution to general log
            with open('log/inputsLog.txt','a+') as logFile:

                # Create file with log of specific execution
                now = datetime.now().strftime('%d-%m-%Y %H.%M.%S') # Get current date and time without / and :
                newFile = 'log/inputsLog('+now+').txt'

                with open(newFile, 'w+') as eLogFile:
                    
                    # Introducing in general log
                    now = datetime.now().strftime('%d/%m/%Y %H:%M:%S') # Get current date and time
                    logFile.write('\n--- Starting execution (' + now + ') ---')
                    logFile.write('\n\nCVE file: '+filename)

                    # Introducing in specific log
                    eLogFile.write('--- Starting execution ---')
                    eLogFile.write('\n\nCVE file: '+filename)

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
                            imageName = getExistingImageNames(product,pv)
                            
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
                                status = launchCreatedImage(product, pv, localPort, containerName)

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

                                    # Check if it was launched successfully
                                    if(status == 'Exit'):
                                        
                                        # Build and run container image
                                        newStatus = launchCreatedImage(product, pv, localPort, containerName)

                                        # Check if it was launched successfully
                                        if(newStatus == 'Exit'):
                                            print('Image could not be launched')
                                        else:
                                            print('\nImage has been launched successfully')

                                        now = datetime.now().strftime('%d/%m/%Y %H:%M:%S') # Get current date and time
                                        logFile.write('\n\n--- End of execution (' + now + ') ---')
                                        eLogFile.write('\n\n--- End of execution ---')
                                    
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
                                        newStatus = launchCreatedImage(product, pv, localPort, containerName)

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
                            print('\nEmpty product')

                            now = datetime.now().strftime('%d/%m/%Y %H:%M:%S') # Get current date and time
                            logFile.write('\n\n--- End of execution (' + now + ') ---')
                            eLogFile.write('\n\n--- End of execution ---')

                    if not pv.keys():
                        print('\nNo product to deploy')

                        now = datetime.now().strftime('%d/%m/%Y %H:%M:%S') # Get current date and time
                        logFile.write('\n\n--- End of execution (' + now + ') ---')
                        eLogFile.write('\n\n--- End of execution ---')

    # Catch File Not Found Error if the file is not found
    except FileNotFoundError as e:
        print('File not accessible. Please, check directory or file name.')
    
    # Ensure that the file is closed even if an exception happends during the program execution
    finally:
        eLogFile.close()
        logFile.close()
        file.close()
