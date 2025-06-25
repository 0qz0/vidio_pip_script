#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版视频画中画脚本
快速启用视频的画中画功能
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def enable_pip(url):
    """
    启用视频画中画功能
    
    Args:
        url (str): 视频页面URL
    """
    # 设置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument('--enable-features=PictureInPicture')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    driver = None
    try:
        print(f"正在打开: {url}")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        
        # 等待视频加载
        print("等待视频加载...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "video"))
        )
        
        # 查找视频元素
        video = driver.find_element(By.TAG_NAME, "video")
        
        # 播放视频
        print("播放视频...")
        driver.execute_script("arguments[0].play();", video)
        time.sleep(2)
        
        # 启用画中画
        print("启用画中画...")
        driver.execute_script("""
            const video = arguments[0];
            if (video.readyState >= 2) {
                video.requestPictureInPicture();
            }
        """, video)
        
        print("✅ 画中画功能已启用！")
        print("视频现在应该以画中画形式显示在屏幕上。")
        print("按 Ctrl+C 退出程序...")
        
        # 保持程序运行
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n程序已退出")
    except Exception as e:
        print(f"❌ 错误: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    # 获取用户输入的视频URL
    url = input("请输入视频页面URL: ").strip()
    if url:
        enable_pip(url)
    else:
        print("请输入有效的URL") 