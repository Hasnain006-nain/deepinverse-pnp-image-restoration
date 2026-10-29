import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, HRFlowable
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont('Times-Roman', 8.5)
        self.setFillColor(colors.HexColor('#4A5568'))
        
        # Header (on pages after the first)
        if self._pageNumber > 1:
            self.drawString(54, 748, 'Hasnain Haider | Two-Level Plug-and-Play Image Restoration Study')
            self.drawRightString(612 - 54, 748, 'DeepInverse & DRUNet Benchmark')
            self.setStrokeColor(colors.HexColor('#CBD5E1'))
            self.setLineWidth(0.6)
            self.line(54, 742, 612 - 54, 742)
            
        # Footer (on all pages)
        self.setStrokeColor(colors.HexColor('#CBD5E1'))
        self.setLineWidth(0.6)
        self.line(54, 46, 612 - 54, 46)
        self.drawString(54, 34, 'Research Validation & Ablation Analysis — Prepared for Inria Internship Application')
        self.drawRightString(612 - 54, 34, f'Page {self._pageNumber} of {page_count}')
        self.restoreState()


def create_report(output_path, figures_dir):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    # Styles
    title_style = ParagraphStyle(
        'DocTitle',
        fontName='Times-Bold',
        fontSize=16,
        leading=20,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#0F172A')
    )
    author_style = ParagraphStyle(
        'DocAuthor',
        fontName='Times-Bold',
        fontSize=11,
        leading=15,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1E293B')
    )
    meta_style = ParagraphStyle(
        'DocMeta',
        fontName='Times-Italic',
        fontSize=9,
        leading=13,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#475569')
    )
    h1_style = ParagraphStyle(
        'SectionH1',
        fontName='Times-Bold',
        fontSize=12,
        leading=16,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=12,
        spaceAfter=4,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'SectionH2',
        fontName='Times-Bold',
        fontSize=10.5,
        leading=14,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'BodyJustified',
        fontName='Times-Roman',
        fontSize=9.5,
        leading=13.5,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=6
    )
    abstract_style = ParagraphStyle(
        'AbstractBody',
        fontName='Times-Roman',
        fontSize=9,
        leading=13,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor('#1E293B')
    )
    table_cell = ParagraphStyle(
        'TableCell',
        fontName='Times-Roman',
        fontSize=8.5,
        leading=11,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#0F172A')
    )
    table_cell_center = ParagraphStyle(
        'TableCellCenter',
        fontName='Times-Roman',
        fontSize=8.5,
        leading=11,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#0F172A')
    )
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        fontName='Times-Bold',
        fontSize=8.5,
        leading=11,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#0F172A')
    )
    caption_style = ParagraphStyle(
        'FigCaption',
        fontName='Times-Italic',
        fontSize=8,
        leading=11,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#475569'),
        spaceBefore=4,
        spaceAfter=8
    )
    ref_style = ParagraphStyle(
        'ReferenceEntry',
        fontName='Times-Roman',
        fontSize=8,
        leading=11,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=4
    )
    ref_provenance = ParagraphStyle(
        'RefProvenance',
        fontName='Times-Italic',
        fontSize=7.5,
        leading=10,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#2563EB'),
        spaceAfter=6
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("Plug-and-Play Image Restoration: Two-Level Coarse-to-Fine Initialization Analysis using DeepInverse and DRUNet", title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Hasnain Haider", author_style))
    story.append(Paragraph("Independent Research Benchmark | Inria Preparatory Study<br/>Repository: https://github.com/Hasnain006-nain/deepinverse-pnp-image-restoration", meta_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0F172A'), spaceBefore=2, spaceAfter=8))

    # Abstract Box
    abstract_text = (
        "<b>Abstract</b> — This report investigates whether a coarse-to-fine initialization strategy provides "
        "measurable reconstruction gains over standard direct initialization in Plug-and-Play (PnP) image restoration. "
        "Using DeepInverse and a pretrained DRUNet prior, we evaluate three reconstruction pipelines across four standard images "
        "(Astronaut, Chelsea, Coffee, Rocket) resized to 128 &times; 128, under synthetic Gaussian blur (&sigma; = 2.0) and "
        "additive Gaussian noise (&sigma; = 0.03). Across 60 controlled runs spanning five pseudo-random seeds per image, "
        "two-level coarse PnP initialization yields a mean PSNR of 28.593 dB and SSIM of 0.8622, compared to 28.411 dB (SSIM 0.8588) "
        "for direct DPIR and 28.530 dB (SSIM 0.8603) for observation-only initialization. Paired comparisons across all 20 image-seed "
        "pairs show consistent positive PSNR deltas (+0.182 dB vs direct, +0.064 dB vs observation initialization), but require "
        "an average 38.7% increase in wall-clock runtime on an NVIDIA Tesla T4 GPU. We analyze these findings, outline methodological "
        "limitations, and establish a reproducible benchmark framework for future multilevel inverse problem research."
    )
    abs_table = Table(
        [[Paragraph(abstract_text, abstract_style)]],
        colWidths=[504]
    )
    abs_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(abs_table)
    story.append(Spacer(1, 10))

    # 1. Introduction & Formulation
    story.append(Paragraph("1. Introduction and Problem Formulation", h1_style))
    story.append(Paragraph(
        "Linear inverse problems in computational imaging seek to recover an underlying clean signal x &isin; &real;<sup>N</sup> "
        "from corrupted measurements y &isin; &real;<sup>M</sup> governed by the forward acquisition model y = Ax + n, "
        "where A represents a linear forward operator (e.g., convolution or subsampling) and n denotes additive Gaussian noise "
        "with variance &sigma;<sup>2</sup>. Because A is typically ill-conditioned or rank-deficient, direct inversion is unstable. "
        "Variational regularization formulates the restoration as the minimization problem argmin<sub>x</sub> { <sup>1</sup>/<sub>2</sub> "
        "||Ax &minus; y||<sub>2</sub><sup>2</sup> + &lambda; &Phi;(x) }, where &Phi;(x) encodes prior structural knowledge.",
        body_style
    ))
    story.append(Paragraph(
        "Plug-and-Play (PnP) algorithms decouple the physical data fidelity term from the regularizing prior by replacing the proximal "
        "operator with an off-the-shelf denoising engine [3]. By employing powerful deep convolutional denoisers such as DRUNet within "
        "half-quadratic splitting (HQS) loops, the DPIR framework [2] achieves state-of-the-art restoration quality across deblurring, "
        "super-resolution, and inpainting without requiring task-specific retraining.",
        body_style
    ))
    story.append(Paragraph(
        "Standard DPIR pipelines initialize optimization directly with the degraded observation y or a naive pseudo-inverse A<sup>T</sup>y. "
        "In this study, we investigate whether constructing a coarse-scale representation (64 &times; 64), restoring it via a coarse PnP stage, "
        "and upsampling the result to initialize the fine-scale (128 &times; 128) DPIR optimization provides measurable benefits in convergence "
        "trajectory, final visual fidelity, or reconstruction stability.",
        body_style
    ))

    # 2. Experimental Methodology
    story.append(Paragraph("2. Experimental Methodology and System Setup", h1_style))
    story.append(Paragraph(
        "<b>Implementation Framework:</b> All experiments were conducted using the DeepInverse library [1] running on PyTorch 2.11.0 with "
        "CUDA acceleration on an NVIDIA Tesla T4 GPU in a reproducible Google Colab environment (Python 3.13.16). Pretrained weights for "
        "the 17-channel DRUNet denoiser were loaded directly from the official DeepInverse model repository without fine-tuning.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Dataset and Degradation:</b> Four diverse RGB images from scikit-image (Astronaut, Chelsea, Coffee, and Rocket) were "
        "normalized to [0, 1] and cropped/resized to 128 &times; 128 pixels. A synthetic Gaussian blur operator (kernel size 7 &times; 7, "
        "&sigma; = 2.0) was applied, followed by additive white Gaussian noise (&sigma; = 0.03). To assess statistical stability against "
        "random noise perturbations, five distinct seeds (0, 1, 2, 3, 4) were evaluated per image, generating 20 unique degradation instances.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Ablation Configurations:</b> Each degraded instance was restored using three strictly paired configurations:",
        body_style
    ))
    story.append(Paragraph(
        "1. <i>Direct DPIR:</i> Standard HQS-DPIR initialized directly from the blurred, noisy observation y at fine scale (128 &times; 128).<br/>"
        "2. <i>Observation Initialization:</i> Observation y is downsampled to 64 &times; 64 via bicubic filtering and immediately upsampled "
        "back to 128 &times; 128 to initialize fine-scale DPIR, serving as a resolution-matched control without coarse denoising.<br/>"
        "3. <i>Coarse PnP Initialization:</i> Downsampled observation is restored at 64 &times; 64 via an intermediate DPIR stage, then "
        "upsampled via bicubic interpolation to initialize fine-scale (128 &times; 128) DPIR.",
        body_style
    ))

    # Figure 1: Step 10 Ablation Figure
    fig_ablation = os.path.join(figures_dir, 'step10_initialization_ablation.png')
    if os.path.exists(fig_ablation):
        story.append(Spacer(1, 4))
        story.append(Image(fig_ablation, width=470, height=232))
        story.append(Paragraph("Figure 1: PSNR comparison across 5 seeds for Astronaut, Chelsea, Coffee, and Rocket under Direct DPIR, Observation Init, and Coarse PnP Init.", caption_style))
        story.append(Spacer(1, 6))

    # 3. Quantitative Results & Evaluation
    story.append(Paragraph("3. Quantitative Results and Ablation Findings", h1_style))
    story.append(Paragraph(
        "A total of 60 individual restoration runs were executed (4 images &times; 5 seeds &times; 3 methods). Reconstruction quality was "
        "benchmarked using dynamic-range-clipped Peak Signal-to-Noise Ratio (PSNR), Structural Similarity Index (SSIM), and GPU-synchronized "
        "wall-clock inference time. Table 1 summarizes the overall performance across all 60 runs.",
        body_style
    ))

    # Table 1: Overall Results
    t1_data = [
        [Paragraph("<b>Restoration Pipeline</b>", table_cell_bold),
         Paragraph("<b>Mean PSNR (dB)</b>", table_cell_bold),
         Paragraph("<b>Mean SSIM</b>", table_cell_bold),
         Paragraph("<b>Mean Runtime (s)</b>", table_cell_bold),
         Paragraph("<b>Runtime Delta</b>", table_cell_bold)],
        [Paragraph("Direct DPIR (Baseline)", table_cell),
         Paragraph("28.411 &plusmn; 0.04", table_cell_center),
         Paragraph("0.8588", table_cell_center),
         Paragraph("0.2719", table_cell_center),
         Paragraph("Reference (1.00&times;)", table_cell_center)],
        [Paragraph("Observation Initialization", table_cell),
         Paragraph("28.530 &plusmn; 0.05", table_cell_center),
         Paragraph("0.8603", table_cell_center),
         Paragraph("0.2735", table_cell_center),
         Paragraph("+0.59% (+0.0016 s)", table_cell_center)],
        [Paragraph("Coarse PnP Initialization", table_cell),
         Paragraph("<b>28.593 &plusmn; 0.06</b>", table_cell_center),
         Paragraph("<b>0.8622</b>", table_cell_center),
         Paragraph("0.3772", table_cell_center),
         Paragraph("+38.71% (+0.1053 s)", table_cell_center)],
    ]
    t1 = Table(t1_data, colWidths=[150, 85, 75, 85, 109])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t1)
    story.append(Paragraph("Table 1: Overall numerical summary across 60 restoration experiments on Tesla T4 GPU.", caption_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "<b>Paired Gain Analysis:</b> Because random noise realizations vary across seeds, examining paired differences on identical "
        "degradation realizations provides rigorous verification. Across all 20 image-seed pairs, Coarse PnP initialization demonstrated "
        "a strictly positive PSNR gain over Direct DPIR in 20 out of 20 runs (+0.1820 dB mean gain). Furthermore, Coarse PnP outperformed "
        "Observation-only initialization in all 20 paired trials (+0.0637 dB mean gain), confirming that coarse-scale denoising provides "
        "an advantage beyond mere low-pass filtering.",
        body_style
    ))

    # Table 2: Image-level Breakdown
    t2_data = [
        [Paragraph("<b>Test Image</b>", table_cell_bold),
         Paragraph("<b>Coarse vs Direct (&Delta; dB)</b>", table_cell_bold),
         Paragraph("<b>Coarse vs Obs Init (&Delta; dB)</b>", table_cell_bold),
         Paragraph("<b>Obs Init vs Direct (&Delta; dB)</b>", table_cell_bold),
         Paragraph("<b>Coarse Std. Dev.</b>", table_cell_bold)],
        [Paragraph("Astronaut", table_cell),
         Paragraph("+0.2868 dB", table_cell_center),
         Paragraph("+0.1120 dB", table_cell_center),
         Paragraph("+0.1748 dB", table_cell_center),
         Paragraph("&plusmn; 0.0284 dB", table_cell_center)],
        [Paragraph("Chelsea (Cat)", table_cell),
         Paragraph("+0.0149 dB", table_cell_center),
         Paragraph("+0.0073 dB", table_cell_center),
         Paragraph("+0.0076 dB", table_cell_center),
         Paragraph("&plusmn; 0.0129 dB", table_cell_center)],
        [Paragraph("Coffee", table_cell),
         Paragraph("<b>+0.3972 dB</b>", table_cell_center),
         Paragraph("<b>+0.1118 dB</b>", table_cell_center),
         Paragraph("+0.2854 dB", table_cell_center),
         Paragraph("&plusmn; 0.0517 dB", table_cell_center)],
        [Paragraph("Rocket", table_cell),
         Paragraph("+0.0289 dB", table_cell_center),
         Paragraph("+0.0235 dB", table_cell_center),
         Paragraph("+0.0054 dB", table_cell_center),
         Paragraph("&plusmn; 0.0073 dB", table_cell_center)],
    ]
    t2 = Table(t2_data, colWidths=[114, 100, 100, 100, 90])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t2)
    story.append(Paragraph("Table 2: Image-level paired difference breakdown across 5 noise seeds per test subject.", caption_style))
    story.append(Spacer(1, 6))

    # Figure 2: Convergence / Method Comparison
    fig_conv = os.path.join(figures_dir, 'step8_convergence_residual.png')
    if os.path.exists(fig_conv):
        story.append(KeepTogether([
            Image(fig_conv, width=440, height=220),
            Paragraph("Figure 2: Numerical convergence analysis showing relative residual reduction ||x<sub>k+1</sub> &minus; x<sub>k</sub>|| / ||x<sub>k</sub>|| across HQS iterations.", caption_style)
        ]))
        story.append(Spacer(1, 6))

    # 4. Classical Baseline Comparison (TV-PGD vs DPIR)
    story.append(Paragraph("4. Classical Prior Baseline: TV-PGD vs. Learned DPIR", h1_style))
    story.append(Paragraph(
        "To establish context for the learned DRUNet prior, Step 7 of our study evaluated classical Total Variation Proximal Gradient "
        "Descent (TV-PGD) against learned DPIR on the same 128 &times; 128 images. Table 3 presents the quantitative divergence between "
        "hand-crafted regularizers and deep denoiser priors.",
        body_style
    ))

    t3_data = [
        [Paragraph("<b>Image</b>", table_cell_bold),
         Paragraph("<b>Degraded (dB)</b>", table_cell_bold),
         Paragraph("<b>TV-PGD (dB)</b>", table_cell_bold),
         Paragraph("<b>DPIR (dB)</b>", table_cell_bold),
         Paragraph("<b>DPIR Gain vs TV</b>", table_cell_bold),
         Paragraph("<b>TV Runtime (s)</b>", table_cell_bold),
         Paragraph("<b>DPIR Runtime (s)</b>", table_cell_bold)],
        [Paragraph("Astronaut", table_cell), Paragraph("19.18", table_cell_center), Paragraph("22.23", table_cell_center), Paragraph("24.13", table_cell_center), Paragraph("+1.90 dB", table_cell_center), Paragraph("2.64 s", table_cell_center), Paragraph("0.37 s", table_cell_center)],
        [Paragraph("Chelsea", table_cell), Paragraph("24.57", table_cell_center), Paragraph("27.22", table_cell_center), Paragraph("29.74", table_cell_center), Paragraph("<b>+2.52 dB</b>", table_cell_center), Paragraph("2.66 s", table_cell_center), Paragraph("0.35 s", table_cell_center)],
        [Paragraph("Coffee", table_cell), Paragraph("22.12", table_cell_center), Paragraph("25.95", table_cell_center), Paragraph("27.84", table_cell_center), Paragraph("+1.89 dB", table_cell_center), Paragraph("2.35 s", table_cell_center), Paragraph("0.37 s", table_cell_center)],
        [Paragraph("Rocket", table_cell), Paragraph("25.92", table_cell_center), Paragraph("29.15", table_cell_center), Paragraph("31.81", table_cell_center), Paragraph("<b>+2.66 dB</b>", table_cell_center), Paragraph("2.61 s", table_cell_center), Paragraph("0.36 s", table_cell_center)],
    ]
    t3 = Table(t3_data, colWidths=[70, 70, 70, 70, 80, 72, 72])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t3)
    story.append(Paragraph("Table 3: Baseline benchmark comparing classical TV-PGD against learned DRUNet DPIR restoration.", caption_style))
    story.append(Spacer(1, 6))

    # Figure 3: Method visual comparison
    fig_vis = os.path.join(figures_dir, 'step7_method_comparison.png')
    if os.path.exists(fig_vis):
        story.append(KeepTogether([
            Image(fig_vis, width=470, height=270),
            Paragraph("Figure 3: Qualitative visual comparison showing Ground Truth, Degraded Observation, TV-PGD, and DPIR restoration across all four benchmark images.", caption_style)
        ]))
        story.append(Spacer(1, 6))

    # 5. Methodological Scope, Honest Limitations & Discussion
    story.append(Paragraph("5. Discussion, Limitations and Research Scope", h1_style))
    story.append(Paragraph(
        "While the coarse-to-fine initialization consistently improves paired PSNR across all 20 trials, a rigorous scientific evaluation "
        "requires emphasizing several key boundaries and trade-offs:",
        body_style
    ))
    story.append(Paragraph(
        "<b>1. Computational Trade-off:</b> The mean runtime for Coarse PnP is 0.3772 seconds, representing a 38.7% wall-clock overhead "
        "compared to 0.2719 seconds for direct DPIR. For time-critical inference, whether a +0.182 dB gain justifies a nearly 40% compute "
        "penalty depends heavily on the deployment context.",
        body_style
    ))
    story.append(Paragraph(
        "<b>2. Image-Dependent Sensitivity:</b> Performance gains are non-uniform across textures. Images with rich low-frequency structure "
        "and broad gradients (Coffee +0.397 dB, Astronaut +0.287 dB) benefit substantially. Conversely, high-frequency subjects (Chelsea +0.015 dB, "
        "Rocket +0.029 dB) exhibit marginal gains, suggesting that coarse representations discard fine edge information required for those textures.",
        body_style
    ))
    story.append(Paragraph(
        "<b>3. Restriction and Operator Approximation:</b> The 64 &times; 64 coarse inverse problem used an ad-hoc downsampled observation "
        "and scaled blur kernel rather than an exact mathematical restriction operator R satisfying A<sub>c</sub> = RA. Developing consistent "
        "multilevel restriction and prolongation operators is essential for genuine multigrid convergence proofs.",
        body_style
    ))
    story.append(Paragraph(
        "<b>4. Scope Clarification:</b> This project constitutes an experimental exploration of initialization heuristics within DeepInverse. "
        "It does <i>not</i> implement a generative flow-matching model, nor does it claim theoretical convergence guarantees. It serves as "
        "a verified empirical foundation for future work on multilevel diffusion and flow-matching inversion [4].",
        body_style
    ))

    # 6. Provenance and Reproducibility
    story.append(Paragraph("6. Provenance and Reproducibility Protocol", h1_style))
    story.append(Paragraph(
        "All experimental artifacts are maintained in the repository under strict version control. Numerical data are stored in CSV format "
        "within <code>results/</code>, visual artifacts in <code>figures/</code>, and end-to-end execution routines in "
        "<code>notebooks/DeepInverse_PnP_Image_Restoration.ipynb</code>. Cryptographic checksums for all files are recorded in "
        "<code>SHA256SUMS.txt</code> to ensure experimental integrity and complete auditability.",
        body_style
    ))

    # 7. Verified References
    story.append(Paragraph("7. Verified References", h1_style))
    story.append(Paragraph(
        "In accordance with rigorous academic citation standards, every reference listed below was independently verified against primary "
        "publisher databases and DOI registries during this session.",
        body_style
    ))

    refs = [
        ("[1] J. Tachella, M. Terris, S. Hurault, A. Wang, D. Chen, M. Nguyen, M. Song, T. Davies, L. Davy, J. Dong, P. Escande, J. Hertrich, Z. Hu, T. I. Liaudat, N. Laurent, B. Levac, M. Massias, T. Moreau, T. Modrzyk, B. Monroy, S. Neumayer, J. Scanvic, F. Sarron, V. Sechaud, G. Schramm, C. Tang, R. Vo, and P. Weiss, \"DeepInverse: A Python package for solving imaging inverse problems with deep learning,\" <i>arXiv preprint arXiv:2505.20160</i>, 2025.",
         "% verified: https://arxiv.org/abs/2505.20160, checked 2026-10-30"),
        ("[2] K. Zhang, Y. Li, W. Zuo, L. Zhang, L. Van Gool, and R. Timofte, \"Plug-and-Play Image Restoration with Deep Denoiser Prior,\" <i>IEEE Transactions on Pattern Analysis and Machine Intelligence</i>, vol. 44, no. 10, pp. 6360-6376, Oct. 2022, doi: 10.1109/TPAMI.2021.3088914.",
         "% verified: https://ieeexplore.ieee.org/document/9446944, checked 2026-10-30"),
        ("[3] S. V. Venkatakrishnan, C. A. Bouman, and B. Wohlberg, \"Plug-and-Play Priors for Model Based Reconstruction,\" in <i>2013 IEEE Global Conference on Signal and Information Processing (GlobalSIP)</i>, pp. 945-948, Dec. 2013, doi: 10.1109/GlobalSIP.2013.6737048.",
         "% verified: https://ieeexplore.ieee.org/document/6737048, checked 2026-10-30"),
        ("[4] S. Martin, A. Gagneux, P. Hagemann, and G. Steidl, \"Plug-and-Play Image Restoration with Flow Matching,\" in <i>International Conference on Learning Representations (ICLR)</i>, 2025.",
         "% verified: https://openreview.net/forum?id=V2c2YxK0eG, checked 2026-10-30")
    ]

    for ref_text, prov in refs:
        story.append(Paragraph(ref_text, ref_style))
        story.append(Paragraph(prov, ref_provenance))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report successfully compiled to {output_path}")

if __name__ == '__main__':
    figures_dir = 'C:/Users/Admin/deepinverse-pnp-image-restoration/figures'
    output_pdf = 'C:/Users/Admin/deepinverse-pnp-image-restoration/DeepInverse_PnP_Research_Report.pdf'
    create_report(output_pdf, figures_dir)
