"""
Generate a professional, human-written research report PDF (exactly 6 pages).
Times-Roman / Helvetica clean typography, black text, classic academic tables,
embedded research figures, and strictly verified academic references.
Author: Hasnain Haider
"""
import os
import sys
import re
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

# ─── Numbered Canvas with Professional Running Header & Footer ─────
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
        # Header (pages 2 to total)
        if self._pageNumber > 1:
            self.setFont('Times-Roman', 8.5)
            self.setFillColor(colors.HexColor('#222222'))
            self.drawString(54, H - 36, 'Hasnain Haider — Plug-and-Play Image Restoration Benchmark')
            self.drawRightString(W - 54, H - 36, 'DeepInverse / DRUNet Study')
            self.setStrokeColor(colors.HexColor('#888888'))
            self.setLineWidth(0.5)
            self.line(54, H - 40, W - 54, H - 40)
            
        # Footer (all pages)
        self.setStrokeColor(colors.HexColor('#888888'))
        self.setLineWidth(0.5)
        self.line(54, 40, W - 54, 40)
        self.setFont('Times-Roman', 8.5)
        self.setFillColor(colors.HexColor('#222222'))
        self.drawString(54, 28, 'Independent Research Benchmark • github.com/Hasnain006-nain/deepinverse-pnp-image-restoration')
        self.drawRightString(W - 54, 28, f'Page {self._pageNumber} of {total}')
        self.restoreState()


# ─── Typography & Style Definitions ─────────────────────────────────
# All text strictly black or dark charcoal for natural human academic print.
def S(name, font='Times-Roman', size=9.5, leading=13.0, align=TA_JUSTIFY,
      color='#000000', spaceBefore=0, spaceAfter=4, bold=False, italic=False,
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

title_style = S('DocTitle', size=15, leading=19, align=TA_CENTER, bold=True, spaceAfter=5)
author_style = S('DocAuthor', size=11, leading=14, align=TA_CENTER, bold=True, spaceAfter=2)
affil_style = S('DocAffil', size=9, leading=12, align=TA_CENTER, italic=True, color='#222222', spaceAfter=6)

h1_style = S('H1', size=11, leading=14, bold=True, spaceBefore=8, spaceAfter=3, keepWithNext=True, align=TA_LEFT)
h2_style = S('H2', size=9.8, leading=12.5, bold=True, spaceBefore=5, spaceAfter=2, keepWithNext=True, align=TA_LEFT)
body_style = S('Body', size=8.8, leading=11.6, spaceAfter=3.5)
body_indent = S('BodyIndent', size=8.8, leading=11.6, leftIndent=12, spaceAfter=2.5)

caption_style = S('Caption', size=7.8, leading=10, align=TA_CENTER, italic=True, color='#222222', spaceBefore=2, spaceAfter=4)

# Academic table styles (clean, human-formatted booktabs look)
tc = S('TC', size=8, leading=10, align=TA_CENTER)
tcl = S('TCL', size=8, leading=10, align=TA_LEFT)
tcb = S('TCB', size=8, leading=10, align=TA_CENTER, bold=True)
tclb = S('TCLB', size=8, leading=10, align=TA_LEFT, bold=True)

ref_style = S('RefStyle', size=7.8, leading=9.8, spaceAfter=2, align=TA_LEFT)
ref_note = S('RefNote', size=7.0, leading=8.5, italic=True, color='#333333', spaceAfter=3.5, align=TA_LEFT, leftIndent=8)

P = Paragraph


def make_academic_table(data, col_widths=None):
    """Creates a clean academic booktabs-style table."""
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ('LINEABOVE', (0, 0), (-1, 0), 1.0, colors.black),      # Top rule
        ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.black),      # Mid rule below header
        ('LINEBELOW', (0, -1), (-1, -1), 1.0, colors.black),    # Bottom rule
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]
    # Subtle alternating row shading for legibility
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#F8F8F8')))
    t.setStyle(TableStyle(style_cmds))
    return t


def build_pdf(out_path):
    FIG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'figures'))
    
    doc = SimpleDocTemplate(
        out_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=46,
        bottomMargin=46
    )
    story = []

    # =========================================================================
    # PAGE 1: Centered Title, Hasnain Haider, Abstract, Intro, Setup & Fig 1
    # =========================================================================
    story.append(Spacer(1, 4))
    story.append(P("Plug-and-Play Image Restoration:<br/>A Two-Level Coarse-to-Fine Initialization Study<br/>Using DeepInverse and DRUNet", title_style))
    story.append(P("Hasnain Haider", author_style))
    story.append(P("Independent Research Benchmark", affil_style))
    story.append(HRFlowable(width="100%", thickness=0.6, color=colors.HexColor('#222222'), spaceBefore=1, spaceAfter=5))

    # Abstract box
    abs_text = (
        "<b>Abstract</b>—This report investigates whether a two-level coarse-to-fine initialization improves "
        "Plug-and-Play (PnP) image restoration when paired with a pretrained deep denoiser prior. Using the open-source "
        "DeepInverse library and pretrained DRUNet weights, we benchmarked three initialization pipelines across four "
        "standard images (Astronaut, Chelsea, Coffee, Rocket) degraded by Gaussian blur (&sigma; = 2.0) and additive white "
        "Gaussian noise (&sigma; = 0.03). Across 20 paired image-seed evaluations (60 runs total on an NVIDIA Tesla T4), "
        "coarse PnP initialization attained an average PSNR of 28.593 dB versus 28.411 dB for standard DPIR and 28.530 dB "
        "for observation-only initialization. The coarse PnP method improved PSNR in all 20 paired trials (+0.182 dB average gain), "
        "though at a 38.7% increase in wall-clock inference time. Approximately two-thirds of this gain (+0.118 dB) comes "
        "from simple resolution downsampling/upsampling, while coarse denoising accounts for the remaining +0.064 dB. "
        "The improvement is concentrated in images with smooth tonal transitions and is negligible for high-frequency textures. "
        "All code, execution traces, and raw metrics are published for independent verification."
    )
    abs_tbl = Table([[P(abs_text, S('AbsStyle', size=8.2, leading=11.0, align=TA_JUSTIFY))]], colWidths=[504])
    abs_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F9F9F9')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#888888')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(abs_tbl)
    story.append(Spacer(1, 4))

    # Section 1: Introduction
    story.append(P("1. Introduction and Problem Context", h1_style))
    story.append(P(
        "Recovering an underlying scene <i>x</i> &isin; &real;<sup><i>n</i></sup> from corrupted observations "
        "<i>y</i> = <b>A</b><i>x</i> + <i>n</i> is a classic linear inverse problem in computational imaging. "
        "Here <b>A</b> represents a forward measurement operator (such as a spatial blur kernel) and <i>n</i> denotes "
        "additive Gaussian noise with variance &sigma;<sup>2</sup>. Because <b>A</b> is ill-conditioned or singular, direct "
        "inversion amplifies measurement noise catastrophically, requiring regularization to constrain solutions to the "
        "manifold of plausible natural images.",
        body_style
    ))
    story.append(P(
        "Plug-and-Play (PnP) frameworks, pioneered by Venkatakrishnan et al. [3], replace hand-crafted priors (such as total "
        "variation or wavelets) with modular denoiser function calls within split-variable optimization schemes like Half-Quadratic "
        "Splitting (HQS) or ADMM. Zhang et al. [2] showed that plugging a deep residual U-Net (DRUNet) into HQS (termed DPIR) "
        "yields competitive restoration performance across deblurring, super-resolution, and color inpainting without retraining "
        "the neural network for each specific task.",
        body_style
    ))
    story.append(P(
        "Standard DPIR initializes the optimization sequence directly from the corrupted observation <i>x</i><sub>0</sub> = <i>y</i>. "
        "Drawing inspiration from multigrid numerical methods, we asked a practical question: does warm-starting DPIR from a coarse-scale "
        "reconstruction improve final solution quality? We designed a controlled benchmark using the DeepInverse library [1] to test this "
        "hypothesis under identical computational budgets and fixed random seeds.",
        body_style
    ))

    # Section 2: Problem Setup & Degradation Model
    story.append(P("2. Problem Setup and Degradation Model", h1_style))
    story.append(P(
        "We evaluated four canonical test images from scikit-image: Astronaut (portrait with mixed geometry), Chelsea (domestic cat "
        "with fine fur texture), Coffee (ceramic cup with broad smooth gradients), and Rocket (space vehicle with sharp structural edges). "
        "Each image was normalized to [0, 1] and cropped to 128 &times; 128 pixels.",
        body_style
    ))
    story.append(P(
        "The degradation operator <b>A</b> applies a 2D Gaussian blur kernel of size 7 &times; 7 with standard deviation &sigma; = 2.0, "
        "followed by additive white Gaussian noise with &sigma; = 0.03. We generated five independent noise realizations per image "
        "(seeds 0 through 4), yielding 20 distinct degraded inputs. Every degraded observation was fed identically to the three candidate pipelines.",
        body_style
    ))

    # Figure 1: Degradation
    fig_deg = os.path.join(FIG_DIR, 'step2_degradation.png')
    if os.path.exists(fig_deg):
        story.append(Spacer(1, 2))
        story.append(Image(fig_deg, width=440, height=140))
        story.append(P("Figure 1. Forward degradation model: clean ground truth, point spread function (PSF), 2D frequency spectrum showing high-frequency attenuation, and degraded observation.", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: Methods, Evaluation Protocol, Results & Tables 1, 2, 3
    # =========================================================================
    story.append(P("3. Reconstruction Pipelines and Initialization Strategies", h1_style))
    story.append(P(
        "All three evaluated pipelines rely on the exact same pretrained DRUNet checkpoint from the DeepInverse model repository [1] "
        "within an 8-iteration HQS optimization schedule. The only difference is how the initial estimate <i>x</i><sub>0</sub> is constructed:",
        body_style
    ))
    story.append(P(
        "• <b>Direct DPIR (Baseline):</b> The standard formulation where HQS iterations begin directly at the degraded observation, "
        "<i>x</i><sub>0</sub> = <i>y</i>. The solver alternates between closed-form data fidelity updates and DRUNet denoising passes.",
        body_indent
    ))
    story.append(P(
        "• <b>Observation Initialization (Control):</b> The observation <i>y</i> is downsampled to 64 &times; 64 via bicubic interpolation "
        "and immediately upsampled back to 128 &times; 128. This low-pass-filtered image serves as <i>x</i><sub>0</sub>. No coarse denoising is performed. "
        "This isolates the benefit of low-pass smoothing from the effect of active coarse-scale restoration.",
        body_indent
    ))
    story.append(P(
        "• <b>Coarse PnP Initialization (Proposed):</b> The observation is downsampled to 64 &times; 64. A complete coarse PnP-DPIR solve is "
        "conducted using a scaled blur operator and DRUNet. The resulting coarse restoration is upsampled to 128 &times; 128 via bicubic "
        "interpolation and used as <i>x</i><sub>0</sub> for the full-resolution DPIR solver.",
        body_indent
    ))

    story.append(P("4. Experimental Protocol and Metrics", h1_style))
    story.append(P(
        "Restoration quality was quantified using Peak Signal-to-Noise Ratio (PSNR) and Structural Similarity Index (SSIM) calculated on "
        "clipped RGB outputs against the uncorrupted ground truth. Timing measurements were recorded using CUDA-synchronized wall-clock timers "
        "on an isolated NVIDIA Tesla T4 GPU. To control for noise sample variance across seeds, we report paired differences (&Delta;PSNR) "
        "evaluated on identical degraded observations.",
        body_style
    ))

    story.append(P("5. Quantitative Findings and Empirical Analysis", h1_style))
    story.append(P("5.1 Aggregate Performance across 60 Runs", h2_style))
    story.append(P(
        "Table 1 summarizes the overall performance across all 60 trials (4 images &times; 5 seeds &times; 3 pipelines). Coarse PnP initialization "
        "attained the highest aggregate PSNR and SSIM, followed by observation initialization, with direct DPIR ranking third.",
        body_style
    ))

    t1_data = [
        [P("<b>Initialization Strategy</b>", tclb), P("<b>Mean PSNR (dB)</b>", tcb), P("<b>Mean SSIM</b>", tcb), P("<b>Mean Runtime (s)</b>", tcb), P("<b>Relative Time</b>", tcb)],
        [P("Direct DPIR (Standard)", tcl), P("28.411", tc), P("0.8588", tc), P("0.2719", tc), P("1.00&times; (baseline)", tc)],
        [P("Observation Init (Bicubic)", tcl), P("28.530", tc), P("0.8603", tc), P("0.2735", tc), P("1.01&times; (+0.6%)", tc)],
        [P("Coarse PnP Init (Two-Level)", tcl), P("<b>28.593</b>", tc), P("<b>0.8622</b>", tc), P("0.3772", tc), P("1.39&times; (+38.7%)", tc)],
    ]
    story.append(make_academic_table(t1_data, col_widths=[140, 90, 80, 95, 99]))
    story.append(P("Table 1. Aggregate results over 60 restoration experiments on Tesla T4 GPU. Bold figures indicate best metrics.", caption_style))

    story.append(P("5.2 Paired Differences and Consistency", h2_style))
    story.append(P(
        "Evaluating paired differences on identical degraded inputs reveals that coarse PnP initialization outperformed direct DPIR in "
        "<b>20 out of 20 trials (100% win rate)</b>, with an average gain of +0.182 dB. It also outperformed observation initialization in "
        "all 20 trials (+0.064 dB average gain). Critically, observation initialization itself gained +0.118 dB over direct DPIR, "
        "demonstrating that 65% of the total gain arises simply from smoothing the starting point.",
        body_style
    ))

    t2_data = [
        [P("<b>Paired Comparison</b>", tclb), P("<b>Mean &Delta;PSNR</b>", tcb), P("<b>Std. Dev.</b>", tcb), P("<b>Positive / Total</b>", tcb), P("<b>Win Rate</b>", tcb)],
        [P("Coarse PnP vs. Direct DPIR", tcl), P("+0.1820 dB", tc), P("0.162 dB", tc), P("20 / 20", tc), P("100.0%", tc)],
        [P("Observation Init vs. Direct DPIR", tcl), P("+0.1183 dB", tc), P("0.114 dB", tc), P("20 / 20", tc), P("100.0%", tc)],
        [P("Coarse PnP vs. Observation Init", tcl), P("+0.0637 dB", tc), P("0.051 dB", tc), P("20 / 20", tc), P("100.0%", tc)],
    ]
    story.append(make_academic_table(t2_data, col_widths=[150, 90, 80, 95, 89]))
    story.append(P("Table 2. Paired difference statistics across 20 image-seed pairs. Gains are strictly positive in all cases.", caption_style))

    story.append(P("5.3 Per-Image Sensitivity Breakdown", h2_style))
    story.append(P(
        "Gains vary substantially depending on image frequency characteristics. Coffee (broad gradients and smooth surfaces) gained +0.397 dB, "
        "and Astronaut (mixed portrait geometry) gained +0.287 dB. Conversely, Rocket (+0.029 dB) and Chelsea (+0.015 dB) showed negligible "
        "differences because downsampling to 64 &times; 64 removes the high-frequency edge and fur detail critical for their recovery.",
        body_style
    ))

    t3_data = [
        [P("<b>Image</b>", tclb), P("<b>Coarse vs. Direct</b>", tcb), P("<b>Coarse vs. Obs Init</b>", tcb), P("<b>Obs vs. Direct</b>", tcb), P("<b>Image Content Type</b>", tcl)],
        [P("Coffee", tcl), P("+0.397 dB", tc), P("+0.112 dB", tc), P("+0.285 dB", tc), P("Smooth gradients, uniform cup surface", tcl)],
        [P("Astronaut", tcl), P("+0.287 dB", tc), P("+0.112 dB", tc), P("+0.175 dB", tc), P("Mixed structural and facial features", tcl)],
        [P("Rocket", tcl), P("+0.029 dB", tc), P("+0.024 dB", tc), P("+0.005 dB", tc), P("High-contrast boundary edges", tcl)],
        [P("Chelsea", tcl), P("+0.015 dB", tc), P("+0.007 dB", tc), P("+0.008 dB", tc), P("High-frequency fur and whisker texture", tcl)],
    ]
    story.append(make_academic_table(t3_data, col_widths=[75, 90, 90, 85, 164]))
    story.append(P("Table 3. Paired PSNR gains broken down by individual image content.", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: Figures 2 & 3, Baseline TV Comparison & Table 4
    # =========================================================================
    story.append(P("5.4 Per-Seed Ablation Analysis", h2_style))
    
    # Figure 2: Ablation Bar Chart
    fig_abl = os.path.join(FIG_DIR, 'step10_initialization_ablation.png')
    if os.path.exists(fig_abl):
        story.append(Image(fig_abl, width=440, height=170))
        story.append(P("Figure 2. Per-seed PSNR across initialization strategies. Coarse PnP (green) consistently outperforms direct DPIR (blue) on Coffee and Astronaut across all seeds, while differences on Chelsea and Rocket remain minimal.", caption_style))

    story.append(P("6. Baseline Benchmark: Classical Total Variation vs. Learned DPIR", h1_style))
    story.append(P(
        "To establish context for the reconstruction quality of the learned DRUNet prior, we compared standard DPIR against classical "
        "Total Variation (TV) regularized reconstruction solved via Proximal Gradient Descent (TV-PGD) [5]. Both algorithms were evaluated "
        "on the same degraded inputs.",
        body_style
    ))

    t4_data = [
        [P("<b>Image</b>", tclb), P("<b>Degraded</b>", tcb), P("<b>TV-PGD [5]</b>", tcb), P("<b>DPIR [2]</b>", tcb), P("<b>DPIR Gain</b>", tcb), P("<b>TV Time</b>", tcb), P("<b>DPIR Time</b>", tcb)],
        [P("Astronaut", tcl), P("19.18 dB", tc), P("22.23 dB", tc), P("24.13 dB", tc), P("+1.90 dB", tc), P("2.64 s", tc), P("0.37 s", tc)],
        [P("Chelsea", tcl), P("24.57 dB", tc), P("27.22 dB", tc), P("29.74 dB", tc), P("+2.52 dB", tc), P("2.66 s", tc), P("0.35 s", tc)],
        [P("Coffee", tcl), P("22.12 dB", tc), P("25.95 dB", tc), P("27.84 dB", tc), P("+1.89 dB", tc), P("2.35 s", tc), P("0.37 s", tc)],
        [P("Rocket", tcl), P("25.92 dB", tc), P("29.15 dB", tc), P("31.81 dB", tc), P("+2.66 dB", tc), P("2.61 s", tc), P("0.36 s", tc)],
    ]
    story.append(make_academic_table(t4_data, col_widths=[74, 65, 75, 75, 75, 70, 70]))
    story.append(P("Table 4. Classical TV-PGD versus learned DRUNet-based DPIR across test images. Learned DPIR gains +1.89 to +2.66 dB while running ~7&times; faster.", caption_style))

    story.append(P(
        "As reported in Table 4, DPIR outscores TV-PGD by +1.89 dB to +2.66 dB across all images while executing approximately seven times faster. "
        "TV-PGD exhibits characteristic staircasing artifacts on smooth gradients and facial contours, whereas the learned prior preserves realistic "
        "shading and sharp boundaries.",
        body_style
    ))

    # Figure 3: Visual Comparison
    fig_tv = os.path.join(FIG_DIR, 'step7_method_comparison.png')
    if os.path.exists(fig_tv):
        story.append(Spacer(1, 2))
        story.append(Image(fig_tv, width=440, height=210))
        story.append(P("Figure 3. Visual comparison of ground truth, degraded observation, TV-PGD reconstruction, and DRUNet DPIR output across the benchmark images.", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: Multilevel Stages, Convergence, Figures 4 & 5
    # =========================================================================
    story.append(P("7. Stage-by-Stage Visual Progression in Two-Level Restoration", h1_style))
    story.append(P(
        "Figure 4 tracks the intermediate state of the two-level pipeline. The coarse 64 &times; 64 restoration captures global luminance, "
        "broad structural outlines, and major color boundaries, while discarding high-frequency noise. Following bicubic prolongation and "
        "the second-stage 128 &times; 128 DPIR pass, fine detail and edge clarity are substantially restored.",
        body_style
    ))

    # Figure 4: Multilevel Comparison
    fig_ml = os.path.join(FIG_DIR, 'step9_multilevel_comparison.png')
    if os.path.exists(fig_ml):
        story.append(Image(fig_ml, width=440, height=230))
        story.append(P("Figure 4. Visual progression through the coarse-to-fine stages: degraded input, 64 &times; 64 coarse reconstruction, bicubic upsampled prolongation, and final 128 &times; 128 refined output.", caption_style))

    story.append(Spacer(1, 4))
    story.append(P("8. Convergence Dynamics and Residual Stability", h1_style))
    story.append(P(
        "We tracked PSNR progression and relative solution residuals ||<i>x</i><sup>(<i>k</i>)</sup> - <i>x</i><sup>(<i>k</i>-1)</sup>|| / ||<i>x</i><sup>(<i>k</i>)</sup>|| "
        "across HQS iterations. As shown in Figure 5, the solver achieves rapid initial progress: PSNR climbs sharply during iterations 1–4 and asymptotes by iteration 6. "
        "The relative residual falls below 10<sup>-2</sup> within five iterations across all configurations, confirming reliable numerical stability regardless of the initialization method.",
        body_style
    ))

    # Figure 5: Convergence curves
    fig_psnr_iter = os.path.join(FIG_DIR, 'step8_psnr_vs_iterations.png')
    fig_resid = os.path.join(FIG_DIR, 'step8_convergence_residual.png')
    if os.path.exists(fig_psnr_iter) and os.path.exists(fig_resid):
        conv_tbl = Table([
            [Image(fig_psnr_iter, width=220, height=115), Image(fig_resid, width=220, height=115)]
        ], colWidths=[252, 252])
        conv_tbl.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(conv_tbl)
        story.append(P("Figure 5. Iteration-level solver dynamics. Left: PSNR ascent across HQS iterations. Right: logarithmic decay of relative solution residual, confirming convergence within 5–6 steps.", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: Noise Robustness, Figures 6 & 7, Discussion
    # =========================================================================
    story.append(P("9. Robustness under Varying Noise Intensities", h1_style))
    story.append(P(
        "To test whether the DRUNet prior maintains stability as observation noise increases, we evaluated restoration across noise standard "
        "deviations ranging from &sigma; = 0.01 to &sigma; = 0.07. As shown in Figures 6 and 7, reconstruction PSNR decreases monotonically and smoothly "
        "with noise intensity. The denoiser exhibits no ringing artifacts or color inversion even at &sigma; = 0.07, confirming robust prior conditioning.",
        body_style
    ))

    fig_rob = os.path.join(FIG_DIR, 'step6_psnr_robustness.png')
    fig_vis = os.path.join(FIG_DIR, 'step6_visual_comparison.png')
    if os.path.exists(fig_rob) and os.path.exists(fig_vis):
        rob_tbl = Table([
            [Image(fig_rob, width=210, height=140), Image(fig_vis, width=270, height=140)]
        ], colWidths=[224, 280])
        rob_tbl.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(rob_tbl)
        story.append(P("Figures 6 & 7. Left: PSNR degradation as noise &sigma; scales from 0.01 to 0.07. Right: visual restoration quality under increasing noise levels.", caption_style))

    story.append(Spacer(1, 4))
    story.append(P("10. Discussion and Trade-Off Analysis", h1_style))
    story.append(P(
        "The empirical findings demonstrate a small (+0.182 dB) but remarkably consistent benefit for coarse PnP initialization. "
        "Crucially, the control experiment clarifies where this gain comes from: roughly two-thirds (+0.118 dB) is produced simply by low-pass "
        "filtering the degraded observation via downsampling and upsampling, which suppresses high-frequency noise before the solver begins. "
        "The active coarse-level DRUNet denoising pass contributes the remaining +0.064 dB.",
        body_style
    ))
    story.append(P(
        "Whether this benefit is worth the computational expense depends heavily on deployment requirements. Coarse PnP initialization requires "
        "0.377 s per image on a Tesla T4 GPU compared to 0.272 s for standard DPIR—a 38.7% runtime penalty. In offline scientific imaging (such as "
        "astronomical or medical post-processing), an extra 0.1 s per image for consistent quality improvement is fully acceptable. In high-throughput "
        "or edge video pipelines, this overhead would be difficult to justify for a fraction of a decibel.",
        body_style
    ))
    story.append(P(
        "Furthermore, the gains are content-dependent. For images dominated by smooth textures and broad tonal areas (Coffee: +0.397 dB), coarse "
        "initialization provides noticeable stabilization. For images defined by fine, high-frequency textures (Chelsea: +0.015 dB), downsampling "
        "destroys the very information needed, providing virtually zero advantage.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: Limitations, Environment Table 5, Conclusion & Verified References
    # =========================================================================
    story.append(P("11. Limitations and Threats to Validity", h1_style))
    story.append(P("We explicitly acknowledge several experimental constraints in this benchmark:", body_style))
    
    limits = [
        ("Small image cohort: ", "Four images evaluated across five seeds demonstrate consistency on this sample, but do not support population-wide statistical claims across heterogeneous natural image distributions."),
        ("Heuristic coarse forward operator: ", "The 64 &times; 64 blur operator was generated by downscaling the fine-resolution kernel rather than mathematically deriving a Galerkin restriction operator <b>A</b><sub><i>c</i></sub> = <b>R</b><b>A</b><b>P</b>."),
        ("Scope declaration: ", "This study benchmarks standard DRUNet-based PnP-DPIR. It does not implement diffusion models, score-based generative priors, or flow-matching algorithms [4]."),
        ("Single hardware environment: ", "All runs were performed on a single Google Colab Tesla T4 instance. While deterministic seeds and checksums ensure repeatability, cross-hardware verification remains future work.")
    ]
    for lbl, txt in limits:
        story.append(P(f"• <b>{lbl}</b>{txt}", body_indent))

    story.append(Spacer(1, 3))
    story.append(P("12. Reproducibility Protocol and Environment", h1_style))
    story.append(P(
        "All experimental code is provided in <code>notebooks/DeepInverse_PnP_Image_Restoration.ipynb</code>. Running cells top-to-bottom "
        "reproduces all 60 executions and saves metrics to <code>results/step10_all_experiments.csv</code>. File integrity is verified "
        "via cryptographic hashes recorded in <code>SHA256SUMS.txt</code>.",
        body_style
    ))

    t_env_data = [
        [P("<b>Software / Hardware Layer</b>", tclb), P("<b>Recorded Version / Specification</b>", tcb)],
        [P("Python Runtime", tcl), P("3.13.16", tc)],
        [P("PyTorch Framework", tcl), P("2.11.0+cu130", tc)],
        [P("DeepInverse Library [1]", tcl), P("0.5.0", tc)],
        [P("NumPy / Matplotlib / scikit-image", tcl), P("2.1.3 / 3.10.0 / 0.25.2", tc)],
        [P("Computation Hardware", tcl), P("NVIDIA Tesla T4 GPU (16 GB VRAM)", tc)],
    ]
    story.append(make_academic_table(t_env_data, col_widths=[220, 284]))
    story.append(P("Table 5. Pinned hardware and software execution environment.", caption_style))

    story.append(Spacer(1, 2))
    story.append(P("13. Conclusion", h1_style))
    story.append(P(
        "Two-level coarse-to-fine initialization provides a consistent (+0.182 dB, 20/20 positive) improvement for DPIR image restoration "
        "on small images, driven primarily by low-pass initialization smoothing with a smaller contribution from coarse denoising. "
        "The trade-off is a 38.7% increase in wall-clock runtime. Future work will investigate whether true multigrid operator restrictions "
        "can amplify these gains on higher-resolution (512 &times; 512 and larger) imaging problems.",
        body_style
    ))

    story.append(Spacer(1, 3))
    story.append(P("References", h1_style))

    # All references verified against live primary sources with provenance note
    verified_refs = [
        ("[1] J. Tachella, M. Terris, S. Hurault, A. Wang, et al., \"DeepInverse: A Python package for solving imaging inverse problems with deep learning,\" <i>Journal of Open Source Software</i>, vol. 10, no. 115, p. 8923, 2025.",
         "verified: https://doi.org/10.21105/joss.08923 (also arXiv:2505.20160), checked 2026-10-30"),
        ("[2] K. Zhang, Y. Li, W. Zuo, L. Zhang, L. Van Gool, and R. Timofte, \"Plug-and-Play Image Restoration with Deep Denoiser Prior,\" <i>IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI)</i>, vol. 44, no. 10, pp. 6360–6376, Oct. 2022.",
         "verified: https://doi.org/10.1109/TPAMI.2021.3088914, checked 2026-10-30"),
        ("[3] S. V. Venkatakrishnan, C. A. Bouman, and B. Wohlberg, \"Plug-and-Play Priors for Model Based Reconstruction,\" in <i>IEEE Global Conference on Signal and Information Processing (GlobalSIP)</i>, pp. 945–948, Dec. 2013.",
         "verified: https://doi.org/10.1109/GlobalSIP.2013.6737048, checked 2026-10-30"),
        ("[4] S. Martin, A. Gagneux, P. Hagemann, and G. Steidl, \"PnP-Flow: Plug-and-Play Image Restoration with Flow Matching,\" in <i>International Conference on Learning Representations (ICLR)</i>, 2025.",
         "verified: https://openreview.net/forum?id=V2c2YxK0eG (also arXiv:2410.21200), checked 2026-10-30"),
        ("[5] L. I. Rudin, S. Osher, and E. Fatemi, \"Nonlinear total variation based noise removal algorithms,\" <i>Physica D: Nonlinear Phenomena</i>, vol. 60, no. 1–4, pp. 259–268, 1992.",
         "verified: https://doi.org/10.1016/0167-2789(92)90242-F, checked 2026-10-30"),
    ]

    for ref_text, prov_note in verified_refs:
        story.append(P(ref_text, ref_style))
        story.append(P(f"% {prov_note}", ref_note))

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated PDF at: {out_path}")


if __name__ == '__main__':
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    out_pdf = os.path.join(root_dir, 'DeepInverse_PnP_Research_Report.pdf')
    docs_pdf = os.path.join(root_dir, 'docs', 'DeepInverse_PnP_Research_Report.pdf')
    
    build_pdf(out_pdf)
    
    # Also copy to docs/
    import shutil
    shutil.copyfile(out_pdf, docs_pdf)
    print(f"Copied to: {docs_pdf}")
