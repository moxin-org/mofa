# Self Refine 模版

Self-Refine模式主要是通过三个环节（任务执行、结果评估和改进建议）的多轮迭代实现任务完成质量提高的目的。

[任务执行的提示词] + LLM推理 --> (结果评估的提示词) + LLM推理 --> (由评估产生改进建议的提示词) +LLM推理 --> 下一轮任务执行的提示词（迭代）。

- [MoFA Self Refine模版的实现](../../mofa/agent_templates/self_refine/README.md)

