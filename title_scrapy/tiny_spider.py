__author__ = 'vpersie9'
# -*-coding:utf-8-*-
import re
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# 　从糗百获取全部代码，并匹配导出所需内容
class recode():
    def scrapy_code(self,url,headers):
        html=requests.get(url,headers=headers).text
        code=re.findall('div class="content">(.*?)<',html,re.S)
        code_we_need=[]
        for each in code:
            code_we_need.append(each)
        return code_we_need
# 　将所需内容保存在txt文本里
    def save_code(self,code_print):
        f=open('code.txt','a')
        for each in code_print:
            f.writelines(each)
        f.close()

if __name__=="__main__":
    url="http://www.qiushibaike.com/"
    headers={"User-Agent":"Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36"}
    get_code=recode()
    code_show=get_code.scrapy_code(url,headers)
    get_code.save_code(code_show)
