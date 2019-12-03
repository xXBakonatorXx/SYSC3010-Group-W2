# Python program to print all paths from a source to destination. 
   
from collections import defaultdict 
   
#This class represents a directed graph  
# using adjacency list representation 
class Graph: 
   
    def __init__(self,vertices): 
        #No. of vertices 
        self.V= vertices  
        self.paths = list()
          
        # default dictionary to store graph 
        self.graph = defaultdict(list)  
   
    # function to add an edge to graph 
    def addEdge(self,u,v): 
        self.graph[u].append(v) 
   
    '''A recursive function to print all paths from 'u' to 'd'. 
    visited[] keeps track of vertices in current path. 
    path[] stores actual vertices and path_index is current 
    index in path[]'''
    def findAllPathsUtil(self, u, d, visited, path): 
  
        # Mark the current node as visited and store in path 
        visited[u]= True
        path.append(u) 
  
        # If current vertex is same as destination, then print 
        # current path[] 
        if u ==d: 
            ###print (path)
            paths = list()
            self.paths = list()
            for node in path:
                self.paths.append(node)
            return
        else: 
            # If current vertex is not destination 
            #Recur for all the vertices adjacent to this vertex 
            for i in self.graph[u]: 
                if visited[i]==False: 
                    self.findAllPathsUtil(i, d, visited, path) 
                      
        # Remove current vertex from path[] and mark it as unvisited 
        path.pop() 
        visited[u]= False
   
   
    # Prints all paths from 's' to 'd' 
    def findAllPaths(self,s, d): 
  
        # Mark all the vertices as not visited 
        visited =[False]*(self.V) 
  
        # Create an array to store paths 
        path = [] 
  
        # Call the recursive helper function to print all paths 
        self.findAllPathsUtil(s, d,visited, path) 
   
    def getPath(self):
        return self.paths
   
if __name__ == "__main__":
    # Create a graph given in the above diagram 
    g = Graph(5) 
    g.addEdge(0, 1)
    g.addEdge(1, 2) 
    g.addEdge(1, 3) 
    g.addEdge(3, 4)  
       
    s = 0 ; d = 4
    print ("Following are all different paths from %s to %s :" %(s, d)) 
    g.findAllPaths(s, d) 
    print(g.getPath())
#This code is contributed by Neelam Yadav 
""" 
    Code based from: https://www.geeksforgeeks.org/find-paths-given-source-destination/
    Original authour: Neelam Yadav

    Many thanks from W2

"""