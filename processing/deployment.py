'''
    Launch a container image
'''
__author__ = "Martin A. Guerrero Romero (marguerom1@alum.us.es)"

import docker

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

def launchCreatedImage(pv, localPort, containerName) -> str:
    '''
        Try to create and launch an image

        :param pv: dictionary product-version(s) of CVE

        :param localPort: user entry local port

        :param containerName: user entry container name
    '''
    res = ''

    with open('Dockerfile', 'w+') as dockerfile:
        
        idx = 0

        # Creating specific Dockerfile
        for product in pv.keys():
            if isinstance(pv[product], list):
                if product == 'openssl':
                    version = pv[product][idx]
                    if idx < len(pv[product]):
                        idx += 1
                    else:
                        res = 'Exit'
                        break

                    dockerfile.write('# Base image\nFROM ubuntu:16.04')
                    dockerfile.write('\n\nRUN apt-get update')
                    dockerfile.write('\nRUN apt-get install -y build-essential cmake zlib1g-dev libcppunit-dev git subversion wget && rm -rf /var/lib/apt/lists/*')
                    dockerfile.write('\nRUN wget https://www.openssl.org/source/openssl-'+version+'.tar.gz -O - | tar -xz')
                    dockerfile.write('\nWORKDIR /openssl-'+version)
                    dockerfile.write('\nRUN ./config --prefix=/usr/local/openssl --openssldir=/usr/local/openssl && make && make install')
                else:
                    version = pv[product][idx]
                    if idx < len(pv[product]):
                        idx += 1
                    else:
                        res = 'Exit'
                        break
                    print('Preparar Dockerfile para otro tipo de producto')
            else:
                if product == 'openssl':
                    dockerfile.write('# Base image\nFROM ubuntu:16.04')
                    dockerfile.write('\n\nRUN apt-get update')
                    dockerfile.write('\nRUN apt-get install -y build-essential cmake zlib1g-dev libcppunit-dev git subversion wget && rm -rf /var/lib/apt/lists/*')
                    dockerfile.write('\nRUN wget https://www.openssl.org/source/openssl-'+pv[product]+'.tar.gz -O - | tar -xz')
                    dockerfile.write('\nWORKDIR /openssl-'+pv[product])
                    dockerfile.write('\nRUN ./config --prefix=/usr/local/openssl --openssldir=/usr/local/openssl && make && make install')
                else:
                    print('Preparar Dockerfile para otro tipo de producto')
    
    # Connect using the default socket or the configuration in your environment
    client = docker.from_env()

    print('\n --- Building the image (this may take a few minutes) ---')
    
    # Añadir try except para el build

    # Build an image of the Dockerfile path and return it. Tag is specific version used
    image = client.images.build(path = "./",rm=True) # ,nocache=True

    print('\n --- Running the container ---')
    
    # Run and start the container with specific name and port on the host
    container = client.containers.run(image[0],detach=True, name=str(containerName), ports={'2222/tcp': localPort})

    # Wait fot the end of the execution to obtain the exit code
    result = container.wait()
    exitCode = result["StatusCode"]
    
    # Check for launch failures
    if (int(exitCode) != 0):
        res = 'Exit'

    return res
