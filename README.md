# ddns.py

```
@author tinko
@version 0.0.1
```

ddns.py 是基于 [DNSPod](http://www.dnspod.cn/docs/records.html#dns) 服务的动态 DNS 脚本，用于检测 IP 变化并更新至 DNSPod，支持多域名解析。支持 Linux 设备，包括树莓派（[Raspberry Pi](https://www.raspberrypi.org/)）。

# Prerequisites

1. python

# Installation

安装 [git](https://git-scm.com/) 客户端，通过本命令获取 ddns.py

<pre>
git clone https://gitee.com/tdg/ddns.git ddns
</pre>

然后到 ddns 目录下新建 ```conf.json``` 文件，根据您的 DNSPod 设置，填入以下内容：

<pre>
{
    "id": &lt;your_api_token_id&gt,
    "token": &lt;your_api_token&gt,
    "domain": &lt;your_domain&gt,
    "sub_domains": [
	{
	    "name": &lt;your_first_sub_domain_name&gt;,
	    "domain_id": &lt;your_domain_id&gt;,
	    "record_id": &lt;your_record_id&gt;
	},
	{
	    "name": &lt;your_second_sub_domain_name&gt;,
	    "domain_id": &lt;your_domain_id&gt;,
	    "record_id": &lt;your_record_id&gt;
	}
    ]
}
</pre>

获取你的domain_id
<pre>
curl -X POST https://dnsapi.cn/Domain.List -d 'login_token=LOGIN_TOKEN&format=json'
</pre>

获取你的record_id
<pre>
curl -X POST https://dnsapi.cn/Record.List -d 'login_token=LOGIN_TOKEN&format=json&domain_id=YOUR_DOMAIN_ID'
</pre>

最后设置 crontab 定时任务
每隔30分钟运行一次，以便更新DNS记录：
<pre>
sudo crontab -e
/30 * * * * python /home/pi/ddns/ddns.py
</pre>
