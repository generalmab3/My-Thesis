#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Professional B.Sc. Defense Presentation Generator (PPTX) with Complete RTL Support
and Deep Academic Content from the Thesis.
Student: Mohammad Amir Babazad
Supervisor: Dr. Babak Azarnavid
University of Bonab - Department of Computer Science
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# -------------------------------------------------------------
# Color Palette Constants (Academic & Modern)
# -------------------------------------------------------------
NAVY_DARK    = RGBColor(15, 32, 67)     # #0F2043 (Deep Academic Navy)
NAVY_BLUE    = RGBColor(26, 68, 128)    # #1A4480 (Rich Academic Blue)
ACCENT_BLUE  = RGBColor(41, 128, 185)   # #2980B9 (Vibrant Blue)
TEAL_DARK    = RGBColor(13, 110, 110)   # #0D6E6E (Accent Teal)
CRIMSON      = RGBColor(185, 28, 28)    # #B91C1C (Highlight Red / Shock)
CHARCOAL     = RGBColor(30, 41, 59)     # #1E293B (Body Text Dark)
GRAY_TEXT    = RGBColor(71, 85, 105)    # #475569 (Muted Text)
CARD_BG      = RGBColor(248, 250, 252)  # #F8FAFC (Card Background)
CARD_BORDER  = RGBColor(226, 232, 240)  # #E2E8F0 (Card Border)
WHITE        = RGBColor(255, 255, 255)
GOLD_ACCENT  = RGBColor(217, 119, 6)    # #D97706 (Amber/Gold Accent)

FONT_FA = "Vazirmatn"
FONT_FALLBACK = "B Nazanin"
FONT_EN = "Calibri"

def apply_rtl(p, align=PP_ALIGN.RIGHT):
    """Explicitly inject XML attributes for full native Right-to-Left in PowerPoint."""
    p.alignment = align
    pPr = p._p.get_or_add_pPr()
    pPr.set("rtl", "1")
    if align == PP_ALIGN.RIGHT:
        pPr.set("algn", "r")
    elif align == PP_ALIGN.CENTER:
        pPr.set("algn", "ctr")
    elif align == PP_ALIGN.LEFT:
        pPr.set("algn", "l")

def add_p_run(p, text, font_size=Pt(11), bold=False, color=CHARCOAL, font_name=FONT_FA, is_ltr=False):
    """Add a run to paragraph with explicit language and font settings."""
    run = p.add_run()
    run.text = text
    run.font.name = font_name
    run.font.size = font_size
    run.font.bold = bold
    run.font.color.rgb = color
    
    rPr = run._r.get_or_add_rPr()
    if is_ltr:
        rPr.set("lang", "en-US")
    else:
        rPr.set("lang", "fa-IR")
        rPr.set("altLang", "en-US")
    return run

def set_slide_background(slide, color):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_header(slide, title_text, category_text="پایان‌نامه کارشناسی علوم کامپیوتر | دانشگاه بناب"):
    # Header Top Bar
    header_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
    header_box.fill.solid()
    header_box.fill.fore_color.rgb = NAVY_DARK
    header_box.line.color.rgb = NAVY_DARK
    
    # Sub-category / Breadcrumb
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.8)
    tf.margin_right = Inches(0.8)
    tf.margin_top = Inches(0.12)
    tf.margin_bottom = Inches(0.05)
    
    p0 = tf.paragraphs[0]
    apply_rtl(p0, PP_ALIGN.RIGHT)
    add_p_run(p0, category_text, Pt(11), bold=False, color=GOLD_ACCENT)
    
    # Main Slide Title
    p1 = tf.add_paragraph()
    apply_rtl(p1, PP_ALIGN.RIGHT)
    p1.space_before = Pt(2)
    add_p_run(p1, title_text, Pt(19), bold=True, color=WHITE)
    
    # Accent thin strip below header
    strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.15), Inches(13.333), Inches(0.06))
    strip.fill.solid()
    strip.fill.fore_color.rgb = ACCENT_BLUE
    strip.line.color.rgb = ACCENT_BLUE

def add_footer(slide, slide_num, total_slides=22):
    footer_strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(7.15), Inches(13.333), Inches(0.35))
    footer_strip.fill.solid()
    footer_strip.fill.fore_color.rgb = NAVY_DARK
    footer_strip.line.color.rgb = NAVY_DARK
    
    tf = footer_strip.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.8)
    tf.margin_right = Inches(0.8)
    tf.margin_top = Inches(0.04)
    tf.margin_bottom = Inches(0.02)
    
    p = tf.paragraphs[0]
    apply_rtl(p, PP_ALIGN.RIGHT)
    
    footer_text = f"ارائه دفاعیه پایان‌نامه کارشناسی | محمد امیر بابازاد | استاد راهنما: دکتر بابک آذرنوید                                                    اسلاید {slide_num} از {total_slides}"
    add_p_run(p, footer_text, Pt(9.5), bold=False, color=WHITE)

def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.2)
    return shape

def add_textbox(slide, left, top, width, height):
    tx_box = slide.shapes.add_textbox(left, top, width, height)
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.12)
    tf.margin_right = Inches(0.12)
    tf.margin_top = Inches(0.12)
    tf.margin_bottom = Inches(0.12)
    return tf

def add_notes(slide, notes_text):
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    p = text_frame.paragraphs[0]
    apply_rtl(p, PP_ALIGN.RIGHT)
    add_p_run(p, notes_text, Pt(11), bold=False, color=CHARCOAL)

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    total_slides = 22

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Cover)
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1, CARD_BG)
    
    # Right decorative bar (RTL convention)
    right_bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(12.933), Inches(0), Inches(0.4), Inches(7.5))
    right_bar.fill.solid()
    right_bar.fill.fore_color.rgb = NAVY_DARK
    right_bar.line.color.rgb = NAVY_DARK
    
    # Top banner
    top_band = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(12.933), Inches(0.12))
    top_band.fill.solid()
    top_band.fill.fore_color.rgb = ACCENT_BLUE
    top_band.line.color.rgb = ACCENT_BLUE
    
    # University Logo (Top-Left)
    logo_path = "MAB-THESIS/figs/logo.png"
    if os.path.exists(logo_path):
        slide1.shapes.add_picture(logo_path, Inches(1.0), Inches(0.55), height=Inches(1.25))
    
    # University Text (Header Right)
    tf_uni = add_textbox(slide1, Inches(2.6), Inches(0.45), Inches(9.8), Inches(1.3))
    p0 = tf_uni.paragraphs[0]
    apply_rtl(p0, PP_ALIGN.RIGHT)
    add_p_run(p0, "دانشگاه بناب", Pt(18), bold=True, color=NAVY_DARK)
    
    p1 = tf_uni.add_paragraph()
    apply_rtl(p1, PP_ALIGN.RIGHT)
    p1.space_before = Pt(3)
    add_p_run(p1, "دانشکده علوم پایه | گروه علوم کامپیوتر", Pt(13), bold=False, color=GRAY_TEXT)

    p2 = tf_uni.add_paragraph()
    apply_rtl(p2, PP_ALIGN.RIGHT)
    p2.space_before = Pt(2)
    add_p_run(p2, "جلسه دفاعیه پایان‌نامه دوره کارشناسی علوم کامپیوتر", Pt(12), bold=True, color=TEAL_DARK)
    
    # Title Box (Main Focus)
    title_card = add_card(slide1, Inches(0.8), Inches(1.9), Inches(11.8), Inches(2.55), WHITE, ACCENT_BLUE)
    tf_main = title_card.text_frame
    tf_main.word_wrap = True
    tf_main.margin_left = Inches(0.4)
    tf_main.margin_right = Inches(0.4)
    tf_main.margin_top = Inches(0.25)
    
    p = tf_main.paragraphs[0]
    apply_rtl(p, PP_ALIGN.RIGHT)
    add_p_run(p, "عنوان پایان‌نامه:", Pt(13.5), bold=True, color=ACCENT_BLUE)
    
    p = tf_main.add_paragraph()
    apply_rtl(p, PP_ALIGN.RIGHT)
    p.space_before = Pt(8)
    add_p_run(p, "حل مسئله مستقیم معادله غیرخطی برگرز با استفاده از شبکه‌های عصبی آگاه از فیزیک (PINN)", Pt(22), bold=True, color=NAVY_DARK)
    
    p = tf_main.add_paragraph()
    apply_rtl(p, PP_ALIGN.RIGHT)
    p.space_before = Pt(8)
    add_p_run(p, "پیاده‌سازی محاسباتی زمان‌پیوسته با کتابخانه جکس (JAX) و تحلیل تطبیقی با مقاله مرجع رئیسی و همکاران (۲۰۱۹)", Pt(12.5), bold=False, color=GRAY_TEXT)

    # Info Cards Bottom (Student & Supervisor) - RTL order: Student on Right, Supervisor on Left
    card_info_right = add_card(slide1, Inches(6.8), Inches(4.7), Inches(5.8), Inches(2.25), WHITE, CARD_BORDER)
    tf_info_r = card_info_right.text_frame
    tf_info_r.word_wrap = True
    tf_info_r.margin_right = Inches(0.3)
    tf_info_r.margin_top = Inches(0.2)
    
    p = tf_info_r.paragraphs[0]
    apply_rtl(p, PP_ALIGN.RIGHT)
    add_p_run(p, "مشخصات پژوهشگر:", Pt(13), bold=True, color=TEAL_DARK)
    
    p = tf_info_r.add_paragraph()
    apply_rtl(p, PP_ALIGN.RIGHT)
    p.space_before = Pt(5)
    add_p_run(p, "دانشجو: ", Pt(13), bold=False, color=CHARCOAL)
    add_p_run(p, "محمد امیر بابازاد", Pt(13.5), bold=True, color=NAVY_DARK)

    p = tf_info_r.add_paragraph()
    apply_rtl(p, PP_ALIGN.RIGHT)
    p.space_before = Pt(3)
    add_p_run(p, "شماره دانشجویی: ", Pt(12), bold=False, color=GRAY_TEXT)
    add_p_run(p, "۱۴۰۲۱۳۵۱۰۴", Pt(12), bold=True, color=CHARCOAL)

    p = tf_info_r.add_paragraph()
    apply_rtl(p, PP_ALIGN.RIGHT)
    p.space_before = Pt(2)
    add_p_run(p, "رشته و مقطع: ", Pt(12), bold=False, color=GRAY_TEXT)
    add_p_run(p, "کارشناسی علوم کامپیوتر", Pt(12), bold=True, color=CHARCOAL)

    card_info_left = add_card(slide1, Inches(0.8), Inches(4.7), Inches(5.8), Inches(2.25), WHITE, CARD_BORDER)
    tf_info_l = card_info_left.text_frame
    tf_info_l.word_wrap = True
    tf_info_l.margin_right = Inches(0.3)
    tf_info_l.margin_top = Inches(0.2)

    p = tf_info_l.paragraphs[0]
    apply_rtl(p, PP_ALIGN.RIGHT)
    add_p_run(p, "هیئت داوری و راهنمایی:", Pt(13), bold=True, color=TEAL_DARK)

    p = tf_info_l.add_paragraph()
    apply_rtl(p, PP_ALIGN.RIGHT)
    p.space_before = Pt(5)
    add_p_run(p, "استاد راهنما: ", Pt(13), bold=False, color=CHARCOAL)
    add_p_run(p, "دکتر بابک آذرنوید", Pt(13.5), bold=True, color=NAVY_DARK)

    p = tf_info_l.add_paragraph()
    apply_rtl(p, PP_ALIGN.RIGHT)
    p.space_before = Pt(3)
    add_p_run(p, "تاریخ دفاع: ", Pt(12), bold=False, color=GRAY_TEXT)
    add_p_run(p, "شهریور ماه ۱۴۰۵", Pt(12), bold=True, color=CHARCOAL)

    p = tf_info_l.add_paragraph()
    apply_rtl(p, PP_ALIGN.RIGHT)
    p.space_before = Pt(2)
    add_p_run(p, "محل برگزاری: ", Pt(12), bold=False, color=GRAY_TEXT)
    add_p_run(p, "دانشگاه بناب، دانشکده علوم پایه", Pt(12), bold=False, color=CHARCOAL)
    
    add_notes(slide1, "متن گفتار دانشجو:\nبنام خدا. با سلام و احترام خدمت استاد راهنمای ارجمندم جناب آقای دکتر آذرنوید، داوران گرامی و حاضران محترم. محمد امیر بابازاد هستم، دانشجوی کارشناسی علوم کامپیوتر دانشگاه بناب. پایان‌نامه حاضر با عنوان «حل مسئله مستقیم معادله غیرخطی برگرز با استفاده از شبکه‌های عصبی آگاه از فیزیک (PINN)» با پیاده‌سازی در بستر جکس و ارزیابی تطبیقی با مقاله معتبر رئیسی و همکاران (۲۰۱۹) تدوین شده است.")

    # =========================================================================
    # SLIDE 2: OUTLINE / ساختار ارائه
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2, CARD_BG)
    add_header(slide2, "ساختار و سرفصل‌های جلسه دفاعیه")
    add_footer(slide2, 2, total_slides)

    topics = [
        ("بخش اول: مقدمه و بیان مسئله", "اهمیت شبیه‌سازی معادلات دیفرانسیل جزئی غیرخطی، چالش‌های روش‌های عددی سنتی و ضرورت تلفیق هوش مصنوعی با قوانین فیزیک", NAVY_DARK),
        ("بخش دوم: مبانی نظری و پیشینه پژوهش", "معادله غیرخطی برگرز، پرسپترون چندلایه، قضیه تقریب عمومی چبنکو و سیر تاریخی روش‌های تلفیقی از ۱۹۹۸ تا ۲۰۱۹", NAVY_BLUE),
        ("بخش سوم: متدولوژی شبکه‌های عصبی آگاه از فیزیک", "فرمول‌بندی تابع هزینه دوگانه، سازوکار مشتق‌گیری خودکار دو سطحی و مقایسه تطبیقی مدل‌های زمان‌پیوسته و زمان‌گسسته", TEAL_DARK),
        ("بخش چهارم: پیاده‌سازی و تحلیل نتایج تجربی", "معماری نرم‌افزاری JAX، استراتژی آموزش دومرحله‌ای (Adam + L-BFGS)، به دام انداختن جبهه شوک و مقایسه با مرجع", CRIMSON),
        ("بخش پنجم: جمع‌بندی و افق‌های توسعه آتی", "دستاوردهای کلیدی، تحلیل نقاط قوت و چالش‌های محاسباتی و ۴ پیشنهاد توسعه برای پژوهش‌های آینده", GOLD_ACCENT),
    ]

    top_pos = 1.42
    for idx, (title, desc, color) in enumerate(topics, 1):
        card = add_card(slide2, Inches(0.8), Inches(top_pos), Inches(11.733), Inches(0.98), WHITE, CARD_BORDER)
        
        # Color bar on RIGHT edge (RTL)
        cbar = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(12.333), Inches(top_pos), Inches(0.2), Inches(0.98))
        cbar.fill.solid()
        cbar.fill.fore_color.rgb = color
        cbar.line.color.rgb = color
        
        tf = add_textbox(slide2, Inches(1.0), Inches(top_pos + 0.04), Inches(11.1), Inches(0.9))
        p = tf.paragraphs[0]
        apply_rtl(p, PP_ALIGN.RIGHT)
        add_p_run(p, title, Pt(13.5), bold=True, color=color)
        
        p2 = tf.add_paragraph()
        apply_rtl(p2, PP_ALIGN.RIGHT)
        p2.space_before = Pt(3)
        add_p_run(p2, desc, Pt(11), bold=False, color=CHARCOAL)
        
        top_pos += 1.10

    add_notes(slide2, "متن گفتار دانشجو:\nارائه امروز در ۵ بخش اصلی تدوین شده است: ابتدا انگیزه و چالش‌های محاسباتی را بیان می‌کنم. سپس به مبانی نظری و معادله برگرز می‌پردازم. در بخش سوم متدولوژی دقیق PINN و مشتق‌گیری خودکار تشریح خواهد شد. بخش چهارم شامل پیاده‌سازی جکس، نتایج تجربی و مقایسه با مقاله مرجع رئیسی است و در پایان با جمع‌بندی و کارهای آینده خاتمه خواهم داد.")

    # =========================================================================
    # SLIDE 3: MOTIVATION & PROBLEM STATEMENT
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3, CARD_BG)
    add_header(slide3, "مقدمه و طرح مسئله: اهمیت شبیه‌سازی معادلات دیفرانسیل جزئی")
    add_footer(slide3, 3, total_slides)

    # 3 Cards side by side (RTL order: Right to Left)
    cards_data = [
        ("۱. جایگاه بنیادین در علوم و مهندسی",
         ["معادلات دیفرانسیل جزئی (PDEs) زبان توصیف پدیده‌های پیوسته فیزیکی هستند.",
          "از دینامیک سیالات و آیرودینامیک تا مدل‌سازی ترافیک و انتقال حرارت.",
          "اکثر این معادلات به دلیل ماهیت غیرخطی، فاقد جواب تحلیلی بسته هستند."],
         NAVY_BLUE),
        ("۲. چالش پدیده‌های غیرخطی و امواج شوک",
         ["در معادلات همرفتی غیرخطی، شیب متغیرها ناگهان بی‌نهایت تند می‌شود.",
          "تشکیل جبهه شوک بزرگ‌ترین آزمون پایداری برای هر روش محاسباتی است.",
          "نیازمند تفکیک مکانی-زمانی فوق‌العاده بالا در نواحی بحرانی."],
         CRIMSON),
        ("۳. ضرورت رهیافت محاسباتی نوین",
         ["تلفیق قابلیت‌های یادگیری عمیق با قوانین فیزیکی حاکم بر سیستم.",
          "حذف وابستگی به شبکه‌بندی صلب هندسی (Mesh-Free).",
          "ایجاد حل‌کننده‌ای پیوسته، مشتق‌پذیر و با قابلیت ارزیابی در هر نقطه دلخواه."],
         TEAL_DARK)
    ]

    # Places: Right card (col 1), Middle card (col 2), Left card (col 3)
    left_positions = [8.8, 4.8, 0.8]
    for idx, (title, points, color) in enumerate(cards_data):
        l_pos = left_positions[idx]
        c = add_card(slide3, Inches(l_pos), Inches(1.45), Inches(3.733), Inches(5.4), WHITE, CARD_BORDER)
        
        tag = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(l_pos), Inches(1.45), Inches(3.733), Inches(0.1))
        tag.fill.solid()
        tag.fill.fore_color.rgb = color
        tag.line.color.rgb = color
        
        tf = add_textbox(slide3, Inches(l_pos + 0.1), Inches(1.65), Inches(3.533), Inches(5.1))
        p = tf.paragraphs[0]
        apply_rtl(p, PP_ALIGN.RIGHT)
        add_p_run(p, title, Pt(13), bold=True, color=color)
        
        for pt in points:
            p = tf.add_paragraph()
            apply_rtl(p, PP_ALIGN.RIGHT)
            p.space_before = Pt(8)
            add_p_run(p, "• ", Pt(11), bold=True, color=color)
            add_p_run(p, pt, Pt(11), bold=False, color=CHARCOAL)

    add_notes(slide3, "متن گفتار دانشجو:\nمعادلات دیفرانسیل جزئی ستون فقرات مدل‌سازی سیستم‌های پیوسته فیزیکی و مهندسی هستند. اما چالش بزرگ زمانی رخ می‌دهد که جملات همرفت غیرخطی باعث تشکیل جبهه‌های تیز شوک می‌شوند. اینجاست که نیاز به الگوی محاسباتی جدیدی حس می‌شود که بتواند بدون محدودیت‌های سنتی، این رفتارها را با وفاداری کامل شبیه‌سازی کند.")

    # =========================================================================
    # SLIDE 4: LIMITATIONS OF CLASSICAL NUMERICAL METHODS
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4, CARD_BG)
    add_header(slide4, "چالش‌ها و محدودیت‌های روش‌های عددی سنتی")
    add_footer(slide4, 4, total_slides)

    methods = [
        ("روش تفاضل‌های محدود (FDM)", "تقریب موضعی مشتقات روی شبکه با بسط تیلور", "سادگی الگوریتمی و پیاده‌سازی سریع", "وابستگی شدید به شبکه ساخت‌یافته و ناتوانی در هندسه‌های نامنظم"),
        ("روش اجزای محدود (FEM)", "فرمول‌بندی ضعیف انتگرالی روی المان‌های مجزا", "انعطاف هندسی بالا در مرزهای پیچیده", "هزینه بسیار سنگین تولید شبکه (Mesh Generation) و محاسبات ماتریسی"),
        ("روش‌های طیفی (Spectral)", "بسط جواب بر حسب توابع پایه سراسری متعامد", "دقت نمایی شگفت‌انگیز برای توابع هموار", "پدیده گیبس در مواجهه با ناپیوستگی‌ها و جبهه‌های شوک تیز"),
    ]

    top_pos = 1.45
    for title, idea, adv, lim in methods:
        card = add_card(slide4, Inches(0.8), Inches(top_pos), Inches(11.733), Inches(1.65), WHITE, CARD_BORDER)
        cbar = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(12.333), Inches(top_pos), Inches(0.2), Inches(1.65))
        cbar.fill.solid()
        cbar.fill.fore_color.rgb = NAVY_BLUE
        cbar.line.color.rgb = NAVY_BLUE
        
        tf = add_textbox(slide4, Inches(1.0), Inches(top_pos + 0.08), Inches(11.1), Inches(1.48))
        
        p = tf.paragraphs[0]
        apply_rtl(p, PP_ALIGN.RIGHT)
        add_p_run(p, title, Pt(13.5), bold=True, color=NAVY_BLUE)
        
        p = tf.add_paragraph()
        apply_rtl(p, PP_ALIGN.RIGHT)
        p.space_before = Pt(3)
        add_p_run(p, "• ایده بنیادین: ", Pt(11), bold=True, color=CHARCOAL)
        add_p_run(p, idea, Pt(11), bold=False, color=CHARCOAL)

        p = tf.add_paragraph()
        apply_rtl(p, PP_ALIGN.RIGHT)
        p.space_before = Pt(3)
        add_p_run(p, "• مزیت اصلی: ", Pt(11), bold=True, color=TEAL_DARK)
        add_p_run(p, adv, Pt(11), bold=False, color=CHARCOAL)
        add_p_run(p, "   |   ", Pt(11), bold=False, color=GRAY_TEXT)
        add_p_run(p, "• محدودیت کلیدی: ", Pt(11), bold=True, color=CRIMSON)
        add_p_run(p, lim, Pt(11), bold=False, color=CHARCOAL)
        
        top_pos += 1.85

    add_notes(slide4, "متن گفتار دانشجو:\nروش‌های کلاسیک مانند تفاضل‌های محدود، اجزای محدود و روش‌های طیفی دهه‌ها خدمت کرده‌اند. اما هر یک محدودیت‌های جدی دارند: تولید شبکه در هندسه‌های پیچیده بسیار زمان‌بر است، پدیده نفرین ابعاد در ابعاد بالا ظاهر می‌شود، و خطاهای تقریب گسسته‌سازی در جبهه‌های شوک باعث نوسانات غیرفیزیکی می‌شوند.")

    # =========================================================================
    # SLIDE 5: LIMITATIONS OF PURE DATA-DRIVEN AI
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5, CARD_BG)
    add_header(slide5, "کاستی‌های هوش مصنوعی صرفاً داده‌محور (جعبه سیاه)")
    add_footer(slide5, 5, total_slides)

    # Right Card: Traditional AI Limitations
    card_r = add_card(slide5, Inches(6.8), Inches(1.45), Inches(5.733), Inches(5.4), WHITE, CARD_BORDER)
    tag_r = slide5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(1.45), Inches(5.733), Inches(0.1))
    tag_r.fill.solid()
    tag_r.fill.fore_color.rgb = CRIMSON
    tag_r.line.color.rgb = CRIMSON
    
    tf_r = card_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_right = Inches(0.25)
    tf_r.margin_top = Inches(0.2)
    
    p = tf_r.paragraphs[0]
    apply_rtl(p, PP_ALIGN.RIGHT)
    add_p_run(p, "معایب یادگیری ماشین سنتی در فیزیک", Pt(13.5), bold=True, color=CRIMSON)

    points_r = [
        ("۱. نیاز به کلان‌داده‌های آزمایشگاهی:", "در مهندسی و علوم تجربی، ثبت داده در همه نقاط پیوسته عملاً ناممکن یا فوق‌العاده پرهزینه است."),
        ("۲. رفتار جعبه سیاه (Black-Box):", "شبکه‌های عصبی استاندارد هیچ درکی از اصول بقای جرم، اندازه حرکت یا انرژی ندارند."),
        ("۳. پیش‌بینی‌های غیرفیزیکی و بیش‌برازش:", "در نواحی فاقد داده، مدل‌ها دچار بیش‌برازش شده و نتایجی کاملاً مغایر با قوانین طبیعت تولید می‌کنند.")
    ]
    for title_p, desc_p in points_r:
        p = tf_r.add_paragraph()
        apply_rtl(p, PP_ALIGN.RIGHT)
        p.space_before = Pt(8)
        add_p_run(p, title_p, Pt(11.5), bold=True, color=NAVY_DARK)
        
        p = tf_r.add_paragraph()
        apply_rtl(p, PP_ALIGN.RIGHT)
        p.space_before = Pt(2)
        add_p_run(p, desc_p, Pt(11), bold=False, color=CHARCOAL)

    # Left Card: PINN Paradigm Shift
    card_l = add_card(slide5, Inches(0.8), Inches(1.45), Inches(5.733), Inches(5.4), WHITE, CARD_BORDER)
    tag_l = slide5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.45), Inches(5.733), Inches(0.1))
    tag_l.fill.solid()
    tag_l.fill.fore_color.rgb = TEAL_DARK
    tag_l.line.color.rgb = TEAL_DARK

    tf_l = card_l.text_frame
    tf_l.word_wrap = True
    tf_l.margin_right = Inches(0.25)
    tf_l.margin_top = Inches(0.2)

    p = tf_l.paragraphs[0]
    apply_rtl(p, PP_ALIGN.RIGHT)
    add_p_run(p, "راهکار تحول‌آفرین: شبکه آگاه از فیزیک (PINN)", Pt(13.5), bold=True, color=TEAL_DARK)

    points_l = [
        ("• ادغام معادلات دیفرانسیل در فرآیند آموزش:", "قانون فیزیک مستقیماً وارد تابع هزینه شبکه شده و به عنوان هدایت‌کننده آموزش عمل می‌کند."),
        ("• حل‌کننده بدون شبکه محاسباتی (Mesh-Free):", "ارزیابی فیزیک روی نقاط هم‌مکانی تصادفی انجام شده و نیازی به شبکه‌بندی هندسی نیست."),
        ("• تضمین تعمیم‌پذیری و پایبندی به قوانین بقا:", "حتی با حداقل داده‌های مرزی، قید فیزیک مانع از انحراف و بیش‌برازش مدل در سراسر دامنه می‌شود.")
    ]
    for title_p, desc_p in points_l:
        p = tf_l.add_paragraph()
        apply_rtl(p, PP_ALIGN.RIGHT)
        p.space_before = Pt(8)
        add_p_run(p, title_p, Pt(11.5), bold=True, color=NAVY_BLUE)
        
        p = tf_l.add_paragraph()
        apply_rtl(p, PP_ALIGN.RIGHT)
        p.space_before = Pt(2)
        add_p_run(p, desc_p, Pt(11), bold=False, color=CHARCOAL)

    add_notes(slide5, "متن گفتار دانشجو:\nاگر از شبکه‌های عصبی استاندارد برای شبیه‌سازی سیستم‌های فیزیکی استفاده کنیم، با دو مانع بزرگ روبرو می‌شویم: نیاز به داده‌های آزمایشگاهی بسیار زیاد که اغلب در دسترس نیست، و تمایل به تولید خروجی‌های غیرفیزیکی. راهکار PINN این است که قانون فیزیک را در مغز شبکه تزریق کنیم تا بدون نیاز به داده‌های متراکم، رفتار واقعی سیستم را یاد بگیرد.")

    # =========================================================================
    # SLIDE 6: CORE CONCEPT OF PINN
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6, CARD_BG)
    add_header(slide6, "ایده کلیدی شبکه‌های عصبی آگاه از فیزیک (PINN)")
    add_footer(slide6, 6, total_slides)

    card_top = add_card(slide6, Inches(0.8), Inches(1.45), Inches(11.733), Inches(2.2), WHITE, NAVY_BLUE)
    tf_top = card_top.text_frame
    tf_top.word_wrap = True
    tf_top.margin_right = Inches(0.3)
    tf_top.margin_top = Inches(0.2)

    p = tf_top.paragraphs[0]
    apply_rtl(p, PP_ALIGN.RIGHT)
    add_p_run(p, "تعریف و سازوکار بنیادین چارچوب PINN (رئیسی و همکاران، ۲۰۱۹)", Pt(14), bold=True, color=NAVY_DARK)

    p = tf_top.add_paragraph()
    apply_rtl(p, PP_ALIGN.RIGHT)
    p.space_before = Pt(8)
    add_p_run(p, "یک پرسپترون چندلایه به عنوان تقریبی پیوسته از میدان سرعت ", Pt(12), bold=False, color=CHARCOAL)
    add_p_run(p, "u(t, x; θ)", Pt(12), bold=True, color=NAVY_DARK, font_name=FONT_EN, is_ltr=True)
    add_p_run(p, " در نظر گرفته می‌شود. ورودی‌های شبکه مختصات پیوسته زمانی و مکانی ", Pt(12), bold=False, color=CHARCOAL)
    add_p_run(p, "(t, x)", Pt(12), bold=True, color=NAVY_DARK, font_name=FONT_EN, is_ltr=True)
    add_p_run(p, " هستند. سپس با استفاده از فناوری «مشتق‌گیری خودکار»، مشتقات جزئی استخراج شده و باقیمانده معادله فیزیک تشکیل می‌گردد.", Pt(12), bold=False, color=CHARCOAL)

    # 3 Pill Cards (RTL: Right to Left)
    pills = [
        ("۱. تطابق با شرایط اولیه و مرزی", "شبکه خروجی خود را با داده‌های اولیه و شرایط مرزی همگام می‌سازد تا قیدهای فیزیکی دامنه ارضا شوند.", NAVY_BLUE),
        ("۲. صفر کردن باقیمانده PDE", "در هزاران نقطه هم‌مکانی درون دامنه، باقیمانده معادله دیفرانسیل به سمت صفر هدایت می‌شود.", TEAL_DARK),
        ("۳. حل پیوسته و بدون شبکه", "حل در تمام نقاط فضا-زمان پیوسته بوده و در هر لحظه و مکان دلخواه مستقیماً قابل ارزیابی است.", GOLD_ACCENT)
    ]
    left_positions_p = [8.8, 4.8, 0.8]
    for idx, (title, desc, col) in enumerate(pills):
        l_pos = left_positions_p[idx]
        c = add_card(slide6, Inches(l_pos), Inches(3.85), Inches(3.733), Inches(3.0), WHITE, CARD_BORDER)
        tag = slide6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(l_pos), Inches(3.85), Inches(3.733), Inches(0.08))
        tag.fill.solid()
        tag.fill.fore_color.rgb = col
        tag.line.color.rgb = col
        
        tf = add_textbox(slide6, Inches(l_pos + 0.1), Inches(4.05), Inches(3.533), Inches(2.7))
        p = tf.paragraphs[0]
        apply_rtl(p, PP_ALIGN.RIGHT)
        add_p_run(p, title, Pt(13), bold=True, color=col)
        
        p = tf.add_paragraph()
        apply_rtl(p, PP_ALIGN.RIGHT)
        p.space_before = Pt(8)
        add_p_run(p, desc, Pt(11), bold=False, color=CHARCOAL)

    add_notes(slide6, "متن گفتار دانشجو:\nدر این اسلاید ساختار کلی PINN را مشاهده می‌کنید. شبکه عصبی نگاشت مختصات فضا-زمان به میدان سرعت را یاد می‌گیرد. از طریق مشتق‌گیری خودکار، مشتقات زمانی و مکانی دقیقاً روی گراف محاسباتی استخراج می‌شوند و باقیمانده فیزیک در تابع هزینه قرار می‌گیرد تا سیستم همزمان داده‌های مرزی و قوانین فیزیک را ارضا کند.")

    # =========================================================================
    # SLIDE 7: BENCHMARK PROBLEM: VISCOUS BURGERS' EQUATION
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7, CARD_BG)
    add_header(slide7, "مسئله معیار: معادله غیرخطی برگرز یک‌بعدی")
    add_footer(slide7, 7, total_slides)

    card_eq = add_card(slide7, Inches(0.8), Inches(1.45), Inches(11.733), Inches(1.75), WHITE, CRIMSON)
    tf_eq = card_eq.text_frame
    tf_eq.word_wrap = True
    tf_eq.margin_right = Inches(0.3)
    tf_eq.margin_top = Inches(0.15)

    p = tf_eq.paragraphs[0]
    apply_rtl(p, PP_ALIGN.RIGHT)
    add_p_run(p, "معادله دیفرانسیل جزئی غیرخطی برگرز با ضریب لزجت:", Pt(13), bold=True, color=CRIMSON)

    p = tf_eq.add_paragraph()
    apply_rtl(p, PP_ALIGN.CENTER)
    p.space_before = Pt(4)
    add_p_run(p, "u_t + u · u_x - (0.01 / π) · u_xx = 0 ,    x ∈ [-1, 1],  t ∈ [0, 1]", Pt(15.5), bold=True, color=NAVY_DARK, font_name=FONT_EN, is_ltr=True)

    p = tf_eq.add_paragraph()
    apply_rtl(p, PP_ALIGN.CENTER)
    p.space_before = Pt(4)
    add_p_run(p, "شرط اولیه سینوسی:  u(0, x) = -sin(πx)   |   شرایط مرزی همگن:  u(t, -1) = u(t, 1) = 0", Pt(11.5), bold=False, color=GRAY_TEXT)

    # 2 Sub-cards (RTL: Right card physics, Left card why burgers)
    c_r = add_card(slide7, Inches(6.8), Inches(3.35), Inches(5.733), Inches(3.5), WHITE, CARD_BORDER)
    tf_cr = c_r.text_frame
    tf_cr.word_wrap = True
    tf_cr.margin_right = Inches(0.25)
    tf_cr.margin_top = Inches(0.2)
    
    p = tf_cr.paragraphs[0]
    apply_rtl(p, PP_ALIGN.RIGHT)
    add_p_run(p, "فیزیک حاکم و رقابت میان ترم‌ها", Pt(13), bold=True, color=NAVY_BLUE)

    p = tf_cr.add_paragraph()
    apply_rtl(p, PP_ALIGN.RIGHT)
    p.space_before = Pt(5)
    add_p_run(p, "• جمله همرفت غیرخطی (u · u_x): ", Pt(11), bold=True, color=CHARCOAL)
    add_p_run(p, "باعث انتقال غیرخطی سرعت، شیب تند پروفیل موج و حرکت به سمت مرکز می‌شود.", Pt(11), bold=False, color=CHARCOAL)

    p = tf_cr.add_paragraph()
    apply_rtl(p, PP_ALIGN.RIGHT)
    p.space_before = Pt(5)
    add_p_run(p, "• جمله پخش لزجت (ν · u_xx): ", Pt(11), bold=True, color=CHARCOAL)
    add_p_run(p, "تمایل به هموارسازی و استهلاک امواج دارد. چون ضریب لزجت بسیار کوچک است (حدود ۰٫۰۰۳۱۸)، همرفت غیرخطی غالب شده و موج شوک تشکیل می‌گردد.", Pt(11), bold=False, color=CHARCOAL)

    c_l = add_card(slide7, Inches(0.8), Inches(3.35), Inches(5.733), Inches(3.5), WHITE, CARD_BORDER)
    tf_cl = c_l.text_frame
    tf_cl.word_wrap = True
    tf_cl.margin_right = Inches(0.25)
    tf_cl.margin_top = Inches(0.2)

    p = tf_cl.paragraphs[0]
    apply_rtl(p, PP_ALIGN.RIGHT)
    add_p_run(p, "چرا معادله برگرز به عنوان محک انتخاب شد؟", Pt(13), bold=True, color=TEAL_DARK)

    points_b = [
        "۱. ساده‌ترین مدل غیرخطی شامل هر دو پدیده همرفت و نفوذ لزجت.",
        "۲. ایجاد جبهه شوک فوق‌العاده تیز در حوالی x = 0 در زمان‌های t > 0.4.",
        "۳. چالش بزرگ برای روش‌های عددی به دلیل گرادیان‌های بسیار شدید مکانی.",
        "۴. مسئله استاندارد طلایی در ادبیات PINN برای اثبات دقت الگوریتم‌ها."
    ]
    for pt in points_b:
        p = tf_cl.add_paragraph()
        apply_rtl(p, PP_ALIGN.RIGHT)
        p.space_before = Pt(4)
        add_p_run(p, pt, Pt(11), bold=False, color=CHARCOAL)

    add_notes(slide7, "متن گفتار دانشجو:\nمعادله غیرخطی برگرز با ضریب لزجت ν = 0.01/π، استانداردترین مسئله محک در دینامیک سیالات محاسباتی است. رقابت بین همرفت غیرخطی و پخش ضعیف لزجت باعث می‌شود که یک شرط اولیه هموار سینوسی با گذشت زمان تبدیل به یک جبهه شوک تقریباً ناپیوسته شود. توانایی تقریب این پدیده، عیار واقعی هر روش شبیه‌سازی است.")

    # =========================================================================
    # SLIDE 8: MATHEMATICAL FORMULATION & COMPOSITE LOSS
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8, CARD_BG)
    add_header(slide8, "فرمول‌بندی نظری و ساختار تابع هزینه دوگانه")
    add_footer(slide8, 8, total_slides)

    card_loss = add_card(slide8, Inches(0.8), Inches(1.45), Inches(11.733), Inches(1.5), WHITE, NAVY_DARK)
    tf_l = card_loss.text_frame
    tf_l.word_wrap = True
    tf_l.margin_right = Inches(0.3)
    tf_l.margin_top = Inches(0.12)

    p = tf_l.paragraphs[0]
    apply_rtl(p, PP_ALIGN.RIGHT)
    add_p_run(p, "تابع هزینه کل در چارچوب شبکه‌های عصبی آگاه از فیزیک:", Pt(13), bold=True, color=NAVY_BLUE)

    p = tf_l.add_paragraph()
    apply_rtl(p, PP_ALIGN.CENTER)
    p.space_before = Pt(4)
    add_p_run(p, "Loss(θ) = MSE_u(θ) + MSE_f(θ)", Pt(18), bold=True, color=CRIMSON, font_name=FONT_EN, is_ltr=True)

    # 2 Sub-cards (RTL: Right = MSE_u, Left = MSE_f)
    c_u = add_card(slide8, Inches(6.8), Inches(3.15), Inches(5.733), Inches(3.7), WHITE, CARD_BORDER)
    tf_u = c_u.text_frame
    tf_u.word_wrap = True
    tf_u.margin_right = Inches(0.25)
    tf_u.margin_top = Inches(0.2)

    p = tf_u.paragraphs[0]
    apply_rtl(p, PP_ALIGN.RIGHT)
    add_p_run(p, "۱. خطای داده‌های مرزی و اولیه (MSE_u)", Pt(13), bold=True, color=NAVY_BLUE)

    p = tf_u.add_paragraph()
    apply_rtl(p, PP_ALIGN.CENTER)
    p.space_before = Pt(6)
    add_p_run(p, "MSE_u = (1 / N_u) · Σ | u(t_u^i, x_u^i) - u^i |^2", Pt(12.5), bold=True, color=NAVY_DARK, font_name=FONT_EN, is_ltr=True)

    points_u = [
        "• ارزیابی روی N_u = ۲۰۰ نقطه داده معلوم.",
        "• ۱۰۰ نقطه روی شرط اولیه t = 0.",
        "• ۱۰۰ نقطه روی شرایط مرزی مکانی x = -1 و x = +1.",
        "• تضمین انطباق جواب شبکه با شرایط فیزیکی مرزها."
    ]
    for pt in points_u:
        p = tf_u.add_paragraph()
        apply_rtl(p, PP_ALIGN.RIGHT)
        p.space_before = Pt(4)
        add_p_run(p, pt, Pt(11), bold=False, color=CHARCOAL)

    c_f = add_card(slide8, Inches(0.8), Inches(3.15), Inches(5.733), Inches(3.7), WHITE, CARD_BORDER)
    tf_f = c_f.text_frame
    tf_f.word_wrap = True
    tf_f.margin_right = Inches(0.25)
    tf_f.margin_top = Inches(0.2)

    p = tf_f.paragraphs[0]
    apply_rtl(p, PP_ALIGN.RIGHT)
    add_p_run(p, "۲. خطای باقیمانده فیزیک (MSE_f)", Pt(13), bold=True, color=TEAL_DARK)

    p = tf_f.add_paragraph()
    apply_rtl(p, PP_ALIGN.CENTER)
    p.space_before = Pt(6)
    add_p_run(p, "MSE_f = (1 / N_f) · Σ | f(t_f^i, x_f^i) |^2", Pt(12.5), bold=True, color=NAVY_DARK, font_name=FONT_EN, is_ltr=True)

    points_f = [
        "• ارزیابی روی N_f = ۱۰۰۰۰ نقطه هم‌مکانی در کل فضا-زمان.",
        "• عملگر باقیمانده: f := u_t + u · u_x - (0.01 / π) · u_xx",
        "• نیازمند هیچ برچسب داده‌ای نیست و ارضای مستقیم قانون بقاست.",
        "• نقش یک منظم‌ساز ساختاری قدرتمند برای حذف بیش‌برازش."
    ]
    for pt in points_f:
        p = tf_f.add_paragraph()
        apply_rtl(p, PP_ALIGN.RIGHT)
        p.space_before = Pt(4)
        add_p_run(p, pt, Pt(11), bold=False, color=CHARCOAL)

    add_notes(slide8, "متن گفتار دانشجو:\nتابع هزینه کل از دو مؤلفه تشکیل شده است: اول خطای داده‌های مرزی و اولیه روی ۲۰۰ نقطه، و دوم خطای باقیمانده فیزیک روی ۱۰ هزار نقطه درون دامنه. مؤلفه اول شبکه را مقید به شرایط مرزی می‌کند و مؤلفه دوم قوانین بقا و دینامیک حاکم بر معادله برگرز را در سراسر میدان تضمین می‌نماید.")

    # =========================================================================
    # SLIDE 9: AUTOMATIC DIFFERENTIATION MECHANICS
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9, CARD_BG)
    add_header(slide9, "سازوکار مشتق‌گیری خودکار (Automatic Differentiation)")
    add_footer(slide9, 9, total_slides)

    # 3 Comparison Boxes (RTL order: Right = AutoDiff, Middle = Symbolic, Left = Numerical)
    diff_types = [
        ("مشتق‌گیری خودکار (AutoDiff)", "اعمال قاعده زنجیره‌ای روی گراف محاسباتی برنامه", "دقت تحلیلی تا حد دقت ممیز شناور ماشین بدون خطای برش و با سرعت فوق‌العاده", TEAL_DARK),
        ("مشتق‌گیری نمادین (Symbolic)", "دستکاری جبری عبارات و فرمول‌های ریاضی", "پدیده تورم نمایی عبارات جبری (Expression Swell) و ناتوانی در کدهای کنترلی", CRIMSON),
        ("مشتق‌گیری عددی (تفاضل محدود)", "بر پایه بسط تیلور با طول گام h", "تعارض خطای برش در h بزرگ و خطای گردکردن در h کوچک", GRAY_TEXT),
    ]

    left_positions_d = [8.8, 4.8, 0.8]
    for idx, (title, idea, feat, col) in enumerate(diff_types):
        l_pos = left_positions_d[idx]
        c = add_card(slide9, Inches(l_pos), Inches(1.45), Inches(3.733), Inches(2.6), WHITE, CARD_BORDER)
        tag = slide9.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(l_pos), Inches(1.45), Inches(3.733), Inches(0.08))
        tag.fill.solid()
        tag.fill.fore_color.rgb = col
        tag.line.color.rgb = col
        
        tf = add_textbox(slide9, Inches(l_pos + 0.1), Inches(1.65), Inches(3.533), Inches(2.3))
        p = tf.paragraphs[0]
        apply_rtl(p, PP_ALIGN.RIGHT)
        add_p_run(p, title, Pt(12.5), bold=True, color=col)

        p = tf.add_paragraph()
        apply_rtl(p, PP_ALIGN.RIGHT)
        p.space_before = Pt(4)
        add_p_run(p, "• ایده: ", Pt(11), bold=True, color=CHARCOAL)
        add_p_run(p, idea, Pt(11), bold=False, color=CHARCOAL)

        p = tf.add_paragraph()
        apply_rtl(p, PP_ALIGN.RIGHT)
        p.space_before = Pt(4)
        add_p_run(p, "• ویژگی: ", Pt(10.5), bold=True, color=GRAY_TEXT)
        add_p_run(p, feat, Pt(10.5), bold=False, color=CHARCOAL)

    # Bottom Architecture of AD in PINN
    card_ad = add_card(slide9, Inches(0.8), Inches(4.25), Inches(11.733), Inches(2.6), WHITE, NAVY_BLUE)
    tf_ad = card_ad.text_frame
    tf_ad.word_wrap = True
    tf_ad.margin_right = Inches(0.3)
    tf_ad.margin_top = Inches(0.15)

    p = tf_ad.paragraphs[0]
    apply_rtl(p, PP_ALIGN.RIGHT)
    add_p_run(p, "ساختار دو سطحی مشتق‌گیری خودکار در آموزش PINN:", Pt(13), bold=True, color=NAVY_DARK)

    p = tf_ad.add_paragraph()
    apply_rtl(p, PP_ALIGN.RIGHT)
    p.space_before = Pt(5)
    add_p_run(p, "• سطح اول (مشتق نسبت به ورودی‌های فضا-زمان): ", Pt(11.5), bold=True, color=NAVY_BLUE)
    add_p_run(p, "محاسبه مشتقات مکانی u_x، مشتق زمانی u_t و مشتق دوم مکانی u_xx با استفاده از تبدیل تابعی jax.grad برای تشکیل عملگر باقیمانده فیزیکی f.", Pt(11.5), bold=False, color=CHARCOAL)

    p = tf_ad.add_paragraph()
    apply_rtl(p, PP_ALIGN.RIGHT)
    p.space_before = Pt(5)
    add_p_run(p, "• سطح دوم (مشتق نسبت به پارامترهای شبکه θ): ", Pt(11.5), bold=True, color=CRIMSON)
    add_p_run(p, "پس‌انتشار خطا و محاسبه گرادیان ∇_θ Loss برای به‌روزرسانی وزن‌ها و بایاس‌ها در بهینه‌سازهای آدام و L-BFGS.", Pt(11.5), bold=False, color=CHARCOAL)

    add_notes(slide9, "متن گفتار دانشجو:\nمشتق‌گیری خودکار قلب تپنده PINN است. بر خلاف تفاضل محدود که خطای برش دارد یا محاسبات نمادین که به شدت سنگین می‌شود، AutoDiff مشتقات دقیق ریاضی را بر پایه قاعده زنجیره‌ای روی کدهای پایتون ارزیابی می‌کند. در PINN ما دو سطح مشتق‌گیری داریم: یکی نسبت به مختصات (t, x) برای فیزیک، و دیگری نسبت به وزن‌های شبکه برای آموزش.")

    # =========================================================================
    # SLIDE 10: CONTINUOUS-TIME VS DISCRETE-TIME MODELS
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10, CARD_BG)
    add_header(slide10, "مقایسه تطبیقی: مدل زمان‌پیوسته در برابر زمان‌گسسته")
    add_footer(slide10, 10, total_slides)

    # 2 Comparison Columns (RTL: Right = Continuous, Left = Discrete)
    col_r = add_card(slide10, Inches(6.8), Inches(1.45), Inches(5.733), Inches(5.4), WHITE, NAVY_BLUE)
    tag_cr = slide10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(1.45), Inches(5.733), Inches(0.1))
    tag_cr.fill.solid()
    tag_cr.fill.fore_color.rgb = NAVY_BLUE
    tag_cr.line.color.rgb = NAVY_BLUE
    
    tf_cr = col_r.text_frame
    tf_cr.word_wrap = True
    tf_cr.margin_right = Inches(0.3)
    tf_cr.margin_top = Inches(0.2)

    p = tf_cr.paragraphs[0]
    apply_rtl(p, PP_ALIGN.RIGHT)
    add_p_run(p, "مدل زمان‌پیوسته (رویکرد پیاده‌شده در این پژوهش)", Pt(13.5), bold=True, color=NAVY_BLUE)

    items_cr = [
        ("• ورودی شبکه:", "بردار پیوسته زمانی و مکانی (t, x)"),
        ("• خروجی شبکه:", "مقدار میدان اسکالر u(t, x) در کل فضا-زمان"),
        ("• روش حل زمانی:", "پیوسته و بدون گام‌بندی زمانی (مشتق‌گیری u_t با AutoDiff)"),
        ("• مزیت اصلی:", "یکپارچگی کامل ساختار، سادگی محاسباتی و ارزیابی در هر زمان دلخواه"),
        ("• وضعیت در پژوهش:", "پیاده‌سازی کامل بومی در جکس و ارزیابی تجربی")
    ]
    for k, v in items_cr:
        p = tf_cr.add_paragraph()
        apply_rtl(p, PP_ALIGN.RIGHT)
        p.space_before = Pt(6)
        add_p_run(p, f"{k} ", Pt(11), bold=True, color=CHARCOAL)
        add_p_run(p, v, Pt(11), bold=False, color=CHARCOAL)

    col_l = add_card(slide10, Inches(0.8), Inches(1.45), Inches(5.733), Inches(5.4), WHITE, CARD_BORDER)
    tag_cl = slide10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.45), Inches(5.733), Inches(0.1))
    tag_cl.fill.solid()
    tag_cl.fill.fore_color.rgb = GRAY_TEXT
    tag_cl.line.color.rgb = GRAY_TEXT

    tf_cl = col_l.text_frame
    tf_cl.word_wrap = True
    tf_cl.margin_right = Inches(0.3)
    tf_cl.margin_top = Inches(0.2)

    p = tf_cl.paragraphs[0]
    apply_rtl(p, PP_ALIGN.RIGHT)
    add_p_run(p, "مدل زمان‌گسسته (روش رانگه--کوتا ضمنی)", Pt(13.5), bold=True, color=GRAY_TEXT)

    items_cl = [
        ("• ورودی شبکه:", "فقط مختصات مکانی x در یک مقطع زمانی"),
        ("• خروجی شبکه:", "بردار مراحل میانی رانگه--کوتا (q مرحله) و u^{n+1}"),
        ("• روش حل زمانی:", "گسسته‌سازی زمانی با روش‌های چندمرحله‌ای ضمنی (IRK)"),
        ("• مزیت اصلی:", "پایداری بالا در گام‌های زمانی بسیار بزرگ"),
        ("• وضعیت در پژوهش:", "بررسی و تحلیل نظری ساختار")
    ]
    for k, v in items_cl:
        p = tf_cl.add_paragraph()
        apply_rtl(p, PP_ALIGN.RIGHT)
        p.space_before = Pt(6)
        add_p_run(p, f"{k} ", Pt(11), bold=True, color=CHARCOAL)
        add_p_run(p, v, Pt(11), bold=False, color=CHARCOAL)

    add_notes(slide10, "متن گفتار دانشجو:\nدر شبکه‌های آگاه از فیزیک دو چارچوب اصلی وجود دارد: زمان‌پیوسته و زمان‌گسسته. مدل زمان‌پیوسته که در این پژوهش پیاده‌سازی شده، زمان را به عنوان یک بعد پیوسته در کنار مکان به شبکه می‌دهد. این رویکرد به دلیل یکپارچگی هندسی و توانایی پیش‌بینی در هر مقطع زمانی، برتری کاربردی و زیبایی ساختاری بالایی دارد.")

    # =========================================================================
    # SLIDE 11: SOFTWARE ARCHITECTURE & JAX FRAMEWORK
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide11, CARD_BG)
    add_header(slide11, "معماری نرم‌افزاری و پیاده‌سازی با کتابخانه جکس (JAX)")
    add_footer(slide11, 11, total_slides)

    jax_feats = [
        ("تبدیل تابعی jax.grad", "مشتق‌گیری خودکار معکوس و مستقیم از توابع پایتون تا مراتب دلخواه به صورت تحلیلی بدون سربار تقریبی.", NAVY_BLUE),
        ("بردارسازی jax.vmap", "اجرای موازی و برداری روی دسته‌های عظیم داده بدون نیاز به حلقه‌های کند پایتون و بدون تغییر کد تک‌نمونه.", TEAL_DARK),
        ("کامپایلر شتاب‌یافته jax.jit", "کامپایل گراف محاسباتی به کدهای بهینه ماشین با موتور XLA برای رسیدن به بالاترین سرعت اجرای سخت‌افزاری.", GOLD_ACCENT),
        ("دقت ۶۴ بیتی Float64", "پیکربندی کامل متغیرها در دقت مضاعف (Double Precision) برای به صفر رساندن خطاهای گردکردن در حل عددی شوک.", CRIMSON),
    ]

    top_j = 1.45
    for title, desc, col in jax_feats:
        c = add_card(slide11, Inches(0.8), Inches(top_j), Inches(11.733), Inches(1.2), WHITE, CARD_BORDER)
        cbar = slide11.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(12.333), Inches(top_j), Inches(0.2), Inches(1.2))
        cbar.fill.solid()
        cbar.fill.fore_color.rgb = col
        cbar.line.color.rgb = col
        
        tf = add_textbox(slide11, Inches(1.0), Inches(top_j + 0.08), Inches(11.1), Inches(1.04))
        p = tf.paragraphs[0]
        apply_rtl(p, PP_ALIGN.RIGHT)
        add_p_run(p, title, Pt(13), bold=True, color=col)

        p = tf.add_paragraph()
        apply_rtl(p, PP_ALIGN.RIGHT)
        p.space_before = Pt(3)
        add_p_run(p, desc, Pt(11), bold=False, color=CHARCOAL)

        top_j += 1.35

    add_notes(slide11, "متن گفتار دانشجو:\nیکی از نوآوری‌های فنی این پایان‌نامه، پیاده‌سازی کامل چارچوب با کتابخانه مدرن JAX است. جکس با تلفیق پارادایم برنامه‌نویسی تابعی، کامپایلر تخصصی XLA، و تبدیلات تابعی فوق‌العاده سریع مانند grad و vmap و jit، عملکردی به مراتب تمیزتر و سریع‌تر نسبت به کتابخانه‌های قدیمی نظیر تنسورفلو ۱ ارائه می‌دهد.")

    # =========================================================================
    # SLIDE 12: NETWORK ARCHITECTURE & ACTIVATION FUNCTION
    # =========================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide12, CARD_BG)
    add_header(slide12, "معماری شبکه، مقداردهی اولیه و تابع فعال‌ساز")
    add_footer(slide12, 12, total_slides)

    # 3 Cards (RTL: Right = MLP arch, Middle = Tanh reason, Left = Xavier)
    cards_arch = [
        ("معماری پرسپترون چندلایه",
         ["• ورودی: ۲ نورون (t, x)",
          "• لایه‌های پنهان: ۴ لایه متوالی با ۵۰ نورون در هر لایه",
          "• خروجی: ۱ نورون خطی u(t,x)",
          "• تعداد کل پارامترها: ۷۸۵۱ وزن و بایاس",
          "• محاسبه دقیق پارامترها:\n  (2×50+50) + 3×(50×50+50) + (50×1+1) = 7851"],
         NAVY_DARK),
        ("چرا تابع فعال‌ساز Tanh؟",
         ["• مشتق‌پذیری بی‌نهایت بار (C^∞): معادله برگرز نیازمند مشتق دوم مکانی u_xx است.",
          "• شکست کامل تابع ReLU: مشتق دوم ReLU همه جا صفر است و باقیمانده فیزیک را پوچ می‌کند!",
          "• تقارن حول مبدأ: بازه خروجی (-1, 1) با میانگین صفر پایداری آموزش را حفظ می‌کند."],
         TEAL_DARK),
        ("مقداردهی گزاویه (Glorot)",
         ["• توزیع یکنواخت گزاویه بر پایه ابعاد ورودی و خروجی لایه‌ها.",
          "• حفظ واریانس سیگنال در گذرهای پیش‌رو و پس‌رو.",
          "• جلوگیری از محو شدن یا انفجار گرادیان‌ها.",
          "• مقداردهی صفر برای تمام بایاس‌ها."],
         CRIMSON)
    ]

    left_positions_a = [8.8, 4.8, 0.8]
    for idx, (title, points, col) in enumerate(cards_arch):
        l_pos = left_positions_a[idx]
        c = add_card(slide12, Inches(l_pos), Inches(1.45), Inches(3.733), Inches(5.4), WHITE, CARD_BORDER)
        tag = slide12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(l_pos), Inches(1.45), Inches(3.733), Inches(0.08))
        tag.fill.solid()
        tag.fill.fore_color.rgb = col
        tag.line.color.rgb = col
        
        tf = add_textbox(slide12, Inches(l_pos + 0.1), Inches(1.65), Inches(3.533), Inches(5.1))
        p = tf.paragraphs[0]
        apply_rtl(p, PP_ALIGN.RIGHT)
        add_p_run(p, title, Pt(13), bold=True, color=col)

        for pt in points:
            p = tf.add_paragraph()
            apply_rtl(p, PP_ALIGN.RIGHT)
            p.space_before = Pt(5)
            add_p_run(p, pt, Pt(10.5), bold=False, color=CHARCOAL)

    add_notes(slide12, "متن گفتار دانشجو:\nمعماری شبکه شامل ۴ لایه پنهان با ۵۰ نورون است که مجموعاً ۷۸۵۱ پارامتر دارد. نکته کلیدی انتخاب تابع فعال‌ساز Tanh است. توابعی مثل ReLU که در بینایی ماشین متداولند، در PINN غیرقابل استفاده‌اند؛ زیرا مشتق دوم ReLU صفر است و ترم لزجت معادله را از بین می‌برد. وزن‌ها نیز با روش یکنواخت گزاویه مقداردهی شده‌اند.")

    # =========================================================================
    # SLIDE 13: COLLOCATION POINTS DISTRIBUTION & SAMPLING
    # =========================================================================
    slide13 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide13, CARD_BG)
    add_header(slide13, "راهبرد نمونه‌برداری و توزیع نقاط هم‌مکانی")
    add_footer(slide13, 13, total_slides)

    # Right: Text Card (RTL)
    c_r = add_card(slide13, Inches(6.8), Inches(1.45), Inches(5.733), Inches(5.4), WHITE, CARD_BORDER)
    tf_r = c_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_right = Inches(0.25)
    tf_r.margin_top = Inches(0.2)

    p = tf_r.paragraphs[0]
    apply_rtl(p, PP_ALIGN.RIGHT)
    add_p_run(p, "ترکیب و استراتژی توزیع نقاط آموزش", Pt(13.5), bold=True, color=NAVY_DARK)

    points_samp = [
        ("• داده‌های مرزی و اولیه (N_u = ۲۰۰ نقطه):", "۱۰۰ نقطه روی شرط اولیه t=0 و ۱۰۰ نقطه روی مرزهای x=±1 (نقاط قرمز شکل)."),
        ("• نقاط هم‌مکانی یکنواخت (۵۰۰۰ نقطه):", "توزیع تصادفی یکنواخت در کل دامنه فضا-زمان [-1,1] × [0,1] برای پوشش سراسری فیزیک."),
        ("• نقاط متمرکز در ناحیه شوک (۵۰۰۰ نقطه):", "تمرکز آماری بالا در حوالی خط مرکزی x ≈ 0 و زمان‌های t > 0.3 به دلیل گرادیان‌های بسیار شدید جبهه شوک."),
        ("• نتیجه راهبرد نمونه‌برداری:", "به دام انداختن جبهه تیز شوک بدون افزایش بی‌رویه بار محاسباتی.")
    ]
    for k, v in points_samp:
        p = tf_r.add_paragraph()
        apply_rtl(p, PP_ALIGN.RIGHT)
        p.space_before = Pt(5)
        add_p_run(p, k, Pt(11), bold=True, color=NAVY_BLUE)
        
        p = tf_r.add_paragraph()
        apply_rtl(p, PP_ALIGN.RIGHT)
        p.space_before = Pt(1)
        add_p_run(p, v, Pt(10.5), bold=False, color=CHARCOAL)

    # Left: Image Card (RTL)
    c_l = add_card(slide13, Inches(0.8), Inches(1.45), Inches(5.733), Inches(5.4), WHITE, CARD_BORDER)
    img_path = "MAB-THESIS/figs/png/forward_points.png"
    if os.path.exists(img_path):
        slide13.shapes.add_picture(img_path, Inches(1.0), Inches(1.7), width=Inches(5.333))

    tf_cap = add_textbox(slide13, Inches(1.0), Inches(5.9), Inches(5.333), Inches(0.8))
    p = tf_cap.paragraphs[0]
    apply_rtl(p, PP_ALIGN.CENTER)
    add_p_run(p, "شکل ۱-۴: نقشه توزیع ۲۰۰ نقطه اولیه-مرزی و ۱۰۰۰۰ نقطه هم‌مکانی با تراکم بالا در خط شوک مرکزی.", Pt(10), bold=False, color=GRAY_TEXT)

    add_notes(slide13, "متن گفتار دانشجو:\nدر این شکل، نقشه توزیع نقاط آموزشی را مشاهده می‌فرمایید. نقاط قرمز رنگ نشان‌دهنده ۲۰۰ نقطه شرط مرزی و اولیه هستند. نقاط خاکستری، ۱۰ هزار نقطه هم‌مکانی فیزیک هستند. هوشمندی این پیاده‌سازی در اختصاص ۵۰ درصد از نقاط به ناحیه مرکزی x حوالی صفر است تا شبکه بتواند رزولوشن کافی برای حل جبهه شوک داشته باشد.")

    # =========================================================================
    # SLIDE 14: TWO-STAGE HYBRID OPTIMIZATION STRATEGY
    # =========================================================================
    slide14 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide14, CARD_BG)
    add_header(slide14, "استراتژی بهینه‌سازی ترکیبی دومرحله‌ای (Adam + L-BFGS)")
    add_footer(slide14, 14, total_slides)

    # Right: Text Card (RTL)
    c_r = add_card(slide14, Inches(6.8), Inches(1.45), Inches(5.733), Inches(5.4), WHITE, CARD_BORDER)
    tf_r = c_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_right = Inches(0.25)
    tf_r.margin_top = Inches(0.2)

    p = tf_r.paragraphs[0]
    apply_rtl(p, PP_ALIGN.RIGHT)
    add_p_run(p, "چرا بهینه‌سازی ترکیبی دومرحله‌ای ضروری است؟", Pt(13.5), bold=True, color=NAVY_DARK)

    p = tf_r.add_paragraph()
    apply_rtl(p, PP_ALIGN.RIGHT)
    p.space_before = Pt(6)
    add_p_run(p, "• فاز اول: الگوریتم آدام (۶۰۰۰ گام با نرخ 0.001)\n", Pt(11.5), bold=True, color=NAVY_BLUE)
    add_p_run(p, "سطح تابع هزینه PINN به شدت غیرمحدب و دارای کمینه‌های محلی ناملایم است. آدام با بهره‌گیری از گشتاورهای گرادیان، شبکه را از نقاط اولیه نامناسب عبور داده و به حوضچه همگرایی مناسب می‌رساند.", Pt(11), bold=False, color=CHARCOAL)

    p = tf_r.add_paragraph()
    apply_rtl(p, PP_ALIGN.RIGHT)
    p.space_before = Pt(8)
    add_p_run(p, "• فاز دوم: الگوریتم شبه‌نیوتنی L-BFGS-B\n", Pt(11.5), bold=True, color=CRIMSON)
    add_p_run(p, "پس از رسیدن به ناحیه مناسب، بهینه‌ساز L-BFGS با تقریب ماتریس معکوس هشین و نرخ همگرایی مرتبه دو و فوق‌خطی، ریزش شارپ در تابع هزینه ایجاد کرده و خطا را به مرتبه ۱۰ به توان ۵- کاهش می‌دهد.", Pt(11), bold=False, color=CHARCOAL)

    # Left: Image of Loss History
    c_l = add_card(slide14, Inches(0.8), Inches(1.45), Inches(5.733), Inches(5.4), WHITE, CARD_BORDER)
    img_path = "MAB-THESIS/figs/png/loss_history.png"
    if os.path.exists(img_path):
        slide14.shapes.add_picture(img_path, Inches(1.0), Inches(1.7), width=Inches(5.333))

    tf_cap = add_textbox(slide14, Inches(1.0), Inches(5.9), Inches(5.333), Inches(0.8))
    p = tf_cap.paragraphs[0]
    apply_rtl(p, PP_ALIGN.CENTER)
    add_p_run(p, "شکل ۲-۴: تاریخچه لگاریتمی همگرایی توابع هزینه در دو فاز آدام و L-BFGS.", Pt(10), bold=False, color=GRAY_TEXT)

    add_notes(slide14, "متن گفتار دانشجو:\nاستراتژی بهینه‌سازی ترکیبی برگ برنده این پژوهش است. آدام برای فرار از کمینه‌های محلی اولیه به کار می‌رود و خطای کل را به مرتبه 10^-3 می‌رساند. سپس L-BFGS وارد عمل شده و با تقریب ماتریس هشین، افت ناگهانی شارپ در تابع هزینه ایجاد می‌کند و خطا را به مرتبه 10^-5 می‌رساند.")

    # =========================================================================
    # SLIDE 15: EXPERIMENTAL RESULTS: SHOCK SNAPSHOTS
    # =========================================================================
    slide15 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide15, CARD_BG)
    add_header(slide15, "نتایج تجربی: بازسازی پروفیل میدان و به دام انداختن شوک")
    add_footer(slide15, 15, total_slides)

    # Top: Snapshot Plot
    c_img = add_card(slide15, Inches(0.8), Inches(1.45), Inches(11.733), Inches(3.2), WHITE, CARD_BORDER)
    img_path = "MAB-THESIS/figs/png/burgers_snapshots.png"
    if os.path.exists(img_path):
        slide15.shapes.add_picture(img_path, Inches(1.0), Inches(1.55), width=Inches(11.333))

    # Bottom: 3 Analysis Cards (RTL: Right = t=0.25, Middle = t=0.50, Left = t=0.75)
    snaps = [
        ("مقطع زمانی t = 0.25", "پروفیل اولیه هموار سینوسی با شیب ملایم به سمت مرکز متمایل شده است. تطابق ۱۰۰ درصدی PINN با خط مرجع.", NAVY_BLUE),
        ("مقطع زمانی t = 0.50", "شیب نمودار در حوالی مبدأ به شدت تند شده و جبهه شوک در حال تکوین است. تقریب عالی شیب شدید.", TEAL_DARK),
        ("مقطع زمانی t = 0.75", "جبهه شوک کامل و افت شبه‌ناپیوسته سرعت از مثبت به منفی در x = 0 بدون نوسانات گیبس.", CRIMSON)
    ]
    left_positions_s = [8.8, 4.8, 0.8]
    for idx, (title, desc, col) in enumerate(snaps):
        l_pos = left_positions_s[idx]
        c = add_card(slide15, Inches(l_pos), Inches(4.8), Inches(3.733), Inches(2.1), WHITE, CARD_BORDER)
        tag = slide15.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(l_pos), Inches(4.8), Inches(3.733), Inches(0.06))
        tag.fill.solid()
        tag.fill.fore_color.rgb = col
        tag.line.color.rgb = col
        
        tf = add_textbox(slide15, Inches(l_pos + 0.1), Inches(4.95), Inches(3.533), Inches(1.8))
        p = tf.paragraphs[0]
        apply_rtl(p, PP_ALIGN.RIGHT)
        add_p_run(p, title, Pt(12), bold=True, color=col)

        p = tf.add_paragraph()
        apply_rtl(p, PP_ALIGN.RIGHT)
        p.space_before = Pt(3)
        add_p_run(p, desc, Pt(10.5), bold=False, color=CHARCOAL)

    add_notes(slide15, "متن گفتار دانشجو:\nاین اسلاید قلب نتایج پایان‌نامه را نشان می‌دهد. مقایسه پیش‌بینی PINN (خط‌چین قرمز) با جواب مرجع در سه مقطع زمانی t=0.25, 0.50, 0.75. مشاهده می‌کنید که چگونه شبکه عصبی موج شوک بسیار تیز در مرکز دامنه را با وفاداری کامل و بدون هیچ‌گونه نوسان غیرفیزیکی بازسازی کرده است.")

    # =========================================================================
    # SLIDE 16: ERROR ANALYSIS & HEATMAP
    # =========================================================================
    slide16 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide16, CARD_BG)
    add_header(slide16, "تحلیل توزیع مکانی-زمانی خطا و کانتور باقیمانده")
    add_footer(slide16, 16, total_slides)

    # Right: Text Card (RTL)
    c_r = add_card(slide16, Inches(6.8), Inches(1.45), Inches(5.733), Inches(5.4), WHITE, CARD_BORDER)
    tf_r = c_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_right = Inches(0.25)
    tf_r.margin_top = Inches(0.2)

    p = tf_r.paragraphs[0]
    apply_rtl(p, PP_ALIGN.RIGHT)
    add_p_run(p, "ویژگی‌های توزیع مکانی-زمانی خطا", Pt(13.5), bold=True, color=NAVY_DARK)

    points_err = [
        ("• خطای نزدیک به صفر در ۹۵٪ دامنه:", "در بخش اعظم فضا-زمان رنگ کانتور تاریک است که نشان‌دهنده انطباق فوق‌العاده با واقعیت فیزیکی است."),
        ("• تمرکز خطا در خط باریک شوک:", "تنها در یک نوار بسیار باریک در حوالی x = 0 و بعد از زمان t > 0.4 به دلیل بی‌نهایت شدن گرادیان‌های مکانی، خطای موضعی اندکی دیده می‌شود."),
        ("• مقادیر خطاهای نهایی مدل:", "خطای باقیمانده فیزیک: MSE_f = 6.36 × 10^-5\nخطای شرایط مرزی: MSE_u = 2.35 × 10^-5\nخطای نسبی در نرم L2: معادل ۲.۱۵ درصد.")
    ]
    for k, v in points_err:
        p = tf_r.add_paragraph()
        apply_rtl(p, PP_ALIGN.RIGHT)
        p.space_before = Pt(5)
        add_p_run(p, k, Pt(11), bold=True, color=NAVY_BLUE)
        
        p = tf_r.add_paragraph()
        apply_rtl(p, PP_ALIGN.RIGHT)
        p.space_before = Pt(1)
        add_p_run(p, v, Pt(10.5), bold=False, color=CHARCOAL)

    # Left: Image Card (RTL)
    c_l = add_card(slide16, Inches(0.8), Inches(1.45), Inches(5.733), Inches(5.4), WHITE, CARD_BORDER)
    img_path = "MAB-THESIS/figs/png/error_heatmap.png"
    if os.path.exists(img_path):
        slide16.shapes.add_picture(img_path, Inches(1.0), Inches(1.7), width=Inches(5.333))

    tf_cap = add_textbox(slide16, Inches(1.0), Inches(5.9), Inches(5.333), Inches(0.8))
    p = tf_cap.paragraphs[0]
    apply_rtl(p, PP_ALIGN.CENTER)
    add_p_run(p, "شکل ۴-۴: نقشه کانتور دوبعدی قدرمطلق خطای نقطه‌ای در دامنه فضا-زمان.", Pt(10), bold=False, color=GRAY_TEXT)

    add_notes(slide16, "متن گفتار دانشجو:\nنقشه کانتور دوبعدی خطا نشان می‌دهد که خطای شبیه‌سازی در ۹۵ درصد دامنه عملاً صفر است. بیشینه خطا صرفاً در امتداد یک نوار باریک مرکزی متمرکز است که ناشی از طبیعت ناپیوستگی شوک است. خطای نسبی کل ۲.۱۵ درصد به دست آمده که با توجه به سخت‌افزار معمولی، بسیار چشمگیر است.")

    # =========================================================================
    # SLIDE 17: COMPARATIVE BENCHMARK WITH RAISSI ET AL. (2019)
    # =========================================================================
    slide17 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide17, CARD_BG)
    add_header(slide17, "مقایسه تطبیقی با مقاله مرجع رئیسی و همکاران (۲۰۱۹)")
    add_footer(slide17, 17, total_slides)

    # Table on Top - Native RTL table
    table_shape = slide17.shapes.add_table(7, 3, Inches(0.8), Inches(1.45), Inches(11.733), Inches(3.2))
    table = table_shape.table
    tblPr = table._tbl.tblPr
    tblPr.set("rtl", "1")
    
    table.columns[0].width = Inches(3.4)
    table.columns[1].width = Inches(4.1)
    table.columns[2].width = Inches(4.233)

    # In RTL table: Col 0 is rightmost (Header: شاخص), Col 1 is middle (رئیسی), Col 2 is leftmost (پژوهش حاضر)
    headers = ["شاخص مقایسه‌ای", "رئیسی و همکاران (۲۰۱۹)", "پژوهش حاضر"]
    for col_idx, h in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_DARK
        p = cell.text_frame.paragraphs[0]
        apply_rtl(p, PP_ALIGN.CENTER)
        add_p_run(p, h, Pt(11.5), bold=True, color=WHITE)

    rows_data = [
        ("معماری شبکه عصبی", "۸ لایه پنهان، ۲۰ نورون در هر لایه", "۴ لایه پنهان، ۵۰ نورون در هر لایه"),
        ("تعداد کل پارامترها", "۳۰۲۱ پارامتر وزن و بایاس", "۷۸۵۱ پارامتر وزن و بایاس"),
        ("نقاط اولیه و مرزی (N_u)", "۱۰۰ نقطه", "۲۰۰ نقطه (توزیع متعادل)"),
        ("توزیع نقاط هم‌مکانی", "نمونه‌برداری ابرمکعب لاتین", "۵۰٪ تصادفی + ۵۰٪ متمرکز در شوک"),
        ("بستر نرم‌افزاری و کامپایلر", "تنسورفلو ۱ (کد کلاسیک)", "جکس (JAX) با کامپایلر XLA"),
        ("خطای نسبی در نرم L2", "6.7 × 10^-4 (سخت‌افزار سرور)", "2.15 × 10^-2 (سخت‌افزار استاندارد)"),
    ]

    for row_idx, row in enumerate(rows_data, 1):
        for col_idx, val in enumerate(row):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if row_idx % 2 == 1 else CARD_BG
            p = cell.text_frame.paragraphs[0]
            apply_rtl(p, PP_ALIGN.CENTER)
            add_p_run(p, val, Pt(10.5), bold=(col_idx == 2), color=CHARCOAL if col_idx != 2 else NAVY_BLUE)

    # Analysis Box Bottom
    c_bot = add_card(slide17, Inches(0.8), Inches(4.85), Inches(11.733), Inches(2.0), WHITE, CARD_BORDER)
    tf_b = c_bot.text_frame
    tf_b.word_wrap = True
    tf_b.margin_right = Inches(0.25)
    tf_b.margin_top = Inches(0.12)

    p = tf_b.paragraphs[0]
    apply_rtl(p, PP_ALIGN.RIGHT)
    add_p_run(p, "تحلیل تفاوت‌ها و دلایل انطباق ساختاری:", Pt(12), bold=True, color=TEAL_DARK)

    p = tf_b.add_paragraph()
    apply_rtl(p, PP_ALIGN.RIGHT)
    p.space_before = Pt(3)
    add_p_run(p, "۱. شبکه عمیق‌تر در مقاله مرجع (۸ لایه پنهان) قابلیت بالاتری در تقریب نواحی با شیب‌های بسیار تیز دارد.\n۲. سقف تکرارهای L-BFGS در مقاله مرجع بر روی سرورهای قدرتمند بسیار بالاتر بوده است.\n۳. از نظر بازتولید کیفی پروفیل شوک و موقعیت فیزیکی آن، پیاده‌سازی جکس در این پژوهش وفاداری کاملی به نتایج مرجع نشان می‌دهد.", Pt(10.5), bold=False, color=CHARCOAL)

    add_notes(slide17, "متن گفتار دانشجو:\nدر این جدول مقایسه تطبیقی با مقاله مرجع رئیسی را ملاحظه می‌فرمایید. مقاله مرجع از شبکه‌ای عمیق‌تر با ۸ لایه پنهان و تعداد تکرارهای بالا بر روی سرور استفاده کرده است. در این پژوهش با معماری ۴ لایه در ۵۰ نورون و پیاده‌سازی بومی در JAX، موقعیت مکانی و شیب شوک با دقت عالی بازتولید شده است.")

    # =========================================================================
    # SLIDE 18: STRENGTHS, LIMITATIONS & TECHNICAL INSIGHTS
    # =========================================================================
    slide18 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide18, CARD_BG)
    add_header(slide18, "تحلیل نقاط قوت، چالش‌های محاسباتی و درس‌آموخته‌ها")
    add_footer(slide18, 18, total_slides)

    # 2 Columns (RTL: Right = Strengths, Left = Limitations)
    c_str = add_card(slide18, Inches(6.8), Inches(1.45), Inches(5.733), Inches(5.4), WHITE, TEAL_DARK)
    tag_s = slide18.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(1.45), Inches(5.733), Inches(0.1))
    tag_s.fill.solid()
    tag_s.fill.fore_color.rgb = TEAL_DARK
    tag_s.line.color.rgb = TEAL_DARK

    tf_s = c_str.text_frame
    tf_s.word_wrap = True
    tf_s.margin_right = Inches(0.25)
    tf_s.margin_top = Inches(0.2)

    p = tf_s.paragraphs[0]
    apply_rtl(p, PP_ALIGN.RIGHT)
    add_p_run(p, "نقاط قوت برجسته رهیافت PINN", Pt(13.5), bold=True, color=TEAL_DARK)

    strengths = [
        "• حل بدون شبکه (Mesh-Free): عدم نیاز به تولید شبکه‌های پیچیده محاسباتی.",
        "• حل پیوسته در فضا-زمان: توانایی ارزیابی میدان و مشتقات در هر نقطه دلخواه.",
        "• مقاومت بالا در برابر بیش‌برازش: قید فیزیک به عنوان یک منظم‌ساز قدرتمند عمل می‌کند.",
        "• انعطاف‌پذیری فوق‌العاده: کدنویسی ماژولار و سریع با تبدیلات تابعی جکس."
    ]
    for st in strengths:
        p = tf_s.add_paragraph()
        apply_rtl(p, PP_ALIGN.RIGHT)
        p.space_before = Pt(6)
        add_p_run(p, st, Pt(11), bold=False, color=CHARCOAL)

    c_lim = add_card(slide18, Inches(0.8), Inches(1.45), Inches(5.733), Inches(5.4), WHITE, CRIMSON)
    tag_l = slide18.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.45), Inches(5.733), Inches(0.1))
    tag_l.fill.solid()
    tag_l.fill.fore_color.rgb = CRIMSON
    tag_l.line.color.rgb = CRIMSON

    tf_l = c_lim.text_frame
    tf_l.word_wrap = True
    tf_l.margin_right = Inches(0.25)
    tf_l.margin_top = Inches(0.2)

    p = tf_l.paragraphs[0]
    apply_rtl(p, PP_ALIGN.RIGHT)
    add_p_run(p, "چالش‌های محاسباتی و محدودیت‌ها", Pt(13.5), bold=True, color=CRIMSON)

    limitations = [
        "• زمان آموزش در مقایسه با روش‌های سنتی: بهینه‌سازی غیرمحدب نسبت به حل‌کننده‌های خطی زمان‌برتر است.",
        "• تعارض گرادیان‌ها در تابع هزینه: رقابت میان مؤلفه مرزی و مؤلفه باقیمانده فیزیک.",
        "• چالش تقریب گرادیان‌های بی‌نهایت: نیاز به شبکه‌های عمیق‌تر در لزجت‌های بسیار نزدیک به صفر.",
        "• حساسیت به نقاط اولیه: ضرورت اجرای فاز اولیه آدام قبل از روش‌های شبه‌نیوتنی."
    ]
    for lim in limitations:
        p = tf_l.add_paragraph()
        apply_rtl(p, PP_ALIGN.RIGHT)
        p.space_before = Pt(6)
        add_p_run(p, lim, Pt(11), bold=False, color=CHARCOAL)

    add_notes(slide18, "متن گفتار دانشجو:\nدر تحلیل منصفانه، مزیت اصلی PINN در بی‌نیازی از شبکه محاسباتی و مقاومت در برابر بیش‌برازش است. اما چالش‌هایی نظیر غیرمحدب بودن تابع هزینه و تعارض گرادیان‌ها میان بخش مرزی و فیزیکی وجود دارد که با استراتژی دومرحله‌ای ما با موفقیت مدیریت شدند.")

    # =========================================================================
    # SLIDE 19: CONCLUSION & RESEARCH CONTRIBUTIONS
    # =========================================================================
    slide19 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide19, CARD_BG)
    add_header(slide19, "جمع‌بندی و دستاوردهای بنیادین پژوهش")
    add_footer(slide19, 19, total_slides)

    achievements = [
        ("۱. اثبات عملی کارآمدی PINN در معادلات غیرخطی", "نشان داده شد که ادغام باقیمانده فیزیکی در تابع هزینه می‌تواند بدون نیاز به شبکه‌بندی صلب، جبهه‌های تیز شوک را با وفاداری بازسازی نماید.", NAVY_DARK),
        ("۲. پیاده‌سازی محاسباتی بومی با کتابخانه JAX", "استفاده از کامپایلر XLA و تبدیلات grad و vmap خط لوله محاسباتی تمیز، سریع و با دقت ممیز شناور ۶۴ بیتی ایجاد کرد.", NAVY_BLUE),
        ("۳. استراتژی ترکیبی بهینه‌سازی و نمونه‌برداری تطبیقی", "ترکیب ۶۰۰۰ گام آدام با روش L-BFGS-B و تمرکز ۵۰٪ نقاط در حوالی شوک همگرایی سریع به خطای کم را تضمین نمود.", TEAL_DARK),
        ("۴. تطابق و اعتبارسنجی با ادبیات مرجع بین‌المللی", "نتایج به دست آمده تطابق کیفی و کمی کاملی با رفتار پیش‌بینی‌شده در مقاله معتبر رئیسی و همکاران (۲۰۱۹) نشان داد.", GOLD_ACCENT),
    ]

    top_a = 1.45
    for title, desc, col in achievements:
        c = add_card(slide19, Inches(0.8), Inches(top_a), Inches(11.733), Inches(1.2), WHITE, CARD_BORDER)
        cbar = slide19.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(12.333), Inches(top_a), Inches(0.2), Inches(1.2))
        cbar.fill.solid()
        cbar.fill.fore_color.rgb = col
        cbar.line.color.rgb = col
        
        tf = add_textbox(slide19, Inches(1.0), Inches(top_a + 0.08), Inches(11.1), Inches(1.04))
        p = tf.paragraphs[0]
        apply_rtl(p, PP_ALIGN.RIGHT)
        add_p_run(p, title, Pt(13), bold=True, color=col)

        p = tf.add_paragraph()
        apply_rtl(p, PP_ALIGN.RIGHT)
        p.space_before = Pt(3)
        add_p_run(p, desc, Pt(11), bold=False, color=CHARCOAL)

        top_a += 1.35

    add_notes(slide19, "متن گفتار دانشجو:\nدر جمع‌بندی، این پایان‌نامه نشان داد که شبکه‌های عصبی آگاه از فیزیک یک ابزار قدرتمند، مدرن و قابل اعتماد برای حل مسائل غیرخطی فیزیک هستند. پیاده‌سازی جکس، راهبرد بهینه‌سازی ترکیبی و نمونه‌برداری متمرکز در شوک، سه دستاورد برجسته فنی این پژوهش به شمار می‌روند.")

    # =========================================================================
    # SLIDE 20: FUTURE WORK & RESEARCH HORIZONS
    # =========================================================================
    slide20 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide20, CARD_BG)
    add_header(slide20, "افق‌های توسعه و پیشنهادهای پژوهشی آتی")
    add_footer(slide20, 20, total_slides)

    horizons = [
        ("۱. وزن‌دهی پویا به مؤلفه‌های تابع هزینه (Self-Adaptive Loss)", "به‌کارگیری ضرایب تطبیقی مانند وزن‌دهی بر پایه مقادیر ویژه ماتریس هسین یا رویکرد بیشینه-کمینه برای تعدیل گرادیان‌ها.", NAVY_BLUE),
        ("۲. شبکه‌های عصبی با ویژگی‌های فوریه (Fourier Feature Networks)", "تعبیه نگاشت‌های فوریه تصادفی در لایه ورودی برای غلبه بر سوگیری فرکانس پایین شبکه‌های عصبی (Spectral Bias).", TEAL_DARK),
        ("۳. تفکیک دامنه و موازی‌سازی (XPINN / FBPINN)", "تقسیم دامنه فضا-زمان به زیردامنه‌های موازی و آموزش شبکه‌های عصبی مستقل در هر ناحیه برای مقیاس‌پذیری بالا.", GOLD_ACCENT),
        ("۴. توسعه به سیستم‌های دوبعدی و سه‌بعدی و معادلات ناویه--استوکس", "تعمیم چارچوب پیاده‌سازی‌شده در جکس به جریان‌های سیال آشفته دوبعدی و سه‌بعدی و هندسه‌های نامنظم صنعتی.", CRIMSON),
    ]

    top_h = 1.45
    for title, desc, col in horizons:
        c = add_card(slide20, Inches(0.8), Inches(top_h), Inches(11.733), Inches(1.2), WHITE, CARD_BORDER)
        cbar = slide20.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(12.333), Inches(top_h), Inches(0.2), Inches(1.2))
        cbar.fill.solid()
        cbar.fill.fore_color.rgb = col
        cbar.line.color.rgb = col
        
        tf = add_textbox(slide20, Inches(1.0), Inches(top_h + 0.08), Inches(11.1), Inches(1.04))
        p = tf.paragraphs[0]
        apply_rtl(p, PP_ALIGN.RIGHT)
        add_p_run(p, title, Pt(13), bold=True, color=col)

        p = tf.add_paragraph()
        apply_rtl(p, PP_ALIGN.RIGHT)
        p.space_before = Pt(3)
        add_p_run(p, desc, Pt(11), bold=False, color=CHARCOAL)

        top_h += 1.35

    add_notes(slide20, "متن گفتار دانشجو:\nبرای کارهای آینده، چهار محور اصلی پیشنهاد می‌شود: استفاده از وزن‌دهی پویا برای حل تعارض گرادیان‌ها، به‌کارگیری توابع پایه فوریه برای بهبود تقریب فرکانس‌های بالا، روش‌های تفکیک دامنه XPINN، و توسعه چارچوب به معادلات دو و سه‌بعدی ناویه-استوکس.")

    # =========================================================================
    # SLIDE 21: KEY REFERENCES & LITERATURE
    # =========================================================================
    slide21 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide21, CARD_BG)
    add_header(slide21, "مراجع کلیدی و ادبیات معتبر بین‌المللی")
    add_footer(slide21, 21, total_slides)

    refs_data = [
        ("Raissi, Perdikaris & Karniadakis (2019)", "Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear PDEs. Journal of Computational Physics, 378, 686-707.", NAVY_DARK),
        ("Cuomo, Di Cola, Giampaolo et al. (2022)", "Scientific Machine Learning Through Physics-Informed Neural Networks: Where we are and What's next. Journal of Scientific Computing, 92(3), 88.", NAVY_BLUE),
        ("Cybenko (1989)", "Approximation by superpositions of a sigmoidal function. Mathematics of Control, Signals and Systems, 2(4), 303-314.", TEAL_DARK),
        ("Bradbury, Frostig, Hawkins et al. (2018)", "JAX: Autograd and XLA for high-performance machine learning research. Software framework.", GOLD_ACCENT),
    ]

    top_r = 1.45
    for author, citation, col in refs_data:
        c = add_card(slide21, Inches(0.8), Inches(top_r), Inches(11.733), Inches(1.2), WHITE, CARD_BORDER)
        cbar = slide21.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(12.333), Inches(top_r), Inches(0.2), Inches(1.2))
        cbar.fill.solid()
        cbar.fill.fore_color.rgb = col
        cbar.line.color.rgb = col
        
        tf = add_textbox(slide21, Inches(1.0), Inches(top_r + 0.08), Inches(11.1), Inches(1.04))
        p = tf.paragraphs[0]
        apply_rtl(p, PP_ALIGN.RIGHT)
        add_p_run(p, author, Pt(12.5), bold=True, color=col)

        p = tf.add_paragraph()
        apply_rtl(p, PP_ALIGN.RIGHT)
        p.space_before = Pt(3)
        add_p_run(p, citation, Pt(10), bold=False, color=CHARCOAL, font_name=FONT_EN, is_ltr=True)

        top_r += 1.35

    add_notes(slide21, "متن گفتار دانشجو:\nاین پژوهش بر پایه مقالات معتبر بین‌المللی از جمله مقاله بنیادین رئیسی، پردیکاریس و کارنیاداکیس در ژورنال JCP (۲۰۱۹)، مقاله مروری کومو و همکاران (۲۰۲۲) و مبانی نظری چبنکو (۱۹۸۹) شکل گرفته است.")

    # =========================================================================
    # SLIDE 22: Q&A & CLOSING SLIDE
    # =========================================================================
    slide22 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide22, NAVY_DARK)
    
    card_end = add_card(slide22, Inches(1.5), Inches(1.2), Inches(10.333), Inches(5.1), WHITE, ACCENT_BLUE)
    tf_e = card_end.text_frame
    tf_e.word_wrap = True
    tf_e.margin_top = Inches(0.4)
    tf_e.margin_left = Inches(0.4)
    tf_e.margin_right = Inches(0.4)

    p = tf_e.paragraphs[0]
    apply_rtl(p, PP_ALIGN.CENTER)
    add_p_run(p, "با تشکر و سپاس فراوان از توجه و شکیبایی شما", Pt(22), bold=True, color=NAVY_DARK)

    p = tf_e.add_paragraph()
    apply_rtl(p, PP_ALIGN.CENTER)
    p.space_before = Pt(14)
    add_p_run(p, "استاد راهنما: جناب آقای دکتر بابک آذرنوید", Pt(15), bold=True, color=TEAL_DARK)

    p = tf_e.add_paragraph()
    apply_rtl(p, PP_ALIGN.CENTER)
    p.space_before = Pt(8)
    add_p_run(p, "دانشجو: محمد امیر بابازاد | دانشکده علوم پایه | گروه علوم کامپیوتر دانشگاه بناب", Pt(12.5), bold=False, color=GRAY_TEXT)

    p = tf_e.add_paragraph()
    apply_rtl(p, PP_ALIGN.CENTER)
    p.space_before = Pt(18)
    add_p_run(p, "«آماده پاسخگویی به پرسش‌ها و بهره‌مندی از نظرات ارزشمند هیئت محترم داوران»", Pt(15), bold=True, color=CRIMSON)

    add_notes(slide22, "متن گفتار دانشجو:\nدر پایان از راهنمایی‌های ارزنده و دلسوزانه استاد راهنمای گرانقدرم جناب آقای دکتر آذرنوید، و از توجه و حضور داوران محترم و همه عزیزان صمیمانه سپاسگزاری می‌کنم. با کمال میل آماده پاسخگویی به سوالات، نقدها و رهنمودهای ارزشمند هیئت محترم داوران هستم.")

    # Post-process all shapes and tables to ensure 100% RTL coverage
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                for p in shape.text_frame.paragraphs:
                    pPr = p._p.get_or_add_pPr()
                    pPr.set("rtl", "1")
                    if not pPr.get("algn"):
                        pPr.set("algn", "r")
                    for r in p.runs:
                        rPr = r._r.get_or_add_rPr()
                        if not rPr.get("lang"):
                            rPr.set("lang", "fa-IR")
                            rPr.set("altLang", "en-US")
            elif shape.has_table:
                tbl = shape.table._tbl
                tbl.tblPr.set("rtl", "1")
                for row in shape.table.rows:
                    for cell in row.cells:
                        for p in cell.text_frame.paragraphs:
                            pPr = p._p.get_or_add_pPr()
                            pPr.set("rtl", "1")
                            if not pPr.get("algn"):
                                pPr.set("algn", "ctr" if p.alignment == PP_ALIGN.CENTER else "r")
                            for r in p.runs:
                                rPr = r._r.get_or_add_rPr()
                                if not rPr.get("lang"):
                                    rPr.set("lang", "fa-IR")
                                    rPr.set("altLang", "en-US")
        if slide.has_notes_slide:
            for p in slide.notes_slide.notes_text_frame.paragraphs:
                pPr = p._p.get_or_add_pPr()
                pPr.set("rtl", "1")
                pPr.set("algn", "r")
                for r in p.runs:
                    rPr = r._r.get_or_add_rPr()
                    if not rPr.get("lang"):
                        rPr.set("lang", "fa-IR")
                        rPr.set("altLang", "en-US")

    # Save presentation
    os.makedirs("MAB-THESIS", exist_ok=True)
    out_path = "MAB-THESIS/defense_presentation.pptx"
    prs.save(out_path)
    print(f"Presentation generated successfully: {out_path} ({len(prs.slides)} slides)")

if __name__ == "__main__":
    build_presentation()
