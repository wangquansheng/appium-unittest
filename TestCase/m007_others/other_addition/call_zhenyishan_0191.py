import time

from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from pages import *
from pages.call.mutivideo import MutiVideoPage
from pages.components.dialogs import SuspendedTips
from preconditions.BasePreconditions import WorkbenchPreconditions


class Preconditions(WorkbenchPreconditions):
    """前置条件"""


class Contacts_demo(TestCase):

    @staticmethod
    def setUp_test_call_zhenyishan_0191():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.create_contacts_if_not_exist_631(
            ["给个名片1, 13800138200", "给个名片2, 13800138300", "测试短信1, 13800138111", "测试短信2, 13800138112",
             "给个红包1, 13800138000", "联系人1, 18312345678", "联系人2, 18323456789", "联系人3, 13812345678", "联系人4, 13823456789"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_zhenyishan_0191(self):
        """多方视频管理界面，检查添加联系人按钮"""
        # 1、已成功发起多方视频，人数未满9人
        # 2、当前为多方视频管理界面
        mess = MessagePage()
        # Step 1、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        cp.click_multi_party_video()
        cmvp = MultiPartyVideoPage()
        cmvp.input_contact_search("15875537272")
        cmvp.click_text('未知号码')
        cmvp.input_contact_search("13800138222")
        cmvp.click_text('未知号码')
        cmvp.click_tv_sure()
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        # Step 2、主叫方点击挂断按钮
        time.sleep(3)

        MutiVideoPage().click_multi_video_add_person()
        time.sleep(2)
        LabelGroupingPage().click_local_contacts('给个名片1', '给个名片2', '测试短信1', '测试短信2', '给个红包1', '联系人1', '联系人2', '联系人3', '联系人4')
        cmvp.is_toast_exist('人数已达上限8人')



