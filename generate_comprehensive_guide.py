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
        self.margin_x = 42
        self.margin_top = 40
        self.margin_bottom = 40
        self.content_width = self.width - 2 * self.margin_x
        self.y = self.height - self.margin_top
        self.page_num = 1

    def reshape_line(self, text):
        if not text:
            return ""
        reshaped = arabic_reshaper.reshape(str(text))
        return get_display(reshaped)

    def wrap_text(self, text, font_name, font_size, max_w):
        words = str(text).split()
        lines = []
        cur = []
        for w in words:
            test = " ".join(cur + [w])
            if pdfmetrics.stringWidth(test, font_name, font_size) <= max_w:
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
        self.c.setFillColor(colors.HexColor('#6B7280'))
        hdr = self.reshape_line("راهنمای جامع تسلط بر پایان‌نامه و آمادگی برای جلسه دفاع — دانشگاه بناب")
        self.c.drawRightString(self.width - self.margin_x, self.height - 25, hdr)
        self.c.setStrokeColor(colors.HexColor('#CBD5E1'))
        self.c.setLineWidth(0.6)
        self.c.line(self.margin_x, self.height - 29, self.width - self.margin_x, self.height - 29)
        self.c.restoreState()

    def draw_footer(self):
        self.c.saveState()
        self.c.setFont('Vazir', 8)
        self.c.setFillColor(colors.HexColor('#6B7280'))
        ftr = self.reshape_line(f"صفحه {self.page_num}")
        self.c.drawCentredString(self.width / 2.0, 22, ftr)
        name = self.reshape_line("محمد امیر بابازاد — راهنما: دکتر بابک آذرنوید")
        self.c.drawString(self.margin_x, 22, name)
        self.c.setStrokeColor(colors.HexColor('#CBD5E1'))
        self.c.setLineWidth(0.6)
        self.c.line(self.margin_x, 32, self.width - self.margin_x, 32)
        self.c.restoreState()

    def add_title(self, text, subtitle=None, meta=None):
        self.c.setFont('Vazir-Bold', 15)
        self.c.setFillColor(colors.HexColor('#003366'))
        shaped = self.reshape_line(text)
        self.c.drawCentredString(self.width / 2.0, self.y, shaped)
        self.y -= 20
        
        if subtitle:
            self.c.setFont('Vazir', 9.5)
            self.c.setFillColor(colors.HexColor('#4B5563'))
            shaped_sub = self.reshape_line(subtitle)
            self.c.drawCentredString(self.width / 2.0, self.y, shaped_sub)
            self.y -= 16

        if meta:
            self.c.setFont('Vazir', 8.5)
            self.c.setFillColor(colors.HexColor('#1E3A8A'))
            shaped_meta = self.reshape_line(meta)
            self.c.drawCentredString(self.width / 2.0, self.y, shaped_meta)
            self.y -= 14

        self.c.setStrokeColor(colors.HexColor('#003366'))
        self.c.setLineWidth(1.2)
        self.c.line(self.margin_x, self.y, self.width - self.margin_x, self.y)
        self.y -= 12

    def add_heading1(self, text):
        self.check_page_break(38)
        self.y -= 6
        self.c.setFont('Vazir-Bold', 11.5)
        self.c.setFillColor(colors.HexColor('#003366'))
        shaped = self.reshape_line(text)
        self.c.drawRightString(self.width - self.margin_x, self.y, shaped)
        self.y -= 5
        self.c.setStrokeColor(colors.HexColor('#003366'))
        self.c.setLineWidth(0.7)
        self.c.line(self.margin_x, self.y, self.width - self.margin_x, self.y)
        self.y -= 10

    def add_heading2(self, text):
        self.check_page_break(26)
        self.y -= 4
        self.c.setFont('Vazir-Bold', 10)
        self.c.setFillColor(colors.HexColor('#8B0000'))
        shaped = self.reshape_line(text)
        self.c.drawRightString(self.width - self.margin_x, self.y, shaped)
        self.y -= 12

    def add_heading3(self, text):
        self.check_page_break(20)
        self.y -= 2
        self.c.setFont('Vazir-Bold', 9)
        self.c.setFillColor(colors.HexColor('#1E3A8A'))
        shaped = self.reshape_line(text)
        self.c.drawRightString(self.width - self.margin_x, self.y, shaped)
        self.y -= 10

    def add_paragraph(self, text, font_size=8.8, leading=13.5, bold=False, color='#1F2937', indent=0):
        font_name = 'Vazir-Bold' if bold else 'Vazir'
        lines = self.wrap_text(text, font_name, font_size, self.content_width - indent)
        total_h = len(lines) * leading + 3
        self.check_page_break(total_h)
        
        self.c.setFont(font_name, font_size)
        self.c.setFillColor(colors.HexColor(color))
        
        for l in lines:
            shaped = self.reshape_line(l)
            self.c.drawRightString(self.width - self.margin_x - indent, self.y, shaped)
            self.y -= leading
        self.y -= 3

    def add_bullet(self, text, bold_prefix="", font_size=8.8, leading=13.5):
        full_text = f"• {bold_prefix} {text}" if bold_prefix else f"• {text}"
        self.add_paragraph(full_text, font_size=font_size, leading=leading, indent=8)

    def add_callout(self, text, title=None, bg_color='#F0F9FF', border_color='#0284C7', title_color='#0369A1'):
        font_size = 8.5
        leading = 13
        padding = 7
        inner_w = self.content_width - 2 * padding
        
        title_lines = self.wrap_text(title, 'Vazir-Bold', 9, inner_w) if title else []
        body_lines = self.wrap_text(text, 'Vazir', font_size, inner_w)
        
        h = len(title_lines) * 15 + len(body_lines) * leading + 2 * padding
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
                shaped = self.reshape_line(l)
                self.c.drawRightString(self.width - self.margin_x - padding, cur_y, shaped)
                cur_y -= 15
        
        self.c.setFont('Vazir', font_size)
        self.c.setFillColor(colors.HexColor('#1F2937'))
        for l in body_lines:
            shaped = self.reshape_line(l)
            self.c.drawRightString(self.width - self.margin_x - padding, cur_y, shaped)
            cur_y -= leading
            
        self.y = bot_y - 6

    def add_qa_box(self, question, answer):
        padding = 6
        q_lines = self.wrap_text(question, 'Vazir-Bold', 8.8, self.content_width - 2 * padding)
        a_lines = self.wrap_text(answer, 'Vazir', 8.5, self.content_width - 2 * padding)
        
        h = len(q_lines) * 14 + len(a_lines) * 13 + 2 * padding + 4
        self.check_page_break(h + 6)
        
        top_y = self.y
        bot_y = self.y - h
        
        self.c.saveState()
        self.c.setFillColor(colors.HexColor('#F8FAFC'))
        self.c.setStrokeColor(colors.HexColor('#CBD5E1'))
        self.c.setLineWidth(0.6)
        self.c.roundRect(self.margin_x, bot_y, self.content_width, h, 3, fill=1, stroke=1)
        
        # Header strip for question
        q_h = len(q_lines) * 14 + padding + 2
        self.c.setFillColor(colors.HexColor('#FEF2F2'))
        self.c.rect(self.margin_x, top_y - q_h, self.content_width, q_h, fill=1, stroke=0)
        self.c.setStrokeColor(colors.HexColor('#FECACA'))
        self.c.line(self.margin_x, top_y - q_h, self.width - self.margin_x, top_y - q_h)
        self.c.restoreState()
        
        cur_y = top_y - padding - 5
        self.c.setFont('Vazir-Bold', 8.8)
        self.c.setFillColor(colors.HexColor('#991B1B'))
        for l in q_lines:
            shaped = self.reshape_line(l)
            self.c.drawRightString(self.width - self.margin_x - padding, cur_y, shaped)
            cur_y -= 14
            
        cur_y -= 4
        self.c.setFont('Vazir', 8.5)
        self.c.setFillColor(colors.HexColor('#166534'))
        for l in a_lines:
            shaped = self.reshape_line(l)
            self.c.drawRightString(self.width - self.margin_x - padding, cur_y, shaped)
            cur_y -= 13
            
        self.y = bot_y - 6

    def add_table(self, data, col_widths, headers=None, bg_header='#003366', bg_row1='#FFFFFF', bg_row2='#F8FAFC'):
        padding = 4.5
        font_size = 8.2
        leading = 12.5
        
        all_rows = []
        if headers:
            all_rows.append((headers, True))
        for r in data:
            all_rows.append((r, False))
            
        row_heights = []
        row_wrapped_lines = []
        
        for r_idx, (row, is_hdr) in enumerate(all_rows):
            f_name = 'Vazir-Bold' if is_hdr else 'Vazir'
            max_lines = 1
            cols_lines = []
            for c_idx, cell_text in enumerate(row):
                w = col_widths[c_idx] - 2 * padding
                lines = self.wrap_text(cell_text, f_name, font_size, w)
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
            t_color = '#FFFFFF' if is_hdr else '#1F2937'
            self.c.setFont(f_name, font_size)
            self.c.setFillColor(colors.HexColor(t_color))
            
            cols_lines = row_wrapped_lines[r_idx]
            for c_idx, lines in enumerate(cols_lines):
                # RTL column layout: col 0 is rightmost
                col_left = start_x + sum(col_widths[c_idx+1:])
                col_right = col_left + col_widths[c_idx]
                
                text_y = top_y - padding - 6
                for l in lines:
                    shaped = self.reshape_line(l)
                    self.c.drawRightString(col_right - padding, text_y, shaped)
                    text_y -= leading
                    
            self.y = bot_y
        self.y -= 8

    def page_break(self):
        self.draw_footer()
        self.c.showPage()
        self.page_num += 1
        self.y = self.height - self.margin_top
        self.draw_header()

    def save(self):
        self.draw_footer()
        self.c.save()
        print(f"Generated comprehensive guide: {self.filename} ({self.page_num} pages)")

def generate():
    doc = PersianDocBuilder("MAB-THESIS/Defense_Guide.pdf")
    
    # ------------------ PAGE 1: TITLE & BIG PICTURE ------------------
    doc.add_title(
        "راهنمای جامع تسلط بر پایان‌نامه و آمادگی برای جلسه دفاع",
        "حل مسئله مستقیم معادله غیرخطی برگرز با استفاده از شبکه‌های عصبی آگاه از فیزیک (PINN)",
        "پژوهشگر: محمد امیر بابازاد  |  استاد راهنما: دکتر بابک آذرنوید  |  دانشگاه بناب — شهریور ۱۴۰۵"
    )
    
    doc.add_callout(
        "این جزوه خودآموز جامع برای این تدوین شده است تا شما بدون نیاز به داشتن دانش عمیق قبلی در ریاضیات پیشرفته یا یادگیری عمیق، به کل متن، مفاهیم، فرمول‌ها، روند الگوریتمی آموزش مدل با JAX، نتایج عددی و منطق علمی پایان‌نامه خود کاملاً مسلط شوید و بتوانید با آرامش و تسلط کامل در جلسه دفاع حاضر شده و نمره عالی کسب کنید.",
        title="پیام مهم به دانشجو (چگونه از این راهنما استفاده کنید؟)",
        bg_color="#EFF6FF", border_color="#3B82F6", title_color="#1D4ED8"
    )
    
    doc.add_heading1("۱. تصویر کلی و داستان پایان‌نامه به زبان بسیار ساده (The Big Picture)")
    
    doc.add_paragraph("هدف بنیادی این پایان‌نامه چیه؟", bold=True, color='#003366')
    doc.add_paragraph("هدف ما پیش‌بینی دقیق سرعت یک میدان پیوسته فیزیکی (مانند سرعت سیال هوا/آب در لوله یا سرعت خودروها در جریان ترافیک جاده‌ای) در طول زمان و مکان است. در فیزیک، پدیده حرکت این جریان‌ها با یک معادله دیفرانسیل جزئی غیرخطی بسیار معروف به نام «معادله برگرز» (Burgers Equation) مدل‌سازی می‌شود.")
    
    doc.add_paragraph("چرا روش‌های مهندسی سنتی (کلاسیک) در حل این مسئله مشکل دارند؟", bold=True, color='#003366')
    doc.add_paragraph("روش‌های قدیمی مثل تفاضل محدود (FDM) و اجزای محدود (FEM) مجبورند کل فضا و زمان را تکه‌تکه کنند و یک شبکه محاسباتی (Mesh) توری‌شکل بسازند و برای تک‌تک گره‌ها معادله جبری حل کنند. این کار سه عیب بزرگ دارد: ۱. در ابعاد بالا با پدیده «نفرین ابعاد» روبه‌رو شده و حجم محاسباتش سر به فلک می‌کشد. ۲. روی هندسه‌های نامنظم پیاده‌سازی بسیار سختی دارد. ۳. به خاطر تقریب تفاضلی مشتقات، خطای برش دارد.")
    
    doc.add_paragraph("چرا هوش مصنوعی معمولی (صرفاً داده‌محور) برای این کار مناسب نیست؟", bold=True, color='#003366')
    doc.add_paragraph("شبکه‌های عصبی معمولی مثل جعبه سیاه عمل می‌کنند؛ یعنی باید هزاران سنسور در نقاط مختلف نصب کنیم و داده‌های تجربی زیادی به شبکه بدهیم تا یاد بگیرد. اما در واقعیت (مثل داخل محفظه احتراق موشک، جریان خون در رگ‌ها یا مخازن عمیق زمین) نصب حسگرهای زیاد غیرممکن است. شبکه عصبی معمولی چون هیچ درکی از قوانین فیزیک ندارد، در جاهایی که حسگر نداشته باشیم (نواحی برون‌یابی) خطاهای وحشتناکی می‌دهد و حتی قوانین پایه‌ای مانند بقای جرم را نقض می‌کند.")
    
    doc.add_paragraph("شاهکار این پایان‌نامه (ایده PINN) چیست؟", bold=True, color='#003366')
    doc.add_paragraph("ما به جای اینکه به داده‌های انبوه وابسته باشیم، خودِ «فرمول فیزیک» (معادله دیفرانسیل برگرز) را وارد تابع هدف و مغز شبکه عصبی می‌کنیم! شبکه عصبی با استفاده از فناوری «مشتق‌گیری خودکار» در کتابخانه جکس (JAX) یاد می‌گیرد خروجی تولید کند که هم شرایط اولیه و مرزی محدود را برآورده کند و هم معادله دیفرانسیل فیزیک در سراسر فضا ارضا شود. به این چارچوب شبکه‌های عصبی آگاه از فیزیک (Physics-Informed Neural Networks یا PINN) می‌گویند.")

    doc.page_break()

    # ------------------ PAGE 2: CHAPTER-BY-CHAPTER SUMMARY (CH1 & CH2) ------------------
    doc.add_heading1("۲. خلاصه و تحلیل موشکافانه محتوای فصول پایان‌نامه (فصل به فصل)")
    
    doc.add_heading2("فصل اول: مقدمه و کلیات پژوهش (صفحات ۱۲ تا ۱۷)")
    doc.add_bullet("طرح موضوع و بیان مسئله: تبیین دلایل شکست مدل‌های داده‌محور خالص در مسائل کم‌داده فیزیکی و ضرورت تزریق قوانین فیزیکی به شبکه عصبی.", "بخش ۱-۱ و ۱-۲:")
    doc.add_bullet("تعریف مسئله مستقیم (Forward Problem): یعنی ضرایب فیزیکی (مانند ضریب لزجت) و معادله کاملاً معلوم است و می‌خواهیم میدان پیوسته پاسخ u(t,x) را بدون شبکه‌بندی بازسازی کنیم.", "مسئله مستقیم:")
    doc.add_bullet("معادله برگرز و چالش جبهه شوک: تشریح اینکه چرا معادله برگرز به خاطر تشکیل پدیده نوک‌تیز موج شوک (افت ناگهانی سرعت در فاصله کوتاه) یک مسئله معیار جهانی برای سنجش دقت الگوریتم‌هاست.", "چالش شوک:")
    doc.add_bullet("پیاده‌سازی مدل زمان‌پیوسته با جکس: تدوین چارچوب آموزش مبتنی بر تبدیل تابعی، کامپایل در زمان اجرا و بهینه‌سازی ترکیبی.", "پیاده‌سازی JAX:")
    
    doc.add_heading2("فصل دوم: مبانی نظری و پیشینه پژوهش (صفحات ۱۸ تا ۲۵)")
    doc.add_bullet("معادلات دیفرانسیل جزئی (بخش ۲-۱): معرفی معادله گرما (پخشی خالص)، معادله غیرخطی برگرز (رقابت همرفت u*u_x و لزجت nu*u_xx) و معادله غیرخطی شرودینگر.", "معادلات فیزیکی:")
    doc.add_bullet("روش‌های عددی کلاسیک (بخش ۲-۲): مقایسه ۳ روش اصلی (تفاضل محدود، اجزای محدود، روش‌های طیفی) در جدول ۲-۱ و تبیین محدودیت‌های آن‌ها در ابعاد بالا و هندسه‌های نامنظم.", "روش‌های کلاسیک:")
    doc.add_bullet("شبکه‌های عصبی مصنوعی (بخش ۲-۳): تشریح ساختار پرسپترون چندلایه (MLP)، روابط لایه‌ها، مقایسه توابع فعال‌ساز (جدول ۲-۲) و اثبات ریاضی قضیه تقریب عمومی سیبنکو (Cybenko).", "ساختار MLP:")
    doc.add_bullet("آموزش شبکه‌های عمیق (بخش ۲-۴): تشریح تابع خطای MSE، الگوریتم گرادیان کاهشی و پس‌انتشار خطا، معرفی بهینه‌ساز آدام (Adam) با روابط گشتاور اول و دوم، بهینه‌ساز شبه‌نیوتنی L-BFGS و مقداردهی گزاویه (Xavier).", "بهینه‌سازی:")
    doc.add_bullet("پیشینه پژوهش (بخش ۲-۵): مرور تاریخی یادگیری فیزیک‌پایه از ایده لاگاریس در ۱۹۹۸، مدل‌های فرآیند گاوسی (۲۰۱۷)، روش SINDy تا شاهکار مقاله رئیسی، پردیکاریس و کارنیاداکیس در سال ۲۰۱۹.", "سیر تحول تاریخی:")

    doc.add_heading2("فصل سوم: شبکه‌های عصبی آگاه از فیزیک (روش پژوهش - صفحات ۲۶ تا ۳۶)")
    doc.add_paragraph("این فصل مهم‌ترین بخش متدولوژی پایان‌نامه شماست و شامل محورهای زیر است:", bold=True, color='#003366')
    doc.add_bullet("صورت‌بندی کلی PINN (بخش ۳-۱): تعریف عملگر باقیمانده f = u_t + N[u] و تابع هزینه دوقلو، همراه با دیاگرام بلوکی شکل ۳-۱.", "ایده محوری:")
    doc.add_bullet("مبانی مشتق‌گیری خودکار (بخش ۳-۲): مقایسه مشتق‌گیری نمادین (تورم جبری عبارات)، مشتق‌گیری عددی (تعارض خطای برش و گردکردن ممیز شناور) و مشتق‌گیری خودکار. تشریح حساب اعداد دوگانه (Dual Numbers با خاصیت اپسیلون به توان دو مساوی صفر) و معرفی حالت مستقیم (JVP) و معکوس (VJP).", "مشتق‌گیری خودکار:")
    doc.add_bullet("به‌کارگیری اختصاصی AD در معادله برگرز (بخش ۳-۳): تشریح ۵ گام تفصیلی ریاضی و الگوریتمی از تعریف نگاشت سرعت، استخراج تحلیلی مشتقات جزئی زمانی و مکانی با قاعده زنجیره‌ای، تشکیل باقیمانده جبری، ساختار دو سطحی AD و پیاده‌سازی تابعی در کتابخانه JAX.", "حل برگرز با AD:")
    doc.add_bullet("مدل‌های زمان‌پیوسته و زمان‌گسسته (بخش ۳-۴ و ۳-۵): فرمول‌بندی ۲۰۰ نقطه مرزی و ۱۰۰۰۰ نقطه هم‌مکانی در مدل پیوسته و تبیین روش‌های رانگه-کوتا ضمنی (IRK) با جدول بوچر در مدل گسسته.", "مدل‌های زمانی:")
    doc.add_bullet("ملاحظات عملیاتی (بخش ۳-۶): توجیه انتخاب ۴ لایه پنهان، ۵۰ نورون، تابع فعال‌ساز Tanh، استراتژی بهینه‌سازی ترکیبی Adam+L-BFGS و نمونه‌برداری متمرکز در ناحیه شوک.", "تنظیمات آموزش:")

    doc.page_break()

    # ------------------ PAGE 3: CHAPTERS 4 & 5 + RESULTS TABLE ------------------
    doc.add_heading2("فصل چهارم: پیاده‌سازی و ارزیابی نتایج (صفحات ۳۷ تا ۴۳)")
    doc.add_bullet("بستر محاسباتی (بخش ۴-۱): استفاده از پایتون ۳ و کتابخانه JAX با دقت ممیز شناور ۶۴ بیتی (Float64) برای مهار خطاهای گردکردن.", "بستر نرم‌افزاری:")
    doc.add_bullet("ساختار الگوریتمی و روند آموزش با JAX (بخش ۴-۲): تشریح جامع خط لوله تبدیلات تابعی (grad، vmap، jit، value_and_grad)، مقداردهی گزاویه و استراتژی بهینه‌سازی دو مرحله‌ای.", "روند آموزش در JAX:")
    doc.add_bullet("نتایج حل مستقیم برگرز (بخش ۴-۳): اجرای آموزش ترکیبی شامل ۶۰۰۰ گام Adam و سپس L-BFGS، کاهش خطای هزینه از مرتبه منفی سه به منفی پنج.", "فرآیند آموزش:")
    doc.add_bullet("ارزیابی مقایسه‌ای با مقاله مرجع رئیسی ۲۰۱۹ (بخش ۴-۴): تحلیل جدول مقایسه تطبیقی (جدول ۴-۲) و نشان دادن بازتولید وفادارانه موقعیت و شیب تیز شوک.", "مقایسه با Raissi 2019:")

    doc.add_heading2("فصل پنجم: نتیجه‌گیری و پیشنهادها (صفحات ۴۴ تا ۴۶)")
    doc.add_bullet("یافته‌های کلیدی: اثبات توانمندی PINN در حل بدون شبکه معادلات غیرخطی و به دام انداختن امواج شوک تنها با ۲۰۰ نقطه مرزی و قید فیزیک.", "دستاوردهای اصلی:")
    doc.add_bullet("پیشنهادهای آتی: ۱. استفاده از توابع فعال‌ساز تطبیقی، ۲. به‌کارگیری شبکه‌های عصبی فوریه، ۳. وزن‌دهی پویا به بخش‌های تابع هزینه، ۴. توسعه به مدل‌های دوبعدی و سه‌بعدی ناویر-استوکس.", "کارهای آینده:")

    doc.add_heading1("۳. جدول جامع مشخصات، مقادیر عددی و نتایج تجربی پایان‌نامه")
    doc.add_paragraph("این جدول حاوی تمامی مقادیر عددی و پارامترهایی است که باید دقیقاً در ذهن داشته باشید:", bold=True, color='#003366')
    
    num_data = [
        ["معادله آزمون", "معادله غیرخطی برگرز با لزجت (1D Burgers PDE)", "u_t + u*u_x - nu*u_xx = 0"],
        ["ضریب لزجت (nu)", "nu = 0.01 / pi (حدود 0.003183)", "هر چه کوچکتر باشد شوک تیزتر و حل سخت‌تر است"],
        ["دامنه حل فضا-زمان", "مکان: [-1, 1]  |  زمان: [0, 1]", "دامنه پیوسته دو بعدی بدون شبکه‌بندی گسسته"],
        ["شرط اولیه و مرزی", "u(0, x) = -sin(pi*x)  |  u(t, -1) = u(t, 1) = 0", "شرایط اولیه سینوسی و مرزهای همگن دیریکله"],
        ["داده‌های مرزی (N_u)", "۲۰۰ نقطه (۱۰۰ نقطه مرزی + ۱۰۰ نقطه اولیه)", "تنها داده‌های برچسب‌دار معلوم در مسئله"],
        ["نقاط هم‌مکانی (N_f)", "۱۰۰۰۰ نقطه درون دامنه فضا-زمان", "نمونه‌برداری متمرکز در حوالی خط شوک x=0"],
        ["معماری شبکه عصبی", "۴ لایه پنهان، ۵۰ نورون در هر لایه", "تابع فعال‌ساز تانژانت هیپربولیک (Tanh)"],
        ["استراتژی آموزش", "ترکیبی دو مرحله‌ای: Adam + L-BFGS", "۶۰۰۰ گام آدام (نرخ 0.001) سپس همگرایی L-BFGS"],
        ["خطای نسبی L2 نهایی", "2.15 * 10^-2  (معادل ۲.۱۵ درصد)", "میزان انحراف شبکه از میدان پاسخ معیار"],
        ["خطای باقیمانده فیزیک", "MSE_f = 6.36 * 10^-5", "نشان‌دهنده ارضای فوق‌العاده قوی قانون فیزیک"],
        ["خطای داده مرزی", "MSE_u = 2.35 * 10^-5", "انطباق عالی خروجی شبکه با شرایط مرزی و اولیه"],
        ["مقایسه با Raissi 2019", "هم‌خوانی کیفی عالی در بازتولید گرادیان تند", "بازتولید موفقیت‌آمیز جبهه شوک مقاله مرجع"]
    ]
    
    doc.add_table(
        num_data,
        [125, 185, 200],
        headers=["شاخص و پارامتر", "مقدار در این پژوهش", "توضیح مفهومی"],
        bg_header="#003366"
    )

    doc.page_break()

    # ------------------ PAGE 4: DETAILED EXPLANATION OF FIGURES & AD MECHANISM ------------------
    doc.add_heading1("۴. تشریح دقیق نمودارهای فصل ۴ و مکانیزم ۵ مرحله‌ای آموزش با JAX")
    
    doc.add_heading2("تحلیل مفهومی شکل‌ها و نمودارهای فصل ۴:")
    doc.add_bullet("شکل ۴-۱ (توزیع نقاط آموزش): این شکل نشان می‌دهد که چگونه ۲۰۰ نقطه با رنگ قرمز روی مرزهای مکانی و لحظه آغازین قرار گرفته‌اند و ۱۰۰۰۰ نقطه خاکستری در سراسر صفحه فضا-زمان پخش شده‌اند. تراکم بالاتر نقاط در خط مرکزی x=0 نشان‌دهنده راهبرد نمونه‌برداری متمرکز در ناحیه تشکیل شوک است.", "شکل ۴-۱:")
    doc.add_bullet("شکل ۴-۲ (تاریخچه همگرایی توابع هزینه): این نمودار لگاریتمی نشان می‌دهد که در فاز اول (بهینه‌ساز Adam)، خطای کل با شیب مناسب افت می‌کند و پس از گام ۶۰۰۰ با ورود بهینه‌ساز شبه‌نیوتنی L-BFGS، خطا دچار یک ریزش شارپ شده و به دقت ۱۰ به توان منفی ۵ می‌رسد.", "شکل ۴-۲:")
    doc.add_bullet("شکل ۴-۳ (مقاطع زمانی پاسخ در زمان‌های t=0.25, 0.50, 0.75): این نمودار قلب نتایج شماست! خطوط ممتد مشکی جواب معیار و خطوط خط‌چین قرمز پیش‌بینی PINN هستند. مشاهده می‌کنید که موج سینوسی هموار اولیه با گذر زمان به سمت مرکز متمایل شده و در حوالی x=0 یک افت عمودی و دیوارمانند (جبهه شوک) ایجاد می‌کند و مدل با دقت عالی آن را بازسازی کرده است.", "شکل ۴-۳:")
    doc.add_bullet("شکل ۴-۴ (نقشه خطای دوبعدی): نمودار کانتور رنگی نشان می‌دهد که در بیش از ۹۵ درصد مساحت دامنه فضا-زمان، خطا به رنگ تیره (نزدیک به صفر) است و بیشینه خطای اندک مدل فقط در امتداد نوار بسیار باریک خط شوک (x=0 برای زمان‌های بعد از 0.3) تمرکز دارد.", "شکل ۴-۴:")

    doc.add_heading2("روند الگوریتمی ۵ مرحله‌ای اجرای مدل در کتابخانه جکس (JAX):")
    
    ad_steps = [
        ("گام اول (مقداردهی اولیه پارامترها):", "وزن‌های شبکه با توزیع یکنواخت گزاویه (گلوروت) بر اساس تعداد نورون‌های ورودی و خروجی مقداردهی شده و بایاس‌ها با صفر آغاز می‌شوند تا پایداری گرادیان‌ها حفظ شود."),
        ("گام دوم (تبدیلات تابعی و مشتق‌گیری):", "تابع پیش‌بینی u_net تعریف شده و مشتقات زمانی و مکانی u_t، u_x و u_xx با استفاده از تبدیل تابعی jax.grad به‌صورت تحلیلی و تودرتو استخراج می‌گردند."),
        ("گام سوم (بردارسازی و کامپایل JIT):", "با استفاده از jax.vmap ارزیابی نقاط به صورت دسته‌ای و برداری درمی‌آید و با jax.jit کل گراف محاسباتی با کامپایلر XLA به کد ماشین بهینه تبدیل می‌شود."),
        ("گام چهارم (محاسبه هم‌زمان تابع هزینه و گرادیان):", "با استفاده از jax.value_and_grad، مقدار تابع هزینه ترکیبی (MSE_u + MSE_f) و بردار گرادیان آن نسبت به پارامترهای شبکه در یک گذر مشترک و سریع به دست می‌آید."),
        ("گام پنجم (استراتژی بهینه‌سازی دو مرحله‌ای):", "ابتدا ۶۰۰۰ تکرار با بهینه‌ساز Adam برای فرار از کمینه‌های محلی اجرا شده و سپس آموزش با روش شبه‌نیوتنی L-BFGS-B تا رسیدن به همگرایی عمیق ادامه می‌یابد.")
    ]
    for s_title, s_desc in ad_steps:
        doc.add_bullet(s_desc, s_title)

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
    doc.add_table(terms_data, [160, 350], headers=["اصطلاح تخصصی", "تعریف و کاربرد در پایان‌نامه"], bg_header="#1E3A8A")

    doc.page_break()

    # ------------------ PAGE 5: GOLD DEFENSE Q&A (QUESTIONS 1 TO 5) ------------------
    doc.add_heading1("۶. بانک سؤالات طلایی داوران و پاسخ‌های مسلط دانشجو (بخش اول)")
    doc.add_paragraph("این سؤالات رایج‌ترین پرسش‌های هیئت داوران در جلسات دفاع یادگیری عمیق و PINN هستند. پاسخ‌های زیر را به دقت مطالعه کنید:", bold=True, color='#003366')
    
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

    doc.page_break()

    # ------------------ PAGE 6: GOLD DEFENSE Q&A (QUESTIONS 6 TO 10) ------------------
    doc.add_heading1("۷. بانک سؤالات طلایی داوران و پاسخ‌های مسلط دانشجو (بخش دوم)")
    
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
        "پاسخ شما: در مقاله بنیادین رئیسی و همکاران (۲۰۱۹) خطای نسبی L2 در حدود ۶.۷ در ۱۰ به توان منفی ۴ گزارش شده است که حاصل بهینه‌سازی بسیار طولانی تا ده‌ها هزار تکرار L-BFGS و ۵۰ هزار نقطه هم‌مکانی بوده است. در پژوهش حاضر با ۶۰۰۰ گام Adam و بهینه‌سازی متعادل L-BFGS با ۱۰۰۰۰ نقطه، به خطای ۲.۱۵ درصدی رسیدیم که از نظر کیفی موقعیت و شیب تیز شوک را در تمام مقاطع زمانی با وفاداری بسیار بالا و بدون هیچ نوسان مصنوعی بازتولید کرده است."
    )

    doc.page_break()

    # ------------------ PAGE 7: DEFENSE PRESENTATION SCRIPT & SLIDES ------------------
    doc.add_heading1("۸. سناریوی گام‌به‌گام و زمان‌بندی ارائه دفاعیه (۲۰ دقیقه سخنرانی بی‌نقص)")
    doc.add_paragraph("اگر می‌خواهید یک ارائه روان، مسلط و بدون استرس داشته باشید، اسلایدهای خود را طبق زمان‌بندی استاندارد زیر تقسیم‌بندی کنید:", bold=True, color='#003366')
    
    slide_data = [
        ["اسلاید ۱ و ۲\n(زمان: ۲ دقیقه)", "عنوان، خوش‌آمدگویی و بیان مسئله", "معرفی خود و استاد راهنما؛ توضیح اینکه روش‌های سنتی وابسته به مش‌بندی هستند و هوش مصنوعی معمولی نیازمند داده بسیار زیاد است و در غیاب داده قوانین فیزیک را نقض می‌کند."],
        ["اسلاید ۳ و ۴\n(زمان: ۳ دقیقه)", "معادله برگرز و چالش شوک", "معرفی فرمول برگرز و توضیح رقابت همرفت و پخش؛ توضیح اینکه تشکیل جبهه تیز شوک به عنوان یک مسئله معیار در مکانیک سیالات و ترافیک مطرح است."],
        ["اسلاید ۵ و ۶\n(زمان: ۳ دقیقه)", "ایده محوری PINN و مشتق‌گیری خودکار", "نمایش دیاگرام بلوکی فصل ۳؛ توضیح اینکه مشتق‌گیری خودکار با قاعده زنجیره‌ای در JAX مشتقات فیزیکی u_t, u_x, u_xx را بدون نیاز به شبکه محاسباتی حساب می‌کند."],
        ["اسلاید ۷ و ۸\n(زمان: ۳ دقیقه)", "تابع هزینه دوقلو و ساختار الگوریتمی JAX", "تشریح تابع خطای Loss = MSE_u + MSE_f با ۲۰۰ نقطه مرزی و ۱۰۰۰۰ نقطه هم‌مکانی؛ توضیح خط لوله کامپایل JIT و بردارسازی VMAP در جکس."],
        ["اسلاید ۹ و ۱۰\n(زمان: ۲ دقیقه)", "استراتژی آموزش ترکیبی Adam و L-BFGS", "توضیح روند دو مرحله‌ای: ۶۰۰۰ گام Adam برای فرار از کمینه‌های محلی و سپس ادامه با L-BFGS برای همگرایی سریع به دقت ۱۰ به توان منفی پنج."],
        ["اسلاید ۱۱ تا ۱۳\n(زمان: ۵ دقیقه)", "نتایج تجربی، نمودارها و مقایسه با مرجع", "نمایش نمودار مقاطع زمانی شکل ۴-۳ و بازسازی دقیق شیب شوک؛ نمایش نقشه خطای شکل ۴-۴؛ گزارش خطای نسبی ۲.۱۵ درصد و مقایسه تطبیقی با مقاله رئیسی ۲۰۱۹."],
        ["اسلاید ۱۴ و ۱۵\n(زمان: ۲ دقیقه)", "نتیجه‌گیری و پیشنهادهای آینده", "جمع‌بندی دستاوردها در حل بدون شبکه معادلات غیرخطی؛ ارائه پیشنهادها برای کارهای آینده (توابع فعال‌ساز تطبیقی، روش‌های دامنه فرکانسی، توسعه به ابعاد بالاتر)."]
    ]
    
    doc.add_table(slide_data, [105, 150, 255], headers=["بخش و زمان", "موضوع اسلاید", "نکات کلیدی صحبت دانشجو در جلسه"], bg_header="#0F766E")
    
    doc.add_heading2("نکات کلیدی برای موفقیت در روز دفاع:")
    doc.add_bullet("آرامش در صدا و زبان بدن: شمرده صحبت کنید و بین جملات مکث‌های کوتاه داشته باشید.", "لحن صحبت:")
    doc.add_bullet("ارجاع به مفاهیم فیزیکی: هر جا سؤالی پرسیده شد، به قانون بقا و ارضای معادله دیفرانسیل اشاره کنید.", "کلیدواژه طلایی:")
    doc.add_bullet("صداقت علمی: اگر داوری نکته‌ای مطرح کرد، ابتدا تشکر کنید («نکته بسیار ارزشمندی است و در کارهای آینده مدنظر قرار خواهد گرفت»).", "پاسخ به انتقادات:")

    doc.add_callout(
        "«شبکه عصبی آگاه از فیزیک (PINN) یک حل‌گر عددی بدون شبکه محاسباتی است که با استفاده از مشتق‌گیری خودکار در کتابخانه جکس، قوانین بنیادین فیزیک را در کل دامنه فضا-زمان ارضا کرده و با کمترین داده‌های مرزی، رفتار پیچیده امواج شوک را با دقت بالا بازسازی می‌نماید.» — با آرزوی موفقیت، درخشش و نمره ۲۰ برای شما!",
        title="جمله طلایی پایانی شما در جلسه دفاع",
        bg_color="#ECFDF5", border_color="#10B981", title_color="#065F46"
    )

    doc.save()

if __name__ == '__main__':
    generate()
