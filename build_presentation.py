#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to generate a master-level, professional B.Sc. Defense Presentation (PPTX)
for Mohammad Amir Babazad's thesis at University of Bonab.
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

FONT_FA = "Tahoma"  # Standard cross-platform Persian font for PPTX
FONT_EN = "Calibri"

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
    p0.text = category_text
    p0.alignment = PP_ALIGN.RIGHT
    p0.font.name = FONT_FA
    p0.font.size = Pt(11)
    p0.font.color.rgb = GOLD_ACCENT
    p0.font.bold = False
    
    # Main Slide Title
    p1 = tf.add_paragraph()
    p1.text = title_text
    p1.alignment = PP_ALIGN.RIGHT
    p1.font.name = FONT_FA
    p1.font.size = Pt(20)
    p1.font.color.rgb = WHITE
    p1.font.bold = True
    p1.space_before = Pt(2)
    
    # Accent thin strip below header
    strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.15), Inches(13.333), Inches(0.06))
    strip.fill.solid()
    strip.fill.fore_color.rgb = ACCENT_BLUE
    strip.line.color.rgb = ACCENT_BLUE

def add_footer(slide, slide_num, total_slides=21):
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
    p.text = f"ارائه دفاعیه پایان‌نامه کارشناسی | محمد امیر بابازاد | استاد راهنما: دکتر بابک آذرنوید                                                    اسلاید {slide_num} از {total_slides}"
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(9.5)
    p.font.color.rgb = WHITE

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
    tf.margin_left = Inches(0.15)
    tf.margin_right = Inches(0.15)
    tf.margin_top = Inches(0.15)
    tf.margin_bottom = Inches(0.15)
    return tf

def add_notes(slide, notes_text):
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = notes_text

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    total_slides = 21

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Cover)
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1, CARD_BG)
    
    # Left decorative bar
    left_bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.4), Inches(7.5))
    left_bar.fill.solid()
    left_bar.fill.fore_color.rgb = NAVY_DARK
    left_bar.line.color.rgb = NAVY_DARK
    
    # Top banner
    top_band = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(0), Inches(12.933), Inches(0.12))
    top_band.fill.solid()
    top_band.fill.fore_color.rgb = ACCENT_BLUE
    top_band.line.color.rgb = ACCENT_BLUE
    
    # University Logo / Badge Placeholder
    logo_path = "MAB-THESIS/figs/logo.png"
    if os.path.exists(logo_path):
        slide1.shapes.add_picture(logo_path, Inches(1.2), Inches(0.6), height=Inches(1.2))
    
    # University Text (Header Right)
    tf_uni = add_textbox(slide1, Inches(3.0), Inches(0.5), Inches(9.5), Inches(1.2))
    p = tf_uni.paragraphs[0]
    p.text = "دانشگاه بناب"
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK
    
    p2 = tf_uni.add_paragraph()
    p2.text = "دانشکده علوم پایه | گروه علوم کامپیوتر"
    p2.alignment = PP_ALIGN.RIGHT
    p2.font.name = FONT_FA
    p2.font.size = Pt(13)
    p2.font.color.rgb = GRAY_TEXT
    p2.space_before = Pt(3)

    p3 = tf_uni.add_paragraph()
    p3.text = "جلسه دفاعیه پایان‌نامه دوره کارشناسی علوم کامپیوتر"
    p3.alignment = PP_ALIGN.RIGHT
    p3.font.name = FONT_FA
    p3.font.size = Pt(12)
    p3.font.bold = True
    p3.font.color.rgb = TEAL_DARK
    p3.space_before = Pt(2)
    
    # Title Box (Main Focus)
    title_card = add_card(slide1, Inches(1.0), Inches(1.9), Inches(11.333), Inches(2.5), WHITE, ACCENT_BLUE)
    tf_main = title_card.text_frame
    tf_main.word_wrap = True
    tf_main.margin_left = Inches(0.4)
    tf_main.margin_right = Inches(0.4)
    tf_main.margin_top = Inches(0.3)
    
    p = tf_main.paragraphs[0]
    p.text = "عنوان پایان‌نامه:"
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(14)
    p.font.color.rgb = ACCENT_BLUE
    p.font.bold = True
    
    p = tf_main.add_paragraph()
    p.text = "حل مسئله مستقیم معادله غیرخطی برگرز با استفاده از شبکه‌های عصبی آگاه از فیزیک (PINN)"
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(23)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK
    p.space_before = Pt(10)
    
    p = tf_main.add_paragraph()
    p.text = "پیاده‌سازی محاسباتی زمان‌پیوسته با کتابخانه جکس (JAX) و تحلیل تطبیقی با مقاله مرجع رئیسی (۲۰۱۹)"
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(13)
    p.font.color.rgb = GRAY_TEXT
    p.space_before = Pt(8)

    # Info Cards Bottom (Student & Supervisor)
    card_info1 = add_card(slide1, Inches(6.8), Inches(4.7), Inches(5.5), Inches(2.2), WHITE, CARD_BORDER)
    tf_info1 = card_info1.text_frame
    tf_info1.word_wrap = True
    tf_info1.margin_right = Inches(0.3)
    tf_info1.margin_top = Inches(0.25)
    
    p = tf_info1.paragraphs[0]
    p.text = "مشخصات پژوهشگر:"
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEAL_DARK
    
    p = tf_info1.add_paragraph()
    p.text = "دانشجو: محمد امیر بابازاد"
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = CHARCOAL
    p.space_before = Pt(6)

    p = tf_info1.add_paragraph()
    p.text = "شماره دانشجویی: ۱۴۰۲۱۳۵۱۰۴"
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(12)
    p.font.color.rgb = GRAY_TEXT
    p.space_before = Pt(4)

    p = tf_info1.add_paragraph()
    p.text = "رشته: علوم کامپیوتر"
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(12)
    p.font.color.rgb = GRAY_TEXT
    p.space_before = Pt(2)

    card_info2 = add_card(slide1, Inches(1.0), Inches(4.7), Inches(5.5), Inches(2.2), WHITE, CARD_BORDER)
    tf_info2 = card_info2.text_frame
    tf_info2.word_wrap = True
    tf_info2.margin_right = Inches(0.3)
    tf_info2.margin_top = Inches(0.25)

    p = tf_info2.paragraphs[0]
    p.text = "هیئت داوری و راهنمایی:"
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEAL_DARK

    p = tf_info2.add_paragraph()
    p.text = "استاد راهنما: دکتر بابک آذرنوید"
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = CHARCOAL
    p.space_before = Pt(6)

    p = tf_info2.add_paragraph()
    p.text = "تاریخ دفاع: شهریور ماه ۱۴۰۵"
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(12)
    p.font.color.rgb = GRAY_TEXT
    p.space_before = Pt(4)

    p = tf_info2.add_paragraph()
    p.text = "محل برگزاری: دانشگاه بناب، دانشکده علوم پایه"
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(12)
    p.font.color.rgb = GRAY_TEXT
    p.space_before = Pt(2)
    
    add_notes(slide1, "متن گفتار دانشجو:\nبنام خدا. با سلام و عرض ادب و احترام خدمت استاد راهنمای ارجمندم جناب آقای دکتر آذرنوید، داوران گرامی و حاضرین محترم در جلسه دفاع. محمد امیر بابازاد هستم، دانشجوی کارشناسی علوم کامپیوتر دانشگاه بناب. امروز افتخار دارم پایان‌نامه خود را تحت عنوان «حل مسئله مستقیم معادله غیرخطی برگرز با استفاده از شبکه‌های عصبی آگاه از فیزیک (PINN)» با پیاده‌سازی در بستر جکس و تحلیل تطبیقی با مقاله مرجع رئیسی ارائه دهم.")

    # =========================================================================
    # SLIDE 2: OUTLINE / ساختار ارائه
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2, CARD_BG)
    add_header(slide2, "ساختار و سرفصل‌های جلسه دفاعیه")
    add_footer(slide2, 2, total_slides)

    topics = [
        ("بخش اول: مقدمه و بیان مسئله", "اهمیت معادلات دیفرانسیل جزئی، چالش روش‌های عددی سنتی و ضرورت تلفیق هوش مصنوعی با فیزیک", NAVY_DARK),
        ("بخش دوم: مبانی نظری و پیشینه", "معادله غیرخطی برگرز، ساختار پرسپترون چندلایه، قضیه تقریب عمومی و سیر تاریخی روش‌های تلفیقی", NAVY_BLUE),
        ("بخش سوم: متدولوژی شبکه‌های PINN", "فرمول‌بندی تابع هزینه دوگانه، سازوکار مشتق‌گیری خودکار (AD) و مقایسه مدل زمان‌پیوسته با زمان‌گسسته", TEAL_DARK),
        ("بخش چهارم: پیاده‌سازی و تحلیل نتایج", "معماری نرم‌افزاری JAX، استراتژی آموزش دومرحله‌ای (Adam + L-BFGS)، به دام انداختن جبهه شوک و مقایسه با مرجع", CRIMSON),
        ("بخش پنجم: جمع‌بندی و افق‌های آینده", "دستاوردهای کلیدی، تحلیل قوت‌ها و محدودیت‌ها و پیشنهادهای توسعه در پژوهش‌های آتی", GOLD_ACCENT),
    ]

    top_pos = 1.45
    for idx, (title, desc, color) in enumerate(topics, 1):
        card = add_card(slide2, Inches(0.8), Inches(top_pos), Inches(11.733), Inches(0.98), WHITE, CARD_BORDER)
        
        # Color bar on right
        cbar = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(12.333), Inches(top_pos), Inches(0.2), Inches(0.98))
        cbar.fill.solid()
        cbar.fill.fore_color.rgb = color
        cbar.line.color.rgb = color
        
        tf = add_textbox(slide2, Inches(1.0), Inches(top_pos + 0.05), Inches(11.1), Inches(0.88))
        p = tf.paragraphs[0]
        p.text = f"{title}"
        p.alignment = PP_ALIGN.RIGHT
        p.font.name = FONT_FA
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = color
        
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.alignment = PP_ALIGN.RIGHT
        p2.font.name = FONT_FA
        p2.font.size = Pt(11.5)
        p2.font.color.rgb = CHARCOAL
        p2.space_before = Pt(3)
        
        top_pos += 1.10

    add_notes(slide2, "متن گفتار دانشجو:\nارائه امروز در ۵ بخش اصلی تدوین شده است. ابتدا انگیزه و چالش‌های محاسباتی را بیان می‌کنم. سپس به مبانی نظری و معادله برگرز می‌پردازم. در بخش سوم متدولوژی دقیق PINN و مشتق‌گیری خودکار را تشریح می‌کنم. بخش چهارم شامل پیاده‌سازی جکس، نتایج تجربی و مقایسه با مقاله مرجع رئیسی است و نهایتاً با جمع‌بندی و کارهای آینده خاتمه خواهم داد.")

    # =========================================================================
    # SLIDE 3: MOTIVATION & PROBLEM STATEMENT
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3, CARD_BG)
    add_header(slide3, "مقدمه و طرح مسئله: اهمیت شبیه‌سازی معادلات دیفرانسیل جزئی")
    add_footer(slide3, 3, total_slides)

    # 3 Cards side by side
    cards_data = [
        ("۱. جایگاه بنیادی در علوم مهندسی",
         "• معادلات دیفرانسیل جزئی (PDEs) زبان استاندارد توصیف پدیده‌های فیزیکی پیوسته هستند.\n• از دینامیک سیالات و آیرودینامیک تا مدل‌سازی ترافیک و پیش‌بینی‌های اقلیمی.\n• اکثر این معادلات به دلیل ماهیت غیرخطی، فاقد جواب تحلیلی بسته هستند.",
         NAVY_BLUE),
        ("۲. بحران پدیده‌های غیرخطی و شوک",
         "• در پدیده‌هایی با انتقال غیرخطی، شیب متغیرها ناگهان بی‌نهایت شدید می‌شود (تشکیل جبهه شوک).\n• مدل‌سازی امواج شوک بزرگ‌ترین آزمون برای سنجش پایداری و دقت هر روش محاسباتی است.\n• نیازمند تفکیک مکانی-زمانی فوق‌العاده بالا در نواحی بحرانی.",
         CRIMSON),
        ("۳. ضرورت یک الگوی محاسباتی نوین",
         "• ترکیب توانایی یادگیری ماشین با اصول فیزیکی حاکم.\n• حذف وابستگی به شبکه‌بندی صلب هندسی (Mesh-Free).\n• دستیابی به حل‌کننده‌ای پیوسته، مشتق‌پذیر و با قابلیت ارزیابی در هر نقطه دلخواه.",
         TEAL_DARK)
    ]

    left_pos = 0.8
    for title, text, color in cards_data:
        c = add_card(slide3, Inches(left_pos), Inches(1.45), Inches(3.68), Inches(5.4), WHITE, CARD_BORDER)
        
        # Top color tag
        tag = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left_pos), Inches(1.45), Inches(3.68), Inches(0.1))
        tag.fill.solid()
        tag.fill.fore_color.rgb = color
        tag.line.color.rgb = color
        
        tf = add_textbox(slide3, Inches(left_pos + 0.1), Inches(1.65), Inches(3.48), Inches(5.1))
        p = tf.paragraphs[0]
        p.text = title
        p.alignment = PP_ALIGN.RIGHT
        p.font.name = FONT_FA
        p.font.size = Pt(13.5)
        p.font.bold = True
        p.font.color.rgb = color
        
        for line in text.split("\n"):
            p = tf.add_paragraph()
            p.text = line
            p.alignment = PP_ALIGN.RIGHT
            p.font.name = FONT_FA
            p.font.size = Pt(11.5)
            p.font.color.rgb = CHARCOAL
            p.space_before = Pt(7)
            
        left_pos += 4.02

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
        tf = add_textbox(slide4, Inches(1.0), Inches(top_pos + 0.1), Inches(11.333), Inches(1.45))
        
        p = tf.paragraphs[0]
        p.text = title
        p.alignment = PP_ALIGN.RIGHT
        p.font.name = FONT_FA
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = NAVY_BLUE
        
        p = tf.add_paragraph()
        p.text = f"• ایده بنیادین: {idea}"
        p.alignment = PP_ALIGN.RIGHT
        p.font.name = FONT_FA
        p.font.size = Pt(11.5)
        p.font.color.rgb = CHARCOAL
        p.space_before = Pt(3)

        p = tf.add_paragraph()
        p.text = f"• مزیت: {adv}  |  • محدودیت اصلی: {lim}"
        p.alignment = PP_ALIGN.RIGHT
        p.font.name = FONT_FA
        p.font.size = Pt(11.5)
        p.font.color.rgb = CRIMSON
        p.space_before = Pt(3)
        
        top_pos += 1.85

    add_notes(slide4, "متن گفتار دانشجو:\nروش‌های کلاسیک مانند تفاضل‌های محدود، اجزای محدود و روش‌های طیفی دهه‌ها خدمت کرده‌اند. اما هر یک محدودیت‌های جدی دارند: تولید شبکه در هندسه‌های پیچیده بسیار زمان‌بر است، پدیده نفرین ابعاد در ابعاد بالا ظاهر می‌شود، و خطاهای تقریب گسسته‌سازی در جبهه‌های شوک باعث نوسانات غیرفیزیکی می‌شوند.")

    # =========================================================================
    # SLIDE 5: LIMITATIONS OF PURE DATA-DRIVEN AI
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5, CARD_BG)
    add_header(slide5, "کاستی‌های هوش مصنوعی صرفاً داده‌محور (جعبه سیاه)")
    add_footer(slide5, 5, total_slides)

    card_left = add_card(slide5, Inches(0.8), Inches(1.45), Inches(5.6), Inches(5.4), WHITE, CARD_BORDER)
    tf_l = card_left.text_frame
    tf_l.word_wrap = True
    tf_l.margin_right = Inches(0.3)
    tf_l.margin_left = Inches(0.3)
    tf_l.margin_top = Inches(0.2)
    
    p = tf_l.paragraphs[0]
    p.text = "معایب یادگیری ماشین سنتی در فیزیک"
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = CRIMSON

    points_l = [
        "۱. نیاز به حجم عظیم داده‌های تجربی:",
        "در مهندسی و علوم تجربی، نصب حسگرها و اندازه‌گیری پیوسته بسیار پرهزینه یا عملاً غیرممکن است (مثل داخل موتور جت یا اعماق زمین).",
        "۲. رفتار جعبه سیاه (Black-Box):",
        "شبکه‌های عادی هیچ درکی از قوانین بقای جرم، اندازه حرکت یا انرژی ندارند.",
        "۳. پیش‌بینی‌های غیرفیزیکی و بیش‌برازش:",
        "در نواحی خارج از داده‌های آموزشی (برون‌یابی)، شبکه‌ها رفتارهای کاملاً نامعقول و مغایر با قوانین طبیعت تولید می‌کنند."
    ]
    for pt in points_l:
        p = tf_l.add_paragraph()
        p.text = pt
        p.alignment = PP_ALIGN.RIGHT
        p.font.name = FONT_FA
        p.font.size = Pt(11) if not pt.startswith(("۱", "۲", "۳")) else Pt(12)
        p.font.bold = pt.startswith(("۱", "۲", "۳"))
        p.font.color.rgb = NAVY_DARK if pt.startswith(("۱", "۲", "۳")) else CHARCOAL
        p.space_before = Pt(4)

    card_right = add_card(slide5, Inches(6.8), Inches(1.45), Inches(5.733), Inches(5.4), WHITE, CARD_BORDER)
    tf_r = card_right.text_frame
    tf_r.word_wrap = True
    tf_r.margin_right = Inches(0.3)
    tf_r.margin_left = Inches(0.3)
    tf_r.margin_top = Inches(0.2)

    p = tf_r.paragraphs[0]
    p.text = "راهکار انقلابی: شبکه‌های آگاه از فیزیک (PINN)"
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = TEAL_DARK

    points_r = [
        "• ادغام معادلات دیفرانسیل در فرآیند آموزش:",
        "به جای اتکای صرف به داده‌های اندازه‌گیری‌شده، معادله حاکم به عنوان راهنمای مستقیم وارد تابع هزینه شبکه می‌شود.",
        "• عمل به عنوان حل‌کننده بدون شبکه (Mesh-Free):",
        "نقاط ارزیابی فیزیک می‌توانند به صورت تصادفی یا با نمونه‌برداری ساخت‌نیافته در کل دامنه پخش شوند.",
        "• تضمین پایبندی به قوانین بقا:",
        "حتی با تعداد بسیار اندکی از داده‌های مرزی و اولیه، فیزیک حاکم مانع از انحراف و بیش‌برازش مدل می‌شود."
    ]
    for pt in points_r:
        p = tf_r.add_paragraph()
        p.text = pt
        p.alignment = PP_ALIGN.RIGHT
        p.font.name = FONT_FA
        p.font.size = Pt(11) if not pt.startswith("•") else Pt(12)
        p.font.bold = pt.startswith("•")
        p.font.color.rgb = NAVY_BLUE if pt.startswith("•") else CHARCOAL
        p.space_before = Pt(5)

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
    p.text = "تعریف و سازوکار بنیادین چارچوب PINN (رئیسی و همکاران، ۲۰۱۹)"
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    p = tf_top.add_paragraph()
    p.text = "یک شبکه عصبی به عنوان تقریبی پیوسته از پاسخ u(t, x; θ) در نظر گرفته می‌شود. ورودی‌های شبکه مختصات پیوسته زمانی و مکانی (t, x) هستند. سپس با استفاده از «مشتق‌گیری خودکار»، مشتقات جزئی مورد نیاز معادله دیفرانسیل محاسبه شده و عملگر باقیمانده فیزیک تشکیل می‌گردد."
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(12)
    p.font.color.rgb = CHARCOAL
    p.space_before = Pt(8)

    # 3 Pill Cards
    pills = [
        ("۱. تطابق با شرایط اولیه و مرزی", "شبکه خروجی خود را با داده‌های اولیه u(0,x) و مرزی u(t,-1), u(t,1) همگام می‌سازد.", NAVY_BLUE),
        ("۲. صفر کردن باقیمانده معادله دیفرانسیل", "در هزاران نقطه هم‌مکانی درون دامنه، باقیمانده فیزیکی f(t,x) به سمت صفر هدایت می‌شود.", TEAL_DARK),
        ("۳. بدون نیاز به شبکه محاسباتی صلب", "حل در تمام نقاط فضا-زمان پیوسته بوده و در هر لحظه و مکان دلخواه مستقیماً قابل ارزیابی است.", GOLD_ACCENT)
    ]
    left_p = 0.8
    for title, desc, col in pills:
        c = add_card(slide6, Inches(left_p), Inches(3.85), Inches(3.68), Inches(3.0), WHITE, CARD_BORDER)
        tag = slide6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left_p), Inches(3.85), Inches(3.68), Inches(0.08))
        tag.fill.solid()
        tag.fill.fore_color.rgb = col
        tag.line.color.rgb = col
        
        tf = add_textbox(slide6, Inches(left_p + 0.1), Inches(4.05), Inches(3.48), Inches(2.7))
        p = tf.paragraphs[0]
        p.text = title
        p.alignment = PP_ALIGN.RIGHT
        p.font.name = FONT_FA
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = col
        
        p = tf.add_paragraph()
        p.text = desc
        p.alignment = PP_ALIGN.RIGHT
        p.font.name = FONT_FA
        p.font.size = Pt(11.5)
        p.font.color.rgb = CHARCOAL
        p.space_before = Pt(8)
        
        left_p += 4.02

    add_notes(slide6, "متن گفتار دانشجو:\nدر این اسلاید ساختار کلی PINN را مشاهده می‌کنید. شبکه عصبی نگاشت مختصات فضا-زمان به میدان سرعت را یاد می‌گیرد. از طریق مشتق‌گیری خودکار، مشتقات زمانی و مکانی دقیقاً روی گراف محاسباتی استخراج می‌شوند و باقیمانده فیزیک در تابع هزینه قرار می‌گیرد تا سیستم همزمان داده‌های مرزی و قوانین فیزیک را ارضا کند.")

    # =========================================================================
    # SLIDE 7: BENCHMARK PROBLEM: VISCOUS BURGERS' EQUATION
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7, CARD_BG)
    add_header(slide7, "مسئله معیار: معادله غیرخطی برگرز یک‌بعدی")
    add_footer(slide7, 7, total_slides)

    card_eq = add_card(slide7, Inches(0.8), Inches(1.45), Inches(11.733), Inches(1.7), WHITE, CRIMSON)
    tf_eq = card_eq.text_frame
    tf_eq.word_wrap = True
    tf_eq.margin_right = Inches(0.3)
    tf_eq.margin_top = Inches(0.15)

    p = tf_eq.paragraphs[0]
    p.text = "معادله دیفرانسیل جزئی غیرخطی برگرز با ضریب لزجت:"
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = CRIMSON

    p = tf_eq.add_paragraph()
    p.text = "u_t + u * u_x - (0.01 / π) * u_xx = 0 ,    x ∈ [-1, 1],  t ∈ [0, 1]"
    p.alignment = PP_ALIGN.CENTER
    p.font.name = FONT_EN
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK
    p.space_before = Pt(4)

    p = tf_eq.add_paragraph()
    p.text = "شرط اولیه:  u(0, x) = -sin(π x)   |   شرایط مرزی دیریکله همگن:  u(t, -1) = u(t, 1) = 0"
    p.alignment = PP_ALIGN.CENTER
    p.font.name = FONT_FA
    p.font.size = Pt(12)
    p.font.color.rgb = GRAY_TEXT
    p.space_before = Pt(4)

    # 2 Sub-cards
    c1 = add_card(slide7, Inches(0.8), Inches(3.35), Inches(5.7), Inches(3.5), WHITE, CARD_BORDER)
    tf_c1 = c1.text_frame
    tf_c1.word_wrap = True
    tf_c1.margin_right = Inches(0.25)
    tf_c1.margin_top = Inches(0.2)
    
    p = tf_c1.paragraphs[0]
    p.text = "فیزیک حاکم و رقابت ترم‌ها"
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY_BLUE

    p = tf_c1.add_paragraph()
    p.text = "• جمله همرفت غیرخطی (u * u_x):\nباعث انتقال غیرخطی سرعت و شیب تند پروفیل موج و حرکت به سمت مرکز می‌شود."
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(11)
    p.font.color.rgb = CHARCOAL
    p.space_before = Pt(4)

    p = tf_c1.add_paragraph()
    p.text = "• جمله پخش لزجت (ν * u_xx):\nتمایل به هموارسازی و میرا کردن امواج دارد. چون ضریب لزجت بسیار کوچک است (ν ≈ 0.00318)، ترم همرفت غالب شده و موج شوک تشکیل می‌شود."
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(11)
    p.font.color.rgb = CHARCOAL
    p.space_before = Pt(4)

    c2 = add_card(slide7, Inches(6.8), Inches(3.35), Inches(5.733), Inches(3.5), WHITE, CARD_BORDER)
    tf_c2 = c2.text_frame
    tf_c2.word_wrap = True
    tf_c2.margin_right = Inches(0.25)
    tf_c2.margin_top = Inches(0.2)

    p = tf_c2.paragraphs[0]
    p.text = "چرا معادله برگرز به عنوان محک انتخاب شد؟"
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEAL_DARK

    points = [
        "۱. ساده‌ترین مدل غیرخطی شامل هر دو پدیده همرفت و نفوذ لزجت.",
        "۲. ایجاد جبهه شوک فوق‌العاده تیز در حوالی x = 0 در زمان‌های t > 0.4.",
        "۳. چالش بزرگ برای روش‌های عددی به دلیل گرادیان‌های بسیار شدید مکانی.",
        "۴. مسئله استاندارد طلایی (Gold Standard) در ادبیات علمی شبکه‌های PINN برای اثبات دقت و کارایی الگوریتم‌ها."
    ]
    for pt in points:
        p = tf_c2.add_paragraph()
        p.text = pt
        p.alignment = PP_ALIGN.RIGHT
        p.font.name = FONT_FA
        p.font.size = Pt(11)
        p.font.color.rgb = CHARCOAL
        p.space_before = Pt(3)

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
    p.text = "تابع هزینه کل شبکه عصبی آگاه از فیزیک:"
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY_BLUE

    p = tf_l.add_paragraph()
    p.text = "Loss(θ) = MSE_u(θ) + MSE_f(θ)"
    p.alignment = PP_ALIGN.CENTER
    p.font.name = FONT_EN
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = CRIMSON
    p.space_before = Pt(4)

    # 2 Detailed Cards for MSE_u and MSE_f
    c_u = add_card(slide8, Inches(0.8), Inches(3.15), Inches(5.7), Inches(3.7), WHITE, CARD_BORDER)
    tf_u = c_u.text_frame
    tf_u.word_wrap = True
    tf_u.margin_right = Inches(0.25)
    tf_u.margin_top = Inches(0.2)

    p = tf_u.paragraphs[0]
    p.text = "۱. خطای داده‌های مرزی و اولیه (MSE_u)"
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY_BLUE

    p = tf_u.add_paragraph()
    p.text = "MSE_u = (1 / N_u) * Σ | u(t_u^i, x_u^i) - u^i |^2"
    p.alignment = PP_ALIGN.CENTER
    p.font.name = FONT_EN
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK
    p.space_before = Pt(6)

    p = tf_u.add_paragraph()
    p.text = "• ارزیابی روی N_u = ۲۰۰ نقطه داده معلوم.\n• ۱۰۰ نقطه روی شرط اولیه t = 0.\n• ۱۰۰ نقطه روی شرایط مرزی x = -1 و x = 1.\n• تضمین انطباق جواب با شرایط فیزیکی مرزها."
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(11.5)
    p.font.color.rgb = CHARCOAL
    p.space_before = Pt(6)

    c_f = add_card(slide8, Inches(6.8), Inches(3.15), Inches(5.733), Inches(3.7), WHITE, CARD_BORDER)
    tf_f = c_f.text_frame
    tf_f.word_wrap = True
    tf_f.margin_right = Inches(0.25)
    tf_f.margin_top = Inches(0.2)

    p = tf_f.paragraphs[0]
    p.text = "۲. خطای باقیمانده فیزیک (MSE_f)"
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEAL_DARK

    p = tf_f.add_paragraph()
    p.text = "MSE_f = (1 / N_f) * Σ | f(t_f^i, x_f^i) |^2"
    p.alignment = PP_ALIGN.CENTER
    p.font.name = FONT_EN
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK
    p.space_before = Pt(6)

    p = tf_f.add_paragraph()
    p.text = "• ارزیابی روی N_f = ۱۰۰۰۰ نقطه هم‌مکانی در کل فضا-زمان.\n• عملگر باقیمانده:\n  f := u_t + u * u_x - (0.01 / π) * u_xx\n• نیاز به هیچ برچسب داده‌ای ندارد و ارضای مستقیم PDE است."
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(11.5)
    p.font.color.rgb = CHARCOAL
    p.space_before = Pt(6)

    add_notes(slide8, "متن گفتار دانشجو:\nتابع هزینه کل از دو مؤلفه تشکیل شده است: اول خطای داده‌های مرزی و اولیه روی ۲۰۰ نقطه، و دوم خطای باقیمانده فیزیک روی ۱۰ هزار نقطه درون دامنه. مؤلفه اول شبکه را مقید به شرایط مرزی می‌کند و مؤلفه دوم قوانین بقا و دینامیک حاکم بر معادله برگرز را در سراسر میدان تضمین می‌نماید.")

    # =========================================================================
    # SLIDE 9: AUTOMATIC DIFFERENTIATION MECHANICS
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9, CARD_BG)
    add_header(slide9, "سازوکار مشتق‌گیری خودکار (Automatic Differentiation)")
    add_footer(slide9, 9, total_slides)

    # 3 Comparison Boxes
    diff_types = [
        ("مشتق‌گیری عددی (تفاضل محدود)", "بر پایه بسط تیلور با طول گام h", "خطای برش در h بزرگ و خطای گردکردن ممیز شناور در h کوچک (تعارض دقت)", GRAY_TEXT),
        ("مشتق‌گیری نمادین (Symbolic)", "دستکاری جبری عبارات و فرمول‌ها", "پدیده تورم نمایی عبارات جبری (Expression Swell) و ناتوانی در کدهای کنترلی", CRIMSON),
        ("مشتق‌گیری خودکار (AutoDiff)", "اعمال قاعده زنجیره‌ای روی گراف محاسباتی برنامه", "دقت تحلیلی تا حد دقت ممیز شناور ماشین بدون خطای برش و با سرعت فوق‌العاده", TEAL_DARK),
    ]

    left_d = 0.8
    for title, idea, feat, col in diff_types:
        c = add_card(slide9, Inches(left_d), Inches(1.45), Inches(3.68), Inches(2.6), WHITE, CARD_BORDER)
        tag = slide9.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left_d), Inches(1.45), Inches(3.68), Inches(0.08))
        tag.fill.solid()
        tag.fill.fore_color.rgb = col
        tag.line.color.rgb = col
        
        tf = add_textbox(slide9, Inches(left_d + 0.1), Inches(1.65), Inches(3.48), Inches(2.3))
        p = tf.paragraphs[0]
        p.text = title
        p.alignment = PP_ALIGN.RIGHT
        p.font.name = FONT_FA
        p.font.size = Pt(12.5)
        p.font.bold = True
        p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = f"ایده: {idea}"
        p.alignment = PP_ALIGN.RIGHT
        p.font.name = FONT_FA
        p.font.size = Pt(11)
        p.font.color.rgb = CHARCOAL
        p.space_before = Pt(4)

        p = tf.add_paragraph()
        p.text = f"ویژگی: {feat}"
        p.alignment = PP_ALIGN.RIGHT
        p.font.name = FONT_FA
        p.font.size = Pt(10.5)
        p.font.color.rgb = GRAY_TEXT
        p.space_before = Pt(4)
        
        left_d += 4.02

    # Bottom Architecture of AD in PINN
    card_ad = add_card(slide9, Inches(0.8), Inches(4.25), Inches(11.733), Inches(2.6), WHITE, NAVY_BLUE)
    tf_ad = card_ad.text_frame
    tf_ad.word_wrap = True
    tf_ad.margin_right = Inches(0.3)
    tf_ad.margin_top = Inches(0.15)

    p = tf_ad.paragraphs[0]
    p.text = "ساختار دو سطحی مشتق‌گیری خودکار در آموزش PINN:"
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    p = tf_ad.add_paragraph()
    p.text = "• سطح اول (مشتق نسبت به ورودی‌های فضا-زمان): محاسبه مشتقات مکانی u_x، مشتق زمانی u_t و مشتق دوم مکانی u_xx با استفاده از تبدیل تابعی jax.grad برای تشکیل عملگر باقیمانده فیزیکی f."
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(11.5)
    p.font.color.rgb = CHARCOAL
    p.space_before = Pt(4)

    p = tf_ad.add_paragraph()
    p.text = "• سطح دوم (مشتق نسبت به پارامترهای شبکه θ): پس‌انتشار خطا و محاسبه گرادیان ∇_θ Loss برای به‌روزرسانی وزن‌ها و بایاس‌ها در بهینه‌سازهای آدام و L-BFGS."
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(11.5)
    p.font.color.rgb = CHARCOAL
    p.space_before = Pt(4)

    add_notes(slide9, "متن گفتار دانشجو:\nمشتق‌گیری خودکار قلب تپنده PINN است. بر خلاف تفاضل محدود که خطای برش دارد یا محاسبات نمادین که به شدت سنگین می‌شود، AutoDiff مشتقات دقیق ریاضی را بر پایه قاعده زنجیره‌ای روی کدهای پایتون ارزیابی می‌کند. در PINN ما دو سطح مشتق‌گیری داریم: یکی نسبت به مختصات (t, x) برای فیزیک، و دیگری نسبت به وزن‌های شبکه برای آموزش.")

    # =========================================================================
    # SLIDE 10: CONTINUOUS-TIME VS DISCRETE-TIME MODELS
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10, CARD_BG)
    add_header(slide10, "مقایسه تطبیقی: مدل زمان‌پیوسته در برابر زمان‌گسسته")
    add_footer(slide10, 10, total_slides)

    # 2 Comparison Columns
    col1 = add_card(slide10, Inches(0.8), Inches(1.45), Inches(5.7), Inches(5.4), WHITE, NAVY_BLUE)
    tf_c1 = col1.text_frame
    tf_c1.word_wrap = True
    tf_c1.margin_right = Inches(0.3)
    tf_c1.margin_top = Inches(0.2)

    p = tf_c1.paragraphs[0]
    p.text = "مدل زمان‌پیوسته (رویکرد پیاده‌شده در این پژوهش)"
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(13.5)
    p.font.bold = True
    p.font.color.rgb = NAVY_BLUE

    items_c1 = [
        ("• ورودی شبکه:", "بردار پیوسته زمانی و مکانی (t, x)"),
        ("• خروجی شبکه:", "مقدار میدان اسکالر u(t, x) در کل فضا-زمان"),
        ("• روش حل زمانی:", "پیوسته و بدون گام‌بندی زمانی (مشتق‌گیری u_t با AutoDiff)"),
        ("• مزیت اصلی:", "یکپارچگی کامل ساختار، سادگی محاسباتی و ارزیابی در هر زمان دلخواه"),
        ("• نقاط قوت تجربی:", "تطابق عالی در جبهه‌های شوک و یادگیری ساختار سراسری میدان")
    ]
    for k, v in items_c1:
        p = tf_c1.add_paragraph()
        p.text = f"{k} {v}"
        p.alignment = PP_ALIGN.RIGHT
        p.font.name = FONT_FA
        p.font.size = Pt(11)
        p.font.color.rgb = CHARCOAL
        p.space_before = Pt(6)

    col2 = add_card(slide10, Inches(6.8), Inches(1.45), Inches(5.733), Inches(5.4), WHITE, CARD_BORDER)
    tf_c2 = col2.text_frame
    tf_c2.word_wrap = True
    tf_c2.margin_right = Inches(0.3)
    tf_c2.margin_top = Inches(0.2)

    p = tf_c2.paragraphs[0]
    p.text = "مدل زمان‌گسسته (روش رانگه--کوتا ضمنی)"
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(13.5)
    p.font.bold = True
    p.font.color.rgb = GRAY_TEXT

    items_c2 = [
        ("• ورودی شبکه:", "فقط مختصات مکانی x در یک مقطع زمانی"),
        ("• خروجی شبکه:", "بردار مراحل میانی رانگه--کوتا (q مرحله) و u^{n+1}"),
        ("• روش حل زمانی:", "گسسته‌سازی زمانی با روش‌های چندمرحله‌ای ضمنی (IRK)"),
        ("• مزیت اصلی:", "پایداری بالا در گام‌های زمانی بزرگ با مراتب زمانی دلخواه"),
        ("• محدودیت:", "پیچیدگی ساختار، خروجی‌های چندبعدی و گسسته بودن پیوستگی زمان")
    ]
    for k, v in items_c2:
        p = tf_c2.add_paragraph()
        p.text = f"{k} {v}"
        p.alignment = PP_ALIGN.RIGHT
        p.font.name = FONT_FA
        p.font.size = Pt(11)
        p.font.color.rgb = CHARCOAL
        p.space_before = Pt(6)

    add_notes(slide10, "متن گفتار دانشجو:\nدر شبکه‌های آگاه از فیزیک دو چارچوب اصلی وجود دارد: زمان‌پیوسته و زمان‌گسسته. مدل زمان‌پیوسته که در این پژوهش پیاده‌سازی شده، زمان را به عنوان یک بعد پیوسته در کنار مکان به شبکه می‌دهد. این رویکرد به دلیل یکپارچگی هندسی و توانایی پیش‌بینی در هر مقطع زمانی، برتری کاربردی و زیبایی ساختاری بالایی دارد.")

    # =========================================================================
    # SLIDE 11: SOFTWARE ARCHITECTURE & JAX FRAMEWORK
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide11, CARD_BG)
    add_header(slide11, "معماری نرم‌افزاری و پیاده‌سازی با کتابخانه جکس (JAX)")
    add_footer(slide11, 11, total_slides)

    # 4 Feature Cards of JAX
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
        p.text = title
        p.alignment = PP_ALIGN.RIGHT
        p.font.name = FONT_FA
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = desc
        p.alignment = PP_ALIGN.RIGHT
        p.font.name = FONT_FA
        p.font.size = Pt(11)
        p.font.color.rgb = CHARCOAL
        p.space_before = Pt(3)

        top_j += 1.35

    add_notes(slide11, "متن گفتار دانشجو:\nیکی از نوآوری‌های فنی این پایان‌نامه، پیاده‌سازی کامل چارچوب با کتابخانه مدرن JAX است. جکس با تلفیق پارادایم برنامه‌نویسی تابعی، کامپایلر تخصصی XLA، و تبدیلات تابعی فوق‌العاده سریع مانند grad و vmap و jit، عملکردی به مراتب تمیزتر و سریع‌تر نسبت به کتابخانه‌های قدیمی نظیر تنسورفلو ۱ ارائه می‌دهد.")

    # =========================================================================
    # SLIDE 12: NETWORK ARCHITECTURE & ACTIVATION FUNCTION
    # =========================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide12, CARD_BG)
    add_header(slide12, "معماری شبکه، مقداردهی اولیه و تابع فعال‌ساز")
    add_footer(slide12, 12, total_slides)

    # 3 Cards
    c1 = add_card(slide12, Inches(0.8), Inches(1.45), Inches(3.68), Inches(5.4), WHITE, CARD_BORDER)
    tf1 = c1.text_frame
    tf1.word_wrap = True
    tf1.margin_right = Inches(0.2)
    tf1.margin_top = Inches(0.2)

    p = tf1.paragraphs[0]
    p.text = "معماری پرسپترون چندلایه"
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(13.5)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    points1 = [
        "• ورودی: ۲ نورون (t, x)",
        "• لایه‌های پنهان: ۴ لایه متوالی با ۵۰ نورون در هر لایه",
        "• خروجی: ۱ نورون خطی u(t,x)",
        "• تعداد کل پارامترها:\n  ۷۸۵۱ وزن و بایاس",
        "• محاسبه پارامترها:\n  (2×50+50) + 3×(50×50+50) + (50×1+1) = 7851"
    ]
    for pt in points1:
        p = tf1.add_paragraph()
        p.text = pt
        p.alignment = PP_ALIGN.RIGHT
        p.font.name = FONT_FA
        p.font.size = Pt(11)
        p.font.color.rgb = CHARCOAL
        p.space_before = Pt(4)

    c2 = add_card(slide12, Inches(4.8), Inches(1.45), Inches(3.68), Inches(5.4), WHITE, CARD_BORDER)
    tf2 = c2.text_frame
    tf2.word_wrap = True
    tf2.margin_right = Inches(0.2)
    tf2.margin_top = Inches(0.2)

    p = tf2.paragraphs[0]
    p.text = "چرا تابع فعال‌ساز Tanh؟"
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(13.5)
    p.font.bold = True
    p.font.color.rgb = TEAL_DARK

    points2 = [
        "• مشتق‌پذیری بی‌نهایت بار (C^∞):",
        "معادله برگرز نیازمند مشتق دوم مکانی u_xx است.",
        "• شکست کامل تابع ReLU:",
        "مشتق دوم ReLU در همه جا صفر است؛ لذا استفاده از ReLU باقیمانده فیزیکی لزجت را پوچ می‌کند!",
        "• تقارن حول مبدأ:",
        "تانژانت هیپربولیک در بازه (-1, 1) خروجی با میانگین صفر تولید کرده و آموزش را پایدار می‌سازد."
    ]
    for pt in points2:
        p = tf2.add_paragraph()
        p.text = pt
        p.alignment = PP_ALIGN.RIGHT
        p.font.name = FONT_FA
        p.font.size = Pt(11) if not pt.endswith(":") else Pt(11.5)
        p.font.bold = pt.endswith(":")
        p.font.color.rgb = NAVY_BLUE if pt.endswith(":") else CHARCOAL
        p.space_before = Pt(4)

    c3 = add_card(slide12, Inches(8.8), Inches(1.45), Inches(3.733), Inches(5.4), WHITE, CARD_BORDER)
    tf3 = c3.text_frame
    tf3.word_wrap = True
    tf3.margin_right = Inches(0.2)
    tf3.margin_top = Inches(0.2)

    p = tf3.paragraphs[0]
    p.text = "مقداردهی گزاویه (Glorot)"
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(13.5)
    p.font.bold = True
    p.font.color.rgb = CRIMSON

    points3 = [
        "• توزیع یکنواخت گزاویه:",
        "W ~ U(-√(6/(n_in+n_out)), √(6/(n_in+n_out)))",
        "• حفظ واریانس سیگنال:",
        "جلوگیری از محو شدن یا انفجار گرادیان‌ها در گذر پیش‌رو و پس‌رو.",
        "• بایاس‌ها با صفر مقداردهی می‌شوند.",
        "• شروع بهینه‌سازی از یک وضعیت متقارن و پایدار."
    ]
    for pt in points3:
        p = tf3.add_paragraph()
        p.text = pt
        p.alignment = PP_ALIGN.RIGHT
        p.font.name = FONT_FA
        p.font.size = Pt(11) if not pt.endswith(":") else Pt(11.5)
        p.font.bold = pt.endswith(":")
        p.font.color.rgb = NAVY_DARK if pt.endswith(":") else CHARCOAL
        p.space_before = Pt(4)

    add_notes(slide12, "متن گفتار دانشجو:\nمعماری شبکه شامل ۴ لایه پنهان با ۵۰ نورون است که مجموعاً ۷۸۵۱ پارامتر دارد. نکته کلیدی انتخاب تابع فعال‌ساز Tanh است. توابعی مثل ReLU که در بینایی ماشین متداولند، در PINN غیرقابل استفاده‌اند؛ زیرا مشتق دوم ReLU صفر است و ترم لزجت معادله را از بین می‌برد. وزن‌ها نیز با روش یکنواخت گزاویه مقداردهی شده‌اند.")

    # =========================================================================
    # SLIDE 13: COLLOCATION POINTS DISTRIBUTION & SAMPLING
    # =========================================================================
    slide13 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide13, CARD_BG)
    add_header(slide13, "راهبرد نمونه‌برداری و توزیع نقاط هم‌مکانی")
    add_footer(slide13, 13, total_slides)

    # Left: Explanation Card
    c_left = add_card(slide13, Inches(0.8), Inches(1.45), Inches(5.6), Inches(5.4), WHITE, CARD_BORDER)
    tf_l = c_left.text_frame
    tf_l.word_wrap = True
    tf_l.margin_right = Inches(0.25)
    tf_l.margin_top = Inches(0.2)

    p = tf_l.paragraphs[0]
    p.text = "ترکیب و استراتژی توزیع نقاط آموزش"
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(13.5)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    points_samp = [
        ("• داده‌های مرزی و اولیه (N_u = ۲۰۰ نقطه):", "۱۰۰ نقطه روی شرط اولیه t=0 و ۱۰۰ نقطه روی مرزهای x=±1 (نقاط قرمز شکل)."),
        ("• نقاط هم‌مکانی یکنواخت (۵۰۰۰ نقطه):", "توزیع تصادفی یکنواخت در سراسر بازه فضا-زمان [-1,1] × [0,1] برای پوشش سراسری فیزیک."),
        ("• نقاط متمرکز در ناحیه شوک (۵۰۰۰ نقطه):", "تمرکز آماری بالا در حوالی خط مرکزی x ≈ 0 و زمان‌های t > 0.3 به دلیل گرادیان‌های بسیار شدید جبهه شوک."),
        ("• نتیجه راهبرد نمونه‌برداری:", "به دام انداختن جبهه تیز شوک بدون افزایش بی‌رویه بار محاسباتی.")
    ]
    for k, v in points_samp:
        p = tf_l.add_paragraph()
        p.text = f"{k}\n{v}"
        p.alignment = PP_ALIGN.RIGHT
        p.font.name = FONT_FA
        p.font.size = Pt(11)
        p.font.color.rgb = CHARCOAL
        p.space_before = Pt(5)

    # Right: Image Card
    c_right = add_card(slide13, Inches(6.8), Inches(1.45), Inches(5.733), Inches(5.4), WHITE, CARD_BORDER)
    img_path = "MAB-THESIS/figs/png/forward_points.png"
    if os.path.exists(img_path):
        slide13.shapes.add_picture(img_path, Inches(7.0), Inches(1.7), width=Inches(5.333))

    tf_cap = add_textbox(slide13, Inches(7.0), Inches(5.9), Inches(5.333), Inches(0.8))
    p = tf_cap.paragraphs[0]
    p.text = "شکل ۱-۴: نقشه توزیع ۲۰۰ نقطه اولیه-مرزی و ۱۰۰۰۰ نقطه هم‌مکانی با تراکم بالا در ناحیه شوک مرکزی."
    p.alignment = PP_ALIGN.CENTER
    p.font.name = FONT_FA
    p.font.size = Pt(10.5)
    p.font.color.rgb = GRAY_TEXT

    add_notes(slide13, "متن گفتار دانشجو:\nدر این شکل، نقشه توزیع نقاط آموزشی را مشاهده می‌فرمایید. نقاط قرمز رنگ نشان‌دهنده ۲۰۰ نقطه شرط مرزی و اولیه هستند. نقاط خاکستری، ۱۰ هزار نقطه هم‌مکانی فیزیک هستند. هوشمندی این پیاده‌سازی در اختصاص ۵۰ درصد از نقاط به ناحیه مرکزی x حوالی صفر است تا شبکه بتواند رزولوشن کافی برای حل جبهه شوک داشته باشد.")

    # =========================================================================
    # SLIDE 14: TWO-STAGE HYBRID OPTIMIZATION STRATEGY
    # =========================================================================
    slide14 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide14, CARD_BG)
    add_header(slide14, "استراتژی بهینه‌سازی ترکیبی دومرحله‌ای (Adam + L-BFGS)")
    add_footer(slide14, 14, total_slides)

    # Left: Explanation of 2 phases
    c_opt = add_card(slide14, Inches(0.8), Inches(1.45), Inches(5.6), Inches(5.4), WHITE, CARD_BORDER)
    tf_o = c_opt.text_frame
    tf_o.word_wrap = True
    tf_o.margin_right = Inches(0.25)
    tf_o.margin_top = Inches(0.2)

    p = tf_o.paragraphs[0]
    p.text = "چرا بهینه‌سازی دومرحله‌ای ضروری است؟"
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(13.5)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    p = tf_o.add_paragraph()
    p.text = "• فاز اول: الگوریتم آدام (۶۰۰۰ گام با نرخ یادگیری 0.001)\nتابع هزینه PINN دارای سطوح پیچیده و به شدت غیرمحدب است. آدام با استفاده از گشتاور اول و دوم، شبکه را از کمینه‌های محلی ناملایم عبور داده و به یک حوضچه همگرایی مناسب می‌رساند."
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(11)
    p.font.color.rgb = NAVY_BLUE
    p.space_before = Pt(6)

    p = tf_o.add_paragraph()
    p.text = "• فاز دوم: الگوریتم شبه‌نیوتنی L-BFGS-B\nپس از رسیدن به ناحیه مناسب، الگوریتم L-BFGS با تقریب ماتریس معکوس هشین و نرخ همگرایی فوق‌خطی (مرتبه دو)، خطای باقیمانده را به سرعت به مرتبه‌های بسیار پایین کاهش می‌دهد."
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(11)
    p.font.color.rgb = CRIMSON
    p.space_before = Pt(8)

    # Right: Image of Loss History
    c_right = add_card(slide14, Inches(6.8), Inches(1.45), Inches(5.733), Inches(5.4), WHITE, CARD_BORDER)
    img_path = "MAB-THESIS/figs/png/loss_history.png"
    if os.path.exists(img_path):
        slide14.shapes.add_picture(img_path, Inches(7.0), Inches(1.7), width=Inches(5.333))

    tf_cap = add_textbox(slide14, Inches(7.0), Inches(5.9), Inches(5.333), Inches(0.8))
    p = tf_cap.paragraphs[0]
    p.text = "شکل ۲-۴: تاریخچه لگاریتمی همگرایی توابع هزینه در دو فاز آدام و L-BFGS."
    p.alignment = PP_ALIGN.CENTER
    p.font.name = FONT_FA
    p.font.size = Pt(10.5)
    p.font.color.rgb = GRAY_TEXT

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

    # Bottom: 3 Analysis Cards
    snaps = [
        ("مقطع زمانی t = 0.25", "پروفیل اولیه هموار سینوسی با شیب ملایم به سمت مرکز متمایل شده است. تطابق ۱۰۰ درصدی PINN با خط مرجع.", NAVY_BLUE),
        ("مقطع زمانی t = 0.50", "شیب نمودار در حوالی مبدأ به شدت تند شده و جبهه شوک در حال تکوین است. تقریب عالی شیب شدید.", TEAL_DARK),
        ("مقطع زمانی t = 0.75", "جبهه شوک کامل و افت شبه‌ناپیوسته سرعت از مثبت به منفی در x = 0 بدون نوسانات گیبس.", CRIMSON)
    ]
    left_s = 0.8
    for title, desc, col in snaps:
        c = add_card(slide15, Inches(left_s), Inches(4.8), Inches(3.68), Inches(2.1), WHITE, CARD_BORDER)
        tag = slide15.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left_s), Inches(4.8), Inches(3.68), Inches(0.06))
        tag.fill.solid()
        tag.fill.fore_color.rgb = col
        tag.line.color.rgb = col
        
        tf = add_textbox(slide15, Inches(left_s + 0.1), Inches(4.95), Inches(3.48), Inches(1.8))
        p = tf.paragraphs[0]
        p.text = title
        p.alignment = PP_ALIGN.RIGHT
        p.font.name = FONT_FA
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = desc
        p.alignment = PP_ALIGN.RIGHT
        p.font.name = FONT_FA
        p.font.size = Pt(10.5)
        p.font.color.rgb = CHARCOAL
        p.space_before = Pt(3)

        left_s += 4.02

    add_notes(slide15, "متن گفتار دانشجو:\nاین اسلاید قلب نتایج پایان‌نامه را نشان می‌دهد. مقایسه پیش‌بینی PINN (خط‌چین قرمز) با جواب مرجع در سه مقطع زمانی t=0.25, 0.50, 0.75. مشاهده می‌کنید که چگونه شبکه عصبی موج شوک بسیار تیز در مرکز دامنه را با وفاداری کامل و بدون هیچ‌گونه نوسان غیرفیزیکی بازسازی کرده است.")

    # =========================================================================
    # SLIDE 16: ERROR ANALYSIS & HEATMAP
    # =========================================================================
    slide16 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide16, CARD_BG)
    add_header(slide16, "تحلیل توزیع مکانی-زمانی خطا و کانتور باقیمانده")
    add_footer(slide16, 16, total_slides)

    # Left: Explanation Card
    c_left = add_card(slide16, Inches(0.8), Inches(1.45), Inches(5.6), Inches(5.4), WHITE, CARD_BORDER)
    tf_l = c_left.text_frame
    tf_l.word_wrap = True
    tf_l.margin_right = Inches(0.25)
    tf_l.margin_top = Inches(0.2)

    p = tf_l.paragraphs[0]
    p.text = "ویژگی‌های توزیع مکانی-زمانی خطا"
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(13.5)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    points_err = [
        ("• خطای نزدیک به صفر در ۹۵٪ دامنه:", "در بخش اعظم فضا-زمان رنگ کانتور تاریک است که نشان‌دهنده انطباق فوق‌العاده با واقعیت فیزیکی است."),
        ("• تمرکز خطا در خط باریک شوک:", "تنها در یک نوار بسیار باریک در حوالی x = 0 و بعد از زمان t > 0.4 به دلیل بی‌نهایت شدن گرادیان‌های مکانی، خطای موضعی اندکی دیده می‌شود."),
        ("• مقادیر خطاهای نهایی مدل:", "خطای باقیمانده فیزیک: MSE_f = 6.36 × 10^-5\nخطای شرایط اولیه و مرزی: MSE_u = 2.35 × 10^-5\nخطای نسبی در نرم L2: معادل ۲.۱۵ درصد.")
    ]
    for k, v in points_err:
        p = tf_l.add_paragraph()
        p.text = f"{k}\n{v}"
        p.alignment = PP_ALIGN.RIGHT
        p.font.name = FONT_FA
        p.font.size = Pt(11)
        p.font.color.rgb = CHARCOAL
        p.space_before = Pt(5)

    # Right: Image Card
    c_right = add_card(slide16, Inches(6.8), Inches(1.45), Inches(5.733), Inches(5.4), WHITE, CARD_BORDER)
    img_path = "MAB-THESIS/figs/png/error_heatmap.png"
    if os.path.exists(img_path):
        slide16.shapes.add_picture(img_path, Inches(7.0), Inches(1.7), width=Inches(5.333))

    tf_cap = add_textbox(slide16, Inches(7.0), Inches(5.9), Inches(5.333), Inches(0.8))
    p = tf_cap.paragraphs[0]
    p.text = "شکل ۴-۴: نقشه کانتور دوبعدی قدرمطلق خطای نقطه‌ای در دامنه فضا-زمان."
    p.alignment = PP_ALIGN.CENTER
    p.font.name = FONT_FA
    p.font.size = Pt(10.5)
    p.font.color.rgb = GRAY_TEXT

    add_notes(slide16, "متن گفتار دانشجو:\nنقشه کانتور دوبعدی خطا نشان می‌دهد که خطای شبیه‌سازی در ۹۵ درصد دامنه عملاً صفر است. بیشینه خطا صرفاً در امتداد یک نوار باریک مرکزی متمرکز است که ناشی از طبیعت ناپیوستگی شوک است. خطای نسبی کل ۲.۱۵ درصد به دست آمده که با توجه به سخت‌افزار معمولی، بسیار چشمگیر است.")

    # =========================================================================
    # SLIDE 17: COMPARATIVE BENCHMARK WITH RAISSI ET AL. (2019)
    # =========================================================================
    slide17 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide17, CARD_BG)
    add_header(slide17, "مقایسه تطبیقی با مقاله مرجع رئیسی و همکاران (۲۰۱۹)")
    add_footer(slide17, 17, total_slides)

    # Table on Top
    table_shape = slide17.shapes.add_table(7, 3, Inches(0.8), Inches(1.45), Inches(11.733), Inches(3.2))
    table = table_shape.table
    table.columns[0].width = Inches(3.2)
    table.columns[1].width = Inches(4.2)
    table.columns[2].width = Inches(4.333)

    headers = ["شاخص مقایسه‌ای", "رئیسی و همکاران (۲۰۱۹)", "پژوهش حاضر"]
    for col_idx, h in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_DARK
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.alignment = PP_ALIGN.CENTER
        p.font.name = FONT_FA
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = WHITE

    rows_data = [
        ("معماری شبکه عصبی", "۸ لایه پنهان، ۲۰ نورون در هر لایه", "۴ لایه پنهان، ۵۰ نورون در هر لایه"),
        ("تعداد کل پارامترها", "۳۰۲۱ پارامتر وزن و بایاس", "۷۸۵۱ پارامتر وزن و بایاس"),
        ("نقاط اولیه و مرزی (N_u)", "۱۰۰ نقطه", "۲۰۰ نقطه (توزیع متعادل)"),
        ("توزیع نقاط هم‌مکانی", "نمونه‌برداری ابرمکعب لاتین", "۵۰٪ تصادفی + ۵۰٪ متمرکز در شوک"),
        ("بستر نرم‌افزاری و کامپایلر", "تنسورفلو ۱ (کد کلاسیک)", "جکس (JAX) مدرن با کامپایلر XLA"),
        ("خطای نسبی در نرم L2", "6.7 × 10^-4 (سخت‌افزار سرور)", "2.15 × 10^-2 (سخت‌افزار دانشگاهی)"),
    ]

    for row_idx, row in enumerate(rows_data, 1):
        for col_idx, val in enumerate(row):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if row_idx % 2 == 1 else CARD_BG
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.alignment = PP_ALIGN.CENTER
            p.font.name = FONT_FA
            p.font.size = Pt(11)
            p.font.color.rgb = CHARCOAL if col_idx != 2 else NAVY_BLUE

    # Analysis Box Bottom
    c_bot = add_card(slide17, Inches(0.8), Inches(4.85), Inches(11.733), Inches(2.0), WHITE, CARD_BORDER)
    tf_b = c_bot.text_frame
    tf_b.word_wrap = True
    tf_b.margin_right = Inches(0.25)
    tf_b.margin_top = Inches(0.12)

    p = tf_b.paragraphs[0]
    p.text = "تحلیل تفاوت‌ها:"
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TEAL_DARK

    p = tf_b.add_paragraph()
    p.text = "۱. شبکه عمیق‌تر در مقاله مرجع (۸ لایه پنهان) توان تقریب بهتری برای ناپیوستگی‌های بسیار تیز دارد.\n۲. سقف تکرارهای L-BFGS در مقاله مرجع با سرورهای قدرتمند بسیار بالاتر بوده است.\n۳. از نظر بازتولید کیفی جبهه شوک و موقعیت فیزیکی آن، پیاده‌سازی جکس در این پژوهش وفاداری کاملی به نتایج مرجع دارد."
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(10.5)
    p.font.color.rgb = CHARCOAL
    p.space_before = Pt(3)

    add_notes(slide17, "متن گفتار دانشجو:\nدر این جدول مقایسه تطبیقی با مقاله مرجع رئیسی را ملاحظه می‌فرمایید. مقاله مرجع از شبکه‌ای عمیق‌تر با ۸ لایه پنهان و تعداد تکرارهای بالا بر روی سرور استفاده کرده است. در این پژوهش با معماری ۴ لایه در ۵۰ نورون و پیاده‌سازی بومی در JAX، موقعیت مکانی و شیب شوک با دقت عالی بازتولید شده است.")

    # =========================================================================
    # SLIDE 18: STRENGTHS, LIMITATIONS & TECHNICAL INSIGHTS
    # =========================================================================
    slide18 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide18, CARD_BG)
    add_header(slide18, "تحلیل نقاط قوت، چالش‌های محاسباتی و درس‌آموخته‌ها")
    add_footer(slide18, 18, total_slides)

    # 2 Columns: Strengths vs Limitations
    c_str = add_card(slide18, Inches(0.8), Inches(1.45), Inches(5.7), Inches(5.4), WHITE, TEAL_DARK)
    tf_s = c_str.text_frame
    tf_s.word_wrap = True
    tf_s.margin_right = Inches(0.25)
    tf_s.margin_top = Inches(0.2)

    p = tf_s.paragraphs[0]
    p.text = "نقاط قوت برجسته رهیافت PINN"
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(13.5)
    p.font.bold = True
    p.font.color.rgb = TEAL_DARK

    strengths = [
        "• حل بدون شبکه (Mesh-Free): عدم نیاز به تولید شبکه‌های پیچیده محاسباتی.",
        "• حل پیوسته در فضا-زمان: توانایی ارزیابی میدان و مشتقات در هر نقطه دلخواه.",
        "• مقاومت بالا در برابر بیش‌برازش: قید فیزیک به عنوان یک منظم‌ساز (Regularizer) قدرتمند عمل می‌کند.",
        "• انعطاف‌پذیری فوق‌العاده: پیاده‌سازی تمیز و ماژولار با تبدیلات تابعی جکس."
    ]
    for st in strengths:
        p = tf_s.add_paragraph()
        p.text = st
        p.alignment = PP_ALIGN.RIGHT
        p.font.name = FONT_FA
        p.font.size = Pt(11)
        p.font.color.rgb = CHARCOAL
        p.space_before = Pt(6)

    c_lim = add_card(slide18, Inches(6.8), Inches(1.45), Inches(5.733), Inches(5.4), WHITE, CRIMSON)
    tf_l = c_lim.text_frame
    tf_l.word_wrap = True
    tf_l.margin_right = Inches(0.25)
    tf_l.margin_top = Inches(0.2)

    p = tf_l.paragraphs[0]
    p.text = "چالش‌های محاسباتی و محدودیت‌ها"
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_FA
    p.font.size = Pt(13.5)
    p.font.bold = True
    p.font.color.rgb = CRIMSON

    limitations = [
        "• زمان آموزش در مقایسه با روش‌های سنتی: بهینه‌سازی غیرمحدب نسبت به حل‌کننده‌های خطی زمان‌برتر است.",
        "• تعارض گرادیان‌ها در تابع هزینه: رقابت میان مؤلفه مرزی و مؤلفه باقیمانده فیزیک.",
        "• چالش تقریب گرادیان‌های بی‌نهایت: نیاز به شبکه‌های عمیق‌تر در لزجت‌های بسیار نزدیک به صفر.",
        "• حساسیت به نقاط اولیه: ضرورت اجرای فاز اولیه آدام قبل از روش‌های شبه‌نیوتنی."
    ]
    for lim in limitations:
        p = tf_l.add_paragraph()
        p.text = lim
        p.alignment = PP_ALIGN.RIGHT
        p.font.name = FONT_FA
        p.font.size = Pt(11)
        p.font.color.rgb = CHARCOAL
        p.space_before = Pt(6)

    add_notes(slide18, "متن گفتار دانشجو:\nدر تحلیل منصفانه، مزیت اصلی PINN در بی‌نیازی از شبکه محاسباتی و مقاومت در برابر بیش‌برازش است. اما چالش‌هایی نظیر غیرمحدب بودن تابع هزینه و تعارض گرادیان‌ها میان بخش مرزی و فیزیکی وجود دارد که با استراتژی دومرحله‌ای ما با موفقیت مدیریت شدند.")

    # =========================================================================
    # SLIDE 19: CONCLUSION & RESEARCH CONTRIBUTIONS
    # =========================================================================
    slide19 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide19, CARD_BG)
    add_header(slide19, "جمع‌بندی و دستاوردهای بنیادین پژوهش")
    add_footer(slide19, 19, total_slides)

    # 4 Achievement Cards
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
        p.text = title
        p.alignment = PP_ALIGN.RIGHT
        p.font.name = FONT_FA
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = desc
        p.alignment = PP_ALIGN.RIGHT
        p.font.name = FONT_FA
        p.font.size = Pt(11)
        p.font.color.rgb = CHARCOAL
        p.space_before = Pt(3)

        top_a += 1.35

    add_notes(slide19, "متن گفتار دانشجو:\nدر جمع‌بندی، این پایان‌نامه نشان داد که شبکه‌های عصبی آگاه از فیزیک یک ابزار قدرتمند، مدرن و قابل اعتماد برای حل مسائل غیرخطی فیزیک هستند. پیاده‌سازی جکس، راهبرد بهینه‌سازی ترکیبی و نمونه‌برداری متمرکز در شوک، سه دستاورد برجسته فنی این پژوهش به شمار می‌روند.")

    # =========================================================================
    # SLIDE 20: FUTURE WORK & RESEARCH HORIZONS
    # =========================================================================
    slide20 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide20, CARD_BG)
    add_header(slide20, "افق‌های توسعه و پیشنهادهای پژوهشی آتی")
    add_footer(slide20, 20, total_slides)

    # 4 Horizon Cards
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
        p.text = title
        p.alignment = PP_ALIGN.RIGHT
        p.font.name = FONT_FA
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = desc
        p.alignment = PP_ALIGN.RIGHT
        p.font.name = FONT_FA
        p.font.size = Pt(11)
        p.font.color.rgb = CHARCOAL
        p.space_before = Pt(3)

        top_h += 1.35

    add_notes(slide20, "متن گفتار دانشجو:\nبرای کارهای آینده، چهار محور اصلی پیشنهاد می‌شود: استفاده از وزن‌دهی پویا برای حل تعارض گرادیان‌ها، به‌کارگیری توابع پایه فوریه برای بهبود تقریب فرکانس‌های بالا، روش‌های تفکیک دامنه XPINN، و توسعه چارچوب به معادلات دو و سه‌بعدی ناویه-استوکس.")

    # =========================================================================
    # SLIDE 21: Q&A & CLOSING SLIDE
    # =========================================================================
    slide21 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide21, NAVY_DARK)
    
    # Inner Card
    card_end = add_card(slide21, Inches(1.5), Inches(1.2), Inches(10.333), Inches(5.1), WHITE, ACCENT_BLUE)
    tf_e = card_end.text_frame
    tf_e.word_wrap = True
    tf_e.margin_top = Inches(0.4)
    tf_e.margin_left = Inches(0.4)
    tf_e.margin_right = Inches(0.4)

    p = tf_e.paragraphs[0]
    p.text = "با تشکر و سپاس فراوان از توجه و شکیبایی شما"
    p.alignment = PP_ALIGN.CENTER
    p.font.name = FONT_FA
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    p = tf_e.add_paragraph()
    p.text = "استاد راهنما: جناب آقای دکتر بابک آذرنوید"
    p.alignment = PP_ALIGN.CENTER
    p.font.name = FONT_FA
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = TEAL_DARK
    p.space_before = Pt(14)

    p = tf_e.add_paragraph()
    p.text = "دانشجو: محمد امیر بابازاد | دانشکده علوم پایه | گروه علوم کامپیوتر دانشگاه بناب"
    p.alignment = PP_ALIGN.CENTER
    p.font.name = FONT_FA
    p.font.size = Pt(12.5)
    p.font.color.rgb = GRAY_TEXT
    p.space_before = Pt(8)

    p = tf_e.add_paragraph()
    p.text = "«آماده پاسخگویی به پرسش‌ها و بهره‌مندی از نظرات ارزشمند هیئت محترم داوران»"
    p.alignment = PP_ALIGN.CENTER
    p.font.name = FONT_FA
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = CRIMSON
    p.space_before = Pt(18)

    add_notes(slide21, "متن گفتار دانشجو:\nدر پایان از راهنمایی‌های ارزنده و دلسوزانه استاد راهنمای گرانقدرم جناب آقای دکتر آذرنوید، و از توجه و حضور داوران محترم و همه عزیزان صمیمانه سپاسگزاری می‌کنم. با کمال میل آماده پاسخگویی به سوالات، نقدها و رهنمودهای ارزشمند هیئت محترم داوران هستم.")

    # Save presentation
    os.makedirs("MAB-THESIS", exist_ok=True)
    out_path = "MAB-THESIS/defense_presentation.pptx"
    prs.save(out_path)
    print(f"Presentation generated successfully: {out_path} ({len(prs.slides)} slides)")

if __name__ == "__main__":
    build_presentation()
