'''
    Implements creating Dockerfile methods
'''
__author__ = "Martin A. Guerrero Romero (marguerom1@alum.us.es)"

def opensslDockerfile(version):
    '''
        Create a Dockerfile with openSSL product
        
        :param version: specific version of OpenSSL
    '''
    with open('Dockerfile', 'w+') as dockerfile:

        dockerfile.write('# Base image\nFROM ubuntu:16.04')
        dockerfile.write('\n\nRUN apt-get update')
        dockerfile.write('\nRUN apt-get install -y build-essential cmake zlib1g-dev libcppunit-dev git subversion wget && rm -rf /var/lib/apt/lists/*')
        dockerfile.write('\nRUN wget https://www.openssl.org/source/openssl-'+version+'.tar.gz -O - | tar -xz')
        dockerfile.write('\nWORKDIR /openssl-'+version)
        dockerfile.write('\nRUN ./config --prefix=/usr/local/openssl --openssldir=/usr/local/openssl && make && make install')

def opensshDockerfile(version):
    '''
        Create a Dockerfile with openSSH product
        
        :param version: specific version of OpenSSH
    '''
    with open('Dockerfile', 'w+') as dockerfile:

        dockerfile.write('# Base image\nFROM ubuntu:16.04')
        dockerfile.write('\n\nRUN apt-get update')
        dockerfile.write('\nRUN apt-get install -y build-essential cmake zlib1g-dev libcppunit-dev git subversion wget && rm -rf /var/lib/apt/lists/*')
        dockerfile.write('\nRUN wget -c https://cdn.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-'+version+'p1.tar.gz')
        dockerfile.write('\nRUN tar -xzf openssh-'+version+'p1.tar.gz')

def firefoxDockerfile(version):
    '''
        Create a Dockerfile with openSSH product
        
        :param version: specific version of OpenSSH
    '''
    with open('Dockerfile', 'w+') as dockerfile:

        dockerfile.write('# Base image\nFROM ubuntu:16.04')
        dockerfile.write('\n\nRUN apt-get update && apt-get install -y apt-transport-https')
        dockerfile.write('\nRUN apt-get purge firefox')
        dockerfile.write('\nRUN apt-cache showpkg firefox')
        dockerfile.write('\nRUN apt-get install -y build-essential cmake zlib1g-dev libcppunit-dev git subversion wget && rm -rf /var/lib/apt/lists/*')
        dockerfile.write('\nRUN wget https://ftp.mozilla.org/pub/firefox/releases/'+version+'/linux-x86_64/en-US/firefox-45.0.tar.bz2')
        dockerfile.write('\nRUN tar -xjf firefox-'+version+'.tar.bz2')

def generalDockerfile(product, version):
    '''
        Create a Dockerfile with any product
        
        :param product: any product
        
        :param version: specific version of any product
    '''
    with open('Dockerfile', 'w+') as dockerfile:

        dockerfile.write('# Base image\nFROM ubuntu:16.04')
        dockerfile.write('\n\nRUN apt-get install '+product+'='+version)
