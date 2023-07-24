from py2neo import Graph
#节点创建
from py2neo import Node

def create_neo4jdatabase():
    graph = Graph("bolt: // localhost:7687", auth=("neo4j", "12345678"))
    query = "MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r"
    nodes = graph.run(query)
    wangfei = Node('明星',name='王菲',sex='女')
    liujialing = Node('明星',name='刘嘉玲',sex='女')
    liangchaowei = Node('明星',name='梁朝伟',sex='男')
    chengguanxi = Node('明星',name='陈冠希',sex='男')
    zhangbozhi = Node('明星',name='张柏芝',sex='女')
    xietingfeng = Node('明星',name='谢霆锋',sex='男')
    lidaqi = Node('明星',name='李大齐',sex='男')
    liyapeng = Node('明星',name='李亚鹏',sex='男')
    zhouxun = Node('明星',name='周迅',sex='女')
    quying = Node('明星',name='瞿颖',sex='女')
    zhangyadong = Node('明星',name='张亚东',sex='男')
    piaoshu = Node('明星',name='朴树',sex='男')
    douying = Node('明星',name='窦颖',sex='女')
    douwei = Node('明星',name='窦唯',sex='男')
    doupeng = Node('明星',name='窦鹏',sex='男')

    graph.create(wangfei)
    graph.create(liujialing)
    graph.create(liangchaowei)
    graph.create(chengguanxi)
    graph.create(zhangbozhi)
    graph.create(xietingfeng)
    graph.create(lidaqi)
    graph.create(zhouxun)
    graph.create(liyapeng)
    graph.create(quying)
    graph.create(zhangyadong)
    graph.create(piaoshu)
    graph.create(douying)
    graph.create(douwei)
    graph.create(doupeng)


    #创建关系
    from py2neo import Relationship
    #王菲的出度关系
    wf_1 = Relationship(wangfei,'好友',liujialing)
    wf_2 = Relationship(wangfei,'旧爱',xietingfeng)
    wf_3 = Relationship(wangfei,'离异',liyapeng)
    wf_4 = Relationship(wangfei,'离异',douwei)
    #刘嘉玲出度关系 —— 无
    #梁朝伟出度关系
    liangchaowei_1 = Relationship(liangchaowei,'夫妻',liujialing)
    #周迅出度关系
    zhouxun_1 = Relationship(zhouxun,'绯闻',liangchaowei)
    zhouxun_2 = Relationship(zhouxun,'旧爱',lidaqi)
    zhouxun_3 = Relationship(zhouxun,'绯闻',xietingfeng)
    zhouxun_4 = Relationship(zhouxun,'旧爱',liyapeng)
    zhouxun_5 = Relationship(zhouxun,'旧爱',piaoshu)
    zhouxun_6 = Relationship(zhouxun,'旧爱',doupeng)
    #陈冠希出度关系
    chengguanxi_1 = Relationship(chengguanxi,'旧爱',zhangbozhi)
    #张柏芝出度关系 —— 无
    #谢霆锋出度关系 —— 无
    xietingfeng_1 = Relationship(xietingfeng,'离异',zhangbozhi)
    xietingfeng_2 = Relationship(xietingfeng,'旧友',chengguanxi)
    #李大齐出度关系 —— 无
    #李亚鹏出度关系
    liyapeng_1 = Relationship(liyapeng,'旧爱',quying)
    #瞿颖出度关系
    quying_1 = Relationship(quying,'旧爱',zhangyadong)
    #张亚东出度关系
    zhangyadong_1 = Relationship(zhangyadong,'制作人',piaoshu)
    zhangyadong_2 = Relationship(zhangyadong,'制作人',wangfei)
    zhangyadong_3 = Relationship(zhangyadong,'离异',douying)
    #窦唯出度关系
    douwei_1 = Relationship(douwei,'兄妹',douying)
    douwei_2 = Relationship(douwei,'堂兄弟',doupeng)

    graph.create(wf_1)
    graph.create(wf_2)
    graph.create(wf_3)
    graph.create(wf_4)

    graph.create(liangchaowei_1)

    graph.create(zhouxun_1)
    graph.create(zhouxun_2)
    graph.create(zhouxun_3)
    graph.create(zhouxun_4)
    graph.create(zhouxun_5)
    graph.create(zhouxun_6)

    graph.create(chengguanxi_1)

    graph.create(xietingfeng_1)
    graph.create(xietingfeng_2)

    graph.create(liyapeng_1)

    graph.create(quying_1)

    graph.create(zhangyadong_1)
    graph.create(zhangyadong_2)
    graph.create(zhangyadong_3)

    graph.create(douwei_1)
    graph.create(douwei_2)
