from py2neo import Graph
from py2neo import NodeMatcher
graph = Graph("bolt: // localhost:7687", auth=("neo4j", "1121162842qazjch"))
matcher = NodeMatcher(graph)

# 1. 添加
# 为节点增加属性
def add_node_attr():
    query_add = "load csv with headers from 'file:///明星属性.csv' as line match (n:明星) where n.name=line.姓名 set n.出生日期=line.出生日期,n.介绍=line.介绍,n.代表作=line.代表作,n.民族=line.民族 return n"
    nodes_add = graph.run(query_add)
# 为关系添加属性
def add_rela_attr():
    query_relation_attr1 = "match (n:`明星`)-[r]-() where type(r)='好友' set r.name=0"
    query_relation_attr2 = "match (n:`明星`)-[r]-() where type(r)='离异' set r.name=1"
    query_relation_attr3 = "match (n:`明星`)-[r]-() where type(r)='旧爱' set r.name=2"
    query_relation_attr4 = "match (n:`明星`)-[r]-() where type(r)='制作人' set r.name=3"
    query_relation_attr5 = "match (n:`明星`)-[r]-() where type(r)='兄妹' set r.name=4"
    query_relation_attr6 = "match (n:`明星`)-[r]-() where type(r)='堂兄弟' set r.name=5"
    query_relation_attr7 = "match (n:`明星`)-[r]-() where type(r)='夫妻' set r.name=6"
    query_relation_attr8 = "match (n:`明星`)-[r]-() where type(r)='绯闻' set r.name=7"
    query_relation_attr9 = "match (n:`明星`)-[r]-() where type(r)='旧友' set r.name=8"
    nodes_relation_attr1 = graph.run(query_relation_attr1)
    nodes_relation_attr2 = graph.run(query_relation_attr2)
    nodes_relation_attr3 = graph.run(query_relation_attr3)
    nodes_relation_attr4 = graph.run(query_relation_attr4)
    nodes_relation_attr5 = graph.run(query_relation_attr5)
    nodes_relation_attr6 = graph.run(query_relation_attr6)
    nodes_relation_attr7 = graph.run(query_relation_attr7)
    nodes_relation_attr8 = graph.run(query_relation_attr8)
    nodes_relation_attr9 = graph.run(query_relation_attr9)
# 添加关系
def add_rela():
    query = "match (n) where n.name='谢霆锋' merge (n)-[:好友]->(m:明星{name:'哈林',sex:'男'})"
    graph.run(query)

# 2. 删除
# 删除属性
def de_attr():
    query_delete_attr = "match (n:`明星`) remove n.民族 return n"
    nodes_delete_attr = graph.run(query_delete_attr)
# 删除关系
def de_rela():
    query_delete_relate = "match (n:`明星`)-[r]-() where n.name='李大齐' delete r"
    nodes_delete_relate = graph.run(query_delete_relate)
# 删除节点
def de_node():
    query_delete_node = "match (n:`明星`) where n.name='李大齐' delete n "
    nodes_delete_node = graph.run(query_delete_node)

# 3.修改
# 王菲属性介绍改为华语天后
def update_attr():
    query = "match (n) where n.name='王菲' set n.介绍='华语天后' return n"
    nodes = graph.run(query)

# 4.查找
# 查找节点
def find_node():
    result = matcher.match("明星",name='王菲')
    list = list(result)
    print(list)
# 查找路径
def find_attr():
    query = "match p = (n:明星)-[:旧爱]->(m:明星{name:'谢霆锋'}) return p "
    rel = graph.run(query)
    for relationship in rel:
        print(relationship)

