#!/usr/bin/env python3
"""
今日头条【文章】发布脚本 v2 - 简化版
核心改进：使用两次点击红色按钮的方式完成发布
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

# 配置
JIMENG_CONFIG = "/home/yqj/.openclaw/workspace/skills/jimeng-image/config.json"
COOKIES_FILE = "/home/yqj/.openclaw/workspace/toutiao_mcp_server/toutiao_cookies_childedu.json"
PICTURE_DIR = "/home/yqj/picture"
ARTICLE_PUBLISH_URL = "https://mp.toutiao.com/profile_v4/graphic/publish"


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
    
    def generate_image(self, prompt: str, ratio: str = "16:9") -> str:
        ratio_map = {
            "16:9": {"width": 640, "height": 360},
            "4:3": {"width": 512, "height": 384},
        }
        size = ratio_map.get(ratio, ratio_map["16:9"])
        
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
    os.makedirs(save_dir, exist_ok=True)
    try:
        resp = requests.get(url, timeout=30, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        if resp.status_code == 200:
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
    with open(COOKIES_FILE, 'r') as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    return data.get('cookies', data)


def click_red_button(driver, expected_text=None):
    """点击页面上的红色按钮，返回按钮文字"""
    from selenium.webdriver.common.action_chains import ActionChains
    
    # 先找到红色按钮
    red_btn = driver.execute_script("""
        var buttons = document.querySelectorAll('button');
        for (var i = 0; i < buttons.length; i++) {
            var btn = buttons[i];
            var styles = window.getComputedStyle(btn);
            var bgColor = styles.backgroundColor;
            // 检查是否是红色按钮
            if (bgColor.includes('255') && (bgColor.includes('94') || bgColor.includes('77'))) {
                if (btn.offsetParent !== null) {
                    return btn;
                }
            }
        }
        return null;
    """)
    
    if red_btn:
        text = red_btn.text.strip() if red_btn.text else ''
        # 使用ActionChains模拟真实点击
        try:
            actions = ActionChains(driver)
            actions.move_to_element(red_btn).pause(0.3).click().perform()
        except:
            # 备用: JS点击
            driver.execute_script("arguments[0].click();", red_btn)
        return {'success': True, 'text': text}
    
    return {'success': False, 'text': ''}


def publish_article(title: str, content: str, cover_path: str = None, content_images: list = None):
    """发布今日头条【文章】"""
    print("="*60)
    print("📰 今日头条【文章】发布 v2")
    print("="*60)
    print(f"📝 标题: {title}")
    print(f"📄 内容长度: {len(content)}字")
    
    cookies = load_cookies()
    print(f"✅ 已加载 {len(cookies)} 个Cookie")
    
    options = uc.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    # 使用xvfb虚拟显示器，不需要headless
    # options.add_argument('--headless=new')
    
    print("\n🚀 启动浏览器（使用xvfb虚拟显示器）...")
    driver = uc.Chrome(options=options, headless=False, use_subprocess=True, version_main=145)
    
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
        
        # 访问文章发布页面
        print(f"📝 访问文章发布页面...")
        driver.get(ARTICLE_PUBLISH_URL)
        time.sleep(5)
        
        # === 输入标题 ===
        print("\n✍️ 输入标题...")
        try:
            title_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"publish-editor-title")]//textarea'))
            )
            title_input.clear()
            title_input.send_keys(title)
            print(f"   ✅ 标题已输入")
        except Exception as e:
            print(f"   ❌ 标题输入失败: {e}")
            return {'success': False, 'message': '标题输入失败'}
        
        time.sleep(1)
        
        # === 输入正文 ===
        print("\n✍️ 输入正文...")
        try:
            editor = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.ProseMirror'))
            )
            editor.click()
            time.sleep(0.5)
            
            # 正文内容
            html_parts = []
            
            # 添加正文内容
            paragraphs = content.split('\n')
            for p in paragraphs:
                p = p.strip()
                if p:
                    # 去掉所有emoji符号（避免显示为感叹号圆圈）
                    import re
                    # 移除emoji和特殊符号
                    p = re.sub(r'[🔹💡😨🎯✨🌟⭐💪🔥❤️👍👎🎉🎊💯📌📍🚀✅❌⚠️ℹ️🔔💬📢🏆💎🌈🍀🌸🌺🌻🌼🍁🍂🍃🌴🌵🌾🌿☀️🌤️⛅🌥️🌦️🌧️☔⛈️🌩️❄️🌨️💧💦🌊⬆️⬇️➡️⬅️↗️↘️↙️↖️↩️↪️⤴️⤵️🔄🔃▶️◀️⏫⏬➕➖✖️➗💲💰🔑🔓🔒📱💻🖥️📷📹📺📻📡🔋🔌💡🔦🕯️📦📬📭📮📧📩📨📫🗂️📋📁📂🗃️📰🔖📎🖇️📐📏🗄️📑📊📈📉📄📃🧾🗒️📓📔📒📕📗📘📙📚🔗✂️🖊️🖋️✒️🖌️🖍️📝✏️🔍🔎👁️‍🗨️👀💭🗯️💬🔊🔉🔇🎵🎶🎼🎤🎧🎷🎸🎹🎺🎻🥁🪘🪗🪕🎬🎭🎨🎰🎲🃏🀄🎴🎯🎮👾🕹️🎳⚽🏀🏈⚾🥎🏐🏉🎾🥏🎱🥊🥋⛳🏌️🏇⛷️🏂🤺🏋️🤼🤸⛹️🤾🏄🏊🚣🧘🛀🛌🧗🤹🎠🎡🎢🏕️🏖️🏜️🏝️🏞️🏟️🏛️🏗️🏘️🏚️🏠🏡🏢🏣🏤🏥🏦🏨🏩🏪🏫🏬🏭🏯🏰💒🗼🗽⛪🕌🛕🕍⛩️🕋⛲⛺🌁🌃🏙️🌄🌅🌆🌇🌉🌌🎠🚂🚃🚄🚅🚆🚇🚈🚉🚊🚝🚞🚋🚌🚍🚎🚐🚑🚒🚓🚔🚕🚖🚗🚘🚙🛻🚚🛚🚜🏎️🏍️🛵🛺🚲🛴🛹🚏⛽🚨🚥🚦🚧⚓🛶⛵🚤🛥️🛳️⛴️🛫🛬🪂💺🚁🚟🚠🚡🛰️🚀🛸🌠✈️🪐⭐🌍🌎🌏🌐🗺️🧭⛰️🏔️🌋🗻🏕️🏖️🏜️🏝️🏞️]', '', p)
                    p = p.strip()
                    if not p:
                        continue
                    # 正文不用H1标题，直接用普通段落
                    html_parts.append(f'<p>{p}</p>')
                else:
                    html_parts.append('<p><br></p>')
            
            html_content = ''.join(html_parts)
            
            driver.execute_script("""
                var editor = arguments[0];
                editor.innerHTML = arguments[1];
                editor.dispatchEvent(new Event('input', {bubbles: true}));
            """, editor, html_content)
            print(f"   ✅ 正文已输入（含标题，共{len(content)}字）")
        except Exception as e:
            print(f"   ❌ 正文输入失败: {e}")
            return {'success': False, 'message': '正文输入失败'}
        
        time.sleep(2)
        
        # 正文图片插入功能暂不支持
        if False and content_images:
            print(f"\n📷 插入正文图片 ({len(content_images)} 张)...")
            for img_path in content_images:
                if os.path.exists(img_path):
                    try:
                        # 方法：直接点击编辑器工具栏的图片图标
                        # 图片图标通常是一个山/太阳的SVG图标
                        
                        # 先点击编辑器获取焦点，并将光标移到标题后
                        editor.click()
                        time.sleep(0.5)
                        
                        # 移动光标到H1标题后面
                        driver.execute_script("""
                            var editor = arguments[0];
                            var h1 = editor.querySelector('h1');
                            if (h1 && h1.nextSibling) {
                                var range = document.createRange();
                                var sel = window.getSelection();
                                range.setStartAfter(h1);
                                range.collapse(true);
                                sel.removeAllRanges();
                                sel.addRange(range);
                            }
                        """, editor)
                        time.sleep(0.5)
                        
                        # 查找并点击图片按钮 - 通过SVG图标特征识别
                        img_btn_result = driver.execute_script("""
                            // 查找所有工具栏按钮
                            var allBtns = document.querySelectorAll('button');
                            var toolbarBtns = [];
                            
                            for (var i = 0; i < allBtns.length; i++) {
                                var btn = allBtns[i];
                                var rect = btn.getBoundingClientRect();
                                // 工具栏按钮在y=80-120范围内
                                if (rect.y > 70 && rect.y < 130 && rect.width > 20 && rect.width < 50) {
                                    var svg = btn.querySelector('svg');
                                    var hasMountainIcon = false;
                                    if (svg) {
                                        // 检查SVG是否包含图片图标的特征（山形或太阳）
                                        var paths = svg.querySelectorAll('path, circle, rect');
                                        var pathCount = paths.length;
                                        // 图片图标通常有2-4个path
                                        if (pathCount >= 2 && pathCount <= 5) {
                                            hasMountainIcon = true;
                                        }
                                    }
                                    toolbarBtns.push({
                                        btn: btn,
                                        x: rect.x,
                                        y: rect.y,
                                        hasSvg: !!svg,
                                        hasMountain: hasMountainIcon,
                                        index: i
                                    });
                                }
                            }
                            
                            // 按x坐标排序
                            toolbarBtns.sort(function(a, b) { return a.x - b.x; });
                            
                            // 打印所有按钮位置供调试
                            var btnInfo = toolbarBtns.map(function(b, idx) {
                                return idx + ':x=' + Math.round(b.x);
                            }).join(', ');
                            
                            // 图片按钮位置分析（根据工具栏x坐标）:
                            // 工具栏按钮: 0:x=374, 1:x=414, 2:x=454, 3:x=494, 4:x=559, 5:x=599, 
                            //            6:x=639, 7:x=679, 8:x=729(图片), 9:x=769(链接)...
                            // 图片按钮应该是索引8 (x=729左右)
                            var targetIndices = [8, 7, 9, 6];
                            
                            for (var t = 0; t < targetIndices.length; t++) {
                                var idx = targetIndices[t];
                                if (toolbarBtns[idx]) {
                                    toolbarBtns[idx].btn.click();
                                    return {
                                        clicked: true, 
                                        x: Math.round(toolbarBtns[idx].x), 
                                        index: idx, 
                                        total: toolbarBtns.length,
                                        allBtns: btnInfo
                                    };
                                }
                            }
                            
                            return {clicked: false, total: toolbarBtns.length, allBtns: btnInfo};
                        """)
                        
                        print(f"   🔍 工具栏: {img_btn_result.get('allBtns', 'N/A')}")
                        
                        if img_btn_result and img_btn_result.get('clicked'):
                            print(f"   ✅ 点击了第{img_btn_result.get('index')}个按钮 (x={img_btn_result.get('x')})")
                            time.sleep(2)
                            
                            # 保存点击后的截图
                            driver.save_screenshot(os.path.join(PICTURE_DIR, "article_v2_img_dialog.png"))
                            
                            # 点击图片按钮后会弹出下拉菜单
                            # 需要点击"本地图片上传"选项
                            time.sleep(1)  # 等待下拉菜单出现
                            
                            # 保存下拉菜单截图用于调试
                            driver.save_screenshot(os.path.join(PICTURE_DIR, "article_v2_img_dropdown.png"))
                            
                            # 查找所有在下拉菜单位置区域的元素（放宽条件）
                            all_elements_in_area = driver.execute_script("""
                                var result = [];
                                var allElements = document.querySelectorAll('*');
                                for (var i = 0; i < allElements.length; i++) {
                                    var el = allElements[i];
                                    var rect = el.getBoundingClientRect();
                                    
                                    // 查找下拉菜单区域 (约 x=180-270, y=265-300) 的所有元素
                                    if (rect.x >= 170 && rect.x <= 280
                                        && rect.y >= 260 && rect.y <= 310
                                        && rect.width > 30 && rect.width < 150
                                        && rect.height > 15 && rect.height < 60) {
                                        var style = window.getComputedStyle(el);
                                        result.push({
                                            tag: el.tagName,
                                            x: Math.round(rect.x),
                                            y: Math.round(rect.y),
                                            w: Math.round(rect.width),
                                            h: Math.round(rect.height),
                                            pos: style.position,
                                            z: style.zIndex,
                                            class: (el.className || '').substring(0, 20),
                                            text: (el.innerText || '').substring(0, 10)
                                        });
                                    }
                                }
                                return result;
                            """)
                            print(f"   🔍 下拉区域元素: {all_elements_in_area[:5]}")  # 只打印前5个
                            
                            # 方法：直接点击该区域的所有可点击元素
                            dropdown_click_result = driver.execute_script("""
                                var allElements = document.querySelectorAll('*');
                                var candidates = [];
                                
                                for (var i = 0; i < allElements.length; i++) {
                                    var el = allElements[i];
                                    var rect = el.getBoundingClientRect();
                                    
                                    // 下拉菜单区域
                                    if (rect.x >= 170 && rect.x <= 280
                                        && rect.y >= 260 && rect.y <= 310
                                        && rect.width > 30 && rect.width < 150
                                        && rect.height > 15 && rect.height < 60) {
                                        candidates.push({el: el, area: rect.width * rect.height, y: rect.y});
                                    }
                                }
                                
                                // 按y坐标排序（取第一个，即最上面的）
                                candidates.sort(function(a, b) { return a.y - b.y; });
                                
                                if (candidates.length > 0) {
                                    // 点击第一个候选元素
                                    candidates[0].el.click();
                                    var rect = candidates[0].el.getBoundingClientRect();
                                    return {
                                        success: true,
                                        tag: candidates[0].el.tagName,
                                        x: rect.x,
                                        y: rect.y,
                                        count: candidates.length
                                    };
                                }
                                
                                return {success: false, count: 0};
                            """)
                            print(f"   🔍 点击下拉菜单: {dropdown_click_result}")
                            
                            time.sleep(3)  # 等待资源选择器弹出
                            
                            # 保存点击后的截图
                            driver.save_screenshot(os.path.join(PICTURE_DIR, "article_v2_after_dropdown_click.png"))
                            
                            # 查找弹出的file input
                            file_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="file"]')
                            print(f"   🔍 找到 {len(file_inputs)} 个file input")
                            
                            img_uploaded = False
                            
                            # 如果有file input，上传图片
                            if len(file_inputs) > 0:
                                for idx, inp in enumerate(file_inputs):
                                    try:
                                        driver.execute_script("""
                                            arguments[0].style.display = 'block';
                                            arguments[0].style.visibility = 'visible';
                                            arguments[0].style.opacity = '1';
                                            arguments[0].style.height = '50px';
                                            arguments[0].style.width = '200px';
                                        """, inp)
                                        time.sleep(0.5)
                                        inp.send_keys(img_path)
                                        print(f"   ✅ 已上传正文图片: {os.path.basename(img_path)}")
                                        img_uploaded = True
                                        time.sleep(5)  # 等待上传完成
                                        
                                        # 保存上传后截图
                                        driver.save_screenshot(os.path.join(PICTURE_DIR, "article_v2_content_img_uploaded.png"))
                                        
                                        # 选择刚上传的图片（点击图片缩略图）
                                        driver.execute_script("""
                                            var imgs = document.querySelectorAll('[class*="resource"] img, [class*="thumbnail"] img, [class*="image-item"] img');
                                            for (var i = 0; i < imgs.length; i++) {
                                                var img = imgs[i];
                                                var rect = img.getBoundingClientRect();
                                                if (rect.width > 50 && rect.height > 50) {
                                                    img.click();
                                                    break;
                                                }
                                            }
                                        """)
                                        time.sleep(1)
                                        
                                        # 点击确定按钮关闭资源选择器
                                        confirm_clicked = driver.execute_script("""
                                            var buttons = document.querySelectorAll('button');
                                            for (var i = 0; i < buttons.length; i++) {
                                                var text = buttons[i].innerText.trim();
                                                if (text === '确定' || text === '确认' || text === '插入') {
                                                    buttons[i].click();
                                                    return true;
                                                }
                                            }
                                            return false;
                                        """)
                                        if confirm_clicked:
                                            print("   ✅ 已点击确定按钮")
                                        time.sleep(2)
                                        break
                                    except Exception as e:
                                        print(f"   ⚠️ input #{idx} 失败: {e}")
                                        continue
                            
                            if not img_uploaded:
                                print("   ⚠️ 正文图片未能成功上传")
                        else:
                            print(f"   ⚠️ 未能点击图片按钮")
                            
                    except Exception as e:
                        print(f"   ⚠️ 插入正文图片异常: {e}")
        
        # 保存发布前截图
        driver.save_screenshot(os.path.join(PICTURE_DIR, "article_v2_before.png"))
        print("📸 已保存发布前截图")
        
        # === 发布流程 ===
        # 1. 先选择"无封面"（避免封面必填问题）
        # 2. 点击"预览并发布" -> 弹出预览界面
        # 3. 在预览界面右下方找到"确认发布"按钮并点击
        
        print("\n🚀 开始发布流程...")
        
        # 处理封面
        cover_uploaded = False
        if cover_path and os.path.exists(cover_path):
            print("\n--- 上传封面图片 ---")
            try:
                # 滚动到封面区域
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                
                cover_section = driver.find_elements(By.XPATH, '//*[contains(text(),"展示封面")]')
                if cover_section:
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cover_section[0])
                    time.sleep(1)
                
                # 先选择"单图"模式
                single_cover_options = driver.find_elements(By.XPATH, '//*[contains(text(),"单图")]')
                for opt in single_cover_options:
                    try:
                        if opt.is_displayed():
                            opt.click()
                            print("   ✅ 已选择'单图'模式")
                            time.sleep(2)
                            break
                    except:
                        continue
                
                # 保存截图以便调试
                driver.save_screenshot(os.path.join(PICTURE_DIR, "article_v2_cover_area.png"))
                
                # 用JavaScript找到并操作file input
                # 今日头条的上传组件通常用隐藏的input[type=file]
                upload_result = driver.execute_script("""
                    // 查找所有file input
                    var inputs = document.querySelectorAll('input[type="file"]');
                    console.log('Found ' + inputs.length + ' file inputs');
                    
                    // 也查找可能的上传容器
                    var uploadContainers = document.querySelectorAll('[class*="upload"], [class*="cover-upload"], [class*="dragger"]');
                    
                    return {
                        inputCount: inputs.length,
                        containerCount: uploadContainers.length,
                        pageHtml: document.body.innerHTML.substring(0, 5000)
                    };
                """)
                print(f"   🔍 JS检测: {upload_result['inputCount']} file inputs, {upload_result['containerCount']} upload containers")
                
                # 尝试直接用JS创建并触发上传
                file_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="file"]')
                
                if len(file_inputs) == 0:
                    # 如果没有file input，尝试点击上传区域来触发
                    print("   🔄 尝试点击上传区域触发file input...")
                    
                    # 查找带"+"号的上传框
                    upload_box = driver.execute_script("""
                        var elements = document.querySelectorAll('*');
                        for (var i = 0; i < elements.length; i++) {
                            var el = elements[i];
                            var text = el.innerText || '';
                            var rect = el.getBoundingClientRect();
                            // 查找封面上传区域附近的可点击元素
                            if (rect.width > 50 && rect.width < 200 && rect.height > 50 && rect.height < 200) {
                                var classes = el.className || '';
                                if (classes.includes('upload') || classes.includes('cover') || classes.includes('dragger')) {
                                    return el;
                                }
                            }
                        }
                        return null;
                    """)
                    
                    if upload_box:
                        upload_box.click()
                        time.sleep(2)
                        file_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="file"]')
                        print(f"   🔍 点击后找到 {len(file_inputs)} 个file input")
                
                # 上传图片
                for idx, file_input in enumerate(file_inputs):
                    try:
                        # 使input可交互
                        driver.execute_script("""
                            var el = arguments[0];
                            el.style.display = 'block';
                            el.style.visibility = 'visible';
                            el.style.opacity = '1';
                            el.style.position = 'absolute';
                            el.style.top = '0';
                            el.style.left = '0';
                            el.style.width = '100px';
                            el.style.height = '100px';
                            el.style.zIndex = '99999';
                        """, file_input)
                        time.sleep(0.5)
                        
                        file_input.send_keys(cover_path)
                        print(f"   ✅ 图片已上传 (input #{idx}): {cover_path}")
                        time.sleep(5)  # 等待上传完成
                        
                        # 保存上传后截图
                        driver.save_screenshot(os.path.join(PICTURE_DIR, "article_v2_after_upload.png"))
                        
                        # 处理资源选择侧边栏
                        # 1. 选择刚上传的图片（点击图片）
                        print("   🔄 选择上传的图片...")
                        time.sleep(2)
                        
                        # 查找并点击图片缩略图
                        img_selected = driver.execute_script("""
                            // 在资源选择器中找到图片并点击
                            var imgs = document.querySelectorAll('.resource-select img, [class*="resource"] img, [class*="thumbnail"] img');
                            for (var i = 0; i < imgs.length; i++) {
                                var img = imgs[i];
                                var rect = img.getBoundingClientRect();
                                if (rect.width > 30 && rect.height > 30) {
                                    img.click();
                                    return true;
                                }
                            }
                            // 也尝试点击可选的资源项
                            var items = document.querySelectorAll('[class*="resource-item"], [class*="selectable"]');
                            for (var i = 0; i < items.length; i++) {
                                items[i].click();
                                return true;
                            }
                            return false;
                        """)
                        if img_selected:
                            print("   ✅ 已选择图片")
                        time.sleep(1)
                        
                        # 2. 点击"确定"按钮关闭资源选择器
                        print("   🔄 点击确定关闭资源选择器...")
                        confirm_clicked = driver.execute_script("""
                            // 查找资源选择器里的确定按钮
                            var buttons = document.querySelectorAll('button');
                            for (var i = 0; i < buttons.length; i++) {
                                var btn = buttons[i];
                                var text = btn.innerText.trim();
                                if (text === '确定' || text === '确认') {
                                    var rect = btn.getBoundingClientRect();
                                    // 确保是右侧面板的按钮（x坐标较大）
                                    if (rect.x > 700 && rect.width > 0) {
                                        btn.click();
                                        return true;
                                    }
                                }
                            }
                            return false;
                        """)
                        if confirm_clicked:
                            print("   ✅ 已关闭资源选择器")
                            cover_uploaded = True
                        time.sleep(2)
                        
                        break
                    except Exception as e:
                        print(f"   ⚠️ input #{idx} 上传失败: {e}")
                        continue
                
            except Exception as e:
                print(f"   ⚠️ 封面上传异常: {e}")
            
            # 如果封面上传失败，选择无封面
            if not cover_uploaded:
                print("   ⚠️ 封面上传未成功，将使用无封面发布")
                no_cover_options = driver.find_elements(By.XPATH, '//*[contains(text(),"无封面")]')
                for opt in no_cover_options:
                    try:
                        if opt.is_displayed():
                            opt.click()
                            print("   ✅ 已选择'无封面'")
                            time.sleep(1)
                            break
                    except:
                        continue
        else:
            # 没有封面，选择"无封面"
            print("\n--- 选择无封面 ---")
            
            # 先滚动到封面区域
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            
            # 使用Selenium直接查找并点击"无封面"
            from selenium.webdriver.common.action_chains import ActionChains
            no_cover_clicked = False
            
            # 方法1：使用XPath查找包含"无封面"文字的label
            try:
                no_cover_labels = driver.find_elements(By.XPATH, '//label[contains(text(),"无封面")] | //label[.//span[contains(text(),"无封面")]]')
                print(f"   🔍 找到 {len(no_cover_labels)} 个无封面label")
                for label in no_cover_labels:
                    if label.is_displayed():
                        actions = ActionChains(driver)
                        actions.move_to_element(label).click().perform()
                        print(f"   ✅ 已点击无封面label (ActionChains)")
                        no_cover_clicked = True
                        break
            except Exception as e:
                print(f"   ⚠️ XPath查找失败: {e}")
            
            # 方法2：如果方法1失败，使用JS点击
            if not no_cover_clicked:
                js_result = driver.execute_script("""
                    // 查找所有span/label，找到"无封面"
                    var elements = document.querySelectorAll('span, label');
                    for (var i = 0; i < elements.length; i++) {
                        var el = elements[i];
                        var text = el.innerText ? el.innerText.trim() : '';
                        if (text === '无封面') {
                            // 模拟真实点击
                            var rect = el.getBoundingClientRect();
                            var clickEvent = new MouseEvent('click', {
                                view: window,
                                bubbles: true,
                                cancelable: true,
                                clientX: rect.left + rect.width / 2,
                                clientY: rect.top + rect.height / 2
                            });
                            el.dispatchEvent(clickEvent);
                            return {success: true, method: 'js_mouse_click', text: text};
                        }
                    }
                    return {success: false};
                """)
                if js_result and js_result.get('success'):
                    print(f"   ✅ 已选择'无封面' (方法: {js_result.get('method')})")
                    no_cover_clicked = True
            
            # 方法3：直接点击第三个封面radio选项
            if not no_cover_clicked:
                try:
                    # 封面选项通常是: 单图、三图、无封面
                    cover_radios = driver.find_elements(By.XPATH, '//label[contains(@class,"radio") or contains(@class,"Radio")]')
                    # 过滤出封面区域的radio（通过位置判断）
                    cover_section_radios = []
                    for radio in cover_radios:
                        try:
                            text = radio.text.strip()
                            if text in ['单图', '三图', '无封面']:
                                cover_section_radios.append(radio)
                        except:
                            pass
                    
                    print(f"   🔍 找到 {len(cover_section_radios)} 个封面radio选项")
                    # 点击"无封面"
                    for radio in cover_section_radios:
                        if '无封面' in radio.text:
                            actions = ActionChains(driver)
                            actions.move_to_element(radio).click().perform()
                            print(f"   ✅ 已点击无封面radio")
                            no_cover_clicked = True
                            break
                except Exception as e:
                    print(f"   ⚠️ 方法3失败: {e}")
            
            time.sleep(2)
            
            if not no_cover_clicked:
                print("   ⚠️ 未能成功选择无封面")
            
            # 保存封面选择后的截图
            driver.save_screenshot(os.path.join(PICTURE_DIR, "article_v2_cover_selected.png"))
            
            # 验证是否成功选择了无封面
            verify_result = driver.execute_script("""
                var radios = document.querySelectorAll('input[type="radio"]');
                for (var i = 0; i < radios.length; i++) {
                    var radio = radios[i];
                    if (radio.checked) {
                        var parent = radio.parentElement;
                        var text = parent ? parent.innerText : '';
                        return {checked: true, text: text.trim().substring(0, 20)};
                    }
                }
                return {checked: false};
            """)
            print(f"   📋 当前选中: {verify_result}")
        
        # 滚动到底部
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        
        # === 选择"投放广告赚收益" ===
        print("\n--- 选择投放广告赚收益 ---")
        ad_selected = False
        try:
            # 方法1: 查找包含"投放广告赚收益"的元素并点击
            ad_options = driver.find_elements(By.XPATH, '//*[contains(text(),"投放广告赚收益")]')
            for opt in ad_options:
                try:
                    if opt.is_displayed():
                        # 找到父级的label或可点击元素
                        parent = opt
                        for _ in range(5):
                            parent = parent.find_element(By.XPATH, '..')
                            tag = parent.tag_name.lower()
                            if tag in ['label', 'div', 'span']:
                                try:
                                    parent.click()
                                    print(f"   ✅ 已点击'投放广告赚收益' (标签: {tag})")
                                    ad_selected = True
                                    break
                                except:
                                    continue
                        if ad_selected:
                            break
                        # 如果父级都不行，直接点击文字元素
                        if not ad_selected:
                            opt.click()
                            print(f"   ✅ 已点击'投放广告赚收益' (直接点击)")
                            ad_selected = True
                            break
                except Exception as e:
                    continue
            
            # 方法2: 用JS点击
            if not ad_selected:
                js_result = driver.execute_script("""
                    var elements = document.querySelectorAll('*');
                    for (var i = 0; i < elements.length; i++) {
                        var el = elements[i];
                        var text = el.innerText || el.textContent || '';
                        if (text.includes('投放广告赚收益') && !text.includes('不投放')) {
                            // 查找可点击的父元素
                            var clickable = el;
                            while (clickable.parentElement) {
                                var tag = clickable.tagName.toLowerCase();
                                if (tag === 'label' || clickable.classList.contains('radio') || clickable.classList.contains('Radio')) {
                                    clickable.click();
                                    return {success: true, tag: tag};
                                }
                                clickable = clickable.parentElement;
                            }
                            // 直接点击
                            el.click();
                            return {success: true, tag: el.tagName};
                        }
                    }
                    return {success: false};
                """)
                if js_result and js_result.get('success'):
                    print(f"   ✅ 已选择'投放广告赚收益' (JS方法, 标签: {js_result.get('tag')})")
                    ad_selected = True
            
            if not ad_selected:
                print("   ⚠️ 未找到'投放广告赚收益'选项，可能默认已选中")
        except Exception as e:
            print(f"   ⚠️ 选择广告收益异常: {e}")
        
        time.sleep(2)
        
        # 第一步：点击"预览并发布"按钮
        print("\n--- 第1步：点击'预览并发布' ---")
        
        from selenium.webdriver.common.action_chains import ActionChains
        
        # 找到红色按钮
        red_btn = None
        all_btns = driver.find_elements(By.TAG_NAME, 'button')
        for btn in all_btns:
            try:
                text = btn.text.strip()
                if '预览并发布' in text and btn.is_displayed():
                    red_btn = btn
                    break
            except:
                continue
        
        if red_btn:
            # 滚动到按钮可见
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", red_btn)
            time.sleep(1)
            
            # 使用Selenium原生click
            print("   🖱️ 使用Selenium原生click...")
            try:
                red_btn.click()
                print(f"   ✅ Selenium click成功")
            except Exception as e:
                print(f"   ⚠️ Selenium click失败: {e}")
                # 备用: ActionChains
                actions = ActionChains(driver)
                actions.move_to_element(red_btn).click().perform()
                print(f"   ✅ ActionChains click成功")
        else:
            print("   ❌ 未找到'预览并发布'按钮")
            return {'success': False, 'message': '未找到发布按钮'}
        
        # 等待预览弹窗加载 - 增加等待时间
        print("   ⏳ 等待预览弹窗加载...")
        time.sleep(5)
        
        # 检查预览弹窗是否出现
        preview_appeared = False
        for i in range(10):  # 最多等10秒
            # 检查是否有"确认发布"按钮出现
            elements = driver.find_elements(By.XPATH, '//*[contains(text(),"确认发布")]')
            if elements:
                for el in elements:
                    if el.is_displayed():
                        print(f"   ✅ 检测到'确认发布'按钮出现 (等待{i}秒)")
                        preview_appeared = True
                        break
            if preview_appeared:
                break
            time.sleep(1)
        
        if not preview_appeared:
            print("   ⚠️ 预览弹窗可能未出现，尝试直接点击'发布文章'按钮...")
            # 尝试直接点击发布按钮
            try:
                publish_btns = driver.find_elements(By.XPATH, '//button[contains(text(),"发布文章")]')
                if publish_btns:
                    for btn in publish_btns:
                        if btn.is_displayed():
                            print("   🖱️ 点击'发布文章'按钮...")
                            driver.execute_script("arguments[0].click();", btn)
                            time.sleep(3)
                            # 检查是否有确认弹窗
                            confirm_elements = driver.find_elements(By.XPATH, '//*[contains(text(),"确认发布")]')
                            if confirm_elements:
                                for ce in confirm_elements:
                                    if ce.is_displayed():
                                        print("   ✅ 确认弹窗出现，点击'确认发布'")
                                        driver.execute_script("arguments[0].click();", ce)
                                        time.sleep(3)
                                        break
                            break
            except Exception as e:
                print(f"   ⚠️ 点击发布按钮失败: {e}")
        
        # 保存截图
        driver.save_screenshot(os.path.join(PICTURE_DIR, "article_v2_preview.png"))
        print("📸 已保存预览界面截图")
        
        # 第二步：在预览弹窗中找到并点击"确认发布"
        print("\n--- 第2步：查找预览弹窗中的'确认发布'按钮 ---")
        
        # 预览弹窗是一个居中的模态框，底部有"返回编辑"和"确认发布"两个按钮
        confirm_btn = None
        
        # 方法1：直接用JavaScript查找并点击"确认发布"按钮
        print("   🔍 用JS查找'确认发布'按钮...")
        js_result = driver.execute_script("""
            // 查找所有按钮和可点击元素
            var allElements = document.querySelectorAll('button, [role="button"], a, span, div');
            var results = [];
            
            for (var i = 0; i < allElements.length; i++) {
                var el = allElements[i];
                var text = el.innerText ? el.innerText.trim() : '';
                var rect = el.getBoundingClientRect();
                
                // 查找"确认发布"文字
                if (text === '确认发布' && rect.width > 0 && rect.height > 0) {
                    results.push({
                        tag: el.tagName,
                        text: text,
                        x: rect.x,
                        y: rect.y,
                        width: rect.width,
                        height: rect.height
                    });
                    
                    // 尝试点击
                    el.click();
                    return {found: true, text: text, clicked: true};
                }
            }
            
            // 如果没找到精确匹配，查找包含"确认"的红色按钮
            var buttons = document.querySelectorAll('button');
            for (var i = 0; i < buttons.length; i++) {
                var btn = buttons[i];
                var text = btn.innerText ? btn.innerText.trim() : '';
                var styles = window.getComputedStyle(btn);
                var bgColor = styles.backgroundColor;
                var rect = btn.getBoundingClientRect();
                
                // 红色按钮且包含"确认"
                if (text.includes('确认') && bgColor.includes('255') && rect.width > 0) {
                    btn.click();
                    return {found: true, text: text, clicked: true, method: 'red_btn'};
                }
            }
            
            return {found: false, allButtons: results};
        """)
        
        if js_result.get('found'):
            print(f"   ✅ JS找到并点击: '{js_result.get('text')}'")
            confirm_btn = True
            time.sleep(5)
        else:
            print(f"   ⚠️ JS未找到'确认发布'按钮")
        
        # 方法2：如果JS没找到，尝试用Selenium按钮遍历
        if not confirm_btn:
            print("   🔄 Selenium遍历所有按钮...")
            all_btns = driver.find_elements(By.TAG_NAME, 'button')
            print(f"   🔍 共找到 {len(all_btns)} 个按钮")
            
            for btn in all_btns:
                try:
                    text = btn.text.strip()
                    if '确认发布' in text:
                        if btn.is_displayed():
                            driver.execute_script("arguments[0].click();", btn)
                            print(f"   ✅ Selenium点击: '{text}'")
                            confirm_btn = btn
                            time.sleep(5)
                            break
                except:
                    continue
        
        # 方法3：如果还没找到，等待更长时间再试
        if not confirm_btn:
            print("   🔄 等待3秒后再次尝试...")
            time.sleep(3)
            
            # 再次用JS查找
            js_result2 = driver.execute_script("""
                var elements = document.querySelectorAll('*');
                for (var i = 0; i < elements.length; i++) {
                    var el = elements[i];
                    var text = el.innerText ? el.innerText.trim() : '';
                    if (text === '确认发布') {
                        el.click();
                        return {found: true, text: text};
                    }
                }
                return {found: false};
            """)
            
            if js_result2.get('found'):
                print(f"   ✅ 第二次尝试成功: '{js_result2.get('text')}'")
                confirm_btn = True
                time.sleep(5)
        
        if not confirm_btn:
            print("   ⚠️ 未能找到'确认发布'按钮")
            # 打印页面上所有包含"发布"的元素
            debug_info = driver.execute_script("""
                var elements = document.querySelectorAll('*');
                var results = [];
                for (var i = 0; i < elements.length; i++) {
                    var el = elements[i];
                    var text = el.innerText ? el.innerText.trim() : '';
                    if (text.includes('发布') && text.length < 20) {
                        var rect = el.getBoundingClientRect();
                        results.push({
                            tag: el.tagName,
                            text: text,
                            visible: rect.width > 0 && rect.height > 0
                        });
                    }
                }
                return results.slice(0, 15);  // 只返回前15个
            """)
            print("   📋 包含'发布'的元素:")
            for info in debug_info:
                print(f"      - {info['tag']}: '{info['text']}' visible={info['visible']}")
        
        # 等待发布完成
        time.sleep(5)
        
        # 保存发布后截图
        driver.save_screenshot(os.path.join(PICTURE_DIR, "article_v2_after.png"))
        print("📸 已保存发布后截图")
        
        # 检查URL是否变化（发布成功通常会跳转）
        current_url = driver.current_url
        print(f"   📍 当前URL: {current_url}")
        
        if 'publish' not in current_url or 'success' in current_url:
            return {'success': True, 'message': '文章发布成功'}
        else:
            return {'success': True, 'message': '文章已提交，请手动确认发布状态'}
    
    finally:
        driver.quit()
        print("\n🔒 浏览器已关闭")


def main():
    parser = argparse.ArgumentParser(description='发布今日头条【文章】v2')
    parser.add_argument('--title', '-t', required=True, help='文章标题')
    parser.add_argument('--content', '-c', help='文章内容')
    parser.add_argument('--file', '-f', help='从文件读取内容')
    parser.add_argument('--cover', help='本地封面图片路径')
    parser.add_argument('--cover-prompt', help='用即梦AI生成封面的提示词')
    parser.add_argument('--insert-cover', action='store_true', help='将封面图片也插入正文中')
    
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
    
    # 获取封面（可选）
    cover_path = None
    if args.cover:
        # 使用本地封面
        if os.path.exists(args.cover):
            cover_path = args.cover
            print(f"\n🖼️ 使用本地封面: {cover_path}")
        else:
            print(f"\n⚠️ 封面文件不存在: {args.cover}")
    elif args.cover_prompt:
        # 使用即梦AI生成封面
        print(f"\n🎨 使用即梦AI生成封面...")
        with open(JIMENG_CONFIG, 'r') as f:
            jimeng_config = json.load(f)
        client = JimengImageClient(jimeng_config['access_key_id'], jimeng_config['secret_access_key'])
        image_url = client.generate_image(args.cover_prompt, "16:9")
        if image_url:
            cover_path = download_image(image_url, PICTURE_DIR)
    
    # 准备正文插图
    content_images = []
    if args.insert_cover and cover_path:
        content_images.append(cover_path)
    
    # 发布
    result = publish_article(args.title, content, cover_path, content_images)
    
    if result['success']:
        print(f"\n🎉 {result['message']}")
    else:
        print(f"\n❌ {result['message']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
