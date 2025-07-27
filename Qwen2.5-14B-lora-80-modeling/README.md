---
base_model: LLMs/Qwen2.5-14B-Instruct
library_name: peft
license: other
tags:
- llama-factory
- lora
- generated_from_trainer
model-index:
- name: qwen2.5-14B-lora-80
  results: []
---

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->

# qwen2.5-14B-lora-80

This model is a fine-tuned version of [LLMs/Qwen2.5-14B-Instruct](https://huggingface.co/LLMs/Qwen2.5-14B-Instruct) on the modeling dataset.
It achieves the following results on the evaluation set:
- Loss: 1.0912

## Model description

More information needed

## Intended uses & limitations

More information needed

## Training and evaluation data

More information needed

## Training procedure

### Training hyperparameters

The following hyperparameters were used during training:
- learning_rate: 0.0001
- train_batch_size: 1
- eval_batch_size: 1
- seed: 42
- distributed_type: multi-GPU
- num_devices: 8
- gradient_accumulation_steps: 2
- total_train_batch_size: 16
- total_eval_batch_size: 8
- optimizer: Adam with betas=(0.9,0.999) and epsilon=1e-08
- lr_scheduler_type: cosine
- lr_scheduler_warmup_ratio: 0.1
- num_epochs: 80
- mixed_precision_training: Native AMP

### Training results

| Training Loss | Epoch   | Step | Validation Loss |
|:-------------:|:-------:|:----:|:---------------:|
| 0.1969        | 8.8496  | 500  | 0.3472          |
| 0.0123        | 17.6991 | 1000 | 0.7114          |
| 0.0035        | 26.5487 | 1500 | 0.8694          |
| 0.0009        | 35.3982 | 2000 | 0.8755          |
| 0.0001        | 44.2478 | 2500 | 1.0252          |
| 0.0001        | 53.0973 | 3000 | 1.0628          |
| 0.0001        | 61.9469 | 3500 | 1.0821          |
| 0.0001        | 70.7965 | 4000 | 1.0903          |


### Framework versions

- PEFT 0.11.1
- Transformers 4.42.3
- Pytorch 2.2.0
- Datasets 2.18.0
- Tokenizers 0.19.1