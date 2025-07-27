---
license: other
base_model: /home/data/LLMs/qwen2.5-32B-Instruct
tags:
- llama-factory
- lora
- generated_from_trainer
metrics:
- accuracy
library_name: peft
model-index:
- name: Qwen2.5-32B-Instruct-lora-300
  results: []
---

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->

# Qwen2.5-32B-Instruct-lora-300

This model is a fine-tuned version of [/home/data/LLMs/qwen2.5-32B-Instruct](https://huggingface.co//home/data/LLMs/qwen2.5-32B-Instruct) on the identity dataset.
It achieves the following results on the evaluation set:
- Loss: 1.6365
- Accuracy: 0.7400

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
- train_batch_size: 4
- eval_batch_size: 1
- seed: 42
- distributed_type: multi-GPU
- num_devices: 16
- gradient_accumulation_steps: 8
- total_train_batch_size: 512
- total_eval_batch_size: 16
- optimizer: Adam with betas=(0.9,0.999) and epsilon=1e-08
- lr_scheduler_type: cosine
- lr_scheduler_warmup_ratio: 0.1
- num_epochs: 300.0
- mixed_precision_training: Native AMP

### Training results



### Framework versions

- PEFT 0.13.2
- Transformers 4.43.3
- Pytorch 2.2.0
- Datasets 2.19.1
- Tokenizers 0.19.1