
## [](#header-31)一个简单的python webshell


众所周知蚁剑是一款很好的文件管理工具和部署工具，黑客可以直接使用蚁剑来连接webshell，那为什么不能用蚁剑来管理自己的服务器呢？

使用方法：只需要下载 webshell.py 并使用 python3 运行即可，自动根据机器生成加密的连接路径、连接参数，然后用蚁剑 CMDLINUX 类型连接即可，非常方便快捷

```
python3 webshell.py
```
![/usage.png](/usage.png)
![/connect.png](/connect.png)

第一次生成的连接路径、连接参数保存在 config/webshell.cfg 文件中，若需要更改请删除该文件，下次使用自动生成新的