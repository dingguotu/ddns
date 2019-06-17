# ddns.py

```bash
@author tinko
@version 0.1.0
```

ddns.py 是基于 [DNSPod](http://www.dnspod.cn/docs/records.html#dns) 服务的动态 DNS 脚本，用于检测 IP 变化并更新至 DNSPod，支持多域名解析。支持 Linux 设备，包括树莓派（[Raspberry Pi](https://www.raspberrypi.org/)）。不需要手动添加解析，也不需要人工获取 domain_id 和 record_id，只要跟着教程来，小白都可以很快上手（软件都不会安装的除外）。

---

## 关键词

1. domain  域名
2. sub_domain  二级域名，子域名

## 前置条件

1. Git
2. python 2.7.*
3. DNSPod 账号

## 使用方法

首先，确保已经安装 [git](https://git-scm.com/) 客户端以及 [python 2.7.*](https://www.python.org/downloads/)，建议python 2.7.13+

---

通过本命令获取 ddns.py

```bash
git clone https://gitee.com/tdg/ddns.git
```

---

接下来到DNSPod中创建API Token，具体步骤是：登录DNSPod -> 进入控制台 -> 用户中心 -> 安全设置 -> 开启API Token（已开启的点击查看） -> 创建API Token（**Token只会显示一次，以后将没办法查看已有的Token，请务必保管好自己的Token，如果不慎丢失，可以删除后重新创建，但是程序里也要及时修改，以免导致程序不能正常运行**）

---

如果域名是在阿里云或其他非腾讯云处购买的，还需要进入相对应的服务商控制台，修改域名的DNS地址为：

```bash
f1g1ns1.dnspod.net
f1g1ns2.dnspod.net
```

---

复制 `conf.sample.json` 文件，并重命名为 `conf.json`，根据您的DNSPod设置修改 `conf.json` 文件，填入以下内容：

```bash
{
    "id": <api_token_id>,
    "token": <api_token>,
    "domains": [
        {
            "name": <first_domain>,
            "sub_domains": [<first_sub_domain_name>, <second_sub_domain_name>,...]
        },
        {
            "name": <second_domain>,
            "sub_domains": [<first_sub_domain_name>, <second_sub_domain_name>,...]
        }
    ]
}
```

`domains`部分，想绑定几个就写几个，不需要多写，`sub_domains`通常写 `@` 和 `*` 就够了，二级子域名直接用 `*` 代替，然后在自己的代理服务器（IIS，nginx，Apache等）上面去进行绑定。domain 和 sub_domain 可以不需要事先手动绑定，本程序会自动识别

---

最后设置 crontab 定时任务，以便更新DNS记录：

```bash
sudo crontab -e
/30 * * * * python /home/pi/ddns/ddns.py
```

本教程的定时任务是Linux版本，`/30` 表示每隔30分钟运行一次，可以自行修改，本教程不做限定。`/home/pi/ddns/ddns.py` 是绝对路径，请根据实际情况进行修改

Windows版请自行学习[Windows 任务计划](https://jingyan.baidu.com/article/0964eca26a53b08285f536d2.html)
