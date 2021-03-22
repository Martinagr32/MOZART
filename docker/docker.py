
import os
import webbrowser

if __name__ == "__main__":

    image = 'wordpress' # Imagen que se despliega
    containerName = 'nameWordpress' # Nombre para trabajar mas comodo con el contenedor
    localPort = '8080' # Puerto local en el que se despliega

    os.system('docker run --name ' + containerName + ' -p ' + localPort + ':80 -d ' + image)

    webbrowser.open('http://localhost:' + localPort, new=2)