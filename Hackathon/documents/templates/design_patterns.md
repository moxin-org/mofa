# MoFA智能体模版和设计模式

**设计模式**（Design Pattern）是是对软件设计中普遍存在和反复出现的各种问题，所提出的解决方案。开发者可以使用这些方案在他们的软件中去解决这些问题。这个术语是由埃里希·伽玛（Erich Gamma）等人从建筑设计领域引入到计算机科学的。他们（Gangs of Four: Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides)写了一本著名的书籍《设计模式：可复用面向对象软件的基础》（Design Patterns: Elements of Reusable Object-Oriented Software），讨论了23种面向对象软件的设计模式。

设计模式并不是直接解决问题的代码，而是描述在各种不同情况下，要怎么解决问题的一种方案。设计模式能使不稳定依赖于相对稳定、具体依赖于相对抽象，避免不成熟的方案会引起麻烦的紧耦合，以增强软件设计面对并适应变化的能力。

并非所有的软件模式都是设计模式，设计模式特指软件“设计”层次上的问题。还有其他非设计模式的模式，如架构模式。同时，算法也不能算是一种设计模式，因为算法主要是用来解决计算上的问题，而非设计上的问题。

MoFA认为，AI智能体的设计也有多种模式。以解决普遍存在和反复出现的各种问题。比如，

- [Reasoner](reasoner_template.md)：通过定制提示为大语言模型推理提供方向。
- [Reflection](self_refine_template.md): 用户的任务在经过大语言模型推理以后，再由大语言模型推理提供反思，并给出改进建议，进一步再将改进建议集成到用户的任务再次推理，获得更好的结果。并可以迭代。
- ...

等。

MoFA以Template的方式提供多种Agent Design Pattern的实现。开发者们可以使用这些Templates，进行进一步定制。