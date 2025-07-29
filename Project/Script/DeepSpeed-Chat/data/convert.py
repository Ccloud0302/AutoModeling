import os
import json
import random
import pandas as pd
from collections import defaultdict
import argparse
import logging
import time
from tqdm import tqdm

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def process_excel_to_deepspeed(input_path, output_dir, train_ratio=0.9):
    """处理Excel文件，转换为DeepSpeed-Chat所需格式"""
    # 读取Excel文件
    try:
        logger.info(f"开始读取Excel文件: {input_path}")
        start_time = time.time()
        xls = pd.ExcelFile(input_path)
        load_time = time.time() - start_time
        logger.info(f"Excel文件读取完成，耗时: {load_time:.2f}秒，包含工作表: {xls.sheet_names}")
    except Exception as e:
        logger.error(f"读取Excel文件失败: {e}")
        return None
    
    all_data = []
    sheet_stats = {}
    valid_x_types = {'ST', 'H'}
    
    # 处理每个工作表
    for sheet_name in xls.sheet_names:
        # 解析工作表名获取x_type和n_value - 适配 "H_Chosen_1" 格式
        if not sheet_name.startswith(('H_Chosen_', 'ST_Chosen_')):
            logger.warning(f"跳过不符合格式的工作表名: {sheet_name}")
            continue
            
        # 提取x_type和n_value
        x_type = sheet_name.split('_')[0]
        try:
            # 从 "H_Chosen_1" 提取数字部分
            n_value = int(sheet_name.split('_')[-1])
            if n_value < 1 or n_value > 6:
                logger.warning(f"跳过n值超出范围的工作表: {sheet_name}")
                continue
        except (ValueError, IndexError):
            logger.warning(f"无法解析n值: {sheet_name}")
            continue
        
        logger.info(f"处理工作表: {sheet_name} (x_type={x_type}, n_value={n_value})")
        
        try:
            # 读取工作表数据
            df = pd.read_excel(input_path, sheet_name=sheet_name)
            logger.info(f"工作表 '{sheet_name}' 包含 {len(df)} 行数据")
            
            sheet_count = 0
            skipped_count = 0
            
            # 处理每行数据
            for idx, row in tqdm(df.iterrows(), total=len(df), desc=f"处理 {sheet_name}"):
                # 处理可能的NaN值
                instruction = str(row.get('instruction', '')).strip()
                input_text = str(row.get('input', '')).strip()
                
                # 获取chosen和rejected响应 - 适配大小写不敏感的列名
                chosen_col = None
                rejected_col = None
                
                # 查找匹配的列名（大小写不敏感）
                for col in df.columns:
                    col_lower = col.lower()
                    if f'chosen_{n_value}'.lower() in col_lower:
                        chosen_col = col
                    if f'rejected_{n_value}'.lower() in col_lower:
                        rejected_col = col
                
                if not chosen_col or not rejected_col:
                    logger.warning(f"在工作表 '{sheet_name}' 中找不到匹配的列名")
                    skipped_count += len(df)
                    break
                
                chosen = str(row.get(chosen_col, '')).strip()
                rejected = str(row.get(rejected_col, '')).strip()
                
                # 验证必要字段
                if not instruction:
                    skipped_count += 1
                    continue
                    
                if not chosen or not rejected:
                    skipped_count += 1
                    continue
                
                # 构造prompt
                prompt = instruction
                if input_text:
                    prompt += f"\n{input_text}"
                    
                all_data.append({
                    "x_type": x_type,
                    "n_value": n_value,
                    "sheet": sheet_name,
                    "prompt": prompt,
                    "chosen": chosen,
                    "rejected": rejected
                })
                sheet_count += 1
            
            sheet_stats[sheet_name] = {
                "total": len(df),
                "processed": sheet_count,
                "skipped": skipped_count
            }
            
            logger.info(f"工作表 '{sheet_name}' 处理完成: 有效 {sheet_count} 条, 跳过 {skipped_count} 条")
        
        except Exception as e:
            logger.error(f"处理工作表 '{sheet_name}' 时出错: {e}")
            continue
    
    if not all_data:
        logger.error("未找到有效数据，请检查Excel文件格式")
        return None
    
    # 划分训练/验证集
    train_data, eval_data = split_data(all_data, train_ratio)
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 保存数据集
    save_datasets(train_data, eval_data, all_data, output_dir)
    
    # 返回统计信息
    return {
        "total_samples": len(all_data),
        "train_samples": len(train_data),
        "eval_samples": len(eval_data),
        "sheet_stats": sheet_stats,
        "x_type_distribution": {x: sum(1 for d in all_data if d['x_type'] == x) for x in valid_x_types}
    }

def split_data(all_data, train_ratio):
    """按x_type分组划分训练/验证集"""
    grouped_data = defaultdict(list)
    for item in all_data:
        grouped_data[item['x_type']].append(item)
    
    train_data, eval_data = [], []
    
    for x_type, items in grouped_data.items():
        random.shuffle(items)
        split_idx = int(len(items) * train_ratio)
        train_data.extend(items[:split_idx])
        eval_data.extend(items[split_idx:])
    
    return train_data, eval_data

def save_datasets(train_data, eval_data, all_data, output_dir):
    """保存各种格式的数据集"""
    # 1. 保存奖励模型数据
    save_jsonl([{"prompt": d["prompt"], "chosen": d["chosen"], "rejected": d["rejected"]} 
               for d in train_data], os.path.join(output_dir, "rm_train.jsonl"))
    save_jsonl([{"prompt": d["prompt"], "chosen": d["chosen"], "rejected": d["rejected"]} 
               for d in eval_data], os.path.join(output_dir, "rm_eval.jsonl"))
    
    # 2. 保存SFT数据
    save_jsonl([{"prompt": d["prompt"], "response": d["chosen"]} 
               for d in all_data], os.path.join(output_dir, "sft_data.jsonl"))
    
    # 3. 保存PPO提示数据（去重）
    unique_prompts = set(d["prompt"] for d in all_data)
    save_jsonl([{"prompt": p} for p in unique_prompts], 
              os.path.join(output_dir, "ppo_prompts.jsonl"))
    
    # 4. 保存完整数据集（含元数据）
    save_jsonl(all_data, os.path.join(output_dir, "full_dataset.jsonl"))
    
    logger.info(f"数据集已保存到: {output_dir}")

def save_jsonl(data, file_path):
    """保存JSONL格式文件"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        logger.info(f"已保存: {file_path} ({len(data)} 条记录)")
    except Exception as e:
        logger.error(f"保存文件 {file_path} 失败: {e}")

def main():
    """主函数：解析命令行参数并处理数据"""
    parser = argparse.ArgumentParser(description='Excel转DeepSpeed-Chat格式工具')
    parser.add_argument('--input', type=str, required=True, 
                       help='输入的Excel文件路径')
    parser.add_argument('--output', type=str, default='deepspeed_data',
                       help='输出目录路径 (默认: deepspeed_data)')
    parser.add_argument('--train_ratio', type=float, default=0.9,
                       help='训练集比例 (默认: 0.9)')
    parser.add_argument('--log_level', type=str, default='INFO',
                       choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       help='日志级别 (默认: INFO)')
    
    args = parser.parse_args()
    
    # 设置日志级别
    logger.setLevel(args.log_level)
    
    logger.info(f"开始处理Excel文件: {args.input}")
    start_time = time.time()
    
    stats = process_excel_to_deepspeed(
        args.input, 
        args.output,
        args.train_ratio
    )
    
    if not stats:
        logger.error("处理失败，无有效数据生成")
        return
    
    total_time = time.time() - start_time
    
    logger.info("\n处理完成! 统计信息:")
    logger.info(f"总样本数: {stats['total_samples']}")
    logger.info(f"训练样本数: {stats['train_samples']} ({stats['train_samples']/stats['total_samples']:.1%})")
    logger.info(f"验证样本数: {stats['eval_samples']} ({stats['eval_samples']/stats['total_samples']:.1%})")
    
    logger.info("\nX类型分布:")
    for x_type, count in stats['x_type_distribution'].items():
        logger.info(f"  {x_type}: {count} 条数据 ({count/stats['total_samples']:.1%})")
    
    logger.info("\n工作表统计:")
    for sheet, info in stats['sheet_stats'].items():
        logger.info(f"  {sheet}: 共 {info['total']} 行, 有效 {info['processed']} 条, 跳过 {info['skipped']} 条")
    
    logger.info("\n输出文件:")
    output_files = [f for f in os.listdir(args.output) if f.endswith('.jsonl')]
    for file in output_files:
        file_path = os.path.join(args.output, file)
        size_kb = os.path.getsize(file_path) // 1024
        logger.info(f"  - {file} ({size_kb} KB)")
    
    logger.info(f"\n总耗时: {total_time:.2f} 秒")

if __name__ == "__main__":
    main()