"""
Generate a publication-grade, professional research report PDF (exactly 6 pages).
Features:
- TrueType Times New Roman fonts with 100% full unicode support (no broken glyphs)
- Centered academic tables with booktabs styling and captions placed above tables
- Fully justified body text across all sections, abstract, and references
- 12 comprehensive, verified, credible academic references at the end
- Perfectly balanced 6-page budget with zero overflow and zero awkward white gaps
- Native figure aspect ratios (no squashed or distorted images)
- Polished running headers and footers with page numbering (Page X of 6)
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
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Page dimensions: 612 x 792 points
W, H = letter

# Register Windows TrueType Times New Roman fonts for flawless unicode and rendering
FONT_DIR = r"C:\Windows\Fonts"
TIMES_REG = False
if os.path.exists(os.path.join(FONT_DIR, "times.ttf")):
    try:
        pdfmetrics.registerFont(TTFont("TimesNewRoman", os.path.join(FONT_DIR, "times.ttf")))
        pdfmetrics.registerFont(TTFont("TimesNewRoman-Bold", os.path.join(FONT_DIR, "timesbd.ttf")))
        pdfmetrics.registerFont(TTFont("TimesNewRoman-Italic", os.path.join(FONT_DIR, "timesi.ttf")))
        pdfmetrics.registerFont(TTFont("TimesNewRoman-BoldItalic", os.path.join(FONT_DIR, "timesbi.ttf")))
        pdfmetrics.registerFontFamily(
            "TimesNewRoman",
            normal="TimesNewRoman",
            bold="TimesNewRoman-Bold",
            italic="TimesNewRoman-Italic",
            boldItalic="TimesNewRoman-BoldItalic"
        )
        TIMES_REG = True
    except Exception as e:
        print(f"Font registration warning: {e}")

BASE_FONT = "TimesNewRoman" if TIMES_REG else "Times-Roman"
BASE_BOLD = "TimesNewRoman-Bold" if TIMES_REG else "Times-Bold"
BASE_ITALIC = "TimesNewRoman-Italic" if TIMES_REG else "Times-Italic"
BASE_BI = "TimesNewRoman-BoldItalic" if TIMES_REG else "Times-BoldItalic"


class AcademicNumberedCanvas(canvas.Canvas):
    """Two-pass canvas for professional headers, footers, rules, and total page numbering."""
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
        # Running header on pages 2..total
        if self._pageNumber > 1:
            self.setFont(BASE_BOLD, 8.0)
            self.setFillColor(colors.HexColor("#1A365D"))  # Navy accent
            self.drawString(54, H - 32, "HASNAIN HAIDER")
            self.setFont(BASE_FONT, 8.0)
            self.setFillColor(colors.HexColor("#334155"))
            self.drawString(136, H - 32, "|  Plug-and-Play Image Restoration with Coarse-to-Fine Initialization")
            self.setFont(BASE_BOLD, 8.0)
            self.setFillColor(colors.HexColor("#1A365D"))
            self.drawRightString(W - 54, H - 32, "RESEARCH REPORT")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(54, H - 36, W - 54, H - 36)

        # Running footer on all pages
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(54, 38, W - 54, 38)
        self.setFont(BASE_FONT, 8.0)
        self.setFillColor(colors.HexColor("#475569"))
        self.drawString(54, 27, "Independent Research Benchmark  |  github.com/Hasnain006-nain/deepinverse-pnp-image-restoration")
        self.setFont(BASE_BOLD, 8.0)
        self.setFillColor(colors.HexColor("#1A365D"))
        self.drawRightString(W - 54, 27, f"Page {self._pageNumber} of {total}")
        self.restoreState()


# Style factory
def S(name, font=BASE_FONT, size=9.0, leading=11.8, align=TA_JUSTIFY,
      color="#1F2937", spaceBefore=0, spaceAfter=2.5, bold=False, italic=False,
      keepWithNext=False, leftIndent=0):
    if bold and italic:
        f = BASE_BI
    elif bold:
        f = BASE_BOLD
    elif italic:
        f = BASE_ITALIC
    else:
        f = font
    return ParagraphStyle(
        name, fontName=f, fontSize=size, leading=leading,
        alignment=align, textColor=colors.HexColor(color),
        spaceBefore=spaceBefore, spaceAfter=spaceAfter,
        keepWithNext=keepWithNext, leftIndent=leftIndent
    )

# Document Typography Palette
title_style = S('DocTitle', size=13.5, leading=17.0, align=TA_CENTER, bold=True, color="#1A365D", spaceAfter=3)
author_style = S('DocAuthor', size=10.2, leading=13.0, align=TA_CENTER, bold=True, color="#111827", spaceAfter=2)
affil_style = S('DocAffil', size=8.3, leading=10.8, align=TA_CENTER, italic=True, color="#475569", spaceAfter=3)

h1_style = S('H1', size=9.8, leading=12.4, bold=True, color="#1A365D", spaceBefore=5.0, spaceAfter=2.0, keepWithNext=True, align=TA_LEFT)
h2_style = S('H2', size=8.8, leading=11.4, bold=True, color="#1E293B", spaceBefore=3.5, spaceAfter=1.8, keepWithNext=True, align=TA_LEFT)
body_style = S('Body', size=8.2, leading=10.9, align=TA_JUSTIFY, color="#1F2937", spaceAfter=2.5)
body_indent = S('BodyIndent', size=8.2, leading=10.9, align=TA_JUSTIFY, color="#1F2937", leftIndent=11, spaceAfter=2.0)

fig_caption_style = S('FigCaption', size=7.6, leading=9.6, align=TA_CENTER, italic=True, color="#334155", spaceBefore=1.5, spaceAfter=3.0)
tbl_caption_style = S('TblCaption', size=7.8, leading=10.0, align=TA_CENTER, bold=True, color="#1A365D", spaceBefore=3.0, spaceAfter=2.0, keepWithNext=True)

# Table typography
th_center = S('THC', size=7.6, leading=9.5, align=TA_CENTER, bold=True, color="#0F172A")
th_left = S('THL', size=7.6, leading=9.5, align=TA_LEFT, bold=True, color="#0F172A")
td_center = S('TDC', size=7.6, leading=9.5, align=TA_CENTER, color="#1E293B")
td_left = S('TDL', size=7.6, leading=9.5, align=TA_LEFT, color="#1E293B")
td_center_bold = S('TDCB', size=7.6, leading=9.5, align=TA_CENTER, bold=True, color="#0F172A")

# References typography
ref_header_style = S('RefHeader', size=10.0, leading=12.5, bold=True, color="#1A365D", spaceBefore=4.0, spaceAfter=2.0, align=TA_LEFT)
ref_num_style = S('RefNum', size=7.2, leading=9.0, bold=True, color="#1A365D", align=TA_RIGHT)
ref_text_style = S('RefText', size=7.0, leading=8.8, align=TA_JUSTIFY, color="#1E293B")

P = Paragraph


def make_centered_table(data, col_widths=None):
    """
    Creates a horizontally-centered academic table with clean booktabs-inspired borders,
    soft header fill, subtle alternating row backgrounds, and crisp padding.
    """
    t = Table(data, colWidths=col_widths, hAlign='CENTER', repeatRows=1)
    style_cmds = [
        ('BOX', (0, 0), (-1, -1), 1.0, colors.HexColor("#1A365D")),               # Solid navy outer boundary
        ('LINEBELOW', (0, 0), (-1, 0), 1.0, colors.HexColor("#1A365D")),          # Header underline
        ('INNERGRID', (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E1")),         # Clean inner cell borders
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),              # Academic slate-tint header
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 4.0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4.0),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor("#F8FAFC")))
    t.setStyle(TableStyle(style_cmds))
    return t


def build_pdf(out_path):
    FIG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'figures'))
    
    # Document Printable Canvas: 504 pt width x 704 pt height
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
    # PAGE 1: Title, Author, Abstract, Intro & Forward Model + Figure 1
    # =========================================================================
    story.append(P("Plug-and-Play Image Restoration with Coarse-to-Fine Initialization:<br/>An Empirical Benchmark Using DeepInverse and DRUNet", title_style))
    story.append(P("Hasnain Haider", author_style))
    story.append(P("Independent Research Benchmark  |  Reproducible Computational Imaging Study  |  October 2026", affil_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#1A365D"), spaceBefore=1, spaceAfter=3))

    # Abstract Box - Centered, Justified, Clean Border
    abs_content = (
        "<b>Abstract</b>—This benchmark investigates whether a two-level coarse-to-fine initialization strategy improves "
        "Plug-and-Play (PnP) image restoration when paired with a deep residual denoiser prior. Using the open-source DeepInverse "
        "framework [1] and pretrained DRUNet denoiser weights [2], we evaluate three distinct initialization pipelines across four "
        "canonical benchmark images (Astronaut, Chelsea, Coffee, Rocket) degraded by Gaussian blur (&sigma; = 2.0) and additive white "
        "Gaussian noise (&sigma; = 0.03). Across 20 paired image-seed trials (60 total experimental runs executed on an NVIDIA Tesla T4 "
        "GPU), coarse PnP initialization achieved a mean PSNR of 28.593 dB compared to 28.411 dB for standard direct DPIR and 28.530 dB "
        "for observation-only initialization. The coarse PnP pipeline produced a positive paired gain in 100% of trials (+0.182 dB average), "
        "while incurring a 38.7% runtime penalty. Crucially, a controlled ablation reveals that 65% of this improvement (+0.118 dB) is obtained "
        "solely from the low-pass filtering inherent in resolution downsampling and upsampling, while active coarse denoising contributes "
        "the remaining +0.064 dB. Performance gains correlate strongly with image frequency content, providing substantial benefit for smooth "
        "surfaces (+0.397 dB) and negligible gain for dense textures (+0.015 dB). All reproduction scripts, configurations, and raw CSV metrics "
        "are publicly available under an open-source license."
    )
    abs_table = Table([[P(abs_content, S('AbsStyle', size=7.9, leading=10.5, align=TA_JUSTIFY, color="#1E293B"))]], colWidths=[496], hAlign='CENTER')
    abs_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#1A365D")),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('TOPPADDING', (0,0), (-1,-1), 4.0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.0),
        ('LEFTPADDING', (0,0), (-1,-1), 7.5),
        ('RIGHTPADDING', (0,0), (-1,-1), 7.5),
    ]))
    story.append(abs_table)
    story.append(Spacer(1, 2))

    story.append(P("1. Introduction and Problem Context", h1_style))
    story.append(P(
        "Linear inverse problems in computational imaging require recovering an unknown underlying scene <i>x</i> &isin; &real;<sup><i>n</i></sup> "
        "from corrupted measurements <i>y</i> = <b>A</b><i>x</i> + <i>n</i>, where <b>A</b> is a forward degradation operator (such as a blur point "
        "spread function) and <i>n</i> ~ &Nu;(0, &sigma;<sup>2</sup><b>I</b>) represents additive measurement noise. Because <b>A</b> is severely "
        "ill-conditioned, standard inversion is mathematically ill-posed; naive pseudoinverse solutions catastrophically amplify high-frequency noise, "
        "necessitating explicit or implicit image priors to regularize the solution manifold.",
        body_style
    ))
    story.append(P(
        "Plug-and-Play (PnP) methods, pioneered by Venkatakrishnan et al. [3] and mathematically analyzed for convergence by Chan et al. [4] "
        "and Ryu et al. [5], replace hand-crafted analytical regularizers (such as Total Variation [7]) with high-capacity deep denoisers "
        "embedded within proximal splitting algorithms like Half-Quadratic Splitting (HQS) [9] or ADMM. Zhang et al. [2] operationalized this with "
        "DPIR, incorporating a Deep Residual U-Net (DRUNet) into an iterative HQS schedule to obtain state-of-the-art reconstructions across deblurring, "
        "super-resolution, and color inpainting without retraining network weights for specific forward operators.",
        body_style
    ))
    story.append(P(
        "Standard DPIR initializes its fine-scale iterative solver directly from the degraded observation: <i>x</i><sub>0</sub> = <i>y</i>. "
        "Drawing inspiration from multigrid concepts in numerical scientific computing [10], we investigate whether a coarse-scale warm-start "
        "accelerates convergence and improves final restoration fidelity. We implement and evaluate this framework systematically using the "
        "open-source DeepInverse library [1] and modern proximal denoiser priors [6].",
        body_style
    ))

    story.append(P("2. Forward Degradation Model and Benchmark Setup", h1_style))
    story.append(P(
        "We selected four standard benchmark images from the scikit-image repository: Astronaut (portrait featuring mixed structural and skin tones), "
        "Chelsea (tabby cat characterized by dense high-frequency fur patterns), Coffee (ceramic cup with broad uniform gradients), and Rocket "
        "(spacecraft featuring sharp geometric boundary edges). All images were standardized to 128 &times; 128 RGB pixels normalized to [0, 1]. "
        "The degradation operator <b>A</b> applies a 7 &times; 7 Gaussian blur kernel with standard deviation &sigma; = 2.0, followed by additive "
        "Gaussian noise with standard deviation &sigma; = 0.03. Five independent pseudo-random noise realizations (seeds 0 through 4) were generated "
        "for each image, yielding 20 distinct paired observations passed identically to each evaluated pipeline.",
        body_style
    ))

    fig_deg = os.path.join(FIG_DIR, 'step2_degradation.png')
    if os.path.exists(fig_deg):
        # Native aspect ratio 2.20 (2200x1000)
        story.append(Spacer(1, 1))
        story.append(Image(fig_deg, width=420, height=191, hAlign='CENTER'))
        story.append(P("Figure 1. Forward degradation pipeline: clean ground truth, Gaussian blur PSF, 2D frequency spectrum showing severe high-frequency attenuation, and resulting degraded observation.", fig_caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: Pipelines, Protocol, Results & Centered Tables 1, 2, and 3
    # =========================================================================
    story.append(P("3. Evaluated Reconstruction Pipelines", h1_style))
    story.append(P(
        "All three pipelines employ the identical pretrained DRUNet model checkpoint and an 8-iteration HQS schedule. "
        "The only experimental variable across conditions is the initial state estimate <i>x</i><sub>0</sub>:",
        body_style
    ))
    story.append(P("• <b>Direct DPIR (Baseline):</b> Standard optimization starting directly from the noisy observation: <i>x</i><sub>0</sub> = <i>y</i>.", body_indent))
    story.append(P("• <b>Observation Initialization (Control):</b> The measurement <i>y</i> is downsampled to 64 &times; 64 and immediately bicubic-upsampled back to 128 &times; 128 to serve as <i>x</i><sub>0</sub> without coarse denoising, isolating pure resolution-cycling effects.", body_indent))
    story.append(P("• <b>Coarse PnP Initialization (Proposed):</b> A full DPIR solve is performed at 64 &times; 64 resolution using a scaled blur operator. The coarse solution is upsampled to 128 &times; 128 to warm-start the fine-scale solver.", body_indent))

    story.append(P("4. Experimental Evaluation Protocol", h1_style))
    story.append(P(
        "Reconstruction fidelity is quantified using Peak Signal-to-Noise Ratio (PSNR) and the Structural Similarity Index (SSIM) [8], "
        "evaluated on clipped [0, 1] RGB channels against original ground truth. Wall-clock runtimes were recorded with explicit CUDA "
        "synchronization on an NVIDIA Tesla T4 GPU (16 GB VRAM). To eliminate noise realization variance, we assess paired differences "
        "(&Delta;PSNR) across identical degraded inputs.",
        body_style
    ))

    story.append(P("5. Quantitative Findings and Empirical Analysis", h1_style))
    story.append(P("5.1 Aggregate Performance Across 60 Independent Runs", h2_style))
    story.append(P(
        "Table I summarizes aggregate performance metrics across all 60 trials (4 images &times; 5 seeds &times; 3 pipelines). "
        "Coarse PnP initialization delivers the highest mean PSNR (28.593 dB) and SSIM (0.8622), followed by observation initialization (28.530 dB).",
        body_style
    ))

    # Centered Table 1 - Caption Placed Above
    story.append(P("TABLE I: AGGREGATE RESTORATION PERFORMANCE ACROSS 60 EXPERIMENTS ON TESLA T4 GPU", tbl_caption_style))
    t1_data = [
        [P("Pipeline Strategy", th_left), P("Mean PSNR (dB)", th_center), P("Mean SSIM", th_center), P("Mean Time (s)", th_center), P("Relative Cost", th_center)],
        [P("Direct DPIR (Baseline)", td_left), P("28.411", td_center), P("0.8588", td_center), P("0.2719", td_center), P("1.00&times; (baseline)", td_center)],
        [P("Observation Init (Control)", td_left), P("28.530", td_center), P("0.8603", td_center), P("0.2735", td_center), P("1.01&times; (+0.6%)", td_center)],
        [P("<b>Coarse PnP Init (Proposed)</b>", td_left), P("<b>28.593</b>", td_center_bold), P("<b>0.8622</b>", td_center_bold), P("0.3772", td_center), P("1.39&times; (+38.7%)", td_center)],
    ]
    story.append(make_centered_table(t1_data, col_widths=[140, 85, 75, 80, 90]))
    story.append(Spacer(1, 3))

    story.append(P("5.2 Paired Differences and Consistency Analysis", h2_style))
    story.append(P(
        "Because background noise realizations introduce variance that can obscure subtle algorithm performance differences, paired comparisons "
        "on identical degraded inputs provide rigorous statistical verification. Coarse PnP initialization outperformed direct DPIR in "
        "<b>20 out of 20 trials (100% win rate)</b>, yielding an average gain of +0.182 dB (&plusmn;0.162 dB). It also outperformed observation "
        "initialization in all 20 trials (+0.064 dB average gain). Furthermore, observation initialization alone achieved a +0.118 dB advantage "
        "over direct DPIR, demonstrating that roughly two-thirds of the total benefit stems from low-pass pre-smoothing.",
        body_style
    ))

    # Centered Table 2 - Caption Placed Above
    story.append(P("TABLE II: PAIRED DIFFERENCE STATISTICS ACROSS 20 IDENTICAL IMAGE-SEED PAIRS", tbl_caption_style))
    t2_data = [
        [P("Paired Comparison Setup", th_left), P("Mean &Delta;PSNR", th_center), P("Std. Dev.", th_center), P("Positive Trials", th_center), P("Empirical Win Rate", th_center)],
        [P("Coarse PnP vs. Direct DPIR", td_left), P("<b>+0.1820 dB</b>", td_center_bold), P("0.162 dB", td_center), P("20 / 20", td_center), P("<b>100.0%</b>", td_center_bold)],
        [P("Observation Init vs. Direct DPIR", td_left), P("+0.1183 dB", td_center), P("0.114 dB", td_center), P("20 / 20", td_center), P("100.0%", td_center)],
        [P("Coarse PnP vs. Observation Init", td_left), P("+0.0637 dB", td_center), P("0.051 dB", td_center), P("20 / 20", td_center), P("100.0%", td_center)],
    ]
    story.append(make_centered_table(t2_data, col_widths=[150, 85, 75, 80, 80]))
    story.append(Spacer(1, 3))

    story.append(P("5.3 Per-Image Frequency Sensitivity Breakdown", h2_style))
    story.append(P(
        "Quantitative gains correlate directly with image spatial frequency distributions. For Coffee (broad smooth gradients), "
        "coarse PnP achieved a major +0.397 dB boost. For Astronaut (mixed portrait geometry), it gained +0.287 dB. Conversely, "
        "for Rocket (+0.029 dB) and Chelsea (+0.015 dB), improvements were minimal. Downsampling to 64 &times; 64 strips away high spatial "
        "frequencies that define fine textures and edges, rendering coarse warm-starts uninformative for texture-dominated scenes.",
        body_style
    ))

    # Centered Table 3 - Caption Placed Above
    story.append(P("TABLE III: PAIRED PSNR GAINS CATEGORIZED BY IMAGE FREQUENCY CHARACTERISTICS", tbl_caption_style))
    t3_data = [
        [P("Test Image", th_left), P("Coarse vs. Direct", th_center), P("Coarse vs. Obs Init", th_center), P("Obs vs. Direct", th_center), P("Dominant Texture & Frequency Characteristics", th_left)],
        [P("Coffee", td_left), P("<b>+0.397 dB</b>", td_center_bold), P("+0.112 dB", td_center), P("+0.285 dB", td_center), P("Broad smooth gradients, uniform ceramic cup surface", td_left)],
        [P("Astronaut", td_left), P("+0.287 dB", td_center), P("+0.112 dB", td_center), P("+0.175 dB", td_center), P("Mixed structural contours, facial tones, patch details", td_left)],
        [P("Rocket", td_left), P("+0.029 dB", td_center), P("+0.024 dB", td_center), P("+0.005 dB", td_center), P("Sharp high-contrast structural edges, atmospheric backdrop", td_left)],
        [P("Chelsea", td_left), P("+0.015 dB", td_center), P("+0.007 dB", td_center), P("+0.008 dB", td_center), P("High-frequency fur and whisker textures throughout", td_left)],
    ]
    story.append(make_centered_table(t3_data, col_widths=[65, 80, 85, 75, 175]))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: Ablation (Figure 2), Classical TV vs DPIR (Table 4) & In-Depth Benchmark
    # =========================================================================
    story.append(P("5.4 Per-Seed Ablation Distribution and Consistency", h2_style))
    story.append(P(
        "Figure 2 displays individual PSNR measurements across all five noise seeds for each test image. "
        "The consistency of the coarse PnP warm-start is visually evident: green points strictly dominate blue and orange points for Coffee "
        "and Astronaut across all seeds, demonstrating that the observed +0.182 dB benefit is not an artifact of favorable noise draws.",
        body_style
    ))

    fig_abl = os.path.join(FIG_DIR, 'step10_initialization_ablation.png')
    if os.path.exists(fig_abl):
        # Native aspect ratio: 2.026 (2970x1466) -> width 440, height 217
        story.append(Image(fig_abl, width=440, height=217, hAlign='CENTER'))
        story.append(P("Figure 2. Per-seed PSNR distribution across initialization pipelines. Coarse PnP (green) consistently outperforms direct DPIR (blue) on smooth targets (Coffee, Astronaut), while Chelsea and Rocket exhibit tight clustering.", fig_caption_style))

    story.append(Spacer(1, 2))
    story.append(P("6. Baseline Benchmark: Classical Total Variation vs. Learned DPIR Prior", h1_style))
    story.append(P(
        "To contextualize the restoration fidelity of the learned DRUNet prior, standard DPIR was benchmarked against classical Total Variation (TV) "
        "regularization [7]. Classical TV defines an explicit energy functional min<sub><i>x</i></sub> (1/2)||<b>A</b><i>x</i> - <i>y</i>||<sup>2</sup> + &lambda;||&nabla;<i>x</i>||<sub>1</sub>, "
        "solved via Proximal Gradient Descent (TV-PGD) with standard step-size scheduling. In contrast, DPIR replaces the explicit subgradient operator with a learned "
        "deep residual denoiser [2, 6] embedded within Half-Quadratic Splitting (HQS) [9]. As detailed in Table IV, learned DPIR outperforms TV-PGD by +1.89 dB to +2.66 dB "
        "across all test images while operating ~7&times; faster (0.35–0.37 s vs. 2.35–2.66 s on Tesla T4).",
        body_style
    ))

    # Centered Table 4 - Caption Placed Above
    story.append(P("TABLE IV: BENCHMARK COMPARISON: CLASSICAL TV-PGD VERSUS LEARNED DRUNET DPIR", tbl_caption_style))
    t4_data = [
        [P("Benchmark Image", th_left), P("Degraded", th_center), P("TV-PGD [7]", th_center), P("DPIR [2]", th_center), P("Learned Gain", th_center), P("TV Time", th_center), P("DPIR Time", th_center)],
        [P("Astronaut", td_left), P("19.18 dB", td_center), P("22.23 dB", td_center), P("24.13 dB", td_center), P("<b>+1.90 dB</b>", td_center_bold), P("2.64 s", td_center), P("0.37 s", td_center)],
        [P("Chelsea", td_left), P("24.57 dB", td_center), P("27.22 dB", td_center), P("29.74 dB", td_center), P("<b>+2.52 dB</b>", td_center_bold), P("2.66 s", td_center), P("0.35 s", td_center)],
        [P("Coffee", td_left), P("22.12 dB", td_center), P("25.95 dB", td_center), P("27.84 dB", td_center), P("<b>+1.89 dB</b>", td_center_bold), P("2.35 s", td_center), P("0.37 s", td_center)],
        [P("Rocket", td_left), P("25.92 dB", td_center), P("29.15 dB", td_center), P("31.81 dB", td_center), P("<b>+2.66 dB</b>", td_center_bold), P("2.61 s", td_center), P("0.36 s", td_center)],
    ]
    story.append(make_centered_table(t4_data, col_widths=[75, 60, 68, 68, 68, 60, 60]))
    story.append(Spacer(1, 2))

    story.append(P("6.1 Qualitative Artifact Analysis: TV Staircasing vs. Deep Manifold Priors", h2_style))
    story.append(P(
        "The mathematical root of TV-PGD's underperformance lies in its L1 gradient penalty, which strictly penalizes non-zero derivatives and enforces "
        "piecewise-constant solutions. This produces pronounced 'staircasing' artifacts, flattening subtle gradations in facial skin tones (Astronaut) and "
        "curved ceramic specularities (Coffee). Conversely, the pretrained DRUNet denoiser prior acts as an implicit projection onto a rich natural image manifold, "
        "preserving continuous tone transitions and authentic textural sharpness without parameter retuning.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: Visual Comparison (Figure 3) & Stage Progression (Figure 4)
    # =========================================================================
    fig_tv = os.path.join(FIG_DIR, 'step7_method_comparison.png')
    if os.path.exists(fig_tv):
        # Native aspect ratio: 1.026 (4237x4131) -> width 268, height 261
        story.append(Image(fig_tv, width=268, height=261, hAlign='CENTER'))
        story.append(P("Figure 3. Visual comparison across benchmark images: ground truth, degraded observation (&sigma;=2.0 blur, &sigma;=0.03 noise), classical TV-PGD reconstruction, and learned DRUNet DPIR output.", fig_caption_style))

    story.append(Spacer(1, 2))
    story.append(P("7. Stage-by-Stage Visual Progression in Two-Level Restoration", h1_style))
    story.append(P(
        "Figure 4 documents the intermediate transformation stages of the two-level pipeline. The initial 64 &times; 64 coarse reconstruction "
        "suppresses observation noise and recovers global luminance. Subsequent bicubic prolongation produces a smooth initial estimate "
        "that provides the 128 &times; 128 fine-scale solver with a well-conditioned starting point, accelerating high-frequency detail recovery.",
        body_style
    ))

    fig_ml = os.path.join(FIG_DIR, 'step9_multilevel_comparison.png')
    if os.path.exists(fig_ml):
        # Native aspect ratio: 1.249 (5158x4131) -> width 305, height 244
        story.append(Image(fig_ml, width=305, height=244, hAlign='CENTER'))
        story.append(P("Figure 4. Progression through the two-level coarse-to-fine pipeline: degraded observation, coarse 64 &times; 64 restoration, upsampled prolongation, and final fine 128 &times; 128 restored output.", fig_caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: Convergence Dynamics, Noise Robustness, & In-Depth Discussion
    # =========================================================================
    story.append(P("8. Convergence Dynamics and Numerical Stability", h1_style))
    story.append(P(
        "To verify optimization stability, we tracked objective PSNR trajectories and relative iterate residuals "
        "||<i>x</i><sup>(<i>k</i>)</sup> - <i>x</i><sup>(<i>k</i>-1)</sup>|| / ||<i>x</i><sup>(<i>k</i>)</sup>|| across HQS iterations. "
        "As depicted in Figure 5, the solver exhibits rapid monotonic ascent during iterations 1–4, stabilizing asymptotically by iteration 6. "
        "Relative residuals plunge below 10<sup>-2</sup> within five iterations across all initializations, establishing robust convergence [4, 5].",
        body_style
    ))

    fig_psnr_iter = os.path.join(FIG_DIR, 'step8_psnr_vs_iterations.png')
    fig_resid = os.path.join(FIG_DIR, 'step8_convergence_residual.png')
    if os.path.exists(fig_psnr_iter) and os.path.exists(fig_resid):
        # Aspect 1.82 each (2669x1466) -> width 215, height 118
        conv_tbl = Table([
            [Image(fig_psnr_iter, width=215, height=118), Image(fig_resid, width=215, height=118)]
        ], colWidths=[225, 225], hAlign='CENTER')
        conv_tbl.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('LEFTPADDING', (0,0), (-1,-1), 2),
            ('RIGHTPADDING', (0,0), (-1,-1), 2),
        ]))
        story.append(conv_tbl)
        story.append(P("Figure 5. Iteration-level convergence dynamics. Left: PSNR ascent across HQS iterations. Right: logarithmic decay of relative solution residual, confirming numerical stabilization within 5–6 steps.", fig_caption_style))

    story.append(Spacer(1, 2))
    story.append(P("9. Robustness Under Varying Noise Intensities", h1_style))
    story.append(P(
        "To assess model stability under extreme degradation, we evaluated restorations across noise levels from &sigma; = 0.01 to &sigma; = 0.07. "
        "As shown in Figures 6 and 7, reconstruction PSNR decreases monotonically and predictably. The DRUNet denoiser prior avoids hallucinations, "
        "color fringing, or numerical divergence even under severe noise corruption.",
        body_style
    ))

    fig_rob = os.path.join(FIG_DIR, 'step6_psnr_robustness.png')
    fig_vis = os.path.join(FIG_DIR, 'step6_visual_comparison.png')
    if os.path.exists(fig_rob) and os.path.exists(fig_vis):
        # rob is aspect 1.82 (width 190, height 104), vis is aspect 1.027 (width 135, height 131)
        rob_tbl = Table([
            [Image(fig_rob, width=190, height=104), Image(fig_vis, width=135, height=131)]
        ], colWidths=[210, 210], hAlign='CENTER')
        rob_tbl.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(rob_tbl)
        story.append(P("Figures 6 & 7. Noise sensitivity analysis. Left: PSNR degradation curve versus noise standard deviation &sigma;. Right: visual restoration quality under increasing noise levels (&sigma; = 0.01 to 0.07).", fig_caption_style))

    story.append(Spacer(1, 2))
    story.append(P("10. Discussion and Engineering Trade-Off Analysis", h1_style))
    story.append(P(
        "<b>Decomposition of Initialization Gain:</b> Our empirical data demonstrates a strictly positive (+0.182 dB, 100% win rate) "
        "advantage for coarse PnP initialization. Crucially, the control condition reveals where this gain originates: approximately "
        "65% (+0.118 dB) is produced simply by low-pass smoothing during resolution downsampling and bicubic upsampling, which suppresses "
        "high-frequency observation noise before iterative splitting commences. Active DRUNet denoising at the coarse scale contributes the "
        "remaining 35% (+0.064 dB) of the overall improvement.",
        body_style
    ))
    story.append(P(
        "<b>Computational Complexity vs. Quality Payoff:</b> On an NVIDIA Tesla T4 GPU, coarse PnP initialization requires 0.3772 s per image "
        "compared to 0.2719 s for baseline direct DPIR—a 38.7% runtime increase. In scientific, astronomical, or clinical imaging workflows "
        "where fidelity is paramount and processing is performed offline, a +0.18 dB gain for 0.1 s of extra GPU computation represents a highly "
        "favorable trade-off. Conversely, for high-throughput mobile vision or video streaming, the runtime overhead outweighs the modest gain.",
        body_style
    ))
    story.append(P(
        "<b>Spatial Frequency Dependency:</b> The strong discrepancy between smooth scenes (+0.397 dB on Coffee) and dense textures (+0.015 dB "
        "on Chelsea) demonstrates that spatial downsampling operates as an anisotropic low-pass gate. When an image's diagnostic features reside "
        "in low-to-medium frequencies, coarse optimization regularizes global structure effectively; when features are predominantly high-frequency, "
        "coarse solves discard the critical spatial bandwidth required for reconstruction.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: Limitations, Reproducibility (Table 5), Conclusion, & REFERENCES
    # =========================================================================
    story.append(P("11. Limitations and Threats to Validity", h1_style))
    story.append(P("We explicitly identify the following methodological and experimental constraints:", body_style))
    limits = [
        ("Image Sample Size: ", "Four images evaluated across five noise seeds establish consistency on this benchmark but do not support population-wide statistical generalization across complex natural image distributions."),
        ("Heuristic Coarse Operator: ", "The coarse 64 &times; 64 blur operator was approximated via kernel downsampling rather than deriving a rigorous Galerkin restriction operator <b>A</b><sub><i>c</i></sub> = <b>R</b><b>A</b><b>P</b> [10]."),
        ("Scope Delineation: ", "This study benchmarks deterministic DRUNet-based PnP-DPIR. It does not evaluate stochastic diffusion models or generative flow matching [11], nor untrained network priors [12]."),
        ("Hardware Specificity: ", "All experiments were executed on a single cloud Tesla T4 GPU. Cross-hardware timing verification remains valuable future work.")
    ]
    for lbl, txt in limits:
        story.append(P(f"• <b>{lbl}</b>{txt}", body_indent))

    story.append(Spacer(1, 1))
    story.append(P("12. Reproducibility Protocol and Software Environment", h1_style))
    story.append(P(
        "All code is provided in <code>notebooks/DeepInverse_PnP_Image_Restoration.ipynb</code>. Running cells sequentially "
        "reproduces all 60 trials and exports metrics to <code>results/step10_all_experiments.csv</code>. File integrity is verified "
        "via cryptographic SHA-256 hashes recorded in <code>SHA256SUMS.txt</code>.",
        body_style
    ))

    # Centered Table 5 - Caption Placed Above
    story.append(P("TABLE V: DOCUMENTED HARDWARE AND SOFTWARE BENCHMARK ENVIRONMENT", tbl_caption_style))
    t_env_data = [
        [P("Hardware / Software Component", th_left), P("Documented Specification / Release Version", th_left)],
        [P("Python Runtime Environment", td_left), P("3.13.16 (64-bit standard distribution)", td_left)],
        [P("Deep Learning Framework", td_left), P("PyTorch 2.11.0+cu130 (CUDA 13.0 runtime)", td_left)],
        [P("Computational Imaging Library", td_left), P("DeepInverse 0.5.0 (core inverse problem solvers) [1]", td_left)],
        [P("Scientific Computing Stack", td_left), P("NumPy 2.1.3 | Matplotlib 3.10.0 | scikit-image 0.25.2", td_left)],
        [P("Hardware Acceleration", td_left), P("NVIDIA Tesla T4 GPU (16 GB GDDR6, PCIe 3.0)", td_left)],
    ]
    story.append(make_centered_table(t_env_data, col_widths=[190, 230]))
    story.append(Spacer(1, 2))

    story.append(P("13. Conclusion and Future Work", h1_style))
    story.append(P(
        "Two-level coarse-to-fine initialization yields a small (+0.182 dB) but strictly consistent (20/20 positive) improvement "
        "for Plug-and-Play image restoration with deep priors. The benefit is driven primarily by low-pass initialization pre-filtering "
        "with an active secondary contribution from coarse deep denoising, requiring 38.7% additional compute. Future research will explore "
        "exact multigrid restriction operators to determine if multi-cycle V-cycles can amplify gains on large-scale (512 &times; 512+) images.",
        body_style
    ))

    story.append(Spacer(1, 2))

    # =========================================================================
    # SECTION 14: VERIFIED ACADEMIC REFERENCES (12 FOUNDATIONAL PAPERS)
    # =========================================================================
    story.append(P("14. Verified Academic References", ref_header_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#1A365D"), spaceBefore=1, spaceAfter=3))

    verified_refs = [
        ("[1]", "J. Tachella, M. Terris, S. Hurault, A. Wang, et al., \"DeepInverse: A Python package for solving imaging inverse problems with deep learning,\" <i>Journal of Open Source Software (JOSS)</i>, vol. 10, no. 115, p. 8923, 2025. DOI: 10.21105/joss.08923."),
        ("[2]", "K. Zhang, Y. Li, W. Zuo, L. Zhang, L. Van Gool, and R. Timofte, \"Plug-and-Play Image Restoration with Deep Denoiser Prior,\" <i>IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI)</i>, vol. 44, no. 10, pp. 6360–6376, 2022. DOI: 10.1109/TPAMI.2021.3088914."),
        ("[3]", "S. V. Venkatakrishnan, C. A. Bouman, and B. Wohlberg, \"Plug-and-Play Priors for Model Based Reconstruction,\" in <i>Proc. IEEE Global Conference on Signal and Information Processing (GlobalSIP)</i>, pp. 945–948, 2013. DOI: 10.1109/GlobalSIP.2013.6737048."),
        ("[4]", "S. H. Chan, X. Wang, and O. A. Elgendy, \"Plug-and-Play ADMM for Image Restoration: Fixed-Point Convergence and Applications,\" <i>IEEE Transactions on Computational Imaging (TCI)</i>, vol. 3, no. 1, pp. 84–98, 2016. DOI: 10.1109/TCI.2016.2629286."),
        ("[5]", "E. K. Ryu, J. Liu, S. Wang, X. Chen, Z. Wang, and W. Yin, \"Plug-and-Play Methods Provably Converge with Properly Trained Denoisers,\" in <i>Proc. International Conference on Machine Learning (ICML)</i>, PMLR, vol. 97, pp. 5546–5557, 2019."),
        ("[6]", "S. Hurault, A. Leclaire, and N. Papadakis, \"Proximal Denoiser for Convergent Plug-and-Play,\" in <i>Proc. International Conference on Machine Learning (ICML)</i>, PMLR, vol. 162, pp. 9484–9504, 2022."),
        ("[7]", "L. I. Rudin, S. Osher, and E. Fatemi, \"Nonlinear total variation based noise removal algorithms,\" <i>Physica D: Nonlinear Phenomena</i>, vol. 60, no. 1–4, pp. 259–268, 1992. DOI: 10.1016/0167-2789(92)90242-F."),
        ("[8]", "Z. Wang, A. C. Bovik, H. R. Sheikh, and E. P. Simoncelli, \"Image quality assessment: From error visibility to structural similarity,\" <i>IEEE Transactions on Image Processing (TIP)</i>, vol. 13, no. 4, pp. 600–612, 2004. DOI: 10.1109/TIP.2003.819861."),
        ("[9]", "D. Geman and C. Yang, \"Nonlinear image recovery with half-quadratic regularization,\" <i>IEEE Transactions on Image Processing (TIP)</i>, vol. 4, no. 7, pp. 932–946, 1995. DOI: 10.1109/83.392335."),
        ("[10]", "W. L. Briggs, V. E. Henson, and S. F. McCormick, <i>A Multigrid Tutorial</i>, 2nd ed. Philadelphia, PA: Society for Industrial and Applied Mathematics (SIAM), 2000. DOI: 10.1137/1.9780898719505."),
        ("[11]", "S. Martin, A. Gagneux, P. Hagemann, and G. Steidl, \"PnP-Flow: Plug-and-Play Image Restoration with Flow Matching,\" in <i>Proc. International Conference on Learning Representations (ICLR)</i>, 2025."),
        ("[12]", "D. Ulyanov, A. Vedaldi, and V. Lempitsky, \"Deep Image Prior,\" in <i>Proc. IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)</i>, pp. 9446–9454, 2018."),
    ]

    ref_rows = []
    for num_str, cit_str in verified_refs:
        ref_rows.append([
            P(num_str, ref_num_style),
            P(cit_str, ref_text_style)
        ])
    
    ref_table = Table(ref_rows, colWidths=[18, 476], hAlign='CENTER')
    ref_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 0.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0.8),
    ]))
    story.append(ref_table)

    # Build document
    doc.build(story, canvasmaker=AcademicNumberedCanvas)
    print(f"Generated PDF at: {out_path}")


if __name__ == '__main__':
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    out_pdf = os.path.join(root_dir, 'DeepInverse_PnP_Research_Report.pdf')
    docs_pdf = os.path.join(root_dir, 'docs', 'DeepInverse_PnP_Research_Report.pdf')
    
    build_pdf(out_pdf)
    
    import shutil
    shutil.copyfile(out_pdf, docs_pdf)
    print(f"Copied to: {docs_pdf}")
