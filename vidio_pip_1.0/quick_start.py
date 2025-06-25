#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速启动脚本 - 视频画中画功能
提供简单的图形化界面
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
from video_pip_script import VideoPiPScript

class PiPGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("视频画中画工具")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # 设置样式
        style = ttk.Style()
        style.theme_use('clam')
        
        self.script = None
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 标题
        title_label = ttk.Label(main_frame, text="🎥 视频画中画工具", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # URL输入
        ttk.Label(main_frame, text="视频URL:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=50)
        self.url_entry.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 选项框架
        options_frame = ttk.LabelFrame(main_frame, text="选项", padding="10")
        options_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # 无头模式选项
        self.headless_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="无头模式（不显示浏览器窗口）", 
                       variable=self.headless_var).grid(row=0, column=0, sticky=tk.W)
        
        # 等待时间
        ttk.Label(options_frame, text="等待时间（秒）:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.wait_var = tk.IntVar(value=5)
        wait_spinbox = ttk.Spinbox(options_frame, from_=1, to=30, textvariable=self.wait_var, width=10)
        wait_spinbox.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        # 开始按钮
        self.start_button = ttk.Button(button_frame, text="🚀 开始画中画", 
                                      command=self.start_pip, style="Accent.TButton")
        self.start_button.grid(row=0, column=0, padx=(0, 10))
        
        # 停止按钮
        self.stop_button = ttk.Button(button_frame, text="⏹️ 停止", 
                                     command=self.stop_pip, state="disabled")
        self.stop_button.grid(row=0, column=1)
        
        # 状态显示
        self.status_var = tk.StringVar(value="准备就绪")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                                font=("Arial", 10))
        status_label.grid(row=5, column=0, columnspan=2, pady=10)
        
        # 日志显示
        log_frame = ttk.LabelFrame(main_frame, text="日志", padding="10")
        log_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.log_text = tk.Text(log_frame, height=8, width=60, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 配置网格权重
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(6, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
    def log_message(self, message):
        """添加日志消息"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def start_pip(self):
        """开始画中画功能"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("错误", "请输入视频URL")
            return
            
        if not url.startswith(('http://', 'https://')):
            messagebox.showerror("错误", "请输入有效的URL（以http://或https://开头）")
            return
        
        # 禁用开始按钮，启用停止按钮
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        
        # 清空日志
        self.log_text.delete(1.0, tk.END)
        
        # 在新线程中运行画中画功能
        self.pip_thread = threading.Thread(target=self.run_pip, args=(url,))
        self.pip_thread.daemon = True
        self.pip_thread.start()
        
    def run_pip(self, url):
        """在新线程中运行画中画功能"""
        try:
            self.log_message("正在初始化浏览器...")
            self.status_var.set("正在初始化...")
            
            # 创建脚本实例
            self.script = VideoPiPScript(headless=self.headless_var.get())
            self.script.setup_driver()
            
            self.log_message(f"正在访问: {url}")
            self.status_var.set("正在访问网页...")
            
            # 启用画中画
            success = self.script.enable_pip(url, self.wait_var.get())
            
            if success:
                self.log_message("✅ 画中画功能启用成功！")
                self.status_var.set("画中画已启用")
                messagebox.showinfo("成功", "画中画功能已启用！\n视频现在应该以画中画形式显示在屏幕上。")
            else:
                self.log_message("❌ 画中画功能启用失败")
                self.status_var.set("启用失败")
                messagebox.showerror("失败", "画中画功能启用失败\n请检查URL和网络连接")
                
        except Exception as e:
            self.log_message(f"❌ 错误: {str(e)}")
            self.status_var.set("发生错误")
            messagebox.showerror("错误", f"程序执行失败:\n{str(e)}")
        finally:
            # 恢复按钮状态
            self.root.after(0, self.reset_buttons)
            
    def stop_pip(self):
        """停止画中画功能"""
        if self.script:
            self.script.close()
            self.script = None
            self.log_message("已停止画中画功能")
            self.status_var.set("已停止")
            
        self.reset_buttons()
        
    def reset_buttons(self):
        """重置按钮状态"""
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        
    def on_closing(self):
        """窗口关闭时的处理"""
        if self.script:
            self.script.close()
        self.root.destroy()

def main():
    """主函数"""
    root = tk.Tk()
    app = PiPGUI(root)
    
    # 设置窗口关闭事件
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # 启动GUI
    root.mainloop()

if __name__ == "__main__":
    main() 