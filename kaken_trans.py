#!/usr/bin/python3

import sys
import pandas as pd
import tqdm
#pd.set_option('display.max_rows', 5000)

# コロンで区切られた年度予算を分割して年度別のレコードへ
def duplicateRecordWithColon(dataFrame, colName, dup_index):
    myyeardf = pd.DataFrame(index=[], columns=df.columns)
    eachval = str(dataFrame.loc[dup_index][colName]).split()
    if len(eachval) > 0:
        for val in eachval:
            item = val.split(':')
            if len(item) > 1:
                dist = dataFrame.loc[dup_index].copy()
                dist[colName+'.'+'年度'] = item[0]
                dist[colName+'.'+'配分額'] = item[1]
                myyeardf = myyeardf.append(dist)
    return myyeardf

#splitedColumns = ['各年度配分額', '各年度配分額 (直接経費)', '各年度配分額 (間接経費)']
# コロンで区切られた年度予算を分割
def splitWithColon(dataFrame, colName):
    newdf = dataFrame[colName].str.split(expand=True)
    for index, row in newdf.iterrows():
        sr = row.str.split(':')
        for item in sr:
            if type(item) == list:
                dataFrame.at[index, colName+'.'+item[0]] = item[1]
# 研究者情報を分割
def splitResearcher(dataFrame, colName):
    newdf1 = dataFrame[colName].str.split('[,()]', n=4, expand=True)
    newdf1.columns = ['tmp', colName+'.'+'学部', colName+'.'+'職階', colName+'.'+'研究者番号','drop']
    newdf2 = newdf1['tmp'].str.rsplit(n=1, expand=True)
    newdf2.columns = [colName+'.'+'氏名', colName+'.'+'所属']
    newdf = pd.concat([dataFrame, newdf2, newdf1[colName+'.'+'学部'], newdf1[colName+'.'+'職階'], newdf1[colName+'.'+'研究者番号']], axis=1)

if __name__ == '__main__':
    # 変換元 CSV ファイル
    infile = sys.argv[1]
    print("read ", infile)

    # 読み込みと前処理
    df = pd.read_csv(infile)
    size = len(df)

    # 研究代表者
    df = pd.concat([df, splitResearcher(df, '研究代表者')])

    # 研究分担者は放置
    #cname = '研究分担者'
    #newdf3 = df[cname].str.split('\n', expand=True)
    #print(newdf3)

    # 審査区分
    cname = '審査区分'
    df[cname+'.コード'] = df[cname].str.split(':',expand=True)[0]
    df[cname+'.分野名'] = df[cname].str.split(':',expand=True)[1]

    # 年度別予算
    yeardf = pd.DataFrame(index=[], columns=df.columns)
    drops = []
    print(len(df.index),"records are processing...")
    for index, row in tqdm.tqdm(df.iterrows()):
        newyeardf = duplicateRecordWithColon(dataFrame=df, colName='各年度配分額', dup_index=index)
        if len(newyeardf.index) > 0:
            yeardf = pd.concat([yeardf, newyeardf], ignore_index=True)
            drops.append(index)
    
    df = pd.concat([df.drop(index=df.index[drops]), yeardf], ignore_index=True)
    #for name in splitedColumns:
    #    splitWithColon(dataFrame=df, colName=name)

    #print(df)
    outfile = infile.replace('.csv', '.xlsx')
    df.to_excel(outfile, index=False)
    print("wrote", outfile)
