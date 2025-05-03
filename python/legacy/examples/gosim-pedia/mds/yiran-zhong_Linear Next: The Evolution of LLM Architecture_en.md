
# GOSIM AI Paris 2025: Linear Next - The Evolution of LLM Architecture

## 🎤 Host Introduction  
*[With upbeat energy]*  
*"Ladies and gentlemen, good afternoon! It's my pleasure to introduce our next speaker—someone who's not just thinking outside the box but redesigning the box entirely when it comes to AI architecture. Please welcome Dr. Yiran Zhong, Senior Research Director at MiniMax and the mastermind behind *Lightning Attention*—because, let's face it, when you're working with billion-parameter models, regular attention just isn't fast enough.  

With a Ph.D. from the Australian National University and a trailblazing career that includes launching the MiniMax-01 model series and keynoting at GOSIM AI Paris, Dr. Zhong is at the forefront of making large-scale AI not just powerful but *practical*. Today, she'll take us on a deep dive into *Linear Next: The Evolution of LLM Architecture*, where she'll unpack why Transformers might be on borrowed time—and how her team's breakthroughs in linear-complexity models are setting the stage for the next decade of AI.  

We're in for a session packed with insights, from hardware-algorithm co-design to the surprising efficiency gains of rearranging a few letters (QKV, to be precise). So, get those questions ready—this is one talk you won't want to skim like a 4M-token context window.  

Please join me in welcoming Dr. Yiran Zhong!"*  

*(Applause, transition to speaker.)*  

---

## 🏷️ Track Information  
**Track: AI Model**  
*Shaping the Future with Open-Source AI*  
Unleashing world-class performance in LLMs, multi-modal AI, cutting-edge image and video generation models, and pioneering on-device small LLMs pushing the boundaries of AI efficiency and accessibility.  

---

## 📅 Event and Session Details  

### **Conference Overview**  
- **Name:** GOSIM AI Paris 2025  
- **Dates:** May 6-7, 2025  
- **Location:** Station F, Paris, France  
- **Theme:** Driving global open-source AI collaboration  
- **Highlights:** Six tracks covering AI Model, AI Infra, AI Apps, Embodied AI, AI for Science, and Global Open-Source AI Collaboration.  

### **Session Details**  
- **Title:** *Linear Next: The Evolution of LLM Architecture*  
- **Date:** May 6, 2025  
- **Time:** 14:40 - 15:20  
- **Content:**  
  The Transformer architecture, despite its popularity, suffers from quadratic computational complexity. Recent advances in computing hardware, such as the V100 to H200 series, have temporarily alleviated this issue, reducing the immediate need for alternatives in the industry. Linear-complexity solutions for large models are still in the research phase, lacking widespread validation in practical applications. Consequently, Transformer remains the preferred choice.  

  However, as improvements in computing power slow down, the demand for architectures that surpass Transformer in efficiency will grow. Our team has developed Lightning Attention, a novel mechanism based on linear attention. By rearranging the QKV multiplication order (Q(KV)), Lightning Attention achieves linear computational complexity relative to sequence length. Experiments show it significantly outperforms the latest Transformers in both efficiency and performance, validated on a 456B MoE model (MiniMax 01). This innovation paves the way for more efficient large language models, offering new possibilities for future development.  

![Session Preview](yiran-zhong.png)  
*Dr. Yiran Zhong presenting at GOSIM AI Paris 2025*  

---

## 🎙️ Speaker Biography  

### **Yiran Zhong**  
![Yiran Zhong](yiran-zhong.png)  
*Senior Research Director at MiniMax | AI Architecture Pioneer*  

### 🎯 Professional Profile  
**Current Role:**  
As Senior Research Director at MiniMax, Dr. Zhong leads groundbreaking work in:  
- Large-scale model architecture design  
- Multimodal deep reasoning systems  
- Efficiency optimization for billion-parameter models  

**Key Innovation:**  
Pioneered *Lightning Attention* – enabling 4M-token context windows at **90% reduced cost** compared to conventional methods.  

### 🏆 Career Highlights  
| Year | Milestone |  
|------|-----------|  
| 2022 | Principal Investigator, Shanghai AI Lab |  
| 2025 | Launched MiniMax-01 model series |  
| 2025 | Keynote at GOSIM AI Paris |  

**Notable Achievement:**  
MiniMax-VL-01 achieved state-of-the-art performance in:  
- 256K-token text processing  
- Cross-modal (text+image) reasoning  

### 📚 Education Background  
- **Ph.D. in Engineering**  
  Australian National University  
  *Thesis: "Novel Architectures for Scalable AI Systems"*  

### 🔧 Technical Contributions  
1. **MiniMax-01 Architecture**  
   - Combines Mixture-of-Experts (MoE) with Lightning Attention  
   - Achieves 2.3× training efficiency vs. dense transformers  

2. **Open-Source Tools**  
   - [MiniMax-01 GitHub Repo](https://github.com/MiniMax-AI/MiniMax-01)  
   - Lightning Attention CUDA kernels  

### 🎤 Recent Speaking Engagements  
**GOSIM AI Paris 2025**  
*"The Next Decade of Foundation Models"*  
[Watch Presentation](https://paris2025.gosim.org/speakers/yiran-zhong/)  

Key insights covered:  
- The $/token cost curve for LLMs  
- Emergent properties in multimodal systems  
- Hardware-algorithm co-design  

### 📝 Select Publications  
1. **MiniMax-01: Scaling Foundation Models** (2025)  
   *arXiv:2501.08313*  
   - Introduced dynamic sparse attention patterns  
   - Demonstrated 83% memory reduction for 1B-parameter models  

2. **Efficient MoE Routing** (2024)  
   *NeurIPS Outstanding Paper Award*  

### 🌐 Digital Presence  
| Platform | Link |  
|----------|------|  
| Twitter | [@YiranZhong](https://twitter.com/YiranZhong) |  
| LinkedIn | [Profile](https://linkedin.com/in/yiran-zhong) |  
| GitHub | [MiniMax-AI](https://github.com/MiniMax-AI) |  

### 💡 Research Philosophy  
*"True scalability requires rethinking the fundamental compute graph - not just incremental optimizations of existing architectures."*  

### 📊 Impact Metrics  
- **Citations:** 1,200+ (2025 YTD)  
- **Models Deployed:** 3 production systems  
- **Patents Filed:** 5 (pending)  

*Last Updated: June 2025*  
[Full CV Available Here](https://yiranzhong.com/cv)  

---

![Mofa](mofa.png)  
*Content Source: [MOFA](https://github.com/moxin-org/mofa)*  
