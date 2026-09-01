# PHOENIX Client Intelligence Registry

## هدف
افزودن قابلیت‌هایی که برای پروژه‌های مشتریان PHOENIX قابل استفاده، قابل توضیح و قابل اندازه‌گیری باشند؛ بدون وابستگی اجباری به سرویس خاص و بدون جایگزینی تصمیم انسانی.

## قابلیت‌های فعال‌شده در هسته

| قابلیت | ماژول | کاربرد |
|---|---|---|
| Social Performance | `phoenix_core.customer_intelligence.SocialMetrics` | محاسبه retention، save-rate، share-rate و conversion-rate از داده مجاز شبکه اجتماعی |
| Content/Funnel Intelligence | `funnel_stage`, `content_score` | اتصال محتوا به Awareness/Consideration/Conversion و امتیازدهی بر مبنای عملکرد |
| Lead Scoring | `lead_score` | اولویت‌بندی سرنخ‌ها با مدل شفاف intent/fit/engagement/recency |
| Customer Segmentation | `segment_customer` | بخش‌بندی ساده و قابل توضیح RFM-style برای خدمات و فروش |
| Business Health | `business_health` | تشخیص گلوگاه عملیاتی از درآمد، تبدیل، نگهداشت و حاشیه سود |

## منابع متن‌باز بررسی‌شده

- Social-media analytics repositories: بررسی برای استخراج الگوهای متریک و داشبورد؛ کدهای وابسته به scraping یا APIهای غیرمجاز وارد هسته نشدند.
- Digital-Marketing-Analytics: به‌عنوان منبع ایده برای تحلیل کمپین و KPI بررسی شد؛ وابستگی مستقیم پذیرفته نشد.
- Customer segmentation / recommendation repositories: الگوهای RFM و بخش‌بندی بررسی شدند؛ پیاده‌سازی سبک و مستقل PHOENIX انتخاب شد.
- AdventureWorks CRM intelligence: برای الگوهای تحلیل مشتری/CRM بررسی شد؛ به‌دلیل حوزه و پیچیدگی داده، کد مستقیم وارد هسته نشد.

## اصول پذیرش
1. کاربرد واقعی برای حداقل یک دسته مشتری PHOENIX.
2. خروجی قابل توضیح و قابل آزمون.
3. ترجیح کد مستقل و کوچک بر وابستگی سنگین.
4. عدم scraping غیرمجاز Instagram یا جمع‌آوری داده خصوصی.
5. عدم تشخیص قطعی ویژگی‌های روان‌شناختی افراد؛ فقط تحلیل رفتار مشاهده‌شده و داده‌های مجاز.
6. هر قابلیت باید قابل اتصال به Data Access، Memory، Agents و Monitoring باشد.
7. تصمیم نهایی کسب‌وکار با انسان باقی می‌ماند.

## نقشه توسعه بعدی
- Meta/Instagram Graph API adapter با مجوزهای رسمی
- صفحه‌خوان KPI و تشخیص افت عملکرد محتوا
- Content recommendation engine بر اساس عملکرد واقعی
- CRM pipeline و lifecycle scoring
- churn/retention prediction با داده کافی
- A/B test evaluator برای پیام و پیشنهاد فروش
- dashboard مشتری و گزارش خودکار
