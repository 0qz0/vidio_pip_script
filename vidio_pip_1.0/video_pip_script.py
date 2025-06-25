#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频画中画(PiP)自动化脚本
支持主流视频网站的画中画功能
"""

import time
import json
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VideoPiPScript:
    def __init__(self, headless=False):
        """
        初始化视频画中画脚本
        
        Args:
            headless (bool): 是否使用无头模式
        """
        self.driver = None
        self.headless = headless
        self.video_selectors = {
            'youtube': {
                'video': 'video',
                'pip_button': 'button[aria-label*="画中画"], button[aria-label*="Picture in picture"]',
                'play_button': 'button[aria-label*="播放"], button[aria-label*="Play"]'
            },
            'bilibili': {
                'video': 'video',
                'pip_button': '.bpx-player-ctrl-pip, .bpx-player-ctrl-pip-btn',
                'play_button': '.bpx-player-ctrl-play'
            },
            'youku': {
                'video': 'video',
                'pip_button': '.control-pip, .pip-btn',
                'play_button': '.control-play'
            },
            'iqiyi': {
                'video': 'video',
                'pip_button': '.iqp-pip-btn, .pip-button',
                'play_button': '.iqp-play-btn'
            },
            'general': {
                'video': 'video',
                'pip_button': '[aria-label*="画中画"], [aria-label*="Picture in picture"], .pip-btn, .pip-button',
                'play_button': '[aria-label*="播放"], [aria-label*="Play"], .play-btn, .play-button'
            }
        }
    
    def setup_driver(self):
        """设置Chrome浏览器驱动"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless')
        
        # 添加必要的参数
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # 启用画中画功能
        chrome_options.add_argument('--enable-features=PictureInPicture')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            logger.info("浏览器驱动初始化成功")
        except Exception as e:
            logger.error(f"浏览器驱动初始化失败: {e}")
            raise
    
    def detect_website(self, url):
        """检测网站类型"""
        if 'youtube.com' in url or 'youtu.be' in url:
            return 'youtube'
        elif 'bilibili.com' in url:
            return 'bilibili'
        elif 'youku.com' in url:
            return 'youku'
        elif 'iqiyi.com' in url:
            return 'iqiyi'
        else:
            return 'general'
    
    def wait_for_video(self, timeout=10):
        """等待视频元素加载"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "video"))
            )
            logger.info("视频元素加载完成")
            return True
        except TimeoutException:
            logger.warning("视频元素加载超时")
            return False
    
    def find_video_element(self):
        """查找视频元素"""
        try:
            video = self.driver.find_element(By.TAG_NAME, "video")
            logger.info("找到视频元素")
            return video
        except NoSuchElementException:
            logger.error("未找到视频元素")
            return None
    
    def enable_pip_via_javascript(self, video_element):
        """通过JavaScript启用画中画"""
        try:
            # 检查浏览器是否支持画中画
            pip_supported = self.driver.execute_script("""
                return document.pictureInPictureEnabled || 
                       'pictureInPictureEnabled' in document;
            """)
            
            if not pip_supported:
                logger.warning("浏览器不支持画中画功能")
                return False
            
            # 尝试启用画中画
            result = self.driver.execute_script("""
                const video = arguments[0];
                if (video.readyState >= 2) {  // HAVE_CURRENT_DATA
                    return video.requestPictureInPicture();
                } else {
                    return Promise.reject('视频未准备好');
                }
            """, video_element)
            
            logger.info("画中画功能已启用")
            return True
            
        except Exception as e:
            logger.error(f"启用画中画失败: {e}")
            return False
    
    def click_pip_button(self, website_type):
        """点击画中画按钮"""
        selectors = self.video_selectors[website_type]
        pip_button_selector = selectors['pip_button']
        
        try:
            # 等待画中画按钮出现
            pip_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, pip_button_selector))
            )
            
            # 点击画中画按钮
            pip_button.click()
            logger.info("画中画按钮点击成功")
            return True
            
        except TimeoutException:
            logger.warning("画中画按钮未找到或不可点击")
            return False
        except Exception as e:
            logger.error(f"点击画中画按钮失败: {e}")
            return False
    
    def play_video(self, website_type):
        """播放视频"""
        selectors = self.video_selectors[website_type]
        play_button_selector = selectors['play_button']
        
        try:
            # 查找播放按钮
            play_button = self.driver.find_element(By.CSS_SELECTOR, play_button_selector)
            play_button.click()
            logger.info("视频播放成功")
            return True
        except NoSuchElementException:
            logger.warning("未找到播放按钮，尝试JavaScript播放")
            return self.play_video_via_javascript()
        except Exception as e:
            logger.error(f"播放视频失败: {e}")
            return False
    
    def play_video_via_javascript(self):
        """通过JavaScript播放视频"""
        try:
            video = self.find_video_element()
            if video:
                self.driver.execute_script("arguments[0].play();", video)
                logger.info("通过JavaScript播放视频成功")
                return True
            return False
        except Exception as e:
            logger.error(f"JavaScript播放失败: {e}")
            return False
    
    def enable_pip(self, url, wait_time=5):
        """
        启用视频画中画功能
        
        Args:
            url (str): 视频页面URL
            wait_time (int): 等待视频加载的时间(秒)
        """
        try:
            logger.info(f"正在访问: {url}")
            self.driver.get(url)
            
            # 检测网站类型
            website_type = self.detect_website(url)
            logger.info(f"检测到网站类型: {website_type}")
            
            # 等待视频加载
            if not self.wait_for_video(wait_time):
                logger.error("视频加载失败")
                return False
            
            # 播放视频
            self.play_video(website_type)
            time.sleep(2)  # 等待视频开始播放
            
            # 查找视频元素
            video_element = self.find_video_element()
            if not video_element:
                return False
            
            # 尝试通过JavaScript启用画中画
            if self.enable_pip_via_javascript(video_element):
                return True
            
            # 如果JavaScript方法失败，尝试点击画中画按钮
            logger.info("尝试点击画中画按钮")
            return self.click_pip_button(website_type)
            
        except Exception as e:
            logger.error(f"启用画中画过程中发生错误: {e}")
            return False
    
    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            logger.info("浏览器已关闭")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='视频画中画自动化脚本')
    parser.add_argument('url', help='视频页面URL')
    parser.add_argument('--headless', action='store_true', help='使用无头模式')
    parser.add_argument('--wait', type=int, default=5, help='等待视频加载的时间(秒)')
    
    args = parser.parse_args()
    
    script = VideoPiPScript(headless=args.headless)
    
    try:
        script.setup_driver()
        success = script.enable_pip(args.url, args.wait)
        
        if success:
            logger.info("画中画功能启用成功！")
            print("\n✅ 画中画功能已启用！")
            print("视频现在应该以画中画形式显示在屏幕上。")
            print("按 Ctrl+C 退出程序...")
            
            # 保持程序运行
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n程序已退出")
        else:
            logger.error("画中画功能启用失败")
            print("\n❌ 画中画功能启用失败")
            print("请检查:")
            print("1. 视频页面是否正确加载")
            print("2. 浏览器是否支持画中画功能")
            print("3. 视频是否已开始播放")
    
    except Exception as e:
        logger.error(f"程序执行失败: {e}")
        print(f"\n❌ 程序执行失败: {e}")
    
    finally:
        script.close()

if __name__ == "__main__":
    main() 