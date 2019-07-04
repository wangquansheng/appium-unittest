import os
import time
import re
import settings

report_path = settings.REPORT_HTML_PATH2

def get_number(content):
    """获取生成的报告数据"""
    list = []
    patt0 = re.findall(r'共 (.*?)，', content)
    patt1 = re.findall(r'通过 (.*?)，', content)
    patt2 = re.findall(r'失败 (.*?)，', content)
    patt3 = re.findall(r'错误 (.*?)，', content)
    patt4 = re.findall(r'通过率= (.*?)%', content)
    # 如果不存在匹配，传入默认值0
    if len(patt0) > 0:
        list.append(patt0[0])
    else:
        list.append("0")
    if len(patt1) > 0:
        list.append(patt1[0])
    else:
        list.append("0")
    if len(patt2) > 0:
        list.append(patt2[0])
    else:
        list.append("0")
    if len(patt3) > 0:
        list.append(patt3[0])
    else:
        list.append("0")
    if len(patt4) > 0:
        list.append(patt4[0])
    else:
        list.append("0")
    return list

def get_content():
    """循环遍历获取报告路径下所有文件数据"""
    path_list = os.listdir(report_path)
    total_list = []
    module_name = []
    for file in path_list:
        file_path = os.path.join(settings.REPORT_HTML_PATH2, file)
        if os.path.getsize(file_path) == 0:
            print(file_path)
            return None, None
        with open(file_path, mode='r', encoding="utf-8") as f:
            content = f.read()
            total_list.append(get_number(content))
            module_name.append(file[:file.index(".")])
    return total_list, module_name

def get_total():
    """进行数据统计"""
    while True:
        total_list, module_name = get_content()
        lists = []
        if total_list:
            number = len(total_list)
            # 统计各个总数
            a = 0
            for i in range(4):
                for j in range(number):
                    a += int(total_list[j][i])
                lists.append(a)
                a = 0
            # 计算平均通过率
            b = 0.0
            for m in range(number):
                b += float(total_list[m][4])
            b = '%.2f' % (b / number)
            lists.append(b)
            total_list.append(lists)
            break
        elif total_list is None:
            print("等待中")
            time.sleep(1800)
    print("统计：")
    print(total_list)
    return total_list, module_name

def send_email():
    """发送邮件"""
    total_list, module_name = get_total()
    # 成功、失败、错误、总计、通过率
    try:
        from library.core.utils import send_report2
        send_report2.get_html_text(total_list, module_name)
        from library.core.utils import CommandLineTool
        cli_commands = CommandLineTool.parse_and_store_command_line_params()
        if cli_commands.sendTo:
            send_report2.send_mail(*cli_commands.sendTo)
    except:
        pass

if __name__ == '__main__':
    send_email()