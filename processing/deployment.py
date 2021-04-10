'''
    Implements web scrapping method to search existing images in Docker Hub
'''
__author__ = "Martin A. Guerrero Romero (marguerom1@alum.us.es)"

import docker

def launchImage(imageName, localPort) -> str:
    '''
        Try to launch an container image and return the status of the attempt

        :param imageName: container image name
    '''
    res = ''
    containerName = imageName[:4] + 'Name'

    # Connect using the default socket or the configuration in your environment
    client = docker.from_env()

    # Pull an image of the given name and return it
    image = client.images.pull(imageName)
    
    # Run and start the container with specific name and port on the host
    container = client.containers.run(image, detach=True, name=str(containerName), ports={'2222/tcp': localPort})

    # Wait fot the end of the execution to obtain the exit code
    result = container.wait()
    exitCode = result["StatusCode"]
    
    # Check for launch failures
    if (int(exitCode) != 0):
        res = 'Exit'

    return res