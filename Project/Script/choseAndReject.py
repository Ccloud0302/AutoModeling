import pandas as pd


# 加载Excel文件
def load_excel(file_path):
    return pd.read_excel(file_path)


# 处理并分割数据到多个sheets
def split_to_sheets(df, file_path):
    # 创建一个Pandas Excel writer使用openpyxl作为引擎
    writer = pd.ExcelWriter(file_path, engine='openpyxl')

    # 获取所有列名
    columns = df.columns.tolist()

    # 始终包括的列
    base_columns = ['instruction', 'input']

    # 识别所有唯一的前缀
    prefixes = set(col.split('_')[0] for col in columns if col not in base_columns)

    # 为每个前缀和每个数字创建一个sheet
    for prefix in prefixes:
        for i in range(1, 7):  # 假设数字最多到6，如您的例子所示
            chosen_col = f'{prefix}_Chosen_{i}'
            rejected_col = f'{prefix}_Rejected_{i}'

            # 检查列是否存在
            if chosen_col in columns and rejected_col in columns:
                # 选择需要的列
                sheet_df = df[base_columns + [chosen_col, rejected_col]]
                # 写入sheet
                sheet_df.to_excel(writer, sheet_name=f'{prefix}_{i}', index=False)

    # 保存文件
    writer.close()


# 主函数
def main():
    file_path = 'C:\\Users\\shiha\\OneDrive - mail.sdu.edu.cn\\Desktop\\博士（论文）\\大模型工作\\评测\\Test_RQ333.xlsx'
    output_path = 'C:\\Users\\shiha\\OneDrive - mail.sdu.edu.cn\\Desktop\\博士（论文）\\大模型工作\\评测\\Test_RQ333_split.xlsx'
    df = load_excel(file_path)
    split_to_sheets(df, output_path)


if __name__ == "__main__":
    main()
