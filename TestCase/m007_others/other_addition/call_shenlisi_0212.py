from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from pages import *
from pages.components import ChatNoticeDialog
from pages.components.dialogs import SuspendedTips
from preconditions.BasePreconditions import WorkbenchPreconditions


class Preconditions(WorkbenchPreconditions):
    """前置条件"""


class Contacts_demo(TestCase):

    @staticmethod
    def setUp_test_call_shenlisi_0212():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.create_contacts_if_not_exist_631(["测试短信1, 13800138111"])


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_shenlisi_0212(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        # 网络正常
        mess = MessagePage()
        # Step 进入群聊页面
        mess.search_and_enter_631('测试短信1')
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_tips_display():
            chatdialog.accept_and_close_tips_alert()
        single_chat = SingleChatPage()
        single_chat.click_more()
        mess.click_element_by_text('音视频通话')
        mess.click_element_by_text('视频通话')
        cp = CallPage()
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        mess.page_should_contain_text('视频通话呼叫中')
        # Step 2、主叫方点击挂断按钮
        cp.hang_up_video_call()



