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
    parser.add_argument('--sendTo', nargs='+', help='匹配的用例标签')
    parser.add_argument('--deviceConfig', '-d', help='手机配置名称')
    parser.add_argument('--appUrl', help='测试APP下载路径')
    parser.add_argument('--installOn', action='store_true', default=False, help='初始化运行时，是否安装应用')
    args = parser.parse_args()
    if args.module_name:
        # if os.path.exists(settings.REPORT_HTML_PATH2):
        #     file_list = os.listdir(settings.REPORT_HTML_PATH2)
        #     for file in file_list:
        #         try:
        #             file_path = os.path.join(settings.REPORT_HTML_PATH2, file)
        #             os.remove(file_path)
        #         except:
        #             print(file + "删除失败")
        settings.REPORT_HTML_PATH= os.path.join(settings.REPORT_HTML_PATH2, args.module_name + '.html')
    if args.include:
        include = json.dumps(args.include, ensure_ascii=False).upper()
        os.environ[TEST_CASE_TAG_ENVIRON] = include
    if args.appUrl:
        os.environ['APP_DOWNLOAD_URL'] = args.appUrl
    if args.installOn:
        os.environ['APPIUM_INSTALL_APP_ACTION'] = 'ON'
    return args
