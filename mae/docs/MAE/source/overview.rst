Moxin App Engine - Overview
===========================

.. attention:: Work In Progress
  
MAE Introduction 
----------------
Defintions
^^^^^^^^^^
**Moxin**

Moxin is an AI LLM client written in Rust to demonstrate the functionality of the Robius, a framework for multi-platform application development in Rust. `Moxin's website <https://github.com/moxin-org>`_

**Moxin App**

A Moxin App is an AI agentic application powered by Moxin framework. 

**Moxin App Engine**

Moxin App Engine provides (1) an low-code environment to construct Moxin Apps, and (2) the run-time environment to run Moxin Apps. 

MAE Feature Highlight 
^^^^^^^^^^^^^^^^^^^^^
- Various Agentic Design Patterns

- Unified Memory, Planning, Tooling, RAG support

- Super Agent Composition

MAE Agentic Design Patterns
---------------------------

.. list-table:: 
   :widths: 20 40 40
   :header-rows: 1

   * - **Design Pattern**
     - **Description**
     - **MAE Notes**

   * - **Moxin Reasoner**
     - Simplest Agentic Pattern, LLM + Customized Prompt
     - MAE provides template so app developers can apply best practices when prompting.  

   * - **Self Refiner**  
     - composed of: (1) A **Reasoner** that provides results of inference, (2) A **Reviewer** that checks whether inference results are good enough, and, (3) A **Refiner** that provides advice on improvement for inferencing in the next roudn of iteration. 
     - In MAE, app developers can specify the details of Reasoner, Reviewer and Refiner and a few tiny but important logistics such as the maximum number of iterations that allows.  

   * - **CrewAI Agent**
     - CrewAI is a multi-agent collaborative framework, in which a crew of multiple agents are defined with the tasks that they can carried out and tools that can be used. 
     - With MAE, CrewAI agents, tasks and tools can be defined, as well as the protocol how the agents are communicated. 

   * - **Actor**  
     - 
     - 

   * - **ReACT**  
     - 
     - 

   * - **Reflection**  
     - 
     - 

   * - **CoT Agent**
     - 
     - 

   * - **AutoGen Agent**  
     - 
     - 

MAE Architecture
----------------
MAE Architectural Mechanism provides Unified RAG, Tooling, Memory and Planning support, for the purpose of support flexible Agentic workflow. 

1. RAG
^^^^^^
MAE Supports RAG

.. list-table:: 
   :widths: 20 40 40
   :header-rows: 1

   * - **Feature**
     - **Description**
     - **MAE notes**

   * - **Feature 1**
     - 
     - 

   * - **Feature 2**
     - 
     - 

2. Memory
^^^^^^^^^
MAE supports memory

.. list-table:: 
   :widths: 20 40 40
   :header-rows: 1

   * - **Feature**
     - **Description**
     - **MAE notes**

   * - **Feature 1**
     - 
     - 

   * - **Feature 2**
     - 
     - 

3. Tooling
^^^^^^^^^^
MAE Tool Use

.. list-table:: 
   :widths: 20 40 40
   :header-rows: 1

   * - **Feature**
     - **Description**
     - **MAE notes**

   * - **Feature 1**
     - 
     - 

   * - **Feature 2**
     - 
     - 


4. Planning
^^^^^^^^^^^
Planning 

.. list-table:: 
   :widths: 20 40 40
   :header-rows: 1

   * - **Feature**
     - **Description**
     - **MAE notes**

   * - **Feature 1**
     - 
     -  

   * - **Feature 2**
     - 
     - 

MAE Super Agent
---------------
Moxin Agents can be assembled to build more powerful super agent. 