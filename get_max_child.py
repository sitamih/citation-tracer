#!/usr/bin/env python
# coding: utf-8

# Purpose: get all children nodes of the input paper, and the max child node
# Install pyalex: pip install pyalex

import pyalex
from pyalex import Works, Authors, Sources, Institutions, Topics, Publishers, Funders

# The function to get children nodes
def get_children(alexid):
    children = []
    cites = Works().filter(cites=alexid).get()
    for k in range(0,len(cites)):
        child = cites[k]['id']
        children.append(child)
    
    return children

# Get all children through the whole tree
def get_all_descendants_list(root):
    # Extract the OpenAlex ID from doi
    work = Works()[f"https://doi.org/{root}"]
    root = work["id"]
    
    visited = []  # Tracks visited nodes
    next_nodes = [root]  # Start with the root node
    all_nodes_count = []
    
    while next_nodes:
        current_nodes = next_nodes  # Nodes to process in this iteration
        next_nodes = []  # Reset for the next level
        next_nodes_count = []
        
        for node in current_nodes:
            if node not in visited:
                visited.append(node)  # Mark as visited
                count = Works()[node]['cited_by_count']
                #print(node, count)
                next_nodes.extend(get_children(node))  # Add children to explore next
                next_nodes_count.append(count)
        #print(next_nodes_count)
        all_nodes_count = all_nodes_count+next_nodes_count
        
    return visited[1:],all_nodes_count[1:]  # Exclude the root itself from the results


# Set input paper
#doi='https://openalex.org/W4393928016'
doi='10.1182/bloodadvances.2023012416'
print('Input doi is: ', doi)

# Get all children and their citations
desc = get_all_descendants_list(doi)

# Get the highest citation among all children
desc_dict = dict(zip(desc[0], desc[1]))
max_item = max(desc_dict.items(), key=lambda x: x[1])
print('Highest cited paper and its citation: ')
print(max_item)  # Output: ('xxx', 8)





