
# Cost Comparison: Running Qwen-3 on Bare Metal vs. AWS

## 🔧 Assumptions

We'll compare based on **GPU instances** typically required to serve a 7B–14B parameter model like Qwen-3:

- **Model size**: Qwen-3 14B
- **Serving requirement**: 1–2 × NVIDIA A100 80GB GPUs (or equivalent like H100 or L40S)
- **Use case**: Always-on model inference (not training)

---

## 💰 Cost Comparison

### 1. AWS (On-Demand EC2)

- **p4d.24xlarge** (8 × A100 40GB): ~$32.77/hour  
- Per GPU hourly: ~$4.10
- Monthly (24/7): $4.10 × 730 ≈ **$2,993/GPU**

> Cheaper options exist via Spot, Savings Plans, or Graviton/Inferentia, but with tradeoffs in reliability and flexibility.

---

### 2. Bare Metal (Colo or On-Prem)

- **Server with 2 × A100 80GB**: ~$60,000–$80,000 upfront
- **Hosting (colocation)**: ~$500–$1,000/month (power + rack + network)
- **Amortized 3-year cost**:  
  - $80K server + $1K/mo hosting × 36 = $116K  
  - $116K ÷ 36 months = **~$3,222/month**
  - Per GPU = **$1,611/month**

With 90%+ utilization, cost per GPU-hour drops to **~$2.20**, compared to AWS at **~$4.10**

---

## 📉 Savings Estimate

| Option        | Cost/GPU/month | Cost/GPU/hr | Savings vs. AWS |
|---------------|----------------|-------------|------------------|
| **AWS**       | ~$2,993        | ~$4.10      | —                |
| **Bare Metal**| ~$1,611        | ~$2.20      | **~46% cheaper** |

> Spot or reserved AWS options can reduce costs, but still generally not below well-utilized bare metal.

---

## 🧠 Key Considerations

### When AWS is better:
- You need **elasticity** or **burst compute**
- You need **global deployment** quickly
- You’re doing **short-term experiments**

### When Bare Metal wins:
- **High, predictable usage** (24/7)
- **Cost-sensitive workloads**
- You’re comfortable with **hardware management** or **colocation vendors**

---

## 💡 TL;DR

Running Qwen-3 or similar models on **bare metal** is typically **40–60% cheaper** than AWS for **steady workloads**, especially with A100/H100-class GPUs and predictable traffic.
