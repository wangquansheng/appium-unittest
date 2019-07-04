import argparse
import json
import os

import settings
from library.core.utils.testcasefilter import TEST_CASE_TAG_ENVIRON


def parse_and_store_command_line_params():
    parser = argparse.ArgumentParser()
    parser.add_argument('--suite', '-s', action='append', help='测试套件路径')
    parser.add_argument('--include', '-i', nargs='+', help='匹配的用例标签')
    parser.add_argument('--module_name', '-m', help='端口模块名称')
    parser.add_argument('--delete_module_name', '-dm', help='端口模块名称2')
    parser.add_argument('--sendTo', nargs='+', help='匹配的用例标签')
    parser.add_argument('--deviceConfig', '-d', help='手机配置名称')
    parser.add_argument('--appUrl', help='测试APP下载路径')
    parser.add_argument('--installOn', action='store_true', default=False, help='初始化运行时，是否安装应用')
    args = parser.parse_args()
    # 如果指定此参数，报告生成路径为TestReport2文件夹，此参数不会删除报告文件
    if args.module_name:
        settings.REPORT_HTML_PATH= os.path.join(settings.REPORT_HTML_PATH2, args.module_name + '.html')
    # 如果指定此参数，报告生成路径为TestReport2文件夹，此参数会删除TestReport2文件夹下未在执行的报告文件
    if args.delete_module_name:
        if os.path.exists(settings.REPORT_HTML_PATH2):
            file_list = os.listdir(settings.REPORT_HTML_PATH2)
            for file in file_list:
                try:
                    file_path = os.path.join(settings.REPORT_HTML_PATH2, file)
                    os.remove(file_path)
                except:
                    print(file + "删除失败")
        settings.REPORT_HTML_PATH= os.path.join(settings.REPORT_HTML_PATH2, args.delete_module_name + '.html')
    if args.include:
        include = json.dumps(args.include, ensure_ascii=False).upper()
        os.environ[TEST_CASE_TAG_ENVIRON] = include
    if args.appUrl:
        os.environ['APP_DOWNLOAD_URL'] = args.appUrl
    if args.installOn:
        os.environ['APPIUM_INSTALL_APP_ACTION'] = 'ON'
    return args
