# راهنمای راه‌اندازی پروژه

این پروژه یک ربات تلگرامی سخنگو هست که مثل یک هوش مصنوعی تو گروه عمل میکنه و بنا به چیزهایی که مدیران گروه بهش یاد میدن میتونه صحبت کنه یا حتی ویس بده ! این پروژه به بهینه ترین حالت ممکن برنامه نویسی شده و پتانسیل فعالیت در چندین هزار گروه رو به صورت همزمان داره و میتونه میلیون ها کلید و مقدار یاد بگیره
## 1. ویرایش فایل کانفیگ

ابتدا فایل کانفیگ را که در مسیر `Khan/db/config.py` قرار دارد، ویرایش کرده و اطلاعات مربوط به تنظیمات پایگاه داده، کلیدهای امنیتی و سایر پارامترهای مهم را وارد کنید.

## 2. ایجاد محیط مجازی

برای اطمینان از اجرای پروژه در یک محیط ایزوله و کنترل شده، یک محیط مجازی ایجاد کنید. برای این کار، دستور زیر را در ترمینال اجرا کنید:

```bash
python3 -m venv venv
```

## 3. ورود به محیط مجازی
پس از ایجاد محیط مجازی، با استفاده از دستور زیر وارد آن شوید:
```bash
source venv/bin/activate
```

نکته: در سیستم‌های ویندوزی، برای فعال‌سازی محیط مجازی از دستور venv\Scripts\activate استفاده کنید.

## 4. نصب پیش‌نیازها
در محیط مجازی، پیش‌نیازهای پروژه را با اجرای دستور زیر نصب کنید:

```bash
pip install -r requirements.txt
```

## 5. اطمینان از نصب موفقیت‌آمیز
اطمینان حاصل کنید که تمامی کتابخانه‌های مورد نیاز به درستی نصب شده‌اند. همچنین بررسی کنید که نرم‌افزارهای tmux، mongo و redis در سیستم شما نصب شده باشند.

## 6. اجرای ربات
پس از انجام تمامی مراحل بالا، می‌توانید ربات را با دستور زیر اجرا کنید:
```bash
python run.py RunAll
```

برای خاموش کردن ربات، از دستور زیر استفاده کنید:
```bash
python run.py KillAll
```

## 7. ساخت ربات‌های جدید
در صورتی که نیاز به ساخت ربات‌های جدید دارید، می‌توانید به سادگی یک پوشه جدید با نام متفاوت ایجاد کرده و محتویات پوشه Khan را در آن کپی کنید. سپس با ساخت یک فایل کانفیگ جدید در مسیر مناسب، می‌توانید به صورت نامحدود ربات‌های جدید بسازید.


## با دادن ستاره به پروژه میتوانید از من حمایت کنید (:
