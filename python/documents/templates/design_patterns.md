# MoFA Agent Templates and Design Patterns

[English](design_patterns.md) | [Simplified Chinese](design_patterns_cn.md)

**Design Patterns** refer to solutions proposed for common and recurring problems in software design. Developers can apply these solutions in their software to address such issues. The term was introduced into computer science by Erich Gamma and others from the field of architectural design. Their renowned book *Design Patterns: Elements of Reusable Object-Oriented Software* (by the "Gang of Four": Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides) discusses 23 object-oriented software design patterns.

Design patterns are not code that directly solves problems; they describe solutions for different scenarios. Design patterns allow unstable elements to depend on relatively stable ones, and concrete implementations to depend on abstract ones. This helps avoid tight coupling caused by immature solutions and enhances software design's adaptability to change.

Not all software patterns are design patterns. Design patterns specifically address issues at the software "design" level. Other patterns, like architectural patterns, exist as well. Algorithms, however, are not considered design patterns as they primarily solve computational rather than design issues.

MoFA recognizes that AI intelligent agents also have various design patterns to address recurring issues. Examples include:

- [Reasoner](reasoner_template.md): Custom prompts guide the reasoning process of large language models.
- [Reflection](self_refine_template.md): After a task is processed by a large language model, a reflection step provides improvement suggestions, which are then integrated into the task for better results. This can be iterative.
- ...

MoFA provides implementations of various agent design patterns in the form of templates. Developers can further customize these templates.