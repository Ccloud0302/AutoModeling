import json


def transform_jsonl(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # 解析原始数据行为JSON对象
            data = json.loads(line)
            # 提取'instruction'字段
            input = data['input']
            # 遍历每个history项
            for history_item in data['history']:
                input_text = history_item[0]  # 从history中提取问题部分
                output_text = history_item[1]  # 从history中提取答案部分
                # 构建新的字典对象
                new_item = {
                    "instruction": "你是一个领域信息抽取模型，" + input_text,
                    "input": input,
                    "output": output_text
                }
                # 将新对象转换为JSON字符串，并写入到输出文件
                json.dump(new_item, outfile, ensure_ascii=False)
                outfile.write('\n')  # 添加换行符，以符合jsonl格式


if __name__ == '__main__':
    # 指定输入和输出文件路径
    input_file_path = 'QA3_qwen7b.jsonl'
    output_file_path = 'qwen_7b_dataset_final.jsonl'

    # 调用函数进行转换
    transform_jsonl(input_file_path, output_file_path)
