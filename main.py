import os
import base64
import requests

INPUT_FILE = "input.txt"
OUTPUT_FILE = "output/clash-meta.yaml"

def read_links():
    """
    خواندن لینک‌ها از فایل input.txt
    """
    if not os.path.exists(INPUT_FILE):
        print(f"[Error] فایل ورودی یافت نشد: {INPUT_FILE}")
        return []
    with open(INPUT_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]

def fetch_sub(url):
    """
    دریافت ساب از لینک‌ها
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"[Error] دریافت لینک {url} با خطا مواجه شد: {e}")
        return ""

def decode_sub(content):
    """
    دیکد کردن ساب (بر اساس base64 یا بدون آن)
    """
    try:
        # ابتدا سعی می‌کنیم که محتوا را base64 decode کنیم
        return base64.b64decode(content).decode("utf-8")
    except Exception:
        return content  # اگر decode نشد، همان محتوا را برمی‌گردانیم

def to_yaml(subs):
    """
    تبدیل داده‌ها به فرمت YAML
    """
    yaml_content = "proxies:\n"
    for i, sub in enumerate(subs):
        decoded = decode_sub(sub)
        yaml_content += f"  - name: node{i}\n    server: {decoded}\n"
    
    # تعریف پروکسی گروپ‌ها و قوانین برای استفاده در Clash Meta
    yaml_content += "proxy-groups:\n"
    yaml_content += "  - name: Auto\n    type: select\n    proxies:\n"
    for i in range(len(subs)):
        yaml_content += f"      - node{i}\n"
    
    # قوانین ساده برای انتخاب پروکسی
    yaml_content += "rules:\n"
    yaml_content += "  - DOMAIN-SUFFIX,example.com,Auto\n"
    yaml_content += "  - GEOIP,CN,Auto\n"
    yaml_content += "  - MATCH,Auto\n"
    
    return yaml_content

def main():
    """
    اجرای فرآیند پردازش
    """
    os.makedirs("output", exist_ok=True)
    print("[Info] شروع پردازش...")
    
    # خواندن لینک‌ها
    links = read_links()
    if not links:
        print("[Warning] هیچ لینکی برای پردازش یافت نشد!")
        return
    
    # دریافت ساب‌ها
    subs = [fetch_sub(url) for url in links]
    
    # تبدیل به فرمت YAML
    yaml_data = to_yaml(subs)
    
    # ذخیره خروجی در فایل
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(yaml_data)
    
    print(f"[Done] خروجی به فرمت Clash Meta ساخته شد: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
