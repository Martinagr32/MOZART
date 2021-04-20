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