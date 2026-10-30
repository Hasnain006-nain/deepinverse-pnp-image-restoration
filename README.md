<div align="center">

# Plug-and-Play Image Restoration with Coarse-to-Fine Initialization

### An Empirical Benchmark on Two-Level DRUNet Initialization using DeepInverse

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.11-EE4C2C?style=flat&logo=pytorch&logoColor=white)](https://pytorch.org)
[![DeepInverse](https://img.shields.io/badge/DeepInverse-0.5.0-10B981?style=flat)](https://deepinv.github.io/deepinv/)
[![Hardware](https://img.shields.io/badge/GPU-Tesla_T4_(16GB)-76B900?style=flat&logo=nvidia&logoColor=white)](#experimental-environment)
[![Technical Report](https://img.shields.io/badge/Technical_Report-6--Page_PDF-blue.svg)](DeepInverse_PnP_Research_Report.pdf)
[![Reproducibility](https://img.shields.io/badge/Reproducibility-Level_5_Deterministic-emerald.svg)](SHA256SUMS.txt)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[**Read 6-Page Technical Report (PDF)**](DeepInverse_PnP_Research_Report.pdf) • [**Launch in Google Colab**](https://colab.research.google.com/github/Hasnain006-nain/deepinverse-pnp-image-restoration/blob/main/notebooks/DeepInverse_PnP_Image_Restoration.ipynb) • [**Raw Numerical CSV Traces**](results/)

<br/>

<img src="figures/deepinverse_restoration_comparison.png" alt="DeepInverse Restoration Comparison" width="860">

</div>

---

## 📌 Executive Summary

This repository hosts a controlled, open-science computational imaging benchmark investigating whether a **two-level coarse-to-fine initialization** improves Plug-and-Play (PnP) image restoration when paired with a deep denoiser prior.

Using the open-source **[DeepInverse](https://deepinv.github.io/deepinv/)** library and pretrained **DRUNet** weights, we evaluated 60 independent restoration experiments across four canonical test images (`Astronaut`, `Chelsea`, `Coffee`, `Rocket`) degraded by synthetic Gaussian blur ($\sigma = 2.0$) and additive white Gaussian noise ($\sigma = 0.03$) over five fixed pseudo-random noise realizations.

> **Key Empirical Takeaway:** Coarse PnP initialization improves reconstruction PSNR across **100% of paired trials (+0.182 dB average gain)**, but requires **38.7% more wall-clock time**. A control experiment reveals that **65% of this benefit (+0.118 dB)** is produced solely by low-pass smoothing during resolution cycling, while coarse-level denoising contributes the remaining +0.064 dB.

---

## 🔬 Benchmark Methodology & Evaluated Pipelines

All evaluations execute on identical degraded observations using an 8-iteration Half-Quadratic Splitting (HQS) schedule with fixed DRUNet weights. The only variable is the starting estimate $x_0$:

| Pipeline ID | Strategy Name | Operational Description | Avg. Runtime (T4) | Compute Overhead |
|:---:|:---|:---|:---:|:---:|
| **1** | **Direct DPIR** *(Baseline)* | Standard HQS optimization initialized directly from degraded observation: $x_0 = y$. | **0.2719 s** | Baseline ($1.00\times$) |
| **2** | **Observation Init** *(Control)* | Degraded observation $y$ is downsampled to $64\times 64$ and immediately bicubic-upsampled back to $128\times 128$ to serve as $x_0$. No coarse denoiser is executed. | **0.2735 s** | $+0.6\%$ ($1.01\times$) |
| **3** | **Coarse PnP Init** *(Proposed)* | Solve a complete DPIR problem at $64\times 64$ resolution with a scaled blur operator. Upsample the coarse solution to $128\times 128$ to initialize fine-scale DPIR. | **0.3772 s** | **$+38.7\%$ ($1.39\times$)** |

---

## 📊 Comprehensive Empirical Findings

### 1. Overall Aggregate Results (60 Runs, NVIDIA Tesla T4 GPU)

| Initialization Strategy | Mean PSNR (dB) | Mean SSIM | Mean Wall-Clock Runtime | Relative Computational Cost |
|:---|:---:|:---:|:---:|:---:|
| Direct DPIR *(Baseline)* | 28.411 dB | 0.8588 | 0.2719 s | $1.00\times$ |
| Observation Init *(Control)* | 28.530 dB | 0.8603 | 0.2735 s | $1.01\times$ |
| **Coarse PnP Init *(Proposed)*** | **28.593 dB** | **0.8622** | **0.3772 s** | **$1.39\times$ (+38.7%)** |

---

### 2. Paired Differences Analysis (Identical Degradation Instances)

Because noise variance alters absolute PSNR across seeds, paired differences ($\Delta\text{PSNR} = \text{PSNR}_{\text{method A}} - \text{PSNR}_{\text{method B}}$) evaluate performance on identical degraded inputs:

| Paired Comparison | Mean $\Delta$PSNR Gain | Std. Deviation | Positive Trials / Total | Win Rate |
|:---|:---:|:---:|:---:|:---:|
| **Coarse PnP vs. Direct DPIR** | **+0.1820 dB** | 0.162 dB | **20 / 20** | **100.0%** |
| **Observation Init vs. Direct DPIR** | **+0.1183 dB** | 0.114 dB | **20 / 20** | **100.0%** |
| **Coarse PnP vs. Observation Init** | **+0.0637 dB** | 0.051 dB | **20 / 20** | **100.0%** |

---

### 3. Image Frequency Sensitivity Breakdown

The magnitude of improvement depends directly on the frequency spectrum of the underlying image:

| Image | Dominant Content Characteristics | Coarse vs. Direct | Coarse vs. Obs Init | Obs Init vs. Direct |
|:---|:---|:---:|:---:|:---:|
| **Coffee** | Broad smooth gradients, uniform cup surface | **+0.397 dB** | +0.112 dB | +0.285 dB |
| **Astronaut** | Mixed structural contours, portrait details | **+0.287 dB** | +0.112 dB | +0.175 dB |
| **Rocket** | Sharp high-contrast boundary edges | **+0.029 dB** | +0.024 dB | +0.005 dB |
| **Chelsea** | High-frequency fur texture, dense whiskers | **+0.015 dB** | +0.007 dB | +0.008 dB |

> **Frequency Insight:** Coarse resolution cycling acts as a pre-smoothing filter. For images with large continuous tonal areas (Coffee, Astronaut), this accelerates accurate gradient reconstruction. For high-frequency texture images (Chelsea, Rocket), $64\times 64$ downsampling removes critical high frequencies, yielding virtually zero net benefit.

---

## 🖼️ Visual Results & Diagnostic Figures

### 1. Forward Degradation Model
<div align="center">
<img src="figures/step2_degradation.png" width="820" alt="Forward Degradation Model">
<p><i>Figure 1: Clean ground truth, point spread function (PSF), 2D frequency spectrum showing high-frequency attenuation, and resulting degraded observation.</i></p>
</div>

---

### 2. Baseline Comparison: Classical TV-PGD vs. Learned DRUNet DPIR
<div align="center">
<img src="figures/step7_method_comparison.png" width="840" alt="TV-PGD vs DPIR">
<p><i>Figure 2: Ground truth, degraded input, Total Variation (TV-PGD) reconstruction, and DRUNet DPIR output.</i></p>
</div>

| Image | Degraded Input | Classical TV-PGD [5] | Learned DRUNet DPIR [2] | PSNR Gain | TV Runtime | DPIR Runtime |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Astronaut** | 19.18 dB | 22.23 dB | **24.13 dB** | **+1.90 dB** | 2.64 s | **0.37 s** *(7.1× faster)* |
| **Chelsea** | 24.57 dB | 27.22 dB | **29.74 dB** | **+2.52 dB** | 2.66 s | **0.35 s** *(7.6× faster)* |
| **Coffee** | 22.12 dB | 25.95 dB | **27.84 dB** | **+1.89 dB** | 2.35 s | **0.37 s** *(6.4× faster)* |
| **Rocket** | 25.92 dB | 29.15 dB | **31.81 dB** | **+2.66 dB** | 2.61 s | **0.36 s** *(7.3× faster)* |

---

### 3. Stage-by-Stage Visual Progression (Two-Level Restoration)
<div align="center">
<img src="figures/step9_multilevel_comparison.png" width="860" alt="Multilevel Stages">
<p><i>Figure 3: Two-level progression: degraded observation, coarse 64×64 solve, bicubic prolongation, and fine-scale 128×128 refined output.</i></p>
</div>

---

### 4. Per-Seed Ablation Distribution Across All Test Images
<div align="center">
<img src="figures/step10_initialization_ablation.png" width="840" alt="Initialization Ablation">
<p><i>Figure 4: Grouped bar chart comparing PSNR per random seed across Direct DPIR (blue), Observation Init (orange), and Coarse PnP Init (green).</i></p>
</div>

---

### 5. Convergence Behavior and Numerical Residual Stability
<div align="center">
<img src="figures/step8_psnr_vs_iterations.png" width="410" alt="PSNR vs Iterations">
<img src="figures/step8_convergence_residual.png" width="410" alt="Residual Decay">
<p><i>Figure 5: Left: PSNR progression over 8 HQS iterations. Right: Logarithmic relative residual decay demonstrating numerical stability within 5 iterations.</i></p>
</div>

---

### 6. Robustness under Scaled Noise Intensities ($\sigma = 0.01$ to $0.07$)
<div align="center">
<img src="figures/step6_psnr_robustness.png" width="370" alt="PSNR Robustness">
<img src="figures/step6_visual_comparison.png" width="470" alt="Visual Robustness">
<p><i>Figure 6: Monotonic PSNR degradation and qualitative stability across noise standard deviations from 0.01 to 0.07.</i></p>
</div>

---

## ⚙️ Quickstart & Reproduction Guide

### Option A: Run Online in Google Colab (Recommended)

Click the badge below to launch the complete notebook in Google Colab with free GPU access:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hasnain006-nain/deepinverse-pnp-image-restoration/blob/main/notebooks/DeepInverse_PnP_Image_Restoration.ipynb)

1. Select **Runtime → Change runtime type → T4 GPU**.
2. Execute cells top-to-bottom to run the complete 60-trial benchmark.

---

### Option B: Local Environment Execution

```bash
# Clone the repository
git clone https://github.com/Hasnain006-nain/deepinverse-pnp-image-restoration.git
cd deepinverse-pnp-image-restoration

# Create and activate virtual environment
python -m venv venv
# Linux/macOS:
source venv/bin/activate
# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Install required dependencies
pip install -r requirements.txt

# Recompile the 6-page research report PDF
python scripts/generate_pdf_report.py
```

---

## 💻 Documented Hardware & Software Environment

| Component | Specification | Verified Version |
|:---|:---|:---|
| **Python Runtime** | CPython | `3.13.16` |
| **Deep Learning Framework** | PyTorch | `2.11.0+cu130` |
| **Computational Imaging Package** | DeepInverse | `0.5.0` |
| **Scientific Computing** | NumPy / SciPy | `2.1.3` / `1.14.1` |
| **Visualization & Processing** | Matplotlib / scikit-image | `3.10.0` / `0.25.2` |
| **Document Compiler** | ReportLab | `4.2.5` |
| **GPU Hardware** | NVIDIA Tesla T4 | 16 GB VRAM |

File integrity is cryptographically validated using SHA-256 hashes recorded in [`SHA256SUMS.txt`](SHA256SUMS.txt).

---

## 📁 Repository Organization

```
deepinverse-pnp-image-restoration/
├── README.md                            # Comprehensive benchmark documentation
├── DeepInverse_PnP_Research_Report.pdf  # 6-page academic research report PDF
├── RESEARCH_SUMMARY.md                  # Concise numerical audit summary
├── LICENSE                              # MIT License
├── requirements.txt                     # Pinned Python package dependencies
├── environment.json                     # Environment configuration dump
├── SHA256SUMS.txt                       # Cryptographic file hashes
│
├── notebooks/
│   └── DeepInverse_PnP_Image_Restoration.ipynb # Full executable Colab notebook
│
├── results/                             # Complete raw CSV execution traces (13 files)
│   ├── step10_all_experiments.csv       # All 60 individual trial metrics
│   ├── step10_paired_comparison.csv     # Paired delta metrics
│   ├── step11_method_summary.csv        # Aggregate metrics per pipeline
│   ├── step11_image_summary.csv         # Aggregate metrics per image
│   ├── step7_tv_vs_dpir_results.csv     # TV vs DPIR comparative results
│   └── step8_convergence_metrics.csv    # Iteration-level convergence traces
│
├── figures/                             # 10 publication-quality research figures
│   ├── deepinverse_restoration_comparison.png
│   ├── step2_degradation.png
│   ├── step7_method_comparison.png
│   ├── step8_convergence_residual.png
│   ├── step8_psnr_vs_iterations.png
│   ├── step9_multilevel_comparison.png
│   └── step10_initialization_ablation.png
│
├── docs/
│   └── DeepInverse_PnP_Research_Report.pdf # Mirrored 6-page report PDF
│
└── scripts/
    └── generate_pdf_report.py           # ReportLab PDF compiler script
```

---

## ⚠️ Limitations & Scoping Statement

1. **Sample Cohort:** The benchmark evaluates four images over five noise seeds (20 paired trials). While sufficient to confirm consistent paired behavior on this sample, it does not represent a population-wide claim across heterogeneous datasets.
2. **Heuristic Coarse Forward Operator:** The $64\times 64$ blur operator was formed by bicubic resizing of the fine blur kernel rather than constructing a true Galerkin restriction operator $A_c = R A P$.
3. **Model Scope:** This project benchmarks classical and deep denoiser Plug-and-Play restoration (DRUNet-DPIR). It does not implement diffusion models or flow-matching algorithms [4].
4. **Execution Ledger:** All timing data reflects CUDA-synchronized single-session execution on an NVIDIA Tesla T4 GPU.

---

## 📚 Verified Academic References

All citations have been verified against primary publisher and indexing databases:

1. **J. Tachella, M. Terris, S. Hurault, A. Wang, et al.**, *"DeepInverse: A Python package for solving imaging inverse problems with deep learning,"* *Journal of Open Source Software*, vol. 10, no. 115, p. 8923, 2025.  
   DOI: [`10.21105/joss.08923`](https://doi.org/10.21105/joss.08923) • arXiv: [`2505.20160`](https://arxiv.org/abs/2505.20160)

2. **K. Zhang, Y. Li, W. Zuo, L. Zhang, L. Van Gool, and R. Timofte**, *"Plug-and-Play Image Restoration with Deep Denoiser Prior,"* *IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI)*, vol. 44, no. 10, pp. 6360–6376, Oct. 2022.  
   DOI: [`10.1109/TPAMI.2021.3088914`](https://doi.org/10.1109/TPAMI.2021.3088914)

3. **S. V. Venkatakrishnan, C. A. Bouman, and B. Wohlberg**, *"Plug-and-Play Priors for Model Based Reconstruction,"* in *IEEE Global Conference on Signal and Information Processing (GlobalSIP)*, pp. 945–948, Dec. 2013.  
   DOI: [`10.1109/GlobalSIP.2013.6737048`](https://doi.org/10.1109/GlobalSIP.2013.6737048)

4. **S. Martin, A. Gagneux, P. Hagemann, and G. Steidl**, *"PnP-Flow: Plug-and-Play Image Restoration with Flow Matching,"* in *International Conference on Learning Representations (ICLR)*, 2025.  
   OpenReview: [`V2c2YxK0eG`](https://openreview.net/forum?id=V2c2YxK0eG) • arXiv: [`2410.21200`](https://arxiv.org/abs/2410.21200)

5. **L. I. Rudin, S. Osher, and E. Fatemi**, *"Nonlinear total variation based noise removal algorithms,"* *Physica D: Nonlinear Phenomena*, vol. 60, no. 1–4, pp. 259–268, 1992.  
   DOI: [`10.1016/0167-2789(92)90242-F`](https://doi.org/10.1016/0167-2789(92)90242-F)

---

## 👤 Author

**Hasnain Haider**  
GitHub: [@Hasnain006-nain](https://github.com/Hasnain006-nain)  
Project Repository: [deepinverse-pnp-image-restoration](https://github.com/Hasnain006-nain/deepinverse-pnp-image-restoration)

---

## 📜 License

This research code, benchmark datasets, and documentation are licensed under the **[MIT License](LICENSE)**.
