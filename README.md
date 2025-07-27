Qwen2.5-14B-lora-80-modeling/Qwen2.5-32B--lora-300-modeling：两个可供测试的模型权重文件

Meta-model：元模型的相关文件

Project：微调和测试所用的数据；数据处理和测试过程中的脚本文件

- ##### 微调环境配置

  | 环境配置项      | 环境配置         |
  | --------------- | ---------------- |
  | 硬件环境        | Atlas800T A2     |
  | 宿主机OS        | kylinSP3         |
  | 容器            | ubuntu22.04      |
  | CANN            | 8.0.RC2.alpha002 |
  | Ascend 驱动版本 | 24.1.rc1         |
  | torch           | 2.2.0            |
  | torch-npu       | 2.2.0            |
  | deepspeed       | 0.14.4           |
  | LLaMA-Factory   | 0.8.3            |
  | Python          | 3.9.18           |

- ![image]910.png)

- ##### 训练参数

```
model_name_or_path: qwen/Qwen2.5-14B-Instruct
### method
stage: sft
do_train: true
finetuning_type: full
# lora_target: all
deepspeed: examples/deepspeed/ds_z3_config.json

### dataset
dataset: yi
template: qwen
cutoff_len: 1024
max_samples: 1000
overwrite_cache: true
preprocessing_num_workers: 16

### output
output_dir: output/Qwen2.5-14B-Instruct
logging_steps: 10
save_steps: 500
plot_loss: true
overwrite_output_dir: true

### train
per_device_train_batch_size: 1
auto_find_batch_size: true
gradient_accumulation_steps: 2
learning_rate: 1.0e-4
num_train_epochs: 80.0
lr_scheduler_type: cosine
warmup_ratio: 0.1
fp16: true
ddp_timeout: 180000000

### eval
val_size: 0.1
per_device_eval_batch_size: 1
eval_strategy: steps
eval_steps: 500
```

- ##### 其他依赖：

| Package & Version                 | Package & Version                        | Package & Version                     | Package & Version                        |
| :-------------------------------- | :--------------------------------------- | :------------------------------------ | :--------------------------------------- |
| **accelerate**: 0.31.0            | **acctransformer**: 1.0.0                | **addict**: 2.4.0                     | **aiofiles**: 23.2.1                     |
| **aiohttp**: 3.9.5                | **aiosignal**: 1.3.1                     | **albumentations**: 1.3.1             | **aliyun-python-sdk-core**: 2.15.1       |
| **aliyun-python-sdk-kms**: 2.16.3 | **altair**: 5.1.2                        | **annotated-types**: 0.7.0            | **antlr4-python3-runtime**: 4.9.3        |
| **anyio**: 3.7.1                  | **APScheduler**: 3.9.1                   | **arrow**: 1.2.3                      | **ascendebug**: 0.1.0                    |
| **asttokens**: 2.4.1              | **astunparse**: 1.6.3                    | **async-timeout**: 4.0.3              | **attrs**: 23.1.0                        |
| **auto-tune**: 0.1.0              | **av**: 14.3.0                           | **backcall**: 0.2.0                   | **backports.functools-lru-cache**: 1.6.5 |
| **backports.zoneinfo**: 0.2.1     | **binaryornot**: 0.4.4                   | **certifi**: 2023.7.22                | **cffi**: 1.15.1                         |
| **chardet**: 5.2.0                | **charset-normalizer**: 3.3.2            | **click**: 8.1.7                      | **cloudpickle**: 3.0.0                   |
| **colorama**: 0.4.4               | **comm**: 0.1.4                          | **configparser**: 5.2.0               | **contourpy**: 1.1.1                     |
| **cookiecutter**: 2.3.0           | **crcmod**: 1.7                          | **cryptography**: 3.4.7               | **cycler**: 0.12.1                       |
| **dataflow**: 0.0.1               | **datasets**: 2.18.0                     | **debugpy**: 1.8.0                    | **decorator**: 5.1.1                     |
| **deepspeed**: 0.14.4             | **defusedxml**: 0.7.1                    | **dill**: 0.3.8                       | **docstring_parser**: 0.16               |
| **einops**: 0.7.0                 | **ephemeral-port-reserve**: 1.1.4        | **esdk-obs-python**: 3.21.4           | **eval_type_backport**: 0.2.0            |
| **exceptiongroup**: 1.1.3         | **executing**: 2.0.1                     | **fastapi**: 0.104.1                  | **ffmpy**: 0.3.1                         |
| **filelock**: 3.13.1              | **fire**: 0.6.0                          | **fonttools**: 4.43.1                 | **frozenlist**: 1.4.1                    |
| **fsspec**: 2023.10.0             | **ftfy**: 6.1.1                          | **gast**: 0.5.5                       | **gradio**: 4.36.1                       |
| **gradio_client**: 1.0.1          | **h11**: 0.14.0                          | **hccl**: 0.1.0                       | **hccl-parser**: 0.1                     |
| **hjson**: 3.1.0                  | **httpcore**: 0.18.0                     | **httpx**: 0.25.0                     | **huaweicloudsdkcore**: 3.1.8            |
| **huaweicloudsdkcsms**: 3.1.8     | **huggingface-hub**: 0.23.4              | **idna**: 3.4                         | **imageio**: 2.31.6                      |
| **imagesize**: 1.4.1              | **importlib-metadata**: 6.8.0            | **importlib-resources**: 6.1.0        | **ipykernel**: 6.26.0                    |
| **ipython**: 8.16.1               | **jedi**: 0.19.1                         | **jieba**: 0.42.1                     | **Jinja2**: 3.1.2                        |
| **jmespath**: 0.10.0              | **joblib**: 1.3.2                        | **jsonschema**: 4.19.2                | **jsonschema-specifications**: 2023.7.1  |
| **jupyter_client**: 8.5.0         | **jupyter_core**: 5.5.0                  | **kiwisolver**: 1.4.5                 | **latex2mathml**: 3.76.0                 |
| **lazy-import**: 0.2.2            | **lazy_loader**: 0.3                     | **llamafactory**: 0.9.1.dev0          | **llm-engine**: 0.0.1                    |
| **lxml**: 4.9.3                   | **ma-cau**: 1.1.4.9                      | **ma-cau-adapter**: 1.1.3             | **ma-cli**: 1.2.1                        |
| **Markdown**: 3.5.1               | **markdown-it-py**: 2.2.0                | **MarkupSafe**: 2.1.3                 | **matplotlib**: 3.8.0                    |
| **matplotlib-inline**: 0.1.6      | **mdtex2html**: 1.2.0                    | **mdurl**: 0.1.2                      | **metrics**: 0.3.3                       |
| **mindpet**: 1.0.3                | **mindspore**: 2.2.13                    | **mindspore-lite**: 2.2.13            | **mock**: 4.0.3                          |
| **modelarts**: 1.4.18             | **modelscope**: 1.15.0                   | **moxing-framework**: 2.1.16.2ae09d45 | **mpmath**: 1.3.0                        |
| **msadvisor**: 1.0.0              | **multidict**: 6.0.5                     | **multiprocess**: 0.70.16             | **nest-asyncio**: 1.5.8                  |
| **networkx**: 3.2.1               | **ninja**: 1.11.1.1                      | **nltk**: 3.8.1                       | **numpy**: 1.26.1                        |
| **nvidia-ml-py**: 12.555.43       | **omegaconf**: 2.3.0                     | **op-compile-tool**: 0.1.0            | **op-gen**: 0.1                          |
| **op-test-frame**: 0.1            | **opc-tool**: 0.1.0                      | **opencv-python**: 4.8.1.78           | **opencv-python-headless**: 4.8.1.78     |
| **orjson**: 3.9.10                | **oss2**: 2.18.6                         | **packaging**: 23.2                   | **pandas**: 2.1.2                        |
| **parso**: 0.8.3                  | **pathlib2**: 2.3.7.post1                | **pathspec**: 0.5.5                   | **peft**: 0.11.1                         |
| **pexpect**: 4.8.0                | **pickleshare**: 0.7.5                   | **Pillow**: 9.0.1                     | **pip**: 23.3.1                          |
| **platformdirs**: 3.11.0          | **prettytable**: 3.5.0                   | **prompt-toolkit**: 3.0.39            | **protobuf**: 3.20.3                     |
| **psutil**: 5.9.5                 | **ptyprocess**: 0.7.0                    | **pure-eval**: 0.2.2                  | **py-cpuinfo**: 9.0.0                    |
| **pyarrow**: 16.1.0               | **pyarrow-hotfix**: 0.6                  | **pycocotools**: 2.0.6                | **pycparser**: 2.21                      |
| **pycryptodome**: 3.20.0          | **pydantic**: 2.7.4                      | **pydantic_core**: 2.18.4             | **pydub**: 0.25.1                        |
| **Pygments**: 2.18.0              | **pyparsing**: 3.1.1                     | **python-dateutil**: 2.8.2            | **python-multipart**: 0.0.9              |
| **python-slugify**: 8.0.1         | **pytz**: 2023.3.post1                   | **PyYAML**: 6.0.1                     | **pyzmq**: 25.1.1                        |
| **qudida**: 0.0.4                 | **rdkit**: 2023.9.2                      | **referencing**: 0.30.2               | **regex**: 2023.10.3                     |
| **requests**: 2.32.3              | **requests-futures**: 1.0.0              | **requests-toolbelt**: 0.10.1         | **rich**: 13.5.2                         |
| **rouge-chinese**: 1.0.3          | **rpds-py**: 0.10.6                      | **ruff**: 0.4.9                       | **safetensors**: 0.4.3                   |
| **schedule-search**: 0.0.1        | **scikit-image**: 0.22.0                 | **scikit-learn**: 1.3.2               | **scipy**: 1.11.3                        |
| **semantic-version**: 2.10.0      | **sentencepiece**: 0.1.99                | **setuptools**: 68.2.2                | **shellingham**: 1.5.4                   |
| **shtab**: 1.7.1                  | **simplejson**: 3.17.0                   | **six**: 1.16.0                       | **sniffio**: 1.3.0                       |
| **sortedcontainers**: 2.4.0       | **sse-starlette**: 2.1.2                 | **stack-data**: 0.6.2                 | **starlette**: 0.27.0                    |
| **sympy**: 1.12                   | **synr**: 0.5.0                          | **tabulate**: 0.8.9                   | **te**: 0.4.0                            |
| **tenacity**: 8.1.0               | **termcolor**: 2.4.0                     | **terminaltables**: 3.1.10            | **text-unidecode**: 1.3                  |
| **threadpoolctl**: 3.2.0          | **tifffile**: 2023.9.26                  | **tiktoken**: 0.7.0                   | **tokenizers**: 0.19.1                   |
| **tomli**: 2.0.1                  | **tomlkit**: 0.12.0                      | **toolz**: 0.12.0                     | **torch**: 2.2.0                         |
| **torch-npu**: 2.2.0              | **tornado**: 6.3.3                       | **tqdm**: 4.66.4                      | **traitlets**: 5.13.0                    |
| **transformers**: 4.42.3          | **transformers-stream-generator**: 0.0.5 | **trl**: 0.9.4                        | **typer**: 0.12.3                        |
| **typing_extensions**: 4.8.0      | **tyro**: 0.8.4                          | **tzdata**: 2023.3                    | **tzlocal**: 5.0.1                       |
| **urllib3**: 2.0.7                | **uvicorn**: 0.23.2                      | **wcwidth**: 0.2.9                    | **websockets**: 11.0.3                   |
| **wheel**: 0.41.3                 | **xxhash**: 3.4.1                        | **yapf**: 0.40.2                      | **yarl**: 1.9.4                          |
| **zipp**: 3.17.0                  |                                          |                                       |                                          |
