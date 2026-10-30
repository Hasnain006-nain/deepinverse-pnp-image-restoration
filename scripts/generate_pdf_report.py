"""
Generate a professional research report PDF (8-10 pages).
Times New Roman, justified text, clean tables, embedded figures.
Human-written academic style throughout.
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, KeepTogether, HRFlowable, PageBreak
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

W, H = letter  # 612 x 792 points

# ─── Numbered canvas with header/footer ─────────────────────────────
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
        # header line (skip page 1)
        if self._pageNumber > 1:
            self.setFont('Times-Roman', 8)
            self.setFillColor(colors.HexColor('#555555'))
            self.drawString(60, H - 36, 'Haider — Plug-and-Play Image Restoration Benchmark')
            self.drawRightString(W - 60, H - 36, 'DeepInverse / DRUNet Study')
            self.setStrokeColor(colors.HexColor('#BBBBBB'))
            self.setLineWidth(0.4)
            self.line(60, H - 40, W - 60, H - 40)
        # footer
        self.setStrokeColor(colors.HexColor('#BBBBBB'))
        self.setLineWidth(0.4)
        self.line(60, 40, W - 60, 40)
        self.setFont('Times-Roman', 8)
        self.setFillColor(colors.HexColor('#555555'))
        self.drawString(60, 28, 'https://github.com/Hasnain006-nain/deepinverse-pnp-image-restoration')
        self.drawRightString(W - 60, 28, f'{self._pageNumber} / {total}')
        self.restoreState()


# ─── Styles ──────────────────────────────────────────────────────────
def S(name, font='Times-Roman', size=10, leading=14, align=TA_JUSTIFY,
      color='#111111', spaceBefore=0, spaceAfter=6, bold=False, italic=False,
      keepWithNext=False, leftIndent=0):
    if bold:
        font = 'Times-Bold'
    if italic:
        font = 'Times-Italic'
    return ParagraphStyle(
        name, fontName=font, fontSize=size, leading=leading,
        alignment=align, textColor=colors.HexColor(color),
        spaceBefore=spaceBefore, spaceAfter=spaceAfter,
        keepWithNext=keepWithNext, leftIndent=leftIndent
    )

title    = S('Title', size=15, leading=19, align=TA_CENTER, bold=True)
author   = S('Author', size=11, leading=14, align=TA_CENTER, bold=True, spaceAfter=2)
affil    = S('Affil', size=9, leading=12, align=TA_CENTER, italic=True, color='#444444', spaceAfter=8)
h1       = S('H1', size=12, leading=16, bold=True, spaceBefore=14, spaceAfter=4, keepWithNext=True, align=TA_LEFT)
h2       = S('H2', size=10.5, leading=14, bold=True, spaceBefore=10, spaceAfter=3, keepWithNext=True, align=TA_LEFT)
body     = S('Body')
body_ind = S('BodyInd', leftIndent=18)
caption  = S('Caption', size=8.5, leading=11, align=TA_CENTER, italic=True, color='#444444', spaceBefore=3, spaceAfter=8)
tc       = S('TC', size=8.5, leading=11, align=TA_CENTER)
tcl      = S('TCL', size=8.5, leading=11, align=TA_LEFT)
tcb      = S('TCB', size=8.5, leading=11, align=TA_CENTER, bold=True)
tclb     = S('TCLB', size=8.5, leading=11, align=TA_LEFT, bold=True)
ref      = S('Ref', size=8.5, leading=11.5, spaceAfter=4, align=TA_LEFT)
refnote  = S('RefNote', size=7.5, leading=10, italic=True, color='#2563EB', spaceAfter=5, align=TA_LEFT)


# ─── Helper: simple data table ───────────────────────────────────────
def make_table(data, col_widths=None, header_bg='#E8E8E8'):
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(header_bg)),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#BBBBBB')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]
    # alternating row shading
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#F5F5F5')))
    t.setStyle(TableStyle(style_cmds))
    return t

P = Paragraph  # shortcut

FIG = 'C:/Users/Admin/deepinverse-pnp-image-restoration/figures'


# ─── Build ───────────────────────────────────────────────────────────
def build():
    out = 'C:/Users/Admin/deepinverse-pnp-image-restoration/DeepInverse_PnP_Research_Report.pdf'
    doc = SimpleDocTemplate(out, pagesize=letter,
                            leftMargin=60, rightMargin=60,
                            topMargin=54, bottomMargin=54)
    s = []  # story

    # ── Title page content ───────────────────────────────────────────
    s.append(Spacer(1, 40))
    s.append(P("Plug-and-Play Image Restoration:<br/>"
               "A Two-Level Coarse-to-Fine Initialization Study<br/>"
               "Using DeepInverse and DRUNet", title))
    s.append(Spacer(1, 10))
    s.append(P("Hasnain Haider", author))
    s.append(P("Independent Research Benchmark<br/>"
               "Prepared for Inria Internship Application", affil))
    s.append(Spacer(1, 6))
    s.append(HRFlowable(width="100%", thickness=0.8,
                         color=colors.HexColor('#333333'),
                         spaceBefore=2, spaceAfter=10))

    # Abstract
    abs_text = (
        "This report describes a controlled experiment comparing three initialization "
        "strategies for Plug-and-Play image restoration with a pretrained DRUNet denoiser. "
        "We degraded four standard test images with synthetic Gaussian blur and noise, then "
        "restored each image five times (different noise seeds) under three conditions: "
        "standard DPIR, observation-only initialization, and two-level coarse PnP initialization. "
        "The two-level approach produced a mean PSNR of 28.593 dB compared to 28.411 dB for "
        "standard DPIR, with all 20 paired comparisons showing positive gains. The improvement "
        "comes at the cost of roughly 39% more computation time. We also compare learned DPIR "
        "against classical Total Variation restoration, examine convergence behavior, and test "
        "noise-level robustness. All code, data, and figures are publicly available for "
        "independent verification."
    )
    abs_tbl = Table(
        [[P("<b>Abstract.</b> " + abs_text, S('abs', size=9.5, leading=13))]],
        colWidths=[W - 120]
    )
    abs_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7F7F7')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#BBBBBB')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    s.append(abs_tbl)
    s.append(Spacer(1, 8))

    # ── 1. Introduction ──────────────────────────────────────────────
    s.append(P("1. Introduction", h1))
    s.append(P(
        "Recovering a clean image from blurred and noisy measurements is a standard problem "
        "in computational imaging. Given an observation y = Ax + n, where A is a known blur "
        "operator and n is Gaussian noise, the goal is to find the best estimate of x. "
        "Variational methods approach this by minimizing a data-fidelity term plus a "
        "regularizer that encodes prior knowledge about natural images.",
        body))
    s.append(P(
        "Plug-and-Play (PnP) methods replace the explicit regularization step with a call "
        "to a pretrained denoiser. The idea, introduced by Venkatakrishnan et al. [3] in 2013, "
        "is that a good denoiser implicitly encodes a prior over clean images. When paired with "
        "a half-quadratic splitting (HQS) optimization loop, this approach is both flexible "
        "and effective. Zhang et al. [2] demonstrated this concretely with DPIR, using a "
        "deep residual U-Net denoiser (DRUNet) that achieves competitive or superior results "
        "across deblurring, super-resolution, and inpainting tasks without any task-specific training.",
        body))
    s.append(P(
        "A natural question arises about initialization: standard DPIR starts the HQS iterations "
        "from the raw observation y. Could we do better by first solving a cheaper, lower-resolution "
        "version of the problem and using that estimate as a warm start? This idea has roots in "
        "multigrid methods from numerical analysis, where coarse-level corrections accelerate "
        "convergence of fine-level solvers.",
        body))
    s.append(P(
        "In this study, we tested exactly that. We compared three initialization strategies on "
        "four standard test images, each evaluated across five independent noise realizations, "
        "yielding 60 total reconstruction experiments. The work was conducted in Google Colab "
        "using the open-source DeepInverse library [1] and pretrained DRUNet weights.",
        body))

    # ── 2. Problem Setup ─────────────────────────────────────────────
    s.append(P("2. Problem Setup and Degradation Model", h1))
    s.append(P(
        "We selected four color images from scikit-image's standard collection: Astronaut "
        "(a portrait with fabric and background detail), Chelsea (a tabby cat with fine fur "
        "texture), Coffee (a cup with smooth gradients and flat surfaces), and Rocket (a launch "
        "vehicle against sky, with strong edges). Each was resized to 128 x 128 pixels and "
        "normalized to the [0, 1] intensity range.",
        body))
    s.append(P(
        "The forward degradation model applied a 2D Gaussian blur kernel (size 7 x 7, standard "
        "deviation 2.0) followed by additive white Gaussian noise with standard deviation 0.03. "
        "This produces a moderately degraded observation that is visually recognizable but "
        "substantially softened and noisy. The degradation was applied identically to all four images, "
        "varying only the random seed for the noise component. Seeds 0 through 4 were used, "
        "giving five observations per image and 20 total degradation instances.",
        body))

    # Figure: degradation
    fig_deg = os.path.join(FIG, 'step2_degradation.png')
    if os.path.exists(fig_deg):
        s.append(Spacer(1, 4))
        s.append(Image(fig_deg, width=420, height=190))
        s.append(P("Figure 1. Degradation pipeline: ground truth, point-spread function, "
                    "frequency spectrum showing high-frequency attenuation, and resulting observation.",
                    caption))

    # ── 3. Methods ───────────────────────────────────────────────────
    s.append(P("3. Reconstruction Methods", h1))
    s.append(P(
        "All three methods used the same DRUNet denoiser (pretrained weights from the DeepInverse "
        "model repository, no fine-tuning) within an HQS optimization loop. The only difference "
        "between them is how the initial estimate x_0 is constructed before iterating.",
        body))

    s.append(P("3.1 Direct DPIR", h2))
    s.append(P(
        "The baseline. The HQS solver is initialized directly with the corrupted observation: "
        "x_0 = y. The solver then alternates between a data-fidelity gradient step and a DRUNet "
        "denoising step at progressively decreasing noise levels. This is the standard approach "
        "described by Zhang et al. [2].",
        body))

    s.append(P("3.2 Observation initialization", h2))
    s.append(P(
        "A control experiment. The observation y is first downsampled to 64 x 64 using bicubic "
        "interpolation, then immediately upsampled back to 128 x 128. This low-pass-filtered "
        "version serves as x_0 for the fine-scale DPIR solver. No denoising is performed at the "
        "coarse level. The purpose is to separate the effect of resolution cycling (which smooths "
        "the initialization) from the effect of actual coarse-level restoration.",
        body))

    s.append(P("3.3 Coarse PnP initialization", h2))
    s.append(P(
        "The experimental method. The observation is downsampled to 64 x 64. A complete PnP-DPIR "
        "solve is performed at this coarse resolution using a scaled blur kernel and the same "
        "DRUNet denoiser. The resulting coarse estimate is then upsampled to 128 x 128 via bicubic "
        "interpolation and used as x_0 for the fine-scale DPIR solver. The total runtime includes "
        "both the coarse and fine stages.",
        body))
    s.append(P(
        "We deliberately kept everything else identical: same DRUNet weights, same HQS parameters, "
        "same number of fine-level iterations. The only variable is the starting point.",
        body))

    # ── 4. Evaluation ────────────────────────────────────────────────
    s.append(P("4. Evaluation Protocol", h1))
    s.append(P(
        "Reconstruction quality was measured using peak signal-to-noise ratio (PSNR) and structural "
        "similarity index (SSIM), both computed on clipped [0, 1] RGB images against the original "
        "ground truth. Runtime was measured using CUDA-synchronized wall-clock timing on an NVIDIA "
        "Tesla T4 GPU.",
        body))
    s.append(P(
        "Because random noise affects absolute PSNR values, we report paired differences: for each "
        "image-seed combination, we compute the PSNR difference between methods applied to the same "
        "degraded observation. This controls for noise variability and gives a more reliable estimate "
        "of the initialization effect.",
        body))

    # ── 5. Results ───────────────────────────────────────────────────
    s.append(P("5. Results", h1))

    s.append(P("5.1 Overall performance", h2))
    s.append(P(
        "Table 1 summarizes the aggregate results across all 60 runs. The coarse PnP method "
        "achieves the highest mean PSNR and SSIM, followed by observation initialization, "
        "with direct DPIR as the baseline.",
        body))

    t1 = make_table([
        [P("<b>Method</b>", tclb), P("<b>Mean PSNR (dB)</b>", tcb),
         P("<b>Mean SSIM</b>", tcb), P("<b>Mean runtime (s)</b>", tcb)],
        [P("Direct DPIR", tcl), P("28.411", tc), P("0.8588", tc), P("0.2719", tc)],
        [P("Observation init", tcl), P("28.530", tc), P("0.8603", tc), P("0.2735", tc)],
        [P("Coarse PnP init", tcl), P("<b>28.593</b>", tc), P("<b>0.8622</b>", tc), P("0.3772", tc)],
    ], col_widths=[150, 100, 80, 100])
    s.append(t1)
    s.append(P("Table 1. Overall results across 60 restoration experiments (4 images, 5 seeds, "
               "3 methods). Boldface indicates the best value.", caption))

    s.append(P("5.2 Paired comparisons", h2))
    s.append(P(
        "The paired analysis reveals that the coarse PnP initialization outperformed direct DPIR "
        "in every single one of the 20 image-seed combinations, with a mean gain of +0.182 dB. "
        "It also outperformed the observation-only initialization in all 20 cases, though by a "
        "smaller margin of +0.064 dB. The fact that observation initialization itself gains "
        "+0.118 dB over direct DPIR suggests that part of the benefit comes simply from smoothing "
        "the initial estimate. But the additional +0.064 dB from coarse PnP confirms that the "
        "coarse-level denoiser contributes something beyond low-pass filtering.",
        body))

    t2 = make_table([
        [P("<b>Comparison</b>", tclb), P("<b>Mean gain (dB)</b>", tcb),
         P("<b>Positive / Total</b>", tcb)],
        [P("Coarse PnP vs Direct", tcl), P("+0.1820", tc), P("20 / 20", tc)],
        [P("Obs init vs Direct", tcl), P("+0.1183", tc), P("20 / 20", tc)],
        [P("Coarse PnP vs Obs init", tcl), P("+0.0637", tc), P("20 / 20", tc)],
    ], col_widths=[180, 120, 120])
    s.append(t2)
    s.append(P("Table 2. Paired PSNR differences. Every comparison is positive in all 20 trials.",
               caption))

    s.append(P("5.3 Image-level breakdown", h2))
    s.append(P(
        "The gains are not uniform across images. Coffee, which has broad tonal areas and "
        "smooth gradients, benefits the most (+0.397 dB). Astronaut, with a mix of face detail "
        "and fabric texture, sees +0.287 dB. Chelsea (fine fur) and Rocket (sharp edges) show "
        "gains below +0.03 dB. This pattern makes physical sense: downsampling to 64 x 64 "
        "discards high-frequency content. Images whose structure is well-captured at low "
        "resolution benefit from the coarse stage; images dominated by fine detail do not.",
        body))

    t3 = make_table([
        [P("<b>Image</b>", tclb), P("<b>Coarse vs<br/>Direct</b>", tcb),
         P("<b>Coarse vs<br/>Obs init</b>", tcb), P("<b>Obs init vs<br/>Direct</b>", tcb),
         P("<b>Std. dev.</b>", tcb)],
        [P("Coffee", tcl), P("+0.397 dB", tc), P("+0.112 dB", tc), P("+0.285 dB", tc), P("0.052 dB", tc)],
        [P("Astronaut", tcl), P("+0.287 dB", tc), P("+0.112 dB", tc), P("+0.175 dB", tc), P("0.028 dB", tc)],
        [P("Rocket", tcl), P("+0.029 dB", tc), P("+0.024 dB", tc), P("+0.005 dB", tc), P("0.007 dB", tc)],
        [P("Chelsea", tcl), P("+0.015 dB", tc), P("+0.007 dB", tc), P("+0.008 dB", tc), P("0.013 dB", tc)],
    ], col_widths=[80, 90, 90, 90, 80])
    s.append(t3)
    s.append(P("Table 3. Paired PSNR gains broken down by test image, averaged over 5 noise seeds.",
               caption))

    # Figure: ablation
    fig_abl = os.path.join(FIG, 'step10_initialization_ablation.png')
    if os.path.exists(fig_abl):
        s.append(Image(fig_abl, width=440, height=218))
        s.append(P("Figure 2. Per-seed PSNR comparison across the three initialization methods for "
                    "each test image. The coarse PnP advantage is visible for Coffee and Astronaut but "
                    "negligible for Chelsea and Rocket.", caption))

    # ── 6. TV-PGD vs DPIR ───────────────────────────────────────────
    s.append(P("6. Baseline Comparison: TV-PGD vs Learned DPIR", h1))
    s.append(P(
        "Before investigating initialization strategies, we compared DRUNet-based DPIR against "
        "classical Total Variation (TV) regularization solved via proximal gradient descent. "
        "This provides context for the overall quality level of the learned prior. Table 4 "
        "shows the results on all four images at a single noise seed.",
        body))

    t4 = make_table([
        [P("<b>Image</b>", tclb), P("<b>Degraded</b>", tcb), P("<b>TV-PGD</b>", tcb),
         P("<b>DPIR</b>", tcb), P("<b>DPIR gain</b>", tcb), P("<b>TV time</b>", tcb),
         P("<b>DPIR time</b>", tcb)],
        [P("Astronaut", tcl), P("19.18 dB", tc), P("22.23 dB", tc), P("24.13 dB", tc),
         P("+1.90 dB", tc), P("2.64 s", tc), P("0.37 s", tc)],
        [P("Chelsea", tcl), P("24.57 dB", tc), P("27.22 dB", tc), P("29.74 dB", tc),
         P("+2.52 dB", tc), P("2.66 s", tc), P("0.35 s", tc)],
        [P("Coffee", tcl), P("22.12 dB", tc), P("25.95 dB", tc), P("27.84 dB", tc),
         P("+1.89 dB", tc), P("2.35 s", tc), P("0.37 s", tc)],
        [P("Rocket", tcl), P("25.92 dB", tc), P("29.15 dB", tc), P("31.81 dB", tc),
         P("+2.66 dB", tc), P("2.61 s", tc), P("0.36 s", tc)],
    ], col_widths=[65, 65, 65, 65, 65, 62, 62])
    s.append(t4)
    s.append(P("Table 4. Classical TV-PGD vs learned DPIR. The learned denoiser prior produces "
               "+1.9 to +2.7 dB higher PSNR while running approximately 7 times faster.", caption))

    s.append(P(
        "The TV reconstructions exhibit the characteristic piecewise-constant staircasing artifacts, "
        "particularly visible on smooth gradients and skin tones. DPIR reconstructions are "
        "substantially sharper and more natural-looking. The TV-PGD regularization parameter was not "
        "exhaustively tuned; the comparison is meant to establish context rather than provide a "
        "definitive verdict on TV methods in general.",
        body))

    # Figure: TV vs DPIR
    fig_tv = os.path.join(FIG, 'step7_method_comparison.png')
    if os.path.exists(fig_tv):
        s.append(Image(fig_tv, width=460, height=265))
        s.append(P("Figure 3. Visual comparison of ground truth, degraded observation, TV-PGD, and "
                    "DRUNet DPIR across all four benchmark images.", caption))

    # ── 7. Multilevel Stages ─────────────────────────────────────────
    s.append(P("7. Two-Level Restoration: Stage-by-Stage Visualization", h1))
    s.append(P(
        "Figure 4 shows the intermediate products of the coarse-to-fine pipeline. The coarse "
        "64 x 64 restoration is visibly softer than the ground truth but captures overall "
        "structure, color distribution, and large-scale edges. After bicubic upsampling and "
        "the fine-scale DPIR pass, the output recovers substantially more detail. The visual "
        "improvement from coarse to fine is most apparent in textured regions.",
        body))

    fig_ml = os.path.join(FIG, 'step9_multilevel_comparison.png')
    if os.path.exists(fig_ml):
        s.append(Image(fig_ml, width=470, height=285))
        s.append(P("Figure 4. Multi-level restoration stages: coarse observation, coarse restored "
                    "estimate (64 x 64), upsampled prolongation, and final refined output (128 x 128).",
                    caption))

    # ── 8. Convergence ───────────────────────────────────────────────
    s.append(P("8. Convergence Behavior", h1))
    s.append(P(
        "We recorded the PSNR trajectory and relative residual at each HQS iteration. As shown "
        "in Figure 5, PSNR rises steeply during the first three to four iterations, then levels "
        "off. The relative residual (defined as the norm of the iterate difference divided by the "
        "current iterate norm) drops below 0.01 within five iterations. This confirms that the "
        "HQS solver converges reliably for this problem configuration, regardless of initialization "
        "strategy.",
        body))

    fig_psnr_iter = os.path.join(FIG, 'step8_psnr_vs_iterations.png')
    fig_resid = os.path.join(FIG, 'step8_convergence_residual.png')
    if os.path.exists(fig_psnr_iter) and os.path.exists(fig_resid):
        conv_tbl = Table([
            [Image(fig_psnr_iter, width=225, height=115),
             Image(fig_resid, width=225, height=115)]
        ], colWidths=[240, 240])
        conv_tbl.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        s.append(conv_tbl)
        s.append(P("Figure 5. Left: PSNR progression over HQS iterations. Right: relative residual "
                    "decay. Both confirm stable convergence within the allocated iteration budget.",
                    caption))

    # ── 9. Noise Robustness ──────────────────────────────────────────
    s.append(P("9. Noise Robustness", h1))
    s.append(P(
        "To check whether the DRUNet prior remains effective under stronger noise, we repeated "
        "the single-image restoration experiment with noise standard deviations ranging from 0.01 "
        "(mild) to 0.07 (heavy). As expected, PSNR decreases monotonically with increasing noise. "
        "Importantly, the DRUNet denoiser degrades gracefully: there are no visible ringing artifacts "
        "or color shifts even at the highest noise level, though fine detail is progressively lost.",
        body))

    fig_rob = os.path.join(FIG, 'step6_psnr_robustness.png')
    if os.path.exists(fig_rob):
        s.append(Image(fig_rob, width=320, height=165))
        s.append(P("Figure 6. PSNR as a function of noise sigma. Performance degrades smoothly; no "
                    "catastrophic failure is observed up to sigma = 0.07.", caption))

    fig_vis = os.path.join(FIG, 'step6_visual_comparison.png')
    if os.path.exists(fig_vis):
        s.append(Image(fig_vis, width=420, height=260))
        s.append(P("Figure 7. Visual restoration quality across noise levels (sigma = 0.01 to 0.07).",
                    caption))

    # ── 10. Discussion ───────────────────────────────────────────────
    s.append(P("10. Discussion and Limitations", h1))

    s.append(P(
        "The paired results are clear: coarse PnP initialization produces higher PSNR than direct "
        "DPIR in every trial we ran. The effect is small in absolute terms (a fifth of a decibel "
        "on average) and varies substantially across images. But it is consistent, which suggests "
        "that the coarse estimate is providing genuinely useful structural information rather than "
        "just getting lucky on some noise realizations.",
        body))
    s.append(P(
        "The observation initialization control is informative. It shows that roughly two-thirds "
        "of the total gain (+0.118 out of +0.182 dB) comes from smoothing the initialization via "
        "downsampling and upsampling. Only the remaining +0.064 dB can be attributed to the coarse "
        "DRUNet denoising step. This is a modest contribution, and it comes at the cost of a full "
        "additional PnP solve at coarse resolution.",
        body))
    s.append(P(
        "The runtime numbers make the trade-off concrete. The coarse PnP method takes 0.377 seconds "
        "on average versus 0.272 seconds for direct DPIR, a 39% increase. Whether +0.18 dB justifies "
        "that overhead depends on the application. For offline processing of scientific imaging data, "
        "it might. For real-time video processing, it almost certainly would not.",
        body))

    s.append(P("There are several limitations that need to be stated plainly:", body))

    limits = [
        ("Small image sample. ",
         "Four images and five noise seeds do not constitute a statistically powerful dataset. "
         "The per-image differences (Coffee +0.40 dB, Chelsea +0.01 dB) are observations about "
         "these specific images, not population-level estimates."),
        ("Approximate coarse operator. ",
         "We constructed the 64 x 64 blur operator by resizing the fine-scale kernel, not by "
         "mathematically deriving a restriction operator. In a proper multigrid framework, the "
         "coarse operator should satisfy A_c = R A P, where R and P are restriction and "
         "prolongation operators. Our heuristic approach does not guarantee this consistency."),
        ("No flow-matching implementation. ",
         "This study uses standard DRUNet denoising within an HQS loop. It does not implement "
         "flow-matching, score-based diffusion, or any generative restoration model. The work "
         "is related to but distinct from the Inria PnP-Flow project [4]."),
        ("Single GPU, single run. ",
         "All experiments were run on a single Tesla T4 GPU in Google Colab. The metrics were "
         "extracted from a single Colab session. While we verified file integrity and numerical "
         "consistency, a completely independent rerun in a fresh environment was not performed."),
    ]
    for heading, text in limits:
        s.append(P("<b>" + heading + "</b>" + text, body_ind))

    # ── 11. Reproducibility ──────────────────────────────────────────
    s.append(P("11. Reproducibility", h1))
    s.append(P(
        "The complete experiment is contained in a single Google Colab notebook available at "
        "notebooks/DeepInverse_PnP_Image_Restoration.ipynb. To reproduce the results: open the "
        "notebook in Colab, select a T4 GPU runtime, and run cells sequentially from top to bottom. "
        "The first cell installs DeepInverse 0.5.0; subsequent cells load pretrained DRUNet weights "
        "from the internet.",
        body))
    s.append(P(
        "All numerical results are stored as CSV files in the results/ directory. Research figures "
        "are in figures/. Cryptographic SHA-256 checksums for all files are recorded in "
        "SHA256SUMS.txt. The exact software environment is documented in environment.json:",
        body))

    t_env = make_table([
        [P("<b>Component</b>", tclb), P("<b>Version</b>", tcb)],
        [P("Python", tcl), P("3.13.16", tc)],
        [P("PyTorch", tcl), P("2.11.0+cu130", tc)],
        [P("DeepInverse", tcl), P("0.5.0", tc)],
        [P("NumPy", tcl), P("2.1.3", tc)],
        [P("Matplotlib", tcl), P("3.10.0", tc)],
        [P("scikit-image", tcl), P("0.25.2", tc)],
        [P("GPU", tcl), P("NVIDIA Tesla T4", tc)],
    ], col_widths=[140, 180])
    s.append(t_env)
    s.append(P("Table 5. Recorded software and hardware environment.", caption))

    # ── 12. Conclusion ───────────────────────────────────────────────
    s.append(P("12. Conclusion", h1))
    s.append(P(
        "We tested whether a two-level coarse-to-fine initialization helps PnP-DPIR image "
        "restoration. On four test images with five noise seeds each, it does: the mean paired "
        "PSNR gain is +0.182 dB, positive in all 20 trials. About two-thirds of this gain comes "
        "from smoothing the initialization; the remaining third comes from coarse-level denoising. "
        "The cost is a 39% increase in computation time.",
        body))
    s.append(P(
        "The practical significance of these findings is limited. The image sample is small, the "
        "gains are modest, and the coarse operator is approximate. But the results are consistent "
        "and reproducible, and they suggest that multi-resolution initialization is worth "
        "exploring further, particularly for larger images and more challenging degradation "
        "models where the coarse stage might provide proportionally greater benefit.",
        body))

    # ── 13. References ───────────────────────────────────────────────
    s.append(P("References", h1))

    refs_data = [
        ("[1] J. Tachella, M. Terris, S. Hurault, A. Wang, D. Chen, M. Nguyen, M. Song, "
         "T. Davies, L. Davy, J. Dong, P. Escande, J. Hertrich, Z. Hu, T. I. Liaudat, "
         "N. Laurent, B. Levac, M. Massias, T. Moreau, T. Modrzyk, B. Monroy, S. Neumayer, "
         "J. Scanvic, F. Sarron, V. Sechaud, G. Schramm, C. Tang, R. Vo, and P. Weiss, "
         "\"DeepInverse: a Python package for solving imaging inverse problems with deep "
         "learning,\" <i>arXiv preprint arXiv:2505.20160</i>, 2025.",
         "verified: https://arxiv.org/abs/2505.20160"),

        ("[2] K. Zhang, Y. Li, W. Zuo, L. Zhang, L. Van Gool, and R. Timofte, \"Plug-and-Play "
         "Image Restoration with Deep Denoiser Prior,\" <i>IEEE Trans. Pattern Anal. Mach. "
         "Intell.</i>, vol. 44, no. 10, pp. 6360-6376, Oct. 2022.",
         "verified: https://doi.org/10.1109/TPAMI.2021.3088914"),

        ("[3] S. V. Venkatakrishnan, C. A. Bouman, and B. Wohlberg, \"Plug-and-Play Priors "
         "for Model Based Reconstruction,\" in <i>2013 IEEE Global Conference on Signal and "
         "Information Processing</i>, pp. 945-948, Dec. 2013.",
         "verified: https://doi.org/10.1109/GlobalSIP.2013.6737048"),

        ("[4] S. Martin, A. Gagneux, P. Hagemann, and G. Steidl, \"Plug-and-Play Image "
         "Restoration with Flow Matching,\" in <i>International Conference on Learning "
         "Representations (ICLR)</i>, 2025.",
         "verified: https://openreview.net/forum?id=V2c2YxK0eG"),
    ]
    for r, v in refs_data:
        s.append(P(r, ref))
        s.append(P("% " + v, refnote))

    # Build
    doc.build(s, canvasmaker=NumberedCanvas)
    print(f"PDF written to {out}")
    print(f"Size: {os.path.getsize(out):,} bytes")


if __name__ == '__main__':
    build()
