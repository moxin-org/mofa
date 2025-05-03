
# GOSIM AI Paris 2025

## 🎤 Host Introduction

*"Good [morning/afternoon/evening], everyone! It's a pleasure to have you here. Now, if you've ever wished your AI models could be faster, smaller, and just a bit less *needy* in terms of compute resources, you're in for a treat.*  

*Let me introduce **Eldar Kurtić**, a Senior ML Research Engineer at Red Hat and Researcher at IST Austria. Eldar is the kind of person who looks at a large language model and thinks, 'Hmm, how can I make this *leaner* without losing its brilliance?'—which, frankly, is the AI equivalent of turning a luxury cruise ship into a speedboat. His work on model sparsity, quantization, and pruning has made waves in the field, and he's here today to share some of that magic.*  

*In this session, **'Scaling LLM Inference with vLLM: Multi-Accelerator Serving and Quantized LLMs,'** Eldar will dive into how vLLM—now the community's go-to engine for efficient inference—can supercharge your deployments. You'll get a blueprint for scaling LLMs with techniques like tensor parallelism, paged attention, and yes, *quantization* (because who doesn't love a good 3.5x speed boost?).*  

*So, whether you're battling latency or just love a well-optimized model, grab your questions—this is one you won't want to miss. Please join me in welcoming **Eldar Kurtić**!"*  

*(Lead applause, then smoothly hand over to Eldar.)*  

---

## � Track Information: **PyTorch Day France**  
*A dedicated space for AI practitioners, researchers, and engineers to explore the latest advancements in deep learning with PyTorch. From cutting-edge model development to scalable deployment, this track offers expert insights, hands-on sessions, and discussions shaping the future of AI with PyTorch.*

---

## 📅 Event and Session Details

### **Conference Overview**  
- **Name**: GOSIM AI Paris 2025  
- **Dates**: May 6-7, 2025  
- **Location**: Station F, Paris, France  
- **Theme**: Driving global open-source AI collaboration across six tracks: AI Model, AI Infra, AI Apps, Embodied AI, AI for Science, and Global Open-Source AI Collaboration.  

### **Session Details**  
- **Title**: Scaling LLM Inference with vLLM: Multi-Accelerator Serving and Quantized LLMs  
- **Date**: May 7, 2025  
- **Time**: 11:30 - 11:50  
- **Content**:  
  vLLM has become the community-standard engine for low-latency LLM inference, achieving a 10× increase in usage in 2024 and surpassing 100,000 daily installs by January 2025. Supported by hundreds of contributors and productized through Red Hat AI, vLLM provides a vendor-neutral solution for serving cutting-edge models at scale. This talk outlines a practical blueprint for scaling LLM inference using vLLM, integrating both system-level techniques and model-level optimizations.  

  We begin by addressing the challenges of deploying LLMs with chain-of-thought reasoning in production. Leveraging vLLM’s engine architecture, multi-accelerator deployments using tensor parallelism, paged attention scheduling, and prefill–decode disaggregation demonstrate how a single node can efficiently drive multiple AI accelerators, enhancing throughput without compromising latency.  

  The second optimization layer focuses on quantization. Based on over 500,000 evaluations across language and vision-language models, we examine the accuracy–speed trade-offs of weight and activation quantization. We introduce new pathways that significantly reduce memory usage while maintaining model quality. Attendees will leave with data-driven insights and ready-to-use configurations for deploying state-of-the-art quantized models in scalable enterprise inference pipelines.  

---

## 👨‍💻 Speaker Biography: Eldar Kurtić  

### 🧠 Personal Information  
- **Full Name**: Eldar Kurtić  
- **Current Position**: Senior ML Research Engineer at Red Hat and Researcher at the Institute of Science and Technology Austria (IST Austria)  
- **Education**:  
  - **MITx**: MicroMasters Program in Statistics and Data Science (2018)  
  - **University of Sarajevo**: Master of Engineering (M.Eng.), Automatic Control and Electronics (2016)  
- **Location**: Vienna, Austria  

### 🚀 Career Path (Timeline)  
- **2013–2018**: Undergraduate Student at the University of Sarajevo – Developed foundational skills in electrical engineering and automatic control.  
- **2018–2020**: Researcher at Virtual Vehicle – Engaged in applied research and technology development in AI.  
- **2020–Present**: Researcher at IST Austria – Advanced research in model sparsity, pruning, and quantization techniques.  
- **2025–Present**: Senior ML Research Engineer at Red Hat – Leading projects in scalable AI deployment and efficient inference techniques.  

### 🎯 Role  
Eldar Kurtić specializes in optimizing deep learning models through techniques like quantization, sparsity, and pruning. His work focuses on making AI models faster, smaller, and more efficient, particularly for deployment on CPUs and GPUs.  

### 📚 Publications  
- **2023**: *Sparse Finetuning for Inference Acceleration of Large Language Models* – Introduced innovative techniques for accelerating large language models through sparse fine-tuning.  
  [Read the full paper here](https://arxiv.org/abs/2310.06927)  
- **2023**: *ZipLM: Code for the NeurIPS 2023 Paper* – Developed a framework for sparse fine-tuning of large language models.  
  [GitHub Repository](https://github.com/IST-DASLab/ZipLM)  

### 🏆 Awards and Recognitions  
- **2023**: Recognition for contributions to making quantization more accessible and performant in AI models.  

### 📺 Media Appearances  
- **2023**: *vLLM Office Hours – Model Quantization for Efficient Inference* – Discussed advancements in model compression and quantization techniques.  
  [Watch the Video Here](https://www.linkedin.com/posts/eldar-kurtić-77963b160_vllm-office-hours-model-quantization-for-activity-7223719003481862144-M8-U)  
- **2023**: *Cohere for AI Event* – Shared insights on sparse fine-tuning and efficient inference.  
  [Event Details](https://twitter.com/_EldarKurtic/status/1897755425509925163)  

### 💡 Personal Insights  
Eldar is passionate about making advanced AI techniques accessible to a broader audience. His work in open-source projects and community engagement reflects his commitment to democratizing AI innovation.  

### 🔗 Social Media Presence  
- **Twitter**: [@_EldarKurtic](https://twitter.com/_EldarKurtic)  
- **GitHub**: [eldarkurtic](https://github.com/eldarkurtic)  
- **LinkedIn**: [Eldar Kurtić](https://www.linkedin.com/in/eldar-kurtić-77963b160/)  
- **Website**: [Red Hat Developer Profile](https://developers.redhat.com/author/eldar-kurtic)  

### 🌍 Influence and Impact  
Eldar Kurtić has significantly influenced the field of AI by advancing techniques in model compression and sparse inference. His work has enabled faster and more efficient AI deployments, making state-of-the-art models accessible for real-world applications.  

### 📷 Images  
![Eldar Kurtić at Red Hat](https://developers.redhat.com/themes/custom/rhdp_fe/favicons/favicon.ico)  
*Image Source: Red Hat Developer*  

### 🎥 Videos  
- **2023**: *vLLM Office Hours – Model Quantization for Efficient Inference* – A deep dive into model compression techniques.  
  [Watch the Video Here](https://www.linkedin.com/posts/eldar-kurtić-77963b160_vllm-office-hours-model-quantization-for-activity-7223719003481862144-M8-U)  

### ✍️ Blogs  
- **2023**: *Enable 3.5 Times Faster Vision Language Models with Quantization* – Explains how quantization techniques can accelerate AI models.  
  [Read the Blog Here](https://developers.redhat.com/author/eldar-kurtic)  

### 🔍 Source Citations  
- [LinkedIn: Eldar Kurtić](https://www.linkedin.com/in/eldar-kurtić-77963b160/)  
- [Google Scholar](https://scholar.google.com/citations?user=jOvBcUUAAAAJ&hl=en)  
- [Red Hat Developer](https://developers.redhat.com/author/eldar-kurtic)  
- [GitHub: Eldar Kurtic](https://github.com/eldarkurtic)  

*Report generated on 2025-04-29.*  

---

![Mofa](mofa.png)  
*Content Source: [MOFA](https://github.com/moxin-org/mofa)*  
