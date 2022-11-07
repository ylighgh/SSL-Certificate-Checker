# WebChecker

## 介绍

通过读取 `WEBSITES` 文件里的网址，返回网址的响应状态码，如果是传输协议是 `https`，同时返回证书相关信息

## 使用

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行

```bash
python web_checker.py
```

### 示例

```bash
$ python web_checker.py 
2022-11-07 09:59:01 3510 [INFO] 
检测域名:packages.cdgeekcamp.com        协议类型:https  网页状态:200    泛域名:*.cdgeekcamp.com     证书有效时间:2022-10-30 23:07:06至2023-01-28 23:07:05   剩余时间:82天13小时8分钟
2022-11-07 09:59:01 3510 [INFO] 
检测域名:blog.csdn.net  协议类型:https  网页状态:200    泛域名:*.csdn.net证书有效时间:2021-11-03 08:00:00至2022-12-03 07:59:59   剩余时间:25天22小时0分钟
2022-11-07 09:59:01 3510 [INFO] 
检测域名:www.baidu.com  协议类型:https  网页状态:200    泛域名:baidu.com证书有效时间:2022-07-05 13:16:02至2023-08-06 13:16:01   剩余时间:272天3小时17分钟
2022-11-07 09:59:02 3510 [INFO] 
检测域名:www.chikexing.com      协议类型:https  网页状态:200    泛域名:www.chikexing.com     证书有效时间:2021-12-09 08:00:00至2022-12-10 07:59:59   剩余时间:32天22小时0分钟
2022-11-07 09:59:02 3510 [INFO] 
检测域名:www.hangzhou.gov.cn    协议类型:http   网页状态:200
2022-11-07 09:59:02 3510 [INFO] 
检测域名:www.hao123.com 协议类型:http   网页状态:200
2022-11-07 09:59:03 3510 [INFO] 
检测域名:www.bilibili.com       协议类型:https  网页状态:200    泛域名:*.bilibili.com        证书有效时间:2022-09-29 17:56:02至2023-10-31 17:56:01   剩余时间:358天7小时56分钟
2022-11-07 09:59:04 3510 [INFO] 
检测域名:www.zhihu.com  协议类型:https  网页状态:200    泛域名:*.zhihu.com证书有效时间:2021-11-30 08:00:00至2023-01-01 07:59:59   剩余时间:54天22小时0分钟
```