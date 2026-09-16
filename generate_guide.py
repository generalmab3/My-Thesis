import sys, os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
import arabic_reshaper
from bidi.algorithm import get_display

# Register Persian Fonts
pdfmetrics.registerFont(TTFont('Vazir', 'MAB-THESIS/fonts/Vazirmatn-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Vazir-Bold', 'MAB-THESIS/fonts/Vazirmatn-Bold.ttf'))

def fa(text):
    if not text:
        return ""
    reshaped = arabic_reshaper.reshape(str(text))
    return get_display(reshaped)

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
        self.setFont('Vazir', 8)
        self.setFillColor(colors.HexColor('#666666'))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            header_text = fa("راهنمای تسلط و دفاع پایان‌نامه — حل معادله برگرز با PINN")
            self.drawRightString(A4[0] - 40, A4[1] - 28, header_text)
            self.setStrokeColor(colors.HexColor('#D0D7DE'))
            self.setLineWidth(0.5)
            self.line(40, A4[1] - 32, A4[0] - 40, A4[1] - 32)
        
        # Footer (all pages)
        footer_text = fa(f"صفحه {self._pageNumber} از {page_count}")
        self.drawCentredString(A4[0] / 2.0, 25, footer_text)
        self.drawString(40, 25, fa("محمد امیر بابازاد — دانشگاه بناب"))
        self.setStrokeColor(colors.HexColor('#D0D7DE'))
        self.setLineWidth(0.5)
        self.line(40, 36, A4[0] - 40, 36)
        
        self.restoreState()

def create_guide_pdf(filename="MAB-THESIS/Defense_Guide.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=45,
        bottomMargin=45
    )
    
    base_style = ParagraphStyle(
        'BaseFa',
        fontName='Vazir',
        fontSize=9.5,
        leading=15,
        alignment=2, # Right
        textColor=colors.HexColor('#24292F')
    )
    
    body_style = ParagraphStyle(
        'BodyFa',
        parent=base_style,
        fontSize=9,
        leading=14.5,
        spaceAfter=4
    )
    
    title_style = ParagraphStyle(
        'TitleFa',
        fontName='Vazir-Bold',
        fontSize=17,
        leading=24,
        alignment=1, # Center
        textColor=colors.HexColor('#003366'),
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'SubTitleFa',
        fontName='Vazir',
        fontSize=10.5,
        leading=16,
        alignment=1, # Center
        textColor=colors.HexColor('#4B5563'),
        spaceAfter=10
    )
    
    h1_style = ParagraphStyle(
        'H1Fa',
        fontName='Vazir-Bold',
        fontSize=11.5,
        leading=17,
        alignment=2,
        textColor=colors.HexColor('#003366'),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )
    
    q_style = ParagraphStyle(
        'QFa',
        fontName='Vazir-Bold',
        fontSize=9.5,
        leading=15,
        alignment=2,
        textColor=colors.HexColor('#9C0006'),
        spaceBefore=3,
        spaceAfter=2,
        keepWithNext=True
    )
    
    ans_style = ParagraphStyle(
        'AnsFa',
        parent=body_style,
        fontSize=9,
        leading=14,
        textColor=colors.HexColor('#1E4620'),
        spaceAfter=4
    )

    story = []
    
    # ================== PAGE 1 ==================
    story.append(Paragraph(fa("راهنمای جامع تسلط و آمادگی برای جلسه دفاع پایان‌نامه"), title_style))
    story.append(Paragraph(fa("حل مسئله مستقیم معادله غیرخطی برگرز با استفاده از شبکه‌های عصبی آگاه از فیزیک (PINN)"), subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#003366'), spaceAfter=8))
    
    meta_text = "<b>پژوهشگر:</b> محمد امیر بابازاد &nbsp;|&nbsp; <b>استاد راهنما:</b> دکتر بابک آذرنوید &nbsp;|&nbsp; <b>دانشگاه بناب — سال تحصیلی ۱۴۰۴-۱۴۰۵</b>"
    story.append(Paragraph(fa(meta_text), ParagraphStyle('Meta', fontName='Vazir', fontSize=8.5, alignment=1, textColor=colors.HexColor('#4B5563'))))
    story.append(Spacer(1, 8))
    
    intro_box_data = [[
        Paragraph(fa(
            "<b>پیام راهنما برای دانشجو:</b> این جزوه اختصاصی به‌گونه‌ای نگارش یافته است که شما بدون نیاز به داشتن پیش‌زمینه عمیق ریاضی یا برنامه‌نویسی، بتوانید در کوتاه‌ترین زمان به کل منطق، مفاهیم، معادلات و نتایج پایان‌نامه مسلط شده و با اعتمادبه‌نفس کامل در جلسه دفاع از پژوهش خود دفاع نمایید."
        ), body_style)
    ]]
    intro_table = Table(intro_box_data, colWidths=[A4[0]-80])
    intro_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EBF3FB')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#8AB4F8')),
        ('PADDING', (0,0), (-1,-1), 7),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(intro_table)
    story.append(Spacer(1, 8))
    
    story.append(Paragraph(fa("۱. داستان کلیدی پایان‌نامه به زبان بسیار ساده و روان (The Big Picture)"), h1_style))
    story.append(Paragraph(fa(
        "<b>هدف کلی پایان‌نامه چیه؟</b> هدف ما محاسبه و پیش‌بینی سرعت یک سیال یا جریان ترافیک در طول زمان و مکان است. فیزیک حاکم بر این پدیده با فرمول معروفی به نام «معادله غیرخطی برگرز» توصیف می‌شود."
    ), body_style))
    
    story.append(Paragraph(fa(
        "<b>مشکل روش‌های مهندسی سنتی چی بود؟</b> روش‌های کلاسیک (مثل تفاضل محدود یا اجزای محدود) کل فضا را مثل یک توری (شبکه) مش‌بندی می‌کنند و برای تک‌تک گره‌ها معادله می‌نویسند. این کار در ابعاد بالا وحشتناک سنگین، کند و مستعد خطای گسسته‌سازی است و اگر شکل دامنه پیچیده باشد به بن‌بست می‌خورد."
    ), body_style))
    
    story.append(Paragraph(fa(
        "<b>چرا هوش مصنوعی معمولی (صرفاً داده‌محور) به درد نمی‌خورد؟</b> شبکه‌های عصبی معمولی جعبه سیاه هستند و برای یادگیری به هزاران داده حسگر نیاز دارند. در مسائل واقعی (مثل موتور موشک یا رگ‌های خون) حسگرهای کمی داریم. شبکه معمولی بدون درک قوانین فیزیک، در مناطقی که داده ندارد خطاهای بزرگی تولید کرده و قوانین بدیهی فیزیک را نقض می‌کند."
    ), body_style))

    story.append(Paragraph(fa(
        "<b>شاهکار پایان‌نامه (ایده PINN) چیه؟</b> ما به جای دادن داده‌های زیاد، خودِ «قانون فیزیک» (معادله دیفرانسیل برگرز) را وارد تابع خطای شبکه عصبی می‌کنیم! شبکه یاد می‌گیرد طوری خروجی دهد که هم با داده‌های مرزی اندک هم‌خوان باشد و هم فرمول فیزیک را در کل فضا ارضا کند. به این مدل <b>Physics-Informed Neural Network (PINN)</b> می‌گویند."
    ), body_style))
    
    story.append(PageBreak())

    # ================== PAGE 2 ==================
    story.append(Paragraph(fa("۲. واژه‌نامه اصطلاحات کلیدی (فرهنگ لغت طلایی برای جلسه دفاع)"), h1_style))
    
    terms = [
        ("معادله برگرز (Burgers Eq)", "معادله دیفرانسیل غیرخطی که رقابت پدیده همرفت (تیز کردن موج) و لزجت (هموار کردن موج) را مدل می‌کند."),
        ("موج شوک (Shock Wave)", "ناحیه باریکی که در آن سرعت در فاصله مکانی کوتاهی ناگهان افت شدید می‌کند (مثل ترافیک سنگین ناگهانی)."),
        ("مسئله مستقیم (Forward)", "مسئله‌ای که فرمول فیزیک و شرایط مرزی معلوم است و هدف یافتن میدان پاسخ u(t,x) در سراسر دامنه است."),
        ("مشتق‌گیری خودکار (AD)", "فناوری دقیق محاسبه مشتق با قاعده زنجیره‌ای روی گراف کدها بدون خطای برش تفاضل محدود."),
        ("نقاط هم‌مکانی (Collocation)", "نقاطی در داخل دامنه که داده تجربی نداریم، ولی باقیمانده فیزیک (f) را در آن‌ها صفر می‌کنیم (۱۰۰۰۰ نقطه)."),
        ("تابع فعال‌ساز Tanh", "تابع غیرخطی نورون‌ها که بی‌نهایت‌بار مشتق‌پذیر و نرم است و اجازه می‌دهد مشتق دوم بدون صفر شدن حساب شود."),
        ("بهینه‌ساز Adam", "الگوریتم گرادیان تصادفی تطبیقی که در فاز اول برای فرار از کمینه‌های محلی استفاده می‌شود (۶۰۰۰ گام)."),
        ("بهینه‌ساز L-BFGS", "الگوریتم شبه‌نیوتنی مرتبه دو که با تقریب ماتریس هشین، در فاز دوم برای همگرایی با دقت بسیار بالا استفاده می‌شود."),
        ("حل‌گر مرجع طیفی (Spectral)", "یک حل‌گر عددی فوق‌العاده دقیق بر پایه تبدیل فوریه که برای ایجاد «پاسخ واقعی و خط‌کش آزمون» ساخته شده است.")
    ]
    
    term_table_data = [[
        Paragraph(fa("<b>تعریف و کاربرد در پایان‌نامه</b>"), ParagraphStyle('TH', fontName='Vazir-Bold', fontSize=8.5, alignment=1, textColor=colors.white)),
        Paragraph(fa("<b>اصطلاح تخصصی</b>"), ParagraphStyle('TH', fontName='Vazir-Bold', fontSize=8.5, alignment=1, textColor=colors.white))
    ]]
    for t_name, t_desc in terms:
        term_table_data.append([
            Paragraph(fa(t_desc), body_style),
            Paragraph(fa(f"<b>{t_name}</b>"), ParagraphStyle('Term', fontName='Vazir-Bold', fontSize=8.5, alignment=2, textColor=colors.HexColor('#003366')))
        ])
    
    term_table = Table(term_table_data, colWidths=[340, 175])
    term_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#003366')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E1E4E8')),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')])
    ]))
    story.append(term_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph(fa("۳. سازوکار ریاضی و الگوریتمی PINN در ۵ گام طلایی"), h1_style))
    story.append(Paragraph(fa(
        "اگر داور پرسید <b>«PINN چطور کار می‌کند و معادله برگرز را چطور حل می‌کند؟»</b>، این ۵ مرحله را بیان کنید:"
    ), body_style))
    
    steps = [
        ("۱. معماری شبکه", "یک MLP با ۴ لایه پنهان، ۵۰ نورون در هر لایه و فعال‌ساز Tanh ورودی (t,x) را می‌گیرد و سرعت u(t,x) را خروجی می‌دهد."),
        ("۲. مشتق‌گیری خودکار (AD)", "مشتقات زمانی و مکانی u_t، u_x و u_xx با قاعده زنجیره‌ای روی گراف محاسباتی JAX با دقت ممیز شناور ماشین حساب می‌شوند."),
        ("۳. تشکیل باقیمانده فیزیک", "باقیمانده f = u_t + u*u_x - nu*u_xx بدون پارامتر جدید تشکیل می‌شود و با جواب دقیق باید صفر شود."),
        ("۴. تابع هزینه دوقلو", "تابع هدف شامل خطای داده روی ۲۰۰ نقطه مرزی-اولیه (MSE_u) و خطای فیزیک روی ۱۰۰۰۰ نقطه هم‌مکانی (MSE_f) است."),
        ("۵. بهینه‌سازی ترکیبی", "ابتدا ۶۰۰۰ گام با Adam برای فرار از کمینه‌های محلی اجرا شده و سپس با L-BFGS به همگرایی با دقت بالا می‌رسیم.")
    ]
    
    for s_title, s_desc in steps:
        box_data = [[Paragraph(fa(f"<b>{s_title}:</b> {s_desc}"), body_style)]]
        box_table = Table(box_data, colWidths=[A4[0]-80])
        box_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
            ('PADDING', (0,0), (-1,-1), 4),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(box_table)
        story.append(Spacer(1, 3))
    
    story.append(PageBreak())

    # ================== PAGE 3 ==================
    story.append(Paragraph(fa("۴. جدول جامع مقادیر عددی، پارامترها و نتایج تجربی"), h1_style))
    story.append(Paragraph(fa(
        "تمامی اعداد و پارامترهای کلیدی پایان‌نامه که برای ارائه و پاسخ به سؤالات لازم دارید:"
    ), body_style))
    
    results_data = [
        [Paragraph(fa("<b>مقدار در این پایان‌نامه</b>"), ParagraphStyle('RH', fontName='Vazir-Bold', fontSize=8.5, alignment=1, textColor=colors.white)),
         Paragraph(fa("<b>شاخص و پارامتر</b>"), ParagraphStyle('RH', fontName='Vazir-Bold', fontSize=8.5, alignment=1, textColor=colors.white))],
        
        [Paragraph(fa("معادله غیرخطی برگرز با لزجت (1D Burgers)"), body_style), Paragraph(fa("معادله آزمون"), body_style)],
        [Paragraph(fa("nu = 0.01 / pi  (حدود 0.003183)"), body_style), Paragraph(fa("ضریب لزجت سینماتیکی"), body_style)],
        [Paragraph(fa("x in [-1, 1]  و  t in [0, 1]"), body_style), Paragraph(fa("دامنه حل فضا-زمان"), body_style)],
        [Paragraph(fa("u(0, x) = -sin(pi * x)"), body_style), Paragraph(fa("شرط اولیه"), body_style)],
        [Paragraph(fa("u(t, -1) = u(t, 1) = 0"), body_style), Paragraph(fa("شرایط مرزی دیریکله"), body_style)],
        [Paragraph(fa("200 نقطه (100 نقطه شرط اولیه + 100 نقطه مرزی)"), body_style), Paragraph(fa("تعداد داده مرزی (N_u)"), body_style)],
        [Paragraph(fa("10000 نقطه با نمونه‌برداری متمرکز در جبهه شوک"), body_style), Paragraph(fa("نقاط هم‌مکانی (N_f)"), body_style)],
        [Paragraph(fa("4 لایه پنهان، 50 نورون در هر لایه، فعال‌ساز Tanh"), body_style), Paragraph(fa("معماری شبکه"), body_style)],
        [Paragraph(fa("ترکیبی: 6000 گام Adam + بهینه‌سازی L-BFGS"), body_style), Paragraph(fa("استراتژی بهینه‌سازی"), body_style)],
        [Paragraph(fa("<b>2.15 * 10^-2  (حدود 2.15 درصد)</b>"), ParagraphStyle('Res', fontName='Vazir-Bold', fontSize=8.5, textColor=colors.HexColor('#003366'), alignment=2)), Paragraph(fa("<b>خطای نسبی L2 با مرجع</b>"), body_style)],
        [Paragraph(fa("6.36 * 10^-5"), body_style), Paragraph(fa("خطای فیزیک (MSE_f)"), body_style)],
        [Paragraph(fa("2.35 * 10^-5"), body_style), Paragraph(fa("خطای مرزی (MSE_u)"), body_style)],
        [Paragraph(fa("پایتون 3 + کتابخانه JAX (کامپایل JIT و VMAP)"), body_style), Paragraph(fa("بستر محاسباتی"), body_style)],
        [Paragraph(fa("هم‌خوانی کیفی عالی در بازتولید گرادیان تند شوک در مقاطع مختلف"), body_style), Paragraph(fa("مقایسه با Raissi 2019"), body_style)]
    ]
    
    res_table = Table(results_data, colWidths=[260, 255])
    res_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')])
    ]))
    story.append(res_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph(fa("تحلیل نمودارهای فصل ۴ پایان‌نامه:"), h1_style))
    analysis_points = [
        "<b>شکل ۴-۱ (نقاط آموزشی):</b> ۲۰۰ نقطه مرزی-اولیه و ۱۰۰۰۰ نقطه هم‌مکانی با تراکم بالاتر در خط x=0 را نشان می‌دهد.",
        "<b>شکل ۴-۲ (تاریخچه همگرایی):</b> افت سریع خطا با Adam و سپس ریزش شارپ آن تا دقت مرتبه منفی پنج با L-BFGS را نمایش می‌دهد.",
        "<b>شکل ۴-۳ (مقاطع زمانی پاسخ):</b> تطابق فوق‌العاده منحنی شبکه با حل مرجع در زمان‌های t=0.25, 0.50, 0.75 را به تصویر کشیده است.",
        "<b>شکل ۴-۴ (نقشه خطای دوبعدی):</b> نشان می‌دهد خطای مدل در اکثر دامنه نزدیک صفر است و بیشینه خطای اندک در لایه شوک متمرکز شده است."
    ]
    for ap in analysis_points:
        story.append(Paragraph(fa(f"• {ap}"), body_style))
    
    story.append(PageBreak())

    # ================== PAGE 4 ==================
    story.append(Paragraph(fa("۵. بانک سؤالات احتمالی داوران و پاسخ‌های طلایی (Q&A Cheat Sheet)"), h1_style))
    story.append(Paragraph(fa(
        "داوران جلسه دفاع معمولاً این سؤالات را مطرح می‌کنند؛ پاسخ‌های آماده و علمی زیر را به خاطر بسپارید:"
    ), body_style))
    
    qa_list = [
        ("سؤال ۱: تفاوت مشتق‌گیری خودکار (AD) با تفاضل محدود چیه؟",
         "تفاضل محدود مشتق را با بسط تیلور و طول گام h تقریب می‌زند که دو خطای متضاد دارد: اگر h بزرگ باشد خطای برش داریم و اگر h کوچک باشد خطای گردکردن ممیز شناور ماشین پیش می‌آید. اما مشتق‌گیری خودکار با قاعده زنجیره‌ای روی گراف محاسباتی کدها، مشتق دقیق را تا حد دقت ماشین و بدون هیچ خطای برشی حساب می‌کند."),
        
        ("سؤال ۲: چرا از تابع فعال‌ساز Tanh استفاده کردی و چرا ReLU نگذاشتی؟",
         "چون در معادله برگرز به مشتق دوم مکانی (u_xx) نیاز داریم. تابع ReLU تکه‌ای خطی است و مشتق دوم آن همه‌جا صفر می‌شود و نمی‌تواند لزجت را مدل کند. در مقابل، Tanh تابعی هموار و بی‌نهایت‌بار مشتق‌پذیر (C-infinity) با مشتقات غیرصفر است."),
        
        ("سؤال ۳: چرا بهینه‌سازی را دو مرحله‌ای (Adam + L-BFGS) انجام دادی؟",
         "سطح خطای توابع فیزیک‌پایه دارای کمینه‌های محلی متعددی است. بهینه‌ساز آدام با گشتاور تصادفی در فرار از کمینه‌های محلی عالی عمل می‌کند اما در همگرایی دقیق کند است. بنابراین ابتدا با آدام به نزدیکی کمینه می‌رسیم و سپس با L-BFGS که روش شبه‌نیوتنی مرتبه دو است، با سرعت فوق‌خطی به دقت نهایی می‌رسیم."),
        
        ("سؤال ۴: نقاط هم‌مکانی (Collocation) چه نقشی دارند و چرا در حوالی x=0 بیشتر بودند؟",
         "نقاط هم‌مکانی نقاطی داخل دامنه هستند که داده تجربی نداریم ولی قید معادله فیزیک در آن‌ها صفر می‌شود. چون در معادله برگرز پدیده موج شوک و گرادیان‌های بسیار تند در خط x=0 (برای زمان‌های t>0.3) رخ می‌دهد، نمونه‌برداری متمرکز در این ناحیه دقت تقریب جبهه شوک را به شدت افزایش داد."),
        
        ("سؤال ۵: چرا حل‌گر مرجع طیفی نوشتی؟ مگه هدف PINN نبود؟",
         "معادله غیرخطی برگرز جواب تحلیلی بسته ساده ندارد. برای اینکه بفهمیم شبکه چقدر خطا دارد و بتوانیم نمودار خطا و خطای نسبی L2 رسم کنیم، نیازمند یک حل‌گر مرجع با دقت بسیار بالا بودیم. بنابراین یک حل‌گر طیفی فوریه با دقت فوق‌العاده بالا پیاده کردیم تا خروجی PINN را با آن مقایسه کنیم."),
        
        ("سؤال ۶: چرا مسئله معکوس را بررسی نکردی و فقط روی مسئله مستقیم متمرکز شدی؟",
         "به توصیه استاد راهنما (جناب آقای دکتر آذرنوید)، برای حفظ عمق علمی و تمرکز دقیق بر چالش‌های بازسازی جبهه‌های نوک‌تیز شوک و ارزیابی موشکافانه خطاهای تقریب مکانی-زمانی، دامنه پژوهش به‌طور کامل و تخصصی بر حل مسئله مستقیم معطوف گردید.")
    ]
    
    for q, a in qa_list:
        q_box = [
            [Paragraph(fa(q), q_style)],
            [Paragraph(fa(a), ans_style)]
        ]
        q_table = Table(q_box, colWidths=[A4[0]-80])
        q_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#FDF2F2')),
            ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#F0FDF4')),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
            ('LINEBELOW', (0,0), (-1,0), 0.5, colors.HexColor('#FECACA')),
            ('PADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(q_table)
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # ================== PAGE 5 ==================
    story.append(Paragraph(fa("۶. سناریوی پیشنهادی ارائه اسلایدها در جلسه دفاع (۲۰ دقیقه)"), h1_style))
    story.append(Paragraph(fa(
        "زمان‌بندی ایده‌آل و چکیده مطالبی که در هر اسلاید باید بیان کنید:"
    ), body_style))
    
    slides = [
        ("اسلاید ۱-۲ (۲ دقیقه): عنوان و بیان مسئله", "معرفی خود و استاد راهنما؛ توضیح اینکه روش‌های سنتی وابسته به شبکه محاسباتی و شبکه‌های عصبی معمولی نیازمند داده انبوه هستند."),
        ("اسلاید ۳-۴ (۳ دقیقه): معادله برگرز و چالش شوک", "معرفی فرمول برگرز و توضیح رقابت همرفت و لزجت؛ اشاره به تشکیل جبهه تیز شوک به عنوان یک مسئله معیار استاندارد در مکانیک سیالات."),
        ("اسلاید ۵-۷ (۵ دقیقه): معماری PINN و مشتق‌گیری خودکار", "نمایش دیاگرام بلوکی؛ تشریح نحوه استخراج مشتقات با مشتق‌گیری خودکار در JAX؛ تعریف تابع خطای دوقلو (MSE_u + MSE_f)."),
        ("اسلاید ۸-۹ (۳ دقیقه): حل‌گر مرجع طیفی و تنظیمات آزمایش", "توضیح حل‌گر طیفی فوریه به عنوان خط‌کش آزمون و مشخصات آزمایش (۲۰۰ نقطه مرزی، ۱۰۰۰۰ نقطه هم‌مکانی، بهینه‌ساز ترکیبی)."),
        ("اسلاید ۱۰-۱۲ (۵ دقیقه): نتایج تجربی، مقایسه با مرجع و نمودارها", "نمایش نمودار مقاطع زمانی (t=0.25, 0.5, 0.75) و بازسازی شوک؛ نمایش نقشه دو بعدی خطا؛ گزارش خطای نسبی ۲.۱۵ درصد و مقایسه با مقاله معتبر رئیسی ۲۰۱۹."),
        ("اسلاید ۱۳ (۲ دقیقه): نتیجه‌گیری و کارهای آینده", "جمع‌بندی دستاوردها در حل بدون شبکه معادلات غیرخطی؛ پیشنهاد برای کارهای آینده (توابع فعال‌ساز تطبیقی، روش‌های دامنه فرکانسی).")
    ]
    
    slide_table_data = [[
        Paragraph(fa("<b>نکات کلیدی صحبت دانشجو در جلسه</b>"), ParagraphStyle('SH', fontName='Vazir-Bold', fontSize=8.5, alignment=1, textColor=colors.white)),
        Paragraph(fa("<b>بخش و زمان</b>"), ParagraphStyle('SH', fontName='Vazir-Bold', fontSize=8.5, alignment=1, textColor=colors.white))
    ]]
    for s_title, s_points in slides:
        slide_table_data.append([
            Paragraph(fa(s_points), body_style),
            Paragraph(fa(f"<b>{s_title}</b>"), ParagraphStyle('ST', fontName='Vazir-Bold', fontSize=8.5, alignment=2, textColor=colors.HexColor('#003366')))
        ])
    
    slide_table = Table(slide_table_data, colWidths=[355, 160])
    slide_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F766E')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')])
    ]))
    story.append(slide_table)
    story.append(Spacer(1, 10))
    
    final_box_data = [[
        Paragraph(fa(
            "<b>پیام پایانی و رمز موفقیت در دفاع:</b> در جلسه دفاع با آرامش و تسلط صحبت کنید. اگر نکته‌ای را فراموش کردید، روی اصل فیزیک و مفهوم کلیدی تمرکز کنید: <i>«شبکه عصبی بر اساس قانون بقای فیزیک هدایت می‌شود و با کمترین داده، رفتار دقیق موج شوک را بازتولید می‌نماید.»</i> با آرزوی درخشش و نمره عالی برای شما!"
        ), ParagraphStyle('Fin', parent=body_style, fontName='Vazir-Bold', fontSize=9, textColor=colors.HexColor('#064E3B')))
    ]]
    final_table = Table(final_box_data, colWidths=[A4[0]-80])
    final_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ECFDF5')),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#10B981')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(final_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Guide PDF generated successfully at: {filename}")

if __name__ == '__main__':
    create_guide_pdf()
