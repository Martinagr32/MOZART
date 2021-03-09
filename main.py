'''
    Implements model readers & docker image generator
'''
__author__ = "Martin A. Guerrero Romero (marguerom1@alum.us.es)"

import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process a vulnerabily model', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('fileDirectoryName', help='input file directory name\n'
                                                'eg. models/example.txt')
    #parser.add_argument('-o', help='optional argument')
    args = parser.parse_args()

    # Check if file exists
    try:
        with open(args.fileDirectoryName) as file:
            data = file.readlines()
            print(data)
            for line in data:
                print(line)
    
    except FileNotFoundError:
        print('File not accessible. Please, check file name.')
