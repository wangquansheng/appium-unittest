import time

from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from pages import *
from preconditions.BasePreconditions import WorkbenchPreconditions


class Preconditions(WorkbenchPreconditions):
    """前置条件"""


class Contacts_demo(TestCase):

    @staticmethod
    def setUp_test_msg_xiaoliping_A_0009():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist_631(["测试短信1, 13800138111", "测试短信2, 13800138112"])
        Preconditions.create_group_if_not_exist_not_enter_chat_631('测试群组1', "测试短信1", "测试短信2")
        mess = MessagePage()
        # Step 进入群聊页面
        mess.search_and_enter('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        # Step 建立群二维码
        groupchat.click_setting()
        groupset.wait_for_page_load()
        groupset.click_QRCode()
        groupset.wait_for_qecode_load()
        groupset.click_qecode_download_button()
        groupset.click_qecode_back_button()
        groupset.click_group_manage()
        groupset.wait_exist_and_delete_confirmation_box_load()
        groupset.click_group_manage_disband_button()
        SingleChatPage().click_sure()
        GroupChatPage().click_back()
        SearchPage().click_back_button()


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoliping_A_0009(self):
        """扫描普通群无效二维码，该群已解散"""
        # 1、网络正常
        # 2、已登录客户端
        # 3、当前在消息列表界面
        # 4、该群已解散）
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_take_a_scan()
        mess.click_enter_photo()
        mess.click_qecode_photo()
        time.sleep(3)
        mess.is_text_present('群已解散')


