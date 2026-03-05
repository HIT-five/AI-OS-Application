#!/usr/bin/env python3
"""
今日头条微头条发布脚本 v2 - 改进版图片上传
"""

import json
import time
import os
import sys
import argparse
import requests
import hashlib
import hmac
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# 配置
JIMENG_CONFIG = "/home/yqj/.openclaw/workspace/skills/jimeng-image/config.json"
COOKIES_FILE = "/home/yqj/.openclaw/workspace/toutiao_mcp_server/toutiao_cookies.json"
PICTURE_DIR = "/home/yqj/picture"


class JimengImageClient:
    """即梦AI图片生成客户端"""
    
    def __init__(self, access_key_id: str, secret_access_key: str):
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.base_url = "https://visual.volcengineapi.com"
        self.host = "visual.volcengineapi.com"
        self.region = "cn-north-1"
        self.service = "cv"
    
    def _sign_v4(self, method, canonical_uri, canonical_querystring, payload, content_hash):
        timestamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
        datestamp = timestamp[:8]
        signed_headers = "content-type;host;x-content-sha256;x-date"
        canonical_headers = (
            f"content-type:application/json\n"
            f"host:{self.host}\n"
            f"x-content-sha256:{content_hash}\n"
            f"x-date:{timestamp}\n"
        )
        canonical_request = "\n".join([
            method, canonical_uri, canonical_querystring,
            canonical_headers, signed_headers, content_hash
        ])
        algorithm = "HMAC-SHA256"
        credential_scope = f"{datestamp}/{self.region}/{self.service}/request"
        string_to_sign = "\n".join([
            algorithm, timestamp, credential_scope,
            hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
        ])
        k_date = hmac.new(self.secret_access_key.encode("utf-8"), datestamp.encode("utf-8"), hashlib.sha256).digest()
        k_region = hmac.new(k_date, self.region.encode("utf-8"), hashlib.sha256).digest()
        k_service = hmac.new(k_region, self.service.encode("utf-8"), hashlib.sha256).digest()
        k_signing = hmac.new(k_service, b"request", hashlib.sha256).digest()
        signature = hmac.new(k_signing, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()
        authorization = f"{algorithm} Credential={self.access_key_id}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}"
        headers = {
            "X-Date": timestamp,
            "Authorization": authorization,
            "X-Content-Sha256": content_hash,
            "Content-Type": "application/json"
        }
        request_url = f"{self.base_url}?{canonical_querystring}"
        return headers, request_url
    
    def generate_image(self, prompt: str, ratio: str = "4:3") -> str:
        """生成图片，返回URL"""
        ratio_map = {
            "4:3": {"width": 512, "height": 384},
            "3:4": {"width": 384, "height": 512},
        }
        size = ratio_map.get(ratio, ratio_map["4:3"])
        
        req_json = {
            "req_key": "jimeng_high_aes_general_v21_L",
            "prompt": prompt,
            "return_url": True,
            "width": size["width"],
            "height": size["height"]
        }
        body = json.dumps(req_json)
        content_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()
        canonical_querystring = "Action=CVProcess&Version=2022-08-31"
        headers, request_url = self._sign_v4("POST", "/", canonical_querystring, body, content_hash)
        
        try:
            response = requests.post(request_url, headers=headers, data=body, timeout=60)
            result = response.json()
            if result.get("code") == 10000:
                urls = result.get("data", {}).get("image_urls", [])
                if urls:
                    return urls[0]
            print(f"   ⚠️ 图片生成失败: {result}")
        except Exception as e:
            print(f"   ❌ 图片生成异常: {e}")
        return None


def download_image(url: str, save_dir: str) -> str:
    """下载图片到指定目录"""
    os.makedirs(save_dir, exist_ok=True)
    
    try:
        resp = requests.get(url, timeout=30, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        if resp.status_code == 200:
            # 生成文件名
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"jimeng_{timestamp}.jpg"
            filepath = os.path.join(save_dir, filename)
            
            with open(filepath, 'wb') as f:
                f.write(resp.content)
            
            print(f"   ✅ 图片已保存: {filepath}")
            return filepath
    except Exception as e:
        print(f"   ❌ 图片下载失败: {e}")
    return None


def load_cookies():
    """加载Cookie"""
    with open(COOKIES_FILE, 'r') as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    return data.get('cookies', data)


def publish_weitt(content: str, image_paths: list = None):
    """发布微头条"""
    print(f"📝 内容长度: {len(content)}字")
    if image_paths:
        print(f"🖼️ 图片数量: {len(image_paths)}张")
        for p in image_paths:
            print(f"   - {p}")
    
    cookies = load_cookies()
    print(f"✅ 已加载 {len(cookies)} 个Cookie")
    
    options = uc.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--headless=new')
    
    print("\n🚀 启动浏览器...")
    driver = uc.Chrome(options=options, headless=True, use_subprocess=True, version_main=144)
    
    try:
        # 设置Cookie
        print("🌐 访问创作者平台...")
        driver.get("https://mp.toutiao.com")
        time.sleep(3)
        
        for cookie in cookies:
            try:
                driver.add_cookie({
                    'name': cookie['name'],
                    'value': cookie['value'],
                    'path': cookie.get('path', '/')
                })
            except:
                pass
        
        driver.refresh()
        time.sleep(3)
        
        # 访问发布页面
        print("📝 访问发布页面...")
        driver.get("https://mp.toutiao.com/profile_v4/weitoutiao/publish")
        time.sleep(5)
        
        # 等待编辑器
        print("⏳ 等待编辑器...")
        try:
            editor = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".ProseMirror"))
            )
            print("✅ 编辑器已加载")
        except:
            print("❌ 编辑器加载失败")
            driver.save_screenshot(os.path.join(PICTURE_DIR, "error_editor.png"))
            return {'success': False, 'message': '编辑器加载失败'}
        
        # === 先输入文字内容 ===
        print("✍️ 输入内容...")
        # 点击编辑器使其获得焦点
        editor.click()
        time.sleep(0.5)
        
        # 使用JavaScript输入内容
        html_content = content.replace('\n', '<br>')
        driver.execute_script("""
            var editor = arguments[0];
            editor.innerHTML = arguments[1];
            var event = new Event('input', { bubbles: true });
            editor.dispatchEvent(event);
        """, editor, html_content)
        time.sleep(2)
        print("   ✅ 内容已输入")
        
        # === 上传图片（支持多张）===
        if image_paths:
            print(f"\n📷 上传 {len(image_paths)} 张图片...")
            
            for idx, image_path in enumerate(image_paths):
                if not os.path.exists(image_path):
                    print(f"   ⚠️ 图片不存在: {image_path}")
                    continue
                    
                print(f"   [{idx+1}/{len(image_paths)}] 上传: {os.path.basename(image_path)}")
                abs_path = os.path.abspath(image_path)
                uploaded = False
                
                # 方法1: 先点击工具栏的图片按钮，触发上传区域出现
                try:
                    # 查找工具栏中的图片按钮（带有 weitoutiao-image-plugin 类或包含"图片"文本的按钮）
                    image_btn_selectors = [
                        ".weitoutiao-image-plugin button",
                        ".syl-toolbar-tool button",
                        "button:has(svg)",
                    ]
                    
                    for selector in image_btn_selectors:
                        try:
                            buttons = driver.find_elements(By.CSS_SELECTOR, selector)
                            for btn in buttons:
                                try:
                                    btn_text = btn.text.strip()
                                    if '图片' in btn_text and btn.is_displayed():
                                        print(f"       🔘 点击图片按钮: {btn_text}")
                                        driver.execute_script("arguments[0].click();", btn)
                                        time.sleep(2)
                                        break
                                except:
                                    continue
                        except:
                            continue
                except Exception as e:
                    print(f"       ⚠️ 点击图片按钮失败: {e}")
                
                # 方法2: 查找并使用file input上传
                time.sleep(1)
                file_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
                print(f"       🔍 找到 {len(file_inputs)} 个文件输入框")
                
                for inp in file_inputs:
                    try:
                        # 检查accept属性
                        accept = inp.get_attribute('accept') or ''
                        parent_class = ''
                        try:
                            parent = inp.find_element(By.XPATH, '..')
                            parent_class = parent.get_attribute('class') or ''
                        except:
                            pass
                        
                        # 优先使用图片相关的input
                        if 'image' in accept or 'upload' in parent_class.lower() or not accept:
                            # 确保input元素可交互
                            driver.execute_script("""
                                var el = arguments[0];
                                el.style.display = 'block';
                                el.style.visibility = 'visible';
                                el.style.opacity = '1';
                                el.style.position = 'relative';
                                el.style.width = '100px';
                                el.style.height = '100px';
                                el.style.zIndex = '99999';
                            """, inp)
                            time.sleep(0.5)
                            
                            # 上传图片
                            inp.send_keys(abs_path)
                            print(f"       ✅ 图片已上传 (accept={accept})")
                            uploaded = True
                            time.sleep(3)  # 等待上传完成
                            break
                    except Exception as e:
                        print(f"       ⚠️ input上传尝试失败: {str(e)[:50]}")
                        continue
                
                # 方法3: 如果还没成功，尝试通过JavaScript创建并触发
                if not uploaded:
                    print(f"       🔄 尝试备用方案...")
                    try:
                        # 查找upload-handler或类似的上传触发区域
                        upload_triggers = driver.find_elements(By.CSS_SELECTOR, 
                            ".upload-handler, .image-item-upload, .upload-wrap, .btn-upload-scand, [class*='upload']")
                        
                        for trigger in upload_triggers:
                            try:
                                if trigger.is_displayed():
                                    # 点击触发上传
                                    driver.execute_script("arguments[0].click();", trigger)
                                    time.sleep(1)
                                    
                                    # 再次查找file input
                                    new_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
                                    for inp in new_inputs:
                                        try:
                                            driver.execute_script("""
                                                arguments[0].style.display = 'block';
                                                arguments[0].style.opacity = '1';
                                            """, inp)
                                            inp.send_keys(abs_path)
                                            print(f"       ✅ 图片已上传(备用方案)")
                                            uploaded = True
                                            time.sleep(3)
                                            break
                                        except:
                                            continue
                                    if uploaded:
                                        break
                            except:
                                continue
                    except Exception as e:
                        print(f"       ⚠️ 备用方案失败: {e}")
                
                if not uploaded:
                    print(f"       ❌ 图片上传失败!")
                    # 保存调试截图
                    driver.save_screenshot(os.path.join(PICTURE_DIR, f"debug_upload_{idx}.png"))
                
                time.sleep(2)  # 每张图片之间等待
            
            # 等待所有上传完成并点击确定
            time.sleep(3)
            try:
                buttons = driver.find_elements(By.TAG_NAME, "button")
                for btn in buttons:
                    try:
                        if btn.text.strip() == '确定' and btn.is_displayed():
                            btn.click()
                            print("   ✅ 点击确定按钮")
                            time.sleep(2)
                            break
                    except:
                        continue
            except:
                pass
        
        # 保存发布前截图
        driver.save_screenshot(os.path.join(PICTURE_DIR, "before_publish.png"))
        print(f"📸 发布前截图已保存")
        
        # === 发布 ===
        print("\n🔍 查找发布按钮...")
        try:
            # 查找红色发布按钮
            publish_btn = None
            buttons = driver.find_elements(By.TAG_NAME, "button")
            for btn in buttons:
                try:
                    text = btn.text.strip()
                    if text == '发布':
                        publish_btn = btn
                        break
                except:
                    continue
            
            if publish_btn:
                driver.execute_script("arguments[0].click();", publish_btn)
                print("✅ 已点击发布按钮")
                time.sleep(3)
            else:
                print("❌ 未找到发布按钮")
                return {'success': False, 'message': '未找到发布按钮'}
            
            # 处理确认对话框
            print("🔍 检查确认对话框...")
            time.sleep(2)
            try:
                buttons = driver.find_elements(By.TAG_NAME, "button")
                for btn in buttons:
                    try:
                        text = btn.text.strip()
                        cls = btn.get_attribute('class') or ''
                        # 找红色/primary按钮
                        if ('确定' in text or '确认' in text) and btn.is_displayed():
                            driver.execute_script("arguments[0].click();", btn)
                            print("   ✅ 点击确认")
                            break
                        elif 'primary' in cls and btn.is_displayed() and text:
                            driver.execute_script("arguments[0].click();", btn)
                            print(f"   ✅ 点击primary按钮: {text}")
                            break
                    except:
                        continue
            except:
                pass
            
            time.sleep(3)
            driver.save_screenshot(os.path.join(PICTURE_DIR, "after_publish.png"))
            print(f"📸 发布后截图已保存")
            
            return {'success': True, 'message': '发布成功'}
            
        except Exception as e:
            print(f"❌ 发布失败: {e}")
            driver.save_screenshot(os.path.join(PICTURE_DIR, "error_publish.png"))
            return {'success': False, 'message': str(e)}
    
    finally:
        driver.quit()
        print("🔒 浏览器已关闭")


def main():
    parser = argparse.ArgumentParser(description='发布今日头条微头条 v2')
    parser.add_argument('--content', '-c', help='微头条内容')
    parser.add_argument('--file', '-f', help='从文件读取内容')
    parser.add_argument('--image-prompt', '-i', action='append', help='配图生成提示词(可多次使用)')
    parser.add_argument('--image', action='append', help='直接使用本地图片路径(可多次使用)')
    
    args = parser.parse_args()
    
    # 获取内容
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
    elif args.content:
        content = args.content
    else:
        print("请提供内容: --content '内容' 或 --file content.txt")
        sys.exit(1)
    
    # 生成或使用图片（支持多张）
    image_paths = []
    
    # 处理本地图片
    if args.image:
        for img in args.image:
            if os.path.exists(img):
                image_paths.append(img)
    
    # 处理AI生成图片
    if args.image_prompt:
        print(f"\n🎨 使用即梦AI生成配图...")
        
        with open(JIMENG_CONFIG, 'r') as f:
            jimeng_config = json.load(f)
        
        client = JimengImageClient(
            jimeng_config['access_key_id'],
            jimeng_config['secret_access_key']
        )
        
        for i, prompt in enumerate(args.image_prompt):
            print(f"   [{i+1}/{len(args.image_prompt)}] 提示词: {prompt}")
            image_url = client.generate_image(prompt, "4:3")
            if image_url:
                print(f"   ✅ 图片URL: {image_url[:60]}...")
                img_path = download_image(image_url, PICTURE_DIR)
                if img_path:
                    image_paths.append(img_path)
    
    # 传递所有图片
    result = publish_weitt(content, image_paths if image_paths else None)
    
    if result['success']:
        print(f"\n🎉 {result['message']}")
    else:
        print(f"\n❌ {result['message']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
