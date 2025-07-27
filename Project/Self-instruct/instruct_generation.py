import json

import re
from openpyxl import load_workbook
import random
from zhipuai import ZhipuAI
import re
from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.bleu_score import SmoothingFunction
import jieba


# 计算rouge_L
def calculate_rouge_l(reference, hypothesis):
    reference_tokens = list(jieba.cut(reference))
    hypothesis_tokens = list(jieba.cut(hypothesis))
    smoothing_function = SmoothingFunction().method7
    rouge_l_score = sentence_bleu([reference_tokens], hypothesis_tokens, smoothing_function=smoothing_function)
    return rouge_l_score


# 将模型的回答转换成问题的列表
def extract_questions(text):
    # 使用正则表达式分割文本
    schemes = re.split(r'\s*工艺生产方案\d+[、|：]', text)
    questions = []
    for scheme in schemes:
        if scheme.strip():
            scheme_new = remove_extra_newline(scheme.strip())
            questions.append(scheme_new)
    return questions

# 提取模型文件中的input，存到list中
def extract_inputs_from_jsonl(file_path):
    inputs = []  # 创建一个空列表来存放input字段的内容
    with open(file_path, 'r',  encoding="UTF-8") as file:
        for line in file:
            try:
                json_data = json.loads(line)  # 解析每一行为JSON
                input_new = remove_extra_newline(json_data['input'])
                inputs.append(input_new)  # 提取input字段并添加到列表中
            except json.JSONDecodeError as e:
                # 打印错误信息和出错的行
                print(f"Error parsing JSON: {e}")
                print(f"Faulty line: {line}")
    return inputs


# 将连续两个换行符替换为一个换行符
def remove_extra_newline(text):
    return text.replace('\n\n', '\n')

def process_list():
    # 读取文件内容
    with open('工艺场景.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 初始化变量
    techniques_list = []
    current_domain = ""

    # 正则表达式，用于识别包含冒号的行，视为领域开始
    domain_pattern = re.compile(r'.*：$')

    # 遍历文件中的每一行
    for line in lines:
        # 去除每行的前后空格
        cleaned_line = line.strip()
        # 检查是否是领域定义行
        if domain_pattern.match(cleaned_line):
            current_domain = cleaned_line[:-1]  # 移除末尾的冒号并保存当前领域
        else:
            # 如果不是领域定义行，且当前领域已经设定，那么这是一个工艺
            if current_domain and cleaned_line:
                techniques_list.append(f"{current_domain}：{cleaned_line}")

    return techniques_list


def generation_prompt(input_list, processList, n):
    generation_instructions_file_path = 'generation_instruction.jsonl'
    generation_instructions_list = extract_inputs_from_jsonl(generation_instructions_file_path)

    # 随机从种子指令和生成指令中取5条
    seed_instructions = random.sample(input_list, 6)
    if len(generation_instructions_list) > 10:
        generation_instructions = random.sample(generation_instructions_list, 2)
    # print(random_list)
    # 建立模版
    prompt = "你是一个离散制造工艺生成模型，下面是一些领域场景的工艺生产方案，生产方案中描述了工艺、工艺的每一道工序，每个工序需要哪些设备，设备由什么事件驱动，设备有哪些属性，设备有哪些状态，在各种状态下进行哪些具体操作及操作参数：\n"
    for index, instruction in enumerate(seed_instructions):
        prompt += f"工艺生产方案{str(index + 1)}、{instruction.strip()}\n"
    if len(generation_instructions_list) > 10:
        for index, instruction in enumerate(generation_instructions):
            prompt += f"工艺生产方案{str(index + 7)}、{instruction.strip()}\n"
    prompt += "请参考上面文本的每个工艺生产方案的内容和形式，再生成1个离散制造工艺的同等详细程度的工艺生产方案的本文（形式不要一模一样，每个工艺的工序、设备等要素要根据自己的真实场景情况来生成，不要每个都一样，不要每个都像模板生成的！！！！）。这个离散制造工艺分别为：{processList}，请以一整段文字给出，每一个都以“工艺生产方案n”开头（n为序号）。".format(processList=processList[n: n+1])
    n += 1
    return prompt, generation_instructions_list, n

def generation(prompt, generation_instructions_list, file):
    # 向GLM4提问并返回答案
    client = ZhipuAI(api_key="8363a2361547c410fb4be690d3436640.CrZUvRtrTAZIbPvC")  # 填写你自己的APIKey
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=[
            {"role": "user",
             "content": prompt}
        ],
    )
    print(response.choices[0].message.content)
    # file.write(response.choices[0].message.content+'\n')

    # 提取问题
    questions = extract_questions(response.choices[0].message.content)
    print(questions)
    for i, question in enumerate(questions, start=1):
        print("question")
        print(f"{question}")

    # 指令存储到文件
    for question in questions:
        max_rouge = 0
        if generation_instructions_list:
            for generation_instruction in generation_instructions_list:
                rouge_l = calculate_rouge_l(question, generation_instruction)
                if rouge_l > max_rouge:
                    max_rouge = rouge_l
        if max_rouge < 0.7:
            # 创建字典并将其转换为JSON字符串
            json_line = json.dumps({'input': question}, ensure_ascii=False)
            print(f"录入：{question}" + "\n")
            file.write(json_line + '\n')


if __name__ == '__main__':
    file = open("generation_instruction.jsonl", 'a', encoding="UTF-8")
    file_path = '../data-convert/data/llm_dataset.jsonl'  # 模型文件的路径

    input_list = extract_inputs_from_jsonl(file_path)

    processList = process_list()

    n = 0
    while(n < len(processList)):  # n < len(input_list)
        prompt, generation_instructions_list, n = generation_prompt(input_list, processList, n)
        generation(prompt, generation_instructions_list, file)
