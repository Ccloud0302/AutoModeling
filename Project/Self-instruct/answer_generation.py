import random
import re

from zhipuai import ZhipuAI
from openai import OpenAI
import json


with open("generation_instruction.txt", "r", encoding="UTF-8") as file:
    content = file.readlines()
    # print(content)
file2 = open("error_instruction.txt", "a", encoding="UTF-8")
file3 = open("QA3.jsonl", "a", encoding="UTF-8")
index = 0

instruction = [
    "请判断并归纳输入文本所属的领域场景。",
    "请根据输入文本识别出工序，归纳为不少于一个的上下文。",
    "请根据输入文本识别出实体以及每个实体的命名空间（Namespace），命名空间形式为'{domain}.{context}，domain为实体所属的工艺场景，context为实体所属的上下文。",
    "请根据输入文本识别出实体以及每个实体所拥有的独特属性。",
    "请根据输入文本识别出实体以及每个实体的前置事件。",
    "请根据输入文本识别出实体以及每个实体的状态。",
    "请根据输入文本识别出的每个状态的前置事件，以及每个状态的每个动作，并识别其中每个动作所拥有的参数。"
]


# 将连续两个换行符替换为一个换行符
def remove_extra_newline(text):
    return text.replace('\n\n', '\n')


def extract_input_from_jsonl(file_path):
    input_list = []  # 创建一个空列表用于存储解析后的数据
    with open(file_path, 'r', encoding="utf-8") as file:
        for line in file:
            input = json.loads(line.strip())  # 解析 JSON
            input_list.append(input)
    return input_list

def extract_history_from_jsonl(file_path):
    # 初始化一个字典，用于存储 history 中的每一项
    history_lists = {}

    # 打开并读取 JSONL 文件
    with open(file_path, 'r', encoding="utf-8") as file:
        for line in file:
            data = json.loads(line)  # 解析 JSON
            history = data['history']  # 获取 history 字段
            input = data['input']
            # 遍历 history 中的每一项
            for index, his in enumerate(history):
                if index not in history_lists:
                    history_lists[index] = []
                # 将当前项添加到相应的列表中
                item = {"input": input, "QA": his}
                history_lists[index].append(item)

    # 将字典的值（列表）转换为一个列表返回，保持顺序
    return list(history_lists.values())

def generation(input_n, history_list, generation_QA_list, input_list):
    while input_n < len(input_list):  # len(input_list)
        generation_history_list = []  # 用来存放模型的回答一轮（6次）的结果

        for his in history_list:
            # 随机从种子指令和生成指令中取10条
            history_list_instructions = random.sample(his, 5)
            # if len(generation_QA_list) > 10:
            #     generation_QA = random.sample(generation_QA_list, 3)
            # 建立模版
            prompt = "你是一个领域信息抽取模型，你的下面是一些抽取实例：\n"
            for index, instruction in enumerate(history_list_instructions):
                prompt += f"{str(index + 1)}、工艺生产方案：{instruction['input'].strip()}\n"
                prompt += f"{str(index + 1)}、问题：{instruction['QA'][0].strip()}\n"
                prompt += f"{str(index + 1)}、答案：{instruction['QA'][1].strip()}\n"
            prompt +="请参考上面问题与回答的内容和形式（请按照给出示例的答案的模板和形式进行回答，不要只回答一个单独的字符串”），根据指令：“{instruction}”，对下面的工艺生产方案进行相应信息的抽取：“{input}”。".format(instruction=instruction['QA'][0], input=input_list[input_n]["input"])
            # if len(generation_QA_list) > 10:
            #     for index_QA, instruction_QA in enumerate(generation_QA):
            #         prompt += f"{str(index_QA + 7)}、工艺生产方案：{instruction_QA['input'].strip()}\n"
            #         prompt += f"{str(index_QA + 7)}、问题：{instruction_QA['QA'][0].strip()}\n"
            #         prompt += f"{str(index_QA + 7)}、答案：{instruction_QA['QA'][1].strip()}\n"
            #         prompt += "======================================================\n"
            # print(prompt)

            # client = ZhipuAI(api_key="8363a2361547c410fb4be690d3436640.CrZUvRtrTAZIbPvC")  # 填写您自己的APIKey
            client = OpenAI(
                base_url='http://172.26.255.255:11434/v1/',
                api_key='ollama',  # 此处的api_key为必填项，但在ollama中会被忽略
            )

            messages = [{"role": "user",
                         "content": prompt}]
            print(messages)
            chat_completion = client.chat.completions.create(
                messages=messages,
                model='llama3:70b',
            )
            answer = chat_completion.choices[0].message.content

            # response = client.chat.completions.create(
            #     model="glm-4",
            #     messages=messages,
            # )
            # answer = response.choices[0].message.content


            print("answer" + answer)
            QAList = []
            QAList.append(instruction['QA'][0])
            QAList.append(answer)
            generation_history_list.append(QAList)
        history_dict = {"instruction": instruction['QA'][0],"input": input_list[input_n]["input"], "output": "", "history": generation_history_list}
        print(f"{input_n + 1}   成功   QA: {history_dict}")
        file3.write(json.dumps(history_dict, ensure_ascii=False) + "\n")

        input_n += 1

# 提取模型文件中的input，存到list中
def extract_inputs_from_jsonl(file_path):
    inputs = []  # 创建一个空列表来存放input字段的内容
    with open(file_path, 'r',  encoding="UTF-8") as file:
        for line in file:
            try:
                json_data = json.loads(line)  # 解析每一行为JSON
                inputs.append(json_data)  # 提取input字段并添加到列表中
            except json.JSONDecodeError as e:
                # 打印错误信息和出错的行
                print(f"Error parsing JSON: {e}")
                print(f"Faulty line: {line}")
    return inputs

# 将连续两个换行符替换为一个换行符
def remove_extra_newline(text):
    return text.replace('\n\n', '\n')

if __name__ == '__main__':
    file_path1 = '../data-convert/data/llm_dataset.jsonl'  # 模型文件的路径
    file_path2 = 'generation_instruction1.jsonl'
    history_list = extract_history_from_jsonl(file_path1)  # 包含7个子问题（从领域到动作）的input&QA对
    input_list = extract_input_from_jsonl(file_path2)
    input_n = 0  # 迭代次数，要生成问题的输入的数量
    example_n = 0  # history示例问题的维度，最大为6

    generation_QA_file_path = 'QA3.jsonl'
    generation_QA_list = extract_inputs_from_jsonl(generation_QA_file_path)


    generation(input_n, history_list, generation_QA_list, input_list)