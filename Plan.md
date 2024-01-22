## Structure2Guidance Plan
### 1. Task-任务
整个NLP Pipeline部分的输入为来自Camera的结构化数据，输出为Text形式的Guidance。
整个任务命名为Structure2Guidance，由两个串联的模块共同完成：Structure2Description以及Description2Guidance.任务的基本结构如下图所示：
![Task](./figs/Task.png)
### 2. Framework-框架
从硬件资源、数据资源，模型以及算法，应用场景的分层角度出发，整个Pipeline的Framework如下图所示：
![Framework](./figs/Framework.png)
现有资源包括Hardware, LLM(开源或API)，需在此基础上搭建数据、算法以及应用模块。

需要注意的是，由于LLM具备多任务的能力，同时为了在硬件资源受限的情况下启动系统，S2D，D2G两个模块最后是***在一个模型上***实现，通过不同的instruction prompt获得结果，暂定Base模型为***LLaMA-2-Chat***.
### 3 Strcuture2Description (S2D)
S2D部分数据构建相对要求低，主要挑战在于***采集足够数量的Structures***。
当获取足量Structures之后，基于GPT或本地LLM大量扩展获取Descriptions。
最后对LLAMA-2-Chat进行模型微调。
![S2D](./figs/S2D.png)
#### 3.1 Description2Guidance (D2G)
该部分数据构建相对困难，当前Description可能没有深度信息，在构建Guidance时，可能先用人工撰写的触觉表述构建demonstrations，再基于GPT-3.5/4大量生成（耗时长），最后可能还需要过滤。
![D2G](./figs/D2G.png)
### 5. Schedule-排期
| Week | Date      | Plan                                  | Person   |
|------|-----------|---------------------------------------|----------|
| 1    | 0128-0202 | 1. 采集Structures <br/> 2. 开源获取Captions | 1. Jason |
| 2    | 0204-0209 | 采集Structures                          | Jason    |
