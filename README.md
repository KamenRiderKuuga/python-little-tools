## python-little-tools

### 描述

这里放置了一些日常用Python写的小东西，作为个人备忘以及分享

#### 1. 通过字符串获取Cookie

这个主要用于平时在写爬虫时，从浏览器或者抓包软件上面复制的Cookie字符串，要转成字典的形式，没什么技术含量，放在这里方便随时取用

#### 2. 用selenium实现的简单野菜部落签到

一个休闲游戏的官网签到，包含了使用selenium进行浏览器操作的最简单的过程
[chromedriver下载地址](https://chromedriver.chromium.org/downloads)，请根据自己电脑上安装的Chrome版本来进行下载，使用时把chormedriver放在python解释器目录或者当前代码文件目录即可，安装selenium用*pip install selenium*

#### 3.异步爬取福利漫画-平行天堂

用爬虫爬取了一部漫画的全集，这里获取漫画详情页的Cookie需要手动调整

#### 4.Python+adb+OpenCV实现控制安卓手机答题脚本

利用adb向安卓手机发送截图指令并pull到PC上，再使用OpenCV对题目进行截图分析并模拟点击手机屏幕

adb下载地址：https://developer.android.com/studio/releases/platform-tools

#### 5.基于mitmproxy抓包工具，通过Python脚本对抓到的内容进行处理

代码很短，这里主要是想记录这个可行的方法，以及[mitmproxy](https://github.com/mitmproxy/mitmproxy)安装和使用的注意事项

安装时使用*pip install mitmproxy*即可，使用时，将脚本文件放在其安装目录下，使用*mitmdump -q -s 处理mitmproxy抓包信息.py*开始抓包，这里的*-q*表示只显示脚本中输入到console的内容，过滤掉其它所有的显示内容，*-s*用来指定要执行的脚本，这里的*mitmdump*也可以换做*mitmweb*，可以提供更容易观察抓包内容的可视化界面，但是长期运行会占用大量内存，抓取手机端*https*数据包时需要在手机端安装证书以及设置代理地址，过程很简单，网上有比较详细的教程



### License 许可证

python-little-tools is licensed under [MIT](https://github.com/xukimseven/HardCandy-Jekyll/blob/master/LICENSE).