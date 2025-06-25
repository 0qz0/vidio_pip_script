# 视频画中画(PiP)自动化脚本

这个脚本可以自动为视频网站的视频启用画中画(Picture-in-Picture)功能，让视频以浮动窗口的形式显示在屏幕上。

## 功能特点

- 🎥 支持主流视频网站（YouTube、Bilibili、优酷、爱奇艺等）
- 🤖 自动化操作，无需手动点击
- 🔧 智能检测网站类型，适配不同平台
- 📱 支持Chrome浏览器的画中画功能
- 🚀 简单易用，一键启用

## 安装要求

### 1. Python环境
- Python 3.7 或更高版本

### 2. Chrome浏览器
- 确保已安装Chrome浏览器
- 建议使用最新版本

### 3. ChromeDriver
- 下载与Chrome版本匹配的ChromeDriver
- 将ChromeDriver放在系统PATH中，或与脚本同目录

## 安装步骤

1. **克隆或下载脚本文件**
   ```bash
   # 确保在项目目录中
   ```

2. **安装Python依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **验证安装**
   ```bash
   python -c "import selenium; print('Selenium安装成功')"
   ```

## 使用方法

### 方法一：使用完整版脚本（推荐）

```bash
# 基本用法
python video_pip_script.py "https://www.youtube.com/watch?v=VIDEO_ID"

# 使用无头模式（不显示浏览器窗口）
python video_pip_script.py "https://www.bilibili.com/video/BV..." --headless

# 自定义等待时间
python video_pip_script.py "https://v.youku.com/v_show/id_..." --wait 10
```

### 方法二：使用简化版脚本

```bash
python simple_pip.py
```
然后按提示输入视频URL。

### 方法三：在Python代码中使用

```python
from video_pip_script import VideoPiPScript

# 创建脚本实例
script = VideoPiPScript()

# 启用画中画
script.setup_driver()
success = script.enable_pip("https://www.youtube.com/watch?v=VIDEO_ID")

if success:
    print("画中画启用成功！")
else:
    print("画中画启用失败")

# 关闭浏览器
script.close()
```

## 支持的网站

| 网站 | 支持状态 | 备注 |
|------|----------|------|
| YouTube | ✅ 完全支持 | 自动检测，支持画中画按钮 |
| Bilibili | ✅ 完全支持 | 自动检测，支持画中画按钮 |
| 优酷 | ✅ 完全支持 | 自动检测，支持画中画按钮 |
| 爱奇艺 | ✅ 完全支持 | 自动检测，支持画中画按钮 |
| 其他视频网站 | ⚠️ 部分支持 | 使用通用方法，可能需手动操作 |

## 常见问题

### Q: 脚本运行后没有启用画中画？
A: 请检查：
1. 浏览器是否支持画中画功能（Chrome 69+）
2. 视频是否已开始播放
3. 网站是否允许画中画功能

### Q: 出现"ChromeDriver not found"错误？
A: 请确保：
1. 已下载ChromeDriver
2. ChromeDriver版本与Chrome浏览器版本匹配
3. ChromeDriver在系统PATH中

### Q: 视频无法自动播放？
A: 某些网站需要用户交互才能播放视频，脚本会尝试自动播放，如果失败可能需要手动点击播放按钮。

### Q: 画中画窗口无法移动？
A: 画中画窗口可以通过鼠标拖拽移动，这是浏览器的标准功能。

## 技术原理

脚本使用Selenium WebDriver自动化浏览器操作：

1. **网站检测**: 根据URL自动识别网站类型
2. **视频定位**: 查找页面中的video元素
3. **自动播放**: 通过JavaScript或点击播放按钮启动视频
4. **画中画启用**: 使用`requestPictureInPicture()`API或点击画中画按钮

## 注意事项

- ⚠️ 请遵守网站的使用条款
- ⚠️ 不要用于商业用途
- ⚠️ 某些网站可能有反爬虫机制
- ⚠️ 建议在个人学习研究中使用

## 更新日志

### v1.0.0
- 初始版本
- 支持主流视频网站
- 自动化画中画功能

## 许可证

本项目仅供学习和研究使用。

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！ 