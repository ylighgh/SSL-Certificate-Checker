#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import ssl
import time
import requests
import socket
import datetime

from happy_python import HappyLog
from urllib.parse import urlparse

hlog = HappyLog.get_instance()

DEFAULT_HTTPS_PORT = 443
DEFAULT_HTTP_PORT = 80
HTTPS_SCHEME = 'https'
HTTP_SCHEME = 'http'

web_sites_file = 'WEBSITES'


def format_time(str_time: str) -> datetime:
    # GMT+8
    return datetime.datetime.strptime(str_time, r'%b %d %H:%M:%S %Y %Z') + datetime.timedelta(hours=8)


def get_now_time() -> datetime:
    return datetime.datetime.strptime(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), '%Y-%m-%d %H:%M:%S')


def get_scheme(url: str) -> str:
    return urlparse(url).scheme


def get_web_status_code(url: str) -> int:
    try:
        status_code = requests.get(url, timeout=3).status_code
    except Exception:
        status_code = 1
    return status_code


def format_remain_time(time_remaining: datetime) -> str:
    day_count = time_remaining.days

    seconds_per_minute = 60
    seconds_per_hour = seconds_per_minute * 60
    seconds_unaccounted_for = time_remaining.seconds

    hours = int(seconds_unaccounted_for / seconds_per_hour)
    seconds_unaccounted_for -= hours * seconds_per_hour
    minutes = int(seconds_unaccounted_for / seconds_per_minute)

    return f'{day_count}天{hours}小时{minutes}分钟'


def get_certificate_info(host, port) -> list:
    context = ssl.create_default_context()
    with context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=host) as s:
        s.connect((host, port))
        certificate_info = s.getpeercert()
        subject = dict(x[0] for x in certificate_info['subject'])

        common_name = subject['commonName']
        register_datetime = format_time(certificate_info['notBefore'])
        expire_datetime = format_time(certificate_info['notAfter'])
        remain_time = format_remain_time(expire_datetime - get_now_time())

        return common_name, register_datetime, expire_datetime, remain_time


def parser_host_port(url: str, scheme: str):
    host = urlparse(url).hostname
    if scheme == HTTPS_SCHEME:
        port = DEFAULT_HTTPS_PORT if urlparse(url).port is None else urlparse(url).port
    else:
        port = DEFAULT_HTTP_PORT if urlparse(url).port is None else urlparse(url).port
    return host, port


class WebSite:
    check_domain: str
    common_domain: str
    scheme: str
    status_code: int
    register_datetime: datetime
    expire_datetime: datetime
    remain_time: datetime

    def __init__(self, hostname, scheme) -> None:
        host, port = parser_host_port(hostname, scheme)
        self.scheme = scheme
        self.check_domain = host
        self.status_code = get_web_status_code(hostname)
        if self.status_code != 1:
            if scheme == HTTPS_SCHEME:
                self.common_domain, self.register_datetime, self.expire_datetime, \
                self.remain_time = get_certificate_info(host, port)

    def info(self):
        if self.status_code == 1:
            hlog.warning(f'\n检测域名:{self.check_domain}\t'
                         f'协议类型:{self.scheme}\t'
                         f'网页状态:无法访问')
        else:
            if self.scheme == HTTPS_SCHEME:
                hlog.info(f'\n检测域名:{self.check_domain}\t'
                          f'协议类型:{self.scheme}\t'
                          f'网页状态:{self.status_code}\t'
                          f'泛域名:{self.common_domain}\t'
                          f'证书有效时间:{self.register_datetime}至{self.expire_datetime}\t'
                          f'剩余时间:{self.remain_time}')
            else:
                hlog.info(f'\n检测域名:{self.check_domain}\t'
                          f'协议类型:{self.scheme}\t'
                          f'网页状态:{self.status_code}')


def main():
    with open(str(web_sites_file), 'r') as f:
        for url in f.readlines():
            url = url.strip()
            scheme = get_scheme(url)
            web = WebSite(url, scheme)
            web.info()


if __name__ == '__main__':
    main()
