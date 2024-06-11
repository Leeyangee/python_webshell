
## [](#header-31)一个简单的python webshell


众所周知蚁剑是一款很好的文件管理工具和部署工具，黑客可以直接使用蚁剑来连接webshell，那为什么不能用蚁剑来管理自己的服务器呢？

使用方法：只需要下载 webshell.py 并使用 python3 运行即可，自动根据机器生成加密的连接路径、连接参数，然后用蚁剑的 CMDLINUX 类型连接，并选择忽略HTTPS证书，非常方便快捷

安装
```
git clone https://github.com/Leeyangee/python_webshell
```
运行
```
python3 webshell.py
```
![/usage.png](/images/usage.png)

使用蚁剑连接

![/connect.png](/images/connect.png)
![/ignore.png](/images/ignore.png)
`*一定要忽略HTTPS证书`


第一次生成的连接路径、连接参数保存在 config/webshell.cfg 文件中，若需要更改请删除该文件，下次使用自动生成新的

--------

1.0: 修改了错误  

1.1: 更全面的配置项，舍弃 os.popen 添加了 stderr 输出  