#For Xcode package automatically

源自网上的一份代码，稍作修改以供使用

此自动打包脚本运行在 [Python3](https://www.python.org/downloads/) 环境下, 依赖 [requests](https://pypi.org/project/requests/#files) 库


环境配置
=====

检查是否安装`Python3`
打开终端, 执行以下命令
```Bash
python3 --version
```
显示 `Python 3.x.x` 即 `Python3` 环境已配置

如果未安装`Python3` 推荐使用 [Homebrew](https://brew.sh/) 安装

* 检查是否安装`Homebrew`
执行以下命令
```Bash
brew --version
```
* 如果未安装`Homebrew`
执行以下命令
```Bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
* 安装完成后, 执行以下命令安装`Python3`
```Bash
brew install python3
```
* 然后安装`requests`

```Bash
pip3 install requests
```

****** 即将完成 ******

到这里基本上就大功告成了, 然鹅还差一小步. 请继续往下看

* 对`Xcode`的配置

打开Xcode->Preferences->Locations->Command Line Tools, 如果为空进行勾选.

* 若使用 `xc_build_automatically.py` 需要用到 `PackageApplication` 工具. 
[下载地址](https://pan.baidu.com/s/1Z0TAsivmt4vE2bHUx_sviA) 密码: `47pj`.  下载完成解压后拷贝至
```Bash
/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/usr/bin/
```
然后执行以下命令
```Bash
chmod +x /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/usr/bin/PackageApplication
```

此工具在 Xcode 8.3 之后被废弃, 使用`xcodebuild -exportArchive` 替代, `xc_archive_automatically.py` 不依赖 `PackageApplication`工具.

* 若使用自动上传至[蒲公英平台](https://www.pgyer.com/). 请打开 `xc_build_automatically.py` 及`xc_archive_automatically.py` 将
```python
API_KEY = 'xxxxxx' #replace with your pgyer apikey
```
修改为你的apikey即可(apikey查看方法：蒲公英->账户设置->API信息)

使用方法
=====

此脚本默认上传至[蒲公英平台](https://www.pgyer.com/), 默认开启自动上传(若不需要上传则在命令后追加 `-m` 即可).

打开终端, cd至该脚本所在目录. 然后执行以下命令即可
```Bash
python3 xc_build_automatically.py -p yourproj.xcodeproj -n yourproj -c Debug
```
或
```Bash
python3 xc_archive_automatically.py -p yourproj.xcodeproj -n yourproj -c Debug
```
导出的文件默认存放在桌面的 `XcodeAPP` 目录下 

* 参数说明

-p proj路径<br>
-w workspace路径<br>
-n target/scheme 一般为工程名<br>
-c Debug/Release 默认为Debug<br>
-o 导出路径 默认为桌面 XcodeAPP 目录<br>
-m 只导出ipa不上传<br>

到这里就结束了, 试一试吧.


