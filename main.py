'''
    Implements model readers & docker image generator
'''
__author__ = "Martin A. Guerrero Romero (marguerom1@alum.us.es)"

from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from PIL import ImageTk, Image
from datetime import datetime

from processing.CVEfiles import getGraph, getProductVersion
from processing.scrapping import getExistingImageNames
from processing.deployment import launchPulledImage, launchCreatedImage

filename = ''
userFilters = ''

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
    filename = askopenfilename()
    return filename

def enterFilters():
    windowF = Toplevel()
    windowF.title("Enter filters")
    windowF.geometry('430x80')
    windowF.wm_iconphoto(False, icon)

    label = Label(windowF, text="Please, enter filter words (separated by commas):")
    label.grid(column=0, row=0, pady=10, padx=10)

    filt = StringVar()
    entry = Entry(windowF, textvariable=filt)
    entry.grid(column=1, row=0, pady=10, padx=10)

    buttonF = Button(windowF, text = "Continue", command= windowF.destroy)
    buttonF.grid(row = 1, columnspan = 2, padx = 10)

    windowF.wait_window()

    return filt

def enterPort():
    windowP = Toplevel()
    windowP.title("Entering deployment port")
    windowP.geometry('425x80')
    windowP.wm_iconphoto(False, icon)

    label = Label(windowP, text="In which port do you want to display the image?")
    label.grid(column=0, row=0, pady=10, padx=10)

    port = StringVar()
    entry = Entry(windowP, textvariable=port)
    entry.grid(column=1, row=0, pady=10, padx=10)

    buttonP = Button(windowP, text = "Continue", command= windowP.destroy)
    buttonP.grid(row = 1, columnspan = 2, padx = 10)

    windowP.wait_window()

    return port

def enterName():
    windowN = Toplevel()
    windowN.title("Entering container name")
    windowN.geometry('550x80')
    windowN.wm_iconphoto(False, icon)

    label = Label(windowN, text="Enter container name (without spaces -> preferable use camelCase)")
    label.grid(column=0, row=0, pady=10, padx=10)

    name = StringVar()
    entry = Entry(windowN, textvariable=name)
    entry.grid(column=1, row=0, pady=10, padx=10)

    buttonP = Button(windowN, text = "Continue", command= windowN.destroy)
    buttonP.grid(row = 1, columnspan = 2, padx = 10)

    windowN.wait_window()

    return name

def start():

    filename = selectCVE()

    # Check if file exists
    try:
        with open(filename) as file:

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
                    enterFilter = enterFilters()
                    filter = enterFilter.get()

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
                                messagebox.showinfo("INFO", "The search has been unsuccessful! No image has been found.")

                                # Ask the user for local host port
                                introducedPort = enterPort()
                                localPort = introducedPort.get()
                                    
                                logFile.write('\nUser-entered port: ' + localPort)
                                eLogFile.write('\nUser-entered port: ' + localPort)

                                localPort = checkPortInput(localPort)

                                # Ask the user for container name
                                introducedName = enterName()
                                containerName = introducedName.get()

                                logFile.write('\nUser-entered container name: ' + containerName)
                                eLogFile.write('\nUser-entered container name: ' + containerName)
                                            
                                if containerName == '' or len(containerName.split()) > 1:
                                    containerName = 'defaultName' # Autogenerate default name

                                # Build and run container image
                                status = launchCreatedImage(product, pv, localPort, containerName)

                                # Check if it was launched successfully
                                if(status == 'Exit'):
                                    messagebox.showinfo("INFO", "Image could not be launched.")
                                    root.quit()                                   
                                else:
                                    messagebox.showinfo("INFO", "Image has been launched successfully.")
                                    root.quit()

                                now = datetime.now().strftime('%d/%m/%Y %H:%M:%S') # Get current date and time
                                logFile.write('\n\n--- End of execution (' + now + ') ---')
                                eLogFile.write('\n\n--- End of execution ---')

                            else:
                                # Check if it is one or more and show number of images found
                                if isinstance(imageName, list):
                                    infoText = "The search has been successful! "+str(len(imageName))+" images have been found."
                                    messagebox.showinfo("INFO", infoText)                                    

                                    # Ask the user for local host port
                                    introducedPort = enterPort()
                                    localPort = introducedPort.get()
                                    
                                    logFile.write('\nUser-entered port: ' + localPort)
                                    eLogFile.write('\nUser-entered port: ' + localPort)

                                    localPort = checkPortInput(localPort)

                                    # ASk the user for container name
                                    introducedName = enterName()
                                    containerName = introducedName.get()

                                    logFile.write('\nUser-entered container name: ' + containerName)
                                    eLogFile.write('\nUser-entered container name: ' + containerName)
                                            
                                    if containerName == '' or len(containerName.split()) > 1:
                                        containerName = 'defaultName' # Autogenerate default name

                                    for image in imageName:

                                        # Pull and run container image
                                        status = launchPulledImage(image, localPort, containerName)
                                        
                                        # Check if it was launched successfully
                                        if(status == 'Exit'):
                                            text = "Image " + image + " could not be launched."
                                            messagebox.showinfo("INFO", text)
                                        else:
                                            text = 'Image '+image+' has been launched successfully'
                                            messagebox.showinfo("INFO", text)
                                            root.quit()
                                            break

                                    # Check if it was launched successfully
                                    if(status == 'Exit'):
                                        
                                        # Build and run container image
                                        newStatus = launchCreatedImage(product, pv, localPort, containerName)

                                        # Check if it was launched successfully
                                        if(newStatus == 'Exit'):
                                            messagebox.showinfo("INFO", 'Image could not be launched')
                                            root.quit()
                                        else:
                                            messagebox.showinfo("INFO", 'Image has been launched successfully')
                                            root.quit()                                            

                                        now = datetime.now().strftime('%d/%m/%Y %H:%M:%S') # Get current date and time
                                        logFile.write('\n\n--- End of execution (' + now + ') ---')
                                        eLogFile.write('\n\n--- End of execution ---')
                                    
                                    now = datetime.now().strftime('%d/%m/%Y %H:%M:%S') # Get current date and time
                                    logFile.write('\n\n--- End of execution (' + now + ') ---')
                                    eLogFile.write('\n\n--- End of execution ---')

                                else:
                                    messagebox.showinfo("INFO", 'The search has been successful! 1 image has been found')                                    

                                    # Ask the user for local host port
                                    introducedPort = enterPort()
                                    localPort = introducedPort.get()

                                    logFile.write('\nUser-entered port: ' + localPort)
                                    eLogFile.write('\nUser-entered port: ' + localPort)

                                    localPort = checkPortInput(localPort)

                                    # ASk the user for container name
                                    introducedName = enterName()
                                    containerName = introducedName.get()

                                    logFile.write('\nUser-entered container name: ' + containerName)
                                    eLogFile.write('\nUser-entered container name: ' + containerName)
                                            
                                    if containerName == '' or len(containerName.split()) > 1:
                                        containerName = 'defaultName' # Autogenerate default name

                                    # Pull and run container image
                                    status = launchPulledImage(imageName, localPort, containerName)
                                    
                                    # Check if it was launched successfully
                                    if(status == 'Exit'):
                                        text = 'Image '+imageName+' could not be launched'
                                        messagebox.showinfo("INFO", text) 
                                        
                                        # Build and run container image
                                        newStatus = launchCreatedImage(product, pv, localPort, containerName)

                                        # Check if it was launched successfully
                                        if(newStatus == 'Exit'):
                                            messagebox.showinfo("INFO", 'Image could not be launched')
                                            root.quit()
                                        else:
                                            messagebox.showinfo("INFO", 'Image has been launched successfully')
                                            root.quit()

                                        now = datetime.now().strftime('%d/%m/%Y %H:%M:%S') # Get current date and time
                                        logFile.write('\n\n--- End of execution (' + now + ') ---')
                                        eLogFile.write('\n\n--- End of execution ---')

                                    else:
                                        text = 'Image '+imageName+' has been launched successfully'
                                        messagebox.showinfo("INFO", text)
                                        root.quit()

                                        now = datetime.now().strftime('%d/%m/%Y %H:%M:%S') # Get current date and time
                                        logFile.write('\n\n--- End of execution (' + now + ') ---')
                                        eLogFile.write('\n\n--- End of execution ---')
                        else:
                            messagebox.showinfo("INFO", 'Empty product')

                            now = datetime.now().strftime('%d/%m/%Y %H:%M:%S') # Get current date and time
                            logFile.write('\n\n--- End of execution (' + now + ') ---')
                            eLogFile.write('\n\n--- End of execution ---')
                            root.quit()

                    if not pv.keys():
                        messagebox.showinfo("INFO", 'No product to deploy')

                        now = datetime.now().strftime('%d/%m/%Y %H:%M:%S') # Get current date and time
                        logFile.write('\n\n--- End of execution (' + now + ') ---')
                        eLogFile.write('\n\n--- End of execution ---')
                        root.quit()

    # Catch File Not Found Error if the file is not found
    except FileNotFoundError as e:
        messagebox.showerror("ERROR", "File not selected. Please, select a file.")


if __name__ == "__main__":

    # Main window
    root = Tk()
    root.title("MOZART")
    root.geometry('520x305')
    
    # Image and icon
    imgPath = "./img/MOZART.jpg"
    img = ImageTk.PhotoImage(Image.open(imgPath))
    panel = Label(root, image = img, anchor="center")
    panel.grid(column=0, row=0, pady=10, padx=10, sticky=W+E+N+S)

    iconPath = "./img/iconMOZART.jpg"
    icon = ImageTk.PhotoImage(Image.open(iconPath))
    root.wm_iconphoto(False, icon)

    # Style
    style = Style()
    style.configure('TButton', font =
               ('calibri', 10, 'bold'),
                foreground = 'black')
    
    # Start button
    buttonStart = Button(root, text="Start!", style = 'TButton', command = start)
    buttonStart.grid(row = 0, column = 1, padx = 70)
    
    root.mainloop()

    