'''
    Implements model readers & docker image generator
'''
__author__ = "Martin A. Guerrero Romero (marguerom1@alum.us.es)"

import argparse

from fileProcessing.processor import getGraph, getProductVersion

def getImageName(pv):
    return 'None'

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
            filters = filter.replace(' ','').split(',')

            # Check if 'version' is one of the filters entered. If that is not the case, he adds it
            if 'version' not in filters:
                filters.append('version')

            # Get Product & Version of filtered leaves of the graph
            pv = getProductVersion(graph, filters)

            imageName = getImageName(pv)

            if(imageName != 'None'):
                print('\nAn image with the specified characteristics was found!')
            else:
                print('\nAn image with the specified characteristics could not be found')

    except FileNotFoundError as e:
        print('File not accessible. Please, check directory or file name.')
        print(e)
