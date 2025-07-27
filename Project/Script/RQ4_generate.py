import json
import random
import pandas as pd


def load_jsonl(file_path):
    """ Load JSON lines from the specified file. """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = [json.loads(line.strip()) for line in file]
    return lines


def format_prompt(examples, target_input):
    """ Format the prompt with the provided examples and a target input. """
    if examples == []:
        prompt = f"你是一个领域信息抽取模型，请针对下面的工艺生产方案“{target_input}，抽取一个结构化的领域模型，包含领域、上下文、实体、实体属性、事件、实体状态、动作和动作参数等要素”。\n"
    else:
        prompt = "你是一个领域信息抽取模型，下面是一些抽取实例：\n"
        for idx, example in enumerate(examples, 1):
            input_text = example['input'].replace('\n\n', '\n')
            prompt += f"第{idx}个：\n1、工艺生产方案：{input_text}\n2、问题：{example['instruction']}\n3、答案：{example['output']}\n\n"
        prompt += f"请参考上面{len(examples)}个实例中问题与回答的内容和形式（请按照给出示例的答案的模板和形式进行回答，不要只回答一个单独的字符串），对下面的工艺生产方案进行相应信息的抽取：“{target_input}”。"
    return prompt


def generate_cot_prompt(examples, target_input):
    """Generate a CoT prompt for each entry in the dataset."""
    if examples == []:
        prompt = f"你是一个领域信息抽取模型，请一步步思考（首先识别领域场景，接着抽取领域包含的上下文，接着抽取各上下文包含的实体，接着抽取实体的属性、事件和状态，以及状态的动作、动作的参数等要素），通过逐步的信息（领域模型要素）抽取对下面的工艺生产方案构建领域模型：“{target_input}”。"
    else:
        prompt = f"你是一个领域信息抽取模型，请一步步思考，通过逐步的信息（领域模型要素）抽取来构建领域模型，以下是{len(examples)}个实例\n"
        for idx, example in enumerate(examples, 1):
            prompt += f"第{idx}个输入（工艺生产方案），其思维步骤如下："
            # Process history to form the sequential thought chain
            history = example['history']
            for his_num in range(len(history)):
                prompt += f"思维步骤{his_num+1}: {history[his_num][0]}\n回答: {history[his_num][1]}\n"
            prompt += f"最终输出（领域模型）: {example['output']}\n"
        prompt += f"请参考上面{len(examples)}个实例中思维链的思考步骤以及最终输出的内容和形式（请按照给出示例的答案的模板和形式进行回答，不要只回答一个单独的字符串），对下面的工艺生产方案进行相应信息的抽取：“{target_input}”。"
    return prompt


def remove_element(lst, element):
    return [x for x in lst if x != element]


if __name__ == '__main__':
    # Specify your .jsonl file path and output file path
    jsonl_path = 'D:\workspace\PycharmProject\LLMs\ChatGLM3\ChatGLM3\my_demo\data-convert\data\llm_dataset.jsonl'
    jsonl_data = load_jsonl(jsonl_path)

    all_prompts = []
    # Randomly select a target input first and remove it from the data
    for json_data in jsonl_data:
        prompts = {}
        target_input = json_data['input'].replace('\n\n', '\n')
        new_jsonl_data = remove_element(jsonl_data, json_data)
        # Generate prompts for different example sizes

        for num_examples in [0, 1, 2, 4]:
            if num_examples == 0:
                selected_examples = []
            else:
                selected_examples = random.sample(new_jsonl_data, k=num_examples)
            prompt_text = format_prompt(selected_examples, target_input)
            prompts[f'{num_examples}_examples'] = prompt_text
            # prompts.append({f'{num_examples}_examples', prompt_text})

        for num_examples in [0, 2]:
            if num_examples == 0:
                selected_examples = []
            else:
                selected_examples = random.sample(new_jsonl_data, k=num_examples)
            prompt_text = generate_cot_prompt(selected_examples, target_input)
            prompts[f'{num_examples}_cot_examples'] = prompt_text
            # prompts.append({f'{num_examples}_cot_examples', prompt_text})

        # print(prompts)
        all_prompts.append(prompts)
        # Create a DataFrame

    df = pd.DataFrame(all_prompts)

    print(df)
    # 存到excel中
    df.to_excel('C:\\Users\\shiha\\OneDrive - mail.sdu.edu.cn\\Desktop\\博士（论文）\\大模型工作\\评测\\Test_RQ4.xlsx', index=False)