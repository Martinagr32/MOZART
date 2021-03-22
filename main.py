<<<<<<< HEAD
'''
    Implements model readers & docker image generator
'''
__author__ = "Martin A. Guerrero Romero (marguerom1@alum.us.es)"

import argparse
import numpy as np

def createGraph(data):
    graph = {}

    for line in data:
        features = line.split()
        source = features.pop(0).replace(':', '')
        for feature in features:
            # Relation of attributes
            if feature == '[1,1]':
                pass
            # Optional attributes
            elif feature.find('[') != -1 and feature.find(']') != -1:
                if source in graph.keys():
                    if not isinstance(graph[source], list):
                        graph[source] = [graph[source]]
                    graph[source].append(feature[1:len(feature)-1])
                else:
                    graph[source] = [feature[1:len(feature)-1]]
            # Relational attributes
            elif feature.find('{') != -1:
                if source in graph.keys():
                    if not isinstance(graph[source], list):
                        graph[source] = [graph[source]]
                    graph[source].append(feature[1:len(feature)])
                else:
                    graph[source] = [feature[1:len(feature)]]
            elif feature.find('}') != -1:
                if source in graph.keys():
                    if not isinstance(graph[source], list):
                        graph[source] = [graph[source]]
                    graph[source].append(feature[0:len(feature)-1])
                else:
                    graph[source] = [feature[0:len(feature)-1]]
            # Common attributes
            else:
                if source in graph.keys():
                    if not isinstance(graph[source], list):
                        graph[source] = [graph[source]]
                    graph[source].append(feature)
                else:
                    graph[source] = feature

    return graph

def getFilterLeaves(graph, filters):
    leaves = np.array([])
    for values in graph.values():
        for value in values:
            if value not in graph.keys() and all(filter in value for filter in filters):
                leaves = np.append(leaves, value)
    return leaves

def getProductVersion(leaves):
    pv = {}
    for leaf in leaves:
        product = leaf.split('_')[2]
        version = leaf.split('version_',1)[1]
        if product in pv.keys():
            if not isinstance(pv[product], list):
                pv[product] = [pv[product]]
            pv[product].append(version)
        else:
            pv[product] = version
    return pv

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process a vulnerabily model', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('fileDirectoryName', help='input file directory name\n'
                                                'eg. models/CVE-example.fm')
    args = parser.parse_args()

    # Check if file exists
    try:
        with open(args.fileDirectoryName) as file:
            data=[]
            # Clean data without newline denotation
            dirtyData = file.readlines()
            for line in dirtyData:
                if line != '\n':
                    data.append(line.replace(';\n', ''))

            # Load description and vulnerability tree
            description = data.pop(0).replace('# vul_description: ', '')
            data.pop(0)
            graph = createGraph(data)

            # Get filter leaves
            filters = ['rc', 'version']
            leavesF = getFilterLeaves(graph, filters)

            # Get Product & Version of filtered leaves
            pv = getProductVersion(leavesF)

            print(pv)

    
    except FileNotFoundError:
        print('File not accessible. Please, check directory or file name.')
=======
'''
    Implements model readers & docker image generator
'''
__author__ = "Martin A. Guerrero Romero (marguerom1@alum.us.es)"

import argparse
import numpy as np

def createGraph(data):
    graph = {}

    for line in data:
        features = line.split()
        source = features.pop(0).replace(':', '')
        for feature in features:
            # Relation of attributes
            if feature == '[1,1]':
                pass
            # Optional attributes
            elif feature.find('[') != -1 and feature.find(']') != -1:
                if source in graph.keys():
                    if not isinstance(graph[source], list):
                        graph[source] = [graph[source]]
                    graph[source].append(feature[1:len(feature)-1])
                else:
                    graph[source] = [feature[1:len(feature)-1]]
            # Relational attributes
            elif feature.find('{') != -1:
                if source in graph.keys():
                    if not isinstance(graph[source], list):
                        graph[source] = [graph[source]]
                    graph[source].append(feature[1:len(feature)])
                else:
                    graph[source] = [feature[1:len(feature)]]
            elif feature.find('}') != -1:
                if source in graph.keys():
                    if not isinstance(graph[source], list):
                        graph[source] = [graph[source]]
                    graph[source].append(feature[0:len(feature)-1])
                else:
                    graph[source] = [feature[0:len(feature)-1]]
            # Common attributes
            else:
                if source in graph.keys():
                    if not isinstance(graph[source], list):
                        graph[source] = [graph[source]]
                    graph[source].append(feature)
                else:
                    graph[source] = [feature]

    return graph

def getLeaves(graph):
    leaves = np.array([])
    for values in graph.values():
        for value in values:
            if value not in graph.keys():
                leaves = np.append(leaves, value)
    return leaves

def getFilterLeaves(graph, filters):
    leaves = np.array([])
    for values in graph.values():
        for value in values:
            if value not in graph.keys() and all(filter in value for filter in filters):
                leaves = np.append(leaves, value)
    return leaves

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process a vulnerabily model', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('fileDirectoryName', help='input file directory name\n'
                                                'eg. models/CVE-example.fm')
    args = parser.parse_args()

    # Check if file exists
    try:
        with open(args.fileDirectoryName) as file:
            data=[]
            # Clean data without newline denotation
            dirtyData = file.readlines()
            for line in dirtyData:
                if line != '\n':
                    data.append(line.replace(';\n', ''))

            # Load description and vulnerability tree
            description = data.pop(0).replace('# vul_description: ', '')
            data.pop(0)
            graph = createGraph(data)

            # Get leaves and filter leaves
            filters = ['rc', 'version']
            leaves = getLeaves(graph)
            leavesF = getFilterLeaves(graph, filters)

            print(leavesF)

    
    except FileNotFoundError:
        print('File not accessible. Please, check directory or file name.')
>>>>>>> 0b7c0fa52338eda1a50f5154f38b9bbdda518d67
