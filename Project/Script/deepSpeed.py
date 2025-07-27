#!/usr/bin/env python
# coding: utf-8

# RLHF Optimization with DeepSpeed-Chat
# 使用 DeepSpeed-Chat 框架实现大模型的 RLHF 迭代优化

import os
import argparse
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from deepspeed.runtime.engine import DeepSpeedEngine
from deepspeed.accelerator import get_accelerator
from deepspeed import init_distributed
from deepspeed.runtime.utils import see_memory_usage
from deepspeed.runtime.config import DeepSpeedConfig


# 初始化分布式环境
def init_distributed_env():
    """初始化分布式训练环境"""
    if not torch.distributed.is_initialized():
        init_distributed()

    # 获取当前进程信息
    local_rank = int(os.getenv('LOCAL_RANK', '0'))
    world_size = int(os.getenv('WORLD_SIZE', '1'))

    # 设置设备
    get_accelerator().set_device(local_rank)
    torch.cuda.set_device(local_rank)

    return local_rank, world_size


# 配置解析器
def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='RLHF Optimization with DeepSpeed-Chat')

    # 模型参数
    parser.add_argument('--model_name', type=str, default='facebook/opt-1.3b',
                        help='预训练模型名称或路径')
    parser.add_argument('--reward_model', type=str, default='reward_model_path',
                        help='奖励模型路径')

    # 训练参数
    parser.add_argument('--num_epochs', type=int, default=3,
                        help='训练轮数')
    parser.add_argument('--batch_size', type=int, default=8,
                        help='批量大小')
    parser.add_argument('--learning_rate', type=float, default=1e-5,
                        help='学习率')
    parser.add_argument('--max_seq_len', type=int, default=512,
                        help='最大序列长度')

    # RLHF 参数
    parser.add_argument('--kl_coeff', type=float, default=0.1,
                        help='KL散度系数')
    parser.add_argument('--clip_reward', type=float, default=10.0,
                        help='奖励裁剪值')
    parser.add_argument('--gamma', type=float, default=0.99,
                        help='折扣因子')
    parser.add_argument('--entropy_coeff', type=float, default=0.01,
                        help='熵奖励系数')

    # DeepSpeed 配置
    parser.add_argument('--deepspeed_config', type=str,
                        default='ds_config.json',
                        help='DeepSpeed配置文件路径')

    # 数据路径
    parser.add_argument('--dataset_path', type=str,
                        default='rlhf_dataset.json',
                        help='训练数据集路径')
    parser.add_argument('--output_dir', type=str, default='output',
                        help='输出目录')

    return parser.parse_args()


# 数据加载器
class RLHFDataset(torch.utils.data.Dataset):
    """RLHF训练数据集"""

    def __init__(self, data_path, tokenizer, max_length=512):
        self.tokenizer = tokenizer
        self.max_length = max_length

        # 加载数据集
        with open(data_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        # 预处理数据
        self.processed_data = []
        for example in self.data:
            # 格式: {"prompt": "人类提示", "response": "模型响应", "reward": 奖励值}
            prompt = example['prompt']
            response = example['response']

            # 编码文本
            input_ids = self.tokenizer.encode(
                prompt + self.tokenizer.eos_token + response,
                max_length=max_length,
                truncation=True,
                padding='max_length',
                return_tensors='pt'
            )

            self.processed_data.append({
                'input_ids': input_ids,
                'attention_mask': (input_ids != self.tokenizer.pad_token_id).long(),
                'rewards': torch.tensor([example['reward']], dtype=torch.float32)
            })

    def __len__(self):
        return len(self.processed_data)

    def __getitem__(self, idx):
        return self.processed_data[idx]


# RLHF 训练引擎
class RLHFTrainer:
    """基于DeepSpeed的RLHF训练引擎"""

    def __init__(self, args, tokenizer, model, reward_model):
        self.args = args
        self.tokenizer = tokenizer
        self.model = model
        self.reward_model = reward_model
        self.optimizer = None
        self.lr_scheduler = None

        # 初始化DeepSpeed引擎
        self._init_deepspeed_engine()

        # 打印内存使用情况
        see_memory_usage("After initializing RLHF trainer")

    def _init_deepspeed_engine(self):
        """初始化DeepSpeed引擎"""
        # 加载DeepSpeed配置
        with open(self.args.deepspeed_config, 'r') as f:
            ds_config = json.load(f)

        # 创建模型、优化器参数
        model_parameters = filter(lambda p: p.requires_grad, self.model.parameters())

        # 初始化DeepSpeed引擎
        self.ds_engine, self.optimizer, _, self.lr_scheduler = DeepSpeedEngine(
            model=self.model,
            optimizer=None,  # DeepSpeed会自动创建优化器
            model_parameters=model_parameters,
            config=ds_config,
            lr_scheduler=None
        )

        # 冻结奖励模型参数
        for param in self.reward_model.parameters():
            param.requires_grad = False

    def compute_rewards(self, input_ids, attention_mask, generated_responses):
        """
        计算奖励值
        :param input_ids: 输入ID
        :param attention_mask: 注意力掩码
        :param generated_responses: 生成的响应
        :return: 奖励值
        """
        # 使用奖励模型计算奖励
        with torch.no_grad():
            # 将生成响应与输入拼接
            full_inputs = torch.cat([input_ids, generated_responses], dim=1)
            full_mask = torch.cat([attention_mask, torch.ones_like(generated_responses)], dim=1)

            # 计算奖励
            rewards = self.reward_model(
                input_ids=full_inputs,
                attention_mask=full_mask
            ).logits.squeeze(-1)

            # 裁剪奖励值
            rewards = torch.clamp(rewards, -self.args.clip_reward, self.args.clip_reward)

            return rewards

    def train_one_epoch(self, dataloader, epoch):
        """训练一个epoch"""
        self.ds_engine.train()
        total_loss = 0.0

        for step, batch in enumerate(dataloader):
            # 将数据移动到设备
            input_ids = batch['input_ids'].to(self.ds_engine.device)
            attention_mask = batch['attention_mask'].to(self.ds_engine.device)
            rewards = batch['rewards'].to(self.ds_engine.device)

            # 前向传播 - 生成响应
            with torch.no_grad():
                # 获取参考模型的logits（用于KL散度计算）
                reference_logits = self.model(
                    input_ids=input_ids,
                    attention_mask=attention_mask
                ).logits

                # 生成响应
                generated_responses = self.model.generate(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    max_length=self.args.max_seq_len,
                    do_sample=True,
                    top_k=50,
                    top_p=0.95
                )

            # 计算奖励
            gen_rewards = self.compute_rewards(input_ids, attention_mask, generated_responses)

            # 结合外部奖励和生成奖励
            combined_rewards = rewards + gen_rewards

            # 策略梯度训练
            self.ds_engine.zero_grad()

            # 当前策略的logits
            current_logits = self.model(
                input_ids=input_ids,
                attention_mask=attention_mask
            ).logits

            # 计算KL散度惩罚 (当前策略 vs 参考策略)
            kl_div = torch.nn.functional.kl_div(
                torch.nn.functional.log_softmax(current_logits, dim=-1),
                torch.nn.functional.log_softmax(reference_logits, dim=-1),
                reduction='batchmean',
                log_target=True
            )

            # 计算熵奖励 (鼓励探索)
            entropy = -torch.sum(
                torch.softmax(current_logits, dim=-1) *
                torch.log_softmax(current_logits, dim=-1),
                dim=-1
            ).mean()

            # 计算损失
            loss = -combined_rewards.mean() + self.args.kl_coeff * kl_div - self.args.entropy_coeff * entropy

            # 反向传播
            self.ds_engine.backward(loss)
            self.ds_engine.step()

            total_loss += loss.item()

            # 每100步打印一次日志
            if step % 100 == 0:
                print(f"Epoch {epoch}, Step {step}/{len(dataloader)}, Loss: {loss.item():.4f}, "
                      f"Reward: {combined_rewards.mean().item():.4f}, "
                      f"KL Div: {kl_div.item():.4f}, Entropy: {entropy.item():.4f}")

        avg_loss = total_loss / len(dataloader)
        print(f"Epoch {epoch} finished. Average Loss: {avg_loss:.4f}")
        return avg_loss

    def save_checkpoint(self, epoch, output_dir):
        """保存模型检查点"""
        checkpoint_dir = os.path.join(output_dir, f"epoch_{epoch}")
        os.makedirs(checkpoint_dir, exist_ok=True)

        # 保存模型
        self.ds_engine.save_checkpoint(checkpoint_dir)

        # 保存配置
        config = {
            'epoch': epoch,
            'model_config': self.model.config.to_dict(),
            'train_args': vars(self.args)
        }
        with open(os.path.join(checkpoint_dir, 'config.json'), 'w') as f:
            json.dump(config, f, indent=2)

        print(f"Checkpoint saved to {checkpoint_dir}")


# 主训练函数
def main():
    # 解析参数
    args = parse_arguments()

    # 初始化分布式环境
    local_rank, world_size = init_distributed_env()

    # 创建输出目录
    if local_rank == 0:
        os.makedirs(args.output_dir, exist_ok=True)

    # 加载tokenizer
    tokenizer = AutoTokenizer.from_pretrained(args.model_name)
    tokenizer.pad_token = tokenizer.eos_token  # 设置填充token

    # 加载模型
    model = AutoModelForCausalLM.from_pretrained(args.model_name)

    # 加载奖励模型
    reward_model = AutoModelForSequenceClassification.from_pretrained(args.reward_model)

    # 创建数据集
    dataset = RLHFDataset(args.dataset_path, tokenizer, max_length=args.max_seq_len)

    # 创建数据加载器
    sampler = torch.utils.data.distributed.DistributedSampler(dataset)
    dataloader = torch.utils.data.DataLoader(
        dataset,
        batch_size=args.batch_size,
        sampler=sampler,
        num_workers=4,
        pin_memory=True
    )

    # 创建RLHF训练器
    trainer = RLHFTrainer(args, tokenizer, model, reward_model)

    # 训练循环
    for epoch in range(args.num_epochs):
        # 设置epoch
        dataloader.sampler.set_epoch(epoch)

        # 训练一个epoch
        avg_loss = trainer.train_one_epoch(dataloader, epoch)

        # 保存检查点 (仅主进程)
        if local_rank == 0:
            trainer.save_checkpoint(epoch, args.output_dir)

    print("RLHF training completed!")


if __name__ == "__main__":
    main()