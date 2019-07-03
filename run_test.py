import os
import time
import re
import settings

report_path = settings.REPORT_HTML_PATH2

def get_number(content):
        list = []
        patt0 = re.findall(r'共 (.*?)，', content)
        patt1 = re.findall(r'通过 (.*?)，', content)
        patt2 = re.findall(r'失败 (.*?)，', content)
        patt3 = re.findall(r'错误 (.*?)，', content)
        patt4 = re.findall(r'通过率= (.*?)%', content)
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
    while True:
        total_list, module_name = get_content()
        lists = []
        if total_list:
            lists.append(int(total_list[0][0]) + int(total_list[1][0]) + int(total_list[2][0]) + int(total_list[3][0]) + int(total_list[4][0]))
            lists.append(int(total_list[0][1]) + int(total_list[1][1]) + int(total_list[2][1]) + int(total_list[3][1]) + int(total_list[4][1]))
            lists.append(int(total_list[0][2]) + int(total_list[1][2]) + int(total_list[2][2]) + int(total_list[3][2]) + int(total_list[4][2]))
            lists.append(int(total_list[0][3]) + int(total_list[1][3]) + int(total_list[2][3]) + int(total_list[3][3]) + int(total_list[4][3]))
            lists.append('%.2f' % ((float(total_list[0][4]) + float(total_list[1][4]) + float(total_list[2][4]) + float(
                total_list[3][4]) + float(total_list[4][4])) / 5))
            total_list.append(lists)
            break
        elif total_list is None:
            print("等待中")
            time.sleep(1800)
    print("统计：")
    print(total_list)
    return total_list, module_name

def send_email():
    total_list, module_name = get_total()
    # 成功、失败、错误、总计、通过率
    try:
        from library.core.utils import send_report2
        send_report2.get_ui_automation_metric(total_list)
        send_report2.get_interface_name(module_name)
        from library.core.utils import CommandLineTool
        cli_commands = CommandLineTool.parse_and_store_command_line_params()
        if cli_commands.sendTo:
            send_report2.send_mail(*cli_commands.sendTo)
    except:
        pass

if __name__ == '__main__':
    send_email()