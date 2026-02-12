import base64
import requests
import os

# فایل ورودی و خروجی
INPUT_FILE = "input.txt"
OUTPUT_FILE = "output/base64.txt"

def read_links(file_path=INPUT_FILE):
    """خواندن لینک‌ها از فایل ورودی"""
    if not os.path.exists(file_path):
        print(f"[Error] فایل لینک موجود نیست: {file_path}")
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def fetch_content(url, timeout=10):
    """دریافت محتوا از URL و تبدیل به Base64"""
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        content = resp.text.strip()
        try:
            return base64.b64decode(content).decode("utf-8")
        except Exception:
            return content  # در صورتی که تبدیل به Base64 نشد، محتوای خام برمی‌گردد
    except Exception as e:
        print(f"[Error] {url} -> {e}")
        return ""

def merge_and_deduplicate(contents):
    """ادغام محتوا و حذف خطوط تکراری"""
    lines = []
    for c in contents:
        lines.extend(c.splitlines())
    unique_lines = list(dict.fromkeys([line.strip() for line in lines if line.strip()]))
    return "\n".join(unique_lines)

def encode_base64(data):
    """کد کردن داده‌ها به Base64"""
    return base64.b64encode(data.encode("utf-8")).decode("utf-8")

def clear_output(file_path=OUTPUT_FILE):
    """پاک کردن فایل خروجی قبلی"""
    if os.path.exists(file_path):
        open(file_path, "w", encoding="utf-8").close()
        print(f"[Info] فایل خروجی پاک شد: {file_path}")

def run_task():
    """اجرای پردازش‌ها"""
    print("[Info] شروع پردازش...")
    clear_output()  # پاک کردن فایل خروجی قبل از هر پردازش
    links = read_links()  # خواندن لینک‌ها از فایل ورودی
    if not links:
        print("[Warning] لینک برای پردازش موجود نیست!")
        return

    all_contents = [fetch_content(url) for url in links]  # دریافت محتوا از لینک‌ها
    merged = merge_and_deduplicate(all_contents)  # ادغام و حذف تکرارها
    b64_result = encode_base64(merged)  # تبدیل به Base64

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(b64_result)  # ذخیره خروجی در فایل
    print(f"[Done] خروجی ساخته شد: {OUTPUT_FILE}")

if __name__ == "__main__":
    run_task()
