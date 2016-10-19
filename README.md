# Profcom
用python 2.7写的深圳大学网络认证客户端 
##项目依赖
如果你需要兼容Windows 7以后版本，请在Windows 7 32bit 下工作。
使用32位的python，下面库也安装32位。
 - requests
 - pycrypto
 - pywin32
 
requests 安装方法 ` pip install requests`

pycrypto [下载地址][1]

pywin32 [下载地址][2]

##用于其他学校
如果学校支持web登录认证，都可以基于本项目修改
 1. 修改loginLogoutUtil.py里面的登录注销方法，使用requests模拟登录，请自行测试。
 2. 更换图片（请保持图片大小一致，至少宽度应该一样，否则界面布局会错乱），修改button颜色。
 
tips:Windows icon需要多尺寸合成，否则某些情况下，会无法显示。

##打包成exe？
如果你需要兼容Windows 7以后版本，请在Windows 7 32bit 下打包。

打包需要安装Pyinstaller模块。pyinstaller [下载地址][3]，建议使用3.1.1版本，解压缩，进入目录，使用命令`python setup.py install`即可安装。打包时注意文件的路径。

tips:使用批处理会更加方便。

进入项目目录，打开命令提示符窗口，输入以下命令。

    pyinstaller --upx-dir=upxdir -F -w --hidden-import=queue -i resources\favicon.ico profcom.py
    pyinstaller --upx-dir=upxdir -F -w --hidden-import=queue -i resources\favicon.ico main.py

|参数|说明|
|-----|------|
|--upx-dir|upx压缩的目录|
|-F |打包成一个文件|
|-w |没有控制台窗口|
|-c|控制台窗口（调试的时候可以打开）|
|--hidden-import | pyinstaller打包Queue模块有点问题（hack手段）|
|-i | 打包后文件图标|
更多使用方法请使用`pyinstaller -h`命令

##制作windows安装程序？
推荐使用inno setup，制作比较简单，按照向导多试几次，就能达到差强人意的效果。当然，阅读inno setup的文档会更好。


  [1]: http://www.voidspace.org.uk/python/pycrypto-2.6.1/
  [2]: https://sourceforge.net/projects/pywin32/files/pywin32/Build%20220/
  [3]: https://github.com/pyinstaller/pyinstaller/releases
