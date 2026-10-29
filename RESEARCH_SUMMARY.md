# Research Summary — DeepInverse Plug-and-Play Image Restoration

**Project type:** Reproducible exploratory image restoration benchmark.  
**System:** Google Colab, NVIDIA Tesla T4; Python 3.13, PyTorch 2.11.0, DeepInverse 0.5.0.  
**Restoration prior:** Pretrained DRUNet (no training performed).  
**Primary question:** Does two-level coarse-to-fine initialization improve standard DPIR reconstruction on small RGB images?

## Design

Four scikit-image examples (Astronaut, Chelsea, Coffee, Rocket) were resized to 128 × 128. Synthetic Gaussian blurring (sigma 2.0) and measurement noise (sigma 0.03) were applied. Each of five random seeds produced **one observation per image**, passed unchanged to three methods:

1. **Direct DPIR:** Standard reconstruction from the observation.
2. **Observation initialization:** Downsampled and upsampled observation used as the fine-scale initialization, without a coarse denoiser.
3. **Coarse PnP initialization:** 64 × 64 DPIR reconstruction, upsampled to initialize 128 × 128 DPIR.

For each image and seed, outputs were evaluated using clipped RGB PSNR, SSIM, and GPU-synchronized wall-clock inference timing. Coarse total runtime includes both coarse and fine reconstruction stages. Results reflect the recorded runs, not new measurements.

## Observed results

| Method | Mean PSNR | Mean SSIM | Mean runtime (T4) |
|---|---:|---:|---:|
| Coarse PnP Init | 28.593 dB | 0.8622 | 0.3772 s |
| Direct DPIR | 28.411 dB | 0.8588 | 0.2719 s |
| Observation Init | 28.530 dB | 0.8603 | 0.2735 s |

**Paired differences across 20 image-seed pairs:** Coarse PnP vs direct **+0.1820 dB**; observation init vs direct **+0.1183 dB**; coarse PnP vs observation **+0.0637 dB**. All 20 coarse-vs-direct and all 20 coarse-vs-observation PSNR comparisons were positive. Results were not independently replicated in a fresh environment during this audit.

| Image | Coarse vs direct | Coarse vs observation |
|---|---:|---:|
| Astronaut | +0.287 dB | +0.112 dB |
| Chelsea | +0.015 dB | +0.007 dB |
| Coffee | +0.397 dB | +0.112 dB |
| Rocket | +0.029 dB | +0.024 dB |

The average coarse-to-fine runtime is **38.7% greater** than direct DPIR. Gains are small and vary notably by image. In earlier exploratory TV-PGD comparisons, DPIR attained 28.38 dB versus TV-PGD 26.14 dB on four images at moderate degradation; that TV baseline was **not comprehensively tuned**.

## Interpretation and limitations

These data support a **small but consistently positive paired PSNR change on this particular sample and configuration**, at higher computational cost. They do **not** establish general superiority, model-independent convergence, statistical significance across image populations, or a new multilevel method. Seed replicates on the same four pictures are correlated at the image level. The approximate coarse inverse operator was not derived as an exact restriction of the fine acquisition model. Additional datasets, independently tuned baselines, matched compute budgets, and uncertainty analysis are future work.

**No flow-matching model was trained or tested.** This is a related preparatory exercise, not a reproduction of the Inria multilevel flow-matching proposal.

## Reproduction and provenance

The code is in `notebooks/DeepInverse_PnP_Image_Restoration.ipynb`, input metrics in `results/step10_all_experiments.csv`, and source experiment outputs/figures in `results/` and `figures/`. The notebook's bulky execution outputs were removed for convenient GitHub viewing; the user's original ZIP contains the executed notebook. No original measurement values were modified.

## References

- DeepInverse documentation: https://deepinv.github.io/deepinv/
- DeepInverse source: https://github.com/deepinv/deepinv
- PnP-Flow paper implementation: https://github.com/annegnx/PnP-Flow
