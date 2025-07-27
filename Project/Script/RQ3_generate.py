import json
import pandas as pd


def chaifen(df, output_file_path):
    # 创建一个新的 Excel writer
    with pd.ExcelWriter(output_file_path, engine="openpyxl") as writer:
        # 获取所有列名
        columns = df.columns.tolist()

        # 找到包含 'Chosen' 和 'Rejected' 的列
        chosen_rejected_columns = [col for col in columns if "Chosen" in col or "Rejected" in col]

        # 按照 'Chosen' 和 'Rejected' 分组
        for i in range(0, len(chosen_rejected_columns), 2):  # 步长为2，因为一对是Chosen和Rejected
            chosen_col = chosen_rejected_columns[i]
            rejected_col = chosen_rejected_columns[i + 1]

            # 提取包含 'instruction', 'input', 以及一对 'Chosen' 和 'Rejected' 的列
            selected_columns = ['instruction', 'input', chosen_col, rejected_col]
            sheet_data = df[selected_columns]

            # 将数据写入新的 sheet
            sheet_name = f"{chosen_col.split('_')[0]}_{chosen_col.split('_')[1]}_{chosen_col.split('_')[2]}"
            sheet_data.to_excel(writer, sheet_name=sheet_name, index=False)

    print("文件已成功拆分并保存为 'output.xlsx'.")

def load_jsonl(file_path):
    """ Load JSON lines from the specified file. """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = [json.loads(line.strip()) for line in file]
    return lines

def transform_to_RejectedAndChosen(answer_file_path, n):
    RC_list = []
    RC_dic = {}
    for i in range(n):
        RC_dic["instruction"] = load_jsonl(answer_file_path[0])[i]["instruction"]
        RC_dic["input"] = load_jsonl(answer_file_path[0])[i]["input"]

        # Human
        RC_dic["H_Chosen_1"] = load_jsonl(answer_file_path[0])[i]["output"]
        RC_dic["H_Rejected_1"] = load_jsonl(answer_file_path[1])[i]["output"]

        RC_dic["H_Chosen_2"] = load_jsonl(answer_file_path[0])[i]["output"]
        RC_dic["H_Rejected_2"] = load_jsonl(answer_file_path[2])[i]["output"]

        RC_dic["H_Chosen_3"] = load_jsonl(answer_file_path[0])[i]["output"]
        RC_dic["H_Rejected_3"] = load_jsonl(answer_file_path[3])[i]["output"]

        RC_dic["H_Chosen_4"] = load_jsonl(answer_file_path[1])[i]["output"]
        RC_dic["H_Rejected_4"] = load_jsonl(answer_file_path[2])[i]["output"]

        RC_dic["H_Chosen_5"] = load_jsonl(answer_file_path[1])[i]["output"]
        RC_dic["H_Rejected_5"] = load_jsonl(answer_file_path[3])[i]["output"]

        RC_dic["H_Chosen_6"] = load_jsonl(answer_file_path[2])[i]["output"]
        RC_dic["H_Rejected_6"] = load_jsonl(answer_file_path[3])[i]["output"]

        # ST
        RC_dic["ST_Chosen_1"] = load_jsonl(answer_file_path[0])[i]["output"]
        RC_dic["ST_Rejected_1"] = load_jsonl(answer_file_path[1])[i]["output"]

        RC_dic["ST_Chosen_2"] = load_jsonl(answer_file_path[0])[i]["output"]
        RC_dic["ST_Rejected_2"] = load_jsonl(answer_file_path[2])[i]["output"]

        RC_dic["ST_Chosen_3"] = load_jsonl(answer_file_path[0])[i]["output"]
        RC_dic["ST_Rejected_3"] = load_jsonl(answer_file_path[3])[i]["output"]

        RC_dic["ST_Chosen_4"] = load_jsonl(answer_file_path[1])[i]["output"]
        RC_dic["ST_Rejected_4"] = load_jsonl(answer_file_path[2])[i]["output"]

        RC_dic["ST_Chosen_5"] = load_jsonl(answer_file_path[1])[i]["output"]
        RC_dic["ST_Rejected_5"] = load_jsonl(answer_file_path[3])[i]["output"]

        RC_dic["ST_Chosen_6"] = load_jsonl(answer_file_path[3])[i]["output"]
        RC_dic["ST_Rejected_6"] = load_jsonl(answer_file_path[2])[i]["output"]

        print(RC_dic)

        RC_list.append(RC_dic)

    return RC_list


if __name__ == '__main__':
    # 指定输入和输出文件路径
    answer1_file_path = '../self-instruct/dataset/qwen2_72b_dataset_final.jsonl'
    answer2_file_path = '../self-instruct/dataset/llama_70b_dataset_final.jsonl'
    answer3_file_path = '../self-instruct/dataset/qwen1.5_72b_dataset_final.jsonl'
    answer4_file_path = '../self-instruct/dataset/qwen_7b_dataset_final.jsonl'
    answer_file_path = [answer1_file_path, answer2_file_path, answer3_file_path, answer4_file_path]
    output_file_path = 'C:\\Users\\shiha\\OneDrive - mail.sdu.edu.cn\\Desktop\\博士（论文）\\大模型工作\\评测\\Test_RQ333.xlsx'

    # n是所有数据的个数
    n = len(load_jsonl(answer1_file_path))
    # 调用函数进行转换
    RC_list = transform_to_RejectedAndChosen(answer_file_path, n)

    print(len(RC_list))

    df = pd.DataFrame(RC_list)

    chaifen(df, output_file_path)

    # df.to_excel(output_file_path, index=False)