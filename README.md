# Plug-and-Play Image Restoration: Two-Level Coarse-to-Fine Initialization Analysis

[![Python 3.13](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![PyTorch 2.11](https://img.shields.io/badge/PyTorch-2.11.0-EE4C2C.svg)](https://pytorch.org/)
[![DeepInverse 0.5.0](https://img.shields.io/badge/DeepInverse-0.5.0-success.svg)](https://deepinv.github.io/deepinv/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: Reproducible Benchmark](https://img.shields.io/badge/Benchmark-Reproducible-brightgreen.svg)]()
[![Author: Hasnain Haider](https://img.shields.io/badge/Author-Hasnain%20Haider-informational.svg)](https://github.com/Hasnain006-nain)

A research benchmark and ablation study evaluating classical and learned-prior image restoration using **[DeepInverse](https://github.com/deepinv/deepinv)**, **PyTorch**, and pretrained **DRUNet**. This repository investigates whether a two-level coarse-to-fine initialization strategy provides measurable quantitative advantages over standard direct initialization in Plug-and-Play (PnP) Half-Quadratic Splitting (HQS) optimization.

> **Read the Full Paper / Research Report:**  
> 📄 **[Download Complete Research Report (PDF)](DeepInverse_PnP_Research_Report.pdf)** | Formatted in standard academic layout by Hasnain Haider.

---

## Table of Contents

- [Overview & Research Questions](#overview--research-questions)
- [Repository Architecture](#repository-architecture)
- [Core Experimental Findings](#core-experimental-findings)
- [Visual Ablation & Comparative Analysis](#visual-ablation--comparative-analysis)
- [Baseline Comparison: Classical TV-PGD vs Learned DPIR](#baseline-comparison-classical-tv-pgd-vs-learned-dpir)
- [Convergence & Iteration Dynamics](#convergence--iteration-dynamics)
- [Critical Methodological Boundaries & Limitations](#critical-methodological-boundaries--limitations)
- [Reproducibility & Execution Guide](#reproducibility--execution-guide)
- [Hardware & Environment Specifications](#hardware--environment-specifications)
- [Verified Academic References](#verified-academic-references)
- [License & Citation](#license--citation)

---

## Overview & Research Questions

In computational imaging, linear inverse problems seek to recover a clean signal $x \in \mathbb{R}^N$ from noisy, blurred measurements $y = Ax + n$, where $A$ is a forward degradation operator and $n \sim \mathcal{N}(0, \sigma^2 I)$ represents additive Gaussian noise. 

Standard Plug-and-Play (PnP) restoration methods (such as DPIR) typically initialize iterative optimization directly with the corrupted observation $y$. This project examines three core questions:

1. **Initialization Advantage:** Does pre-solving a low-resolution ($64 \times 64$) coarse inverse problem and upsampling the estimate provide a superior starting point for fine-scale ($128 \times 128$) restoration?
2. **Denoiser vs Upsampling Control:** Does the performance gain arise from coarse-level learned prior denoising, or simply from bicubic anti-aliasing?
3. **Computational Trade-off:** Does the reconstruction improvement justify the additional GPU wall-clock runtime?

```
                      +-----------------------------+
                      | Degraded Observation (y)    |
                      | 128x128 Gaussian Blur+Noise |
                      +--------------+--------------+
                                     |
         +---------------------------+---------------------------+
         |                                                       |
         v                                                       v
+------------------+                                   +-------------------+
| Direct DPIR      |                                   | Downsample (64x64)|
| Fine Scale Init  |                                   +---------+---------+
+--------+---------+                                             |
         |                                   +-------------------+-------------------+
         |                                   |                                       |
         |                                   v                                       v
         |                         +-------------------+                   +-------------------+
         |                         | Observation Init  |                   | Coarse PnP Solve  |
         |                         | Direct Upsampling |                   | 64x64 DRUNet PnP  |
         |                         +---------+---------+                   +---------+---------+
         |                                   |                                       |
         |                                   v                                       v
         |                         +-------------------+                   +-------------------+
         |                         | Upsample 128x128  |                   | Upsample 128x128  |
         |                         +---------+---------+                   +---------+---------+
         |                                   |                                       |
         +---------------------------------> | <-------------------------------------+
                                             v
                              +-----------------------------+
                              | Fine-Scale DPIR HQS Solve   |
                              | 128x128 DRUNet Restoration  |
                              +--------------+--------------+
                                             v
                              +-----------------------------+
                              | Final Restored Image (x_hat)|
                              +-----------------------------+
```

---

## Repository Architecture

The project is structured into modular directories separating notebooks, numerical results, visual figures, and documentation:

```text
deepinverse-pnp-image-restoration/
├── DeepInverse_PnP_Research_Report.pdf  # Complete academic research paper (Times New Roman, justified)
├── README.md                           # Main repository presentation and documentation
├── LICENSE                             # MIT Open-Source License
├── environment.json                    # Exact pinned Python, PyTorch, CUDA, and library versions
├── requirements.txt                    # Python dependency manifest
├── SHA256SUMS.txt                      # Cryptographic integrity checksums for all files
├── notebooks/
│   └── DeepInverse_PnP_Image_Restoration.ipynb  # Executable Colab workflow
├── results/                            # Numerical CSV results from all 60 experimental runs
│   ├── step10_all_experiments.csv      # Complete 60-run evaluation metrics
│   ├── step10_paired_comparison.csv    # Paired seed-level differences
│   ├── step10_image_summary.csv        # Per-image aggregate statistics
│   ├── step11_method_summary.csv       # Overall method performance summary
│   ├── step11_image_summary.csv        # Mean and standard deviation per image
│   ├── step11_paired_results.csv       # Full paired deltas across 20 trials
│   ├── step6_robustness_full_results.csv # Noise level robustness grid
│   ├── step6_robustness_summary.csv    # Noise level aggregate response
│   ├── step7_tv_vs_dpir_results.csv    # Classical TV vs learned DPIR metrics
│   ├── step8_convergence_metrics.csv   # Per-iteration objective and residual history
│   └── step9_multilevel_results.csv    # Multi-resolution stage comparison
├── figures/                            # High-resolution research figures
│   ├── step10_initialization_ablation.png
│   ├── step9_multilevel_comparison.png
│   ├── step7_method_comparison.png
│   ├── step8_convergence_residual.png
│   ├── step8_psnr_vs_iterations.png
│   ├── step6_visual_comparison.png
│   ├── step6_psnr_robustness.png
│   ├── step2_degradation.png
│   ├── deepinverse_restoration_comparison.png
│   └── multi_image_restoration_comparison.png
├── docs/
│   ├── DeepInverse_PnP_Research_Report.pdf
│   └── RESEARCH_SUMMARY.md
└── scripts/
    └── generate_pdf_report.py          # Standalone PDF compilation script (ReportLab)
```

---

## Core Experimental Findings

The primary evaluation spans **60 restoration experiments** (4 standard images $\times$ 5 pseudo-random noise seeds $\times$ 3 reconstruction pipelines). Images (Astronaut, Chelsea, Coffee, Rocket) were blurred with a Gaussian kernel ($\sigma = 2.0$) and corrupted with additive Gaussian noise ($\sigma = 0.03$).

### Overall Benchmark Summary (60 Runs)

| Restoration Pipeline | Mean PSNR | Mean SSIM | Mean GPU Runtime (T4) | Relative Compute Overhead |
|:---|:---:|:---:|:---:|:---:|
| **Direct DPIR (Baseline)** | 28.411 dB | 0.8588 | 0.2719 s | Reference (1.00&times;) |
| **Observation Initialization** | 28.530 dB | 0.8603 | 0.2735 s | +0.59% (+0.0016 s) |
| **Coarse PnP Initialization** | **28.593 dB** | **0.8622** | **0.3772 s** | **+38.71% (+0.1053 s)** |

### Paired Delta Analysis Across 20 Realizations

Evaluating paired differences on identical noise realizations confirms the consistency of the effect:
- **Coarse PnP vs Direct DPIR:** Mean gain of **+0.1820 dB** (positive in **20 / 20** runs).
- **Observation Init vs Direct DPIR:** Mean gain of **+0.1183 dB** (positive in **20 / 20** runs).
- **Coarse PnP vs Observation Init:** Mean gain of **+0.0637 dB** (positive in **20 / 20** runs).

### Image-Level Sensitivity Breakdown

The magnitude of initialization benefit depends heavily on image frequency content:

| Image Subject | Coarse vs Direct ($\Delta$ PSNR) | Coarse vs Obs Init ($\Delta$ PSNR) | Obs Init vs Direct ($\Delta$ PSNR) | Coarse Gain Std. Dev. |
|:---|:---:|:---:|:---:|:---:|
| **Coffee** (Broad textures, smooth tones) | **+0.3972 dB** | **+0.1118 dB** | +0.2854 dB | &plusmn; 0.0517 dB |
| **Astronaut** (Mixed face & suit details) | **+0.2868 dB** | **+0.1120 dB** | +0.1748 dB | &plusmn; 0.0284 dB |
| **Rocket** (High contrast, sharp contours) | +0.0289 dB | +0.0235 dB | +0.0054 dB | &plusmn; 0.0073 dB |
| **Chelsea** (Fine high-frequency fur patterns) | +0.0149 dB | +0.0073 dB | +0.0076 dB | &plusmn; 0.0129 dB |

---

## Visual Ablation & Comparative Analysis

### Multi-Seed Initialization Ablation
The figure below illustrates the PSNR distribution across all five noise seeds for each test image under the three evaluated pipelines:

<p align="center">
  <img src="figures/step10_initialization_ablation.png" alt="Step 10 Initialization Ablation" width="850">
</p>

*Figure 1: Reconstruction quality across 5 random seeds for Astronaut, Chelsea, Coffee, and Rocket. Coarse PnP initialization consistently leads in PSNR across every seed realization.*

---

## Baseline Comparison: Classical TV-PGD vs Learned DPIR

To benchmark learned priors against classical variational methods, we compared Total Variation Proximal Gradient Descent (TV-PGD) against learned DRUNet DPIR on the identical test suite:

| Test Subject | Degraded Observation | TV-PGD Reconstruction | Learned DPIR (DRUNet) | DPIR Quality Advantage | TV Runtime | DPIR Runtime |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Astronaut** | 19.18 dB (0.5628) | 22.23 dB (0.7584) | **24.13 dB (0.8452)** | **+1.90 dB** | 2.64 s | **0.37 s** |
| **Chelsea** | 24.57 dB (0.6073) | 27.22 dB (0.7407) | **29.74 dB (0.8567)** | **+2.52 dB** | 2.66 s | **0.35 s** |
| **Coffee** | 22.12 dB (0.5676) | 25.95 dB (0.7598) | **27.84 dB (0.8339)** | **+1.89 dB** | 2.35 s | **0.37 s** |
| **Rocket** | 25.92 dB (0.5231) | 29.15 dB (0.8360) | **31.81 dB (0.8987)** | **+2.66 dB** | 2.61 s | **0.36 s** |

<p align="center">
  <img src="figures/step7_method_comparison.png" alt="Method Comparison" width="850">
</p>

*Figure 2: Visual comparison between Ground Truth, Degraded Observation, Classical TV-PGD, and Deep DRUNet DPIR across all benchmark images.*

---

## Convergence & Iteration Dynamics

We tracked the iteration trajectories of the Half-Quadratic Splitting (HQS) algorithm to inspect whether coarse initialization accelerates convergence:

<p align="center">
  <img src="figures/step8_convergence_residual.png" alt="Convergence Residuals" width="420">
  <img src="figures/step8_psnr_vs_iterations.png" alt="PSNR vs Iterations" width="420">
</p>

*Figure 3: (Left) Relative residual reduction $\|x_{k+1} - x_k\| / \|x_k\|$ across iterations. (Right) Monotonic PSNR progression over optimization steps.*

---

## Critical Methodological Boundaries & Limitations

To maintain scientific integrity, the following boundaries of this study must be underscored:

1. **Computational Trade-Off:** Coarse PnP initialization requires an average inference time of 0.377 s vs 0.272 s for standard DPIR (a **38.7% runtime increase**). For latency-critical applications, a +0.182 dB gain may not justify this computational cost.
2. **Texture-Specific Gains:** The strategy yields meaningful improvements on images dominated by structural geometry and low frequencies (+0.40 dB on Coffee), but yields negligible gains on high-frequency stochastic textures (+0.015 dB on Chelsea).
3. **Approximation of Coarse Physics:** The coarse operator $A_c$ was modeled by downsampling the fine observation and resizing the blur kernel, rather than deriving an exact restriction operator satisfying $A_c = R A$ with consistent prolongation $P$.
4. **Scope of Prior:** The study evaluates off-the-shelf DRUNet within DeepInverse. It does **not** introduce a new generative flow-matching model or theoretical convergence proof.

---

## Reproducibility & Execution Guide

### Option 1: Run in Google Colab (Recommended)
1. Open [`notebooks/DeepInverse_PnP_Image_Restoration.ipynb`](notebooks/DeepInverse_PnP_Image_Restoration.ipynb) in [Google Colab](https://colab.research.google.com/).
2. Select a GPU runtime (`Runtime` &rarr; `Change runtime type` &rarr; `T4 GPU`).
3. Execute the notebook cells sequentially from top to bottom.

### Option 2: Local Reproduction

Clone the repository and install dependencies:
```bash
git clone https://github.com/Hasnain006-nain/deepinverse-pnp-image-restoration.git
cd deepinverse-pnp-image-restoration

# Install required packages
pip install -r requirements.txt
```

Verify experimental integrity:
```bash
# On Linux / macOS
sha256sum -c SHA256SUMS.txt

# On Windows PowerShell
Get-FileHash -Algorithm SHA256 (Get-ChildItem -Recurse -File)
```

Recompile the PDF research report:
```bash
python scripts/generate_pdf_report.py
```

---

## Hardware & Environment Specifications

The experimental figures and metrics were recorded under the following environment:

```json
{
  "python": "3.13.16",
  "packages": {
    "torch": "2.11.0+cu130",
    "deepinv": "0.5.0",
    "numpy": "2.1.3",
    "pandas": "2.2.3",
    "matplotlib": "3.10.0",
    "scikit-image": "0.25.2"
  },
  "cuda_available": true,
  "gpu": "Tesla T4"
}
```

---

## Verified Academic References

Every reference below was independently verified against primary publisher databases and DOI registries during this session:

1. **DeepInverse:**  
   J. Tachella, M. Terris, S. Hurault, A. Wang, D. Chen, M. Nguyen, M. Song, T. Davies, L. Davy, J. Dong, P. Escande, J. Hertrich, Z. Hu, T. I. Liaudat, N. Laurent, B. Levac, M. Massias, T. Moreau, T. Modrzyk, B. Monroy, S. Neumayer, J. Scanvic, F. Sarron, V. Sechaud, G. Schramm, C. Tang, R. Vo, and P. Weiss, *"DeepInverse: A Python package for solving imaging inverse problems with deep learning,"* arXiv preprint arXiv:2505.20160, 2025.  
   `% verified: https://arxiv.org/abs/2505.20160, checked 2026-10-30`

2. **DPIR Framework:**  
   K. Zhang, Y. Li, W. Zuo, L. Zhang, L. Van Gool, and R. Timofte, *"Plug-and-Play Image Restoration with Deep Denoiser Prior,"* IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI), vol. 44, no. 10, pp. 6360-6376, Oct. 2022.  
   DOI: [10.1109/TPAMI.2021.3088914](https://doi.org/10.1109/TPAMI.2021.3088914)  
   `% verified: https://ieeexplore.ieee.org/document/9446944, checked 2026-10-30`

3. **Plug-and-Play Priors:**  
   S. V. Venkatakrishnan, C. A. Bouman, and B. Wohlberg, *"Plug-and-Play Priors for Model Based Reconstruction,"* in 2013 IEEE Global Conference on Signal and Information Processing (GlobalSIP), pp. 945-948, Dec. 2013.  
   DOI: [10.1109/GlobalSIP.2013.6737048](https://doi.org/10.1109/GlobalSIP.2013.6737048)  
   `% verified: https://ieeexplore.ieee.org/document/6737048, checked 2026-10-30`

4. **PnP-Flow:**  
   S. Martin, A. Gagneux, P. Hagemann, and G. Steidl, *"Plug-and-Play Image Restoration with Flow Matching,"* in International Conference on Learning Representations (ICLR), 2025.  
   `% verified: https://openreview.net/forum?id=V2c2YxK0eG, checked 2026-10-30`

---

## License & Citation

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

If you utilize this benchmark or code in your research, please cite:

```bibtex
@misc{haider2026deepinversepnp,
  author       = {Hasnain Haider},
  title        = {Plug-and-Play Image Restoration: Two-Level Coarse-to-Fine Initialization Analysis using DeepInverse and DRUNet},
  year         = {2026},
  publisher    = {GitHub},
  howpublished = {\url{https://github.com/Hasnain006-nain/deepinverse-pnp-image-restoration}}
}
```
