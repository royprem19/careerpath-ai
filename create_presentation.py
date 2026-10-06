"""
CareerPath AI - Professional Hackathon Presentation Generator
Build For Bharat 2.0 | September 25, 2026
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.chart.data import CategoryChartData
import os

# ============================================================================
# DESIGN SYSTEM
# ============================================================================

# Color Palette
PRIMARY_BLUE = RGBColor(0x1E, 0x3A, 0x8A)       # Deep blue
ACCENT_BLUE = RGBColor(0x3B, 0x82, 0xF6)         # Bright blue
ACCENT_PURPLE = RGBColor(0x7C, 0x3A, 0xED)       # Vibrant purple
LIGHT_BLUE = RGBColor(0xDB, 0xEA, 0xFE)          # Light blue bg
LIGHT_PURPLE = RGBColor(0xED, 0xE9, 0xFE)        # Light purple bg
DARK_TEXT = RGBColor(0x1E, 0x29, 0x3B)            # Near black
MEDIUM_TEXT = RGBColor(0x47, 0x55, 0x69)          # Gray text
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xF1, 0xF5, 0xF9)          # Subtle bg
BORDER_GRAY = RGBColor(0xE2, 0xE8, 0xF0)         # Border
SUCCESS_GREEN = RGBColor(0x05, 0x96, 0x69)        # Green accent
ORANGE = RGBColor(0xEA, 0x58, 0x0C)              # Orange accent
RED_ACCENT = RGBColor(0xDC, 0x26, 0x26)           # Red for problems
GRADIENT_START = RGBColor(0x0F, 0x17, 0x2A)       # Dark navy
GRADIENT_MID = RGBColor(0x1E, 0x3A, 0x5F)         # Mid navy

SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

def create_pptx():
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT

    # Use blank layout
    blank_layout = prs.slide_layouts[6]

    # ========================================================================
    # HELPER FUNCTIONS
    # ========================================================================

    def add_background(slide, color=WHITE):
        """Set slide background color."""
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_gradient_bg(slide):
        """Add a dark gradient-like background using shapes."""
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = GRADIENT_START
        # Add a subtle overlay rectangle for depth
        rect = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), SLIDE_WIDTH, SLIDE_HEIGHT
        )
        rect.fill.solid()
        rect.fill.fore_color.rgb = GRADIENT_MID
        rect.fill.fore_color.brightness = -0.1
        rect.line.fill.background()
        # Add decorative circle accents
        for cx, cy, sz, alpha in [
            (Inches(10), Inches(-1), Inches(4), 0.08),
            (Inches(-1), Inches(5), Inches(3), 0.06),
            (Inches(11), Inches(5.5), Inches(2.5), 0.05),
        ]:
            c = slide.shapes.add_shape(MSO_SHAPE.OVAL, cx, cy, sz, sz)
            c.fill.solid()
            c.fill.fore_color.rgb = ACCENT_BLUE
            c.fill.fore_color.brightness = 0.3
            c.line.fill.background()

    def add_top_accent_bar(slide):
        """Add a thin accent bar at the top of a slide."""
        bar = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), SLIDE_WIDTH, Inches(0.08)
        )
        bar.fill.solid()
        bar.fill.fore_color.rgb = ACCENT_BLUE
        bar.line.fill.background()

    def add_bottom_bar(slide, text="CareerPath AI  |  Build For Bharat 2.0  |  September 2026"):
        """Add footer bar."""
        bar = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0), Inches(7.0), SLIDE_WIDTH, Inches(0.5)
        )
        bar.fill.solid()
        bar.fill.fore_color.rgb = LIGHT_GRAY
        bar.line.fill.background()
        tf = bar.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(9)
        p.font.color.rgb = MEDIUM_TEXT
        p.alignment = PP_ALIGN.CENTER

    def add_slide_number(slide, num, total=13):
        """Add slide number."""
        txBox = slide.shapes.add_textbox(
            Inches(12.5), Inches(7.05), Inches(0.7), Inches(0.4)
        )
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = f"{num}/{total}"
        p.font.size = Pt(9)
        p.font.color.rgb = MEDIUM_TEXT
        p.alignment = PP_ALIGN.RIGHT

    def add_section_header(slide, section_num, section_title, left=Inches(0.8), top=Inches(0.4)):
        """Add section number badge and title."""
        # Section number badge
        badge = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(0.45), Inches(0.4)
        )
        badge.fill.solid()
        badge.fill.fore_color.rgb = ACCENT_BLUE
        badge.line.fill.background()
        tf = badge.text_frame
        tf.word_wrap = False
        p = tf.paragraphs[0]
        p.text = f"{section_num:02d}"
        p.font.size = Pt(12)
        p.font.color.rgb = WHITE
        p.font.bold = True
        p.alignment = PP_ALIGN.CENTER
        tf.paragraphs[0].space_before = Pt(2)

        # Section title
        txBox = slide.shapes.add_textbox(
            left + Inches(0.6), top - Inches(0.02), Inches(8), Inches(0.5)
        )
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = section_title
        p.font.size = Pt(28)
        p.font.color.rgb = PRIMARY_BLUE
        p.font.bold = True
        return top + Inches(0.6)

    def add_card(slide, left, top, width, height, title="", body_lines=None,
                 title_color=PRIMARY_BLUE, bg_color=WHITE, border_color=BORDER_GRAY,
                 icon_text="", accent_color=ACCENT_BLUE):
        """Add a styled card with optional icon, title, and bullet points."""
        # Card background
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height
        )
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        card.shadow.inherit = False

        # Accent strip at top of card
        strip = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, left + Inches(0.02), top + Inches(0.02),
            width - Inches(0.04), Inches(0.06)
        )
        strip.fill.solid()
        strip.fill.fore_color.rgb = accent_color
        strip.line.fill.background()

        current_top = top + Inches(0.15)

        # Icon circle
        if icon_text:
            icon_circle = slide.shapes.add_shape(
                MSO_SHAPE.OVAL,
                left + Inches(0.15), current_top,
                Inches(0.45), Inches(0.45)
            )
            icon_circle.fill.solid()
            icon_circle.fill.fore_color.rgb = accent_color
            icon_circle.line.fill.background()
            tf = icon_circle.text_frame
            p = tf.paragraphs[0]
            p.text = icon_text
            p.font.size = Pt(16)
            p.font.color.rgb = WHITE
            p.alignment = PP_ALIGN.CENTER
            current_top += Inches(0.55)

        # Title
        if title:
            txBox = slide.shapes.add_textbox(
                left + Inches(0.15), current_top,
                width - Inches(0.3), Inches(0.4)
            )
            tf = txBox.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = title
            p.font.size = Pt(13)
            p.font.color.rgb = title_color
            p.font.bold = True
            current_top += Inches(0.35)

        # Body lines
        if body_lines:
            txBox = slide.shapes.add_textbox(
                left + Inches(0.15), current_top,
                width - Inches(0.3), height - (current_top - top) - Inches(0.15)
            )
            tf = txBox.text_frame
            tf.word_wrap = True
            for i, line in enumerate(body_lines):
                if i == 0:
                    p = tf.paragraphs[0]
                else:
                    p = tf.add_paragraph()
                p.text = line
                p.font.size = Pt(10)
                p.font.color.rgb = MEDIUM_TEXT
                p.space_after = Pt(3)

    def add_text_block(slide, left, top, width, height, lines,
                       font_size=Pt(14), color=DARK_TEXT, bold=False,
                       alignment=PP_ALIGN.LEFT, line_spacing=1.2, bullet=False):
        """Add a text block with multiple lines."""
        txBox = slide.shapes.add_textbox(left, top, width, height)
        tf = txBox.text_frame
        tf.word_wrap = True
        for i, line in enumerate(lines):
            if i == 0:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()
            p.text = line
            p.font.size = font_size
            p.font.color.rgb = color
            p.font.bold = bold
            p.alignment = alignment
            p.space_after = Pt(4)
            if bullet and not line.startswith("•"):
                p.text = f"• {line}"

    def add_stat_box(slide, left, top, number, label, color=ACCENT_BLUE):
        """Add a statistic highlight box."""
        box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(2.5), Inches(1.2)
        )
        box.fill.solid()
        box.fill.fore_color.rgb = WHITE
        box.line.color.rgb = color
        box.line.width = Pt(2)

        # Number
        txBox = slide.shapes.add_textbox(left + Inches(0.1), top + Inches(0.1),
                                          Inches(2.3), Inches(0.6))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = number
        p.font.size = Pt(28)
        p.font.color.rgb = color
        p.font.bold = True
        p.alignment = PP_ALIGN.CENTER

        # Label
        txBox2 = slide.shapes.add_textbox(left + Inches(0.1), top + Inches(0.65),
                                           Inches(2.3), Inches(0.5))
        tf2 = txBox2.text_frame
        tf2.word_wrap = True
        p2 = tf2.paragraphs[0]
        p2.text = label
        p2.font.size = Pt(10)
        p2.font.color.rgb = MEDIUM_TEXT
        p2.alignment = PP_ALIGN.CENTER

    # ========================================================================
    # SLIDE 1: TITLE SLIDE
    # ========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    add_gradient_bg(slide1)

    # Project name
    txBox = slide1.shapes.add_textbox(Inches(1), Inches(1.2), Inches(11), Inches(1.2))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = "CareerPath AI"
    p.font.size = Pt(52)
    p.font.color.rgb = WHITE
    p.font.bold = True
    p.alignment = PP_ALIGN.LEFT

    # Tagline
    txBox2 = slide1.shapes.add_textbox(Inches(1), Inches(2.3), Inches(9), Inches(0.6))
    tf2 = txBox2.text_frame
    p2 = tf2.paragraphs[0]
    p2.text = "AI-Powered Skill Gap Analysis & Career Intelligence Platform"
    p2.font.size = Pt(22)
    p2.font.color.rgb = RGBColor(0x93, 0xC5, 0xFD)
    p2.alignment = PP_ALIGN.LEFT

    # Divider line
    line = slide1.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(1), Inches(3.1), Inches(3), Inches(0.04)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = ACCENT_BLUE
    line.line.fill.background()

    # Problem statement badge
    badge = slide1.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1), Inches(3.4), Inches(5.5), Inches(0.5)
    )
    badge.fill.solid()
    badge.fill.fore_color.rgb = RGBColor(0x1E, 0x3A, 0x5F)
    badge.line.color.rgb = ACCENT_BLUE
    badge.line.width = Pt(1)
    tf = badge.text_frame
    p = tf.paragraphs[0]
    p.text = "🏆  Problem: Intelligent Talent & Workforce Ecosystem"
    p.font.size = Pt(13)
    p.font.color.rgb = RGBColor(0x93, 0xC5, 0xFD)
    p.alignment = PP_ALIGN.CENTER

    # Hackathon & Date
    txBox3 = slide1.shapes.add_textbox(Inches(1), Inches(4.2), Inches(6), Inches(0.8))
    tf3 = txBox3.text_frame
    p3 = tf3.paragraphs[0]
    p3.text = "Build For Bharat 2.0  ·  September 25, 2026"
    p3.font.size = Pt(16)
    p3.font.color.rgb = RGBColor(0xBF, 0xDB, 0xFE)
    p3.alignment = PP_ALIGN.LEFT

    # Team info card (right side)
    team_card = slide1.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.5), Inches(3.0), Inches(4.2), Inches(3.8)
    )
    team_card.fill.solid()
    team_card.fill.fore_color.rgb = RGBColor(0x1E, 0x2D, 0x4A)
    team_card.line.color.rgb = RGBColor(0x33, 0x4E, 0x78)
    team_card.line.width = Pt(1)

    # Team header
    txBox4 = slide1.shapes.add_textbox(Inches(8.7), Inches(3.15), Inches(3.8), Inches(0.4))
    tf4 = txBox4.text_frame
    p4 = tf4.paragraphs[0]
    p4.text = "TEAM"
    p4.font.size = Pt(11)
    p4.font.color.rgb = ACCENT_BLUE
    p4.font.bold = True
    p4.alignment = PP_ALIGN.LEFT

    team_name_box = slide1.shapes.add_textbox(Inches(8.7), Inches(3.5), Inches(3.8), Inches(0.4))
    tf_tn = team_name_box.text_frame
    p_tn = tf_tn.paragraphs[0]
    p_tn.text = "[Your Team Name]"
    p_tn.font.size = Pt(18)
    p_tn.font.color.rgb = WHITE
    p_tn.font.bold = True

    # Team members
    members = [
        ("[Name 1]", "Full Stack Developer"),
        ("[Name 2]", "ML / NLP Engineer"),
        ("[Name 3]", "UI / UX Designer"),
    ]
    for idx, (name, role) in enumerate(members):
        y = Inches(4.15) + Inches(idx * 0.55)
        # Dot
        dot = slide1.shapes.add_shape(MSO_SHAPE.OVAL, Inches(8.85), y + Inches(0.07), Inches(0.12), Inches(0.12))
        dot.fill.solid()
        dot.fill.fore_color.rgb = ACCENT_BLUE
        dot.line.fill.background()
        # Name
        tb = slide1.shapes.add_textbox(Inches(9.1), y - Inches(0.02), Inches(3.4), Inches(0.28))
        tfm = tb.text_frame
        pm = tfm.paragraphs[0]
        pm.text = name
        pm.font.size = Pt(13)
        pm.font.color.rgb = WHITE
        pm.font.bold = True
        # Role
        tb2 = slide1.shapes.add_textbox(Inches(9.1), y + Inches(0.22), Inches(3.4), Inches(0.22))
        tfr = tb2.text_frame
        pr = tfr.paragraphs[0]
        pr.text = role
        pr.font.size = Pt(10)
        pr.font.color.rgb = RGBColor(0x93, 0xC5, 0xFD)

    # Contact
    txBox5 = slide1.shapes.add_textbox(Inches(8.7), Inches(6.1), Inches(3.8), Inches(0.4))
    tf5 = txBox5.text_frame
    p5 = tf5.paragraphs[0]
    p5.text = "📧  [team.lead@email.com]"
    p5.font.size = Pt(10)
    p5.font.color.rgb = RGBColor(0x93, 0xC5, 0xFD)

    # ========================================================================
    # SLIDE 2: PROBLEM STATEMENT
    # ========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_background(slide2, WHITE)
    add_top_accent_bar(slide2)
    y = add_section_header(slide2, 1, "The Problem")
    add_bottom_bar(slide2)
    add_slide_number(slide2, 2)

    # Stats row
    add_stat_box(slide2, Inches(0.8), Inches(1.3), "1.5M+", "Engineering graduates\nper year in India", RED_ACCENT)
    add_stat_box(slide2, Inches(3.6), Inches(1.3), "60%", "Remain unemployed or\nunderemployed", ORANGE)
    add_stat_box(slide2, Inches(6.4), Inches(1.3), "#1", "Reason: Skill mismatch\nwith industry needs", PRIMARY_BLUE)

    # "Students Don't Know" card
    add_card(slide2, Inches(0.8), Inches(2.85), Inches(3.6), Inches(2.0),
             title="❓ Students Don't Know",
             body_lines=[
                 "Which roles match their current skills",
                 "What critical skills they're missing",
                 "How to close the gap effectively",
                 "Where to start their career journey"
             ],
             accent_color=RED_ACCENT, bg_color=LIGHT_GRAY)

    # "Current Solutions" card
    add_card(slide2, Inches(4.7), Inches(2.85), Inches(3.8), Inches(2.0),
             title="⚠️ Current Solutions Fall Short",
             body_lines=[
                 "Internshala → Job listings, no skill assessment",
                 "LinkedIn → Built for professionals, not students",
                 "Coursera → Courses, but no personalized roadmap",
                 "Naukri → Listings only, no guidance"
             ],
             accent_color=ORANGE, bg_color=LIGHT_GRAY)

    # "Gap" callout
    gap_box = slide2.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(2.85), Inches(3.8), Inches(2.0)
    )
    gap_box.fill.solid()
    gap_box.fill.fore_color.rgb = LIGHT_BLUE
    gap_box.line.color.rgb = ACCENT_BLUE
    gap_box.line.width = Pt(2)

    txBox = slide2.shapes.add_textbox(Inches(9.0), Inches(3.0), Inches(3.4), Inches(0.35))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = "🔍 THE GAP"
    p.font.size = Pt(14)
    p.font.color.rgb = PRIMARY_BLUE
    p.font.bold = True

    txBox2 = slide2.shapes.add_textbox(Inches(9.0), Inches(3.4), Inches(3.4), Inches(1.2))
    tf2 = txBox2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = "No platform tells students:"
    p2.font.size = Pt(11)
    p2.font.color.rgb = MEDIUM_TEXT
    p3 = tf2.add_paragraph()
    p3.text = '"You\'re ready for X role, but need to learn Y and Z first"'
    p3.font.size = Pt(12)
    p3.font.color.rgb = PRIMARY_BLUE
    p3.font.bold = True
    p3.font.italic = True
    p3.space_before = Pt(8)

    # Impact row
    impact_items = [
        ("⏰", "Wasted time applying\nto wrong roles"),
        ("😞", "Lost confidence from\nrepeated rejections"),
        ("🏢", "Employers can't find\nready-to-hire talent"),
    ]
    for i, (icon, text) in enumerate(impact_items):
        x = Inches(0.8) + Inches(i * 3.8)
        box = slide2.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(5.2), Inches(3.4), Inches(1.2)
        )
        box.fill.solid()
        box.fill.fore_color.rgb = WHITE
        box.line.color.rgb = BORDER_GRAY
        box.line.width = Pt(1)

        txIcon = slide2.shapes.add_textbox(x + Inches(0.15), Inches(5.3), Inches(0.4), Inches(0.4))
        tfI = txIcon.text_frame
        pI = tfI.paragraphs[0]
        pI.text = icon
        pI.font.size = Pt(22)

        txT = slide2.shapes.add_textbox(x + Inches(0.6), Inches(5.35), Inches(2.6), Inches(0.9))
        tfT = txT.text_frame
        tfT.word_wrap = True
        pT = tfT.paragraphs[0]
        pT.text = text
        pT.font.size = Pt(12)
        pT.font.color.rgb = DARK_TEXT

    # ========================================================================
    # SLIDE 3: OUR SOLUTION
    # ========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_background(slide3, WHITE)
    add_top_accent_bar(slide3)
    add_section_header(slide3, 2, "Our Solution")
    add_bottom_bar(slide3)
    add_slide_number(slide3, 3)

    # Pitch callout
    pitch = slide3.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.2), Inches(11.7), Inches(0.8)
    )
    pitch.fill.solid()
    pitch.fill.fore_color.rgb = LIGHT_BLUE
    pitch.line.color.rgb = ACCENT_BLUE
    pitch.line.width = Pt(1.5)
    txPitch = slide3.shapes.add_textbox(Inches(1.0), Inches(1.3), Inches(11.3), Inches(0.6))
    tfP = txPitch.text_frame
    tfP.word_wrap = True
    pP = tfP.paragraphs[0]
    pP.text = '💡  "Upload your resume, get a skill gap analysis, and receive a week-by-week learning roadmap to become job-ready in your best-fit role."'
    pP.font.size = Pt(15)
    pP.font.color.rgb = PRIMARY_BLUE
    pP.font.bold = True
    pP.alignment = PP_ALIGN.CENTER

    # 5-step flow
    steps = [
        ("📄", "Upload", "Resume or\nenter skills"),
        ("🤖", "Extract", "AI identifies\nyour skills"),
        ("📊", "Compare", "Match against\n7 roles"),
        ("🗺️", "Roadmap", "4-week plan\nwith courses"),
        ("📥", "Export", "Download\nPDF report"),
    ]
    for i, (icon, title, desc) in enumerate(steps):
        x = Inches(0.8) + Inches(i * 2.45)
        # Step card
        card = slide3.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(2.35), Inches(2.1), Inches(2.0)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = LIGHT_GRAY
        card.line.color.rgb = BORDER_GRAY
        card.line.width = Pt(1)

        # Step number
        num_badge = slide3.shapes.add_shape(
            MSO_SHAPE.OVAL, x + Inches(0.75), Inches(2.5), Inches(0.55), Inches(0.55)
        )
        num_badge.fill.solid()
        num_badge.fill.fore_color.rgb = ACCENT_BLUE
        num_badge.line.fill.background()
        tf = num_badge.text_frame
        p = tf.paragraphs[0]
        p.text = str(i + 1)
        p.font.size = Pt(16)
        p.font.color.rgb = WHITE
        p.font.bold = True
        p.alignment = PP_ALIGN.CENTER

        # Icon
        txI = slide3.shapes.add_textbox(x + Inches(0.65), Inches(3.15), Inches(0.8), Inches(0.4))
        tfI = txI.text_frame
        pI = tfI.paragraphs[0]
        pI.text = icon
        pI.font.size = Pt(22)
        pI.alignment = PP_ALIGN.CENTER

        # Title
        txT = slide3.shapes.add_textbox(x + Inches(0.1), Inches(3.55), Inches(1.9), Inches(0.3))
        tfT = txT.text_frame
        pT = tfT.paragraphs[0]
        pT.text = title
        pT.font.size = Pt(14)
        pT.font.color.rgb = PRIMARY_BLUE
        pT.font.bold = True
        pT.alignment = PP_ALIGN.CENTER

        # Description
        txD = slide3.shapes.add_textbox(x + Inches(0.1), Inches(3.85), Inches(1.9), Inches(0.5))
        tfD = txD.text_frame
        tfD.word_wrap = True
        pD = tfD.paragraphs[0]
        pD.text = desc
        pD.font.size = Pt(10)
        pD.font.color.rgb = MEDIUM_TEXT
        pD.alignment = PP_ALIGN.CENTER

        # Arrow between steps
        if i < 4:
            arrow = slide3.shapes.add_shape(
                MSO_SHAPE.RIGHT_ARROW, x + Inches(2.1), Inches(3.15),
                Inches(0.35), Inches(0.25)
            )
            arrow.fill.solid()
            arrow.fill.fore_color.rgb = ACCENT_BLUE
            arrow.line.fill.background()

    # Differentiators
    diff_items = [
        ("🎯", "Skill Readiness First", "Not just job listings — we assess your readiness"),
        ("🔍", "Explainable AI", "Full breakdown of why roles are recommended"),
        ("🔒", "Privacy-First", "Session-only processing, DPDP Act 2023 compliant"),
    ]
    for i, (icon, title, desc) in enumerate(diff_items):
        x = Inches(0.8) + Inches(i * 4.1)
        box = slide3.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(4.8), Inches(3.8), Inches(1.5)
        )
        box.fill.solid()
        box.fill.fore_color.rgb = WHITE
        box.line.color.rgb = ACCENT_BLUE
        box.line.width = Pt(1.5)

        txI = slide3.shapes.add_textbox(x + Inches(0.15), Inches(4.9), Inches(0.4), Inches(0.4))
        tfI = txI.text_frame
        pI = tfI.paragraphs[0]
        pI.text = icon
        pI.font.size = Pt(22)

        txT = slide3.shapes.add_textbox(x + Inches(0.55), Inches(4.92), Inches(3.0), Inches(0.3))
        tfT = txT.text_frame
        pT = tfT.paragraphs[0]
        pT.text = title
        pT.font.size = Pt(14)
        pT.font.color.rgb = PRIMARY_BLUE
        pT.font.bold = True

        txD = slide3.shapes.add_textbox(x + Inches(0.15), Inches(5.4), Inches(3.5), Inches(0.7))
        tfD = txD.text_frame
        tfD.word_wrap = True
        pD = tfD.paragraphs[0]
        pD.text = desc
        pD.font.size = Pt(11)
        pD.font.color.rgb = MEDIUM_TEXT

    # ========================================================================
    # SLIDE 4: TARGET USERS & MARKET
    # ========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_background(slide4, WHITE)
    add_top_accent_bar(slide4)
    add_section_header(slide4, 3, "Target Users & Market Opportunity")
    add_bottom_bar(slide4)
    add_slide_number(slide4, 4)

    # Primary Users cards
    users = [
        ("🎓", "Final-Year Students", "B.Tech / B.E. (21-23 yrs)\nPlacement pressure, need guidance"),
        ("🚀", "Fresh Graduates", "0-1 years experience\nSkill-to-role confusion"),
        ("🔄", "Career Switchers", "1-3 years, wanting to pivot\nNeed structured upskilling path"),
    ]
    for i, (icon, title, desc) in enumerate(users):
        x = Inches(0.8) + Inches(i * 4.0)
        add_card(slide4, x, Inches(1.3), Inches(3.6), Inches(1.7),
                 title=title, body_lines=desc.split("\n"),
                 icon_text=icon,
                 accent_color=[ACCENT_BLUE, ACCENT_PURPLE, SUCCESS_GREEN][i])

    # Market size funnel
    funnel_data = [
        ("TAM", "1.5M", "Engineering graduates / year", Inches(7.5), ACCENT_BLUE),
        ("SAM", "600K", "Actively job-seeking students", Inches(5.5), ACCENT_PURPLE),
        ("SOM", "50K", "Year 1 target (college partners)", Inches(3.5), SUCCESS_GREEN),
    ]
    for label, num, desc, width, color in funnel_data:
        x_start = Inches(0.8) + (Inches(7.5) - width) / 2
        y_offset = Inches(3.5) + Inches(funnel_data.index((label, num, desc, width, color)) * 0.85)

        bar = slide4.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, x_start, y_offset, width, Inches(0.65)
        )
        bar.fill.solid()
        bar.fill.fore_color.rgb = color
        bar.line.fill.background()

        tf = bar.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"{label}:  {num}  —  {desc}"
        p.font.size = Pt(13)
        p.font.color.rgb = WHITE
        p.font.bold = True
        p.alignment = PP_ALIGN.CENTER

    # Why This Market
    why_box = slide4.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(3.5), Inches(4.0), Inches(3.0)
    )
    why_box.fill.solid()
    why_box.fill.fore_color.rgb = LIGHT_PURPLE
    why_box.line.color.rgb = ACCENT_PURPLE
    why_box.line.width = Pt(1.5)

    txBox = slide4.shapes.add_textbox(Inches(9.0), Inches(3.6), Inches(3.6), Inches(0.35))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = "Why This Market?"
    p.font.size = Pt(16)
    p.font.color.rgb = ACCENT_PURPLE
    p.font.bold = True

    why_items = [
        "🔥  High pain intensity (placement pressure)",
        "📱  Digital-native, willing to try new tools",
        "🔗  Viral potential (peer recommendations)",
        "🏫  College partnerships = instant scale",
    ]
    txBox2 = slide4.shapes.add_textbox(Inches(9.0), Inches(4.1), Inches(3.6), Inches(2.2))
    tf2 = txBox2.text_frame
    tf2.word_wrap = True
    for i, item in enumerate(why_items):
        if i == 0:
            p = tf2.paragraphs[0]
        else:
            p = tf2.add_paragraph()
        p.text = item
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(8)

    # ========================================================================
    # SLIDE 5: SOLUTION ARCHITECTURE
    # ========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_background(slide5, WHITE)
    add_top_accent_bar(slide5)
    add_section_header(slide5, 4, "Solution Architecture")
    add_bottom_bar(slide5)
    add_slide_number(slide5, 5)

    # Architecture layers
    layers = [
        ("Frontend", ACCENT_BLUE, [
            "React.js + Vite",
            "TailwindCSS",
            "Recharts",
        ]),
        ("Backend API", ACCENT_PURPLE, [
            "FastAPI (Python)",
            "In-memory sessions",
            "JSON knowledge base",
        ]),
        ("AI / ML Engine", SUCCESS_GREEN, [
            "Keyword skill extraction",
            "Fit score (70/30 weighting)",
            "Explainable recommendations",
        ]),
        ("Data Layer", ORANGE, [
            "Role-skill catalog (7 roles, 80+ skills)",
            "Validated vs 23K Naukri postings",
            "ESCO-aligned · Free course DB",
        ]),
    ]

    for i, (name, color, items) in enumerate(layers):
        y = Inches(1.2) + Inches(i * 1.35)
        # Layer bar
        bar = slide5.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(2.2), Inches(1.1)
        )
        bar.fill.solid()
        bar.fill.fore_color.rgb = color
        bar.line.fill.background()
        tf = bar.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = name
        p.font.size = Pt(16)
        p.font.color.rgb = WHITE
        p.font.bold = True
        p.alignment = PP_ALIGN.CENTER
        tf.paragraphs[0].space_before = Pt(14)

        # Details
        detail_box = slide5.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.2), y, Inches(5.5), Inches(1.1)
        )
        detail_box.fill.solid()
        detail_box.fill.fore_color.rgb = LIGHT_GRAY
        detail_box.line.color.rgb = BORDER_GRAY
        detail_box.line.width = Pt(1)

        txBox = slide5.shapes.add_textbox(Inches(3.4), y + Inches(0.08), Inches(5.1), Inches(0.9))
        tf2 = txBox.text_frame
        tf2.word_wrap = True
        for j, item in enumerate(items):
            if j == 0:
                p2 = tf2.paragraphs[0]
            else:
                p2 = tf2.add_paragraph()
            p2.text = f"▸  {item}"
            p2.font.size = Pt(12)
            p2.font.color.rgb = DARK_TEXT
            p2.space_after = Pt(2)

        # Connector arrows between layers
        if i < 3:
            arrow = slide5.shapes.add_shape(
                MSO_SHAPE.DOWN_ARROW, Inches(1.7), y + Inches(1.1),
                Inches(0.3), Inches(0.25)
            )
            arrow.fill.solid()
            arrow.fill.fore_color.rgb = MEDIUM_TEXT
            arrow.line.fill.background()

    # Deployment box
    deploy_box = slide5.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.2), Inches(1.2), Inches(3.6), Inches(5.4)
    )
    deploy_box.fill.solid()
    deploy_box.fill.fore_color.rgb = LIGHT_BLUE
    deploy_box.line.color.rgb = ACCENT_BLUE
    deploy_box.line.width = Pt(1.5)

    txBox = slide5.shapes.add_textbox(Inches(9.4), Inches(1.35), Inches(3.2), Inches(0.4))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = "🚀 Deployment"
    p.font.size = Pt(16)
    p.font.color.rgb = PRIMARY_BLUE
    p.font.bold = True

    deploy_items = [
        ("Frontend", "Vercel / Netlify"),
        ("Backend", "Render / Railway"),
        ("Database", "In-memory (demo)"),
        ("APIs", "Self-contained"),
        ("", ""),
        ("✅ Key Properties", ""),
        ("", "No external API deps"),
        ("", "Fully offline capable"),
        ("", "< 5s response time"),
        ("", "100 concurrent users"),
    ]
    txBox2 = slide5.shapes.add_textbox(Inches(9.4), Inches(1.85), Inches(3.2), Inches(4.5))
    tf2 = txBox2.text_frame
    tf2.word_wrap = True
    for i, (key, val) in enumerate(deploy_items):
        if i == 0:
            p2 = tf2.paragraphs[0]
        else:
            p2 = tf2.add_paragraph()
        if key and val:
            p2.text = f"{key}:  {val}"
        elif key:
            p2.text = key
            p2.font.bold = True
            p2.space_before = Pt(8)
        elif val:
            p2.text = f"  ▸ {val}"
        else:
            p2.text = ""
        p2.font.size = Pt(11)
        p2.font.color.rgb = DARK_TEXT if key else MEDIUM_TEXT
        p2.space_after = Pt(3)

    # ========================================================================
    # SLIDE 6: KEY FEATURES
    # ========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_background(slide6, WHITE)
    add_top_accent_bar(slide6)
    add_section_header(slide6, 5, "Key Features")
    add_bottom_bar(slide6)
    add_slide_number(slide6, 6)

    features = [
        ("📄", "Resume Parsing &\nSkill Extraction", [
            "Upload PDF / DOCX",
            "Keyword-based extraction",
            "Manual edit fallback"
        ], ACCENT_BLUE),
        ("📊", "Role Comparison &\nFit Scoring", [
            "Compare against 7 roles",
            "Fit score with breakdown",
            "Explainable reasoning"
        ], ACCENT_PURPLE),
        ("🗺️", "Learning Roadmap\nGenerator", [
            "Week-by-week plan",
            "Free curated courses",
            "10-15 hrs/week estimate"
        ], SUCCESS_GREEN),
        ("🔒", "Privacy-First\nDesign", [
            "Session-only processing",
            "DPDP Act 2023 compliant",
            "One-click data delete"
        ], RGBColor(0xDC, 0x26, 0x26)),
        ("📥", "Printable Reports", [
            "PDF / HTML export",
            "Shareable with mentors",
            "Professional formatting"
        ], ORANGE),
        ("💼", "Mock Job\nListings", [
            "Realistic demo data",
            "Naukri-style cards",
            "API integration planned"
        ], RGBColor(0x06, 0x4E, 0x3B)),
    ]

    for i, (icon, title, items, color) in enumerate(features):
        col = i % 3
        row = i // 3
        x = Inches(0.8) + Inches(col * 4.1)
        y = Inches(1.15) + Inches(row * 2.85)

        add_card(slide6, x, y, Inches(3.7), Inches(2.5),
                 title=title, body_lines=items,
                 icon_text=icon, accent_color=color)

    # ========================================================================
    # SLIDE 7: AI/ML APPROACH (REPLACES DEMO SCREENSHOTS)
    # ========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_background(slide7, WHITE)
    add_top_accent_bar(slide7)
    add_section_header(slide7, 6, "AI / ML Approach & Algorithms")
    add_bottom_bar(slide7)
    add_slide_number(slide7, 7)

    # Skill Extraction
    add_card(slide7, Inches(0.8), Inches(1.2), Inches(5.8), Inches(2.3),
             title="🤖 Skill Extraction Pipeline",
             body_lines=[
                 "1. Resume text extraction (PyPDF2 / pdfplumber)",
                 "2. Keyword matching against 80+ skill dictionary",
                 "3. Normalize to canonical skill IDs",
                 "4. Confidence scoring + user edit capability",
                 "5. Fallback: Manual skill entry or quiz"
             ],
             accent_color=ACCENT_BLUE)

    # Fit Score Formula
    formula_box = slide7.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.0), Inches(1.2), Inches(5.8), Inches(2.3)
    )
    formula_box.fill.solid()
    formula_box.fill.fore_color.rgb = LIGHT_PURPLE
    formula_box.line.color.rgb = ACCENT_PURPLE
    formula_box.line.width = Pt(1.5)

    txBox = slide7.shapes.add_textbox(Inches(7.2), Inches(1.35), Inches(5.4), Inches(0.35))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = "📐 Fit Score Calculation"
    p.font.size = Pt(15)
    p.font.color.rgb = ACCENT_PURPLE
    p.font.bold = True

    formula_lines = [
        "Essential Coverage = |User Skills ∩ Essential| / |Essential|",
        "Optional Coverage = |User Skills ∩ Optional| / |Optional|",
        "",
        "FitScore = 0.7 × EssentialCoverage + 0.3 × OptionalCoverage",
        "",
        "Gap = Essential \\ User Skills  (prioritized missing list)",
    ]
    txBox2 = slide7.shapes.add_textbox(Inches(7.2), Inches(1.8), Inches(5.4), Inches(1.5))
    tf2 = txBox2.text_frame
    tf2.word_wrap = True
    for i, line in enumerate(formula_lines):
        if i == 0:
            p2 = tf2.paragraphs[0]
        else:
            p2 = tf2.add_paragraph()
        p2.text = line
        p2.font.size = Pt(11)
        p2.font.color.rgb = DARK_TEXT
        if "FitScore" in line:
            p2.font.bold = True
            p2.font.color.rgb = ACCENT_PURPLE
        p2.space_after = Pt(2)

    # Recommendation engine
    add_card(slide7, Inches(0.8), Inches(3.85), Inches(5.8), Inches(2.5),
             title="🎯 Career Recommendation Engine",
             body_lines=[
                 "Hybrid Approach:",
                 "▸ Content-based: Semantic similarity (user ↔ role)",
                 "▸ Rule-based: Boost by education & experience",
                 "▸ RoleScore = α×Similarity + β×FitScore + γ×Boost",
                 "▸ Rank top 5 roles with full explanations",
                 "▸ Show: matched skills, missing skills, why recommended"
             ],
             accent_color=SUCCESS_GREEN)

    # Roadmap generation
    add_card(slide7, Inches(7.0), Inches(3.85), Inches(5.8), Inches(2.5),
             title="🗺️ Roadmap Generation Logic",
             body_lines=[
                 "For each missing skill:",
                 "▸ Query curated course database (skill → course)",
                 "▸ Prioritize free, short-duration resources",
                 "▸ Include project-based learning milestones",
                 "▸ Output: Week 1 → Skill A, Week 2 → Skill B...",
                 "▸ Sources: Coursera, Udemy, YouTube, NPTEL"
             ],
             accent_color=ORANGE)

    # ========================================================================
    # SLIDE 8: SYSTEM WORKFLOW (DETAILED FLOW)
    # ========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    add_background(slide8, WHITE)
    add_top_accent_bar(slide8)
    add_section_header(slide8, 7, "System Workflow")
    add_bottom_bar(slide8)
    add_slide_number(slide8, 8)

    # Flow diagram
    flow_steps = [
        ("User", "📤 Upload Resume\nor Enter Skills", ACCENT_BLUE),
        ("Parser", "📝 Text Extraction\n(PDF/DOCX)", ACCENT_PURPLE),
        ("NLP", "🔍 Skill Extraction\n& Normalization", SUCCESS_GREEN),
        ("Engine", "⚙️ Gap Analysis\n& Fit Scoring", ORANGE),
        ("AI", "🎯 Career\nRecommendations", RGBColor(0xDC, 0x26, 0x26)),
        ("Output", "🗺️ Learning\nRoadmap + Report", PRIMARY_BLUE),
    ]

    for i, (label, desc, color) in enumerate(flow_steps):
        x = Inches(0.5) + Inches(i * 2.1)
        y = Inches(1.3)

        # Box
        box = slide8.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(1.8), Inches(1.6)
        )
        box.fill.solid()
        box.fill.fore_color.rgb = color
        box.line.fill.background()

        # Label
        txL = slide8.shapes.add_textbox(x, y + Inches(0.1), Inches(1.8), Inches(0.25))
        tfL = txL.text_frame
        pL = tfL.paragraphs[0]
        pL.text = label.upper()
        pL.font.size = Pt(9)
        pL.font.color.rgb = WHITE
        pL.font.bold = True
        pL.alignment = PP_ALIGN.CENTER

        # Description
        txD = slide8.shapes.add_textbox(x + Inches(0.05), y + Inches(0.4), Inches(1.7), Inches(1.1))
        tfD = txD.text_frame
        tfD.word_wrap = True
        pD = tfD.paragraphs[0]
        pD.text = desc
        pD.font.size = Pt(11)
        pD.font.color.rgb = WHITE
        pD.alignment = PP_ALIGN.CENTER

        # Arrow
        if i < 5:
            arrow = slide8.shapes.add_shape(
                MSO_SHAPE.RIGHT_ARROW, x + Inches(1.8), y + Inches(0.6),
                Inches(0.3), Inches(0.2)
            )
            arrow.fill.solid()
            arrow.fill.fore_color.rgb = MEDIUM_TEXT
            arrow.line.fill.background()

    # Detailed data flow below
    txBox = slide8.shapes.add_textbox(Inches(0.8), Inches(3.2), Inches(11.5), Inches(0.35))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = "Detailed API Flow"
    p.font.size = Pt(16)
    p.font.color.rgb = PRIMARY_BLUE
    p.font.bold = True

    api_endpoints = [
        ("POST", "/api/resume/upload", "Upload & parse resume file"),
        ("GET", "/api/resume/parse", "Return extracted skills & profile"),
        ("GET", "/api/roles", "List available target roles"),
        ("POST", "/api/analysis/gap", "Compute skill gap for user + role"),
        ("POST", "/api/recommendations", "Get top recommended roles"),
        ("POST", "/api/roadmap", "Generate learning roadmap"),
        ("GET", "/api/report/:userId", "Download PDF/CSV report"),
    ]

    # Table header
    header_bar = slide8.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.65), Inches(11.5), Inches(0.4)
    )
    header_bar.fill.solid()
    header_bar.fill.fore_color.rgb = PRIMARY_BLUE
    header_bar.line.fill.background()

    cols = [
        (Inches(0.9), Inches(1.0), "Method"),
        (Inches(2.0), Inches(3.5), "Endpoint"),
        (Inches(5.6), Inches(6.5), "Description"),
    ]
    for x, w, text in cols:
        txBox = slide8.shapes.add_textbox(x, Inches(3.7), w, Inches(0.3))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(11)
        p.font.color.rgb = WHITE
        p.font.bold = True

    for i, (method, endpoint, desc) in enumerate(api_endpoints):
        y = Inches(4.1) + Inches(i * 0.38)
        bg_color = LIGHT_GRAY if i % 2 == 0 else WHITE
        row_bg = slide8.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0.8), y, Inches(11.5), Inches(0.38)
        )
        row_bg.fill.solid()
        row_bg.fill.fore_color.rgb = bg_color
        row_bg.line.fill.background()

        # Method badge
        method_badge = slide8.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), y + Inches(0.04),
            Inches(0.8), Inches(0.28)
        )
        method_color = SUCCESS_GREEN if method == "GET" else ACCENT_BLUE
        method_badge.fill.solid()
        method_badge.fill.fore_color.rgb = method_color
        method_badge.line.fill.background()
        tf = method_badge.text_frame
        p = tf.paragraphs[0]
        p.text = method
        p.font.size = Pt(9)
        p.font.color.rgb = WHITE
        p.font.bold = True
        p.alignment = PP_ALIGN.CENTER

        # Endpoint
        txE = slide8.shapes.add_textbox(Inches(2.0), y + Inches(0.02), Inches(3.5), Inches(0.3))
        tfE = txE.text_frame
        pE = tfE.paragraphs[0]
        pE.text = endpoint
        pE.font.size = Pt(11)
        pE.font.color.rgb = DARK_TEXT
        pE.font.bold = True

        # Description
        txDe = slide8.shapes.add_textbox(Inches(5.6), y + Inches(0.02), Inches(6.5), Inches(0.3))
        tfDe = txDe.text_frame
        pDe = tfDe.paragraphs[0]
        pDe.text = desc
        pDe.font.size = Pt(11)
        pDe.font.color.rgb = MEDIUM_TEXT

    # ========================================================================
    # SLIDE 9: INNOVATION & COMPARISON
    # ========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    add_background(slide9, WHITE)
    add_top_accent_bar(slide9)
    add_section_header(slide9, 8, "Innovation & Competitive Edge")
    add_bottom_bar(slide9)
    add_slide_number(slide9, 9)

    # Comparison table
    headers = ["Feature", "CareerPath AI", "Internshala", "LinkedIn", "Coursera"]
    header_colors = [PRIMARY_BLUE, ACCENT_BLUE, ORANGE, RGBColor(0x0A, 0x66, 0xC2), RGBColor(0x00, 0x56, 0xD2)]

    rows_data = [
        ["Skill Gap Analysis", "✅ Core Feature", "❌ No", "❌ No", "❌ No"],
        ["Explainable AI", "✅ Full Breakdown", "❌ Black Box", "❌ Black Box", "❌ N/A"],
        ["DPDP Compliant", "✅ Session-Only", "❌ Stores All", "❌ Stores All", "❌ Stores All"],
        ["India-Localized", "✅ Built for India", "✅ India", "❌ Global", "❌ Global"],
        ["Free for Students", "✅ Core Free", "❌ Paid", "❌ Premium", "❌ Paid"],
        ["Learning Roadmap", "✅ Week-by-Week", "❌ Course List", "❌ No", "❌ Course List"],
        ["Career Readiness", "✅ Score + Path", "❌ No", "❌ No", "❌ No"],
    ]

    col_widths = [Inches(2.5), Inches(2.4), Inches(2.0), Inches(2.0), Inches(2.0)]
    table_x = Inches(0.8)

    # Header row
    x_pos = table_x
    for i, (header, color) in enumerate(zip(headers, header_colors)):
        hdr_box = slide9.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE if i == 0 else MSO_SHAPE.RECTANGLE,
            x_pos, Inches(1.2), col_widths[i], Inches(0.5)
        )
        hdr_box.fill.solid()
        hdr_box.fill.fore_color.rgb = color
        hdr_box.line.fill.background()
        tf = hdr_box.text_frame
        p = tf.paragraphs[0]
        p.text = header
        p.font.size = Pt(12)
        p.font.color.rgb = WHITE
        p.font.bold = True
        p.alignment = PP_ALIGN.CENTER
        x_pos += col_widths[i] + Inches(0.05)

    # Data rows
    for row_idx, row in enumerate(rows_data):
        y = Inches(1.8) + Inches(row_idx * 0.48)
        x_pos = table_x
        for col_idx, cell in enumerate(row):
            bg = LIGHT_GRAY if row_idx % 2 == 0 else WHITE
            if col_idx == 1 and "✅" in cell:
                bg = RGBColor(0xEC, 0xFD, 0xF5)  # Light green for our features

            cell_box = slide9.shapes.add_shape(
                MSO_SHAPE.RECTANGLE, x_pos, y, col_widths[col_idx], Inches(0.44)
            )
            cell_box.fill.solid()
            cell_box.fill.fore_color.rgb = bg
            cell_box.line.color.rgb = BORDER_GRAY
            cell_box.line.width = Pt(0.5)

            tf = cell_box.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = cell
            p.font.size = Pt(10)
            p.font.color.rgb = DARK_TEXT
            if col_idx == 0:
                p.font.bold = True
            p.alignment = PP_ALIGN.CENTER
            x_pos += col_widths[col_idx] + Inches(0.05)

    # UVP callout
    uvp_box = slide9.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.5), Inches(5.6), Inches(8.3), Inches(0.9)
    )
    uvp_box.fill.solid()
    uvp_box.fill.fore_color.rgb = LIGHT_BLUE
    uvp_box.line.color.rgb = ACCENT_BLUE
    uvp_box.line.width = Pt(2)

    txBox = slide9.shapes.add_textbox(Inches(2.7), Inches(5.65), Inches(7.9), Inches(0.8))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = '🏆 Unique Value Proposition'
    p.font.size = Pt(12)
    p.font.color.rgb = ACCENT_BLUE
    p.font.bold = True
    p.alignment = PP_ALIGN.CENTER
    p2 = tf.add_paragraph()
    p2.text = '"We don\'t just list jobs. We make you job-ready first."'
    p2.font.size = Pt(18)
    p2.font.color.rgb = PRIMARY_BLUE
    p2.font.bold = True
    p2.font.italic = True
    p2.alignment = PP_ALIGN.CENTER

    # ========================================================================
    # SLIDE 10: IMPACT & METRICS
    # ========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    add_background(slide10, WHITE)
    add_top_accent_bar(slide10)
    add_section_header(slide10, 9, "Impact & Projected Metrics")
    add_bottom_bar(slide10)
    add_slide_number(slide10, 10)

    # Year 1 metrics
    metrics = [
        ("50,000", "Students Served", ACCENT_BLUE),
        ("60%", "Report Increased\nCareer Confidence", SUCCESS_GREEN),
        ("40%", "Complete Learning\nRoadmap", ACCENT_PURPLE),
        ("25%", "Improved Interview\nConversion", ORANGE),
    ]

    for i, (num, label, color) in enumerate(metrics):
        x = Inches(0.8) + Inches(i * 3.1)
        box = slide10.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.2), Inches(2.8), Inches(1.6)
        )
        box.fill.solid()
        box.fill.fore_color.rgb = WHITE
        box.line.color.rgb = color
        box.line.width = Pt(2.5)

        # Number
        txN = slide10.shapes.add_textbox(x + Inches(0.1), Inches(1.35), Inches(2.6), Inches(0.6))
        tfN = txN.text_frame
        pN = tfN.paragraphs[0]
        pN.text = num
        pN.font.size = Pt(32)
        pN.font.color.rgb = color
        pN.font.bold = True
        pN.alignment = PP_ALIGN.CENTER

        # Label
        txL = slide10.shapes.add_textbox(x + Inches(0.1), Inches(1.95), Inches(2.6), Inches(0.7))
        tfL = txL.text_frame
        tfL.word_wrap = True
        pL = tfL.paragraphs[0]
        pL.text = label
        pL.font.size = Pt(11)
        pL.font.color.rgb = MEDIUM_TEXT
        pL.alignment = PP_ALIGN.CENTER

    # Social Impact
    social_items = [
        ("🎯", "Democratizes career guidance — free for all students"),
        ("⚖️", "Reduces skill mismatch in Indian job market"),
        ("🏫", "Helps Tier-2/3 college students compete with Tier-1"),
        ("📈", "Aligns education outcomes with industry demand"),
    ]
    social_box = slide10.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.1), Inches(6.0), Inches(2.8)
    )
    social_box.fill.solid()
    social_box.fill.fore_color.rgb = LIGHT_GRAY
    social_box.line.color.rgb = BORDER_GRAY
    social_box.line.width = Pt(1)

    txH = slide10.shapes.add_textbox(Inches(1.0), Inches(3.2), Inches(5.6), Inches(0.35))
    tfH = txH.text_frame
    pH = tfH.paragraphs[0]
    pH.text = "🌍 Social Impact"
    pH.font.size = Pt(16)
    pH.font.color.rgb = PRIMARY_BLUE
    pH.font.bold = True

    txS = slide10.shapes.add_textbox(Inches(1.0), Inches(3.65), Inches(5.6), Inches(2.0))
    tfS = txS.text_frame
    tfS.word_wrap = True
    for i, (icon, text) in enumerate(social_items):
        if i == 0:
            p = tfS.paragraphs[0]
        else:
            p = tfS.add_paragraph()
        p.text = f"{icon}  {text}"
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(6)

    # Scalability
    scale_items = [
        "Add 100+ roles (currently 7)",
        "Integrate real job APIs (Naukri, LinkedIn)",
        "Partner with 100+ colleges",
        "Expand to regional languages",
        "Mobile app for wider reach",
    ]
    scale_box = slide10.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.2), Inches(3.1), Inches(5.6), Inches(2.8)
    )
    scale_box.fill.solid()
    scale_box.fill.fore_color.rgb = LIGHT_BLUE
    scale_box.line.color.rgb = ACCENT_BLUE
    scale_box.line.width = Pt(1)

    txH2 = slide10.shapes.add_textbox(Inches(7.4), Inches(3.2), Inches(5.2), Inches(0.35))
    tfH2 = txH2.text_frame
    pH2 = tfH2.paragraphs[0]
    pH2.text = "📈 Scalability Roadmap"
    pH2.font.size = Pt(16)
    pH2.font.color.rgb = PRIMARY_BLUE
    pH2.font.bold = True

    txSc = slide10.shapes.add_textbox(Inches(7.4), Inches(3.65), Inches(5.2), Inches(2.0))
    tfSc = txSc.text_frame
    tfSc.word_wrap = True
    for i, item in enumerate(scale_items):
        if i == 0:
            p = tfSc.paragraphs[0]
        else:
            p = tfSc.add_paragraph()
        p.text = f"▸  {item}"
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(6)

    # Chart - bar chart for impact projections
    chart_data = CategoryChartData()
    chart_data.categories = ['Month 1', 'Month 3', 'Month 6', 'Month 9', 'Month 12']
    chart_data.add_series('Users (K)', (2, 8, 18, 32, 50))

    chart = slide10.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED,
        Inches(0.8), Inches(6.05), Inches(5.5), Inches(0.85),
        chart_data
    ).chart

    chart.has_legend = False
    chart.style = 2
    plot = chart.plots[0]
    series = plot.series[0]
    series.format.fill.solid()
    series.format.fill.fore_color.rgb = ACCENT_BLUE

    # ========================================================================
    # SLIDE 11: CHALLENGES & LEARNINGS
    # ========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    add_background(slide11, WHITE)
    add_top_accent_bar(slide11)
    add_section_header(slide11, 10, "Challenges & Key Learnings")
    add_bottom_bar(slide11)
    add_slide_number(slide11, 11)

    # Technical Challenges
    challenges = [
        ("⚠️", "Resume Parsing Edge Cases",
         "Scanned PDFs, complex layouts, non-standard formats",
         "Manual entry fallback + clear error messages + format validation"),
        ("🎯", "Skill Extraction Accuracy",
         "Keyword matching misses context and synonyms",
         "Confidence scoring + user edit capability + synonym dictionary"),
        ("⏰", "Hackathon Time Constraints",
         "48 hours for full-stack development",
         "Prioritized core journey, mocked non-essential features"),
    ]

    for i, (icon, title, problem, solution) in enumerate(challenges):
        y = Inches(1.2) + Inches(i * 1.7)
        # Challenge card
        card = slide11.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(7.0), Inches(1.45)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = BORDER_GRAY
        card.line.width = Pt(1)

        # Icon + Title
        txT = slide11.shapes.add_textbox(Inches(1.0), y + Inches(0.08), Inches(6.6), Inches(0.3))
        tfT = txT.text_frame
        pT = tfT.paragraphs[0]
        pT.text = f"{icon}  {title}"
        pT.font.size = Pt(14)
        pT.font.color.rgb = PRIMARY_BLUE
        pT.font.bold = True

        # Problem
        txP = slide11.shapes.add_textbox(Inches(1.0), y + Inches(0.45), Inches(3.2), Inches(0.8))
        tfP = txP.text_frame
        tfP.word_wrap = True
        pH = tfP.paragraphs[0]
        pH.text = "Problem:"
        pH.font.size = Pt(10)
        pH.font.color.rgb = RED_ACCENT
        pH.font.bold = True
        pB = tfP.add_paragraph()
        pB.text = problem
        pB.font.size = Pt(10)
        pB.font.color.rgb = MEDIUM_TEXT

        # Solution
        txS = slide11.shapes.add_textbox(Inches(4.4), y + Inches(0.45), Inches(3.2), Inches(0.8))
        tfS2 = txS.text_frame
        tfS2.word_wrap = True
        pSH = tfS2.paragraphs[0]
        pSH.text = "Solution:"
        pSH.font.size = Pt(10)
        pSH.font.color.rgb = SUCCESS_GREEN
        pSH.font.bold = True
        pSB = tfS2.add_paragraph()
        pSB.text = solution
        pSB.font.size = Pt(10)
        pSB.font.color.rgb = MEDIUM_TEXT

    # Key Learnings
    learnings_box = slide11.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.2), Inches(1.2), Inches(4.6), Inches(5.0)
    )
    learnings_box.fill.solid()
    learnings_box.fill.fore_color.rgb = LIGHT_PURPLE
    learnings_box.line.color.rgb = ACCENT_PURPLE
    learnings_box.line.width = Pt(1.5)

    txLH = slide11.shapes.add_textbox(Inches(8.4), Inches(1.35), Inches(4.2), Inches(0.4))
    tfLH = txLH.text_frame
    pLH = tfLH.paragraphs[0]
    pLH.text = "💡 Key Learnings"
    pLH.font.size = Pt(18)
    pLH.font.color.rgb = ACCENT_PURPLE
    pLH.font.bold = True

    learnings = [
        ("🔒", "Privacy-first design builds user trust"),
        ("🔍", "Explainability > Accuracy for user adoption"),
        ("🇮🇳", "India-localization is a competitive advantage"),
        ("🎯", "Core journey first, polish later"),
        ("👥", "User feedback loops are essential"),
        ("📊", "Simple algorithms with good data beat complex ML"),
    ]
    txLL = slide11.shapes.add_textbox(Inches(8.4), Inches(1.9), Inches(4.2), Inches(4.0))
    tfLL = txLL.text_frame
    tfLL.word_wrap = True
    for i, (icon, text) in enumerate(learnings):
        if i == 0:
            p = tfLL.paragraphs[0]
        else:
            p = tfLL.add_paragraph()
        p.text = f"{icon}  {text}"
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(10)

    # ========================================================================
    # SLIDE 12: FUTURE ROADMAP
    # ========================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    add_background(slide12, WHITE)
    add_top_accent_bar(slide12)
    add_section_header(slide12, 11, "Future Roadmap & Monetization")
    add_bottom_bar(slide12)
    add_slide_number(slide12, 12)

    # Phase cards
    phases = [
        ("Phase 1", "Post-Hackathon\n(3 months)", ACCENT_BLUE, [
            "Add 20+ more roles",
            "Integrate Naukri / LinkedIn APIs",
            "Email progress notifications",
            "User feedback & analytics",
        ]),
        ("Phase 2", "Growth\n(6 months)", ACCENT_PURPLE, [
            "Mobile app (React Native)",
            "College placement dashboard",
            "Premium features launch",
            "1-on-1 career coaching",
        ]),
        ("Phase 3", "Scale\n(12 months)", SUCCESS_GREEN, [
            "AI chatbot (RAG-based Q&A)",
            "Employer talent dashboard",
            "Expand to 5 countries",
            "Regional language support",
        ]),
    ]

    for i, (phase, timeline, color, items) in enumerate(phases):
        x = Inches(0.8) + Inches(i * 4.1)
        # Phase header
        hdr = slide12.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.2), Inches(3.7), Inches(0.65)
        )
        hdr.fill.solid()
        hdr.fill.fore_color.rgb = color
        hdr.line.fill.background()

        txPh = slide12.shapes.add_textbox(x + Inches(0.15), Inches(1.23), Inches(1.5), Inches(0.55))
        tfPh = txPh.text_frame
        pPh = tfPh.paragraphs[0]
        pPh.text = phase
        pPh.font.size = Pt(18)
        pPh.font.color.rgb = WHITE
        pPh.font.bold = True

        txTl = slide12.shapes.add_textbox(x + Inches(1.7), Inches(1.25), Inches(1.9), Inches(0.55))
        tfTl = txTl.text_frame
        tfTl.word_wrap = True
        pTl = tfTl.paragraphs[0]
        pTl.text = timeline
        pTl.font.size = Pt(10)
        pTl.font.color.rgb = WHITE

        # Items
        item_box = slide12.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(2.0), Inches(3.7), Inches(2.2)
        )
        item_box.fill.solid()
        item_box.fill.fore_color.rgb = WHITE
        item_box.line.color.rgb = color
        item_box.line.width = Pt(1.5)

        txItems = slide12.shapes.add_textbox(x + Inches(0.15), Inches(2.15), Inches(3.4), Inches(1.9))
        tfItems = txItems.text_frame
        tfItems.word_wrap = True
        for j, item in enumerate(items):
            if j == 0:
                p = tfItems.paragraphs[0]
            else:
                p = tfItems.add_paragraph()
            p.text = f"▸  {item}"
            p.font.size = Pt(12)
            p.font.color.rgb = DARK_TEXT
            p.space_after = Pt(6)

    # Monetization
    mon_box = slide12.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.6), Inches(11.7), Inches(2.0)
    )
    mon_box.fill.solid()
    mon_box.fill.fore_color.rgb = LIGHT_GRAY
    mon_box.line.color.rgb = BORDER_GRAY
    mon_box.line.width = Pt(1)

    txMH = slide12.shapes.add_textbox(Inches(1.0), Inches(4.7), Inches(3.0), Inches(0.35))
    tfMH = txMH.text_frame
    pMH = tfMH.paragraphs[0]
    pMH.text = "💰 Monetization Strategy"
    pMH.font.size = Pt(16)
    pMH.font.color.rgb = PRIMARY_BLUE
    pMH.font.bold = True

    mon_items = [
        ("🆓", "Freemium", "Core features free forever for students", Inches(1.0)),
        ("⭐", "Premium", "₹299/month — Advanced analytics, priority support", Inches(4.5)),
        ("🏢", "B2B", "₹50,000/year per college — Placement cell dashboard", Inches(8.5)),
    ]
    for icon, title, desc, x in mon_items:
        txI = slide12.shapes.add_textbox(x, Inches(5.2), Inches(3.5), Inches(0.3))
        tfI = txI.text_frame
        pI = tfI.paragraphs[0]
        pI.text = f"{icon}  {title}"
        pI.font.size = Pt(14)
        pI.font.color.rgb = PRIMARY_BLUE
        pI.font.bold = True

        txD = slide12.shapes.add_textbox(x + Inches(0.3), Inches(5.55), Inches(3.2), Inches(0.8))
        tfD = txD.text_frame
        tfD.word_wrap = True
        pD = tfD.paragraphs[0]
        pD.text = desc
        pD.font.size = Pt(11)
        pD.font.color.rgb = MEDIUM_TEXT

    # ========================================================================
    # SLIDE 13: THANK YOU / Q&A
    # ========================================================================
    slide13 = prs.slides.add_slide(blank_layout)
    add_gradient_bg(slide13)

    # Thank you text
    txBox = slide13.shapes.add_textbox(Inches(1), Inches(1.5), Inches(11), Inches(1.2))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = "Thank You!"
    p.font.size = Pt(52)
    p.font.color.rgb = WHITE
    p.font.bold = True
    p.alignment = PP_ALIGN.CENTER

    # Subtitle
    txBox2 = slide13.shapes.add_textbox(Inches(2), Inches(2.7), Inches(9), Inches(0.6))
    tf2 = txBox2.text_frame
    p2 = tf2.paragraphs[0]
    p2.text = "CareerPath AI  —  Making India's Students Job-Ready"
    p2.font.size = Pt(22)
    p2.font.color.rgb = RGBColor(0x93, 0xC5, 0xFD)
    p2.alignment = PP_ALIGN.CENTER

    # Divider
    line = slide13.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(5.5), Inches(3.5), Inches(2.3), Inches(0.04)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = ACCENT_BLUE
    line.line.fill.background()

    # Q&A
    txQ = slide13.shapes.add_textbox(Inches(3), Inches(3.8), Inches(7), Inches(0.6))
    tfQ = txQ.text_frame
    pQ = tfQ.paragraphs[0]
    pQ.text = "Questions & Discussion"
    pQ.font.size = Pt(28)
    pQ.font.color.rgb = WHITE
    pQ.alignment = PP_ALIGN.CENTER

    # Contact card
    contact_card = slide13.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.5), Inches(4.8), Inches(6.3), Inches(1.8)
    )
    contact_card.fill.solid()
    contact_card.fill.fore_color.rgb = RGBColor(0x1E, 0x2D, 0x4A)
    contact_card.line.color.rgb = RGBColor(0x33, 0x4E, 0x78)
    contact_card.line.width = Pt(1)

    contact_lines = [
        ("👥", "Team: [Your Team Name]"),
        ("📧", "Email: [team.lead@email.com]"),
        ("🔗", "Demo: [your-demo-url.vercel.app]"),
        ("💻", "GitHub: [github.com/your-repo]"),
    ]
    txC = slide13.shapes.add_textbox(Inches(3.8), Inches(4.95), Inches(5.7), Inches(1.5))
    tfC = txC.text_frame
    tfC.word_wrap = True
    for i, (icon, text) in enumerate(contact_lines):
        if i == 0:
            p = tfC.paragraphs[0]
        else:
            p = tfC.add_paragraph()
        p.text = f"{icon}  {text}"
        p.font.size = Pt(14)
        p.font.color.rgb = WHITE
        p.space_after = Pt(4)

    # Hackathon badge
    badge = slide13.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.5), Inches(6.8), Inches(4.3), Inches(0.45)
    )
    badge.fill.solid()
    badge.fill.fore_color.rgb = ACCENT_BLUE
    badge.line.fill.background()
    tf = badge.text_frame
    p = tf.paragraphs[0]
    p.text = "🏆  Build For Bharat 2.0  |  September 2026"
    p.font.size = Pt(13)
    p.font.color.rgb = WHITE
    p.font.bold = True
    p.alignment = PP_ALIGN.CENTER

    # ========================================================================
    # SAVE
    # ========================================================================
    output_path = os.path.join(os.path.dirname(__file__), "CareerPath_AI_Presentation.pptx")
    prs.save(output_path)
    print(f"[OK] Presentation saved to: {output_path}")
    print(f"     Total slides: {len(prs.slides)}")
    return output_path


if __name__ == "__main__":
    create_pptx()
