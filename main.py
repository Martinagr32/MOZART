'''
    Implements model readers & docker image generator
'''
__author__ = "Martin A. Guerrero Romero (marguerom1@alum.us.es)"

import argparse

from processing.CVEfiles import getGraph, getProductVersion
from processing.scrapping import getExistingImageNames

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
                print('\nAn image with the specified characteristics could not be found')
                # Aqui habra q montar el docker-compose para montar la imagen que queremos
            else:
                print('\nAn image with the specified characteristics was found!')
                # Elegir una de ellas y lanzarla

    except FileNotFoundError as e:
        print('File not accessible. Please, check directory or file name.')
        print(e)
