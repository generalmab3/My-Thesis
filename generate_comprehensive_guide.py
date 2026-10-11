#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Professional, Master-level B.Sc. Defense Guide Generator (PDF)
for Mohammad Amir Babazad's Thesis at University of Bonab.
Supervisor: Dr. Babak Azarnavid.
"""

import os
import arabic_reshaper
from bidi.algorithm import get_display

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# -------------------------------------------------------------
# Font Registration & Reshaper Setup
# -------------------------------------------------------------
FONT_REGULAR_PATH = "MAB-THESIS/fonts/Vazirmatn-Regular.ttf"
FONT_BOLD_PATH = "MAB-THESIS/fonts/Vazirmatn-Bold.ttf"

pdfmetrics.registerFont(TTFont("Vazir", FONT_REGULAR_PATH))
pdfmetrics.registerFont(TTFont("Vazir-Bold", FONT_BOLD_PATH))

reshaper = arabic_reshaper.ArabicReshaper(configuration={
    "delete_harakat": True,
    "support_ligatures": True,
})

def fa(text):
    """Shape Persian/Arabic text and reorder for RTL display."""
    if not text:
        return ""
    reshaped = reshaper.reshape(str(text))
    return get_display(reshaped, base_dir="R")

# -------------------------------------------------------------
# Color Constants
# -------------------------------------------------------------
C_NAVY_DARK    = colors.HexColor("#0F2043")
C_NAVY_BLUE    = colors.HexColor("#1A4480")
C_ACCENT_BLUE  = colors.HexColor("#2980B9")
C_TEAL_DARK    = colors.HexColor("#0D6E6E")
C_CRIMSON      = colors.HexColor("#B91C1C")
C_GOLD         = colors.HexColor("#D97706")
C_CHARCOAL     = colors.HexColor("#1E293B")
C_GRAY_TEXT    = colors.HexColor("#475569")
C_LIGHT_BG     = colors.HexColor("#F8FAFC")
C_CARD_BORDER  = colors.HexColor("#E2E8F0")
C_Q_BG         = colors.HexColor("#FEF2F2")
C_Q_BORDER     = colors.HexColor("#FECACA")
C_A_BG         = colors.HexColor("#F0FDF4")
C_A_BORDER     = colors.HexColor("#BBF7D0")
C_CALLOUT_BG   = colors.HexColor("#EFF6FF")
C_CALLOUT_BOR  = colors.HexColor("#BFDBFE")
C_WHITE        = colors.white

# -------------------------------------------------------------
# Numbered Canvas for Total Page Count
# -------------------------------------------------------------
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
        width, height = A4
        margin_x = 36
        
        # Header (Pages 2+)
        if self._pageNumber > 1:
            self.setFont("Vazir", 8.5)
            self.setFillColor(C_GRAY_TEXT)
            self.drawRightString(width - margin_x, height - 26, fa("راهنمای جامع تسلط بر پایان‌نامه و جلسه دفاع | دانشگاه بناب"))
            self.drawString(margin_x, height - 26, fa("محمد امیر بابازاد — استاد راهنما: دکتر بابک آذرنوید"))
            
            self.setStrokeColor(C_CARD_BORDER)
            self.setLineWidth(0.6)
            self.line(margin_x, height - 32, width - margin_x, height - 32)
            
        # Footer (All pages)
        self.setStrokeColor(C_CARD_BORDER)
        self.setLineWidth(0.6)
        self.line(margin_x, 34, width - margin_x, 34)
        
        self.setFont("Vazir", 8.5)
        self.setFillColor(C_GRAY_TEXT)
        self.drawRightString(width - margin_x, 20, fa("پایان‌نامه کارشناسی علوم کامپیوتر — حل معادله برگرز با شبکه آگاه از فیزیک (PINN) در JAX"))
        page_str = fa(f"صفحه {self._pageNumber} از {page_count}")
        self.drawString(margin_x, 20, page_str)

# -------------------------------------------------------------
# PDF Layout & Rendering Engine
# -------------------------------------------------------------
class GuideDoc:
    def __init__(self, filename="MAB-THESIS/Defense_Guide.pdf"):
        self.filename = filename
        self.width, self.height = A4
        self.margin_x = 36
        self.margin_top = 45
        self.margin_bottom = 45
        self.content_width = self.width - 2 * self.margin_x
        self.y = self.height - self.margin_top
        self.c = NumberedCanvas(self.filename, pagesize=A4)

    def check_space(self, required_height):
        """If remaining vertical space is less than required, create a new page."""
        if self.y - required_height < self.margin_bottom:
            self.c.showPage()
            self.y = self.height - self.margin_top

    def new_page(self):
        """Force a new page."""
        self.c.showPage()
        self.y = self.height - self.margin_top

    def wrap_words_to_lines(self, text, font_name, font_size, max_w):
        """Wrap text words so each line fits within max_w width."""
        words = text.split()
        if not words:
            return []
        lines = []
        curr = [words[0]]
        for w in words[1:]:
            test_line = " ".join(curr + [w])
            if pdfmetrics.stringWidth(test_line, font_name, font_size) <= max_w:
                curr.append(w)
            else:
                lines.append(" ".join(curr))
                curr = [w]
        if curr:
            lines.append(" ".join(curr))
        return lines

    def draw_text_block(self, text, font_name="Vazir", font_size=9.5, color=C_CHARCOAL,
                        leading=14.5, max_w=None, align="right", indent=0):
        if max_w is None:
            max_w = self.content_width - indent
        lines = self.wrap_words_to_lines(text, font_name, font_size, max_w)
        for line in lines:
            self.check_space(leading)
            self.c.setFont(font_name, font_size)
            self.c.setFillColor(color)
            if align == "right":
                x_pos = self.width - self.margin_x - indent
                self.c.drawRightString(x_pos, self.y, fa(line))
            elif align == "center":
                x_pos = self.margin_x + (self.content_width / 2.0)
                self.c.drawCentredString(x_pos, self.y, fa(line))
            else:
                x_pos = self.margin_x + indent
                self.c.drawString(x_pos, self.y, fa(line))
            self.y -= leading

    def draw_banner(self, title, subtitle, meta_lines):
        """Draw top banner on cover page."""
        banner_h = 105
        self.check_space(banner_h)
        top_y = self.y
        
        # Outer Card
        self.c.setFillColor(C_NAVY_DARK)
        self.c.roundRect(self.margin_x, top_y - banner_h, self.content_width, banner_h, 6, fill=1, stroke=0)
        
        # Accent Strip
        self.c.setFillColor(C_ACCENT_BLUE)
        self.c.roundRect(self.margin_x, top_y - 8, self.content_width, 8, 3, fill=1, stroke=0)
        
        # Title text
        self.c.setFont("Vazir-Bold", 15)
        self.c.setFillColor(C_WHITE)
        self.c.drawCentredString(self.width / 2.0, top_y - 32, fa(title))
        
        # Subtitle
        self.c.setFont("Vazir", 10.5)
        self.c.setFillColor(colors.HexColor("#CBD5E1"))
        self.c.drawCentredString(self.width / 2.0, top_y - 52, fa(subtitle))
        
        # Meta Strip
        meta_str = " | ".join(meta_lines)
        self.c.setFont("Vazir", 9)
        self.c.setFillColor(C_GOLD)
        self.c.drawCentredString(self.width / 2.0, top_y - 74, fa(meta_str))
        
        tag_str = "راهنمای جامع تسلط و آمادگی کامل برای پاسخ به پرسش‌های هیئت داوران"
        self.c.setFont("Vazir-Bold", 8.5)
        self.c.setFillColor(colors.HexColor("#93C5FD"))
        self.c.drawCentredString(self.width / 2.0, top_y - 92, fa(tag_str))
        
        self.y = top_y - banner_h - 14

    def draw_section_header(self, num_str, title_str, color=C_NAVY_DARK):
        """Draw modern section title bar."""
        header_h = 28
        self.check_space(header_h + 15)
        top_y = self.y
        
        # Background bar
        self.c.setFillColor(C_LIGHT_BG)
        self.c.setStrokeColor(C_CARD_BORDER)
        self.c.setLineWidth(1)
        self.c.roundRect(self.margin_x, top_y - header_h, self.content_width, header_h, 4, fill=1, stroke=1)
        
        # Tag on right
        tag_w = 6
        self.c.setFillColor(color)
        self.c.rect(self.width - self.margin_x - tag_w, top_y - header_h, tag_w, header_h, fill=1, stroke=0)
        
        # Section text
        full_title = f"{num_str}. {title_str}"
        self.c.setFont("Vazir-Bold", 12)
        self.c.setFillColor(color)
        self.c.drawRightString(self.width - self.margin_x - 14, top_y - 19, fa(full_title))
        
        self.y = top_y - header_h - 10

    def draw_callout_box(self, title, text, bg_col=C_CALLOUT_BG, border_col=C_CALLOUT_BOR, title_col=C_NAVY_BLUE):
        """Draw an elegant callout highlight box."""
        pad_x = 12
        pad_y = 10
        inner_w = self.content_width - 2 * pad_x
        
        title_lines = self.wrap_words_to_lines(title, "Vazir-Bold", 10.5, inner_w) if title else []
        body_lines = self.wrap_words_to_lines(text, "Vazir", 9.2, inner_w)
        
        box_h = pad_y * 2 + len(title_lines) * 16 + len(body_lines) * 14 + (6 if title else 0)
        self.check_space(box_h + 8)
        
        top_y = self.y
        self.c.setFillColor(bg_col)
        self.c.setStrokeColor(border_col)
        self.c.setLineWidth(1.2)
        self.c.roundRect(self.margin_x, top_y - box_h, self.content_width, box_h, 5, fill=1, stroke=1)
        
        cur_y = top_y - pad_y - 10
        if title:
            for tl in title_lines:
                self.c.setFont("Vazir-Bold", 10.5)
                self.c.setFillColor(title_col)
                self.c.drawRightString(self.width - self.margin_x - pad_x, cur_y, fa(tl))
                cur_y -= 16
            cur_y -= 4
            
        for bl in body_lines:
            self.c.setFont("Vazir", 9.2)
            self.c.setFillColor(C_CHARCOAL)
            self.c.drawRightString(self.width - self.margin_x - pad_x, cur_y, fa(bl))
            cur_y -= 14
            
        self.y = top_y - box_h - 10

    def draw_bullet_item(self, bold_prefix, text_body, color=C_CHARCOAL):
        """Draw a clean bullet point."""
        full_text = f"• {bold_prefix} {text_body}"
        self.draw_text_block(full_text, font_name="Vazir", font_size=9.2, color=color, leading=14.5, indent=8)
        self.y -= 3

    def draw_qa_item(self, q_num, question, answer, core_insight=None):
        """Draw an ultra-clear, professional Q&A box."""
        pad_x = 12
        pad_y = 8
        inner_w = self.content_width - 2 * pad_x
        
        q_full = f"پرسش {q_num}: {question}"
        q_lines = self.wrap_words_to_lines(q_full, "Vazir-Bold", 10, inner_w - 10)
        
        ans_prefix = "پاسخ دفاعیه دانشجو: "
        ans_lines = self.wrap_words_to_lines(ans_prefix + answer, "Vazir", 9, inner_w)
        
        ins_lines = self.wrap_words_to_lines(f"نکته کلیدی و برنده: {core_insight}", "Vazir-Bold", 8.5, inner_w) if core_insight else []
        
        q_header_h = len(q_lines) * 15 + 12
        ans_body_h = len(ans_lines) * 13.5 + 14 + (len(ins_lines) * 13 + 8 if ins_lines else 0)
        total_h = q_header_h + ans_body_h
        
        self.check_space(total_h + 8)
        top_y = self.y
        
        # Outer Card
        self.c.setFillColor(C_WHITE)
        self.c.setStrokeColor(C_CARD_BORDER)
        self.c.setLineWidth(1)
        self.c.roundRect(self.margin_x, top_y - total_h, self.content_width, total_h, 4, fill=1, stroke=1)
        
        # Question Header Box
        self.c.setFillColor(C_Q_BG)
        self.c.setStrokeColor(C_Q_BORDER)
        self.c.roundRect(self.margin_x, top_y - q_header_h, self.content_width, q_header_h, 4, fill=1, stroke=1)
        
        # Red Tag
        self.c.setFillColor(C_CRIMSON)
        self.c.rect(self.width - self.margin_x - 5, top_y - q_header_h, 5, q_header_h, fill=1, stroke=0)
        
        # Draw Question Lines
        cur_y = top_y - 14
        for ql in q_lines:
            self.c.setFont("Vazir-Bold", 9.8)
            self.c.setFillColor(C_CRIMSON)
            self.c.drawRightString(self.width - self.margin_x - pad_x, cur_y, fa(ql))
            cur_y -= 15
            
        # Draw Answer Lines
        cur_y = top_y - q_header_h - 13
        for idx, al in enumerate(ans_lines):
            self.c.setFont("Vazir-Bold" if idx == 0 and "پاسخ دفاعیه" in al else "Vazir", 9)
            self.c.setFillColor(C_NAVY_DARK if idx == 0 else C_CHARCOAL)
            self.c.drawRightString(self.width - self.margin_x - pad_x, cur_y, fa(al))
            cur_y -= 13.5
            
        if ins_lines:
            cur_y -= 4
            for inl in ins_lines:
                self.c.setFont("Vazir-Bold", 8.5)
                self.c.setFillColor(C_TEAL_DARK)
                self.c.drawRightString(self.width - self.margin_x - pad_x, cur_y, fa(inl))
                cur_y -= 13
                
        self.y = top_y - total_h - 8

    def draw_table(self, title, headers, rows, col_widths, col_aligns=None):
        """Draw a formatted table with multiline cell support."""
        if col_aligns is None:
            col_aligns = ["center"] * len(headers)
            
        header_h = 24
        
        # Pre-calculate row heights based on wrapped cell lines
        row_heights = []
        wrapped_rows = []
        for r in rows:
            max_lines = 1
            wrapped_cells = []
            for c_idx, val in enumerate(r):
                w = col_widths[c_idx] - 12
                lines = self.wrap_words_to_lines(str(val), "Vazir", 8.8, w)
                wrapped_cells.append(lines if lines else [""])
                if len(lines) > max_lines:
                    max_lines = len(lines)
            row_h = max(21, max_lines * 13 + 8)
            row_heights.append(row_h)
            wrapped_rows.append(wrapped_cells)
            
        total_h = header_h + sum(row_heights) + (20 if title else 0)
        self.check_space(total_h + 10)
        
        top_y = self.y
        if title:
            self.c.setFont("Vazir-Bold", 10.5)
            self.c.setFillColor(C_NAVY_DARK)
            self.c.drawRightString(self.width - self.margin_x, top_y - 12, fa(title))
            top_y -= 20
            
        # Draw Header
        self.c.setFillColor(C_NAVY_DARK)
        self.c.rect(self.margin_x, top_y - header_h, self.content_width, header_h, fill=1, stroke=0)
        
        cur_x = self.width - self.margin_x
        for idx, (h, w) in enumerate(zip(headers, col_widths)):
            self.c.setFont("Vazir-Bold", 9.5)
            self.c.setFillColor(C_WHITE)
            center_x = cur_x - (w / 2.0)
            self.c.drawCentredString(center_x, top_y - 16, fa(h))
            cur_x -= w
            
        # Draw Rows
        cur_y = top_y - header_h
        for r_idx, (wrapped_cells, row_h) in enumerate(zip(wrapped_rows, row_heights)):
            bg = C_WHITE if r_idx % 2 == 0 else C_LIGHT_BG
            self.c.setFillColor(bg)
            self.c.rect(self.margin_x, cur_y - row_h, self.content_width, row_h, fill=1, stroke=0)
            
            # Row border
            self.c.setStrokeColor(C_CARD_BORDER)
            self.c.setLineWidth(0.6)
            self.c.line(self.margin_x, cur_y - row_h, self.width - self.margin_x, cur_y - row_h)
            
            cur_x = self.width - self.margin_x
            for c_idx, (lines, w) in enumerate(zip(wrapped_cells, col_widths)):
                align = col_aligns[c_idx]
                start_y = cur_y - (row_h / 2.0) + (len(lines) * 12.0 / 2.0) - 9
                for l_idx, line in enumerate(lines):
                    line_y = start_y - (l_idx * 12)
                    self.c.setFont("Vazir", 8.8)
                    self.c.setFillColor(C_CHARCOAL)
                    if align == "center":
                        self.c.drawCentredString(cur_x - (w / 2.0), line_y, fa(line))
                    elif align == "right":
                        self.c.drawRightString(cur_x - 6, line_y, fa(line))
                    else:
                        self.c.drawString(cur_x - w + 6, line_y, fa(line))
                cur_x -= w
            cur_y -= row_h
            
        # Outer table border
        self.c.setStrokeColor(C_CARD_BORDER)
        self.c.setLineWidth(1)
        self.c.rect(self.margin_x, top_y - header_h - sum(row_heights), self.content_width, header_h + sum(row_heights), fill=0, stroke=1)
        
        self.y = top_y - header_h - sum(row_heights) - 10

    def save(self):
        self.c.showPage()
        self.c.save()
        print(f"Comprehensive Defense Guide successfully built: {self.filename}")

# -------------------------------------------------------------
# Main Generation Routine
# -------------------------------------------------------------
def build_guide():
    doc = GuideDoc("MAB-THESIS/Defense_Guide.pdf")
    
    # ---------------------------------------------------------
    # COVER BANNER
    # ---------------------------------------------------------
    doc.draw_banner(
        title="راهنمای جامع تسلط بر پایان‌نامه و آمادگی کامل برای جلسه دفاع",
        subtitle="حل مسئله مستقیم معادله غیرخطی برگرز با استفاده از شبکه‌های عصبی آگاه از فیزیک (PINN) در JAX",
        meta_lines=[
            "پژوهشگر: محمد امیر بابازاد",
            "استاد راهنما: دکتر بابک آذرنوید",
            "دانشگاه بناب — دانشکده علوم پایه",
            "شهریور ۱۴۰۵"
        ]
    )

    # ---------------------------------------------------------
    # SECTION 1: BIG PICTURE & CORE INTUITION
    # ---------------------------------------------------------
    doc.draw_callout_box(
        title="پیام مهم به دانشجو: چگونه با این جزوه در جلسه دفاع بدرخشید؟",
        text="این راهنمای اختصاصی با زبانی شفاف، عمیق و آکادمیک تدوین شده تا بدون نیاز به پیچیدگی‌های غیرضروری، بر تمام مبانی تئوری، کدهای جکس، نتایج تجربی و منطق علمی پایان‌نامه تسلط ۱۰۰ درصدی پیدا کنید. با مطالعه این فایل، به تمام پرسش‌های داوران با اعتمادبه‌نفس، استدلال محکم و تسلط پاسخ خواهید داد.",
        bg_col=C_CALLOUT_BG,
        border_col=C_CALLOUT_BOR,
        title_col=C_NAVY_DARK
    )

    doc.draw_section_header("۱", "تصویر کلان و منطق علمی پایان‌نامه (به زبان ساده و ملموس)", C_NAVY_DARK)

    doc.draw_bullet_item(
        "هدف بنیادین این پایان‌نامه چیست؟",
        "هدف ما محاسبه و پیش‌بینی رفتار میدان سرعت یک سیال پیوسته در طول فضا و زمان است. این پدیده با یک معادله دیفرانسیل جزئی غیرخطی بسیار معروف به نام «معادله برگرز» مدل‌سازی می‌شود که چالش اصلی آن، تشکیل جبهه تیز و ناگهانی موج شوک است."
    )

    doc.draw_bullet_item(
        "چرا روش‌های محاسباتی سنتی در حل این مسئله با چالش روبرو می‌شوند؟",
        "روش‌های کلاسیک مهندسی (نظیر تفاضل‌های محدود و اجزای محدود) مجبورند کل فضا و زمان را به شبکه‌ای از نقاط (مش) تقسیم کنند. این کار سه ایراد اساسی دارد: ۱. در ابعاد بالا با پدیده نفرین ابعاد و هزینه محاسباتی فوق‌العاده سنگین مواجه می‌شویم. ۲. روی هندسه‌های نامنظم، ساخت شبکه محاسباتی بسیار پیچیده است. ۳. تقریب‌های گسسته‌سازی مشتقات در جبهه‌های شوک خطای زیادی ایجاد می‌کنند."
    )

    doc.draw_bullet_item(
        "چرا هوش مصنوعی و یادگیری عمیق معمولی (صرفاً داده‌محور) کافی نیست؟",
        "شبکه‌های عصبی استاندارد مثل جعبه سیاه عمل می‌کنند؛ یعنی نیازمند هزاران نقطه داده تجربی و آزمایشگاهی هستند. در مسائل فیزیکی، ثبت داده در همه نقاط پیوسته عملاً غیرممکن است. اگر داده کم باشد، شبکه معمولی دچار بیش‌برازش شده و پیش‌بینی‌هایی تولید می‌کند که قوانین بنیادین فیزیک (نظیر بقای جرم و انرژی) را نقض می‌نماید."
    )

    doc.draw_bullet_item(
        "شاهکار این پایان‌نامه و ایده کلیدی شبکه آگاه از فیزیک (PINN) چیست؟",
        "ما به جای وابستگی به داده‌های انبوه، خود «قانون فیزیک» (معادله دیفرانسیل برگرز) را وارد تابع هدف شبکه عصبی می‌کنیم. شبکه با استفاده از فناوری «مشتق‌گیری خودکار» در کتابخانه جکس، یاد می‌گیرد خروجی‌ای تولید کند که هم شرایط اولیه و مرزی را ارضا نماید و هم باقیمانده معادله فیزیک در سراسر دامنه فضا-زمان صفر شود."
    )

    # ---------------------------------------------------------
    # SECTION 2: CHAPTER-BY-CHAPTER BREAKDOWN
    # ---------------------------------------------------------
    doc.draw_section_header("۲", "کالبدشکافی و خلاصه محتوای فصل‌های پایان‌نامه (فصل به فصل)", C_NAVY_BLUE)

    doc.draw_bullet_item(
        "فصل اول (مقدمه و کلیات پژوهش):",
        "طرح موضوع، تبیین ناکارآمدی روش‌های سنتی مبتنی بر شبکه، تعریف دقیق مسئله مستقیم، معرفی معادله برگرز و چالش جبهه شوک، بستر نرم‌افزاری جکس (JAX) و ساختار اهداف و نوآوری‌های پایان‌نامه."
    )

    doc.draw_bullet_item(
        "فصل دوم (مبانی نظری و پیشینه پژوهش):",
        "معرفی فیزیک حاکم بر معادله برگرز (رقابت همرفت غیرخطی و لزجت)، مقایسه ۳ روش کلاسیک عددی (تفاضل محدود، اجزای محدود، طیفی)، معماری شبکه پرسپترون چندلایه (MLP)، مقایسه توابع فعال‌ساز، قضیه تقریب عمومی چبنکو، روش‌های بهینه‌سازی آدام و ال-بی‌اف‌جی‌اس و سیر تاریخی تکامل روش‌های تلفیقی از ۱۹۹۸ تا شاهکار ۲۰۱۹ رئیسی."
    )

    doc.draw_bullet_item(
        "فصل سوم (شبکه‌های عصبی آگاه از فیزیک — روش پژوهش):",
        "ایده محوری و دیاگرام بلوکی، تابع هزینه دوگانه، مقایسه مشتق‌گیری خودکار با تفاضل محدود و مشتق نمادین، تشریح ۵ گام ریاضی استخراج مشتقات در جکس، ساختار دو سطحی مشتق‌گیری، مقایسه مدل زمان‌پیوسته با زمان‌گسسته رانگه--کوتا و دلایل انتخاب تابع تانژانت هیپربولیک و بهینه‌سازی ترکیبی."
    )

    doc.draw_bullet_item(
        "فصل چهارم (پیاده‌سازی و ارزیابی تجربی نتایج):",
        "پیکربندی بستر جکس و دقت ممیز شناور ۶۴ بیتی، خط لوله تبدیلات تابعی (grad, vmap, jit)، نتایج حل مستقیم معادله برگرز، تحلیل تاریخچه همگرایی توابع هزینه، بازسازی جبهه شوک در مقاطع زمانی مختلف، نقشه دوبعدی خطا و ارزیابی تطبیقی با مقاله مرجع رئیسی و همکاران (۲۰۱۹)."
    )

    doc.draw_bullet_item(
        "فصل پنجم (نتیجه‌گیری و پیشنهادها):",
        "جمع‌بندی دستاوردهای علمی در حل بدون شبکه معادلات غیرخطی و ارائه ۴ افق توسعه آتی (توابع فعال‌ساز تطبیقی، شبکه‌های ویژگی فوریه، تفکیک دامنه و تعمیم به معادلات دوبعدی و سه‌بعدی ناویه--استوکس)."
    )

    # ---------------------------------------------------------
    # SECTION 3: NUMERICAL FACTSHEET TABLE
    # ---------------------------------------------------------
    doc.draw_section_header("۳", "شناسنامه محاسباتی، مقادیر عددی و نتایج تجربی پایان‌نامه", C_TEAL_DARK)

    doc.draw_callout_box(
        title="اعداد و پارامترهای طلایی که باید در جلسه دفاع حفظ باشید:",
        text="این جدول کل مقادیر تجربی و پارامترهای پیاده‌سازی‌شده در کد پایان‌نامه را خلاصه می‌کند. داوران معمولاً این اعداد را می‌پرسند تا از تسلط عملی شما بر اجرای آزمایش‌ها مطمئن شوند.",
        bg_col=C_LIGHT_BG,
        border_col=C_CARD_BORDER,
        title_col=C_NAVY_DARK
    )

    headers = ["شاخص محاسباتی", "مقدار در این پژوهش", "توضیح مفهومی و کاربرد"]
    col_w = [140, 160, 220]
    rows = [
        ["معادله دیفرانسیل آزمون", "معادله غیرخطی برگرز با لزجت", "توصیف رقابت همرفت غیرخطی و پخش لزجت"],
        ["ضریب لزجت سینماتیکی", "۰٫۰۱ تقسیم بر پی (حدود ۰٫۰۰۳۱۸)", "هرچه کمتر باشد جبهه شوک تیزتر و حل سخت‌تر است"],
        ["دامنه فضا و زمان", "مکان از ۱- تا ۱+ و زمان از ۰ تا ۱", "دامنه دوبعدی پیوسته فضا-زمان بدون شبکه‌بندی"],
        ["شرط اولیه و مرزها", "سینوسی با مرزهای همگن دیریکله", "مقدار اولیه منفی سینوس پی ایکس و صفر در مرزها"],
        ["داده‌های مرزی و اولیه", "۲۰۰ نقطه (۱۰۰ مرزی + ۱۰۰ اولیه)", "تنها داده‌های برچسب‌دار معلوم در کل مسئله"],
        ["نقاط هم‌مکانی باقیمانده", "۱۰۰۰۰ نقطه درون فضا-زمان", "۵۰٪ تصادفی یکنواخت + ۵۰٪ متمرکز در شوک"],
        ["معماری شبکه عصبی", "۴ لایه پنهان، ۵۰ نورون در هر لایه", "پرسپترون چندلایه با تابع فعال‌ساز Tanh"],
        ["تعداد کل پارامترها", "۷۸۵۱ پارامتر وزن و بایاس", "مقداردهی اولیه وزن‌ها با توزیع یکنواخت گزاویه"],
        ["استراتژی آموزش مدل", "ترکیبی: آدام و سپس ال-بی‌اف‌جی‌اس", "۶۰۰۰ گام آدام و سپس L-BFGS تا همگرایی"],
        ["دقت ممیز شناور", "۶۴ بیتی (Float64)", "حذف خطاهای گردکردن در تقریب شیب‌های تند"],
        ["خطای نسبی در نرم L2", "۲٫۱۵ درصد", "میزان انحراف میدان پیش‌بینی از میدان مرجع"],
        ["خطای باقیمانده فیزیک", "۶٫۳۶ در ۱۰ به توان ۵-", "نشان‌دهنده ارضای فوق‌العاده قوی قانون فیزیک"],
        ["خطای داده‌های مرزی", "۲٫۳۵ در ۱۰ به توان ۵-", "انطباق عالی خروجی شبکه با شرایط مرزی و اولیه"],
    ]
    doc.draw_table("", headers, rows, col_w, ["center", "center", "right"])

    # ---------------------------------------------------------
    # SECTION 4: EXPLANATION OF FIGURES & CHARTS
    # ---------------------------------------------------------
    doc.draw_section_header("۴", "تحلیل دقیق نمودارها و شکل‌های فصل چهارم پایان‌نامه", C_NAVY_DARK)

    doc.draw_bullet_item(
        "شکل ۱-۴ (توزیع نقاط آموزش در دامنه فضا-زمان):",
        "این شکل نشان می‌دهد چگونه ۲۰۰ نقطه قرمز رنگ روی مرزهای مکانی و لحظه آغازین قرار گرفته‌اند و ۱۰۰۰۰ نقطه خاکستری در سراسر دامنه پخش شده‌اند. تراکم بالاتر نقاط در خط مرکزی x=0 نشان‌دهنده راهبرد نمونه‌برداری متمرکز در ناحیه تشکیل موج شوک است."
    )

    doc.draw_bullet_item(
        "شکل ۲-۴ (تاریخچه همگرایی توابع هزینه در مقیاس لگاریتمی):",
        "این نمودار نشان می‌دهد که در فاز اول (بهینه‌ساز آدام)، خطای کل با شیب مناسب افت می‌کند و پس از گام ۶۰۰۰ با ورود بهینه‌ساز شبه‌نیوتنی L-BFGS، خطا دچار یک ریزش شارپ شده و به دقت ۱۰ به توان منفی ۵ می‌رسد."
    )

    doc.draw_bullet_item(
        "شکل ۳-۴ (مقاطع زمانی پاسخ در لحظات t=0.25, 0.50, 0.75):",
        "این نمودار قلب نتایج تجربی پایان‌نامه است. خطوط ممتد مشکی جواب مرجع و خط‌چین قرمز پیش‌بینی PINN هستند. مشاهده می‌شود که موج سینوسی هموار اولیه با گذر زمان به سمت مرکز متمایل شده و در حوالی x=0 یک افت عمودی و دیوارمانند (جبهه شوک) ایجاد می‌کند و مدل با دقت عالی آن را بازسازی کرده است."
    )

    doc.draw_bullet_item(
        "شکل ۴-۴ (نقشه کانتور دوبعدی قدرمطلق خطا):",
        "نمودار کانتور رنگی نشان می‌دهد که در بیش از ۹۵ درصد مساحت دامنه، خطا بسیار ناچیز و نزدیک به صفر است و بیشینه خطای اندک مدل فقط در امتداد نوار بسیار باریک خط شوک (برای زمان‌های بعد از ۰٫۳) متمرکز شده است."
    )

    # ---------------------------------------------------------
    # SECTION 5: JAX EXECUTION PIPELINE
    # ---------------------------------------------------------
    doc.draw_section_header("۵", "خط لوله ۵ مرحله‌ای اجرای مدل در کتابخانه جکس (JAX)", C_TEAL_DARK)

    doc.draw_bullet_item(
        "گام اول (مقداردهی اولیه پارامترها):",
        "وزن‌های شبکه با توزیع یکنواخت گزاویه (بر اساس تعداد نورون‌های ورودی و خروجی) و بایاس‌ها با صفر آغاز می‌شوند تا پایداری واریانس گرادیان‌ها حفظ شود."
    )

    doc.draw_bullet_item(
        "گام دوم (تبدیلات تابعی و مشتق‌گیری خودکار):",
        "تابع پیش‌بینی شبکه تعریف شده و مشتقات زمانی و مکانی با استفاده از تبدیل تابعی jax.grad به صورت تحلیلی و تودرتو استخراج می‌گردند."
    )

    doc.draw_bullet_item(
        "گام سوم (بردارسازی و کامپایل JIT):",
        "با استفاده از jax.vmap ارزیابی نقاط به صورت دسته‌ای و برداری درمی‌آید و با jax.jit کل گراف محاسباتی با کامپایلر XLA به کد ماشین بهینه تبدیل می‌شود."
    )

    doc.draw_bullet_item(
        "گام چهارم (محاسبه همزمان تابع هزینه و گرادیان):",
        "با استفاده از jax.value_and_grad، مقدار تابع هزینه ترکیبی و بردار گرادیان آن نسبت به پارامترهای شبکه در یک گذر مشترک و سریع به دست می‌آید."
    )

    doc.draw_bullet_item(
        "گام پنجم (استراتژی بهینه‌سازی دو مرحله‌ای):",
        "ابتدا ۶۰۰۰ تکرار با بهینه‌ساز آدام برای فرار از کمینه‌های محلی اجرا شده و سپس آموزش با روش شبه‌نیوتنی L-BFGS-B تا رسیدن به همگرایی عمیق ادامه می‌یابد."
    )

    # ---------------------------------------------------------
    # SECTION 6: GOLDEN DEFENSE Q&A BANK (18 High-Yield Questions)
    # ---------------------------------------------------------
    doc.draw_section_header("۶", "بانک طلایی ۱۸ پرسش کلیدی داوران و پاسخ‌های مسلط و دفاع‌محور", C_CRIMSON)

    doc.draw_callout_box(
        title="راهنمای تسلط بر جلسه دفاع:",
        text="این ۱۸ پرسش پرتکرارترین، تخصصی‌ترین و چالش‌برانگیزترین سوالاتی هستند که اساتید راهنما و داوران در جلسات دفاع مطرح می‌کنند. تسلط بر این پاسخ‌ها تضمین‌کننده نمره کامل و آرامش روانی شماست.",
        bg_col=C_Q_BG,
        border_col=C_Q_BORDER,
        title_col=C_CRIMSON
    )

    qa_list = [
        (
            "۱",
            "تفاوت بنیادین مشتق‌گیری خودکار (AutoDiff) با مشتق‌گیری عددی و نمادین چیست؟",
            "مشتق‌گیری عددی (تفاضل محدود) دچار تعارض دو خطاست: خطای برش در طول گام بزرگ و خطای گردکردن در طول گام کوچک. مشتق‌گیری نمادین هم با پدیده تورم نمایی عبارات جبری مواجه است. در مقابل، مشتق‌گیری خودکار با ساخت گراف محاسباتی کد پایتون و اعمال دقیق قاعده زنجیره‌ای، مشتقات جزئی را با دقت تحلیلی تا حد دقت ممیز شناور ماشین بدون هیچ خطای برشی ارزیابی می‌کند.",
            "مشتق‌گیری خودکار نه نمادین است و نه عددی، بلکه اعمال سیستماتیک قاعده زنجیره‌ای روی کدهای اجرایی برنامه است."
        ),
        (
            "۲",
            "چرا در معماری شبکه عصبی از تابع فعال‌ساز Tanh استفاده کردید و چرا ReLU کارایی ندارد؟",
            "معادله برگرز نیازمند مشتق دوم مکانی برای مدل‌سازی لزجت است. تابع ReLU یک تابع تکه‌ای خطی است که مشتق اول آن پله‌ای و مشتق دوم آن در همه نقاط صفر است. بنابراین با ReLU، ترم لزجت معادله کاملاً پوچ می‌شود. در مقابل، تانژانت هیپربولیک (Tanh) یک تابع هموار و بی‌نهایت بار مشتق‌پذیر است و مشتقات اول و دوم تحلیلی غیرصفر و منظم تولید می‌کند.",
            "مشتق دوم ReLU صفر است؛ لذا استفاده از ReLU در حل معادلات دیفرانسیل مرتبه دو از نظر ریاضی غیرممکن است."
        ),
        (
            "۳",
            "ساختار دو سطحی مشتق‌گیری خودکار که در فصل ۳ تشریح شده است دقیقاً یعنی چه؟",
            "در PINN دو سطح متمایز مشتق‌گیری داریم: سطح اول (مشتق داخلی) مشتق‌گیری از خروجی شبکه نسبت به ورودی‌های فیزیکی فضا-زمان (t, x) برای تشکیل عملگر باقیمانده فیزیک است. سطح دوم (مشتق خارجی) مشتق‌گیری از تابع هزینه کل نسبت به پارامترهای وزن و بایاس شبکه برای پس‌انتشار خطا و آموزش مدل است.",
            "سطح اول قوانین فیزیک را می‌سازد و سطح دوم وزن‌های شبکه عصبی را به‌روزرسانی می‌کند."
        ),
        (
            "۴",
            "چرا فرآیند آموزش را به صورت دو مرحله‌ای (ابتدا Adam و سپس L-BFGS) طراحی کردید؟",
            "توابع هزینه در شبکه‌های آگاه از فیزیک غیرمحدب و دارای کمینه‌های محلی فراوان هستند. بهینه‌ساز آدام با بهره‌گیری از گشتاور اول و دوم، در مراحل اولیه برای فرار از کمینه‌های محلی و کاهش سریع خطا بسیار توانمند است. اما در نزدیکی نقطه بهینه سرعت آن کند می‌شود. بهینه‌ساز شبه‌نیوتنی L-BFGS با تقریب ماتریس معکوس هشین، سرعت همگرایی فوق‌خطی و مرتبه دو دارد و دقت نهایی را رقم می‌زند.",
            "آدام مدل را به حوضچه همگرایی می‌رساند و ال-بی‌اف‌جی‌اس ریزش شارپ نهایی به سمت صفر را ایجاد می‌کند."
        ),
        (
            "۵",
            "نقاط هم‌مکانی (Collocation Points) چیستند و چرا چگالی آن‌ها در حوالی x=0 بیشتر بود؟",
            "نقاط هم‌مکانی نقاطی درون دامنه پیوسته فضا-زمان هستند که هیچ داده اندازه‌گیری تجربی برای آن‌ها نداریم، اما باقیمانده معادله فیزیک در آن‌ها محاسبه و صفر می‌شود. در معادله برگرز پدیده موج شوک و گرادیان‌های شدید در حوالی خط مرکزی x=0 رخ می‌دهد. اختصاص ۵۰٪ نقاط به این ناحیه باعث شد شبکه رزولوشن بالاتری برای یادگیری جبهه تیز شوک داشته باشد.",
            "نمونه‌برداری متمرکز در ناحیه شوک باعث به دام انداختن ناپیوستگی بدون افزایش بیهوده کل نقاط محاسباتی می‌شود."
        ),
        (
            "۶",
            "چرا کتابخانه جکس (JAX) را به جای PyTorch یا TensorFlow انتخاب کردید؟",
            "جکس مبتنی بر پارادایم برنامه‌نویسی تابعی محض طراحی شده و تبدیلات تابعی فوق‌العاده‌ای نظیر grad برای مشتق‌گیری مراتب بالا، vmap برای بردارسازی موازی و jit برای کامپایل بهینه با موتور XLA ارائه می‌دهد. این ویژگی‌ها سرعت محاسباتی بسیار بالا، کدنویسی تمیز و سازگاری کامل با دقت ۶۴ بیتی را فراهم می‌کنند.",
            "ترکیب grad و vmap و jit در جکس، ایده‌آل‌ترین خط لوله برای حل معادلات دیفرانسیل بدون حلقه‌های کند پایتون است."
        ),
        (
            "۷",
            "چرا در این پژوهش صرفاً بر مسئله مستقیم تمرکز کردید و مسئله معکوس بررسی نشد؟",
            "با راهنمایی استاد محترم راهنما (جناب آقای دکتر آذرنوید)، برای حفظ تمرکز عمیق پژوهش بر روی چالش‌های محاسباتی بازسازی جبهه‌های نوک‌تیز موج شوک و تحلیل توزیع مکانی-زمانی خطا و مقایسه جامع با مقاله مرجع معتبر رئیسی و همکاران (۲۰۱۹)، دامنه این پایان‌نامه به صورت تخصصی بر حل مسئله مستقیم معطوف گردید.",
            "تمرکز بر مسئله مستقیم امکان تحلیل عمیق‌تر پایداری الگوریتم و رفتار مکانی-زمانی خطا در جبهه شوک را فراهم آورد."
        ),
        (
            "۸",
            "نقش ضریب لزجت (nu) در رفتار معادله برگرز چیست و اگر مقدار آن کمتر شود چه اتفاقی می‌افتد؟",
            "ضریب لزجت بیانگر شدت پخش و اصطکاک سیال است که تمایل به هموارسازی امواج دارد. در مقابل، جمله غیرخطی تمایل به جلو کشیدن موج و ایجاد ناپیوستگی دارد. هرچه لزجت کمتر باشد، جبهه شوک نوک‌تیزتر، شیب‌دارتر و باریک‌تر می‌شود و چالش تقریب شبکه عصبی به شدت افزایش می‌یابد.",
            "ضریب لزجت کوچک یعنی غلبه همرفت غیرخطی بر پخش، که منجر به پیدایش موج شوک شبه‌ناپیوسته می‌شود."
        ),
        (
            "۹",
            "آیا شبکه عصبی PINN دچار بیش‌برازش (Overfitting) نمی‌شود؟ چرا از Dropout استفاده نکردید؟",
            "خیر؛ در شبکه‌های آگاه از فیزیک، وجود جمله باقیمانده فیزیک کل فضای فرضیات شبکه را به توابعی محدود می‌کند که قوانین دیفرانسیل حاکم را ارضا کنند. این قید فیزیکی در حقیقت نقش یک منظم‌ساز ساختاری فوق‌العاده قدرتمند را ایفا می‌کند که مانع از بیش‌برازش می‌شود؛ لذا نیازی به تکنیک‌های تجربی مثل لایه‌های دراپ‌اوت وجود ندارد.",
            "قانون فیزیک قدرتمندترین منظم‌ساز ریاضی است و شبکه را در تمام دامنه مهار می‌کند."
        ),
        (
            "۱۰",
            "خطای ۲٫۱۵ درصدی به دست آمده در مقایسه با مقاله مرجع رئیسی (۲۰۱۹) چگونه ارزیابی می‌شود؟",
            "در مقاله مرجع رئیسی از شبکه‌ای عمیق‌تر (۸ لایه پنهان) با ده‌ها هزار تکرار L-BFGS بر روی کارت‌های گرافیکی تخصصی سرور استفاده شده است. در پژوهش حاضر با معماری ۴ لایه و بهینه‌سازی متعادل روی پردازنده مرکزی معمولی، به خطای ۲٫۱۵ درصد رسیدیم که از نظر کیفی موقعیت و شیب تیز شوک را در تمام مقاطع زمانی با وفاداری کامل بازتولید کرده است.",
            "تطابق ساختاری پروفیل شوک در سه مقطع زمانی نشان‌دهنده موفقیت کیفی و کمی مدل در چارچوب سخت‌افزار استاندارد است."
        ),
        (
            "۱۱",
            "تفاوت مدل زمان‌پیوسته و زمان‌گسسته چیست و چرا مدل زمان‌پیوسته را پیاده‌سازی کردید؟",
            "در مدل زمان‌پیوسته، فضا و زمان به صورت متغیرهای پیوسته همزمان به شبکه داده می‌شوند و میدان در کل دامنه ارزیابی می‌شود. در مدل زمان‌گسسته، از روش‌های رانگه--کوتا ضمنی برای گام‌زنی زمانی استفاده می‌شود. مدل زمان‌پیوسته به دلیل ساختار یکپارچه، سادگی محاسباتی و توانایی ارزیابی میدان در هر لحظه دلخواه، رویکرد اصلی این پژوهش بوده است.",
            "مدل زمان‌پیوسته نیازی به گام‌بندی گسسته زمانی ندارد و حل پیوسته در تمام فضا-زمان ارائه می‌دهد."
        ),
        (
            "۱۲",
            "آیا این چارچوب برای معادلات دوبعدی، سه‌بعدی و هندسه‌های نامنظم هم کاربرد دارد؟",
            "بله؛ بزرگ‌ترین مزیت PINN بدون شبکه بودن (Mesh-Free) آن است. در ابعاد بالاتر کافی است بردار ورودی شبکه به ابعاد بالاتر گسترش یابد و نقاط هم‌مکانی درون هندسه نامنظم نمونه‌برداری شوند، بدون اینکه نیازی به تولید توری یا المان‌بندی‌های پیچیده مهندسی باشد.",
            "چارچوب PINN هندسه‌ناپذیر و مستقل از شبکه است و به راحتی به ابعاد بالاتر تعمیم می‌یابد."
        ),
        (
            "۱۳",
            "چرا مقداردهی اولیه وزن‌ها با روش گزاویه (Glorot) انجام شد؟",
            "مقداردهی گزاویه واریانس خروجی هر لایه را با واریانس ورودی آن برابر نگه می‌دارد. این کار مانع از پدیده‌های مخرب محو شدن یا انفجار گرادیان‌ها در لایه‌های متوالی شبکه می‌شود و نقطه آغازین بهینه‌سازی را در یک وضعیت متقارن و پایدار قرار می‌دهد.",
            "مقداردهی گزاویه تعادل سیگنال را در تمام لایه‌های پرسپترون حفظ می‌کند."
        ),
        (
            "۱۴",
            "نقش قضیه تقریب عمومی چبنکو (Universal Approximation) در این پایان‌نامه چیست؟",
            "قضیه چبنکو اثبات ریاضی می‌کند که یک شبکه پرسپترون چندلایه با توابع فعال‌ساز غیرخطی و پیوسته می‌تواند هر تابع پیوسته دلخواهی را با دقت مطلوب تقریب بزند. این قضیه تضمین نظری وجود جوابی برای تقریب میدان سرعت معادله برگرز توسط ساختار شبکه ماست.",
            "قضیه چبنکو پشتوانه نظری امکان‌پذیری حل معادلات دیفرانسیل توسط شبکه‌های عصبی است."
        ),
        (
            "۱۵",
            "چرا از دقت ممیز شناور ۶۴ بیتی (Float64) در جکس استفاده کردید؟",
            "محاسبه مشتقات مرتبه دوم در نزدیکی جبهه شوک به دلیل تفریق اعداد بسیار نزدیک، مستعد خطای حذف رقایم بامعنی (Catastrophic Cancellation) است. فعال‌سازی دقت ۶۴ بیتی در جکس باعث شد خطاهای گردکردن ممیز شناور عملاً به صفر برسد.",
            "دقت مضاعف ۶۴ بیتی پایداری مشتقات مرتبه بالا در جبهه‌های تیز شوک را تضمین می‌کند."
        ),
        (
            "۱۶",
            "پدیده سوگیری طیفی (Spectral Bias) در شبکه‌های عصبی چیست؟",
            "شبکه‌های عصبی استاندارد تمایل دارند ابتدا فرکانس‌های پایین و رفتارهای هموار را یاد بگیرند و یادگیری مؤلفه‌های فرکانس بالا (مثل جبهه‌های شوک تیز) بسیار کندتر انجام می‌شود. این موضوع دلیل اصلی کندی همگرایی در حوالی خط شوک است که در کارهای آینده با توابع ویژگی فوریه قابل حل است.",
            "سوگیری طیفی تمایل طبیعی شبکه به هموارسازی است که با روش‌های تعبیه فرکانسی اصلاح می‌شود."
        ),
        (
            "۱۷",
            "تعارض گرادیان‌ها میان تابع هزینه مرزی و فیزیک چیست و چگونه مدیریت شد؟",
            "در طول آموزش، گرادیان‌های ناشی از باقیمانده فیزیک ممکن است با گرادیان‌های داده‌های مرزی زاویه باز بسازند و یکدیگر را تضعیف کنند. در این پژوهش با شروع از بهینه‌ساز آدام و سپس استفاده از L-BFGS و انتخاب دقیق تعداد نقاط، تعادل لازم بین دو مؤلفه برقرار گردید.",
            "بهینه‌سازی ترکیبی و نمونه‌برداری متوازن مانع از تسلط یک مؤلفه بر دیگری شد."
        ),
        (
            "۱۸",
            "اگر داور بگوید «روش‌های سنتی برای این مسئله ۱ بعدی سریع‌ترند، مزیت کار شما چیست؟» چه پاسخی می‌دهید؟",
            "پاسخ من این است که مسئله برگرز ۱ بعدی یک بستر آزمون استاندارد و اثبات مفهوم (Proof of Concept) است. مزیت بنیادین روش ما در این است که اگر این مسئله به ابعاد بالاتر (مثلاً معادلات ۳ بعدی ناویه--استوکس در یک هندسه پیچیده مثل پره توربین) برود، روش‌های سنتی با بحران تولید شبکه و نفرین ابعاد مواجه می‌شوند؛ در حالی که ساختار PINN پیاده‌شده بدون هیچ تغییر ساختاری و بدون نیاز به شبکه، قابل اجرا خواهد بود.",
            "معادله برگرز یک محک استاندارد برای اثبات توانایی حل بدون شبکه در مسائل غیرخطی پیچیده است."
        )
    ]

    for q_data in qa_list:
        q_num, q_text, ans_text, core_ins = q_data
        doc.draw_qa_item(q_num, q_text, ans_text, core_ins)

    # ---------------------------------------------------------
    # SECTION 7: DEFENSE PRESENTATION SCRIPT (Minute-by-Minute)
    # Start on a fresh clean page for perfect layout
    # ---------------------------------------------------------
    doc.new_page()

    doc.draw_section_header("۷", "سناریوی گام‌به‌گام و زمان‌بندی ارائه دفاعیه (۲۰ دقیقه سخنرانی بی‌نقص)", C_NAVY_DARK)

    doc.draw_callout_box(
        title="تقسیم‌بندی استاندارد زمان ۲۰ دقیقه‌ای جلسه دفاع:",
        text="یک دفاعیه استاندارد و آکادمیک باید دقیقاً در ۲۰ دقیقه به پایان برسد تا داوران خسته نشوند و زمان کافی برای پرسش و پاسخ باقی بماند. اسلایدهای پاورپوینت دقیقاً با این سناریو همگام شده‌اند.",
        bg_col=C_LIGHT_BG,
        border_col=C_CARD_BORDER,
        title_col=C_NAVY_DARK
    )

    p_headers = ["بخش و اسلایدها", "زمان‌بندی", "موضوع محوری", "نکات کلیدی صحبت دانشجو"]
    p_col_w = [105, 60, 140, 215]
    p_rows = [
        ["اسلاید ۱ و ۲", "۲ دقیقه", "عنوان و ساختار ارائه", "خوش‌آمدگویی، معرفی خود و استاد راهنما، بیان فهرست مطالب"],
        ["اسلاید ۳ تا ۵", "۳ دقیقه", "مقدمه و کاستی‌های موجود", "اهمیت معادلات غیرخطی، چالش‌های FDM و FEM و محدودیت هوش مصنوعی سنتی"],
        ["اسلاید ۶ تا ۸", "۳ دقیقه", "ایده PINN و معادله برگرز", "تلفیق فیزیک با شبکه، رقابت همرفت و لزجت، تابع هزینه دوگانه"],
        ["اسلاید ۹ و ۱۰", "۲ دقیقه", "مشتق‌گیری خودکار و مدل‌ها", "مزیت AutoDiff نسبت به تفاضل محدود، مقایسه زمان‌پیوسته با زمان‌گسسته"],
        ["اسلاید ۱۱ تا ۱۴", "۴ دقیقه", "پیاده‌سازی جکس و بهینه‌سازی", "تبدیلات grad و vmap و jit، معماری ۴ لایه، تابع Tanh و آموزش دو مرحله‌ای"],
        ["اسلاید ۱۵ تا ۱۸", "۴ دقیقه", "نتایج تجربی و مقایسه", "بازسازی موج شوک (شکل ۳-۴)، نقشه خطا، مقایسه با مقاله مرجع رئیسی"],
        ["اسلاید ۱۹ تا ۲۱", "۲ دقیقه", "جمع‌بندی و سپاسگزاری", "دستاوردهای اصلی، ۴ افق آینده، تشکر از استاد راهنما و اعلام آمادگی"],
    ]
    doc.draw_table("", p_headers, p_rows, p_col_w, ["center", "center", "right", "right"])

    # ---------------------------------------------------------
    # SECTION 8: BODY LANGUAGE & DEFENSE ETIQUETTE
    # ---------------------------------------------------------
    doc.draw_section_header("۸", "نکات طلایی زبان بدن، مدیریت جلسه و کلام پایانی برای کسب نمره ۲۰", C_TEAL_DARK)

    doc.draw_bullet_item(
        "لحن و شیوه صحبت:",
        "شمرده، آرام و با تن صدای رسا و با اعتمادبه‌نفس صحبت کنید. از تند صحبت کردن پرهیز نمایید. بین جملات کلیدی مکث‌های کوتاه ۲ ثانیه‌ای داشته باشید تا مفاهیم در ذهن داور بنشیند."
    )

    doc.draw_bullet_item(
        "نحوه برخورد با انتقادات و سوالات داور:",
        "هرگز با داور وارد بحث فرسایشی یا لحن تدافعی نشوید. ابتدا با کمال احترام بگویید: «بسیار سپاسگزارم از نکته دقیق و ارزشمندی که استاد محترم فرمودند». سپس با استناد به مبانی ریاضی و شواهد تجربی پاسخ دهید."
    )

    doc.draw_bullet_item(
        "کلیدواژه طلایی که باید در پاسخ‌ها بدرخشد:",
        "«ارضای مستقیم قوانین فیزیک بدون نیاز به تولید شبکه محاسباتی (Mesh-Free) و با بهره‌گیری از مشتق‌گیری خودکار در کتابخانه جکس»."
    )

    doc.draw_callout_box(
        title="جمله طلایی و ماندگار شما برای پایان جلسه دفاع:",
        text="«شبکه عصبی آگاه از فیزیک (PINN) یک حل‌گر عددی مدرن و بدون شبکه محاسباتی است که با بهره‌گیری از مشتق‌گیری خودکار، قوانین بنیادین فیزیک را در سراسر فضا-زمان ارضا کرده و با کمترین داده‌های مرزی، رفتار پیچیده امواج شوک را با دقت بالا بازسازی می‌نماید. با تشکر فراوان از توجه و شکیبایی هیئت محترم داوران.»",
        bg_col=C_A_BG,
        border_col=C_A_BORDER,
        title_col=C_TEAL_DARK
    )

    doc.save()

if __name__ == "__main__":
    build_guide()
