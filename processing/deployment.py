'''
    Launch a container image
'''
__author__ = "Martin A. Guerrero Romero (marguerom1@alum.us.es)"

import docker
from processing.dockerfiles import opensslDockerfile

def launchPulledImage(imageName, localPort, containerName) -> str:
    '''
        Try to launch a container pulled image and return the status of the attempt

        :param imageName: container image name

        :param localPort: user entry local port

        :param containerName: user entry container name
    '''
    res = ''

    print('\n --- Connecting and pulling an image ---')

    # Connect using the default socket or the configuration in your environment
    client = docker.from_env()

    # Pull an image of the given name and return it
    image = client.images.pull(imageName)

    print('\n --- Running the container ---')
    
    # Run and start the container with specific name and port on the host
    container = client.containers.run(image,detach=True, name=str(containerName), ports={'2222/tcp': localPort})

    # Wait fot the end of the execution to obtain the exit code
    result = container.wait()
    exitCode = result["StatusCode"]
    
    # Check for launch failures
    if (int(exitCode) != 0):
        res = 'Exit'

    return res

def buildAndRunImage(containerName, localPort) -> int:
    '''
        Create and launch an image

        :param localPort: user entry local port

        :param containerName: user entry container name
    '''
    # Connect using the default socket or the configuration in your environment
    client = docker.from_env()

    try:
        # Build an image of the Dockerfile path and return it.
        image = client.images.build(path = "./",rm=True) # ,nocache=True    

        print('\n --- Running the container ---')
                            
        # Run and start the container with specific name and port on the host
        container = client.containers.run(image[0],detach=True, name=str(containerName), ports={'2222/tcp': localPort})

        # Wait fot the end of the execution to obtain the exit code
        result = container.wait()
        exitCode = result["StatusCode"]

        return exitCode
    except:
        return 1

def launchCreatedImage(pv, localPort, containerName) -> str:
    '''
        Try to create and launch an image with specific product-version

        :param pv: dictionary product-version(s) of CVE

        :param localPort: user entry local port

        :param containerName: user entry container name
    '''
    res = ''

    print('\n --- Building the image (this may take a few minutes) ---')

    # Creating specific Dockerfile
    for product in pv.keys():

        idx = 0

        if isinstance(pv[product], list):
            if product == 'openssl':
                while idx < len(pv[product]):
                    version = pv[product][idx]
                    opensslDockerfile(version)

                    exitCode = buildAndRunImage(containerName, localPort)
                        
                    # Check for launch failures
                    if (int(exitCode) == 0):
                        res = ''
                        break
                    else:
                        res = 'Exit'
                        idx += 1
            else:
                print('Preparar Dockerfile para otro tipo de producto')
        else:
            if product == 'openssl':
                opensslDockerfile(pv[product])
                    
                exitCode = buildAndRunImage(containerName, localPort)
                            
                # Check for launch failures
                if (int(exitCode) != 0):
                    res = 'Exit'

            else:
                print('Preparar Dockerfile para otro tipo de producto')
    
    return res
