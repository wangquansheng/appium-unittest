import time
import unittest

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.call.mutivideo import MutiVideoPage
from pages.components import ChatNoticeDialog, ContactsSelector
from pages.components.dialogs import SuspendedTips
from pages.message.Send_CardName import Send_CardNamePage
from preconditions.BasePreconditions import LoginPreconditions, WorkbenchPreconditions


class Preconditions(WorkbenchPreconditions):
    """前置条件"""
    contacts_name_1 = LoginPreconditions.get_contacts_by_row_linename(0, 'contacts_name')
    telephone_num_1 = LoginPreconditions.get_contacts_by_row_linename(0, 'telephone_num')

    @staticmethod
    def hang_up_fetion_call():
        time.sleep(3)
        callpage = CallPage()
        count = 65
        while count > 0:
            try:
                if callpage.wait_for_call_page2(timeout=1):
                    break
                callpage.hang_up_the_call()
            except:
                pass
        else:
            return True


class ContactsDemo(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        import warnings
        warnings.simplefilter('ignore', ResourceWarning)

    def default_setUp(self):
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')

    def default_tearDown(self):
        Preconditions.disconnect_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_shenlisi_0071(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        # 网络正常
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        time.sleep(2)
        # 是否存在多方电话弹出提示
        if cp.is_exist_multi_party_telephone():
            # 存在提示点击跳过
            cp.click_multi_party_telephone()
            # 是否存在知道了弹出提示
            time.sleep(2)
            if cp.is_exist_know():
                # 存在提示点击跳过
                cp.click_know()
            # 是否存在授权允许弹出提示
            time.sleep(1)
            if cp.is_exist_allow_button():
                # 存在提示点击允许
                cp.click_allow_button(False)
            # 点击返回按钮返回通话页面
            time.sleep(1)
            cp.click_back()
        cp.wait_for_page_load()
        pad = cp.is_on_the_dial_pad()
        if not pad:
            cp.click_dial_pad()
            time.sleep(1)
            cp.click_one()
            cp.click_five()
            cp.click_eight()
            cp.click_seven()
            cp.click_five()
            cp.click_five()
            cp.click_three()
            cp.click_seven()
            cp.click_two()
            cp.click_seven()
            cp.click_two()
            time.sleep(1)
        cp.click_call_phone()
        time.sleep(1)
        cp.page_should_contain_text('飞信电话（免费）')
        cp.page_should_contain_text('语音通话')
        cp.page_should_contain_text('普通电话')
        cp.click_voice_call()
        time.sleep(1)
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        time.sleep(1)
        if not (cp.is_text_present('15875537272') or cp.is_text_present('测试人员2')):
            raise Exception("Error")
        cp.page_should_contain_text('正在呼叫...')
        cp.hang_up_voice_call()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_shenlisi_0072(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        # 网络正常
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        time.sleep(2)
        # 是否存在多方电话弹出提示
        if cp.is_exist_multi_party_telephone():
            # 存在提示点击跳过
            cp.click_multi_party_telephone()
            # 是否存在知道了弹出提示
            time.sleep(2)
            if cp.is_exist_know():
                # 存在提示点击跳过
                cp.click_know()
            # 是否存在授权允许弹出提示
            time.sleep(1)
            if cp.is_exist_allow_button():
                # 存在提示点击允许
                cp.click_allow_button(False)
            # 点击返回按钮返回通话页面
            time.sleep(1)
            cp.click_back()
        cp.wait_for_page_load()
        pad = cp.is_on_the_dial_pad()
        if not pad:
            cp.click_dial_pad()
            time.sleep(1)
            cp.click_one()
            cp.click_five()
            cp.click_eight()
            cp.click_seven()
            cp.click_five()
            cp.click_five()
            cp.click_three()
            cp.click_seven()
            cp.click_two()
            cp.click_seven()
            cp.click_two()
            time.sleep(1)
        cp.click_call_phone()
        time.sleep(1)
        cp.click_voice_call()
        time.sleep(1)
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        time.sleep(1)
        cp.hang_up_voice_call()
        time.sleep(1)
        mess.click_element_by_text('15875537272')
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        time.sleep(1)
        if not (cp.is_text_present('15875537272') or cp.is_text_present('测试人员2')):
            raise Exception("Error")
        cp.page_should_contain_text('正在呼叫...')
        cp.hang_up_voice_call()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_shenlisi_0073(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        # 网络正常
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        time.sleep(2)
        # 是否存在多方电话弹出提示
        if cp.is_exist_multi_party_telephone():
            # 存在提示点击跳过
            cp.click_multi_party_telephone()
            # 是否存在知道了弹出提示
            time.sleep(2)
            if cp.is_exist_know():
                # 存在提示点击跳过
                cp.click_know()
            # 是否存在授权允许弹出提示
            time.sleep(1)
            if cp.is_exist_allow_button():
                # 存在提示点击允许
                cp.click_allow_button(False)
            # 点击返回按钮返回通话页面
            time.sleep(1)
            cp.click_back()
        cp.wait_for_page_load()
        pad = cp.is_on_the_dial_pad()
        if not pad:
            cp.click_dial_pad()
            time.sleep(1)
            cp.click_one()
            cp.click_five()
            cp.click_eight()
            cp.click_seven()
            cp.click_five()
            cp.click_five()
            cp.click_three()
            cp.click_seven()
            cp.click_two()
            cp.click_seven()
            cp.click_two()
            time.sleep(1)
        cp.click_call_phone()
        time.sleep(1)
        cp.click_voice_call()
        time.sleep(1)
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        time.sleep(1)
        cp.hang_up_voice_call()
        time.sleep(1)
        mess.click_element_by_text('15875537272')
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        time.sleep(1)
        if not (cp.is_text_present('15875537272') or cp.is_text_present('测试人员2')):
            raise Exception("Error")
        cp.page_should_contain_text('正在呼叫...')
        cp.hang_up_voice_call()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_shenlisi_0074(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        Preconditions.create_contacts_if_not_exist_631(["测试短信1, 13800138111"])
        # 网络正常
        mess = MessagePage()
        # Step 进入群聊页面
        mess.search_and_enter_631('测试短信1')
        ContactDetailsPage().click_voice_call_icon()
        cp = CallPage()
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        time.sleep(1)
        cp.page_should_contain_text('测试短信1')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_shenlisi_0093(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        # 网络正常
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        pad = cp.is_on_the_dial_pad()
        if not pad:
            cp.click_dial_pad()
            time.sleep(1)
            cp.click_one()
            cp.click_five()
            cp.click_eight()
            cp.click_seven()
            cp.click_five()
            cp.click_five()
            cp.click_three()
            cp.click_seven()
            cp.click_two()
            cp.click_seven()
            cp.click_two()
            time.sleep(1)
        cp.click_call_phone()
        cp.click_voice_call()
        time.sleep(1)
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        time.sleep(2)
        cp.hang_up_voice_call()
        mess.is_toast_exist('通话结束')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_shenlisi_0208(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        # 网络正常
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        pad = cp.is_on_the_dial_pad()
        if not pad:
            cp.click_dial_pad()
            time.sleep(1)
            cp.click_one()
            cp.click_five()
            cp.click_eight()
            cp.click_seven()
            cp.click_five()
            cp.click_five()
            cp.click_three()
            cp.click_seven()
            cp.click_two()
            cp.click_seven()
            cp.click_two()
            time.sleep(1)
        cp.click_call_phone()
        cp.click_voice_call()
        time.sleep(1)
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        time.sleep(2)
        cp.hang_up_voice_call()
        cp.is_type_hefeixin(0, '语音通话')
        # 进入详情页
        time.sleep(3)
        cp.click_ganggang_call_time()
        ContactDetailsPage().click_video_call_icon()
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        mess.page_should_contain_text('视频通话呼叫中')
        # Step 2、主叫方点击挂断按钮
        cp.hang_up_video_call()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_shenlisi_0209(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        # 网络正常
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        pad = cp.is_on_the_dial_pad()
        if not pad:
            cp.click_dial_pad()
            time.sleep(1)
            cp.click_one()
            cp.click_five()
            cp.click_eight()
            cp.click_seven()
            cp.click_five()
            cp.click_five()
            cp.click_three()
            cp.click_seven()
            cp.click_two()
            cp.click_seven()
            cp.click_two()
            time.sleep(1)
        cp.click_call_phone()
        cp.click_voice_call()
        time.sleep(1)
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        time.sleep(2)
        cp.hang_up_voice_call()
        cp.is_type_hefeixin(0, '语音通话')
        # 进入详情页
        time.sleep(3)
        cp.click_ganggang_call_time()
        ContactDetailsPage().click_video_call_icon()
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        mess.page_should_contain_text('视频通话呼叫中')
        # Step 2、主叫方点击挂断按钮
        cp.hang_up_video_call()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_shenlisi_0210(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        # 网络正常
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        pad = cp.is_on_the_dial_pad()
        if not pad:
            cp.click_dial_pad()
            time.sleep(1)
            cp.click_one()
            cp.click_five()
            cp.click_eight()
            cp.click_seven()
            cp.click_five()
            cp.click_five()
            cp.click_three()
            cp.click_seven()
            cp.click_two()
            cp.click_seven()
            cp.click_two()
            time.sleep(1)
        cp.click_call_phone()
        cp.click_voice_call()
        time.sleep(1)
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        time.sleep(2)
        cp.hang_up_voice_call()
        cp.is_type_hefeixin(0, '语音通话')
        # 进入详情页
        time.sleep(3)
        cp.click_ganggang_call_time()
        ContactDetailsPage().click_video_call_icon()
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        mess.page_should_contain_text('视频通话呼叫中')
        # Step 2、主叫方点击挂断按钮
        cp.hang_up_video_call()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_shenlisi_0212(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        Preconditions.create_contacts_if_not_exist_631(["测试短信1, 13800138111"])
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
        # mess.page_should_contain_text('视频通话呼叫中')
        # # Step 2、主叫方点击挂断按钮
        # cp.hang_up_video_call()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_shenlisi_0346(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        # 网络正常
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        pad = cp.is_on_the_dial_pad()
        if not pad:
            cp.click_dial_pad()
            time.sleep(1)
            cp.click_phone_number('15875537272')
            time.sleep(1)
        cp.click_call_phone()
        cp.click_voice_call()
        time.sleep(1)
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        cp.hang_up_voice_call()
        cp.is_type_hefeixin(0, '语音通话')
        # 进入详情页
        time.sleep(3)
        cp.click_ganggang_call_time()
        # Checkpoint：查看详情页面是否是为飞信电话？
        cp.page_should_contain_text('语音通话')
        mess.click_back_by_android()
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        cp.click_multi_party_video()
        cmvp = MultiPartyVideoPage()
        cmvp.input_contact_search("15875537272")
        if cmvp.is_text_present('未知号码'):
            cmvp.click_text('未知号码')
        else:
            cmvp.click_text('测试人员2')
        cmvp.click_tv_sure()
        time.sleep(1)
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        cp.hang_up_video_call()
        cp.is_type_hefeixin(0, '视频通话')
        # 进入详情页
        time.sleep(3)
        cp.click_ganggang_call_time()
        # Checkpoint：查看详情页面是否是为飞信电话？
        cp.page_should_contain_text('视频通话')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0063(self):
        """发起1人的多方电话--再次呼叫，网络正常重新呼叫和飞信电话"""

        # 下面根据用例情况进入相应的页面
        # 需要预置联系人
        contactname1 = Preconditions.contacts_name_1
        contactnum1 = Preconditions.telephone_num_1
        # 新建联系人
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits_631(contactname1, contactnum1)
        # 进入通话页签
        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 选择指定联系人 点击呼叫
        from pages.components import ContactsSelector
        contactselect = ContactsSelector()
        contactselect.select_local_contacts_search(contactnum1)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        from pages import GrantPemissionsPage
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()

        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 会控页面挂断和飞信电话，回到通话页
        callpage = CallPage()
        Preconditions.hang_up_fetion_call()
        # Checkpoint：拨打的通话记录为飞信电话 进入通话详情页，标题为飞信通话类型
        callpage.is_type_hefeixin(0, '飞信电话')
        # 进入详情页
        time.sleep(3)
        callpage.click_ganggang_call_time()
        # Checkpoint：查看详情页面是否是为飞信电话？
        callpage.is_hefeixin_page('飞信电话')

        # 点击‘再次呼叫’
        callpage.click_mutil_call_again()
        suspend.ignore_tips_if_tips_display()
        # Checkpoint：当前是否是和飞信通话会控页
        # time.sleep(2)
        Preconditions.hang_up_fetion_call()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0145(self):
        """发起1人的多方电话--再次呼叫，网络正常重新呼叫和飞信电话"""

        current_mobile().launch_app()
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()
        # 下面根据用例情况进入相应的页面
        # 新建联系人
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits_631("测试短信1", "13800138111")
        # 进入通话页签
        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 选择指定联系人 点击呼叫
        from pages.components import ContactsSelector
        contactselect = ContactsSelector()
        contactselect.select_local_contacts_search("测试短信1")
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        from pages import GrantPemissionsPage
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()

        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 会控页面挂断和飞信电话，回到通话页
        callpage = CallPage()
        Preconditions.hang_up_fetion_call()

        # Checkpoint：拨打的通话记录为飞信电话 进入通话详情页，标题为飞信通话类型
        callpage.is_type_hefeixin(0, '飞信电话')
        # 进入详情页
        time.sleep(3)
        callpage.click_ganggang_call_time()
        # Checkpoint：查看详情页面是否是为飞信电话？
        callpage.page_should_contain_text('[飞信电话]')
        callpage.page_should_contain_text('拨出电话')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0146(self):
        """发起1人的多方电话--再次呼叫，网络正常重新呼叫和飞信电话"""

        current_mobile().launch_app()
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()
        # 下面根据用例情况进入相应的页面
        # 新建联系人
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        Preconditions.create_contacts_if_not_exist_631(
            ["给个名片1, 13800138200", "给个名片2, 13800138300", "测试短信1, 13800138111", "测试短信2, 13800138112",
             "给个红包1, 13800138000", "联系人1, 18312345678", "联系人2, 18323456789", "联系人3, 13812345678", "联系人4, 13823456789"])

        # 进入通话页签
        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 选择指定联系人 点击呼叫
        from pages.components import ContactsSelector
        ContactsSelector().select_local_contacts_search('给个名片1', '给个名片2', '测试短信1', '测试短信2', '给个红包1', '联系人1', '联系人2', '联系人3')
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        from pages import GrantPemissionsPage
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()

        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 会控页面挂断和飞信电话，回到通话页
        callpage = CallPage()
        Preconditions.hang_up_fetion_call()

        # Checkpoint：拨打的通话记录为飞信电话 进入通话详情页，标题为飞信通话类型
        callpage.is_type_hefeixin(0, '飞信电话')
        # 进入详情页
        time.sleep(3)
        callpage.click_ganggang_call_time()
        # Checkpoint：查看详情页面是否是为飞信电话？
        callpage.page_should_contain_text('[飞信电话]')
        callpage.page_should_contain_text('拨出电话')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0147(self):
        """发起1人的多方电话--再次呼叫，网络正常重新呼叫和飞信电话"""

        current_mobile().launch_app()
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()
        # 下面根据用例情况进入相应的页面
        # 新建联系人
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        Preconditions.create_contacts_if_not_exist_631(
            ["给个名片1, 13800138200", "给个名片2, 13800138300", "测试短信1, 13800138111", "测试短信2, 13800138112",
             "给个红包1, 13800138000", "联系人1, 18312345678", "联系人2, 18323456789"])

        # 进入通话页签
        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 选择指定联系人 点击呼叫
        from pages.components import ContactsSelector
        cmvp = MultiPartyVideoPage()
        ContactsSelector().select_local_contacts_search('15875537272', '给个名片1', '给个名片2', '测试短信1', '测试短信2', '给个红包1', '联系人1', '联系人2')
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        from pages import GrantPemissionsPage
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()

        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 会控页面挂断和飞信电话，回到通话页
        callpage = CallPage()
        Preconditions.hang_up_fetion_call()

        # Checkpoint：拨打的通话记录为飞信电话 进入通话详情页，标题为飞信通话类型
        callpage.is_type_hefeixin(0, '飞信电话')
        # 进入详情页
        time.sleep(3)
        callpage.click_ganggang_call_time()
        # Checkpoint：查看详情页面是否是为飞信电话？
        callpage.page_should_contain_text('[飞信电话]')
        callpage.page_should_contain_text('拨出电话')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0193(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        # 网络正常
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        cp.click_free_call()
        callcontact = CalllogBannerPage()
        cmvp = MultiPartyVideoPage()
        cmvp.input_contact_search("012560")
        cmvp.click_contact_head()
        cmvp.click_tv_sure()
        time.sleep(1)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()
        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        Preconditions.hang_up_fetion_call()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0389(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        # 网络正常
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        cp.click_free_call()
        callcontact = CalllogBannerPage()
        ContactsSelector().select_local_contacts_search('给个名片1', '15875537272')
        time.sleep(3)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()
        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 当出现系统通话页面，则进入手机home页
        callpage = CallPage()
        i = 0
        while i < 30:
            # time.sleep(1)
            if callpage.is_phone_in_calling_state():
                break
            else:
                i = i + 1
        # 再次激活进入和飞信app
        current_mobile().launch_app()
        mess.wait_for_page_load()
        # 点击进入通话会控页，
        current_mobile().set_network_status(0)
        time.sleep(1)
        mess.page_should_contain_text('当前网络不可用')
        Preconditions.hang_up_fetion_call()

    def tearDown_test_call_wangqiong_0389(self):
        current_mobile().set_network_status(6)
        Preconditions.disconnect_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0401(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        # 网络正常
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        cp.click_free_call()
        callcontact = CalllogBannerPage()
        ContactsSelector().select_local_contacts_search('13800138222', '15875537272')
        time.sleep(3)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()
        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 当出现系统通话页面，则进入手机home页
        i = 0
        while i < 30:
            # time.sleep(1)
            if cp.is_phone_in_calling_state():
                break
            else:
                i = i + 1
        # 回到手机主页面
        current_mobile().launch_app()
        mess.wait_for_page_load()
        Preconditions.hang_up_fetion_call()

    @unittest.skip('悬浮窗无法抓取')
    def test_call_wangqiong_0405(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        # 网络正常
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        cp.click_free_call()
        callcontact = CalllogBannerPage()
        ContactsSelector().select_local_contacts_search('13800138222', '15875537272')
        time.sleep(3)
        # time.sleep(1)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()
        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 当出现系统通话页面，则进入手机home页
        callpage = CallPage()
        Flag = True
        i = 0
        while Flag:
            # time.sleep(1)
            if callpage.is_phone_in_calling_state():
                break
            elif i > 30:
                break
            else:
                i = i + 1
        # 回到手机主页面
        from pages import OneKeyLoginPage
        page = OneKeyLoginPage()
        page.press_home_key()
        # time.sleep(2)
        # 再次激活进入和飞信app
        current_mobile().activate_app(app_id='com.chinasofti.rcs')
        # 点击进入通话会控页，
        callpage.click_back_to_call_631()
        current_mobile().set_network_status(0)
        time.sleep(1)
        mess.page_should_contain_text('当前网络不可用')
        # current_mobile().set_network_status(6)
        # time.sleep(2)
        # callpage.hang_up_hefeixin_call_631()

    def tearDown_test_call_wangqiong_0405(self):
        current_mobile().set_network_status(6)
        Preconditions.disconnect_mobile('Android-移动')

    @unittest.skip('悬浮窗无法抓取')
    def test_call_wangqiong_0495(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        # 网络正常
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        cp.click_free_call()
        callcontact = CalllogBannerPage()
        cmvp = MultiPartyVideoPage()
        cmvp.input_contact_search("15875537272")
        if cmvp.is_text_present('未知号码'):
            cmvp.click_text('未知号码')
        else:
            cmvp.click_text('测试人员2')
        cmvp.input_contact_search("13800138222")
        cmvp.click_text('未知号码')
        cmvp.click_tv_sure()
        # time.sleep(1)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()
        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 当出现系统通话页面，则进入手机home页
        callpage = CallPage()
        Flag = True
        i = 0
        while Flag:
            # time.sleep(1)
            if callpage.is_phone_in_calling_state():
                break
            elif i > 30:
                break
            else:
                i = i + 1
        # 回到手机主页面
        from pages import OneKeyLoginPage
        page = OneKeyLoginPage()
        page.press_home_key()
        # time.sleep(2)
        # 再次激活进入和飞信app
        current_mobile().activate_app(app_id='com.chinasofti.rcs')
        # 点击进入通话会控页，
        callpage.click_back_to_call_631()
        current_mobile().set_network_status(0)
        time.sleep(1)
        mess.page_should_contain_text('当前网络不可用，为管理通话成员状态，请连接wifi或启用VoLTE')
        # current_mobile().set_network_status(6)
        # time.sleep(2)
        # callpage.hang_up_hefeixin_call_631()

    def tearDown_test_call_wangqiong_0495(self):
        current_mobile().set_network_status(6)
        Preconditions.disconnect_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_zengxi_0001(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        # 网络正常
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        pad = cp.is_on_the_dial_pad()
        if not pad:
            cp.click_dial_pad()
            time.sleep(1)
            cp.click_one()
            cp.click_five()
            cp.click_eight()
            cp.click_seven()
            cp.click_five()
            cp.click_five()
            cp.click_three()
            cp.click_seven()
            cp.click_two()
            cp.click_seven()
            cp.click_two()
            time.sleep(1)
        cp.click_call_phone()
        cp.click_voice_call()
        time.sleep(1)
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        cp.click_voice_call_small()
        time.sleep(2)
        # Checkpoint 1、在消息列表页上方显示消息通知条        # 2、显示消息通知条和语音通话提示条
        self.assertTrue(mess.is_text_present('你正在语音通话'))
        mess.click_element_by_text('你正在语音通话')
        time.sleep(4)
        mess.is_toast_exist('通话结束')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_zengxi_0005(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        # 网络正常
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        cp.click_multi_party_video()
        cmvp = MultiPartyVideoPage()
        cmvp.input_contact_search("15875537272")
        if cmvp.is_text_present('未知号码'):
            cmvp.click_text('未知号码')
        else:
            cmvp.click_text('测试人员2')
        cmvp.click_tv_sure()
        time.sleep(1)
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        cp.click_video_call_small()
        time.sleep(2)
        # Checkpoint 1、在消息列表页上方显示消息通知条        # 2、显示消息通知条和语音通话提示条
        self.assertTrue(mess.is_text_present('你正在视频通话'))
        mess.click_element_by_text('你正在视频通话')
        time.sleep(4)
        mess.is_toast_exist('通话结束')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_zengxi_0009(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        # 网络正常
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        cp.click_multi_party_video()
        cmvp = MultiPartyVideoPage()
        cmvp.input_contact_search("15875537272")
        if cmvp.is_text_present('未知号码'):
            cmvp.click_text('未知号码')
        else:
            cmvp.click_text('测试人员2')
        cmvp.input_contact_search("13899138122")
        cmvp.click_text('未知号码')
        cmvp.click_tv_sure()
        time.sleep(1)
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        cp.click_more_video_call_small()
        time.sleep(2)
        # Checkpoint 1、在消息列表页上方显示消息通知条        # 2、显示消息通知条和语音通话提示条
        self.assertTrue(mess.is_text_present('你正在多方视频'))
        mess.click_element_by_text('你正在多方视频')
        time.sleep(4)
        mess.is_toast_exist('通话结束')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_zengxi_0013(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        # 网络正常
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        cp.click_free_call()
        callcontact = CalllogBannerPage()
        cmvp = MultiPartyVideoPage()
        cmvp.input_contact_search("15875537272")
        if cmvp.is_text_present('未知号码'):
            cmvp.click_text('未知号码')
        else:
            cmvp.click_text('测试人员2')
        cmvp.input_contact_search("13800138222")
        cmvp.click_text('未知号码')
        cmvp.click_tv_sure()
        time.sleep(1)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()
        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 当出现系统通话页面，则进入手机home页
        callpage = CallPage()
        Flag = True
        i = 0
        while Flag:
            time.sleep(1)
            if callpage.is_phone_in_calling_state():
                break
            elif i > 30:
                break
            else:
                i = i + 1
        # 回到手机主页面
        from pages import OneKeyLoginPage
        page = OneKeyLoginPage()
        page.press_home_key()
        time.sleep(2)
        # 再次激活进入和飞信app
        current_mobile().activate_app(app_id='com.chinasofti.rcs')
        time.sleep(3)
        self.assertTrue(mess.is_text_present('你正在飞信电话'))
        mess.click_element_by_text('你正在飞信电话')
        time.sleep(4)
        mess.is_toast_exist('通话结束')
        mess.hang_up_the_call()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_zengxi_0017(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        # 网络正常
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        pad = cp.is_on_the_dial_pad()
        if not pad:
            cp.click_dial_pad()
            time.sleep(1)
            cp.click_one()
            cp.click_five()
            cp.click_eight()
            cp.click_seven()
            cp.click_five()
            cp.click_five()
            cp.click_three()
            cp.click_seven()
            cp.click_two()
            cp.click_seven()
            cp.click_two()
            time.sleep(1)
        cp.click_call_phone()
        cp.click_voice_call()
        time.sleep(1)
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        cp.click_voice_call_small()
        time.sleep(2)
        # Checkpoint 1、在消息列表页上方显示消息通知条        # 2、显示消息通知条和语音通话提示条
        self.assertTrue(mess.is_text_present('你正在语音通话'))
        mess.click_element_by_text('你正在语音通话')
        time.sleep(2)
        self.assertTrue(cp.check_end_voice_call())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_zhenyishan_0112(self):
        """通话模块：当前勾选人数已有8人，继续勾选团队联系人，检查提示"""
        current_mobile().launch_app()
        Preconditions.create_contacts_if_not_exist_631(
            ["给个名片1, 13800138200", "给个名片2, 13800138300", "测试短信1, 13800138111", "测试短信2, 13800138112",
             "给个红包1, 13800138000", "联系人1, 18312345678", "联系人2, 18323456789", "联系人3, 13812345678", "联系人4, 13823456789"])

        # 1、当前为团队联系人选择页
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        cp.click_multi_party_video()

        ContactsSelector().select_local_contacts('给个名片1', '给个名片2', '测试短信1', '测试短信2', '给个红包1', '联系人1', '联系人2', '联系人3',
                                                 '联系人4')
        mess.is_toast_exist('最多只能选择8人')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_zhenyishan_0153(self):
        """分组群发/标签分组/群发消息：多方视频联系人选择器--点击任意群成员"""
        current_mobile().launch_app()
        Preconditions.create_contacts_if_not_exist_631(
            ["给个名片1, 13800138200", "给个名片2, 13800138300", "测试短信1, 13800138111", "测试短信2, 13800138112",
             "给个红包1, 13800138000", "联系人1, 18312345678", "联系人2, 18323456789", "联系人3, 13812345678", "联系人4, 13823456789"])
        # 1、已通过分组群发/标签分组/群发消息进入多方视频联系人选择器
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_label_grouping_631()
        labellist = LabelGroupingPage()
        time.sleep(2)
        if '测试分组Beta' not in labellist.get_label_grouping_names():
            labellist.create_group_631('测试分组Beta', '给个名片1', '给个名片2', '测试短信1', '测试短信2', '给个红包1', '联系人1', '联系人2', '联系人3',
                                       '联系人4')
        # Step 2.任意点击一存在多名成员的标签分组
        contactspage.click_element_by_text('测试分组Beta')
        # labellist.click_label_group('测试分组Beta')
        time.sleep(2)
        # 选择成员进行多方视频
        labellist.click_four_image_call()
        time.sleep(2)
        labellist.click_local_contacts('给个名片1', '给个名片2', '测试短信1', '测试短信2', '给个红包1', '联系人1', '联系人2', '联系人3', '联系人4')
        labellist.is_toast_exist('人数已达上限8人')
        labellist.click_back_by_android()
        labellist.click_four_image_call()
        labellist.page_should_contain_text('呼叫')
        labellist.click_local_contacts('测试短信1')
        labellist.page_should_contain_text('呼叫(1/8)')
        labellist.page_should_contain_text('信1')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_zhenyishan_0178(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        # 网络正常
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        cp.click_multi_party_video()
        cmvp = MultiPartyVideoPage()
        cmvp.input_contact_search("15875537272")
        if cmvp.is_text_present('未知号码'):
            cmvp.click_text('未知号码')
        else:
            cmvp.click_text('测试人员2')
        cmvp.input_contact_search("13899138122")
        cmvp.click_text('未知号码')
        cmvp.click_tv_sure()
        time.sleep(1)
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        time.sleep(1)
        cp.end_multi_video_phone()
        cp.is_type_hefeixin(0, '多方视频')
        # 进入详情页
        time.sleep(3)
        cp.click_ganggang_call_time()
        cp.click_mutil_call_again()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_zhenyishan_0183(self):
        """主叫多方视频管理界面，检查挂断按钮"""
        # 1、已成功发起多方视频
        # 2、当前为主叫多方视频管理界面
        mess = MessagePage()
        # Step 1、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        cp.click_multi_party_video()
        cmvp = MultiPartyVideoPage()
        cmvp.input_contact_search("15875537272")
        if cmvp.is_text_present('未知号码'):
            cmvp.click_text('未知号码')
        else:
            cmvp.click_text('测试人员2')
        cmvp.input_contact_search("13800138222")
        cmvp.click_text('未知号码')
        cmvp.click_tv_sure()
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        # Step 2、主叫方点击挂断按钮
        cmvp.click_end_video_call()
        cmvp.click_end_cancel()
        cmvp.page_should_contain_text('关闭摄像头')
        cmvp.click_end_video_call()
        cmvp.click_end_ok()
        time.sleep(3)
        cmvp.page_should_not_contain_text('关闭摄像头')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_zhenyishan_0186(self):
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
        if cmvp.is_text_present('未知号码'):
            cmvp.click_text('未知号码')
        else:
            cmvp.click_text('测试人员2')
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
        time.sleep(1)
        self.assertFalse(cmvp.is_enabled_tv_sure())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_zhenyishan_0191(self):
        """多方视频管理界面，检查添加联系人按钮"""
        current_mobile().launch_app()
        Preconditions.create_contacts_if_not_exist_631(
            ["给个名片1, 13800138200", "给个名片2, 13800138300", "测试短信1, 13800138111", "测试短信2, 13800138112",
             "给个红包1, 13800138000", "联系人1, 18312345678", "联系人2, 18323456789", "联系人3, 13812345678", "联系人4, 13823456789"])
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
        if cmvp.is_text_present('未知号码'):
            cmvp.click_text('未知号码')
        else:
            cmvp.click_text('测试人员2')
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
        LabelGroupingPage().click_local_contacts('给个名片1', '给个名片2', '测试短信1', '测试短信2', '给个红包1', '联系人1', '联系人2', '联系人3',
                                                 '联系人4')
        cmvp.is_toast_exist('人数已达上限8人')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_zhenyishan_0328(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        # 网络正常
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        pad = cp.is_on_the_dial_pad()
        if not pad:
            cp.click_dial_pad()
            time.sleep(1)
            cp.click_one()
            cp.click_five()
            cp.click_eight()
            cp.click_seven()
            cp.click_five()
            cp.click_five()
            cp.click_three()
            cp.click_seven()
            cp.click_two()
            cp.click_seven()
            cp.click_two()
            time.sleep(1)
        cp.click_call_phone()
        cp.click_voice_call()
        time.sleep(1)
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        time.sleep(1)

        # cp.click_call_cancel()
        # time.sleep(2)
        # cp.click_ganggang_call_time()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_zhenyishan_0382(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        # 网络正常
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        pad = cp.is_on_the_dial_pad()
        if not pad:
            cp.click_dial_pad()
            time.sleep(1)
            cp.click_one()
            cp.click_five()
            cp.click_eight()
            cp.click_seven()
            cp.click_five()
            cp.click_five()
            cp.click_three()
            cp.click_seven()
            cp.click_two()
            cp.click_seven()
            cp.click_two()
            time.sleep(1)
        cp.click_call_phone()
        cp.click_voice_call()
        # time.sleep(1)
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        # time.sleep(1)
        cp.hang_up_voice_call()
        time.sleep(2)
        cp.click_ganggang_call_time()
        cp.page_should_contain_text('语音通话')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_zhenyishan_0387(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_allinfo_if_not_exits('给个名片99', '13800138299', '中软国际', '软件工程师', 'test1234@163.com')

        # 网络正常
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        pad = cp.is_on_the_dial_pad()
        if not pad:
            cp.click_dial_pad()
            time.sleep(1)
            cp.click_one()
            cp.click_three()
            cp.click_eight()
            cp.click_zero()
            cp.click_zero()
            cp.click_one()
            cp.click_three()
            cp.click_eight()
            cp.click_two()
            cp.click_nine()
            cp.click_nine()
            time.sleep(1)
        cp.click_call_phone()
        cp.click_voice_call()
        time.sleep(1)
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        time.sleep(1)

        cp.click_call_cancel()
        time.sleep(2)
        cp.click_ganggang_call_time()
        cp.page_should_contain_text('中软国际')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_hanjiabin_0192(self):

        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        Preconditions.create_contacts_if_not_exist_631(["给个名片1, 13800138200", "给个名片2, 13800138300"])

        mess = MessagePage()
        singlechat = SingleChatPage()
        # Step 1.进入一对一聊天窗口
        mess.search_and_enter_631('给个名片1')
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        singlechat.click_more()
        singlechat.click_profile()

        selectcontact = SelectLocalContactsPage()
        send_card = Send_CardNamePage()
        # Checkpoint 进入到联系人选择器页面
        selectcontact.wait_for_page_load()
        # Step 任意选中一个联系人的名片，发送出去
        ContactsSelector().click_local_contacts('给个名片2')
        time.sleep(2)
        send_card.click_share_btn()
        send_card.press_mess('给个名片2')
        singlechat.select_collect_item()
        mess.click_back_by_android(times=3)
        mess.click_me_icon()
        me = MePage()
        me.click_collection()
        mess.is_text_present('[名片]给个名片2的个人名片')

    @staticmethod
    def setUp_test_msg_huangcaizui_D_0112():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 1、在我-设置-消息通知页面将接收消息通知权限关闭
        mess = MessagePage()
        mess.click_me_icon()
        me = MePage()
        me.wait_for_head_load()
        me.click_setting_menu()
        set = SettingPage()
        set.click_message_setting()
        Mess_notice_set = MessageNoticeSettingPage()
        Mess_notice_set.get_new_message_notice_setting()
        time.sleep(2)
        Mess_notice_set.new_message_switch_bar_turn_off()
        CallPage().click_back_by_android(times=3)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0112(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        # 网络正常
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        pad = cp.is_on_the_dial_pad()
        if not pad:
            cp.click_dial_pad()
            time.sleep(1)
            cp.click_one()
            cp.click_five()
            cp.click_eight()
            cp.click_seven()
            cp.click_five()
            cp.click_five()
            cp.click_three()
            cp.click_seven()
            cp.click_two()
            cp.click_seven()
            cp.click_two()
            time.sleep(1)
        cp.click_call_phone()
        cp.click_voice_call()
        time.sleep(1)
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        cp.click_voice_call_small()
        time.sleep(2)
        # Checkpoint 1、在消息列表页上方显示消息通知条        # 2、显示消息通知条和语音通话提示条
        self.assertTrue(mess.is_text_present('开启消息通知，不错过重要消息提醒'))
        self.assertTrue(mess.is_text_present('你正在语音通话'))

    @staticmethod
    def setUp_test_msg_huangcaizui_D_0113():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 1、在我-设置-消息通知页面将接收消息通知权限关闭
        mess = MessagePage()
        mess.click_me_icon()
        me = MePage()
        me.wait_for_head_load()
        me.click_setting_menu()
        set = SettingPage()
        set.click_message_setting()
        Mess_notice_set = MessageNoticeSettingPage()
        Mess_notice_set.get_new_message_notice_setting()
        time.sleep(2)
        Mess_notice_set.new_message_switch_bar_turn_off()
        CallPage().click_back_by_android(times=3)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0113(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        # 网络正常
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        cp.click_multi_party_video()
        cmvp = MultiPartyVideoPage()
        cmvp.input_contact_search("15875537272")
        if cmvp.is_text_present('未知号码'):
            cmvp.click_text('未知号码')
        else:
            cmvp.click_text('测试人员2')
        cmvp.click_tv_sure()
        time.sleep(1)
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        cp.click_video_call_small()
        time.sleep(2)
        # Checkpoint 1、在消息列表页上方显示消息通知条        # 2、显示消息通知条和语音通话提示条
        self.assertTrue(mess.is_text_present('开启消息通知，不错过重要消息提醒'))
        self.assertTrue(mess.is_text_present('你正在视频通话'))

    @staticmethod
    def setUp_test_msg_huangcaizui_D_0114():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 1、在我-设置-消息通知页面将接收消息通知权限关闭
        mess = MessagePage()
        mess.click_me_icon()
        me = MePage()
        me.wait_for_head_load()
        me.click_setting_menu()
        set = SettingPage()
        set.click_message_setting()
        Mess_notice_set = MessageNoticeSettingPage()
        Mess_notice_set.get_new_message_notice_setting()
        time.sleep(2)
        Mess_notice_set.new_message_switch_bar_turn_off()
        CallPage().click_back_by_android(times=3)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0114(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        # 网络正常
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        cp.click_multi_party_video()
        cmvp = MultiPartyVideoPage()
        cmvp.input_contact_search("15875537272")
        if cmvp.is_text_present('未知号码'):
            cmvp.click_text('未知号码')
        else:
            cmvp.click_text('测试人员2')
        cmvp.input_contact_search("13899138122")
        cmvp.click_text('未知号码')
        cmvp.click_tv_sure()
        time.sleep(1)
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        cp.click_more_video_call_small()
        time.sleep(2)
        # Checkpoint 1、在消息列表页上方显示消息通知条        # 2、显示消息通知条和语音通话提示条
        self.assertTrue(mess.is_text_present('开启消息通知，不错过重要消息提醒'))
        self.assertTrue(mess.is_text_present('你正在多方视频'))

    @staticmethod
    def setUp_test_msg_huangcaizui_D_0115():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 1、在我-设置-消息通知页面将接收消息通知权限关闭
        mess = MessagePage()
        mess.click_me_icon()
        me = MePage()
        me.wait_for_head_load()
        me.click_setting_menu()
        set = SettingPage()
        set.click_message_setting()
        Mess_notice_set = MessageNoticeSettingPage()
        Mess_notice_set.get_new_message_notice_setting()
        time.sleep(2)
        Mess_notice_set.new_message_switch_bar_turn_off()
        CallPage().click_back_by_android(times=3)

    @unittest.skip('悬浮窗无法抓取')
    def test_msg_huangcaizui_D_0115(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        # 网络正常
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        cp.click_free_call()
        callcontact = CalllogBannerPage()
        cmvp = MultiPartyVideoPage()
        cmvp.input_contact_search("15875537272")
        if cmvp.is_text_present('未知号码'):
            cmvp.click_text('未知号码')
        else:
            cmvp.click_text('测试人员2')
        cmvp.input_contact_search("13899138122")
        cmvp.click_text('未知号码')
        cmvp.click_tv_sure()
        time.sleep(1)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()
        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 当出现系统通话页面，则进入手机home页
        callpage = CallPage()
        Flag = True
        i = 0
        while Flag:
            time.sleep(1)
            if callpage.is_phone_in_calling_state():
                break
            elif i > 30:
                break
            else:
                i = i + 1
        # 回到手机主页面
        from pages import OneKeyLoginPage
        page = OneKeyLoginPage()
        page.press_home_key()
        time.sleep(2)
        # 再次激活进入和飞信app
        current_mobile().activate_app(app_id='com.chinasofti.rcs')
        time.sleep(3)
        self.assertTrue(mess.is_text_present('开启消息通知，不错过重要消息提醒'))
        self.assertTrue(mess.is_text_present('你正在飞信电话'))
        # 点击进入通话会控页，
        callpage.click_back_to_call_631()
        time.sleep(2)
        callpage.hang_up_hefeixin_call_631()

    @staticmethod
    def setUp_test_msg_huangcaizui_D_0120():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 1、在我-设置-消息通知页面将接收消息通知权限关闭
        mess = MessagePage()
        mess.click_me_icon()
        me = MePage()
        me.wait_for_head_load()
        me.click_setting_menu()
        set = SettingPage()
        set.click_message_setting()
        Mess_notice_set = MessageNoticeSettingPage()
        Mess_notice_set.get_new_message_notice_setting()
        time.sleep(2)
        Mess_notice_set.new_message_switch_bar_turn_on()
        CallPage().click_back_by_android(times=3)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0120(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        # 网络正常
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        pad = cp.is_on_the_dial_pad()
        if not pad:
            cp.click_dial_pad()
            time.sleep(1)
            cp.click_one()
            cp.click_five()
            cp.click_eight()
            cp.click_seven()
            cp.click_five()
            cp.click_five()
            cp.click_three()
            cp.click_seven()
            cp.click_two()
            cp.click_seven()
            cp.click_two()
            time.sleep(1)
        cp.click_call_phone()
        cp.click_voice_call()
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        cp.click_voice_call_small()
        mess.click_me_icon()
        me = MePage()
        me.click_setting_menu_631()
        set = SettingPage()
        set.click_message_setting()
        Mess_notice_set = MessageNoticeSettingPage()
        Mess_notice_set.get_new_message_notice_setting()
        Mess_notice_set.new_message_switch_bar_turn_off()
        CallPage().click_back_by_android(times=3)
        mess.open_message_page()
        # Checkpoint 1、在消息列表页上方显示消息通知条        # 2、显示消息通知条和语音通话提示条
        self.assertTrue(mess.is_text_present('你正在语音通话'))
        self.assertTrue(mess.is_text_present('开启消息通知，不错过重要消息提醒'))

    @staticmethod
    def setUp_test_msg_huangcaizui_D_0121():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 1、在我-设置-消息通知页面将接收消息通知权限关闭
        mess = MessagePage()
        mess.click_me_icon()
        me = MePage()
        me.wait_for_head_load()
        me.click_setting_menu()
        set = SettingPage()
        set.click_message_setting()
        Mess_notice_set = MessageNoticeSettingPage()
        Mess_notice_set.get_new_message_notice_setting()
        time.sleep(2)
        Mess_notice_set.new_message_switch_bar_turn_on()
        CallPage().click_back_by_android(times=3)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0121(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        # 网络正常
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        cp.click_multi_party_video()
        cmvp = MultiPartyVideoPage()
        cmvp.input_contact_search("15875537272")
        if cmvp.is_text_present('未知号码'):
            cmvp.click_text('未知号码')
        else:
            cmvp.click_text('测试人员2')
        cmvp.click_tv_sure()
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        cp.click_video_call_small()
        mess.click_me_icon()
        me = MePage()
        me.click_setting_menu_631()
        set = SettingPage()
        set.click_message_setting()
        Mess_notice_set = MessageNoticeSettingPage()
        Mess_notice_set.get_new_message_notice_setting()
        Mess_notice_set.new_message_switch_bar_turn_off()
        CallPage().click_back_by_android(times=3)
        mess.open_message_page()
        # Checkpoint 1、在消息列表页上方显示消息通知条        # 2、显示消息通知条和语音通话提示条
        self.assertTrue(mess.is_text_present('你正在视频通话'))
        self.assertTrue(mess.is_text_present('开启消息通知，不错过重要消息提醒'))

    @staticmethod
    def setUp_test_msg_huangcaizui_D_0122():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 1、在我-设置-消息通知页面将接收消息通知权限关闭
        mess = MessagePage()
        mess.click_me_icon()
        me = MePage()
        me.wait_for_head_load()
        me.click_setting_menu()
        set = SettingPage()
        set.click_message_setting()
        Mess_notice_set = MessageNoticeSettingPage()
        Mess_notice_set.get_new_message_notice_setting()
        time.sleep(2)
        Mess_notice_set.new_message_switch_bar_turn_on()
        CallPage().click_back_by_android(times=3)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0122(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        # 网络正常
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        cp.click_multi_party_video()
        cmvp = MultiPartyVideoPage()
        cmvp.input_contact_search("15875537272")
        if cmvp.is_text_present('未知号码'):
            cmvp.click_text('未知号码')
        else:
            cmvp.click_text('测试人员2')
        cmvp.input_contact_search("13899138122")
        cmvp.click_text('未知号码')
        cmvp.click_tv_sure()
        # time.sleep(1)
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        cp.click_more_video_call_small()
        mess.click_me_icon()
        me = MePage()
        me.click_setting_menu_631()
        set = SettingPage()
        set.click_message_setting()
        Mess_notice_set = MessageNoticeSettingPage()
        Mess_notice_set.get_new_message_notice_setting()
        Mess_notice_set.new_message_switch_bar_turn_off()
        CallPage().click_back_by_android(times=3)
        mess.open_message_page()
        # Checkpoint 1、在消息列表页上方显示消息通知条        # 2、显示消息通知条和语音通话提示条
        self.assertTrue(mess.is_text_present('你正在多方视频'))
        self.assertTrue(mess.is_text_present('开启消息通知，不错过重要消息提醒'))

    @staticmethod
    def setUp_test_msg_huangcaizui_D_0123():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 1、在我-设置-消息通知页面将接收消息通知权限关闭
        mess = MessagePage()
        mess.click_me_icon()
        me = MePage()
        me.wait_for_head_load()
        me.click_setting_menu()
        set = SettingPage()
        set.click_message_setting()
        Mess_notice_set = MessageNoticeSettingPage()
        Mess_notice_set.get_new_message_notice_setting()
        time.sleep(2)
        Mess_notice_set.new_message_switch_bar_turn_on()
        CallPage().click_back_by_android(times=3)

    @unittest.skip('悬浮窗无法抓取')
    def test_msg_huangcaizui_D_0123(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        # 网络正常
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        cp.click_free_call()
        callcontact = CalllogBannerPage()
        cmvp = MultiPartyVideoPage()
        cmvp.input_contact_search("15875537272")
        if cmvp.is_text_present('未知号码'):
            cmvp.click_text('未知号码')
        else:
            cmvp.click_text('测试人员2')
        cmvp.input_contact_search("13899138122")
        cmvp.click_text('未知号码')
        cmvp.click_tv_sure()
        # time.sleep(1)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()
        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 当出现系统通话页面，则进入手机home页
        callpage = CallPage()
        Flag = True
        i = 0
        while Flag:
            # time.sleep(1)
            if callpage.is_phone_in_calling_state():
                break
            elif i > 30:
                break
            else:
                i = i + 1
        # 回到手机主页面
        from pages import OneKeyLoginPage
        page = OneKeyLoginPage()
        page.press_home_key()
        # time.sleep(2)
        # 再次激活进入和飞信app
        current_mobile().activate_app(app_id='com.chinasofti.rcs')
        mess.click_me_icon()
        me = MePage()
        me.click_setting_menu_631()
        set = SettingPage()
        set.click_message_setting()
        Mess_notice_set = MessageNoticeSettingPage()
        Mess_notice_set.get_new_message_notice_setting()
        Mess_notice_set.new_message_switch_bar_turn_off()
        CallPage().click_back_by_android(times=3)
        mess.open_message_page()
        self.assertTrue(mess.is_text_present('你正在飞信电话'))
        self.assertTrue(mess.is_text_present('开启消息通知，不错过重要消息提醒'))
        # 点击进入通话会控页，
        # callpage.click_back_to_call_631()
        # time.sleep(1)
        # callpage.hang_up_hefeixin_call_631()

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0259():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        Preconditions.create_contacts_if_not_exist_631(["给个名片1, 13800138200", "给个名片2, 13800138300"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0259(self):
        """验证在我的电脑-查找聊天内容-文件页面点击打开已下载的不可预览文件-右上角的更多按钮-转发时是否正常"""
        # 1、当前在我的电脑-查找聊天内容-文件页面
        # 2、当前页面有已下载的不可预览文件
        # 3、网络异常
        MessagePage().search_and_enter_631('给个名片1')
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        single_chat = SingleChatPage()
        single_chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        time.sleep(2)
        single_chat.set_network_status(1)
        file_name = '录制.txt'
        path = 'aaaresource'
        single_chat.send_file_messages_631(path, file_name)
        time.sleep(2)
        single_chat.click_mess_text('录制.txt')
        time.sleep(3)
        single_chat.page_should_contain_text('录制.txt')

    def tearDown_test_msg_weifenglian_1V1_0259(self):
        SingleChatPage().set_network_status(6)
        Preconditions.disconnect_mobile('Android-移动')

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0268():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        Preconditions.create_contacts_if_not_exist_631(["给个名片1, 13800138200", "给个名片2, 13800138300"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0268(self):
        """验证转发文件到当前单聊会话窗口，文件发送失败的重发按钮，点击确定时是否正常发送"""
        # 1、当前在单聊会话窗口页面
        # 2、当前会话页面有发送失败的文件
        MessagePage().search_and_enter_631('给个名片1')
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()

        single_chat = SingleChatPage()
        single_chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        time.sleep(2)
        single_chat.set_network_status(1)
        file_name = '录制.txt'
        path = 'aaaresource'
        single_chat.send_file_messages_631(path, file_name)
        time.sleep(2)
        single_chat.click_msg_send_failed_button(0)
        single_chat.click_sure()

    def tearDown_test_msg_weifenglian_1V1_0268(self):
        SingleChatPage().set_network_status(6)
        Preconditions.disconnect_mobile('Android-移动')

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0274():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist_631(["测试短信1, 13800138111"])
        mess = MessagePage()
        # Step 进入群聊页面
        mess.search_and_enter_631('测试短信1')
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_tips_display():
            chatdialog.accept_and_close_tips_alert()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0274(self):
        """验证在单聊会话窗口点击打开已下载的可预览文件-右上角的更多按钮-转发时是否正常"""
        # 1、当前在单聊会话窗口页面
        # 2、当前会话窗口有已下载的可预览文件
        # 3、网络正常
        mess = MessagePage()
        single_chat = SingleChatPage()
        single_chat.wait_for_page_load()
        single_chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        time.sleep(2)
        file_name = '2018-11-09 11-06-18-722582.log'
        path = 'aaaresource'
        single_chat.send_file_messages_631(path, file_name)
        single_chat.re_send_file_messages(file_name)

    @staticmethod
    def setUp_test_msg_weifenglian_PC_0233():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        mess = MessagePage()
        mess.click_me_icon()
        me = MePage()
        me.wait_for_head_load()
        me.click_setting_menu()
        set = SettingPage()
        set.click_message_setting()
        Mess_notice_set = MessageNoticeSettingPage()
        Mess_notice_set.get_new_message_notice_setting()
        time.sleep(2)
        Mess_notice_set.new_message_switch_bar_turn_on()
        CallPage().click_back_by_android(times=3)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0233(self):
        """验证在我的电脑-查找聊天内容-文件页面点击未下载且不可直接预览的文件-下载完成后，点击右上角的更多按钮-收藏时是否正常"""
        # 1、当前在我的电脑-查找聊天内容-文件页面-已下载完成的文件详情页
        # 2、网络正常
        mess = MessagePage()
        mess.open_message_page()
        Preconditions.enter_my_computer_page()
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0237(self):
        """验证在我的电脑-查找聊天内容-文件页面点击未下载且不可直接预览的文件-下载完成后，点击右上角的更多按钮-收藏时是否正常"""
        Preconditions.enter_my_computer_page()
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
        single_chat.assert_transmit_record_file()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0238(self):
        """验证在我的电脑-查找聊天内容-文件页面点击未下载且不可直接预览的文件-下载完成后，点击右上角的更多按钮-收藏时是否正常"""
        Preconditions.enter_my_computer_page()
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0240(self):
        """验证在我的电脑-查找聊天内容-文件页面点击未下载且不可直接预览的文件-下载完成后，点击右上角的更多按钮-收藏时是否正常"""
        Preconditions.enter_my_computer_page()
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
        single_chat.other_app_open_file()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0243(self):
        """验证在我的电脑-查找聊天内容-文件页面点击未下载且不可直接预览的文件-下载完成后，点击右上角的更多按钮-收藏时是否正常"""
        Preconditions.enter_my_computer_page()
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
        single_chat.assert_transmit_record_file()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0244(self):
        """验证在我的电脑-查找聊天内容-文件页面点击未下载且不可直接预览的文件-下载完成后，点击右上角的更多按钮-收藏时是否正常"""
        Preconditions.enter_my_computer_page()
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0248(self):
        """验证在我的电脑-查找聊天内容-文件页面点击未下载且可直接预览的文件-下载完成后，点击右上角的更多按钮-转发时是否正常"""
        Preconditions.enter_my_computer_page()
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
        single_chat.assert_transmit_record_file()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0249(self):
        """验证在我的电脑-查找聊天内容-文件页面点击未下载且不可直接预览的文件-下载完成后，点击右上角的更多按钮-收藏时是否正常"""
        Preconditions.enter_my_computer_page()
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0251(self):
        """验证在我的电脑-查找聊天内容-文件页面点击未下载且不可直接预览的文件-下载完成后，点击右上角的更多按钮-收藏时是否正常"""
        Preconditions.enter_my_computer_page()
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
        single_chat.other_app_open_file()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0261(self):
        """验证在我的电脑-查找聊天内容-文件页面点击打开已下载的可预览文件时，右上角是否新增更多功能入口"""
        Preconditions.enter_my_computer_page()
        # 1、当前在我的电脑-查找聊天内容-文件页面
        # 2、当前页面有已下载的可预览文件
        # 3、网络正常
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
        single_chat.assert_id_menu_more()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0310(self):
        """验证在我的电脑-查找聊天内容-文件页面点击打开已下载的可预览文件时，右上角是否新增更多功能入口"""
        Preconditions.enter_my_computer_page()
        # 1、当前在我的电脑-查找聊天内容-文件页面
        # 2、当前页面有已下载的可预览文件
        # 3、网络异常
        single_chat = SingleChatPage()
        single_chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        time.sleep(2)
        file_name = '录制.txt'
        path = 'aaaresource'
        single_chat.send_file_messages_631(path, file_name)
        time.sleep(3)
        single_chat.set_network_status(1)
        single_chat.click_setting()
        single_chat.search_chat_record_file(file_name)
        single_chat.assert_id_menu_more()

    def tearDown_test_msg_weifenglian_PC_0310(self):
        SingleChatPage().set_network_status(6)
        Preconditions.disconnect_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0314(self):
        """验证在我的电脑-查找聊天内容-文件页面点击未下载且不可直接预览的文件-下载完成后，点击右上角的更多按钮-收藏时是否正常"""
        Preconditions.enter_my_computer_page()
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
        time.sleep(3)
        single_chat.set_network_status(1)
        single_chat.click_setting()
        single_chat.search_chat_record_file(file_name)
        single_chat.assert_collect_record_file()

    def tearDown_test_msg_weifenglian_PC_0314(self):
        SingleChatPage().set_network_status(6)
        Preconditions.disconnect_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0315(self):
        """验证在我的电脑-查找聊天内容-文件页面点击打开已下载的可预览文件-右上角的更多按钮-其他应用打开时是否正常"""
        Preconditions.enter_my_computer_page()
        # 1、当前在我的电脑-查找聊天内容-文件页面
        # 2、当前页面有已下载的可预览文件
        # 3、网络异常
        single_chat = SingleChatPage()
        single_chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        time.sleep(2)
        file_name = '录制.txt'
        path = 'aaaresource'
        single_chat.send_file_messages_631(path, file_name)
        time.sleep(3)
        single_chat.set_network_status(1)
        single_chat.click_setting()
        single_chat.search_chat_record_file(file_name)
        single_chat.other_app_open_file()

    def tearDown_test_msg_weifenglian_PC_0315(self):
        SingleChatPage().set_network_status(6)
        Preconditions.disconnect_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0320(self):
        """验证在我的电脑-查找聊天内容-文件页面点击打开已下载的不可预览文件-右上角的更多按钮-转发时是否正常"""
        Preconditions.enter_my_computer_page()
        # 1、当前在我的电脑-查找聊天内容-文件页面
        # 2、当前页面有已下载的不可预览文件
        # 3、网络异常
        single_chat = SingleChatPage()
        single_chat.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        time.sleep(2)
        file_name = '录制.txt'
        path = 'aaaresource'
        single_chat.send_file_messages_631(path, file_name)
        time.sleep(3)
        single_chat.set_network_status(1)
        single_chat.click_setting()
        single_chat.search_chat_record_file(file_name)
        single_chat.assert_transmit_record_file()

    def tearDown_test_msg_weifenglian_PC_0320(self):
        SingleChatPage().set_network_status(6)
        Preconditions.disconnect_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0321(self):
        """验证在我的电脑-查找聊天内容-文件页面点击未下载且不可直接预览的文件-下载完成后，点击右上角的更多按钮-收藏时是否正常"""
        Preconditions.enter_my_computer_page()
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
        time.sleep(3)
        single_chat.set_network_status(1)
        single_chat.click_setting()
        single_chat.search_chat_record_file(file_name)
        single_chat.assert_collect_record_file()

    def tearDown_test_msg_weifenglian_PC_0321(self):
        SingleChatPage().set_network_status(6)
        Preconditions.disconnect_mobile('Android-移动')

    @staticmethod
    def setUp_test_msg_xiaoliping_A_0006():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
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
        groupset.click_back()
        CallPage().click_back_by_android(times=2)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoliping_A_0006(self):
        """扫描已有群二维码"""
        # 1、网络正常
        # 2、已登录客户端
        # 3、当前在消息列表界面
        # 4、群二维码（已在群聊中）
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_take_a_scan()
        mess.click_enter_photo()
        mess.click_qecode_photo()
        GroupChatPage().wait_for_page_load()

    @staticmethod
    def setUp_test_msg_xiaoliping_A_0009():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
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
