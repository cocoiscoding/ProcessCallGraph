import pandas as pd
import numpy as np
import random
import os

if __name__ == '__main__':
    # cg = pd.read_csv('CallGraph_0.csv', on_bad_lines='skip')
    # data = set(cg['um'].tolist())
    # random.seed(8866)
    # ums = random.sample(list(data), 1)
    # print(ums)
    # ums = random.sample(list(data), 420)  # 抽样420个服务名
    # 写进映射文件
    # mp = pd.read_csv('mapping.csv', on_bad_lines='skip')
    # mp.insert(2, 'um', ums)
    # mp.to_csv('mapping.csv', index=False)

    # 改POD
    # filenames = os.listdir('table')
    # for fname in filenames:
    #     df = pd.read_csv('table/'+fname, on_bad_lines='skip')
    #     df.dropna(inplace=True)
    #     df.drop_duplicates(inplace=True)
    #     ums = df['um'].tolist()  # um列表
    #     uminstids = df['uminstanceid'].tolist()  # uminstanceid列表
    #     for idx in range(len(ums)):
    #         u = ums[idx][3:]
    #         uii = uminstids[idx]
    #         uiis = uii.split('_')
    #         if len(uiis) == 1:
    #             uminstids[idx] = ums[idx] + '_POD_' + str(random.randint(0, 10000))
    #             continue
    #         uiis[1] = u
    #         uminstids[idx] = '_'.join(uiis)
    #     dms = df['dm'].tolist()
    #     dminstids = df['dminstanceid'].tolist()
    #     for idx in range(len(dms)):
    #         if dms[idx] != 'Null':
    #             d = dms[idx][3:]
    #             dii = dminstids[idx]
    #             diis = dii.split('_')
    #             if len(diis) == 1:
    #                 dminstids[idx] = dms[idx] + '_POD_' + str(random.randint(0, 10000))
    #                 continue
    #             diis[1] = d
    #             dminstids[idx] = '_'.join(diis)
    #         else:
    #             dminstids[idx] = 'UNKNOWN'
    #     df['uminstanceid'] = uminstids
    #     df['dminstanceid'] = dminstids
    #     df.to_csv('new_table/'+fname, index=False)

    for idx in [7, 8, 9, 10, 11, 12]:
        # 抽样
        cg = pd.read_csv('CallGraph_' + str(idx) + '.csv', on_bad_lines='skip')
        cg.dropna(inplace=True)
        cg.drop_duplicates(inplace=True)
        filenames = os.listdir('rawdata')
        for fname in filenames:
            rawdf = pd.read_csv('rawdata/' + fname, on_bad_lines='skip', header=None)
            num = len(rawdf)  # 数据数量
            cg = cg.sample(n=num, replace=True)
            cg = cg.sort_values(by=['timestamp'], ascending=True)  # 按时间戳排序
            cg.to_csv('mapping/cg' + str(idx) + '/' + fname, index=False)

        # 替换um和dm
        filenames = os.listdir('rawdata')
        for fname in filenames:
            new_cg = pd.read_csv('mapping/cg' + str(idx) + '/' + fname, on_bad_lines='skip')
            raw_data = pd.read_csv('rawdata/' + fname, on_bad_lines='skip', header=None)
            nodes = raw_data.iloc[:, 1].tolist()  # 第二列
            fathers, childs = [], []
            for node in nodes:
                node = node.split('->')
                father, child = node[0], node[1]  # 拿到树的父子结点
                fathers.append(father)
                childs.append(child)
            new_cg['um'] = fathers
            new_cg['dm'] = childs
            new_cg.to_csv('mapping/cg' + str(idx) + '/' + fname, index=False)

        print('[{}] Finished!'.format(idx))
