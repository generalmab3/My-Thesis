# -*- coding: utf-8 -*-
"""
Defense Guide Generator for Mohammad Amir Babazad's B.Sc. Thesis
University of Bonab - Supervisor: Dr. Babak Azarnavid
Clean, robust Persian typography using ReportLab with exact RTL BiDi rendering.
"""

import os, sys
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib import colors

# Register Persian Fonts
pdfmetrics.registerFont(TTFont('Vazir', 'MAB-THESIS/fonts/Vazirmatn-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Vazir-Bold', 'MAB-THESIS/fonts/Vazirmatn-Bold.ttf'))

class PersianDocBuilder:
    def __init__(self, filename):
        self.filename = filename
        self.c = canvas.Canvas(filename, pagesize=A4)
        self.width, self.height = A4
        self.margin_x = 38
        self.margin_top = 36
        self.margin_bottom = 34
        self.content_width = self.width - 2 * self.margin_x
        self.y = self.height - self.margin_top
        self.page_num = 1

    def reshape_line(self, text, base_dir='R'):
        if not text:
            return ""
        t = str(text).strip()
        reshaped = arabic_reshaper.reshape(t)
        return get_display(reshaped, base_dir=base_dir)

    def wrap_text_rtl(self, text, font_name, font_size, max_w):
        words = str(text).split()
        lines = []
        cur = []
        for w in words:
            test_words = cur + [w]
            test_str = " ".join(test_words)
            shaped = self.reshape_line(test_str, base_dir='R')
            if pdfmetrics.stringWidth(shaped, font_name, font_size) <= max_w:
                cur.append(w)
            else:
                if cur:
                    lines.append(" ".join(cur))
                cur = [w]
        if cur:
            lines.append(" ".join(cur))
        return lines

    def check_page_break(self, needed_height):
        if self.y - needed_height < self.margin_bottom:
            self.draw_footer()
            self.c.showPage()
            self.page_num += 1
            self.y = self.height - self.margin_top
            self.draw_header()

    def draw_header(self):
        self.c.saveState()
        self.c.setFont('Vazir', 8)
        self.c.setFillColor(colors.HexColor('#64748B'))
        hdr = self.reshape_line("راهنمای جامع تسلط بر پایان‌نامه و آمادگی برای جلسه دفاع — دانشگاه بناب", base_dir='R')
        self.c.drawRightString(self.width - self.margin_x, self.height - 23, hdr)
        self.c.setStrokeColor(colors.HexColor('#CBD5E1'))
        self.c.setLineWidth(0.6)
        self.c.line(self.margin_x, self.height - 27, self.width - self.margin_x, self.height - 27)
        self.c.restoreState()

    def draw_footer(self):
        self.c.saveState()
        self.c.setFont('Vazir', 8)
        self.c.setFillColor(colors.HexColor('#64748B'))
        ftr = self.reshape_line(f"صفحه {self.page_num}", base_dir='R')
        self.c.drawCentredString(self.width / 2.0, 19, ftr)
        name = self.reshape_line("محمد امیر بابازاد — استاد راهنما: دکتر بابک آذرنوید", base_dir='R')
        self.c.drawString(self.margin_x, 19, name)
        self.c.setStrokeColor(colors.HexColor('#CBD5E1'))
        self.c.setLineWidth(0.6)
        self.c.line(self.margin_x, 28, self.width - self.margin_x, 28)
        self.c.restoreState()

    def add_title(self, text, subtitle=None, meta=None):
        self.c.setFont('Vazir-Bold', 14.5)
        self.c.setFillColor(colors.HexColor('#003366'))
        shaped = self.reshape_line(text, base_dir='R')
        self.c.drawCentredString(self.width / 2.0, self.y, shaped)
        self.y -= 18
        
        if subtitle:
            self.c.setFont('Vazir', 9.5)
            self.c.setFillColor(colors.HexColor('#334155'))
            shaped_sub = self.reshape_line(subtitle, base_dir='R')
            self.c.drawCentredString(self.width / 2.0, self.y, shaped_sub)
            self.y -= 15

        if meta:
            self.c.setFont('Vazir', 8.5)
            self.c.setFillColor(colors.HexColor('#1E3A8A'))
            shaped_meta = self.reshape_line(meta, base_dir='R')
            self.c.drawCentredString(self.width / 2.0, self.y, shaped_meta)
            self.y -= 13

        self.c.setStrokeColor(colors.HexColor('#003366'))
        self.c.setLineWidth(1.2)
        self.c.line(self.margin_x, self.y, self.width - self.margin_x, self.y)
        self.y -= 10

    def add_heading1(self, text):
        self.check_page_break(40)
        self.y -= 6
        self.c.setFont('Vazir-Bold', 11)
        self.c.setFillColor(colors.HexColor('#003366'))
        shaped = self.reshape_line(text, base_dir='R')
        self.c.drawRightString(self.width - self.margin_x, self.y, shaped)
        self.y -= 4
        self.c.setStrokeColor(colors.HexColor('#003366'))
        self.c.setLineWidth(0.7)
        self.c.line(self.margin_x, self.y, self.width - self.margin_x, self.y)
        self.y -= 9

    def add_heading2(self, text):
        self.check_page_break(26)
        self.y -= 4
        self.c.setFont('Vazir-Bold', 9.8)
        self.c.setFillColor(colors.HexColor('#8B0000'))
        shaped = self.reshape_line(text, base_dir='R')
        self.c.drawRightString(self.width - self.margin_x, self.y, shaped)
        self.y -= 10

    def add_heading3(self, text):
        self.check_page_break(20)
        self.y -= 3
        self.c.setFont('Vazir-Bold', 9)
        self.c.setFillColor(colors.HexColor('#1E3A8A'))
        shaped = self.reshape_line(text, base_dir='R')
        self.c.drawRightString(self.width - self.margin_x, self.y, shaped)
        self.y -= 9

    def add_paragraph(self, text, font_size=8.6, leading=13.0, bold=False, color='#1E293B', indent=0):
        font_name = 'Vazir-Bold' if bold else 'Vazir'
        lines = self.wrap_text_rtl(text, font_name, font_size, self.content_width - indent)
        total_h = len(lines) * leading + 2
        self.check_page_break(total_h)
        
        self.c.setFont(font_name, font_size)
        self.c.setFillColor(colors.HexColor(color))
        
        for l in lines:
            shaped = self.reshape_line(l, base_dir='R')
            self.c.drawRightString(self.width - self.margin_x - indent, self.y, shaped)
            self.y -= leading
        self.y -= 2

    def add_bullet(self, text, bold_prefix="", font_size=8.6, leading=13.0):
        full_text = f"• {bold_prefix} {text}" if bold_prefix else f"• {text}"
        self.add_paragraph(full_text, font_size=font_size, leading=leading, indent=8)

    def add_callout(self, text, title=None, bg_color='#F0F9FF', border_color='#0284C7', title_color='#0369A1'):
        font_size = 8.4
        leading = 12.6
        padding = 6
        inner_w = self.content_width - 2 * padding
        
        title_lines = self.wrap_text_rtl(title, 'Vazir-Bold', 9, inner_w) if title else []
        body_lines = self.wrap_text_rtl(text, 'Vazir', font_size, inner_w)
        
        h = len(title_lines) * 14 + len(body_lines) * leading + 2 * padding + 2
        self.check_page_break(h + 6)
        
        top_y = self.y
        bot_y = self.y - h
        
        self.c.saveState()
        self.c.setFillColor(colors.HexColor(bg_color))
        self.c.setStrokeColor(colors.HexColor(border_color))
        self.c.setLineWidth(0.8)
        self.c.roundRect(self.margin_x, bot_y, self.content_width, h, 3, fill=1, stroke=1)
        self.c.restoreState()
        
        cur_y = top_y - padding - 6
        if title_lines:
            self.c.setFont('Vazir-Bold', 9)
            self.c.setFillColor(colors.HexColor(title_color))
            for l in title_lines:
                shaped = self.reshape_line(l, base_dir='R')
                self.c.drawRightString(self.width - self.margin_x - padding, cur_y, shaped)
                cur_y -= 14
        
        self.c.setFont('Vazir', font_size)
        self.c.setFillColor(colors.HexColor('#1E293B'))
        for l in body_lines:
            shaped = self.reshape_line(l, base_dir='R')
            self.c.drawRightString(self.width - self.margin_x - padding, cur_y, shaped)
            cur_y -= leading
            
        self.y = bot_y - 6

    def add_qa_box(self, question, answer):
        padding = 5.5
        inner_w = self.content_width - 2 * padding
        q_lines = self.wrap_text_rtl(question, 'Vazir-Bold', 8.6, inner_w)
        a_lines = self.wrap_text_rtl(answer, 'Vazir', 8.3, inner_w)
        
        q_h = len(q_lines) * 13 + 2 * padding
        a_h = len(a_lines) * 12.3 + padding + 4
        h = q_h + a_h
        
        self.check_page_break(h + 5)
        
        top_y = self.y
        bot_y = self.y - h
        
        self.c.saveState()
        self.c.setFillColor(colors.HexColor('#F8FAFC'))
        self.c.setStrokeColor(colors.HexColor('#CBD5E1'))
        self.c.setLineWidth(0.6)
        self.c.roundRect(self.margin_x, bot_y, self.content_width, h, 3, fill=1, stroke=1)
        
        # Header strip for question
        self.c.setFillColor(colors.HexColor('#FEF2F2'))
        self.c.rect(self.margin_x, top_y - q_h, self.content_width, q_h, fill=1, stroke=0)
        self.c.setStrokeColor(colors.HexColor('#FECACA'))
        self.c.line(self.margin_x, top_y - q_h, self.width - self.margin_x, top_y - q_h)
        self.c.restoreState()
        
        cur_y = top_y - padding - 4.5
        self.c.setFont('Vazir-Bold', 8.6)
        self.c.setFillColor(colors.HexColor('#991B1B'))
        for l in q_lines:
            shaped = self.reshape_line(l, base_dir='R')
            self.c.drawRightString(self.width - self.margin_x - padding, cur_y, shaped)
            cur_y -= 13
            
        cur_y = top_y - q_h - padding - 4.5
        self.c.setFont('Vazir', 8.3)
        self.c.setFillColor(colors.HexColor('#14532D'))
        for l in a_lines:
            shaped = self.reshape_line(l, base_dir='R')
            self.c.drawRightString(self.width - self.margin_x - padding, cur_y, shaped)
            cur_y -= 12.3
            
        self.y = bot_y - 5.5

    def add_table(self, data, col_widths, headers=None, bg_header='#003366', bg_row1='#FFFFFF', bg_row2='#F8FAFC', col_aligns=None):
        padding = 4
        font_size = 8.0
        leading = 11.8
        
        all_rows = []
        if headers:
            all_rows.append((headers, True))
        for r in data:
            all_rows.append((r, False))
            
        row_heights = []
        row_wrapped_lines = []
        
        if not col_aligns:
            col_aligns = ['R'] * len(col_widths)
            
        for r_idx, (row, is_hdr) in enumerate(all_rows):
            f_name = 'Vazir-Bold' if is_hdr else 'Vazir'
            max_lines = 1
            cols_lines = []
            for c_idx, cell_text in enumerate(row):
                w = col_widths[c_idx] - 2 * padding
                lines = self.wrap_text_rtl(cell_text, f_name, font_size, w)
                cols_lines.append(lines)
                if len(lines) > max_lines:
                    max_lines = len(lines)
            row_wrapped_lines.append(cols_lines)
            row_heights.append(max_lines * leading + 2 * padding)
            
        start_x = self.margin_x
        for r_idx, (row, is_hdr) in enumerate(all_rows):
            h = row_heights[r_idx]
            self.check_page_break(h)
            
            top_y = self.y
            bot_y = self.y - h
            
            self.c.saveState()
            if is_hdr:
                self.c.setFillColor(colors.HexColor(bg_header))
            else:
                self.c.setFillColor(colors.HexColor(bg_row2 if r_idx % 2 == 0 else bg_row1))
            self.c.setStrokeColor(colors.HexColor('#CBD5E1'))
            self.c.setLineWidth(0.5)
            self.c.rect(start_x, bot_y, sum(col_widths), h, fill=1, stroke=1)
            
            # Vertical column lines
            cur_x = start_x
            for w in col_widths[:-1]:
                cur_x += w
                self.c.line(cur_x, bot_y, cur_x, top_y)
            self.c.restoreState()
            
            f_name = 'Vazir-Bold' if is_hdr else 'Vazir'
            t_color = '#FFFFFF' if is_hdr else '#1E293B'
            self.c.setFont(f_name, font_size)
            self.c.setFillColor(colors.HexColor(t_color))
            
            cols_lines = row_wrapped_lines[r_idx]
            for c_idx, lines in enumerate(cols_lines):
                col_left = start_x + sum(col_widths[c_idx+1:])
                col_right = col_left + col_widths[c_idx]
                align = col_aligns[c_idx] if not is_hdr else 'C'
                
                text_y = top_y - padding - 5.5
                for l in lines:
                    shaped = self.reshape_line(l, base_dir='R')
                    if align == 'C':
                        self.c.drawCentredString((col_left + col_right) / 2.0, text_y, shaped)
                    elif align == 'L':
                        self.c.drawString(col_left + padding, text_y, shaped)
                    else:
                        self.c.drawRightString(col_right - padding, text_y, shaped)
                    text_y -= leading
                    
            self.y = bot_y
        self.y -= 7

    def save(self):
        self.draw_footer()
        self.c.save()
        print(f"Generated comprehensive guide: {self.filename} ({self.page_num} pages)")

def generate():
    doc = PersianDocBuilder("MAB-THESIS/Defense_Guide.pdf")
    
    # ------------------ SECTION 1: TITLE & BIG PICTURE ------------------
    doc.add_title(
        "راهنمای جامع تسلط بر پایان‌نامه و آمادگی برای جلسه دفاع",
        "حل مسئله مستقیم معادله غیرخطی برگرز با استفاده از شبکه‌های عصبی آگاه از فیزیک (PINN)",
        "پژوهشگر: محمد امیر بابازاد  |  استاد راهنما: دکتر بابک آذرنوید  |  دانشگاه بناب — شهریور ۱۴۰۵"
    )
    
    doc.add_callout(
        "این راهنمای جامع و اختصاصی برای این تدوین شده است تا بدون نیاز به دانش عمیق پیشین در ریاضیات پیشرفته یا یادگیری عمیق، به تمام مفاهیم، فرمول‌ها، مراحل الگوریتمی آموزش در جکس، نتایج تجربی و منطق علمی پایان‌نامه خود تسلط ۱۰۰ درصدی پیدا کنید و با اعتمادبه‌نفس کامل در جلسه دفاع حاضر شده و نمره عالی کسب نمایید.",
        title="پیام مهم به پژوهشگر (چگونه از این جزوه استفاده کنید؟)",
        bg_color="#EFF6FF", border_color="#3B82F6", title_color="#1D4ED8"
    )

    doc.add_heading1("۱. تصویر کلان و منطق علمی پایان‌نامه به زبان ساده و ملموس")
    
    doc.add_heading2("هدف بنیادی پایان‌نامه چیست؟")
    doc.add_paragraph("هدف ما محاسبه و پیش‌بینی سرعت یک سیال پیوسته (مانند هوا یا آب در لوله، یا سرعت خودروها در جریان ترافیک جاده‌ای) در سراسر فضا و زمان است. در فیزیک، تغییرات و اندرکنش این جریان‌ها با یک معادله دیفرانسیل جزئی غیرخطی بسیار معروف به نام «معادله برگرز» مدل‌سازی می‌شود.")

    doc.add_heading2("چرا روش‌های محاسباتی سنتی در حل این مسئله با چالش روبه‌رو می‌شوند؟")
    doc.add_paragraph("روش‌های سنتی مهندسی نظیر تفاضل‌های محدود (FDM) و اجزای محدود (FEM) مجبورند کل فضا و زمان را به شبکه‌ای از نقاط (توری یا مش محاسباتی) تقسیم کنند. این کار سه ایراد اساسی دارد: ۱. در ابعاد بالا، تعداد خانه‌های شبکه منفجر شده و با پدیده نفرین ابعاد و هزینه محاسباتی فوق‌العاده سنگین روبه‌رو می‌شویم. ۲. روی هندسه‌های نامنظم، ساخت شبکه محاسباتی بسیار پیچیده و دشوار است. ۳. به دلیل تقریب گسسته مشتقات، همواره خطای برش عددی وجود دارد.")

    doc.add_heading2("چرا هوش مصنوعی و یادگیری عمیق معمولی (صرفا داده‌محور) برای این کار کافی نیست؟")
    doc.add_paragraph("شبکه‌های عصبی معمولی مانند جعبه سیاه عمل می‌کنند؛ یعنی نیازمند هزاران نقطه داده تجربی و آزمایشگاهی هستند تا رفتار سیستم را یاد بگیرند. اما در سامانه‌های واقعی فیزیکی و مهندسی (نظیر داخل موتور جت یا اعماق چاه‌های نفت)، نصب حسگر و ثبت داده پیوسته عملا غیرممکن است. اگر داده کم باشد، شبکه معمولی دچار بیش‌برازش شده و در نواحی بدون حسگر، پیش‌بینی‌های غیرمنطقی تولید می‌کند که قوانین پایه‌ای فیزیک (نظیر بقای جرم و انرژی) را نقض می‌نماید.")

    doc.add_heading2("شاهکار این پایان‌نامه و ایده کلیدی شبکه آگاه از فیزیک (PINN) چیست؟")
    doc.add_paragraph("ما به جای وابستگی به داده‌های انبوه آزمایشگاهی، خود «قانون فیزیک» (معادله دیفرانسیل برگرز) را وارد تابع هدف و مغز شبکه عصبی می‌کنیم. شبکه عصبی با استفاده از فناوری «مشتق‌گیری خودکار» در کتابخانه جکس، یاد می‌گیرد خروجی‌ای تولید کند که هم شرایط اولیه و مرزی محدود را برآورده کند و هم باقیمانده معادله فیزیک در کل دامنه فضا-زمان صفر شود. به این چارچوب یکپارچه، «شبکه عصبی آگاه از فیزیک» یا PINN می‌گویند.")

    # ------------------ SECTION 2: CHAPTER BY CHAPTER BREAKDOWN ------------------
    doc.add_heading1("۲. خلاصه و کالبدشکافی محتوای فصول پایان‌نامه (فصل به فصل)")
    
    doc.add_heading2("فصل اول: مقدمه و کلیات پژوهش (صفحات ۱۲ تا ۱۷)")
    doc.add_bullet("طرح موضوع و بیان مسئله (بخش ۱-۱ و ۱-۲): تبیین ناکارآمدی روش‌های سنتی مبتنی بر شبکه محاسباتی و شکست مدل‌های داده‌محور در سناریوهای کم‌داده فیزیکی.", "محور اول:")
    doc.add_bullet("تعریف مسئله مستقیم (Forward Problem): ساختار معادله و ضرایب فیزیکی (ضریب لزجت) کاملاً معلوم است و هدف محاسبه میدان پیوسته پاسخ u(t,x) در کل فضا-زمان است.", "محور دوم:")
    doc.add_bullet("معادله برگرز و چالش جبهه شوک: توضیح چرایی انتخاب معادله برگرز به خاطر تشکیل پدیده موج شوک (افت ناگهانی سرعت در فاصله مکانی بسیار کوتاه) به عنوان مسئله معیار سنجش الگوریتم‌ها.", "محور سوم:")
    doc.add_bullet("بستر نرم‌افزاری جکس (JAX): پیاده‌سازی مدل زمان‌پیوسته با تبدیل‌های تابعی مشتق‌گیری، بردارسازی خودکار، کامپایل در زمان اجرا و استراتژی بهینه‌سازی ترکیبی.", "محور چهارم:")

    doc.add_heading2("فصل دوم: مبانی نظری و پیشینه پژوهش (صفحات ۱۸ تا ۲۵)")
    doc.add_bullet("معادلات دیفرانسیل جزئی (بخش ۲-۱): معرفی معادله گرما (پخشی خالص)، معادله برگرز (رقابت همرفت غیرخطی u*u_x و لزجت پخشی nu*u_xx) و معادله غیرخطی شرودینگر.", "معادلات فیزیکی:")
    doc.add_bullet("روش‌های عددی کلاسیک (بخش ۲-۲): مقایسه ۳ روش اصلی در جدول ۲-۱ (تفاضل‌های محدود، اجزای محدود، روش‌های طیفی) و تبیین محدودیت‌های آن‌ها در ابعاد بالا و هندسه‌های نامنظم.", "روش‌های کلاسیک:")
    doc.add_bullet("شبکه‌های عصبی مصنوعی (بخش ۲-۳): تشریح ساختار پرسپترون چندلایه (MLP)، مقایسه توابع فعال‌ساز (جدول ۲-۲) و اثبات ریاضی قضیه تقریب عمومی سیبنکو (Cybenko).", "ساختار شبکه:")
    doc.add_bullet("آموزش شبکه‌های عمیق (بخش ۲-۴): تابع خطای MSE، گرادیان کاهشی و پس‌انتشار خطا، معرفی بهینه‌ساز آدام (Adam) با روابط گشتاور اول و دوم، بهینه‌ساز شبه‌نیوتنی L-BFGS و مقداردهی گزاویه (Xavier).", "بهینه‌سازی:")
    doc.add_bullet("پیشینه تاریخی (بخش ۲-۵): سیر تحول از ایده لاگاریس در ۱۹۹۸ تا مدل‌های فرآیند گاوسی (۲۰۱۷)، روش SINDy برانتون و شاهکار مقاله ۲۰۱۹ رئیسی، پردیکاریس و کارنیاداکیس.", "سیر تحول علمی:")

    doc.add_heading2("فصل سوم: شبکه‌های عصبی آگاه از فیزیک — روش پژوهش (صفحات ۲۶ تا ۳۶)")
    doc.add_paragraph("این فصل مهم‌ترین بخش متدولوژی پایان‌نامه شماست و شامل محورهای زیر است:", bold=True, color='#003366')
    doc.add_bullet("ایده محوری و صورت‌بندی کلی (بخش ۳-۱): تعریف عملگر باقیمانده فیزیک f = u_t + N[u] و تابع هزینه دوقلو، همراه با دیاگرام بلوکی شکل ۳-۱.", "صورت‌بندی مسئله:")
    doc.add_bullet("مشتق‌گیری خودکار (بخش ۳-۲): مقایسه مشتق‌گیری نمادین (تورم جبری عبارات)، مشتق‌گیری عددی (تعارض خطای برش و گردکردن) و مشتق‌گیری خودکار. تشریح حساب اعداد دوگانه (Dual Numbers با خاصیت اپسیلون به توان دو مساوی صفر) و معرفی حالت مستقیم (JVP) و معکوس (VJP).", "مشتق‌گیری خودکار:")
    doc.add_bullet("به‌کارگیری AD در معادله برگرز (بخش ۳-۳): تشریح ۵ گام تفصیلی ریاضی و الگوریتمی از تعریف نگاشت سرعت، استخراج تحلیلی مشتقات زمانی و مکانی با قاعده زنجیره‌ای، تشکیل باقیمانده جبری، ساختار دو سطحی AD و پیاده‌سازی تابعی در JAX.", "حل برگرز با AD:")
    doc.add_bullet("مدل‌های زمانی (بخش ۳-۴ و ۳-۵): فرمول‌بندی مدل زمان‌پیوسته با ۲۰۰ نقطه مرزی و ۱۰۰۰۰ نقطه هم‌مکانی در برابر مدل زمان‌گسسته رانگه-کوتا ضمنی (IRK) با جدول بوچر (جدول ۳-۱).", "پیوسته و گسسته:")
    doc.add_bullet("ملاحظات عملیاتی (بخش ۳-۶): توجیه انتخاب ۴ لایه پنهان، ۵۰ نورون، تابع فعال‌ساز Tanh، استراتژی بهینه‌سازی ترکیبی Adam و L-BFGS و نمونه‌برداری متمرکز در ناحیه شوک.", "نکات عملی:")

    doc.add_heading2("فصل چهارم: پیاده‌سازی و ارزیابی نتایج (صفحات ۳۷ تا ۴۳)")
    doc.add_bullet("بستر محاسباتی (بخش ۴-۱): استفاده از پایتون ۳.۱۱ و کتابخانه JAX با دقت ممیز شناور ۶۴ بیتی (Float64) برای به صفر رساندن خطاهای گردکردن.", "بستر نرم‌افزاری:")
    doc.add_bullet("روند آموزش در JAX (بخش ۴-۲): تشریح جامع خط لوله تبدیلات تابعی (grad, vmap, jit, value_and_grad)، مقداردهی گزاویه و استراتژی بهینه‌سازی دو مرحله‌ای.", "روند آموزش:")
    doc.add_bullet("نتایج حل مستقیم برگرز (بخش ۴-۳): اجرای آموزش ترکیبی شامل ۶۰۰۰ گام Adam و سپس L-BFGS-B، کاهش خطای هزینه از مرتبه منفی ۳ به منفی ۵.", "فرآیند آموزش:")
    doc.add_bullet("ارزیابی مقایسه‌ای با مقاله مرجع رئیسی ۲۰۱۹ (بخش ۴-۴): تحلیل جدول مقایسه تطبیقی (جدول ۴-۲) و نشان دادن بازتولید وفادارانه موقعیت و شیب تیز شوک.", "مقایسه با مرجع:")

    doc.add_heading2("فصل پنجم: نتیجه‌گیری و پیشنهادها (صفحات ۴۴ تا ۴۶)")
    doc.add_bullet("اثبات توانمندی PINN در حل بدون شبکه معادلات غیرخطی و به دام انداختن امواج شوک تنها با ۲۰۰ نقطه مرزی و قید فیزیک.", "یافته‌های کلیدی:")
    doc.add_bullet("پیشنهادهای آتی: ۱. استفاده از توابع فعال‌ساز تطبیقی، ۲. به‌کارگیری شبکه‌های عصبی فوریه، ۳. وزن‌دهی پویا به بخش‌های تابع هزینه، ۴. توسعه به مدل‌های دو‌بعدی و سه‌بعدی ناویه-استوکس.", "کارهای آینده:")

    # ------------------ SECTION 3: KEY NUMBERS & PARAMETERS ------------------
    doc.add_heading1("۳. جدول جامع مشخصات، مقادیر عددی و نتایج تجربی پایان‌نامه")
    doc.add_paragraph("این جدول حاوی تمامی مقادیر عددی و پارامترهایی است که باید دقیقاً در ذهن داشته باشید:", bold=True, color='#003366')
    
    table_data = [
        ["معادله دیفرانسیل آزمون", "معادله غیرخطی برگرز با لزجت", "u_t + u u_x - nu u_xx = 0"],
        ["ضریب لزجت سینماتیکی (nu)", "0.01 / pi (حدود 0.003183)", "هر چه کوچکتر باشد شوک تیزتر و حل سخت‌تر است"],
        ["دامنه حل فضا-زمان", "بازه مکانی ۱- تا ۱+ و زمانی ۰ تا ۱", "دامنه پیوسته دوبعدی بدون شبکه‌بندی گسسته"],
        ["شرط اولیه و مرزی", "شرط اولیه سینوسی و مرزهای همگن دیریکله", "u(0,x) = -sin(pi x) | u(t,-1) = u(t,1) = 0"],
        ["داده‌های مرزی و اولیه (N_u)", "۲۰۰ نقطه (۱۰۰ مرزی + ۱۰۰ اولیه)", "تنها داده‌های برچسب‌دار معلوم در کل مسئله"],
        ["نقاط هم‌مکانی باقیمانده (N_f)", "۱۰۰۰۰ نقطه درون دامنه فضا-زمان", "نمونه‌برداری متمرکز در حوالی خط شوک x=0"],
        ["معماری شبکه عصبی", "۴ لایه پنهان، ۵۰ نورون در هر لایه", "تابع فعال‌ساز تانژانت هیپربولیک (Tanh)"],
        ["تعداد کل پارامترها", "۷۸۵۱ پارامتر وزن و بایاس", "مقداردهی اولیه با روش یکنواخت گزاویه"],
        ["استراتژی آموزش مدل", "ترکیبی دو مرحله‌ای: Adam + L-BFGS", "۶۰۰۰ گام آدام (نرخ 0.001) سپس همگرایی L-BFGS"],
        ["دقت ممیز شناور ماشین", "۶۴ بیتی (Float64)", "جهت حفظ بالاترین دقت و حذف خطای گردکردن"],
        ["خطای نسبی نهایی در نرم L2", "2.15e-2 (معادل ۲.۱۵ درصد)", "میزان انحراف شبکه از میدان پاسخ معیار"],
        ["خطای باقیمانده فیزیک", "MSE_f = 6.36e-5", "نشان‌دهنده ارضای فوق‌العاده قوی قانون فیزیک"],
        ["خطای داده‌های مرزی", "MSE_u = 2.35e-5", "انطباق عالی خروجی شبکه با شرایط مرزی و اولیه"],
        ["مقایسه با Raissi 2019", "هم‌خوانی کیفی عالی در بازتولید گرادیان", "بازتولید موفقیت‌آمیز جبهه شوک مقاله مرجع"]
    ]
    doc.add_table(table_data, [130, 185, 204], headers=["شاخص و پارامتر", "مقدار در این پژوهش", "توضیح مفهومی"], bg_header="#003366", col_aligns=['R', 'C', 'R'])

    # ------------------ SECTION 4: FIGURE INTERPRETATION & JAX PIPELINE ------------------
    doc.add_heading1("۴. تشریح دقیق نمودارهای فصل ۴ و مکانیزم ۵ مرحله‌ای آموزش با JAX")
    
    doc.add_heading2("تحلیل مفهومی شکل‌ها و نمودارهای فصل ۴:")
    doc.add_bullet("شکل ۴-۱ (توزیع نقاط آموزش): این شکل نشان می‌دهد که چگونه ۲۰۰ نقطه با رنگ قرمز روی مرزهای مکانی و لحظه آغازین قرار گرفته‌اند و ۱۰۰۰۰ نقطه خاکستری در سراسر صفحه فضا-زمان پخش شده‌اند. تراکم بالاتر نقاط در خط مرکزی x=0 نشان‌دهنده راهبرد نمونه‌برداری متمرکز در ناحیه تشکیل شوک است.", "شکل ۴-۱:")
    doc.add_bullet("شکل ۴-۲ (تاریخچه همگرایی توابع هزینه): این نمودار لگاریتمی نشان می‌دهد که در فاز اول (بهینه‌ساز Adam)، خطای کل با شیب مناسب افت می‌کند و پس از گام ۶۰۰۰ با ورود بهینه‌ساز شبه‌نیوتنی L-BFGS، خطا دچار یک ریزش شارپ شده و به دقت ۱۰ به توان منفی ۵ می‌رسد.", "شکل ۴-۲:")
    doc.add_bullet("شکل ۴-۳ (مقاطع زمانی پاسخ در زمان‌های t=0.25, 0.50, 0.75): این نمودار قلب نتایج شماست! خطوط ممتد مشکی جواب معیار و خطوط خط‌چین قرمز پیش‌بینی PINN هستند. مشاهده می‌کنید که موج سینوسی هموار اولیه با گذر زمان به سمت مرکز متمایل شده و در حوالی x=0 یک افت عمودی و دیوارمانند (جبهه شوک) ایجاد می‌کند و مدل با دقت عالی آن را بازسازی کرده است.", "شکل ۴-۳:")
    doc.add_bullet("شکل ۴-۴ (نقشه خطای دوبعدی): نمودار کانتور رنگی نشان می‌دهد که در بیش از ۹۵ درصد مساحت دامنه فضا-زمان، خطا به رنگ تیره (نزدیک به صفر) است و بیشینه خطای اندک مدل فقط در امتداد نوار بسیار باریک خط شوک (برای زمان‌های بعد از 0.3) متمرکز است.", "شکل ۴-۴:")

    doc.add_heading2("روند الگوریتمی ۵ مرحله‌ای اجرای مدل در کتابخانه جکس (JAX):")
    doc.add_bullet("گام اول (مقداردهی اولیه پارامترها): وزن‌های شبکه با توزیع یکنواخت گزاویه (گلوروت) بر اساس تعداد نورون‌های ورودی و خروجی مقداردهی شده و بایاس‌ها با صفر آغاز می‌شوند تا پایداری گرادیان‌ها حفظ شود.", "گام اول:")
    doc.add_bullet("گام دوم (تبدیلات تابعی و مشتق‌گیری): تابع پیش‌بینی u_net تعریف شده و مشتقات زمانی و مکانی u_t, u_x, u_xx با استفاده از تبدیل تابعی jax.grad به‌صورت تحلیلی و تودرتو استخراج می‌گردند.", "گام دوم:")
    doc.add_bullet("گام سوم (بردارسازی و کامپایل JIT): با استفاده از jax.vmap ارزیابی نقاط به صورت دسته‌ای و برداری درمی‌آید و با jax.jit کل گراف محاسباتی با کامپایلر XLA به کد ماشین بهینه تبدیل می‌شود.", "گام سوم:")
    doc.add_bullet("گام چهارم (محاسبه هم‌زمان تابع هزینه و گرادیان): با استفاده از jax.value_and_grad، مقدار تابع هزینه ترکیبی (MSE_u + MSE_f) و بردار گرادیان آن نسبت به پارامترهای شبکه در یک گذر مشترک و سریع به دست می‌آید.", "گام چهارم:")
    doc.add_bullet("گام پنجم (استراتژی بهینه‌سازی دو مرحله‌ای): ابتدا ۶۰۰۰ تکرار با بهینه‌ساز Adam برای فرار از کمینه‌های محلی اجرا شده و سپس آموزش با روش شبه‌نیوتنی L-BFGS-B تا رسیدن به همگرایی عمیق ادامه می‌یابد.", "گام پنجم:")

    # ------------------ SECTION 5: GLOSSARY OF KEY TERMS ------------------
    doc.add_heading1("۵. فرهنگ لغت اصطلاحات کلیدی و تخصصی پایان‌نامه")
    
    terms_data = [
        ["معادله برگرز (Burgers Eq)", "یک PDE غیرخطی بنیادین که رقابت دو اثر همرفت (انتقال غیرخطی) و لزجت (پخش اصطکاکی) را توصیف می‌کند."],
        ["موج شوک (Shock Wave)", "ناحیه بسیار فشرده‌ای که مشخصات جریان (مثل سرعت) در فاصله مکانی فوق‌العاده کوتاهی دچار افت یا جهش شدید می‌شود."],
        ["مسئله مستقیم (Forward Problem)", "مسئله‌ای که ساختار معادله و شرایط مرزی-اولیه معلوم است و هدف محاسبه میدان پاسخ زمانی-مکانی u(t,x) است."],
        ["مشتق‌گیری خودکار (AutoDiff / AD)", "تکنیک ارزیابی دقیق مشتقات برنامه‌های کامپیوتری با اعمال قاعده زنجیره‌ای روی گراف محاسباتی با دقت اعشار ماشین."],
        ["نقاط هم‌مکانی (Collocation Points)", "نقاطی در درون دامنه که داده سنسوری نداریم، اما معادله فیزیک در آن‌ها ارزیابی و باقیمانده آن صفر می‌شود."],
        ["کامپایل در زمان اجرا (JIT / XLA)", "فناوری کامپایل توابع پایتون به کدهای بهینه‌سازی‌شده ماشین که سرعت محاسبات را تا چندین برابر افزایش می‌دهد."],
        ["بهینه‌ساز شبه‌نیوتنی L-BFGS", "یک الگوریتم بهینه‌سازی مرتبه دوم که با تقریب ماتریس معکوس هشین، همگرایی فوق‌خطی و دقت بسیار بالایی ایجاد می‌کند."],
        ["بردارسازی خودکار (VMAP)", "قابلیت کتابخانه JAX برای اجرای موازی و برداری توابع روی دسته‌های بزرگ داده بدون نیاز به حلقه‌های کند پایتون."]
    ]
    doc.add_table(terms_data, [160, 359], headers=["اصطلاح تخصصی", "تعریف و کاربرد در پایان‌نامه"], bg_header="#1E3A8A", col_aligns=['R', 'R'])

    # ------------------ SECTION 6: GOLD DEFENSE Q&A (12 QUESTIONS) ------------------
    doc.add_heading1("۶. بانک جامع ۱۲ سؤال طلایی داوران و پاسخ‌های مسلط و دفاع‌محور")
    doc.add_paragraph("این سؤالات رایج‌ترین و کلیدی‌ترین پرسش‌های هیئت داوران در جلسات دفاع یادگیری عمیق و PINN هستند. پاسخ‌های زیر را به دقت مطالعه کنید:", bold=True, color='#003366')
    
    doc.add_qa_box(
        "سؤال ۱: تفاوت بنیادی مشتق‌گیری خودکار (AD) با مشتق‌گیری عددی (مثل تفاضل محدود) چیست؟",
        "پاسخ شما: مشتق‌گیری عددی مبتنی بر بسط تیلور با طول گام h است که دچار دو خطای متضاد می‌شود: اگر h بزرگ باشد خطای برش داریم و اگر h خیلی کوچک باشد خطای گردکردن ممیز شناور ناشی از تفریق اعداد بسیار نزدیک رخ می‌دهد. علاوه بر این، نیازمند شبکه‌بندی دامنه است. در مقابل، مشتق‌گیری خودکار نه عددی است و نه نمادین، بلکه با ساخت گراف محاسباتی کد و اعمال نظام‌مند قاعده زنجیره‌ای، مشتقات جزئی را با دقت تحلیلی کامپیوتر و بدون هیچ‌گونه خطای برش در زمان اجرای برنامه ارزیابی می‌کند."
    )
    
    doc.add_qa_box(
        "سؤال ۲: چرا در معماری شبکه عصبی از تابع فعال‌ساز Tanh استفاده کردید و چرا از ReLU استفاده نکردید؟",
        "پاسخ شما: در معادله غیرخطی برگرز به مشتق مرتبه دوم مکانی (u_xx) برای مدل‌سازی جمله لزجت و پخش سینماتیکی نیاز داریم. تابع فعال‌ساز ReLU یک تابع پیوسته اما تکه‌ای خطی است که مشتق اول آن پله‌ای و مشتق دوم آن در همه نقاط صفر است؛ بنابراین با ReLU نمی‌توان جملات دیفرانسیلی مرتبه دو را تشکیل داد. در مقابل، تابع تانژانت هیپربولیک (Tanh) یک تابع هموار و بی‌نهایت‌بار مشتق‌پذیر (C-infinity) است که مشتقات اول و دوم تحلیلی غیرصفر تولید می‌نماید."
    )
    
    doc.add_qa_box(
        "سؤال ۳: چرا فرآیند آموزش را به صورت دو مرحله‌ای (ابتدا Adam و سپس L-BFGS) طراحی کردید؟",
        "پاسخ شما: توابع هزینه در شبکه‌های آگاه از فیزیک غیرخطی و پیچیده بوده و دارای کمینه‌های محلی متعددی هستند. بهینه‌ساز آدام با بهره‌گیری از گشتاور اول و دوم گرادیان‌ها در مراحل اولیه در فرار از کمینه‌های محلی و کاهش سریع خطا بسیار توانمند است، اما در نزدیکی نقطه بهینه همگرایی کندی دارد. در مقابل، بهینه‌ساز شبه‌نیوتنی L-BFGS با تقریب ماتریس هشین، در نزدیکی کمینه سراسری سرعت همگرایی فوق‌خطی و مرتبه دو دارد. ترکیب این دو روش بالاترین پایداری و بیشترین دقت نهایی را تضمین می‌کند."
    )
    
    doc.add_qa_box(
        "سؤال ۴: نقاط هم‌مکانی (Collocation Points) چیستند، چند تا بودند و چرا چگالی آن‌ها در حوالی x=0 بیشتر بود؟",
        "پاسخ شما: نقاط هم‌مکانی نقاطی درون دامنه پیوسته فضا-زمان هستند که هیچ داده اندازه‌گیری تجربی یا برچسبی برای آن‌ها نداریم، اما باقیمانده معادله فیزیک در آن‌ها ارزیابی و صفر می‌شود. در این پژوهش ۱۰۰۰۰ نقطه هم‌مکانی استفاده شد. از آن‌جا که در معادله برگرز پدیده موج شوک و گرادیان‌های بسیار شدید سرعت در حوالی خط مرکزی x=0 (برای زمان‌های t>0.3) رخ می‌دهد، نمونه‌برداری متمرکز در این ناحیه باعث شد که شبکه عصبی رزولوشن بالاتری در یادگیری جبهه تیز شوک داشته باشد."
    )
    
    doc.add_qa_box(
        "سؤال ۵: چرا کتابخانه جکس (JAX) را برای پیاده‌سازی انتخاب کردید و چه مزیتی نسبت به PyTorch یا TensorFlow دارد؟",
        "پاسخ شما: جکس مبتنی بر پارادایم برنامه‌نویسی تابعی محض طراحی شده و با ارائه تبدیل‌های تابعی ترکیب‌پذیر نظیر grad برای مشتق‌گیری مراتب بالا، vmap برای بردارسازی خودکار بدون حلقه‌های پایتون و jit برای کامپایل بهینه‌ساز XLA، سرعت محاسباتی فوق‌العاده بالا و ساختار کدی بسیار شفاف و مستقیمی را برای فرمول‌بندی معادلات دیفرانسیل فراهم می‌سازد."
    )

    doc.add_qa_box(
        "سؤال ۶: چرا مسئله معکوس (Inverse Problem) را بررسی نکردید و روی مسئله مستقیم متمرکز شدید؟",
        "پاسخ شما: به راهنمایی استاد محترم راهنما (جناب آقای دکتر آذرنوید)، برای حفظ تمرکز عمیق علمی پژوهش بر روی چالش‌های محاسباتی بازسازی جبهه‌های نوک‌تیز موج شوک و بررسی دقیق توزیع مکانی-زمانی خطا و مقایسه جامع با نتایج مقاله مرجع معتبر رئیسی و همکاران (۲۰۱۹)، دامنه این پایان‌نامه به‌طور تخصصی و دقیق بر حل مسئله مستقیم معطوف گردید."
    )

    doc.add_qa_box(
        "سؤال ۷: نقش ضریب لزجت (nu = 0.01/pi) در رفتار معادله برگرز چیست و اگر این مقدار کمتر شود چه اتفاقی می‌افتد؟",
        "پاسخ شما: ضریب لزجت سینماتیکی (nu) بیانگر شدت پخش و اصطکاک در جریان است که تمایل به هموارسازی امواج دارد. در مقابل، جمله غیرخطی u*u_x تمایل به جلو کشیدن موج و ایجاد ناپیوستگی شوک دارد. هر چه ضریب لزجت کوچکتر باشد، اثر اصطکاک کمتر شده و جبهه شوک نوک‌تیزتر، شیب‌دارتر و باریک‌تر می‌شود و چالش تقریب شبکه عصبی به شدت افزایش می‌یابد."
    )
    
    doc.add_qa_box(
        "سؤال ۸: آیا شبکه عصبی PINN دچار بیش‌برازش (Overfitting) نمی‌شود؟ چرا از Dropout استفاده نکردید؟",
        "پاسخ شما: خیر؛ در شبکه‌های آگاه از فیزیک به دلیل وجود جمله خطای باقیمانده فیزیک (MSE_f)، کل فضای فرضیات شبکه به توابعی محدود می‌شود که قوانین بقا و معادله دیفرانسیل حاکم را ارضا کنند. این قید فیزیکی در حقیقت نقش یک منظم‌ساز (Regularizer) ساختاری بسیار قدرتمند را ایفا می‌کند که مانع بیش‌برازش می‌شود؛ بنابراین نیازی به استفاده از تکنیک‌های تجربی مثل لایه‌های دراپ‌اوت (Dropout) وجود ندارد."
    )
    
    doc.add_qa_box(
        "سؤال ۹: ساختار دو سطحی مشتق‌گیری خودکار که در فصل ۳ تشریح شده است دقیقاً یعنی چه؟",
        "پاسخ شما: مشتق‌گیری خودکار در PINN در دو سطح مجزا عمل می‌کند: ۱. سطح اول (مشتق‌گیری داخلی نسبت به متغیرهای فیزیکی فضا-زمان): که مشتقات u_t، u_x و u_xx را نسبت به ورودی‌های مختصاتی (t,x) برای تشکیل معادله باقیمانده f حساب می‌کند. ۲. سطح دوم (مشتق‌گیری خارجی نسبت به پارامترهای شبکه): که پس از محاسبه تابع هزینه کل، گرادیان آن را نسبت به وزن‌ها و بایاس‌های شبکه (grad_theta Loss) برای آموزش مدل محاسبه می‌نماید."
    )
    
    doc.add_qa_box(
        "سؤال ۱۰: خطای ۲.۱۵ درصدی به دست آمده در مقایسه با مقاله مرجع رئیسی (۲۰۱۹) چگونه ارزیابی می‌شود؟",
        "پاسخ شما: در مقاله بنیادین رئیسی و همکاران (۲۰۱۹) خطای نسبی L2 در حدود ۶.۷ در ۱۰ به توان منفی ۴ گزارش شده است که حاصل بهینه‌سازی بسیار طولانی تا ده‌ها هزار تکرار L-BFGS و ۵۰ هزار نقطه هم‌مکانی بر روی کارت‌های گرافیکی تخصصی بوده است. در پژوهش حاضر با ۶۰۰۰ گام Adam و بهینه‌سازی متعادل L-BFGS با ۱۰۰۰۰ نقطه بر بستر پردازنده مرکزی استاندارد، به خطای ۲.۱۵ درصدی رسیدیم که از نظر کیفی موقعیت و شیب تیز شوک را در تمام مقاطع زمانی با وفاداری بسیار بالا بازتولید کرده است."
    )

    doc.add_qa_box(
        "سؤال ۱۱: تفاوت مدل زمان‌پیوسته و زمان‌گسسته چیست و چرا مدل زمان‌پیوسته را پیاده‌سازی کردید؟",
        "پاسخ شما: در مدل زمان‌پیوسته، فضا و زمان به صورت هم‌زمان به شبکه داده می‌شوند و شبکه خروجی پیوسته u(t,x) را در کل دامنه برمی‌گرداند. در مدل زمان‌گسسته، با استفاده از روش‌های رانگه-کوتا ضمنی (IRK) گام‌زنی زمانی انجام می‌شود و شبکه جواب را در مراحل میانی تقریب می‌زند. مدل زمان‌پیوسته به دلیل ساختار یکپارچه، سادگی محاسباتی و توانایی ارزیابی در هر لحظه دلخواه زمانی، انتخاب اصلی این پایان‌نامه بوده است."
    )

    doc.add_qa_box(
        "سؤال ۱۲: آیا این چارچوب برای معادلات دوبعدی، سه‌بعدی و هندسه‌های نامنظم هم کاربرد دارد؟",
        "پاسخ شما: بله؛ بزرگترین مزیت PINN بدون شبکه (Mesh-Free) بودن آن است. در ابعاد بالاتر، کافی است بردار ورودی شبکه از (t,x) به (t,x,y,z) گسترش یابد و نقاط هم‌مکانی درون هندسه نامنظم نمونه‌برداری شوند، بدون اینکه نیازی به تولید توری یا المان‌بندی‌های پیچیده مهندسی باشد."
    )

    # ------------------ SECTION 7: DEFENSE PRESENTATION SCRIPT & SLIDES ------------------
    doc.add_heading1("۷. سناریوی گام‌به‌گام و زمان‌بندی ارائه دفاعیه (۲۰ دقیقه سخنرانی بی‌نقص)")
    doc.add_paragraph("اگر می‌خواهید یک ارائه روان، مسلط و بدون استرس داشته باشید، اسلایدهای خود را طبق زمان‌بندی استاندارد زیر تقسیم‌بندی کنید:", bold=True, color='#003366')
    
    slide_data = [
        ["اسلاید ۱ و ۲\n(۲ دقیقه)", "عنوان، خوش‌آمدگویی و بیان مسئله", "معرفی خود و استاد راهنما؛ توضیح اینکه روش‌های سنتی وابسته به مش‌بندی هستند و هوش مصنوعی معمولی نیازمند داده بسیار زیاد است و در غیاب داده قوانین فیزیک را نقض می‌کند."],
        ["اسلاید ۳ و ۴\n(۳ دقیقه)", "معادله برگرز و چالش شوک", "معرفی فرمول برگرز و توضیح رقابت همرفت و پخش؛ توضیح اینکه تشکیل جبهه تیز شوک به عنوان یک مسئله معیار در مکانیک سیالات و ترافیک مطرح است."],
        ["اسلاید ۵ و ۶\n(۳ دقیقه)", "ایده محوری PINN و مشتق‌گیری خودکار", "نمایش دیاگرام بلوکی فصل ۳؛ توضیح اینکه مشتق‌گیری خودکار با قاعده زنجیره‌ای در JAX مشتقات فیزیکی u_t, u_x, u_xx را بدون نیاز به شبکه محاسباتی حساب می‌کند."],
        ["اسلاید ۷ و ۸\n(۳ دقیقه)", "تابع هزینه دوقلو و ساختار الگوریتمی JAX", "تشریح تابع خطای Loss = MSE_u + MSE_f با ۲۰۰ نقطه مرزی و ۱۰۰۰۰ نقطه هم‌مکانی؛ توضیح خط لوله کامپایل JIT و بردارسازی VMAP در جکس."],
        ["اسلاید ۹ و ۱۰\n(۲ دقیقه)", "استراتژی آموزش ترکیبی Adam و L-BFGS", "توضیح روند دو مرحله‌ای: ۶۰۰۰ گام Adam برای فرار از کمینه‌های محلی و سپس ادامه با L-BFGS برای همگرایی سریع به دقت ۱۰ به توان منفی پنج."],
        ["اسلاید ۱۱ تا ۱۳\n(۵ دقیقه)", "نتایج تجربی، نمودارها و مقایسه با مرجع", "نمایش نمودار مقاطع زمانی شکل ۴-۳ و بازسازی دقیق شیب شوک، نمایش نقشه خطای شکل ۴-۴، گزارش خطای نسبی ۲.۱۵ درصد و مقایسه تطبیقی با مقاله مرجع رئیسی (۲۰۱۹)."],
        ["اسلاید ۱۴ و ۱۵\n(۲ دقیقه)", "نتیجه‌گیری و پیشنهادهای آینده", "جمع‌بندی دستاوردها در حل بدون شبکه معادلات غیرخطی؛ ارائه پیشنهادها برای کارهای آینده (توابع فعال‌ساز تطبیقی، روش‌های دامنه فرکانسی، توسعه به ابعاد بالاتر)."]
    ]
    
    doc.add_table(slide_data, [95, 150, 274], headers=["بخش و زمان", "موضوع اسلاید", "نکات کلیدی صحبت دانشجو در جلسه"], bg_header="#0F766E", col_aligns=['C', 'R', 'R'])
    
    doc.add_heading2("نکات کلیدی برای درخشش و تسلط در روز دفاع:")
    doc.add_bullet("آرامش در صدا و زبان بدن: شمرده صحبت کنید و بین جملات مکث‌های کوتاه داشته باشید.", "لحن صحبت:")
    doc.add_bullet("ارجاع به مفاهیم فیزیکی: هر جا سؤالی پرسیده شد، به قانون بقا و ارضای معادله دیفرانسیل اشاره کنید.", "کلیدواژه طلایی:")
    doc.add_bullet("صداقت علمی: اگر داوری نکته‌ای مطرح کرد، ابتدا تشکر کنید («نکته بسیار ارزشمندی است و در کارهای آینده مدنظر قرار خواهد گرفت»).", "پاسخ به انتقادات:")

    doc.add_callout(
        "«شبکه عصبی آگاه از فیزیک (PINN) یک حل‌گر عددی بدون شبکه محاسباتی است که با استفاده از مشتق‌گیری خودکار در کتابخانه جکس، قوانین بنیادین فیزیک را در کل دامنه فضا-زمان ارضا کرده و با کمترین داده‌های مرزی، رفتار پیچیده امواج شوک را با دقت بالا بازسازی می‌نماید.» — با آرزوی موفقیت، درخشش و نمره ۲۰ برای شما در جلسه دفاع!",
        title="جمله طلایی پایانی شما در جلسه دفاع",
        bg_color="#ECFDF5", border_color="#10B981", title_color="#065F46"
    )

    doc.save()

if __name__ == '__main__':
    generate()
