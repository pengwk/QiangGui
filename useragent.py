# _*_ coding:utf-8 _*_
import random

__doc__ = u"generate random useragent"

user_agents = {"ie6": "Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1)",
               "ie7": " Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
               "ie8_1": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)",
               "ie8_2": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)",
               "ie9": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 7.1; Trident/5.0)",
               "ie10": "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
               "ie11": "Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko",
               "64_IE_64_Win": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Win64; x64; Trident/4.0)",
               "32_IE_64_Win": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; WOW64; Trident/4.0)",
               "IE8_Win7": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)",
               "safari": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9) AppleWebKit/537.71 (KHTML, like Gecko) Version/7.0 Safari/537.71",
               "chrome_1": "Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
               "chrome_2": "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
               "chrome_3": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36"}


def rand_agent():
    u"""返回一个随机的user agent
    """
    user_agent = random.choice(user_agents.values())
    return user_agent


def header(Host,Cookie,Referer,ContentType,Origin,UserAgent):
    u"""产生header

    """
    return nice_header


