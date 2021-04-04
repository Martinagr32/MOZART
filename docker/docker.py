import os
import webbrowser
import docker

if __name__ == "__main__":

    # ESTO ES PARA LANZAR UN CONTENEDOR DE FORMA MANUAL
    '''
    image = 'wordpress' # Imagen que se despliega
    containerName = 'nameWordpress' # Nombre para trabajar mas comodo con el contenedor
    localPort = '8080' # Puerto local en el que se despliega

    os.system('docker run --name ' + containerName + ' -p ' + localPort + ':80 -d ' + image)

    webbrowser.open('http://localhost:' + localPort, new=2)
    '''

    # ESTOS ES PARA TRABAJAR CON DOCKER SDK FOR PYTHON
    client = docker.from_env()

    # Similar to docker search
    search = client.images.search('terminoBusqueda')

    # Pull an image (without auth)
    imageName = 'wordpress' # Algunas imagenes (como openssl no tienen con su nombre solo, usar los names resultados del search)
    image = client.images.pull(imageName)

    # Run a container (in the background)
    container = client.containers.run(image, detach=True)
    

