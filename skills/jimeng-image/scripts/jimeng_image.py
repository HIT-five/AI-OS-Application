#!/usr/bin/env python3
"""
即梦AI 图片生成 API 客户端
基于火山引擎视觉服务

功能：使用即梦AI生成高质量图片
"""

import json
import hashlib
import hmac
import time
import requests
import base64
import os
from pathlib import Path


class JimengImageClient:
    """即梦AI图片生成客户端"""
    
    def __init__(self, access_key_id: str, secret_access_key: str):
        """
        初始化客户端
        
        Args:
            access_key_id: 火山引擎 AccessKeyId
            secret_access_key: 火山引擎 SecretAccessKey
        """
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.base_url = "https://visual.volcengineapi.com"
        self.host = "visual.volcengineapi.com"
        self.region = "cn-north-1"
        self.service = "cv"
    
    def _sign_v4(self, method: str, canonical_uri: str, canonical_querystring: str, 
                 payload: str, content_hash: str) -> tuple:
        """
        火山引擎签名 v4
        
        Returns:
            (headers, request_url)
        """
        timestamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
        datestamp = timestamp[:8]
        
        # Signed headers
        signed_headers = "content-type;host;x-content-sha256;x-date"
        
        # Canonical headers
        canonical_headers = (
            f"content-type:application/json\n"
            f"host:{self.host}\n"
            f"x-content-sha256:{content_hash}\n"
            f"x-date:{timestamp}\n"
        )
        
        # Canonical request
        canonical_request = "\n".join([
            method,
            canonical_uri,
            canonical_querystring,
            canonical_headers,
            signed_headers,
            content_hash
        ])
        
        # String to sign
        algorithm = "HMAC-SHA256"
        credential_scope = f"{datestamp}/{self.region}/{self.service}/request"
        string_to_sign = "\n".join([
            algorithm,
            timestamp,
            credential_scope,
            hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
        ])
        
        # Signing key
        k_date = hmac.new(
            self.secret_access_key.encode("utf-8"),
            datestamp.encode("utf-8"),
            hashlib.sha256
        ).digest()
        k_region = hmac.new(k_date, self.region.encode("utf-8"), hashlib.sha256).digest()
        k_service = hmac.new(k_region, self.service.encode("utf-8"), hashlib.sha256).digest()
        k_signing = hmac.new(k_service, b"request", hashlib.sha256).digest()
        
        # Signature
        signature = hmac.new(
            k_signing,
            string_to_sign.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        
        # Authorization header
        authorization = (
            f"{algorithm} Credential={self.access_key_id}/{credential_scope}, "
            f"SignedHeaders={signed_headers}, Signature={signature}"
        )
        
        headers = {
            "X-Date": timestamp,
            "Authorization": authorization,
            "X-Content-Sha256": content_hash,
            "Content-Type": "application/json"
        }
        
        request_url = f"{self.base_url}?{canonical_querystring}"
        
        return headers, request_url
    
    def _api_request(self, action: str, req_json: dict) -> dict:
        """发送API请求"""
        body = json.dumps(req_json)
        content_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()
        canonical_querystring = f"Action={action}&Version=2022-08-31"
        
        headers, request_url = self._sign_v4(
            "POST", "/", canonical_querystring, body, content_hash
        )
        
        try:
            response = requests.post(
                request_url,
                headers=headers,
                data=body,
                timeout=60
            )
            return response.json()
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def submit_task(self, prompt: str, ratio: str = "1:1") -> dict:
        """
        提交图片生成任务
        
        Args:
            prompt: 图片描述提示词
            ratio: 图片比例，支持 "1:1", "4:3", "3:4", "16:9", "9:16"
            
        Returns:
            API响应结果，包含 task_id
        """
        # 图片比例映射 (使用1024基准)
        ratio_map = {
            "1:1": {"width": 1024, "height": 1024},
            "4:3": {"width": 1024, "height": 768},
            "3:4": {"width": 768, "height": 1024},
            "16:9": {"width": 1024, "height": 576},
            "9:16": {"width": 576, "height": 1024}
        }
        
        if ratio not in ratio_map:
            return {"error": f"不支持的图片比例 {ratio}，支持: 1:1, 4:3, 3:4, 16:9, 9:16"}
        
        size = ratio_map[ratio]
        
        req_json = {
            "req_key": "jimeng_t2i_v40",
            "prompt": prompt,
            "return_url": True,
            "width": size["width"],
            "height": size["height"]
        }
        
        return self._api_request("CVSync2AsyncSubmitTask", req_json)
    
    def get_result(self, task_id: str) -> dict:
        """
        查询任务结果
        
        Args:
            task_id: 任务ID
            
        Returns:
            API响应结果，包含图片数据
        """
        req_json = {
            "req_key": "jimeng_t2i_v40",
            "task_id": task_id
        }
        
        return self._api_request("CVSync2AsyncGetResult", req_json)
    
    def generate_image(self, prompt: str, ratio: str = "1:1", 
                       output_path: str = None, max_wait: int = 120) -> dict:
        """
        生成图片（完整流程：提交 + 轮询 + 保存）
        
        Args:
            prompt: 图片描述提示词
            ratio: 图片比例
            output_path: 输出文件路径（可选）
            max_wait: 最大等待时间（秒）
            
        Returns:
            包含图片路径或错误信息的字典
        """
        # 1. 提交任务
        submit_result = self.submit_task(prompt, ratio)
        
        if submit_result.get("code") != 10000:
            return {"success": False, "error": submit_result.get("message", "提交失败")}
        
        task_id = submit_result.get("data", {}).get("task_id")
        if not task_id:
            return {"success": False, "error": "未获取到task_id"}
        
        print(f"📋 任务已提交，task_id: {task_id}")
        
        # 2. 轮询等待结果
        start_time = time.time()
        while time.time() - start_time < max_wait:
            time.sleep(5)  # 每5秒查询一次
            
            result = self.get_result(task_id)
            
            if result.get("code") == 10000:
                data = result.get("data", {})
                status = data.get("status")
                
                if status == "done":
                    # 获取图片数据
                    b64_list = data.get("binary_data_base64", [])
                    url_list = data.get("image_urls", [])
                    
                    if b64_list and b64_list[0]:
                        # Base64 解码保存
                        img_data = base64.b64decode(b64_list[0])
                        
                        if output_path:
                            save_path = output_path
                        else:
                            save_path = f"/home/yqj/picture/jimeng_{task_id}.png"
                        
                        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
                        with open(save_path, "wb") as f:
                            f.write(img_data)
                        
                        print(f"✅ 图片已保存: {save_path}")
                        return {
                            "success": True,
                            "path": save_path,
                            "task_id": task_id
                        }
                    
                    elif url_list and url_list[0]:
                        # 下载URL
                        img_url = url_list[0]
                        if output_path:
                            save_path = output_path
                        else:
                            save_path = f"/home/yqj/picture/jimeng_{task_id}.png"
                        
                        img_resp = requests.get(img_url, timeout=30)
                        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
                        with open(save_path, "wb") as f:
                            f.write(img_resp.content)
                        
                        print(f"✅ 图片已保存: {save_path}")
                        return {
                            "success": True,
                            "path": save_path,
                            "url": img_url,
                            "task_id": task_id
                        }
                    
                    return {"success": False, "error": "任务完成但无图片数据"}
                
                elif status == "failed":
                    return {"success": False, "error": "图片生成失败"}
                
                else:
                    print(f"⏳ 生成中... ({int(time.time() - start_time)}s)")
            
            elif result.get("code") == 50501:
                # 内部错误，可能是参数问题
                return {"success": False, "error": result.get("message", "内部错误")}
        
        return {"success": False, "error": f"超时（{max_wait}秒）"}


def main():
    """命令行工具"""
    import argparse
    import sys
    
    # 获取脚本所在目录
    script_dir = Path(__file__).parent.absolute()
    config_path = script_dir / "config.json"
    
    # 加载配置
    config = {}
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        pass
    
    parser = argparse.ArgumentParser(description="即梦AI图片生成")
    parser.add_argument("--prompt", "-p", help="图片描述提示词")
    parser.add_argument("--ratio", "-r", default="1:1", 
                       choices=["1:1", "4:3", "3:4", "16:9", "9:16"],
                       help="图片比例 (默认: 1:1)")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument("--key-id", "-k", default=config.get("access_key_id"), help="AccessKeyId")
    parser.add_argument("--secret", "-s", default=config.get("secret_access_key"), help="SecretAccessKey")
    parser.add_argument("--timeout", "-t", type=int, default=120, help="最大等待时间（秒）")
    
    args = parser.parse_args()
    
    if not args.key_id or not args.secret:
        print("❌ 缺少凭证")
        print(f"请在 {config_path} 中配置或使用 --key-id --secret 参数")
        sys.exit(1)
    
    if not args.prompt:
        print("❌ 请提供 --prompt 参数")
        sys.exit(1)
    
    client = JimengImageClient(args.key_id, args.secret)
    
    print(f"🎨 开始生成图片...")
    print(f"📝 描述: {args.prompt}")
    print(f"📐 比例: {args.ratio}")
    
    result = client.generate_image(
        args.prompt, 
        args.ratio, 
        args.output,
        args.timeout
    )
    
    if result.get("success"):
        print(f"\n🎉 生成成功!")
        print(f"📁 文件: {result.get('path')}")
    else:
        print(f"\n❌ 生成失败: {result.get('error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
