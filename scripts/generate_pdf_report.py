"""
Generate a professional, publication-grade research report PDF (exactly 6 pages).
Features:
- Title in EXACTLY 2 lines (centered, bold)
- Author (Hasnain Haider) centered directly below title
- Subtitle: Independent Research Benchmark (centered)
- 100% black typography for human academic print with justified text
- Full-border academic tables with clean outer borders and inner grids
- Prominent, un-truncated, fully verified REFERENCES section
- Balanced 6-page budget with zero overflow
"""
import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, KeepTogether, HRFlowable, PageBreak
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas

W, H = letter  # 612 x 792 points


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved = []

    def showPage(self):
        self._saved.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._saved)
        for state in self._saved:
            self.__dict__.update(state)
            self._decorate(total)
            super().showPage()
        super().save()

    def _decorate(self, total):
        self.saveState()
        # Header on pages 2..total
        if self._pageNumber > 1:
            self.setFont('Times-Bold', 8.0)
            self.setFillColor(colors.black)
            self.drawString(54, H - 34, 'HASNAIN HAIDER')
            self.setFont('Times-Roman', 8.0)
            self.drawString(136, H - 34, '— Plug-and-Play Image Restoration with Coarse-to-Fine Initialization')
            self.drawRightString(W - 54, H - 34, 'RESEARCH REPORT')
            self.setStrokeColor(colors.black)
            self.setLineWidth(0.6)
            self.line(54, H - 38, W - 54, H - 38)
            
        # Footer on all pages
        self.setStrokeColor(colors.black)
        self.setLineWidth(0.6)
        self.line(54, 38, W - 54, 38)
        self.setFont('Times-Roman', 8.0)
        self.setFillColor(colors.black)
        self.drawString(54, 27, 'Independent Research Benchmark • github.com/Hasnain006-nain/deepinverse-pnp-image-restoration')
        self.drawRightString(W - 54, 27, f'Page {self._pageNumber} of {total}')
        self.restoreState()


# Style helper
def S(name, font='Times-Roman', size=9.0, leading=11.8, align=TA_JUSTIFY,
      color='#000000', spaceBefore=0, spaceAfter=3.0, bold=False, italic=False,
      keepWithNext=False, leftIndent=0):
    if bold and italic:
        font = 'Times-BoldItalic'
    elif bold:
        font = 'Times-Bold'
    elif italic:
        font = 'Times-Italic'
    return ParagraphStyle(
        name, fontName=font, fontSize=size, leading=leading,
        alignment=align, textColor=colors.HexColor(color),
        spaceBefore=spaceBefore, spaceAfter=spaceAfter,
        keepWithNext=keepWithNext, leftIndent=leftIndent
    )

# Typography styles
title_style = S('DocTitle', size=13.5, leading=17.0, align=TA_CENTER, bold=True, spaceAfter=4)
author_style = S('DocAuthor', size=10.5, leading=13.5, align=TA_CENTER, bold=True, spaceAfter=2)
affil_style = S('DocAffil', size=8.5, leading=11.0, align=TA_CENTER, italic=True, spaceAfter=4)

h1_style = S('H1', size=10.0, leading=12.5, bold=True, spaceBefore=6, spaceAfter=2.5, keepWithNext=True, align=TA_LEFT)
h2_style = S('H2', size=9.0, leading=11.5, bold=True, spaceBefore=4, spaceAfter=2.0, keepWithNext=True, align=TA_LEFT)
body_style = S('Body', size=8.3, leading=10.8, align=TA_JUSTIFY, spaceAfter=2.8)
body_indent = S('BodyIndent', size=8.3, leading=10.8, align=TA_JUSTIFY, leftIndent=10, spaceAfter=2.0)
caption_style = S('Caption', size=7.6, leading=9.5, align=TA_CENTER, italic=True, spaceBefore=1.5, spaceAfter=3.5)

# Table cell styles
tc = S('TC', size=7.8, leading=9.5, align=TA_CENTER)
tcl = S('TCL', size=7.8, leading=9.5, align=TA_LEFT)
tcb = S('TCB', size=7.8, leading=9.5, align=TA_CENTER, bold=True)
tclb = S('TCLB', size=7.8, leading=9.5, align=TA_LEFT, bold=True)

# References typography (Prominent, cleanly formatted)
ref_header_style = S('RefHeader', size=10.5, leading=13.0, bold=True, spaceBefore=6, spaceAfter=3.0, align=TA_LEFT)
ref_num = S('RefNum', size=8.0, leading=10.2, bold=True, align=TA_LEFT)
ref_text = S('RefText', size=8.0, leading=10.2, align=TA_JUSTIFY, spaceAfter=1.0)
ref_note = S('RefNote', size=7.0, leading=8.5, italic=True, color='#222222', spaceAfter=3.5, align=TA_LEFT, leftIndent=6)

P = Paragraph


def make_full_border_table(data, col_widths=None):
    """Creates a clean academic table with COMPLETE FULL BORDERS on all cells."""
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ('BOX', (0, 0), (-1, -1), 1.0, colors.black),              # Solid full outer border
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#333333')), # Full inner cell borders
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#EBEBEB')),     # Clean header background
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 4.0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4.0),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#F8F8F8')))
    t.setStyle(TableStyle(style_cmds))
    return t


def build_pdf(out_path):
    FIG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'figures'))
    
    # Printable area: 504 pt width x 704 pt height
    doc = SimpleDocTemplate(
        out_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=44,
        bottomMargin=44
    )
    story = []

    # =========================================================================
    # PAGE 1: Title (EXACTLY 2 LINES), Author (Hasnain Haider), Abstract, Intro, Setup & Fig 1
    # =========================================================================
    story.append(P("Plug-and-Play Image Restoration with Coarse-to-Fine Initialization:<br/>An Empirical Benchmark Using DeepInverse and DRUNet", title_style))
    story.append(P("Hasnain Haider", author_style))
    story.append(P("Independent Research Benchmark", affil_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.black, spaceBefore=1, spaceAfter=4))

    # Abstract Container with Full Border
    abs_content = (
        "<b>Abstract</b>—This benchmark investigates whether a two-level coarse-to-fine initialization improves "
        "Plug-and-Play (PnP) image restoration when paired with a deep denoiser prior. Using the DeepInverse framework [1] "
        "and pretrained DRUNet weights [2], we evaluated three initialization pipelines on four standard test images "
        "(Astronaut, Chelsea, Coffee, Rocket) degraded by Gaussian blur (&sigma; = 2.0) and additive Gaussian noise (&sigma; = 0.03). "
        "Across 20 paired image-seed trials (60 total runs on an NVIDIA Tesla T4 GPU), coarse PnP initialization achieved a mean PSNR "
        "of 28.593 dB compared to 28.411 dB for standard direct DPIR and 28.530 dB for observation-only initialization. "
        "The coarse PnP pipeline achieved a positive paired gain in 100% of trials (+0.182 dB average), but incurred a 38.7% "
        "runtime penalty. Notably, 65% of this improvement (+0.118 dB) is obtained solely from resolution downsampling and upsampling, "
        "while active coarse denoising contributes the remaining +0.064 dB. Benefits are highest for smooth surfaces (+0.397 dB) "
        "and negligible for high-frequency textures (+0.015 dB). All reproduction scripts and CSV metrics are publicly available."
    )
    abs_table = Table([[P(abs_content, S('AbsStyle', size=8.0, leading=10.6, align=TA_JUSTIFY))]], colWidths=[504])
    abs_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.8, colors.black),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F9F9F9')),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 7.0),
        ('RIGHTPADDING', (0,0), (-1,-1), 7.0),
    ]))
    story.append(abs_table)
    story.append(Spacer(1, 3))

    story.append(P("1. Introduction and Problem Context", h1_style))
    story.append(P(
        "Linear inverse problems in computational imaging require reconstructing an uncorrupted image <i>x</i> &isin; &real;<sup><i>n</i></sup> "
        "from degraded measurements <i>y</i> = <b>A</b><i>x</i> + <i>n</i>, where <b>A</b> is a linear operator (such as a blur point spread function) "
        "and <i>n</i> ~ &Nu;(0, &sigma;<sup>2</sup><b>I</b>) represents additive measurement noise. Because <b>A</b> is severely ill-conditioned, "
        "naive pseudoinverse solutions blow up noise variance, necessitating explicit or implicit image priors to regularize the solution manifold.",
        body_style
    ))
    story.append(P(
        "Plug-and-Play (PnP) methods, introduced by Venkatakrishnan et al. [3], replace hand-crafted mathematical regularizers with advanced "
        "image denoisers within variable-splitting schemes such as Half-Quadratic Splitting (HQS) or ADMM. Zhang et al. [2] developed DPIR, "
        "embedding a Deep Residual U-Net (DRUNet) into HQS to obtain high-fidelity reconstructions across deblurring, super-resolution, and "
        "inpainting tasks without retraining network parameters for individual forward models.",
        body_style
    ))
    story.append(P(
        "Standard DPIR begins its iterative optimization directly from the degraded observation: <i>x</i><sub>0</sub> = <i>y</i>. "
        "Drawing from multigrid concepts in scientific computing, we investigate whether a coarse-scale warm-start improves convergence "
        "and final restoration fidelity. We implement and evaluate this approach systematically using the open-source DeepInverse package [1].",
        body_style
    ))

    story.append(P("2. Forward Degradation Model and Benchmark Setup", h1_style))
    story.append(P(
        "We selected four standard benchmark images from scikit-image: Astronaut (portrait with mixed geometric contours), "
        "Chelsea (tabby cat featuring high-frequency fur patterns), Coffee (ceramic cup with broad uniform gradients), and Rocket "
        "(launch vehicle with high-contrast structural edges). Images were scaled to 128 &times; 128 pixels with pixel values normalized to [0, 1].",
        body_style
    ))
    story.append(P(
        "The degradation operator <b>A</b> applies a 7 &times; 7 Gaussian blur kernel with standard deviation &sigma; = 2.0, followed by "
        "additive Gaussian noise with &sigma; = 0.03. Five independent noise seeds (0 through 4) were applied to each image, generating "
        "20 distinct observation instances. Identical inputs were fed across all three initialization pipelines.",
        body_style
    ))

    fig_deg = os.path.join(FIG_DIR, 'step2_degradation.png')
    if os.path.exists(fig_deg):
        story.append(Spacer(1, 1))
        story.append(Image(fig_deg, width=440, height=135))
        story.append(P("Figure 1. Forward degradation pipeline: clean reference, Gaussian blur PSF, 2D frequency spectrum showing attenuation, and noisy observation.", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: Pipelines, Protocol, Results & Tables 1, 2, 3 (Full Borders)
    # =========================================================================
    story.append(P("3. Evaluated Reconstruction Pipelines", h1_style))
    story.append(P(
        "All pipelines use the identical pretrained DRUNet model checkpoint and an 8-iteration HQS schedule. "
        "The sole variable across conditions is the initial state <i>x</i><sub>0</sub>:",
        body_style
    ))
    story.append(P("• <b>Direct DPIR (Baseline):</b> Optimization begins directly at the corrupted measurement, <i>x</i><sub>0</sub> = <i>y</i>.", body_indent))
    story.append(P("• <b>Observation Initialization (Control):</b> <i>y</i> is downsampled to 64 &times; 64 and bicubic-upsampled back to 128 &times; 128, serving as <i>x</i><sub>0</sub> without coarse denoising to isolate resolution-cycling effects.", body_indent))
    story.append(P("• <b>Coarse PnP Initialization (Proposed):</b> A complete DPIR solve is performed at 64 &times; 64 resolution using a scaled blur operator. The coarse result is upsampled to 128 &times; 128 to warm-start the fine-scale solver.", body_indent))

    story.append(P("4. Experimental Evaluation Protocol", h1_style))
    story.append(P(
        "Performance is measured via Peak Signal-to-Noise Ratio (PSNR) and Structural Similarity (SSIM) computed on clipped RGB values "
        "against the ground truth. Wall-clock runtimes were recorded with CUDA synchronization on an NVIDIA Tesla T4 GPU. "
        "To eliminate noise sample variance, we evaluate paired differences (&Delta;PSNR) across identical degraded inputs.",
        body_style
    ))

    story.append(P("5. Quantitative Findings and Empirical Analysis", h1_style))
    story.append(P("5.1 Aggregate Performance across 60 Experiments", h2_style))
    story.append(P(
        "Table 1 reports the aggregate results over all 60 trials (4 images &times; 5 seeds &times; 3 pipelines). "
        "Coarse PnP initialization achieves the highest overall PSNR and SSIM, followed by observation initialization.",
        body_style
    ))

    t1_data = [
        [P("<b>Pipeline Strategy</b>", tclb), P("<b>Mean PSNR (dB)</b>", tcb), P("<b>Mean SSIM</b>", tcb), P("<b>Mean Runtime (s)</b>", tcb), P("<b>Relative Time</b>", tcb)],
        [P("Direct DPIR (Baseline)", tcl), P("28.411", tc), P("0.8588", tc), P("0.2719", tc), P("1.00&times; (baseline)", tc)],
        [P("Observation Init (Control)", tcl), P("28.530", tc), P("0.8603", tc), P("0.2735", tc), P("1.01&times; (+0.6%)", tc)],
        [P("Coarse PnP Init (Proposed)", tcl), P("<b>28.593</b>", tc), P("<b>0.8622</b>", tc), P("0.3772", tc), P("1.39&times; (+38.7%)", tc)],
    ]
    story.append(make_full_border_table(t1_data, col_widths=[140, 90, 80, 95, 99]))
    story.append(P("Table 1. Aggregate restoration performance across 60 experiments on Tesla T4 GPU. Bold figures indicate best results.", caption_style))

    story.append(P("5.2 Paired Differences and Consistency Analysis", h2_style))
    story.append(P(
        "Evaluating paired differences on identical observations confirms that coarse PnP initialization outperformed direct DPIR in "
        "<b>20 out of 20 trials (100% win rate)</b>, yielding an average gain of +0.182 dB. It also surpassed observation initialization in "
        "all 20 trials (+0.064 dB average gain). Importantly, observation initialization alone gained +0.118 dB over direct DPIR, "
        "showing that nearly two-thirds of the total advantage stems from initial low-pass smoothing.",
        body_style
    ))

    t2_data = [
        [P("<b>Paired Comparison</b>", tclb), P("<b>Mean &Delta;PSNR</b>", tcb), P("<b>Std. Dev.</b>", tcb), P("<b>Positive Trials</b>", tcb), P("<b>Win Rate</b>", tcb)],
        [P("Coarse PnP vs. Direct DPIR", tcl), P("+0.1820 dB", tc), P("0.162 dB", tc), P("20 / 20", tc), P("100.0%", tc)],
        [P("Observation Init vs. Direct DPIR", tcl), P("+0.1183 dB", tc), P("0.114 dB", tc), P("20 / 20", tc), P("100.0%", tc)],
        [P("Coarse PnP vs. Observation Init", tcl), P("+0.0637 dB", tc), P("0.051 dB", tc), P("20 / 20", tc), P("100.0%", tc)],
    ]
    story.append(make_full_border_table(t2_data, col_widths=[150, 90, 80, 95, 89]))
    story.append(P("Table 2. Paired difference statistics across 20 image-seed pairs. Gains are strictly positive in every trial.", caption_style))

    story.append(P("5.3 Per-Image Frequency Sensitivity Breakdown", h2_style))
    story.append(P(
        "Gains are strongly correlated with image frequency content. Coffee (smooth surfaces and broad tonal gradients) gained +0.397 dB, "
        "and Astronaut (mixed portrait geometry) gained +0.287 dB. In contrast, Rocket (+0.029 dB) and Chelsea (+0.015 dB) showed minimal "
        "change, as downsampling to 64 &times; 64 discards the high-frequency edge and texture information essential to their restoration.",
        body_style
    ))

    t3_data = [
        [P("<b>Image</b>", tclb), P("<b>Coarse vs. Direct</b>", tcb), P("<b>Coarse vs. Obs Init</b>", tcb), P("<b>Obs vs. Direct</b>", tcb), P("<b>Dominant Texture Characteristics</b>", tcl)],
        [P("Coffee", tcl), P("+0.397 dB", tc), P("+0.112 dB", tc), P("+0.285 dB", tc), P("Broad smooth gradients, uniform cup surface", tcl)],
        [P("Astronaut", tcl), P("+0.287 dB", tc), P("+0.112 dB", tc), P("+0.175 dB", tc), P("Mixed structural contours and portrait details", tcl)],
        [P("Rocket", tcl), P("+0.029 dB", tc), P("+0.024 dB", tc), P("+0.005 dB", tc), P("High-contrast boundary edges and sky background", tcl)],
        [P("Chelsea", tcl), P("+0.015 dB", tc), P("+0.007 dB", tc), P("+0.008 dB", tc), P("High-frequency fur and whisker textures", tcl)],
    ]
    story.append(make_full_border_table(t3_data, col_widths=[75, 90, 90, 85, 164]))
    story.append(P("Table 3. Paired PSNR gains categorized by test image and frequency characteristics.", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: Figures 2 & 3, Baseline TV Comparison & Table 4 (Full Borders)
    # =========================================================================
    story.append(P("5.4 Per-Seed Ablation Distribution", h2_style))
    
    fig_abl = os.path.join(FIG_DIR, 'step10_initialization_ablation.png')
    if os.path.exists(fig_abl):
        story.append(Image(fig_abl, width=440, height=165))
        story.append(P("Figure 2. Per-seed PSNR across initialization methods. Coarse PnP (green) consistently exceeds direct DPIR (blue) on Coffee and Astronaut, while Chelsea and Rocket exhibit minimal variance.", caption_style))

    story.append(P("6. Baseline Benchmark: Classical Total Variation vs. Learned DPIR", h1_style))
    story.append(P(
        "To contextualize the restoration fidelity of the learned DRUNet prior, we benchmarked standard DPIR against classical "
        "Total Variation (TV) regularized inversion solved via Proximal Gradient Descent (TV-PGD) [5] under identical degradation.",
        body_style
    ))

    t4_data = [
        [P("<b>Image</b>", tclb), P("<b>Degraded</b>", tcb), P("<b>TV-PGD [5]</b>", tcb), P("<b>DPIR [2]</b>", tcb), P("<b>DPIR Gain</b>", tcb), P("<b>TV Time</b>", tcb), P("<b>DPIR Time</b>", tcb)],
        [P("Astronaut", tcl), P("19.18 dB", tc), P("22.23 dB", tc), P("24.13 dB", tc), P("+1.90 dB", tc), P("2.64 s", tc), P("0.37 s", tc)],
        [P("Chelsea", tcl), P("24.57 dB", tc), P("27.22 dB", tc), P("29.74 dB", tc), P("+2.52 dB", tc), P("2.66 s", tc), P("0.35 s", tc)],
        [P("Coffee", tcl), P("22.12 dB", tc), P("25.95 dB", tc), P("27.84 dB", tc), P("+1.89 dB", tc), P("2.35 s", tc), P("0.37 s", tc)],
        [P("Rocket", tcl), P("25.92 dB", tc), P("29.15 dB", tc), P("31.81 dB", tc), P("+2.66 dB", tc), P("2.61 s", tc), P("0.36 s", tc)],
    ]
    story.append(make_full_border_table(t4_data, col_widths=[74, 65, 75, 75, 75, 70, 70]))
    story.append(P("Table 4. Classical TV-PGD versus learned DRUNet DPIR. Learned DPIR provides +1.89 to +2.66 dB higher PSNR while running ~7&times; faster.", caption_style))

    story.append(P(
        "As detailed in Table 4, DPIR outperforms TV-PGD by +1.89 dB to +2.66 dB across all images while running ~7&times; faster. "
        "TV-PGD introduces severe staircasing artifacts on smooth facial regions and gradients, whereas DRUNet produces natural textures.",
        body_style
    ))

    fig_tv = os.path.join(FIG_DIR, 'step7_method_comparison.png')
    if os.path.exists(fig_tv):
        story.append(Spacer(1, 1))
        story.append(Image(fig_tv, width=440, height=205))
        story.append(P("Figure 3. Visual comparison of ground truth, degraded observation, TV-PGD reconstruction, and DRUNet DPIR across the benchmark set.", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: Multilevel Stages, Convergence, Figures 4 & 5
    # =========================================================================
    story.append(P("7. Stage-by-Stage Visual Progression in Two-Level Restoration", h1_style))
    story.append(P(
        "Figure 4 tracks the intermediate states of the coarse-to-fine restoration. The initial 64 &times; 64 reconstruction recovers global "
        "luminance and primary edges while suppressing sensor noise. After bicubic prolongation and the fine-scale DPIR pass, "
        "fine details and edge crispness are substantially enhanced.",
        body_style
    ))

    fig_ml = os.path.join(FIG_DIR, 'step9_multilevel_comparison.png')
    if os.path.exists(fig_ml):
        story.append(Image(fig_ml, width=440, height=220))
        story.append(P("Figure 4. Progression through the two-level pipeline: degraded input, coarse 64 &times; 64 restoration, upsampled prolongation, and refined 128 &times; 128 output.", caption_style))

    story.append(Spacer(1, 3))
    story.append(P("8. Convergence Dynamics and Numerical Stability", h1_style))
    story.append(P(
        "We tracked PSNR progression and relative solution residuals ||<i>x</i><sup>(<i>k</i>)</sup> - <i>x</i><sup>(<i>k</i>-1)</sup>|| / ||<i>x</i><sup>(<i>k</i>)</sup>|| "
        "across iterations. As illustrated in Figure 5, the solver makes rapid early progress: PSNR climbs steeply across iterations 1–4 and asymptotes by iteration 6. "
        "Relative residuals decline below 10<sup>-2</sup> within 5 iterations across all setups, demonstrating dependable numerical convergence.",
        body_style
    ))

    fig_psnr_iter = os.path.join(FIG_DIR, 'step8_psnr_vs_iterations.png')
    fig_resid = os.path.join(FIG_DIR, 'step8_convergence_residual.png')
    if os.path.exists(fig_psnr_iter) and os.path.exists(fig_resid):
        conv_tbl = Table([
            [Image(fig_psnr_iter, width=220, height=110), Image(fig_resid, width=220, height=110)]
        ], colWidths=[252, 252])
        conv_tbl.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(conv_tbl)
        story.append(P("Figure 5. Iteration-level convergence. Left: PSNR ascent across HQS iterations. Right: logarithmic decay of relative residual, demonstrating convergence within 5–6 steps.", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: Noise Robustness, Figures 6 & 7, Discussion
    # =========================================================================
    story.append(P("9. Robustness under Varying Noise Intensities", h1_style))
    story.append(P(
        "To test whether the DRUNet prior maintains stability under severe corruption, we benchmarked restorations across noise levels "
        "ranging from &sigma; = 0.01 to &sigma; = 0.07. As shown in Figures 6 and 7, reconstruction PSNR degrades smoothly and monotonically. "
        "The model produces no high-frequency artifacts or color inversions even under heavy noise (&sigma; = 0.07).",
        body_style
    ))

    fig_rob = os.path.join(FIG_DIR, 'step6_psnr_robustness.png')
    fig_vis = os.path.join(FIG_DIR, 'step6_visual_comparison.png')
    if os.path.exists(fig_rob) and os.path.exists(fig_vis):
        rob_tbl = Table([
            [Image(fig_rob, width=205, height=135), Image(fig_vis, width=275, height=135)]
        ], colWidths=[220, 284])
        rob_tbl.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(rob_tbl)
        story.append(P("Figures 6 & 7. Left: PSNR vs. noise standard deviation &sigma;. Right: visual restoration quality under increasing noise levels (&sigma; = 0.01 to 0.07).", caption_style))

    story.append(Spacer(1, 3))
    story.append(P("10. Discussion and Engineering Trade-Off Analysis", h1_style))
    story.append(P(
        "The empirical data establishes a consistent (+0.182 dB, 100% positive) benefit for coarse PnP initialization. "
        "Crucially, our control condition explains where this gain originates: roughly 65% (+0.118 dB) is produced by low-pass smoothing "
        "inherent in the bicubic resolution cycling, which suppresses high-frequency observation noise before fine-scale iterations begin. "
        "The active coarse DRUNet denoising solve contributes the remaining 35% (+0.064 dB).",
        body_style
    ))
    story.append(P(
        "Whether this benefit is worth deploying depends on application constraints. Coarse PnP initialization requires 0.377 s per image "
        "on a Tesla T4 GPU versus 0.272 s for direct DPIR—a 38.7% runtime increase. In offline computational imaging (such as scientific, "
        "astronomical, or medical post-processing), spending an extra 0.1 s per image for consistent quality improvement is fully acceptable. "
        "In high-frame-rate or edge video processing, this overhead would be difficult to justify for a modest fraction of a decibel.",
        body_style
    ))
    story.append(P(
        "Additionally, performance gains depend heavily on scene semantics. Images dominated by broad tonal transitions and low-frequency "
        "gradients (Coffee: +0.397 dB) benefit substantially. Images dominated by high-frequency textures (Chelsea: +0.015 dB) gain virtually "
        "nothing, because 64 &times; 64 downsampling eliminates the very spatial frequencies required to reconstruct fine detail.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: Limitations, Table 5 (Full Border), Conclusion & PROMINENT REFERENCES
    # =========================================================================
    story.append(P("11. Limitations and Threats to Validity", h1_style))
    story.append(P("We explicitly report the following experimental constraints in this study:", body_style))
    
    limits = [
        ("Image sample size: ", "Four images evaluated across five seeds demonstrate consistency on this sample, but do not support population-wide statistical claims across heterogeneous natural image distributions."),
        ("Heuristic coarse operator: ", "The 64 &times; 64 blur operator was constructed by downsampling the fine kernel rather than deriving an exact Galerkin restriction operator <b>A</b><sub><i>c</i></sub> = <b>R</b><b>A</b><b>P</b>."),
        ("Scope declaration: ", "This study benchmarks standard DRUNet-based PnP-DPIR. It does not evaluate score-based diffusion models or generative flow-matching algorithms [4]."),
        ("Single hardware environment: ", "All runs were performed on a single Google Colab Tesla T4 instance. While deterministic seeds and checksums ensure repeatability, cross-hardware verification remains future work.")
    ]
    for lbl, txt in limits:
        story.append(P(f"• <b>{lbl}</b>{txt}", body_indent))

    story.append(Spacer(1, 2))
    story.append(P("12. Reproducibility Protocol and Environment", h1_style))
    story.append(P(
        "All code is provided in <code>notebooks/DeepInverse_PnP_Image_Restoration.ipynb</code>. Running cells sequentially "
        "reproduces all 60 executions and saves raw metrics to <code>results/step10_all_experiments.csv</code>. File integrity is verified "
        "via cryptographic hashes recorded in <code>SHA256SUMS.txt</code>.",
        body_style
    ))

    t_env_data = [
        [P("<b>Software / Hardware Layer</b>", tclb), P("<b>Recorded Version / Specification</b>", tcb)],
        [P("Python Runtime Environment", tcl), P("3.13.16", tc)],
        [P("PyTorch Deep Learning Framework", tcl), P("2.11.0+cu130", tc)],
        [P("DeepInverse Computational Imaging Library [1]", tcl), P("0.5.0", tc)],
        [P("NumPy / Matplotlib / scikit-image", tcl), P("2.1.3 / 3.10.0 / 0.25.2", tc)],
        [P("Hardware Acceleration", tcl), P("NVIDIA Tesla T4 GPU (16 GB VRAM)", tc)],
    ]
    story.append(make_full_border_table(t_env_data, col_widths=[220, 284]))
    story.append(P("Table 5. Documented hardware and software execution environment (full-border verification).", caption_style))

    story.append(Spacer(1, 2))
    story.append(P("13. Conclusion", h1_style))
    story.append(P(
        "Two-level coarse-to-fine initialization yields a small (+0.182 dB) but remarkably consistent (20/20 positive) improvement "
        "for PnP-DPIR image restoration on small images. The effect is driven primarily by low-pass initialization smoothing with a "
        "secondary contribution from coarse denoising, at the cost of a 38.7% runtime increase. Future work will investigate whether "
        "rigorous multigrid operator restrictions can amplify these gains on large-scale (512 &times; 512 and larger) imaging problems.",
        body_style
    ))

    story.append(Spacer(1, 2))
    
    # ─── SECTION 14: VERIFIED ACADEMIC REFERENCES (PROMINENT, VISIBLE, FULLY CITED) ───
    story.append(P("14. Verified Academic References", ref_header_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.black, spaceBefore=1, spaceAfter=4))

    verified_refs = [
        ("<b>[1]</b>",
         "J. Tachella, M. Terris, S. Hurault, A. Wang, et al., \"DeepInverse: A Python package for solving imaging inverse problems with deep learning,\" <i>Journal of Open Source Software</i>, vol. 10, no. 115, p. 8923, 2025.",
         "% Verified via CrossRef / JOSS DOI: https://doi.org/10.21105/joss.08923 (also arXiv:2505.20160), checked 2026-10-30"),
        ("<b>[2]</b>",
         "K. Zhang, Y. Li, W. Zuo, L. Zhang, L. Van Gool, and R. Timofte, \"Plug-and-Play Image Restoration with Deep Denoiser Prior,\" <i>IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI)</i>, vol. 44, no. 10, pp. 6360–6376, Oct. 2022.",
         "% Verified via IEEE Xplore DOI: https://doi.org/10.1109/TPAMI.2021.3088914, checked 2026-10-30"),
        ("<b>[3]</b>",
         "S. V. Venkatakrishnan, C. A. Bouman, and B. Wohlberg, \"Plug-and-Play Priors for Model Based Reconstruction,\" in <i>IEEE Global Conference on Signal and Information Processing (GlobalSIP)</i>, pp. 945–948, Dec. 2013.",
         "% Verified via IEEE Xplore DOI: https://doi.org/10.1109/GlobalSIP.2013.6737048, checked 2026-10-30"),
        ("<b>[4]</b>",
         "S. Martin, A. Gagneux, P. Hagemann, and G. Steidl, \"PnP-Flow: Plug-and-Play Image Restoration with Flow Matching,\" in <i>International Conference on Learning Representations (ICLR)</i>, 2025.",
         "% Verified via OpenReview: https://openreview.net/forum?id=V2c2YxK0eG (also arXiv:2410.21200), checked 2026-10-30"),
        ("<b>[5]</b>",
         "L. I. Rudin, S. Osher, and E. Fatemi, \"Nonlinear total variation based noise removal algorithms,\" <i>Physica D: Nonlinear Phenomena</i>, vol. 60, no. 1–4, pp. 259–268, 1992.",
         "% Verified via ScienceDirect / Elsevier DOI: https://doi.org/10.1016/0167-2789(92)90242-F, checked 2026-10-30"),
    ]

    for num_str, cit_str, prov_str in verified_refs:
        ref_table = Table([
            [P(num_str, ref_num), P(cit_str, ref_text)]
        ], colWidths=[20, 484])
        ref_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0.5),
        ]))
        story.append(ref_table)
        story.append(P(prov_str, ref_note))

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated PDF at: {out_path}")


if __name__ == '__main__':
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    out_pdf = os.path.join(root_dir, 'DeepInverse_PnP_Research_Report.pdf')
    docs_pdf = os.path.join(root_dir, 'docs', 'DeepInverse_PnP_Research_Report.pdf')
    
    build_pdf(out_pdf)
    
    import shutil
    shutil.copyfile(out_pdf, docs_pdf)
    print(f"Copied to: {docs_pdf}")
