'''
    Implements data processing methods
'''
__author__ = "Martin A. Guerrero Romero (marguerom1@alum.us.es)"

import numpy as np

def getCleanData(file) -> list:
    '''
        Clean data of newline denotation and empty lines

        :param file: CVE file directory name to work with
    '''
    data=[]

    dirtyData = file.readlines()
    for line in dirtyData:
        if line != '\n':
            data.append(line.replace(';\n', ''))
    data.pop(1)
    
    return data

def getGraph(file) -> dict:
    '''
        Create a graph with the data from a CVE file

        :param file: CVE file directory name to work with
    '''
    graph = {}

    data = getCleanData(file)

    # Load CVE description
    description = data.pop(0).replace('# vul_description: ', '')

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

    return description, graph

def getFilterLeaves(graph, filters) -> list:
    '''
        Get filtered leaves from filters and graph received

        :param graph: Graph with the data from a CVE file

        :param filters: List of words to filter with
    '''
    leavesF = np.array([])

    for values in graph.values():
        # Check if it a list to go through it
        if isinstance(values, list):
            for value in values:
                # Check if the value is leaf and satisfy all the filters
                if value not in graph.keys() and all(filter in value for filter in filters):
                    leavesF = np.append(leavesF, value)
        else:
            # Check if the value is leaf and satisfy all the filters
            if values not in graph.keys() and all(filter in values for filter in filters):
                leavesF = np.append(leavesF, values)

    return leavesF

def getProductVersion(graph, filters) -> dict:
    '''
        Get Product & Version(s) of filtered leaves

        :param graph: Graph with the data from a CVE file

        :param filters: List of words to filter with
    '''
    pv = {}

    leaves = getFilterLeaves(graph, filters)
    print(leaves)

    for leaf in leaves:

        # Check if it is a running configuration and get the product accordingly
        if 'rc' in filters:
            product = leaf.split('_')[2]
        else:
            product = leaf.split('_')[1]
            
        version = leaf.split('version_',1)[1].replace('__','.')

        # Check if that product already exists
        if product in pv.keys():
            # Check if the key value is a list. If that is not the case, transform it
            if not isinstance(pv[product], list):
                pv[product] = [pv[product]]
            pv[product].append(version)
        else:
            pv[product] = version

    return pv