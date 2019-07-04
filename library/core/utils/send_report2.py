# -*- coding: utf-8 -*-

import json
import os
import smtplib
import time
import traceback
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import settings

SUBJECT = u'【持续集成】和飞信[%s]集成报告'
HOST = 'smtp.139.com'
PORT = 25
FROM = '19876283465@139.com'
PASSWORD = 'cmcc2018@'

# 报告路径
UI_REPORT = settings.REPORT_HTML_PATH2
FILES = [UI_REPORT]
SONAR_URL = """
http://10.1.0.101:9000/api/measures/component?\
additionalFields=metrics,periods&componentKey=andfetion_android&\
metricKeys=ncloc,bugs,vulnerabilities,code_smells,duplicated_lines_density
"""
PGYER_URL = 'https://www.pgyer.com/apiv2/app/builds'
PGYER_PAYLOAD = {
    '_api_key': '82fe733ec2739d270885b28d7239d185',
    'appKey': '296e3112fabb6768b8abbb0cd54ae6b1'
}
CURRENT_VERSION = u'未知版本'

CODE_CHECK = {
    'LINE': u'暂无数据',
    'BUG': u'暂无数据',
    'VUL': u'暂无数据',
    'SMELL': u'暂无数据',
    'DUP': u'暂无数据'
}

UNIT_TEST = {
    'COVER': u'暂无数据',
    'TOTAL': u'暂无数据',
    'SUCCESS': u'暂无数据',
    'FAIL': u'暂无数据',
    'RATE': u'暂无数据'
}

UI_AUTOMATION = {
    'TOTAL': u'暂无数据',
    'SUCCESS': u'暂无数据',
    'FAIL': u'暂无数据',
    'ERROR': u'暂无数据',
    'RATE': u'暂无数据'
}

API_AUTOMATION = {
    'TOTAL': u'暂无数据',
    'SUCCESS': u'暂无数据',
    'FAIL': u'暂无数据',
    'RATE': u'暂无数据'
}

HTML_TEXT = ""

def get_sonar_metric():
    """获取静态代码扫描结果"""
    try:
        response = requests.get(SONAR_URL)
        result = json.loads(response.text)
        measures = result['component']['measures']
        global CODE_CHECK
        for measure in measures:
            if measure['metric'] == 'ncloc':
                CODE_CHECK['LINE'] = measure['value']
            elif measure['metric'] == 'bugs':
                CODE_CHECK['BUG'] = measure['value']
            elif measure['metric'] == 'vulnerabilities':
                CODE_CHECK['VUL'] = measure['value']
            elif measure['metric'] == 'code_smells':
                CODE_CHECK['SMELL'] = measure['value']
            elif measure['metric'] == 'duplicated_lines_density':
                CODE_CHECK['DUP'] = measure['value'] + '%'
    except:
        print("获取SONAR数据失败")
        traceback.print_exc()

def get_html_text(total_list, module_name):
    """获取报告数据，生成HTML文件"""

    global HTML_TEXT
    HTML_TEXT = """
<html>
	<head></head>
	<body style="font-size: 20px; line-height: 20px;">
		<br>
		<h3>UI自动化测试</h3>
		<table border="1" cellspacing="0" cellpadding="6">
			<th colspan="6" bgcolor="grey" width="600px">UI自动化测试结果</th>
			<tr><td></td><td style="color: purple; font-weight: bold;">用例数</td><td style="color: green; font-weight: bold;">成功数</td><td style="color: red; font-weight: bold;">失败数</td><td style="color: red; font-weight: bold;">错误数</td><td style="color: purple; font-weight: bold;">通过率</td></tr>
        """
    number = len(module_name)
    for i in range(number):
        HTML_TEXT += "<tr><td>" + module_name[i] + "</td>"
        for j in range(len(total_list[i])):
            if j == (len(total_list[i])-1):
                HTML_TEXT += "<td>" + total_list[i][j] + "%</td>"
            else:
                HTML_TEXT += "<td>" + total_list[i][j] + "</td>"
        HTML_TEXT += "</tr>\n"
    HTML_TEXT += "<tr><td>合计</td><td>" + str(total_list[number][0]) + "</td><td>" + str(total_list[number][1]) + "</td><td>" + \
                 str(total_list[number][2]) + "</td><td>" + str(total_list[number][3]) + "</td><td>" + str(total_list[number][4]) + "%</td></tr>"
    HTML_TEXT += """
		</table>
		<br>
		<p style="font-size: 16px; color: blue;">UI自动化测试明细详见附件</p>
		<br>
		<hr>
		<p style="font-size: 14px; color: red;">此邮件为系统邮件，请勿直接回复。如有问题请联系<b>【测试团队】</b>相关同事。</p>
	</body>
</html>
    """

def get_current_version():
    """获取APP当前版本号"""
    global CURRENT_VERSION
    try:
        response = requests.post(url=PGYER_URL, data=PGYER_PAYLOAD)
        assert response.status_code == 200
        result = json.loads(response.text)
        # CURRENT_VERSION = 'V' + result['data']['list'][0]['buildVersion']
        CURRENT_VERSION = 'V6.3.1.0524'
    except:
        print("获取APP当前版本号失败")
        traceback.print_exc()


def zip_dir(path, zip_handle):
    for root, dirs, files in os.walk(path):
        for file in files:
            zip_handle.write(os.path.join(root, file))


def send_mail(*to):
    get_sonar_metric()
    get_current_version()

    mail = MIMEMultipart()
    # 使用Header封装，139会报550错误：Mail rejected
    """
    mail['From'] = Header(u'品质管理部', 'utf-8')
    mail['To'] = Header(u'自研版和飞信', 'utf-8')
    mail['Subject'] = Header(SUBJECT % CURRENT_VERSION, 'utf-8')
    """
    mail['From'] = FROM
    mail['To'] = ','.join(to)
    mail['Subject'] = SUBJECT % CURRENT_VERSION

    mail.attach(MIMEText(HTML_TEXT, 'html', 'utf-8'))

    for FILE in FILES:
        if os.path.isfile(os.path.abspath(FILE)):
            attachment = MIMEApplication(open(FILE, 'rb').read())
            attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(FILE))
            mail.attach(attachment)
        elif os.path.isdir(os.path.abspath(FILE)):
            import zipfile, tempfile
            tf = tempfile.mktemp()
            with zipfile.ZipFile(tf, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zip_dir(os.path.relpath(FILE), zipf)
                zipf.close()
            with open(tf, 'rb') as f:
                result = f.read()
                attachment = MIMEApplication(result)
                attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(FILE) + '.zip')
                mail.attach(attachment)

    retry = 3
    while True:
        if retry <= 0:
            print(u'发送邮件重试已达3次，不再重试')
            break
        try:
            smtp = smtplib.SMTP(host=HOST, port=PORT)
            smtp.login(user=FROM, password=PASSWORD)
            smtp.sendmail(from_addr=FROM, to_addrs=to, msg=mail.as_string())
            print(u'发送邮件成功')
            break
        except:
            print(u'发送邮件失败')
            traceback.print_exc()
            retry -= 1
            time.sleep(5)
    smtp.quit()


if __name__ == '__main__':
    send_mail()
