import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

#should return neighbours,distances,angles
def determine_neighbours(coords,max_neighbours=4,neighbour_range=0.1,bi_directional=False):
    
    # distances
    d=np.zeros((coords.shape[0],coords.shape[0]))
    d_phi=np.zeros((coords.shape[0],coords.shape[0]))
    d_theta=np.zeros((coords.shape[0],coords.shape[0]))
    
    for i in range(coords.shape[0]):
        d_phi[:,i]=coords[:,0]-coords[i,0]
        d_theta[:,i]=coords[:,1]-coords[i,1]
        d[:,i]=np.sqrt(d_phi[:,i]**2+d_theta[:,i]**2)

    d[(np.arange(d.shape[0]),np.arange(d.shape[0]))]=np.inf




    # angles (of vectors from one node to the other on phi-theta-2D-plane)
    angles=np.arctan(d_theta/d_phi)
    negative=np.where(d_phi<0)
    s=np.sign(d_theta[negative])
    s[np.where(s==0)]=1
    angles[negative]=s*np.pi+angles[negative]
    


    if bi_directional:
        neighbours=_determine_neighbours_bi(d,max_neighbours,neighbour_range)
    else:
        neighbours=_determine_neighbours_single(d,max_neighbours,neighbour_range)

    return neighbours,d,angles


def plot_neighbourhood(ax,coords,neighbours,angles=None,directions_dict={}):
    
    G=coords_to_graph(coords)

    neighbours_to_graph_edges(G,neighbours)

    pos_dict={}

    for i in range(coords.shape[0]):
        pos_dict[i]=coords[i,:]


    edge_colors='black'

    if len(list(directions_dict.keys()))>0:
        if angles!=None:
            edge_colors=[]
            for edge_origin in list(G.edge.keys()):
                for edge_target in list(G.edge[edge_origin].keys()):
                    angle=angles[edge_target,edge_origin]
                    print(("angle="+str(angle)))
                    interval_found=False
                    for key in directions_dict:
                        if interval_found:
                            break
                        count=0
                        for interval in directions_dict[key][1:]:
                            count+=1
                            if angle>=interval[0] and angle<=interval[1]:
                                edge_colors.append(directions_dict[key][0])
                                interval_found=True
                                print("found! "+key)
                                break

                        print("checked "+str(count)+" intervals")
                                



    print(edge_colors)
    print(len(edge_colors))
    print(G.number_of_edges())


    nx.draw(G,pos_dict,ax,with_labels=True,edge_color=edge_colors)
    
    return G

def coords_to_graph(coords):
    G=nx.DiGraph()
    for i in range(coords.shape[0]):
        G.add_node(i,x=coords[0],y=coords[1])

    return G

def neighbours_to_graph_edges(G,neighbours):
    for i in range(len(neighbours)):
        #print neighbours[i]
        for j in range(len(neighbours[i])):
            G.add_edge(neighbours[i][j],i)
            #print "added edge from "+str(i)+" to "+str(j)


#should return only neighbours
def _determine_neighbours_single(distances,max_neighbours,neighbour_range):
    neighbours=[]

    for i in range(0,distances.shape[0]):
        neighbour_list=list(np.where(distances[i,:]<neighbour_range)[0])
        if len(neighbour_list)>max_neighbours:
            d=[(distances[i,j],j) for j in neighbour_list]
            d.sort()
            neighbour_list=[k[1] for k in d[:max_neighbours]]
        if len(neighbour_list)==0:
            print('WARNING: sensor (node) '+str(i)+' has no neighbours in range!')
        neighbours.append(neighbour_list)

    return neighbours

#should return only neighbours
def _determine_neighbours_bi(distances,max_neighbours,neighbour_range):
    print("!--!"*10)
    print("WARNING: bi directional neighbour detection not implemented yet!") 
    print("Using single directional detection instead")
    print("!--!"*10)

    return _determine_neighbours_single(distances,max_neighbours,neighbour_range)


if __name__=="__main__":

    plt.ion()

    coords=np.array(([0.5,0.75],[0.25,0.5],[0.5,0.5],[0.75,0.5],[0.5,0.25]))
    #coords=np.random.rand(8,2)

    neighbours,distances,angles=determine_neighbours(coords,4,0.3)

    
    f,ax=plt.subplots(1,1)
    
    #G=plot_neighbourhood(ax,coords,neighbours)
    G=plot_neighbourhood(ax,coords,neighbours,angles,{'HP':('r',[-np.pi/4,np.pi/4]),
                                                      'HN':('blue',[3./4*np.pi,np.pi],[-np.pi,-3./4*np.pi]),
                                                      'VP':('g',[np.pi/4.,3./4*np.pi]),
                                                      'VN':('purple',[-3./4*np.pi,-np.pi/4])})

    f.show()
