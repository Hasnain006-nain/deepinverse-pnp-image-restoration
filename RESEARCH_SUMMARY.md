# Research Summary — DeepInverse Plug-and-Play Image Restoration

**Project type:** Reproducible computational imaging benchmark.  
**System:** Google Colab, NVIDIA Tesla T4 GPU (16 GB VRAM); Python 3.13, PyTorch 2.11.0, DeepInverse 0.5.0.  
**Restoration prior:** Pretrained DRUNet deep denoiser (no network training performed).  
**Primary research question:** Does a two-level coarse-to-fine initialization improve standard DPIR reconstruction on small RGB images degraded by blur and additive noise?

## Experimental Design

Four canonical scikit-image benchmarks (`astronaut`, `chelsea`, `coffee`, `rocket`) were standardized to 128 × 128 RGB pixels normalized to [0, 1]. Degradation was simulated with a 7 × 7 Gaussian blur kernel ($\sigma_b = 2.0$) and additive white Gaussian noise ($\sigma_n = 0.03$). For each image, five pseudo-random noise seeds (2026, 2126, 2226, 2326, 2426 + offset) were applied, generating **20 matched image-seed observations**.

Each observation was passed identically to three initialization strategies:

1. **Direct DPIR (Baseline):** Standard HQS optimization initialized directly from the noisy observation: $x_0 = y$.
2. **Observation Initialization (Control):** The observation $y$ is downsampled via 2×2 average pooling ($64 \times 64$) and immediately prolonged back to $128 \times 128$ via PyTorch **bilinear interpolation** (`align_corners=False`) without coarse denoising, isolating resolution-cycling smoothing effects.
3. **Coarse PnP Initialization (Proposed):** An approximate coarse forward model ($64 \times 64$, Gaussian blur $\sigma_b = 1.0$, noise $\sigma_n = 0.015$) is solved via 8-iteration coarse DPIR. The coarse restoration is prolonged via **bilinear interpolation** to warm-start fine-scale 128 × 128 DPIR.

For each run, reconstruction quality was evaluated using clipped [0, 1] RGB Peak Signal-to-Noise Ratio (PSNR) and Structural Similarity Index (SSIM). Wall-clock execution times were recorded with explicit CUDA GPU synchronization.

## Observed Results

### 1. Method-Level Aggregates (20 Matched Observations, 60 Total Runs)

| Method | Mean PSNR | Mean SSIM | Mean Runtime (T4) | Compute Overhead |
|---|---:|---:|---:|---:|
| Direct DPIR (Baseline) | 28.4112 dB | 0.8588 | 0.2719 s | 1.00× (baseline) |
| Observation Init (Control) | 28.5295 dB | 0.8603 | 0.2735 s | 1.01× (+0.6%) |
| **Coarse PnP Init (Proposed)** | **28.5932 dB** | **0.8622** | **0.3772 s** | **1.39× (+38.7%)** |

### 2. Paired Differences Across 20 Matched Image-Seed Pairs

Evaluating paired differences on identical degraded observations isolates algorithm behavior from noise realization variance:

- **Coarse PnP vs. Direct DPIR:** Mean **+0.1820 dB** (std 0.1714 dB); positive gain in **20 / 20 pairs (100.0%)**.
- **Observation Init vs. Direct DPIR:** Mean **+0.1183 dB** (std 0.1222 dB); positive gain in **18 / 20 pairs (90.0%)** (with slight negative differences on Chelsea seed 2227 [-0.0008 dB] and Rocket seed 2029 [-0.0018 dB]).
- **Coarse PnP vs. Observation Init:** Mean **+0.0637 dB** (std 0.0585 dB); positive gain in **20 / 20 pairs (100.0%)**.

### 3. Per-Image Breakdown

| Test Image | Coarse vs. Direct | Coarse vs. Obs Init | Obs Init vs. Direct | Content Characteristics |
|---|---:|---:|---:|---|
| **Coffee** | **+0.3972 dB** | +0.1118 dB | +0.2854 dB | Broad smooth gradients, uniform cup surface |
| **Astronaut** | **+0.2868 dB** | +0.1120 dB | +0.1748 dB | Mixed structural contours, portrait tones |
| **Rocket** | **+0.0289 dB** | +0.0235 dB | +0.0054 dB | Sharp high-contrast structural edges |
| **Chelsea** | **+0.0149 dB** | +0.0073 dB | +0.0076 dB | High-frequency fur and whisker textures |

## Scientific Interpretation and Methodological Scoping

1. **Empirical Hypothesis on Smoothing:** In this specific benchmark, observation initialization alone accounted for ~65% (+0.1183 dB) of the coarse-to-fine gain, while coarse learned denoising contributed the remaining ~35% (+0.0637 dB). This supports the hypothesis that low-pass filtering from resolution cycling removes high-frequency noise prior to iterative optimization, but should not be interpreted as an established universal causal proof across other forward models or image distributions.
2. **Frequency Sensitivity:** Performance gains correlate strongly with image spatial frequencies: smooth images with broad gradients (Coffee, Astronaut) show notable improvements, whereas dense texture images (Chelsea, Rocket) show negligible differences, as 64×64 downsampling eliminates fine spatial detail.
3. **Computational Trade-Off:** Coarse PnP initialization requires **38.7% additional runtime** (0.3772 s vs. 0.2719 s). Whether a modest +0.18 dB gain justifies this overhead depends strictly on application constraints (e.g., viable for offline imaging, prohibitive for real-time video).
4. **Coarse Forward Operator Approximation:** The coarse blur model was approximated by parameterizing a Gaussian blur kernel with $\sigma_b = 1.0$ and noise $\sigma_n = 0.015$ on $64 \times 64$, rather than forming a mathematically exact Galerkin restriction operator $A_c = R A P$.
5. **Sample Size Limitations:** Replicate noise seeds on the same four images are correlated at the image level; sixty reconstruction runs across four images do not constitute sixty statistically independent image samples. Generalization across natural image populations requires broader evaluation.
6. **Coupled Robustness Scope:** In exploratory degradation experiments (E1: $\sigma_b=1.0, \sigma_n=0.01$; E2: $\sigma_b=2.0, \sigma_n=0.03$; E3: $\sigma_b=3.0, \sigma_n=0.05$), blur and noise were increased together. These tests evaluate combined degradation severity and do not isolate blur from noise.
7. **Model Scoping Declaration:** This benchmark evaluates existing pretrained DRUNet weights with DeepInverse DPIR. **No generative flow-matching model or diffusion model was trained or tested.**

## Provenance and Reproducibility

- Notebook: `notebooks/DeepInverse_PnP_Image_Restoration.ipynb`
- Automated CSV validation: `scripts/validate_results.py`
- Raw metrics: `results/step10_all_experiments.csv`
- Cryptographic verification: `SHA256SUMS.txt`
