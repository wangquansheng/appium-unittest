import time

from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from pages import *
from preconditions.BasePreconditions import WorkbenchPreconditions


class Preconditions(WorkbenchPreconditions):
    """前置条件"""


class Contacts_demo(TestCase):

    @staticmethod
    def setUp_test_msg_weifenglian_PC_0249():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.enter_my_computer_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0249(self):
        """验证在我的电脑-查找聊天内容-文件页面点击未下载且不可直接预览的文件-下载完成后，点击右上角的更多按钮-收藏时是否正常"""
        # 1、当前在我的电脑-查找聊天内容-文件页面-已下载完成的文件详情页
        # 2、网络正常
        single_chat = SingleChatPage()
        single_chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        time.sleep(2)
        file_name = '录制.txt'
        path = 'aaaresource'
        single_chat.send_file_messages_631(path, file_name)
        single_chat.click_setting()
        single_chat.search_chat_record_file(file_name)
        single_chat.assert_collect_record_file()

