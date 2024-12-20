# 日本新干线高速铁路网络社区分析

在本项目中，我们以日本新干线运行系统中的各个站点作为节点，以铁路线路作为边，线路的数量作为边的权重，构建了与现实情况相吻合的日本新干线网络。

![日本新干线网络可视化图](shinkansen_lines_weighted_visualization.png)

在构建的权重图上，我们对新干线网络做了基本的分析，并提供了数种 Python 方法可供其他程序调用。为了研究日本新干线网络，我们使用 Infomap 和 Louvain 两种方法对新干线网络做了分析，并将分析结果与现实情况做了比较。结果表明，两种方法均能较好地与现实情况相对应，但在社区划分的整体性和精细程度上有所区别。总的来说，Infomap 方法更好的体现了新干线的跨线运行的实际情况，而 Louvain 则更明确地反映了线路内的区域连接性。

## 日本新干线简介

日本新干线（Shinkansen）是日本高速铁路系统的核心，自1964年开通以来，已发展为覆盖全国主要城市的综合交通网络。新干线以高速、高效和高安全性为特征，当前运营的最高速度可达320公里/小时。网络由多条线路组成，包括东海道、山阳、东北、北陆、北海道等，覆盖范围从北海道到九州，总长度超过3000公里。作为现代交通基础设施的重要组成部分，新干线显著提高了区域间的连通性和经济活动效率，同时通过电力驱动和优化的运行系统减少了环境影响。其设计和运营经验也成为全球高速铁路发展的重要参考。

![新干线线路图](RouteMap.png)

日本新干线网络由多条线路组成，每条线路覆盖特定区域，满足不同地区间的交通需求。

1. 东海道新干线，连接东京、名古屋、大阪三大城市，覆盖日本经济最发达的东海道地区。
2. 山阳新干线，连接大阪和博多（福冈市），与东海道新干线相连，贯穿本州西部地区，是通往九州的主要高速通道。
3. 东北新干线，起点为东京，向东北延伸至新青森，覆盖福岛、仙台、盛冈等东北主要城市，是东北地区的交通动脉。
4. 北陆新干线，起点为东京，经过长野、富山，终点为金泽，服务于北陆地区，是连接日本中部与首都圈的重要线路。
5. 北海道新干线，从新青森通过青函隧道延伸至北海道函馆，未来规划将延伸至札幌，是连接本州与北海道的重要交通线路。
6. 九州新干线，分为博多至鹿儿岛中央的南段和计划中的北段（连接长崎），主要服务九州地区。
7. 西九州新干线，连接博多和长崎，是九州新干线的重要组成部分，但尚未与北段连接。
8. 上越新干线，连接东京与新潟，贯穿群马和长野地区，为日本中部与北部地区提供高速铁路服务。
9. 秋田新干线和山形新干线，分别从东京延伸至秋田和山形，服务于东北地区内陆区域。

## 日本新干线网络基本数据

通过以日本新干线运行系统中的各个站点作为节点，以铁路线路作为边，线路的数量作为边的权重，我们构建了对应的无向权重图，并对网络的基本参数做了分析。

从图中可以看出，因为西九州新干线尚未与北段连接，因此在网络中表现为一个独立的部分。其他线路之间的连接性较好，表现为一个整体网络。

经统计，日本新干线网络共有 124 个节点（站点）和 122 条边（线路），平均度为 1.97，平均聚类系数为 0.33，排除西九州段后直径为 71，西九州段直径为 5。

## 社区发现方法

### Infomap 方法

Infomap是一种基于信息理论的社区发现方法，用于网络中的节点群体划分。其核心思想是通过最小化随机游走者在网络中的路径编码长度来揭示社区结构。具体而言，Infomap将网络视为一个信息流系统，模拟随机游走者在网络中的移动，并使用二级Huffman编码描述游走路径。当游走者频繁访问某些节点群体时，这些节点被归类为一个社区，以减少整体编码长度。

与其他方法相比，Infomap具备高效性和适应性，能够处理有向、无向以及加权网络，同时在大规模网络上表现优异。由于其将社区划分与最优信息压缩问题联系起来，Infomap不仅提供了解释性强的社区划分结果，还能反映网络中的实际信息流动特性，是复杂网络研究中的重要工具。

### Louvain 方法

Louvain方法是一种基于模块度优化的社区发现算法，用于揭示网络中的社区结构。该方法通过迭代优化模块度（modularity）这一指标，来最大化网络中节点群体内部的连通性与群体间的分离性。

Louvain方法的执行过程包括两个主要阶段：

1. 局部模块度优化：初始化时，每个节点被视为一个独立社区，算法逐步将节点移入使模块度增加的邻居社区，直到无法进一步提升模块度。
2. 社区聚合与全局优化：将先前划分的社区作为超节点进行聚合，形成新的简化网络，随后在新的网络上重复上述过程，直到模块度收敛或达到最大值。

Louvain方法具有高效性和可扩展性，能够处理大规模网络，并广泛应用于社会网络、生物网络和信息传播网络的社区结构分析。其简单的实现和优良的性能使其成为社区发现领域的经典算法。

在代码中，我们调用了 community_louvain 和 infomap 第三方库，对新干线网络进行社区划分，并将结果储存在 `communities_infomap.json` 和 `communities_louvain.json` 文件中。

## 社区划分结果

### Infomap 结果

社区 1：`東京, 上野, 大宮, 小山, 宇都宮, 那須塩原, 新白河, 郡山, 福島, 熊谷, 本庄早稲田, 高崎, 上毛高原, 越後湯沢, 浦佐, 長岡, 燕三条, 新潟, ガーラ湯沢, 安中榛名`

这一社区包含東北新幹線的一部分（東京到那須塩原），以及上越新幹線（大宮到新潟），还包含了支线 北陸新幹線的一部分（高崎到安中榛名）。这一社区准确地涵盖了东日本地区主要的新干线线路，说明社区检测成功识别了相对密切的地理和交通网络关系。

社区 2：`品川, 新横浜, 小田原, 熱海, 三島, 新富士, 静岡, 掛川, 浜松, 豊橋, 三河安城, 名古屋, 岐阜羽島, 米原, 京都, 新大阪, 新神戸, 西明石, 姫路, 相生, 岡山, 新倉敷, 福山, 新尾道, 三原, 東広島, 広島, 新岩国, 徳山, 新山口, 厚狭, 新下関, 小倉, 博多, 新鳥栖, 久留米, 筑後船小屋, 新大牟田, 新玉名, 熊本, 新八代, 新水俣, 出水, 川内, 鹿児島中央`

这一社区准确对应東海道新幹線 和山陽新幹線，并延伸至九州新幹線，这一社区非常符合现实，因为这些线路是从东京延伸至九州地区的主干线，检测结果充分体现了这些线路的高连通性。

社区 3：`白石蔵王, 仙台, 古川, くりこま高原, 一ノ関, 水沢江刺, 北上, 新花巻, 盛岡, いわて沼宮内, 二戸, 八戸, 七戸十和田, 新青森, 雫石, 田沢湖, 角館, 大曲, 秋田, 奥津軽いまべつ, 木古内, 新函館北斗, 新八雲, 長万部, 倶知安, 新小樽, 札幌`

包含東北新幹線盛岡以北段和北海道新幹線，并且包括秋田新幹線和北海道新干线终点札幌。这一社区成功划分了东北、北海道方向的站点群，具有较强的地理一致性，同时，秋田新干线的纳入符合其与东北新干线共享部分轨道的现实。

社区 4：`軽井沢, 佐久平, 上田, 長野, 飯山, 上越妙高, 糸魚川, 黒部宇奈月温泉, 富山, 新高岡, 金沢, 小松, 加賀温泉, 芦原温泉, 福井, 越前たけふ, 敦賀`

划分结果完美匹配北陸新幹線，体现了算法对地理位置紧密连接线路的敏感性。

社区 5：`米沢, 高畠, 赤湯, かみのやま温泉, 山形, 天童, さくらんぼ東根, 村山, 大石田, 新庄`

山形新干线被完整地单独识别为一个社区，符合其独立的支线特点。

社区 6：`武雄温泉, 嬉野温泉, 新大村, 諫早, 長崎`

对应西九州新幹線，符合其独立于其他线路的特点。

总的来说，Infomap方法成功地将新干线网络划分为了与现实情况相符合的社区，各社区之间的连接性和地理位置关系得到了很好的体现。部分线路的共享部分被划分到了同一社区，反映了新干线网络的实际运行情况。

### Louvain 结果

与 Infomap相比，Louvain 算法的划分结果更细致，将一些线路进一步细分为多个社区。新划分中，社区划分更明确地反映了线路内的区域连接性，同时山形新干线、北陆新干线、西九州新干线依然作为独立的社区划分，与 Infomap 结果一致。

具体而言，在东京周边，东北新干线、上越新干线的起始段`東京, 上野, 大宮, 熊谷, 本庄早稲田, 高崎`被划分到了同一社区，而东北新干线中段则作为`小山, 宇都宮, 那須塩原, 新白河, 郡山, 福島`独立社区出现。

东北新干线北端和北海道新干线这两条联通的线路则以日本东北的重要城市盛冈为分界被分为了两段，`白石蔵王, 仙台, 古川, くりこま高原, 一ノ関, 水沢江刺, 北上, 新花巻, 盛岡` 和 `いわて沼宮内, 二戸, 八戸, 七戸十和田, 新青森, 奥津軽いまべつ, 木古内, 新函館北斗, 新八雲, 長万部, 倶知安, 新小樽, 札幌`

而贯通运行的东海道新干线和山阳新干线则被分为 3 段，`品川, 新横浜, 小田原, 熱海, 三島, 新富士, 静岡, 掛川, 浜松`，`豊橋, 三河安城, 名古屋, 岐阜羽島, 米原, 京都, 新大阪, 新神戸, 西明石, 姫路, 相生, 岡山` 和 `新倉敷, 福山, 新尾道, 三原, 東広島, 広島, 新岩国, 徳山, 新山口, 厚狭, 新下関, 小倉, 博多`，这种细致的拆分反映了线路内交通流量的区域性。

Louvain 算法的划分结果更精细，更贴合线路的实际区域性分布，突出了交通流量和区域节点的特点。但是，部分划分（如东海道新干线的进一步细分）可能导致整体连接性上的割裂感，不如上一份结果整体性强。

## 结论

通过对日本新干线高速铁路网络的分析，本文采用了 Infomap 和 Louvain 两种社区发现方法，展示了不同算法在网络划分上的特点及其与实际情况的对应性。结果表明，Infomap 方法更倾向于以整体性为导向，能较好地识别跨线路的运行特性和连接性；而 Louvain 方法则更注重细致的区域划分，更贴近线路内部的局部流量特征。

新干线网络的社区划分不仅验证了两种算法的有效性，还反映了日本高速铁路网络的复杂性和高效性。这些分析结果有助于进一步理解新干线网络的运行规律，为未来的交通规划和优化提供参考。同时，本文所用的方法和代码具有通用性，能够扩展到其他复杂交通网络的研究中。

未来工作可探索更多基于动态网络的社区发现方法，进一步分析新干线网络在不同时间尺度下的变化特性，从而揭示其潜在的发展趋势和优化空间。
