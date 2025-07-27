import pandas as pd
import json

# 读取Excel文件
excel_file = 'C:\\Users\\shiha\\OneDrive - mail.sdu.edu.cn\\Desktop\\博士（论文）\\大模型工作\\评测\\Test_RQ333.xlsx'  # 替换为您的Excel文件路径
sheet_names = pd.ExcelFile(excel_file).sheet_names  # 获取所有sheet名称

# 用于存储所有sheet的所有行数据
all_data = []

# 逐个读取每个sheet
for sheet in sheet_names:
    # 读取sheet的数据
    df = pd.read_excel(excel_file, sheet_name=sheet)

    # 假设每个sheet包含四列，遍历每一行并将其转换为字典
    for index, row in df.iterrows():
        row_dict = row.to_dict()
        # 将当前行数据添加到all_data中
        all_data.append(row_dict)

# 将所有数据写入JSON文件，每行一个JSON对象
with open('output.json', 'w', encoding='utf-8') as json_file:
    for data in all_data:
        json_file.write(json.dumps(data, ensure_ascii=False) + '\n')

print("Excel文件已成功转换为JSON文件！")
