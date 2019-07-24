import pandas as pd
import numpy as np
import networkx as nx
import math
from networkx.readwrite import json_graph
import csv
import json
from sklearn.manifold import TSNE


with open('./thiers_2012.csv') as f:
    thiers_2012 = csv.reader(f, delimiter = '\t')
    links = []
    for row in thiers_2012:
        i = row[0].split('\t')
        #print(i)
        links.append({
            'time':int(i[0]),
            'id0':int(i[1]),
            'id1':int(i[2]),
            'class0': i[3],
            'class1': i[4]
        })
  #  print(links[1])
snapshots = []
start_time = 1353303380
end_time =1354032880
n = math.ceil((end_time - start_time) / 360)
#print(n)
for i in range(n):
    snapshot = []
    snapshots.append(snapshot)
#print(snapshots)
interval = 360
start = start_time#6:36:20
students = set()


split_day = []#每天24点正等于的秒数

total_day = math.ceil((end_time - (start_time - (6 * 3600 +36 * 60 + 20))) / (3600 * 24))
#print(total_day) #9天
first_endtime = start_time + 24 * 3600 - (6 * 3600 + 36 * 60 + 20)
split_day.append(first_endtime)
temp_time = first_endtime + 24 * 3600
for i in range(8):
    split_day.append(temp_time)
    temp_time += 24 * 3600
#print(split_day)
snapshot_day = []
snapshot_start = start_time
for i in range(len(links)):
    for index,endtime in enumerate(split_day):
        if snapshot_start < endtime:
            snapshot_day.append(index+1)
            break
    snapshot_start += interval
#print(snapshot_day)
for i in links:
    students.add(i['id0']) # 180个节点全部加入生成邻接矩阵
    students.add(i['id1'])
    l_time = start
    r_time = l_time + 3600
    while l_time  < end_time:
        if i['time'] >= l_time and i['time'] <= r_time:
            snapshots[(l_time - start_time)// interval].append(i)
            l_time += interval
            r_time += interval
        elif i['time'] < l_time:
            break
        else :
            l_time += interval
            r_time += interval
# for i in range(len(snapshots)):
#     print('s[{}] = {}
vectors = pd.read_csv("dimention.csv") #读取T-SNE降维后的坐标表
vectors = np.array(vectors)
#print(vectors)
graphs = []
total_python = []
for index,snapshot in enumerate(snapshots):
    graph = nx.Graph()
    edge_dic = {}
    nodes_set = set()
    single_dic = {}
    degrees = {}
    for row in snapshot:
        nodes_set.add(row['id0'])
        nodes_set.add(row['id1'])
        if row['id0'] < row['id1']:# 为方便统计，一律以ID较小的点作为边的起始点
            group = (row['id0'],row['id1'])
        else:
            group = (row['id1'],row['id0'])
        if group in edge_dic:
            edge_dic[group] += 1
        else :
            edge_dic[group] = 1
    nodes = list(nodes_set)
    graph.add_nodes_from(nodes)
    for key in edge_dic.keys():
     #   print("{} {} {}".format(key[0],key[1],edge_dic[key]))
        if key[0] in degrees:
            degrees[key[0]] += 1
        else: degrees[key[0]] = 1
        if key[1] in degrees:
            degrees[key[1]] += 1
        else: degrees[key[1]] = 1
        graph.add_edge(key[0],key[1],weight = edge_dic[key])
    graphs.append(graph)
    graph_python = json_graph.node_link_data(graph)
    for node in graph_python['nodes']:
        node['degree'] = degrees[node['id']]
    #print(graph_python['nodes'])
    single_dic['day'] = snapshot_day[index]
    single_dic['graph'] = graph_python
    single_dic['vector'] = [vectors[index][1],vectors[index][2]]
    total_python.append(single_dic)


#print(json.dumps(total_python))
with open('graph2.json','w',encoding='utf-8') as f:
    json.dump(total_python,f)
#json_data = json_graph.node_link_data(graphs)
#print(json_data)
# vectors = []
# for graph in graphs:
#     #if graph.size() != 0:
#         A = nx.adjacency_matrix(graph).todense()
#         vector = np.array([])
#         for row in A:
#             vector = np.append(vector,row)
#     #else:
#      #   vector = np.array([])
#         vectors.append(vector)
#         print(len(vectors))
# v = np.array(vectors)
# df = pd.DataFrame(v)
# df.to_csv('E:/summercamp/dimention.csv')
# print(v.shape)
# estimator = TSNE(n_components=2)
# X_pca = estimator.fit_transform(v)
# df = pd.DataFrame(X_pca)
# df.to_csv('E:/summercamp/dimention.csv')