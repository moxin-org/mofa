# 1, Agent的三种设计
## 1.1 Dspy-Agent设计模式
我们使用 Python + DSPy 库来设计 Agent。
### DSPy-Agent 优点  
- **自定义Prompt框架**：可以轻松定制Prompt，不再需要花费大量时间进行提示工程编写和优化，只需在框架中填写需求即可。  
- **模块化功能**：支持自定义模块，可以将所需功能封装成不同模块，通过Python调用，实现不同功能组合使用。  
- **自训练优化器**：DSPy支持自训练`Optimizers`，使LLM能够更加高效地理解需求，生成更准确的结果，满足具体要求。





## 1.2 CrewAI-Agent设计模式

我们使用 Python + CrewAI 库来设计 Agent。  
  
### CrewAI-Agent 优点  
- **无缝协作**：通过模块化设计和简洁的原则，实现多个智能代理之间的无缝协作。  
- **灵活集成**：CrewAI 可以与LangChain等工具集成，为用户提供极大的灵活性。我们还可以自定义不同的Function，让CrewAI根据任务需求自动调用和实现。


## 1.3 Super-Agent 多Agent混合模式
使用多个小的Agent结合Dora流程实现Self-Refine的Agent