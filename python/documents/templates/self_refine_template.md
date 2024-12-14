# Self Refine Template

[English](self_refine_template_patterns.md) | [Simplified Chinese](self_refine_template_cn.md)

The Self-Refine pattern primarily improves task completion quality through multiple iterative rounds involving three steps: task execution, result evaluation, and improvement suggestions.

[Task Execution Prompt] + LLM Reasoning --> (Result Evaluation Prompt) + LLM Reasoning --> (Improvement Suggestions Prompt Generated from Evaluation) + LLM Reasoning --> Next Round of Task Execution Prompt (Iteration).

- Implementation of MoFA Self-Refine Template
