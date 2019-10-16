from pages.me.MeViewUserProfile import MeViewUserProfilePage

from pages.message.Send_CardName import Send_CardNamePage
import random
from pages.components import ChatNoticeDialog, ContactsSelector, BaseChatPage
from pages.call.multipartycall import MultipartyCallPage
from pages.message.FreeMsg import FreeMsgPage
import os
import time

from appium.webdriver.common.mobileby import MobileBy
from dataproviders import contact2
from preconditions.BasePreconditions import LoginPreconditions, WorkbenchPreconditions
from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from settings import PROJECT_PATH


class Preconditions(WorkbenchPreconditions):
    """前置条件"""

    @staticmethod
    def enter_group_chat_page(name):
        """进入群聊聊天会话页面"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击发起群聊
        mp.click_group_chat()
        scg = SelectContactsPage()
        times = 15
        n = 0
        # 重置应用时需要再次点击才会出现选择一个群
        while n < times:
            # 等待选择联系人页面加载
            flag = scg.wait_for_page_load()
            if not flag:
                scg.click_back()
                time.sleep(2)
                mp.click_add_icon()
                mp.click_group_chat()
            else:
                break
            n = n + 1
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name(name)
        gcp = GroupChatPage()
        gcp.wait_for_page_load()

    @staticmethod
    def make_already_have_my_group(reset=False):
        """确保有群，没有群则创建群名为mygroup+电话号码后4位的群"""
        # 消息页面
        Preconditions.make_already_in_message_page(reset)
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        times = 15
        n = 0
        # 重置应用时需要再次点击才会出现选择一个群
        while n < times:
            flag = sc.wait_for_page_load()
            if not flag:
                sc.click_back()
                time.sleep(2)
                mess.click_add_icon()
                mess.click_group_chat()
                sc = SelectContactsPage()
            else:
                break
            n = n + 1
        time.sleep(3)
        sc.click_select_one_group()
        # 群名
        group_name = Preconditions.get_group_chat_name()
        # 获取已有群名
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        time.sleep(2)
        sog.input_search_keyword(group_name)
        time.sleep(2)
        if sog.is_element_exit("群聊名"):
            current_mobile().back()
            time.sleep(2)
            current_mobile().back()
            return
        current_mobile().back()
        time.sleep(2)
        current_mobile().back()
        sog.click_back()
        time.sleep(2)
        sc.click_back()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 从本地联系人中选择成员创建群
        sc.click_local_contacts()
        time.sleep(2)
        slc = SelectLocalContactsPage()
        a = 0
        names = {}
        while a < 3:
            names = slc.get_contacts_name()
            num = len(names)
            if not names:
                raise AssertionError("No contacts, please add contacts in address book.")
            if num == 1:
                sog.page_up()
                a += 1
                if a == 3:
                    raise AssertionError("联系人只有一个，请再添加多个不同名字联系人组成群聊")
            else:
                break
        # 选择成员
        for name in names:
            slc.select_one_member_by_name(name)
        slc.click_sure()
        # 创建群
        cgnp = CreateGroupNamePage()
        cgnp.input_group_name(group_name)
        cgnp.click_sure()
        # 等待群聊页面加载
        GroupChatPage().wait_for_page_load()

    @staticmethod
    def get_group_chat_name():
        """获取群名"""
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "ag" + phone_number[-4:]
        return group_name

    @staticmethod
    def make_already_in_one_key_login_page():
        """已经进入一键登录页"""
        # 如果当前页面已经是一键登录页，不做任何操作
        one_key = OneKeyLoginPage()
        if one_key.is_on_this_page():
            return

        # 如果当前页不是引导页第一页，重新启动app
        guide_page = GuidePage()
        if not guide_page.is_on_the_first_guide_page():
            # current_mobile().launch_app()
            current_mobile().reset_app()
            guide_page.wait_for_page_load(20)

        # 跳过引导页
        guide_page.wait_for_page_load(30)
        # guide_page.swipe_to_the_second_banner()
        # guide_page.swipe_to_the_third_banner()
        # current_mobile().hide_keyboard_if_display()
        guide_page.click_start_the_experience()

        # 点击权限列表页面的确定按钮
        permission_list = PermissionListPage()
        # permission_list.click_submit_button()
        permission_list.go_permission()
        permission_list.click_permission_button()
        one_key.wait_for_page_load(30)

    @staticmethod
    def login_by_one_key_login():
        """
        从一键登录页面登录
        :return:
        """
        # 等待号码加载完成后，点击一键登录
        one_key = OneKeyLoginPage()
        one_key.wait_for_page_load()
        # one_key.wait_for_tell_number_load(60)
        one_key.click_one_key_login()
        # if one_key.have_read_agreement_detail():
        #     one_key.click_read_agreement_detail()
        #     # 同意协议
        #     agreement = AgreementDetailPage()
        #     agreement.click_agree_button()
        agreement = AgreementDetailPage()
        time.sleep(1)
        agreement.click_agree_button()
        # 等待消息页
        message_page = MessagePage()
        message_page.wait_login_success(60)

    @staticmethod
    def public_send_file(file_type):
        """选择指定类型文件发送"""
        # 1、在当前聊天会话页面，点击更多富媒体的文件按钮
        chat = GroupChatPage()
        chat.wait_for_page_load()
        chat.click_more()
        # 2、点击本地文件
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        # 3、选择任意文件，点击发送按钮
        local_file = ChatSelectLocalFilePage()
        # 没有预置文件，则上传
        flag = local_file.push_preset_file()
        if flag:
            local_file.click_back()
            csf.click_local_file()
        # 进入预置文件目录，选择文件发送
        local_file.click_preset_file_dir()
        file = local_file.select_file(file_type)
        if file:
            local_file.click_send()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        chat.wait_for_page_load()

    @staticmethod
    def delete_record_group_chat():
        # 删除聊天记录
        scp = GroupChatPage()
        if scp.is_on_this_page():
            scp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 点击删除聊天记录
            gcsp.click_clear_chat_record()
            gcsp.wait_clear_chat_record_confirmation_box_load()
            # 点击确认
            gcsp.click_determine()
            time.sleep(3)
            # if not gcsp.is_toast_exist("聊天记录清除成功"):
            #     raise AssertionError("没有聊天记录清除成功弹窗")
            # 点击返回群聊页面
            gcsp.click_back()
            time.sleep(2)
            # 判断是否返回到群聊页面
            if not scp.is_on_this_page():
                raise AssertionError("没有返回到群聊页面")
        else:
            try:
                raise AssertionError("没有返回到群聊页面，无法删除记录")
            except AssertionError as e:
                raise e

    @staticmethod
    def build_one_new_group(group_name):
        """新建一个指定名称的群，如果已存在，不建群"""
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        times = 15
        n = 0
        # 重置应用时需要再次点击才会出现选择一个群
        while n < times:
            flag = sc.wait_for_page_load()
            if not flag:
                sc.click_back()
                time.sleep(2)
                mess.click_add_icon()
                mess.click_group_chat()
                sc = SelectContactsPage()
            else:
                break
            n = n + 1
        time.sleep(2)
        sc.click_select_one_group()
        # 群名
        # group_name = Preconditions.get_group_chat_name()
        # 获取已有群名
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        time.sleep(2)
        sog.input_search_keyword(group_name)
        time.sleep(2)
        if sog.is_element_exit("群聊名"):
            current_mobile().back()
            time.sleep(2)
            current_mobile().back()
            if not mess.is_on_this_page():
                current_mobile().back()
                time.sleep(2)
                current_mobile().back()
            return
        current_mobile().back()
        time.sleep(2)
        current_mobile().back()
        if not mess.is_on_this_page():
            current_mobile().back()
            time.sleep(2)
            current_mobile().back()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 从本地联系人中选择成员创建群
        sc.click_local_contacts()
        time.sleep(2)
        slc = SelectLocalContactsPage()
        a = 0
        names = {}
        while a < 3:
            names = slc.get_contacts_name()
            num = len(names)
            if not names:
                raise AssertionError("No contacts, please add contacts in address book.")
            if num == 1:
                sog.page_up()
                a += 1
                if a == 3:
                    raise AssertionError("联系人只有一个，请再添加多个不同名字联系人组成群聊")
            else:
                break
        # 选择成员
        for name in names:
            slc.select_one_member_by_name(name)
        slc.click_sure()
        # 创建群
        cgnp = CreateGroupNamePage()
        cgnp.input_group_name(group_name)
        cgnp.click_sure()
        # 等待群聊页面加载
        GroupChatPage().wait_for_page_load()
        GroupChatPage().click_back()

    @staticmethod
    def make_in_message_page(moible_param, reset=False):
        """确保应用在消息页面"""
        Preconditions.select_mobile(moible_param, reset)
        current_mobile().hide_keyboard_if_display()
        time.sleep(1)
        # 如果在消息页，不做任何操作
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        # 进入一键登录页
        Preconditions.make_already_in_one_key_login_page()
        #  从一键登录页面登录
        Preconditions.login_by_one_key_login()

    @staticmethod
    def build_one_new_group_with_number(puhone_number, group_name):
        """新建一个指定成员和名称的群，如果已存在，不建群"""
        # 消息页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        times = 15
        n = 0
        # 重置应用时需要再次点击才会出现选择一个群
        while n < times:
            flag = sc.wait_for_page_load()
            if not flag:
                sc.click_back()
                time.sleep(2)
                mess.click_add_icon()
                mess.click_group_chat()
                sc = SelectContactsPage()
            else:
                break
            n = n + 1
        time.sleep(3)
        sc.click_select_one_group()
        # 群名
        # group_name = Preconditions.get_group_chat_name()
        # 获取已有群名
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        time.sleep(2)
        sog.input_search_keyword(group_name)
        time.sleep(2)
        if sog.is_element_exit("群聊名"):
            current_mobile().back()
            time.sleep(2)
            current_mobile().back()
            return True
        current_mobile().back()
        time.sleep(2)
        current_mobile().back()
        current_mobile().back()
        time.sleep(2)
        current_mobile().back()
        time.sleep(2)
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 添加指定电话成员
        time.sleep(2)
        sc.input_search_keyword(puhone_number)
        time.sleep(2)
        sog.click_text("tel")
        time.sleep(2)
        # 从本地联系人中选择成员创建群
        sc.click_local_contacts()
        time.sleep(2)
        slc = SelectLocalContactsPage()
        SelectContactsPage().click_one_contact_631("飞信电话")
        slc.click_sure()
        # 创建群
        cgnp = CreateGroupNamePage()
        cgnp.input_group_name(group_name)
        cgnp.click_sure()
        # 等待群聊页面加载
        GroupChatPage().wait_for_page_load()
        return False

    @staticmethod
    def get_group_chat_name_double():
        """获取多人群名"""
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "多机" + phone_number[-4:]
        return group_name

    @staticmethod
    def go_to_group_double(group_name):
        """从消息列表进入双机群聊，前提：已经存在双机群聊"""
        mess = MessagePage()
        mess.wait_for_page_load()
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        times = 15
        n = 0
        # 重置应用时需要再次点击才会出现选择一个群
        while n < times:
            flag = sc.wait_for_page_load()
            if not flag:
                sc.click_back()
                time.sleep(2)
                mess.click_add_icon()
                mess.click_group_chat()
                sc = SelectContactsPage()
            else:
                break
            n = n + 1
        time.sleep(3)
        sc.click_select_one_group()
        # # 群名
        # group_name = Preconditions.get_group_chat_name_double()
        # 获取已有群名
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        time.sleep(2)
        sog.input_search_keyword(group_name)
        time.sleep(2)
        if not sog.is_element_exit("群聊名"):
            raise AssertionError("没有找到双机群聊，请确认是否创建")
        sog.click_element_("群聊名")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()

    @staticmethod
    def change_mobile(moible_param):
        """转换设备连接并且确保在消息列表页面"""
        Preconditions.select_mobile(moible_param)
        current_mobile().hide_keyboard_if_display()
        current_mobile().launch_app()
        Preconditions.make_in_message_page(moible_param)

    @staticmethod
    def activate_app(app_id=None):
        """激活APP"""
        if not app_id:
            app_id = current_mobile().driver.desired_capabilities['appPackage']
        current_mobile().driver.activate_app(app_id)

    @staticmethod
    def get_into_group_chat_page(name):
        """进入群聊聊天会话页面"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击发起群聊
        mp.click_group_chat()
        scg = SelectContactsPage()
        times = 15
        n = 0
        # 重置应用时需要再次点击才会出现选择一个群
        while n < times:
            # 等待选择联系人页面加载
            flag = scg.wait_for_page_load()
            if not flag:
                scg.click_back()
                time.sleep(2)
                mp.click_add_icon()
                mp.click_group_chat()
            else:
                break
            n += 1
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name(name)
        gcp = GroupChatPage()
        gcp.wait_for_page_load()

    @staticmethod
    def enter_message_page(reset=False):
        """进入消息页面"""
        # 登录进入消息页面
        Preconditions.make_already_in_message_page(reset)

    @staticmethod
    def enter_single_chat_page(name):
        """进入单聊聊天会话页面"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击“新建消息”
        mp.click_new_message()
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        # 进入单聊会话页面
        slc.selecting_local_contacts_by_name(name)
        bcp = BaseChatPage()
        if bcp.is_exist_dialog():
            # 点击我已阅读
            bcp.click_i_have_read()
        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @staticmethod
    def dismiss_one_group(name):
        Preconditions.get_into_group_chat_page(name)
        GroupChatPage().click_setting()
        page = GroupChatSetPage()
        time.sleep(1)
        page.click_group_manage()
        time.sleep(1)
        page.click_group_manage_disband_button()
        time.sleep(0.5)
        page.click_element_('确定')
        time.sleep(3)
        page.wait_for_text('该群已解散')

    @staticmethod
    def dismiss_one_group2(name):
        Preconditions.get_into_group_chat_page(name)
        GroupChatPage().click_setting()
        page = GroupChatSetPage()
        time.sleep(1)
        page.click_group_manage2()
        time.sleep(1)
        page.click_group_manage_disband_button()
        time.sleep(0.5)
        page.click_element_('确定')
        time.sleep(3)
        page.wait_for_text('该群已解散')


class MsgAllPrior(TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def default_setUp(self):
        """确保每个用例运行前在消息页面"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        else:
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_login_chenjialiang_0256(self):
        """通讯录权限-消息-新建消息"""
        message = MessagePage()
        message.wait_for_page_load()
        message.click_add_icon()
        message.click_new_message()
        message.wait_for_page_load()
        # 点击返回，并判断是否正常
        slc = SelectContactsPage()
        # slc.click_back()
        # self.assertTrue(message.is_on_this_page)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_019(self):
        """会话窗口中点击删除文本消息"""
        # 打开‘我’页面
        me = MePage()
        me.open_me_page()
        time.sleep(3)
        self.assertTrue(me.is_on_this_page())
        # 打开‘查看并编辑个人资料’页面
        me.click_view_edit()
        # 点击分享名片
        view_user_profile_page = MeViewUserProfilePage()
        view_user_profile_page.page_down()
        view_user_profile_page.click_share_card()
        # 选择本地联系人
        sc = SelectContactsPage()
        sc.click_phone_contact()
        local_contacts_page = SelectLocalContactsPage()
        local_contacts_page.search("1111111111111111")
        result = local_contacts_page.no_search_result()
        self.assertTrue(result)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0023(self):
        """进入免费/发送短信--选择联系人页面"""
        message_page = MessagePage()
        # 点击+号
        message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/action_add'))
        # 点击免费短信
        message_page.click_free_sms()
        try:
            text = message_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
            if text == "确定":
                message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
        except BaseException:
            print("warn ：非首次进入，无需确认！")
        select_contacts_page = SelectContactsPage()
        time.sleep(2)
        select_contacts_page.click_one_contact_631("大佬1")
        sms_text = select_contacts_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/et_sms'))
        self.assertTrue(sms_text == '发送短信...')
        select_contacts_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/et_sms'), "你好，testOK !")
        select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_sms_send'))
        # 	com.chinasofti.rcs:id/ib_sms_send
        try:
            select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'))
        except BaseException:
            print("warn ：非首次进入，无需资费提醒确认！")
        select_contacts_page.click_element((MobileBy.ID, 'com.android.mms:id/send_button_sms'))
        # com.android.mms:id/send_button_sms


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0036(self):
        """进入免费/发送短信--选择联系人页面"""
        message_page = MessagePage()
        message_page.open_message_page()
        # 点击+号
        message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/action_add'))
        # 点击免费短信
        message_page.click_free_sms()
        try:
            text = message_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
            if text == "确定":
                message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
        except BaseException:
            print("warn ：非首次进入，无需确认！")
        select_contacts_page = SelectContactsPage()
        time.sleep(2)
        select_contacts_page.click_one_contact_631("大佬1")
        msg_text = '你好，testOK !'
        select_contacts_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/et_sms'), msg_text)
        select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_sms_send'))
        try:
            select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'))
        except BaseException:
            print("warn ：非首次进入，无需资费提醒确认！")
        select_contacts_page.click_element((MobileBy.ID, 'com.android.mms:id/send_button_sms'))
        select_contacts_page.press_mess(msg_text)
        select_contacts_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="转发"]'))
        time.sleep(2)
        select_contacts_page.click_one_contact_631("大佬2")
        select_contacts_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/btn_ok" and @text="确定"]'))
        exist = select_contacts_page.is_toast_exist('已转发')
        self.assertTrue(exist)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0037(self):
        """进入免费/发送短信--选择联系人页面"""
        message_page = MessagePage()
        # 点击+号
        message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/action_add'))
        # 点击免费短信
        message_page.click_free_sms()
        try:
            text = message_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
            if text == "确定":
                message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
        except BaseException:
            print("warn ：非首次进入，无需确认！")
        select_contacts_page = SelectContactsPage()
        time.sleep(2)
        select_contacts_page.click_one_contact_631("大佬1")
        msg_text = '你好，testOK !' + str(random.random())
        select_contacts_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/et_sms'), msg_text)
        select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_sms_send'))
        try:
            select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'))
        except BaseException:
            print("warn ：非首次进入，无需资费提醒确认！")
        select_contacts_page.click_element((MobileBy.ID, 'com.android.mms:id/send_button_sms'))
        select_contacts_page.press_mess(msg_text)
        select_contacts_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="删除"]'))
        elements = select_contacts_page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="删除"]'))
        self.assertTrue(len(elements) == 0)


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0038(self):
        """进入免费/发送短信--选择联系人页面"""
        message_page = MessagePage()
        # 点击+号
        message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/action_add'))
        # 点击免费短信
        message_page.click_free_sms()
        try:
            text = message_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
            if text == "确定":
                message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
        except BaseException:
            print("warn ：非首次进入，无需确认！")
        select_contacts_page = SelectContactsPage()
        time.sleep(2)
        select_contacts_page.click_one_contact_631("大佬1")
        msg_text = '你好，testOK !' + str(random.random())
        select_contacts_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/et_sms'), msg_text)
        select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_sms_send'))
        try:
            select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'))
        except BaseException:
            print("warn ：非首次进入，无需资费提醒确认！")
        select_contacts_page.click_element((MobileBy.ID, 'com.android.mms:id/send_button_sms'))
        select_contacts_page.press_mess(msg_text)
        select_contacts_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="复制"]'))
        flag = select_contacts_page.is_toast_exist('和飞信：已复制')
        self.assertTrue(flag)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0039(self):
        """进入免费/发送短信--选择联系人页面"""
        message_page = MessagePage()
        # 点击+号
        time.sleep(5)
        message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/action_add'))
        # message_page.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/action_add" and @class="android.widget.ImageView"]'))
        # 点击免费短信
        message_page.click_free_sms()
        try:
            text = message_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
            if text == "确定":
                message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
        except BaseException:
            print("warn ：非首次进入，无需确认！")
        select_contacts_page = SelectContactsPage()
        time.sleep(2)
        select_contacts_page.click_one_contact_631("大佬1")
        msg_text = '你好，testOK !' + str(random.random())
        select_contacts_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/et_sms'), msg_text)
        select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_sms_send'))
        try:
            select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'))
        except BaseException:
            print("warn ：非首次进入，无需资费提醒确认！")
        select_contacts_page.click_element((MobileBy.ID, 'com.android.mms:id/send_button_sms'))
        select_contacts_page.press_mess(msg_text)
        select_contacts_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="收藏"]'))
        flag = select_contacts_page.is_toast_exist('已收藏')
        self.assertTrue(flag)


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0040(self):
        """进入免费/发送短信--选择联系人页面"""
        message_page = MessagePage()
        # 点击+号
        message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/action_add'))
        # 点击免费短信
        message_page.click_free_sms()
        try:
            text = message_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
            if text == "确定":
                message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
        except BaseException:
            print("warn ：非首次进入，无需确认！")
        select_contacts_page = SelectContactsPage()
        time.sleep(2)
        select_contacts_page.click_one_contact_631("大佬1")
        sms_text = select_contacts_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/et_sms'))
        self.assertTrue(sms_text == '发送短信...')
        msg_text = '你好，testOK !' + str(random.random())
        select_contacts_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/et_sms'), msg_text)
        select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_sms_send'))
        try:
            select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'))
        except BaseException:
            print("warn ：非首次进入，无需资费提醒确认！")
        select_contacts_page.click_element((MobileBy.ID, 'com.android.mms:id/send_button_sms'))
        select_contacts_page.press_mess(msg_text)
        select_contacts_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="多选"]'))
        self.assertTrue(select_contacts_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/multi_btn_forward')) == '转发')
        select_contacts_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/multi_btn_delete" and @text="删除"]'))
        select_contacts_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/btn_ok" and @text="删除"]'))
        select_contacts_page.is_toast_exist("和飞信：删除成功")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0061(self):
        """进入免费/发送短信查看展示页面"""
        message_page = MessagePage()
        time.sleep(4)
        # 点击+号
        message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/action_add'))
        # 点击免费短信
        message_page.click_free_sms()
        try:
            text = message_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
            if text == "确定":
                message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
        except BaseException:
            print("warn ：非首次进入，无需确认！")
        title_text = message_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/title'))
        self.assertTrue(title_text == "选择联系人")

        search_bar_text = message_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'))
        self.assertTrue(search_bar_text == "搜索或输入手机号")

        hint_text = message_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/text_hint'))
        self.assertTrue(hint_text == "选择团队联系人")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0062(self):
        """进入免费/发送短信--选择联系人页面"""
        message_page = MessagePage()
        time.sleep(4)
        # 点击+号
        message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/action_add'))
        # 点击免费短信
        message_page.click_free_sms()
        try:
            text = message_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
            if text == "确定":
                message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
        except BaseException:
            print("warn ：非首次进入，无需确认！")
        select_contacts_page = SelectContactsPage()
        time.sleep(2)
        select_contacts_page.click_one_contact_631("大佬1")


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0063(self):
        """进入免费/发送短信--选择联系人页面"""
        message_page = MessagePage()
        # 点击+号
        message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/action_add'))
        # 点击免费短信
        message_page.click_free_sms()
        try:
            text = message_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
            if text == "确定":
                message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
        except BaseException:
            print("warn ：非首次进入，无需确认！")
        select_contacts_page = SelectContactsPage()
        time.sleep(2)
        self.assertFalse(select_contacts_page.search_contact_is_exsit("关飞"))
        # 当搜索我的电脑相关时，不显示我的电脑
        self.assertFalse(select_contacts_page.search_contact_is_exsit("我的电脑"))
        # 当搜索一个手机号时
        select_contacts_page.search('13782572918')
        time.sleep(3)
        # 显示网络搜索
        view_elements = select_contacts_page.get_elements(
            (MobileBy.XPATH, '//*[contains(@text,"(未知号码)")]'))
        self.assertTrue(len(view_elements) > 0)


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0071(self):
        """进入免费/发送短信--选择联系人页面"""
        message_page = MessagePage()
        # 点击+号
        message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/action_add'))
        # 点击免费短信
        message_page.click_free_sms()
        try:
            text = message_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
            if text == "确定":
                message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
        except BaseException:
            print("warn ：非首次进入，无需确认！")
        select_contacts_page = SelectContactsPage()
        time.sleep(2)
        select_contacts_page.click_one_contact_631("大佬1")
        sms_text = select_contacts_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/et_sms'))
        self.assertTrue(sms_text == '发送短信...')

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0076():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_single_chat_page("大佬1")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0076(self):
        """将自己发送的文件转发到企业群"""
        scp = SingleChatPage()
        scp.wait_for_page_load()
        if scp.is_exist_msg_file():
            pass
        else:
            scp =  SingleChatPage()
            scp.click_file()
            select_file_type = ChatSelectFilePage()
            select_file_type.wait_for_page_load()
            select_file_type.click_local_file()
            local_file = ChatSelectLocalFilePage()
            local_file.click_preset_file_dir()
            local_file.select_file(".xlsx")
            local_file.click_send()
            scp.wait_for_page_load()
        # 转发xls文件
        ChatFilePage().forward_file('.xlsx')
        SelectContactsPage().wait_for_page_load()
        # 需要转发的群
        SelectContactsPage().click_select_one_group()
        group_name = "测试企业群"
        SelectOneGroupPage().selecting_one_group_by_name(group_name)
        SelectOneGroupPage().click_sure_forward()
        # 转发成功并回到聊天页面
        self.assertTrue(scp.is_exist_forward())
        scp.wait_for_page_load()
        self.assertFalse(scp.is_exist_msg_send_failed_button())


    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0106():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_single_chat_page("大佬1")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0106(self):
        """将自己发送的文件转发到团队置灰的联系人"""
        scp = SingleChatPage()
        scp.wait_for_page_load()
        if scp.is_exist_msg_file():
            pass
        else:
            scp = SingleChatPage()
            scp.click_file()
            select_file_type = ChatSelectFilePage()
            select_file_type.wait_for_page_load()
            select_file_type.click_local_file()
            local_file = ChatSelectLocalFilePage()
            local_file.click_preset_file_dir()
            local_file.select_file(".xlsx")
            local_file.click_send()
            scp.wait_for_page_load()
        # 转发xls文件
        ChatFilePage().forward_file('.xlsx')
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2.点击“选择和通讯录联系人”菜单
        scp.click_text_or_description("选择团队联系人")
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 3.在搜索框输入置灰的联系人
        shc.input_search("admin")
        # 4.点击搜索的团队联系人
        shc.click_search_team_contacts()
        flag = shc.is_toast_exist("该联系人不可选择")
        if not flag:
            raise AssertionError("在转发发送自己的位置时，没有‘该联系人不可选择’提示")

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0125():
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        # 从消息进入创建团队页面
        mess.open_workbench_page()
        workbench = WorkbenchPage()
        workbench.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_actionbar'))
        elements = workbench.get_elements((MobileBy.XPATH,
                                           '//*[@resource-id="com.chinasofti.rcs:id/tv_listitem" and @text="%s"]' % Preconditions.get_team_name()))

        if len(elements) == 0:
            Preconditions.enter_create_team_page()
            Preconditions.create_team()
        else:
            elements[0].click()
        Preconditions.make_already_have_my_group()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0125(self):
        """会话窗口中点击删除文本消息"""
        # 推送文件到指定目录
        path = 'aaaresource'
        contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
                                                     os.path.join(PROJECT_PATH, path))
        select_one_group_page = SelectOneGroupPage()
        group_chat_name = Preconditions.get_group_chat_name()
        select_one_group_page.select_one_group_by_name("群聊2")
        select_one_group_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        ChatMorePage().click_file1()
        ChatSelectFilePage().click_local_file()
        elements = select_one_group_page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        while len(elements) == 0:
            select_one_group_page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
            time.sleep(1)
            elements = select_one_group_page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        select_one_group_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        select_one_group_page.click_element_by_path("2018-11-09 11-06-18-722582.log")
        select_one_group_page.click_send_message()
        time.sleep(1)
        file_elements = select_one_group_page.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and @text="2018-11-09 11-06-18-722582.log"]'))
        time.sleep(1)
        select_one_group_page.press(file_elements[0])
        select_one_group_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="转发"]'))
        select_one_group_page.input_text(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_search_bar" and @text="搜索或输入手机号"]'),
            '我的电脑')
        # 点击我的电脑
        select_one_group_page.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="我的电脑"]'))
        select_one_group_page.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/btn_ok" and @text="确定"]'))
        exist = select_one_group_page.is_toast_exist("已转发")
        self.assertTrue(exist)
        # 删除所有转发信息
        wait_del_file_elements = select_one_group_page.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and @text="2018-11-09 11-06-18-722582.log"]'))
        for file_element in wait_del_file_elements:
            select_one_group_page.press(file_element)
            select_one_group_page.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="删除"]'))

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0126():
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        # 从消息进入创建团队页面
        mess.open_workbench_page()
        workbench = WorkbenchPage()
        workbench.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_actionbar'))
        elements = workbench.get_elements((MobileBy.XPATH,
                                           '//*[@resource-id="com.chinasofti.rcs:id/tv_listitem" and @text="%s"]' % Preconditions.get_team_name()))

        if len(elements) == 0:
            Preconditions.enter_create_team_page()
            Preconditions.create_team()
        else:
            elements[0].click()
        Preconditions.make_already_have_my_group()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0126(self):
        """会话窗口中点击删除文本消息"""
        # 推送文件到指定目录
        path = 'aaaresource'
        contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
                                                     os.path.join(PROJECT_PATH, path))
        select_one_group_page = SelectOneGroupPage()
        group_chat_name = Preconditions.get_group_chat_name()
        select_one_group_page.select_one_group_by_name(group_chat_name)
        select_one_group_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        ChatMorePage().click_file1()
        ChatSelectFilePage().click_local_file()
        elements = select_one_group_page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        while len(elements) == 0:
            select_one_group_page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
            time.sleep(1)
            elements = select_one_group_page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        select_one_group_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        select_one_group_page.click_element_by_path("2018-11-09 11-06-18-722582.log")
        select_one_group_page.click_send_message()
        time.sleep(1)
        file_elements = select_one_group_page.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and @text="2018-11-09 11-06-18-722582.log"]'))
        time.sleep(1)
        select_one_group_page.press(file_elements[0])
        select_one_group_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="转发"]'))
        # 点击我的电脑
        select_one_group_page.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/item_rl" and @index="1"]'))
        select_one_group_page.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/btn_ok" and @text="确定"]'))
        exist = select_one_group_page.is_toast_exist("已转发")
        self.assertTrue(exist)
        # 删除所有转发信息
        wait_del_file_elements = select_one_group_page.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and @text="2018-11-09 11-06-18-722582.log"]'))
        for file_element in wait_del_file_elements:
            select_one_group_page.press(file_element)
            select_one_group_page.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="删除"]'))

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0129():
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        # 从消息进入创建团队页面
        mess.open_workbench_page()
        workbench = WorkbenchPage()
        workbench.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_actionbar'))
        elements = workbench.get_elements((MobileBy.XPATH,
                                           '//*[@resource-id="com.chinasofti.rcs:id/tv_listitem" and @text="%s"]' % Preconditions.get_team_name()))

        if len(elements) == 0:
            Preconditions.enter_create_team_page()
            Preconditions.create_team()
        else:
            elements[0].click()
        Preconditions.make_already_have_my_group()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0129(self):
        """会话窗口中点击删除文本消息"""
        # 推送文件到指定目录
        path = 'aaaresource'
        contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
                                                     os.path.join(PROJECT_PATH, path))
        select_one_group_page = SelectOneGroupPage()
        group_chat_name = Preconditions.get_group_chat_name()
        select_one_group_page.select_one_group_by_name(group_chat_name)
        select_one_group_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        ChatMorePage().click_file1()
        ChatSelectFilePage().click_local_file()
        elements = select_one_group_page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        while len(elements) == 0:
            select_one_group_page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
            time.sleep(1)
            elements = select_one_group_page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        select_one_group_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        select_one_group_page.click_element_by_path("2018-11-09 11-06-18-722582.log")
        select_one_group_page.click_send_message()
        time.sleep(1)
        file_elements = select_one_group_page.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and @text="2018-11-09 11-06-18-722582.log"]'))
        time.sleep(1)
        select_one_group_page.press(file_elements[0])
        select_one_group_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="转发"]'))
        # 点击我的电脑
        select_one_group_page.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/item_rl" and @index="1"]'))
        select_one_group_page.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/btn_ok" and @text="确定"]'))
        exist = select_one_group_page.is_toast_exist("已转发")
        self.assertTrue(exist)
        # 删除所有转发信息
        wait_del_file_elements = select_one_group_page.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and @text="2018-11-09 11-06-18-722582.log"]'))
        for file_element in wait_del_file_elements:
            select_one_group_page.press(file_element)
            select_one_group_page.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="删除"]'))


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0392(self):
        """会控页未创建会场成功时（12560未回呼）添加成员按钮置灰"""

        # # 启动App
        # Preconditions.select_mobile('Android-移动')
        # # 启动后不论当前在哪个页面，强制进入消息页面
        # Preconditions.force_enter_message_page_631()
        # # 下面根据用例情况进入相应的页面
        # # 需要预置联系人
        # contactname1 = Preconditions.contacts_name_1
        # contactnum1 = Preconditions.telephone_num_1
        # contactname2 = Preconditions.contacts_name_2
        # contactnum2 = Preconditions.telephone_num_2
        # # 新建联系人
        # contactspage = ContactsPage()
        # contactspage.open_contacts_page()
        # contactspage.create_contacts_if_not_exits_631(contactname1, contactnum1)
        # contactspage.create_contacts_if_not_exits_631(contactname2, contactnum2)

        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 1.1选择指定联系人 发起和飞信呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.search("大佬1")
        selectcontacts.click_contact_by_name("大佬1")
        time.sleep(4)
        selectcontacts.click_sure_bottom()
        time.sleep(1)
        # # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        # callcontact.click_elsfif_ikonw()
        # # 是否存在权限窗口 自动赋权
        # grantpemiss = GrantPemissionsPage()
        # grantpemiss.allow_contacts_permission()
        # # checkpoint1: 是否存在设置悬浮窗，存在暂不开启
        # from pages.components.dialogs import SuspendedTips
        # suspend = SuspendedTips()
        # suspend.ignore_tips_if_tips_display()
        # # checkpoint2: 点击‘+’按钮，提示toast“请接听和飞信电话后再试”’
        # multiparty = MultipartyCallPage()
        # multiparty.click_caller_add_icon()
        # multiparty.is_exist_accept_feixincall_then_tryagain()
        # # 判断当前是否在系统通话界面 是的话 挂断系统电话
        # callpage = CallPage()
        # Flag = True
        # i = 0
        # while Flag:
        #     time.sleep(1)
        #     if callpage.is_phone_in_calling_state():
        #         break
        #     elif i > 5:
        #         break
        #     else:
        #         i = i + 1
        # time.sleep(2)
        # callpage.hang_up_the_call()



    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0393(self):
        """会控页未创建会场成功时（12560未回呼）点击呼叫中的成员头像提示语"""

        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 1.1选择指定联系人 发起和飞信呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.search("大佬2")
        selectcontacts.click_contact_by_name("大佬2")
        time.sleep(4)
        selectcontacts.click_sure_bottom()
        time.sleep(1)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        # callcontact.click_elsfif_ikonw()
        # # 是否存在权限窗口 自动赋权
        # grantpemiss = GrantPemissionsPage()
        # grantpemiss.allow_contacts_permission()
        # # checkpoint1: 是否存在设置悬浮窗，存在暂不开启
        # from pages.components.dialogs import SuspendedTips
        # suspend = SuspendedTips()
        # suspend.ignore_tips_if_tips_display()
        # # checkpoint2: 点击成员头像，提示toast“请接听和飞信电话后再试”’
        # multiparty = MultipartyCallPage()
        # multiparty.click_caller_image()
        # multiparty.is_exist_accept_feixincall_then_tryagain()
        # # 判断当前是否在系统通话界面 是的话 挂断系统电话
        # callpage = CallPage()
        # Flag = True
        # i = 0
        # while Flag:
        #     time.sleep(1)
        #     if callpage.is_phone_in_calling_state():
        #         break
        #     elif i > 30:
        #         break
        #     else:
        #         i = i + 1
        # time.sleep(2)
        # callpage.hang_up_the_call()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0394(self):
        """会控页未创建会场成功时（12560未回呼）点击缩小按钮"""

        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 1.1选择指定联系人 发起和飞信呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.search("大佬1")
        selectcontacts.click_contact_by_name("大佬1")
        time.sleep(4)
        selectcontacts.click_sure_bottom()
        time.sleep(1)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        # callcontact.click_elsfif_ikonw()
        # # 是否存在权限窗口 自动赋权
        # grantpemiss = GrantPemissionsPage()
        # grantpemiss.allow_contacts_permission()
        # # 是否存在设置悬浮窗，存在暂不开启
        # from pages.components.dialogs import SuspendedTips
        # suspend = SuspendedTips()
        # suspend.ignore_tips_if_tips_display()
        # # checkpoint1: 点击最小化，回到消息界面”’
        # multiparty = MultipartyCallPage()
        # multiparty.click_min_window()
        # # checkpoint2: 消息界面存在“你正在飞信电话”’
        # callpage = CallPage()
        # callpage.is_you_are_calling_exists()
        # # 判断当前是否在系统通话界面 是的话 挂断系统电话
        # callpage = CallPage()
        # Flag = True
        # i = 0
        # while Flag:
        #     time.sleep(1)
        #     if callpage.is_phone_in_calling_state():
        #         break
        #     elif i > 30:
        #         break
        #     else:
        #         i = i + 1
        # time.sleep(2)
        # callpage.hang_up_the_call()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0395(self):
        """会控页未创建会场成功时（12560未回呼）点击全员禁言按钮"""

        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 1.1选择指定联系人 发起和飞信呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.search("大佬1")
        selectcontacts.click_contact_by_name("大佬1")
        time.sleep(4)
        selectcontacts.click_sure_bottom()
        time.sleep(1)
        # # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        # callcontact.click_elsfif_ikonw()
        # # 是否存在权限窗口 自动赋权
        # grantpemiss = GrantPemissionsPage()
        # grantpemiss.allow_contacts_permission()
        # # 是否存在设置悬浮窗，存在暂不开启
        # from pages.components.dialogs import SuspendedTips
        # suspend = SuspendedTips()
        # suspend.ignore_tips_if_tips_display()
        # # checkpoint1: 点击全员禁言”’
        # multiparty = MultipartyCallPage()
        # multiparty.click_groupcall_mute()
        # # 判断当前是否在系统通话界面 是的话 挂断系统电话
        # callpage = CallPage()
        # Flag = True
        # i = 0
        # while Flag:
        #     time.sleep(1)
        #     if callpage.is_phone_in_calling_state():
        #         break
        #     elif i > 30:
        #         break
        #     else:
        #         i = i + 1
        # time.sleep(2)
        # callpage.hang_up_the_call()


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0396(self):
        """会控页未创建会场成功时（12560未回呼）点击挂断"""

        # 进入通话页签
        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 1.1选择指定联系人 发起和飞信呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.search("大佬1")
        selectcontacts.click_contact_by_name("大佬1")
        time.sleep(4)
        selectcontacts.click_sure_bottom()
        time.sleep(1)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        # callcontact.click_elsfif_ikonw()
        # # 是否存在权限窗口 自动赋权
        # grantpemiss = GrantPemissionsPage()
        # grantpemiss.allow_contacts_permission()
        # # 是否存在设置悬浮窗，存在暂不开启
        # from pages.components.dialogs import SuspendedTips
        # suspend = SuspendedTips()
        # suspend.ignore_tips_if_tips_display()
        # # checkpoint1: 点击挂断和飞信电话”’
        # callpage = CallPage()
        # callpage.hang_up_hefeixin_call_631()
        # # checkpoint2: 挂断电话回到通话页签
        # time.sleep(3)
        # self.assertTrue(callpage.is_on_the_call_page())


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0397(self):
        """成功创建会场成功后（12560回呼接通）进入会控页"""

        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 1.1选择指定联系人 发起和飞信呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.search("大佬1")
        selectcontacts.click_contact_by_name("大佬1")
        time.sleep(4)
        selectcontacts.click_sure_bottom()
        time.sleep(1)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        # callcontact.click_elsfif_ikonw()
        # # 是否存在权限窗口 自动赋权
        # grantpemiss = GrantPemissionsPage()
        # grantpemiss.allow_contacts_permission()
        # # 是否存在设置悬浮窗，存在暂不开启
        # from pages.components.dialogs import SuspendedTips
        # suspend = SuspendedTips()
        # suspend.ignore_tips_if_tips_display()
        # # 判断当前是否在系统通话界面,是的话进入手机home页
        # callpage = CallPage()
        # Flag = True
        # i = 0
        # while Flag:
        #     time.sleep(1)
        #     if callpage.is_phone_in_calling_state():
        #         break
        #     elif i > 30:
        #         break
        #     else:
        #         i = i + 1
        # # 进入手机home页
        # from pages import OneKeyLoginPage
        # page = OneKeyLoginPage()
        # page.press_home_key()
        # time.sleep(2)
        # # 再次激活进入和飞信app
        # current_mobile().activate_app(app_id='com.chinasofti.rcs')
        # time.sleep(3)
        # # 点击进入通话会控页，
        # callpage.click_back_to_call_631()
        # time.sleep(2)
        # # checkpoint：点击添加会话人，进入选择联系人页面
        # multipage = MultipartyCallPage()
        # multipage.click_caller_add_icon()
        # # checkpoint：当前在选择联系人界面
        # time.sleep(2)
        # self.assertTrue(callpage.is_text_present('飞信电话'))
        # multipage.click_back()
        # callpage.hang_up_hefeixin_call_631()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0398(self):
        """成功创建会场成功后（12560回呼接通）点击添加成员"""

        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 1.1选择指定联系人 发起和飞信呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.search("大佬1")
        selectcontacts.click_contact_by_name("大佬1")
        time.sleep(4)
        selectcontacts.click_sure_bottom()
        time.sleep(1)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        # callcontact.click_elsfif_ikonw()
        # # 是否存在权限窗口 自动赋权
        # grantpemiss = GrantPemissionsPage()
        # grantpemiss.allow_contacts_permission()
        # # 是否存在设置悬浮窗，存在暂不开启
        # from pages.components.dialogs import SuspendedTips
        # suspend = SuspendedTips()
        # suspend.ignore_tips_if_tips_display()
        # # 当出现系统通话页面，则进入手机home页
        # callpage = CallPage()
        # Flag = True
        # i = 0
        # while Flag:
        #     time.sleep(1)
        #     if callpage.is_phone_in_calling_state():
        #         break
        #     elif i > 30:
        #         break
        #     else:
        #         i = i + 1
        # from pages import OneKeyLoginPage
        # page = OneKeyLoginPage()
        # page.press_home_key()
        # time.sleep(2)
        # # 再次激活进入和飞信app
        # current_mobile().activate_app(app_id='com.chinasofti.rcs')
        # time.sleep(3)
        # # 点击进入通话会控页，
        # callpage.click_back_to_call_631()
        # time.sleep(2)
        # # checkpoint：点击添加会话人，进入选择联系人页面
        # multipage = MultipartyCallPage()
        # multipage.click_caller_add_icon()
        # # checkpoint：成功吊起联系人选择器
        # time.sleep(2)
        # self.assertTrue(callpage.is_text_present('飞信电话'))
        # multipage.click_back()
        # callpage.hang_up_hefeixin_call_631()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0399(self):
        """成功创建会场成功后（12560回呼接通）缩小悬浮窗"""

        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 1.1选择指定联系人 发起和飞信呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.search("大佬1")
        selectcontacts.click_contact_by_name("大佬1")
        time.sleep(4)
        selectcontacts.click_sure_bottom()
        time.sleep(1)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        # callcontact.click_elsfif_ikonw()
        # # 是否存在权限窗口 自动赋权
        # grantpemiss = GrantPemissionsPage()
        # grantpemiss.allow_contacts_permission()
        # # 是否存在设置悬浮窗，存在暂不开启
        # from pages.components.dialogs import SuspendedTips
        # suspend = SuspendedTips()
        # suspend.ignore_tips_if_tips_display()
        # # 当出现系统通话页面，则进入手机home页
        # callpage = CallPage()
        # Flag = True
        # i = 0
        # while Flag:
        #     time.sleep(1)
        #     if callpage.is_phone_in_calling_state():
        #         break
        #     elif i > 30:
        #         break
        #     else:
        #         i = i + 1
        # # 回到手机主页面
        # from pages import OneKeyLoginPage
        # page = OneKeyLoginPage()
        # page.press_home_key()
        # time.sleep(2)
        # # 再次激活进入和飞信app
        # current_mobile().activate_app(app_id='com.chinasofti.rcs')
        # time.sleep(2)
        # # 点击进入通话会控页，
        # callpage.click_back_to_call_631()
        # time.sleep(2)
        # # checkpoint：点击缩小按扭
        # multipage = MultipartyCallPage()
        # multipage.click_min_window()
        # time.sleep(3)
        # # checkpoint：成功进入消息页面，再次进入会控页面挂断电话
        # callpage.click_back_to_call_631()
        # callpage.hang_up_hefeixin_call_631()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0400(self):
        """成功创建会场成功后（12560回呼接通）点击全员禁言"""

        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 1.1选择指定联系人 发起和飞信呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.search("大佬1")
        selectcontacts.click_contact_by_name("大佬1")
        time.sleep(4)
        selectcontacts.click_sure_bottom()
        time.sleep(1)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        # callcontact.click_elsfif_ikonw()
        # # 是否存在权限窗口 自动赋权
        # grantpemiss = GrantPemissionsPage()
        # grantpemiss.allow_contacts_permission()
        # # 是否存在设置悬浮窗，存在暂不开启
        # from pages.components.dialogs import SuspendedTips
        # suspend = SuspendedTips()
        # suspend.ignore_tips_if_tips_display()
        # # 当出现系统通话页面，则进入手机home页
        # callpage = CallPage()
        # Flag = True
        # i = 0
        # while Flag:
        #     time.sleep(1)
        #     if callpage.is_phone_in_calling_state():
        #         break
        #     elif i > 30:
        #         break
        #     else:
        #         i = i + 1
        # # 回到手机主页面
        # from pages import OneKeyLoginPage
        # page = OneKeyLoginPage()
        # page.press_home_key()
        # time.sleep(2)
        # # 再次激活进入和飞信app
        # current_mobile().activate_app(app_id='com.chinasofti.rcs')
        # time.sleep(3)
        # # 点击进入通话会控页，
        # callpage.click_back_to_call_631()
        # time.sleep(2)
        # # checkpoint：点击全员禁言
        # multipage = MultipartyCallPage()
        # multipage.click_groupcall_mute()
        # # checkpoint：当前在选择联系人界面
        # time.sleep(2)
        # self.assertTrue(callpage.is_text_present('全员禁言'))
        # callpage.hang_up_hefeixin_call_631()


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0404(self):
        """成功创建会场成功后（12560回呼接通）挂断当前通话"""

        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 1.1选择指定联系人 发起和飞信呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.search("大佬1")
        selectcontacts.click_contact_by_name("大佬1")
        time.sleep(4)
        selectcontacts.click_sure_bottom()
        time.sleep(1)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        # callcontact.click_elsfif_ikonw()
        # # 是否存在权限窗口 自动赋权
        # grantpemiss = GrantPemissionsPage()
        # grantpemiss.allow_contacts_permission()
        # # 是否存在设置悬浮窗，存在暂不开启
        # from pages.components.dialogs import SuspendedTips
        # suspend = SuspendedTips()
        # suspend.ignore_tips_if_tips_display()
        # # 当出现系统通话页面，则进入手机home页
        # callpage = CallPage()
        # Flag = True
        # i = 0
        # while Flag:
        #     time.sleep(1)
        #     if callpage.is_phone_in_calling_state():
        #         break
        #     elif i > 30:
        #         break
        #     else:
        #         i = i + 1
        # # 回到手机主页面
        # from pages import OneKeyLoginPage
        # page = OneKeyLoginPage()
        # page.press_home_key()
        # time.sleep(2)
        # # 再次激活进入和飞信app
        # current_mobile().activate_app(app_id='com.chinasofti.rcs')
        # time.sleep(3)
        # # 点击进入通话会控页，
        # callpage.click_back_to_call_631()
        # time.sleep(2)
        # # checkpoint：当前页面是会控页面，挂断飞信电话
        # callpage.hang_up_hefeixin_call_631()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0406(self):
        """大陆用户实现自动接听的号码：12560结尾的长度不超过9位的号码"""

        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 选择指定联系人 点击呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.search("大佬1")
        selectcontacts.click_contact_by_name("大佬1")
        time.sleep(4)
        selectcontacts.click_sure_bottom()
        time.sleep(1)

        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        # callcontact.click_elsfif_ikonw()
        #
        # # 是否存在权限窗口 自动赋权
        # from pages import GrantPemissionsPage
        # grantpemiss = GrantPemissionsPage()
        # grantpemiss.allow_contacts_permission()
        #
        # # 是否存在设置悬浮窗，存在暂不开启
        # from pages.components.dialogs import SuspendedTips
        # suspend = SuspendedTips()
        # suspend.ignore_tips_if_tips_display()
        # # 等待和飞信电话自动接听，到达系统通话页面
        # # 当出现系统通话页面，则进入手机home页
        # callpage = CallPage()
        # Flag = True
        # i = 0
        # while Flag:
        #     time.sleep(1)
        #     if callpage.is_phone_in_calling_state():
        #         break
        #     elif i > 30:
        #         break
        #     else:
        #         i = i + 1
        # # Checkpoint：当前页面是否是系统挂断页面
        # aa = callpage.is_phone_in_calling_state()
        # self.assertTrue(aa)
        # # 挂断系统电话
        # callpage.hang_up_the_call()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0409(self):
        """大陆用户实现自动接听的号码：12560结尾的长度不超过9位的号码"""

        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 选择指定联系人 点击呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.search("大佬1")
        selectcontacts.click_contact_by_name("大佬1")
        time.sleep(4)
        selectcontacts.click_sure_bottom()
        time.sleep(2)

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
        # Checkpoint：当前页面是否是系统挂断页面
        callpage = CallPage()
        aa = callpage.is_phone_in_calling_state()
        self.assertTrue(aa)
        # 挂断系统电话
        callpage.hang_up_the_call()
        time.sleep(5)
        # checkpoint: 刚才拨打的类型为【电话】,号码包含12560
        callpage.is_type_hefeixin(0, '电话')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0494(self):
        """成功创建会场成功后（12560回呼接通）挂断当前通话"""

        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 选择指定联系人 点击呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.search("大佬1")
        selectcontacts.click_contact_by_name("大佬1")
        time.sleep(4)
        selectcontacts.click_sure_bottom()
        time.sleep(1)

        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        # callcontact.click_elsfif_ikonw()
        #
        # # 是否存在权限窗口 自动赋权
        # from pages import GrantPemissionsPage
        # grantpemiss = GrantPemissionsPage()
        # grantpemiss.allow_contacts_permission()
        #
        # # 是否存在设置悬浮窗，存在暂不开启
        # from pages.components.dialogs import SuspendedTips
        # suspend = SuspendedTips()
        # suspend.ignore_tips_if_tips_display()
        # # 挂断多方通话
        # callpage = CallPage()
        # callpage.hang_up_hefeixin_call_631()
        # time.sleep(3)
        # # Checkpoint：挂断电话回到多方通话界面
        # self.assertTrue(callpage.is_on_the_call_page())

    @staticmethod
    def setUp_test_msg_weifenglian_PC_0354():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 进入单聊页面
        Preconditions.enter_private_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0354(self):
        """单聊-位置"""
        chat_window_page = ChatWindowPage()
        chat_window_page.click_add_icon()
        chat_window_page.click_menu_icon('位置')
        elements = chat_window_page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.lbe.security.miui:id/permission_message"]'))
        self.assertTrue(len(elements) > 0)

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0433():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 进入单聊页面
        Preconditions.enter_private_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0433(self):
        """单聊-位置"""
        chat_window_page = ChatWindowPage()
        chat_window_page.click_add_icon()
        chat_window_page.click_menu_icon('位置')
        elements = chat_window_page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.lbe.security.miui:id/permission_message"]'))
        self.assertTrue(len(elements) > 0)

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0436():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 进入单聊页面
        Preconditions.enter_private_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0436(self):
        """单聊-位置"""
        chat_window_page = ChatWindowPage()
        chat_window_page.click_add_icon()
        chat_window_page.click_menu_icon('位置')
        elements = chat_window_page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.lbe.security.miui:id/permission_message"]'))
        if len(elements) > 0:
            chat_window_page.click_element((MobileBy.XPATH, '//*[@resource-id="android:id/button1"]'))
        chat_window_page.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/location_ok_btn"]'))
        # 长按位置信息
        time.sleep(3)
        chat_window_page.press(chat_window_page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/image_view_lloc_icon"]'))[0])
        # 获取操作信息
        time.sleep(3)
        ops_elements = chat_window_page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view"]'))
        self.assertTrue(len(ops_elements) > 0)

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0437():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 进入单聊页面
        Preconditions.enter_private_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0437(self):
        """单聊-位置"""
        chat_window_page = ChatWindowPage()
        chat_window_page.click_add_icon()
        chat_window_page.click_menu_icon('位置')
        elements = chat_window_page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.lbe.security.miui:id/permission_message"]'))
        if len(elements) > 0:
            chat_window_page.click_element((MobileBy.XPATH, '//*[@resource-id="android:id/button1"]'))
        chat_window_page.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/location_ok_btn"]'))
        # 长按位置信息
        time.sleep(3)
        chat_window_page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/image_view_lloc_icon"]'))[0].click()
        # 获取操作信息
        time.sleep(3)
        enabled_status = chat_window_page.get_element_attribute(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/location_nativ_btn"]'), 'enabled')
        self.assertTrue(enabled_status == "true")

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0445():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 进入单聊页面
        Preconditions.enter_private_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0445(self):
        """单聊-位置"""
        chat_window_page = ChatWindowPage()
        chat_window_page.click_add_icon()
        chat_window_page.click_menu_icon('位置')
        elements = chat_window_page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.lbe.security.miui:id/permission_message"]'))
        if len(elements) > 0:
            chat_window_page.click_element((MobileBy.XPATH, '//*[@resource-id="android:id/button1"]'))

        chat_window_page.input_text((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/search_edit"]'), "医院")

        chat_window_page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/poi_list_item_title"]'))[0].click()

        chat_window_page.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/location_ok_btn"]'))
        # 长按位置信息
        time.sleep(3)
        window_page_get_elements = chat_window_page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/image_view_lloc_icon"]'))
        self.assertTrue(len(window_page_get_elements) > 0)

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0450():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 进入单聊页面
        Preconditions.enter_private_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0450(self):
        """单聊-位置"""
        chat_window_page = ChatWindowPage()
        chat_window_page.click_add_icon()
        chat_window_page.click_menu_icon('位置')
        elements = chat_window_page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.lbe.security.miui:id/permission_message"]'))
        if len(elements) > 0:
            chat_window_page.click_element((MobileBy.XPATH, '//*[@resource-id="android:id/button1"]'))

        chat_window_page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/gd_map_view'), 'up')
        time.sleep(5)
        chat_window_page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/poi_list_item_title"]'))[0].click()

        chat_window_page.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/location_ok_btn"]'))
        # 按位置信息
        time.sleep(3)
        window_page_get_elements = chat_window_page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/image_view_lloc_icon"]'))
        self.assertTrue(len(window_page_get_elements) > 0)

    @staticmethod
    def setUp_test_msg_weifenglian_PC_0042():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 进入我的电脑页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.search_and_enter("我的电脑")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0042(self):
        """会话窗口中点击删除文本消息"""
        # 推送文件到指定目录
        path = 'aaaresource'
        # contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
        #                                              os.path.join(PROJECT_PATH, path))

        # 转发文件的名称
        file_name = '2018-11-09 11-06-18-722582.log'
        chatWindowPage = ChatWindowPage()
        chatWindowPage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_file'))
        chatWindowPage.click_element(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ll_music'))
        time.sleep(2)
        elements = chatWindowPage.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/cb_choose_icon"]'))
        self.assertTrue(len(elements) > 0)
        elements[0].click()
        # 发送
        chatWindowPage.click_element((MobileBy.XPATH,
                                      '//*[@resource-id="com.chinasofti.rcs:id/button_send" and @text="发送"]'))
        try:
            chatWindowPage.click_element((MobileBy.XPATH,
                                          '//*[@resource-id="com.chinasofti.rcs:id/continue_call" and @text="继续发送"]'))
        except BaseException as e:
            print(e)
        time.sleep(3)
        page_elements = chatWindowPage.get_elements((MobileBy.XPATH,
                                                     '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name"]'))
        self.assertTrue(len(page_elements) > 0)

    @staticmethod
    def setUp_test_msg_huangcaizui_D_0048():
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0048(self):
        """1、点击GIF"""
        mess = MessagePage()
        # 判断网络是否正常
        ns = mess.get_network_status()
        self.assertTrue(ns in [2, 4, 6])
        # 点击我的电脑
        self.assertTrue(mess.page_should_contain_my_computer())
        mess.click_my_computer()
        cwp = ChatWindowPage()
        # 点击表情
        cwp.click_expression()
        time.sleep(1)
        # 点击gif
        cwp.click_gif()
        cgp = ChatGIFPage()
        cgp.wait_for_page_load()
        # 判断是否出现gif界面
        self.assertTrue(cgp.is_on_this_page())

    @staticmethod
    def setUp_test_msg_huangcaizui_D_0049():
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0049(self):
        """1、点击GIF 2、选择表情点击"""
        mess = MessagePage()
        # 判断网络是否正常
        ns = mess.get_network_status()
        self.assertTrue(ns in [2, 4, 6])
        # 点击我的电脑
        self.assertTrue(mess.page_should_contain_my_computer())
        mess.click_my_computer()
        cwp = ChatWindowPage()
        # 点击表情
        cwp.click_expression()
        time.sleep(1)
        # 点击gif
        cwp.click_gif()
        cgp = ChatGIFPage()
        cgp.wait_for_page_load()
        # 判断是否出现gif界面
        self.assertTrue(cgp.is_on_this_page())
        # 点击第一个表情包
        cgp.send_gif()
        # 判断是否发送成功
        cwp.wait_for_msg_send_status_become_to("发送成功", max_wait_time=10)

    @staticmethod
    def setUp_test_msg_huangcaizui_D_0051():
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0051(self):
        """1、点击GIF图标 2、搜索框输入数字 3、点击选择表情"""
        mess = MessagePage()
        # 判断网络是否正常
        ns = mess.get_network_status()
        self.assertTrue(ns in [2, 4, 6])
        # 点击我的电脑
        self.assertTrue(mess.page_should_contain_my_computer())
        mess.click_my_computer()
        cwp = ChatWindowPage()
        # 点击表情
        cwp.click_expression()
        time.sleep(1)
        # 点击gif
        cwp.click_gif()
        cgp = ChatGIFPage()
        cgp.wait_for_page_load()
        # 点击表情搜搜
        cgp.input_message("6")
        time.sleep(1)
        # 点击第一个表情包
        cgp.send_gif()
        # 判断是否发送成功
        cwp.wait_for_msg_send_status_become_to("发送成功", max_wait_time=10)

    @staticmethod
    def setUp_test_msg_huangcaizui_D_0052():
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0052(self):
        """1、点击GIF图标 2、搜索框输入特殊字符 3、点击选择表情"""
        # 判断网络是否正常
        mess = MessagePage()
        ns = mess.get_network_status()
        self.assertTrue(ns in [2, 4, 6])
        # 点击我的电脑
        self.assertTrue(mess.page_should_contain_my_computer())
        mess.click_my_computer()
        cwp = ChatWindowPage()
        # 点击表情
        cwp.click_expression()
        time.sleep(1)
        # 点击gif
        cwp.click_gif()
        cgp = ChatGIFPage()
        cgp.wait_for_page_load()
        # 点击表情搜搜
        cgp.input_message("囍")
        time.sleep(1)
        # 点击第一个表情包
        cgp.send_gif()
        # 判断是否发送成功
        cwp.wait_for_msg_send_status_become_to("发送成功", max_wait_time=10)

    @staticmethod
    def setUp_test_msg_huangcaizui_D_0053():
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0053(self):
        """1、点击GIF图标 2、搜索框输入特殊字符 3、点击选择表情"""
        # 判断网络是否正常
        mess = MessagePage()
        ns = mess.get_network_status()
        self.assertTrue(ns in [2, 4, 6])
        # 点击我的电脑
        self.assertTrue(mess.page_should_contain_my_computer())
        mess.click_my_computer()
        cwp = ChatWindowPage()
        # 点击表情
        cwp.click_expression()
        time.sleep(1)
        # 点击gif
        cwp.click_gif()
        cgp = ChatGIFPage()
        cgp.wait_for_page_load()
        # 点击表情搜搜
        cgp.input_message("q")
        self.assertTrue(cwp.is_toast_exist("无搜索结果，换个热词试试"))

    @staticmethod
    def setUp_test_msg_huangcaizui_D_0054():
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0054(self):
        """1、点击GIF图标 2、搜索框输入关键字匹配到对应结果后点击返回 3、再次进入该会话页面"""
        # 判断网络是否正常
        mess = MessagePage()
        ns = mess.get_network_status()
        self.assertTrue(ns in [2, 4, 6])
        # 点击我的电脑
        self.assertTrue(mess.page_should_contain_my_computer())
        mess.click_my_computer()
        cwp = ChatWindowPage()
        # 点击表情
        cwp.click_expression()
        time.sleep(1)
        # 点击gif
        cwp.click_gif()
        cgp = ChatGIFPage()
        cgp.wait_for_page_load()
        # 点击表情搜搜
        cgp.input_message("6")
        time.sleep(1)
        # 退出对话
        cwp.click_back1()
        time.sleep(1)
        # 再次点击我的电脑
        mess.click_my_computer()
        # 判断搜索结果是否存在
        self.assertFalse(cgp.is_on_this_page())

    @staticmethod
    def setUp_test_msg_huangcaizui_D_0055():
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0055(self):
        """1、点击GIF图标 2、搜索框输入关键字匹配到对应结果后点击发送"""
        # 判断网络是否正常
        mess = MessagePage()
        ns = mess.get_network_status()
        self.assertTrue(ns in [2, 4, 6])
        # 点击我的电脑
        self.assertTrue(mess.page_should_contain_my_computer())
        mess.click_my_computer()
        cwp = ChatWindowPage()
        # 点击表情
        cwp.click_expression()
        time.sleep(1)
        # 点击gif
        cwp.click_gif()
        cgp = ChatGIFPage()
        cgp.wait_for_page_load()
        # 点击表情搜搜
        cgp.input_message("6")
        time.sleep(1)
        # 点击第一个表情包
        cgp.send_gif()
        # 判断是否发送成功
        cwp.wait_for_msg_send_status_become_to("发送成功", max_wait_time=10)
        # 判断搜索结果是否存在
        self.assertTrue(cgp.is_on_this_page())

    @staticmethod
    def setUp_test_msg_huangcaizui_D_0057():
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0057(self):
        """1、点击GIF图标 2、点击搜索框右方×"""
        # 判断网络是否正常
        mess = MessagePage()
        ns = mess.get_network_status()
        self.assertTrue(ns in [2, 4, 6])
        # 点击我的电脑
        self.assertTrue(mess.page_should_contain_my_computer())
        mess.click_my_computer()
        cwp = ChatWindowPage()
        # 点击表情
        cwp.click_expression()
        time.sleep(1)
        # 点击gif
        cwp.click_gif()
        cgp = ChatGIFPage()
        cgp.wait_for_page_load()
        # 判断是否在gif页面
        self.assertTrue(cgp.is_on_this_page())
        # 点击退出gif页面
        cgp.close_gif()
        # 判断是否在gif页面
        self.assertFalse(cgp.is_on_this_page())


class Contacts_demo(TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def default_setUp(self):
        """确保每个用例运行前在消息页面"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        else:
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()

    @staticmethod
    def setUp_test_msg_hanjiabin_0193():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_allinfo_if_not_exits('给个名片1', '13800138200', '中软国际', '软件工程师', 'test1234@163.com')
        contactspage.create_contacts_allinfo_if_not_exits('给个名片2', '13800138300', '中软国际', '软件工程师', 'test1234@163.com')
        contactspage.open_message_page()


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_hanjiabin_0193(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词给个红包1
        SearchPage().input_search_keyword("给个名片1")
        # 选择联系人进入联系人页
        mess.choose_chat_by_name('给个名片1')
        # 点击消息按钮发送消息
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        ChatMorePage().close_more()
        mess.click_element_by_text('名片')
        SelectContactsPage().select_one_contact_by_name("给个名片2")
        send_card = Send_CardNamePage()
        send_card.click_share_btn()
        time.sleep(660)
        send_card.press_mess('给个名片2')
        mess.page_should_not_contain_element((MobileBy.XPATH, '//*[@text="删除"]'))

    @staticmethod
    def setUp_test_msg_hanjiabin_0194():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_allinfo_if_not_exits('给个名片1', '13800138200', '中软国际', '软件工程师', 'test1234@163.com')
        contactspage.create_contacts_allinfo_if_not_exits('给个名片2', '13800138300', '中软国际', '软件工程师', 'test1234@163.com')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_hanjiabin_0194(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词给个红包1
        SearchPage().input_search_keyword("给个名片1")
        # 选择联系人进入联系人页
        mess.choose_chat_by_name('给个名片1')
        # 点击消息按钮发送消息
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        ChatMorePage().close_more()
        mess.click_element_by_text('名片')
        SelectContactsPage().select_one_contact_by_name("给个名片2")
        send_card = Send_CardNamePage()
        send_card.click_share_btn()
        send_card.press_mess('给个名片2')
        mess.click_element((MobileBy.XPATH, '//*[@text="删除"]'))
        mess.page_should_not_contain_text('给个名片2')

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0023():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["给个红包1, 13800138000"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0023(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词给个红包1
        SearchPage().input_search_keyword("给个红包1")
        # 选择联系人进入联系人页
        mess.choose_chat_by_name('给个红包1')
        # 点击消息按钮发送消息
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        single = SingleChatPage()
        # 如果当前页面不存在消息，发送一条消息
        if not single._is_element_present((MobileBy.XPATH, '//*[@text ="测试一个呵呵"]')):
            single.input_text_message("测试一个呵呵")
            single.send_text()
        single.press_mess("测试一个呵呵")
        single.click_forward()
        select_page = SelectContactPage()
        # 判断存在选择联系人
        select_page.is_exist_select_contact_btn()
        # 判断存在搜索或输入手机号提示
        select_page.is_exist_selectorinput_toast()
        # 判断存在选择团队联系人按钮
        single.page_should_contain_element((MobileBy.XPATH, '//*[@text ="选择一个群"]'))
        single.page_should_contain_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
        single.page_should_contain_element((MobileBy.XPATH, '//*[@text ="选择团队联系人"]'))

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0279():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.enter_call_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0279(self):
        """从通话——拨号盘——输入陌生号码——进入单聊页面"""
        # 1.客户端已登录
        # 2.网络正常
        # 3.在通话模块
        call = CallPage()
        # Step 1.点击拨号盘
        if not call.is_on_the_dial_pad():
            call.click_dial_pad()
        # Checkpoint 1.调起拨号盘，输入陌生号码
        call.click_one()
        call.click_three()
        call.click_seven()
        call.click_seven()
        call.click_five()
        call.click_five()
        call.click_five()
        call.click_five()
        call.click_five()
        call.click_three()
        call.click_three()
        time.sleep(3)
        # Step 2.点击上方发送消息
        call.click_send_message()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        # Checkpoint 2.进入单聊页面
        self.assertTrue(SingleChatPage().is_on_this_page())

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0280():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["给个红包1, 13800138000"])
        Preconditions.enter_call_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0280(self):
        call = CallPage()
        if not call.is_on_the_dial_pad():
            call.click_element((MobileBy.ID, "com.chinasofti.rcs:id/tvCall"))
        call.click_one()
        call.click_three()
        call.click_eight()
        call.click_zero()
        call.click_zero()
        call.click_one()
        call.click_three()
        call.click_eight()
        call.click_zero()
        call.click_zero()
        call.click_zero()
        time.sleep(3)
        call.click_call_profile()
        # 点击消息按钮发送消息
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        self.assertTrue(SingleChatPage().is_on_this_page())

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0285():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0285(self):
        contactdetail = ContactDetailsPage()
        contactdetail.delete_contact('测试短信1')
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()

        create_page = CreateContactPage()
        contactspage.click_add()
        create_page.wait_for_page_load()
        create_page.hide_keyboard_if_display()
        create_page.create_contact('测试短信1', '13800138111')
        contactdetail.wait_for_page_load()
        ContactDetailsPage().click_message_icon()
        time.sleep(2)
        # 若存在资费提醒对话框，点击确认
        chatdialog = ChatNoticeDialog()
        if chatdialog.is_tips_display():
            chatdialog.accept_and_close_tips_alert()
        self.assertTrue(SingleChatPage().is_on_this_page())

    @staticmethod
    def setUp_test_msg_huangcaizui_B_0015():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["给个红包1, 13800138000"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0015(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词给个红包1
        SearchPage().input_search_keyword("给个红包1")
        # 选择联系人进入联系人页
        mess.choose_chat_by_name('给个红包1')
        # 点击消息按钮发送消息
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_tips_display():
            chatdialog.accept_and_close_tips_alert()
        # 点击短信按钮
        SingleChatPage().click_sms()
        time.sleep(2)
        # 判断存在？标志
        FreeMsgPage().wait_is_exist_wenhao()
        # 判断存在退出短信按钮
        FreeMsgPage().wait_is_exist_exit()
        # 点击？按钮
        chatdialog.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/sms_direction'))
        # 判断弹出资费提醒提示框
        chatdialog.page_should_contain_text('资费提醒')
        # 点击我知道了按钮
        chatdialog.click_element((MobileBy.XPATH, '//*[@text ="我知道了"]'))
        # 判断资费提醒对话框消失
        chatdialog.page_should_not_contain_text('资费提醒')

    @staticmethod
    def setUp_test_msg_huangcaizui_B_0016():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["给个红包1, 13800138000"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0016(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词给个红包1
        SearchPage().input_search_keyword("给个红包1")
        # 选择联系人进入联系人页
        mess.choose_chat_by_name('给个红包1')
        # 点击消息按钮发送消息
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        singlechat = SingleChatPage()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_tips_display():
            chatdialog.accept_and_close_tips_alert()
        # 点击短信按钮
        singlechat.click_sms()
        # 判断存在？标志
        time.sleep(2)
        FreeMsgPage().wait_is_exist_wenhao()
        # 判断存在退出短信按钮
        FreeMsgPage().wait_is_exist_exit()
        # 点击退出短信按钮
        singe_chat.click_exit_sms()
        # 判断是否进入单聊对话框
        text = singlechat.is_on_this_page()
        self.assertTrue(lambda: (text.endswith(')') and text.startswith('(')))

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0022():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_E_0022(self):
        # 打开‘我’页面
        me = MePage()
        me.open_me_page()
        time.sleep(3)
        self.assertTrue(me.is_on_this_page())
        me.click_setting_menu()
        me.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/setting_sms_text'))
        SmsSettingPage().assert_menu_item_has_been_turn_on('应用内收发短信')

    @staticmethod
    def setUp_test_msg_huangmianhua_0400():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["给个红包1, 13800138000"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangmianhua_0400(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词给个红包1
        SearchPage().input_search_keyword("给个红包1")
        # 选择联系人进入联系人页
        mess.choose_chat_by_name('给个红包1')
        # 点击消息按钮发送消息
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        single = SingleChatPage()
        single.input_text_message("测试一个呵呵")
        single.send_text()
        single.click_back()
        mess.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_back'))
        mess.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_back01'))
        mess.is_on_this_page()
        single.press_mess("给个红包1")
        mess.click_element((MobileBy.XPATH, '//*[@text ="置顶聊天"]'))
        single.press_mess("给个红包1")
        mess.click_element((MobileBy.XPATH, '//*[@text ="取消置顶"]'))
        mess.delete_message_record_by_name("给个红包1")
        mess.page_should_not_contain_text('给个红包1')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0140():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0140(self):
        """群主——修改群昵称"""
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_group_name()
        groupset.wait_for_modify_groupname_load()
        groupset.click_edit_group_name_back()
        groupset.wait_for_page_load()
        groupset.click_modify_group_name()
        groupset.save_group_name()
        groupset.wait_for_page_load()
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/group_name')), '测试群组1')
        groupset.click_modify_group_name()
        groupset.wait_for_modify_groupname_load()
        groupset.click_iv_delete_button()
        self.assertEqual(groupset.get_edit_query_text(), '请输入群聊名称')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0141():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0141(self):
        """群主——清除旧名称——录入一个汉字"""
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_group_name()
        time.sleep(2)
        groupset.clear_group_name()
        groupset.input_new_group_name("和")
        groupset.save_group_name()
        time.sleep(10)
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/group_name')), '和')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0142():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0142(self):
        """群主——清除旧名称——录入5个汉字"""
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_group_name()
        time.sleep(2)
        groupset.clear_group_name()
        groupset.input_new_group_name("和飞信测试")
        groupset.save_group_name()
        time.sleep(10)
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/group_name')), '和飞信测试')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0143():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0143(self):
        """群主——清除旧名称——录入10个汉字"""
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_group_name()
        time.sleep(2)
        groupset.clear_group_name()
        groupset.input_new_group_name("和飞信测试和飞信测试")
        groupset.save_group_name()
        time.sleep(10)
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/group_name')), '和飞信测试和飞信测试')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0144():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0144(self):
        """群主——清除旧名称——录入11个汉字"""
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_group_name()
        time.sleep(2)
        groupset.clear_group_name()
        groupset.input_new_group_name("和飞信测试和飞信测试的")
        groupset.save_group_name()
        time.sleep(10)
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/group_name')), '和飞信测试和飞信测试')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0145():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0145(self):
        """群主——清除旧名称——录入1个字母（不区分大、小写）"""
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_group_name()
        time.sleep(2)
        groupset.clear_group_name()
        groupset.input_new_group_name("A")
        groupset.save_group_name()
        time.sleep(10)
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/group_name')), 'A')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0146():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0146(self):
        """群主——清除旧名称——录入10个字母（不区分大、小写）"""
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_group_name()
        time.sleep(2)
        groupset.clear_group_name()
        groupset.input_new_group_name("AABBCCDDEE")
        groupset.save_group_name()
        time.sleep(10)
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/group_name')), 'AABBCCDDEE')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0147():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0147(self):
        """群主——清除旧名称——录入29个字母（不区分大、小写）"""
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_group_name()
        time.sleep(2)
        groupset.clear_group_name()
        groupset.input_new_group_name("AABBCCDDEEAABBCCDDEEAABBCCDDE")
        groupset.save_group_name()
        time.sleep(10)
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/group_name')),
                         'AABBCCDDEEAABBCCDDEEAABBCCDDE')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0148():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0148(self):
        """群主——清除旧名称——录入30个字母（不区分大、小写）"""
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_group_name()
        time.sleep(2)
        groupset.clear_group_name()
        groupset.input_new_group_name("AABBCCDDEEAABBCCDDEEAABBCCDDEE")
        groupset.save_group_name()
        time.sleep(10)
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/group_name')),
                         'AABBCCDDEEAABBCCDDEEAABBCCDDEE')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0149():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0149(self):
        """群主——清除旧名称——录入31个字母（不区分大、小写）"""
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_group_name()
        time.sleep(2)
        groupset.clear_group_name()
        groupset.input_new_group_name("AABBCCDDEEAABBCCDDEEAABBCCDDEEE")
        groupset.save_group_name()
        time.sleep(10)
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/group_name')),
                         'AABBCCDDEEAABBCCDDEEAABBCCDDEE')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0150():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0150(self):
        """群主——清除旧名称——录入1个数字"""
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_group_name()
        time.sleep(2)
        groupset.clear_group_name()
        groupset.input_new_group_name("1")
        groupset.save_group_name()
        time.sleep(10)
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/group_name')), '1')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0151():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0151(self):
        """群主——清除旧名称——录入10个数字"""
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_group_name()
        time.sleep(2)
        groupset.clear_group_name()
        groupset.input_new_group_name("1")
        groupset.save_group_name()
        time.sleep(10)
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/group_name')), '1')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0152():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0152(self):
        """群主——清除旧名称——录入30个数字"""
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_group_name()
        time.sleep(2)
        groupset.clear_group_name()
        groupset.input_new_group_name("112233445511223344551122334455")
        groupset.save_group_name()
        time.sleep(10)
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/group_name')),
                         '112233445511223344551122334455')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0153():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0153(self):
        """群主——清除旧名称——录入31个数字"""
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_group_name()
        time.sleep(2)
        groupset.clear_group_name()
        groupset.input_new_group_name("1122334455112233445511223344556")
        groupset.save_group_name()
        time.sleep(10)
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/group_name')),
                         '112233445511223344551122334455')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0154():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0154(self):
        """群主——清除旧名称——录入汉字+字母+数字"""
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_group_name()
        time.sleep(2)
        groupset.clear_group_name()
        groupset.input_new_group_name("测试233AA")
        groupset.save_group_name()
        time.sleep(10)
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/group_name')), '测试233AA')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0155():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0155(self):
        """群主——清除旧名称——录入特殊字符"""
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_group_name()
        time.sleep(2)
        groupset.clear_group_name()
        groupset.input_new_group_name("!@#$%")
        groupset.save_group_name()
        time.sleep(10)
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/group_name')), '!@#$%')
        groupset.click_modify_group_name()
        time.sleep(2)
        groupset.clear_group_name()
        self.assertFalse(groupset.is_enabled_of_save_group_name_button())

    @staticmethod
    def setUp_test_msg_xiaoqiu_0156():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0156(self):
        """群主——修改群名片"""
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_group_name()
        groupset.wait_for_modify_groupname_load()
        groupset.click_edit_group_name_back()
        groupset.wait_for_page_load()
        groupset.click_modify_group_name()
        groupset.save_group_name()
        groupset.wait_for_page_load()
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/group_name')), '测试群组1')
        groupset.click_modify_group_name()
        groupset.wait_for_modify_groupname_load()
        groupset.click_iv_delete_button()
        self.assertEqual(groupset.get_edit_query_text(), '请输入群聊名称')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0157():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0157(self):
        """群主——清除旧名片——录入一个汉字"""
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_my_group_name()
        groupset.wait_for_modify_mygroupname_load()
        groupset.clear_group_name()
        groupset.input_new_group_name("和")
        groupset.save_group_card_name()
        groupset.wait_for_page_load()
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/my_group_name')), '和')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0158():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0158(self):
        """群主——清除旧名片——录入5个汉字"""
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_my_group_name()
        groupset.wait_for_modify_mygroupname_load()
        groupset.clear_group_name()
        groupset.input_new_group_name("和飞信测试")
        groupset.save_group_card_name()
        groupset.wait_for_page_load()
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/my_group_name')), '和飞信测试')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0159():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0159(self):
        """群主——清除旧名片——录入10个汉字"""
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_my_group_name()
        groupset.wait_for_modify_mygroupname_load()
        groupset.clear_group_name()
        groupset.input_new_group_name("和飞信测试和飞信测试")
        groupset.save_group_card_name()
        groupset.wait_for_page_load()
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/my_group_name')), '和飞信测试和飞信测试')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0160():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0160(self):
        """群主——清除旧名片——录入11个汉字"""
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_my_group_name()
        groupset.wait_for_modify_mygroupname_load()
        groupset.clear_group_name()
        groupset.input_new_group_name("和飞信测试和飞信测试的")
        groupset.save_group_card_name()
        groupset.wait_for_page_load()
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/my_group_name')), '和飞信测试和飞信测试')

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0049():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0049(self):
        """消息-消息列表界面新建消息页面返回操作"""
        # 1.正常联网
        # 2.正常登录
        # 3.当前所在的页面是消息列表页面
        mess = MessagePage()
        # Step: 1.点击右上角的+号按钮
        mess.click_add_icon()
        mess.click_new_message()
        select_page = SelectContactPage()
        # checkpoint:1、成功进入新建消息界面
        # 判断存在选择联系人
        select_page.is_exist_select_contact_btn()
        # 判断存在搜索或输入手机号提示
        select_page.is_exist_selectorinput_toast()
        select_page.is_exist_selectortuandui_toast()
        # Setp: 2、点击左上角返回按钮
        select_page.click_back()
        # Checkpoint:2、退出新建消息，返回消息列表
        mess.wait_login_success()

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0276():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["给个红包1, 13800138000"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0276(self):
        """从发送短信进入单聊"""
        # 1.客户端已登录
        # 2.网络正常
        # 3.异网用户
        mess = MessagePage()
        # Step 1.点击右上角“+”
        mess.click_add_icon()
        # Step 2.点击发送短信
        mess.click_free_sms()
        freemsg = FreeMsgPage()
        # 若存在欢迎页面
        if freemsg.wait_is_exist_welcomepage():
            # 点击确定按钮
            freemsg.click_sure_btn()
            CallPage().wait_for_freemsg_load()
        select_page = SelectContactPage()
        # Checkpoint 进入联系人选择器（直接选择本地通讯录联系人)
        select_page.is_exist_select_contact_btn()
        # Checkpoint 进入联系人选择器（可在搜索框输入联系人姓名或电话号码搜索)
        select_page.is_exist_selectorinput_toast()
        # Checkpoint 进入联系人选择器（选择团队联系人)
        select_page.is_exist_selectortuandui_toast()
        # Step 3.任意选择一联系人
        ContactsSelector().click_local_contacts('给个红包1')
        # Checkpoint 进入短信编辑页面
        freemsg.wait_is_exist_wenhao()
        freemsg.wait_is_exist_exit()

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0283():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0283(self):
        """联系——标签分组——进入单聊页面"""
        # 1.客户端已登录
        # 2.网络正常
        # 3.在联系模块
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        # Step 1.点击上方标签分组图标
        contactspage.click_label_grouping()
        labelgroup = LabelGroupingPage()
        time.sleep(2)
        if '测试分组1' not in labelgroup.get_label_grouping_names():
            labelgroup.create_group('测试分组1', '测试短信1', '测试短信2')
        # Step 2.任意点击一存在多名成员的标签分组
        labelgroup.click_label_group('测试分组1')
        time.sleep(2)
        # Checkpoint 2.进入成员列表页，显示该标签分组中的所有成员
        contactspage.page_should_contain_text('测试短信1')
        contactspage.page_should_contain_text('测试短信2')
        # Step 3.任意选择一标签分组中的联系人
        BaseChatPage().click_to_do('测试短信1')
        # Checkpoint 3.进入联系人详情页面
        self.assertTrue(ContactDetailsPage().is_on_this_page())
        # Step 4.点击消息
        ContactDetailsPage().click_message_icon()
        time.sleep(2)
        # Checkpoint 4.进入单聊页面
        self.assertTrue(SingleChatPage().is_on_this_page())

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0284():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0284(self):
        """联系——标签分组——进入单聊页面"""
        # 1.客户端已登录
        # 2.网络正常
        # 3.在联系模块
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        # Step 1.点击上方标签分组图标
        contactspage.click_label_grouping()
        labelgroup = LabelGroupingPage()
        time.sleep(2)
        if '测试分组2' not in labelgroup.get_label_grouping_names():
            labelgroup.create_group('测试分组2', '测试短信1')
        # Step 2.点击只有一名成员的标签分组
        labelgroup.click_label_group('测试分组2')
        time.sleep(2)
        # Checkpoint 1.进入标签分组页面 2.进入成员列表页面
        contactspage.page_should_contain_text('测试短信1')
        # Step 3.点击群发消息按钮
        LableGroupDetailPage().click_send_smsall()
        time.sleep(2)
        # Checkpoint 3.进入群聊页面
        self.assertTrue(GroupChatPage().is_on_this_page())

    @staticmethod
    def setUp_test_msg_huangcaizui_B_0020():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0020(self):
        """验证编辑短信后不发送，是否信息草稿"""
        # 1.网络正常，本网用户
        # 2.客户端已登录
        # 3.首次使用发送短信，短信设置开关已开启
        # 4.已进入的单聊页面
        mess = MessagePage()
        # Step 1.点击右上角“+”
        mess.click_add_icon()
        # Step 点击下方发送短信按钮
        mess.click_free_sms()
        freemsg = FreeMsgPage()
        # 若存在欢迎页面
        if freemsg.wait_is_exist_welcomepage():
            # 点击确定按钮
            freemsg.click_sure_btn()
            CallPage().wait_for_freemsg_load()
        ContactsSelector().click_local_contacts('测试短信1')
        singe_chat = SingleChatPage()
        chatdialog = ChatNoticeDialog()
        # Checkpoint 2.进入发送短信页面
        singe_chat.input_sms_message("测试前一半")
        # 点击发送按钮
        singe_chat.send_sms()
        if singe_chat.is_present_sms_fee_remind():
            singe_chat.click_sure()
        # Step 输入想存为草稿的内容
        singe_chat.input_sms_message('测试后一半')
        # Step 3.编辑好短信，点击系统返回按钮
        singe_chat.click_back()
        # Checkpoint 回到消息列表页面，并显示未发送的短信草稿
        time.sleep(2)
        chatdialog.page_should_contain_text('[草稿] ')
        chatdialog.page_should_contain_text('测试短信1')
        chatdialog.page_should_contain_text('测试后一半')
        # Step 4.再次点击进入
        mess.click_message('测试短信1')
        # Checkpoint 进入短信编辑页面，可继续编辑该短信
        singe_chat.clear_inputtext()
        singe_chat.click_back()

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0024():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        Preconditions.create_contacts_if_not_exist(["转发短信1, 13800138114"])
        Preconditions.create_contacts_if_not_exist(["转发短信2, 13800138113"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_E_0024(self):
        """查看更多聊天记录"""
        # 1、联网正常
        # 2、已登录客户端
        # 3、当前聊天页面搜索页面
        # 4、同一个群或联系人有多条相同的聊天记录
        mess = MessagePage()
        # Step 1.点击右上角“+”
        mess.click_add_icon()
        # Step 点击下方发送短信按钮
        mess.click_free_sms()
        freemsg = FreeMsgPage()
        # 若存在欢迎页面
        if freemsg.wait_is_exist_welcomepage():
            # 点击确定按钮
            freemsg.click_sure_btn()
            CallPage().wait_for_freemsg_load()
        ContactsSelector().click_local_contacts('转发短信1')
        singe_chat = SingleChatPage()
        singe_chat.wait_for_page_load()
        singe_chat.clear_msg()
        singe_chat.input_sms_message("发送第一条")
        # 点击发送按钮
        singe_chat.send_sms()
        if singe_chat.is_present_sms_fee_remind():
            singe_chat.click_sure()
        singe_chat.input_sms_message("发送第一条")
        singe_chat.send_sms()
        singe_chat.click_back()
        mess.click_search()
        # Step 1.搜索框输入一条有多条相同的聊天记录
        SearchPage().input_search_keyword("发送第一条")
        # 选择联系人进入联系人页
        time.sleep(2)
        current_mobile().hide_keyboard_if_display()
        # Checkpoint 1.显示有这条聊天记录的群名或联系人，并显示对应聊天记录的数量
        mess.page_should_contain_text('转发短信1')
        mess.page_should_contain_text('2条相关聊天记录')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0207():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        # 预置联系人
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0207(self):
        """群聊设置页面——查找聊天内容——英文搜索——搜索结果展示"""
        mess = MessagePage()
        # 1.、成功登录和飞信
        # 2、已创建或者加入群聊
        # 3、群主、普通成员
        # 4、聊天会话页面不存在文本消息
        # 预置群聊
        Preconditions.create_group_if_not_exist_not_enter_chat('测试群组1', "测试短信1", "测试短信2")
        # Step 进入群聊页面
        mess.search_and_enter('测试群组1')

        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.click_setting()
        groupset.wait_for_page_load()
        # Step 聊天会话页面不存在文本，清除聊天记录
        groupset.click_clear_chat_record()
        groupset.wait_clear_chat_record_confirmation_box_load()
        groupset.click_sure()
        # Step 进入查找聊天内容页面
        groupset.click_find_chat_record()
        search = GroupChatSetFindChatContentPage()
        search.wait_for_page_load()
        # Step 1、在查找聊天内容页面，输入框中，输入英文字母作为搜索条件
        search.search('AAVBVAW')
        # Checkpoint 展示无搜索结果
        search.check_no_search_result()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0208():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        # 预置联系人
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0208(self):
        """群聊设置页面——查找聊天内容——特殊字符搜索——搜索结果展示"""
        mess = MessagePage()
        # 1.、成功登录和飞信
        # 2、已创建或者加入群聊
        # 3、群主、普通成员
        # 4、聊天会话页面不存在文本消息
        # 预置群聊
        Preconditions.create_group_if_not_exist_not_enter_chat('测试群组1', "测试短信1", "测试短信2")
        # Step 进入群聊页面
        mess.search_and_enter('测试群组1')

        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.click_setting()
        groupset.wait_for_page_load()
        # Step 聊天会话页面不存在文本，清除聊天记录
        groupset.click_clear_chat_record()
        groupset.wait_clear_chat_record_confirmation_box_load()
        groupset.click_sure()
        # Step 进入查找聊天内容页面
        groupset.click_find_chat_record()
        search = GroupChatSetFindChatContentPage()
        search.wait_for_page_load()
        # Step 1、在查找聊天内容页面，输入框中，输入特殊字符字母作为搜索条件
        search.search('!@#$%')
        # Checkpoint 展示无搜索结果
        search.check_no_search_result()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0212():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        # 预置联系人
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0212(self):
        """群聊设置页面——查找聊天内容——特殊字符搜索——搜索结果展示"""
        mess = MessagePage()
        # 1.、成功登录和飞信
        # 2、已创建或者加入群聊
        # 3、群主、普通成员
        # 4、聊天会话页面不存在文本消息
        # 预置群聊
        Preconditions.create_group_if_not_exist_not_enter_chat('测试群组1', "测试短信1", "测试短信2")
        # Step 进入群聊页面
        mess.search_and_enter('测试群组1')

        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.click_setting()
        groupset.wait_for_page_load()
        # Step 聊天会话页面不存在文本，清除聊天记录
        groupset.click_clear_chat_record()
        groupset.wait_clear_chat_record_confirmation_box_load()
        groupset.click_sure()
        groupset.click_back()
        SingleChatPage().send_text_if_not_exist("九个一个的")
        groupchat.click_setting()
        groupset.wait_for_page_load()
        # Step 进入查找聊天内容页面
        groupset.click_find_chat_record()
        search = GroupChatSetFindChatContentPage()
        search.wait_for_page_load()
        # Step 1、在查找聊天内容页面，输入框中，输入搜索条件搜索
        search.search('无赖地痞别跑')
        # Checkpoint 展示无搜索结果
        search.check_no_search_result()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0216():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        # 预置联系人
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0216(self):
        """群聊设置页面——关闭消息免打扰——网络断网"""
        mess = MessagePage()
        # 1.、成功登录和飞信
        # 2、已创建或者加入群聊
        # 3、群主、普通成员
        # 4、网络断网
        # 5、消息免打扰开启状态
        # 预置群聊
        Preconditions.create_group_if_not_exist_not_enter_chat('测试群组5', "测试短信1", "测试短信2")
        # Step 进入群聊页面
        mess.search_and_enter('测试群组5')

        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.click_setting()
        groupset.wait_for_page_load()
        # Step 消息免打扰开启状态
        if not groupset.get_switch_undisturb_status():
            groupset.click_switch_undisturb()
        time.sleep(2)
        # Step 网络断网
        current_mobile().set_network_status(0)
        time.sleep(2)
        # Step 点击关闭消息免打扰开关
        groupset.click_switch_undisturb()
        # Checkpoint 会弹出toast提示：无网络，请连接网络重试
        mess.is_toast_exist("无网络，请连接网络重试")
        current_mobile().set_network_status(6)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0216():
        current_mobile().set_network_status(6)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0217():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        # 预置联系人
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0217(self):
        """群聊设置页面——关闭消息免打扰——网络断网"""
        mess = MessagePage()
        # 1.、成功登录和飞信
        # 2、已创建或者加入群聊
        # 3、群主、普通成员
        # 4、网络断网
        # 5、消息免打扰关闭状态
        # 预置群聊
        Preconditions.create_group_if_not_exist_not_enter_chat('测试群组5', "测试短信1", "测试短信2")
        # Step 进入群聊页面
        mess.search_and_enter('测试群组5')

        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.click_setting()
        groupset.wait_for_page_load()
        # Step 消息免打扰关闭状态
        if groupset.get_switch_undisturb_status():
            groupset.click_switch_undisturb()
        time.sleep(2)
        # Step 网络断网
        current_mobile().set_network_status(0)
        time.sleep(2)
        # Step 点击打开消息免打扰开关
        groupset.click_switch_undisturb()
        # Checkpoint 会弹出toast提示：无网络，请连接网络重试
        mess.is_toast_exist("无网络，请连接网络重试")

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0217():
        current_mobile().set_network_status(6)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0223():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        # 预置联系人
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0223(self):
        """聊天设置页面——清空聊天记录"""
        mess = MessagePage()
        # 1、已成功登录和飞信
        # 2、已创建一个群聊
        # 3、群主、普通成员
        # 4、聊天会话页面存在记录
        # 预置群聊
        Preconditions.create_group_if_not_exist_not_enter_chat('测试群组1', "测试短信1", "测试短信2")
        # Step 进入群聊页面
        mess.search_and_enter('测试群组1')

        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        # Step 1、点击【设置】
        groupchat.click_setting()
        # Checkpoint 进入“设置”页面
        groupset.wait_for_page_load()
        # Step 点击【清空聊天记录】
        groupset.click_clear_chat_record()
        groupset.wait_clear_chat_record_confirmation_box_load()
        groupset.click_sure()
        # Checkpoint 会弹出toast提示：无网络，请连接网络重试
        mess.is_toast_exist("聊天记录清除成功")

    @staticmethod
    def setUp_test_msg_xiaoqiu_0226():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0226(self):
        """聊天设置页面——删除并退出群聊——群成员"""
        # 1、已成功登录和飞信
        # 2、已加入群聊
        # 3、普通成员
        # 4、群人数小于：3
        # 5、网络正常（4G/WIFI ）
        mess = MessagePage()
        Preconditions.create_group_if_not_exist_not_enter_chat('测试群组1', "测试短信1", "测试短信2")
        mess.search_and_enter('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        # Step 在聊天设置页面
        groupchat.click_setting()
        groupset.wait_for_page_load()
        groupset.click_delete_and_exit()
        # Step 点击页面底部的“删除并退出”按钮
        SearchPage().click_back_button()
        # Checkpoint 会退出当前群聊返回到消息列表并收到一条系统消息：你已退出群
        ContactsPage().select_people_by_name("系统消息")
        mess.page_should_contain_text("你已退出群")
        mess.page_should_contain_text("来自群聊测试群组1")

    @staticmethod
    def setUp_test_msg_xiaoqiu_0229():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0229(self):
        """聊天设置页面——删除并退出群聊——群主"""
        # 1、已成功登录和飞信
        # 2、已加入群聊
        # 3、群主权限
        # 4、群人数小于：3
        # 5、网络正常（4G/WIFI ）
        mess = MessagePage()
        Preconditions.create_group_if_not_exist_not_enter_chat('测试群组1', "测试短信1", "测试短信2")
        mess.search_and_enter('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        # Step 在聊天设置页面
        groupchat.click_setting()
        groupset.wait_for_page_load()
        # Step 点击页面底部的“删除并退出”按钮 点击确定
        groupset.click_delete_and_exit()
        SearchPage().click_back_button()
        # Checkpoint 返回到消息列表并收到一条系统消息，该群已解散
        ContactsPage().select_people_by_name("系统消息")
        mess.page_should_contain_text('你已退出群')
        mess.page_should_contain_text('来自群聊测试群组1')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0250():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0250(self):
        """消息列表——群聊天会话窗口——发送的消息类型展示"""
        # 1、已成功登录和飞信
        # 2、网络正常（4G/WIFI ）
        # 3、消息列表页面
        # 4、发送消息类型展示
        mess = MessagePage()
        Preconditions.create_group_if_not_exist_not_enter_chat('测试群组1', "测试短信1", "测试短信2")
        mess.search_and_enter('测试群组1')
        # Step 群聊会话页面中，发送到新消息
        single = SingleChatPage()
        if not single.is_text_present('测试一个呵呵'):
            single.input_text_message("测试一个呵呵")
            single.send_text()
        mess.click_back()
        SearchPage().click_back_button()
        # Checkpoint 会在消息列表的会话窗口展示：接发送消息的类型或者类型+内容展示
        mess.is_on_this_page()
        mess.page_should_contain_text('测试群组1')
        mess.page_should_contain_text('测试一个呵呵')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0251():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0251(self):
        """群名称过长时——展示"""
        # 1、已成功登录和飞信
        # 2、网络正常（4G/WIFI ）
        # 3、消息列表页面
        groupchat = GroupChatPage()
        # Step 预置群聊
        Preconditions.create_group_if_not_exist('123456789012345678901234567890', "测试短信1", "测试短信2")
        # Checkpoint 用省略号隐藏群名称的中间名称，只展示前后名称
        self.assertEqual(groupchat.get_group_name(), '123456789012345678901234567890(1)')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0269():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0269(self):
        """普通群——聊天会话页面——未进群联系人展示"""
        # 1、已成功登录和飞信
        # 2、网络正常（4G/WIFI ）
        # 3、群主权限
        mess = MessagePage()
        Preconditions.create_group_if_not_exist_not_enter_chat('测试群组3', "测试短信1", "测试短信2")
        mess.search_and_enter('测试群组3')
        # Step 存在未进群的联系人时，在聊天会话页面，发送一条消息
        single = SingleChatPage()
        if not single.is_text_present('测试一个呵呵'):
            single.input_text_message("测试一个呵呵")
            single.send_text()
        # Checkpoint 提示：还有人未进群，再次邀请
        time.sleep(2)
        mess.page_should_contain_text('还有人未进群,再次邀请')
        # Step 再次发送3次消息
        count = 0
        while count <= 2:
            single.input_text_message("测试一个呵呵")
            single.send_text()
            time.sleep(5)
            count = count + 1
        # Checkpoint 一共只有3个提示
        mess.check_group_toast_num()
        GroupChatPage().click_setting()
        GroupChatSetPage().wait_for_page_load()
        GroupChatSetPage().click_delete_and_exit()

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0091():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist_631(["测试短信1, 13800138111", "测试短信2, 13800138112"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0091(self):
        """一对一聊天设置创建群聊"""
        # 1.已有一对一的聊天窗口
        mess = MessagePage()
        singlechat = SingleChatPage()
        # Step 1.进入一对一聊天窗口
        mess.search_and_enter_631('测试短信1')
        ContactDetailsPage().click_message_icon()
        singlechat.wait_for_page_load()
        # Step 2.点击进入聊天设置，再点击+添加成员
        singlechat.click_setting()
        SingleChatSetPage().click_add_icon()
        # Step 3.选择一个或多个成员,点击确定
        ContactsSelector().select_local_contacts('测试短信2')
        # Checkpoint 1.进入群聊名称设置
        GroupNamePage().wait_for_page_load_631()

    @staticmethod
    def setUp_test_msg_huangmianhua_0187():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'middle')
    def test_msg_huangmianhua_0187(self):
        """通讯录——群聊——搜索——选择一个群"""
        # 1.正常联网
        # 2.正常登录
        # 3.当前所在的页面是消息列表页面
        # 4、存在跟搜索条件匹配的群聊
        # 5、通讯录 - 群聊
        groupchat = MessagePage()
        # Step:1、点击右上角的+号
        groupchat.click_add_icon()
        # 点击 发起群聊
        groupchat.click_group_chat()
        # Step:2、点击选择一个群
        groupchat.click_element_by_text("选择一个群")
        # CheckPoint：是否可以进入到群聊列表展示页面

        # Step: 3、点击搜索群组
        groupchat.click_element_by_text("搜索群组")
        # 进行中文模糊搜索
        global_search_group_page = GlobalSearchGroupPage()
        global_search_group_page.search("群")
        # CheckPoint：检测是否有包含名为"群聊"的群
        self.assertIsNotNone(global_search_group_page.is_group_in_list("群聊"))

    @staticmethod
    def setUp_test_msg_huangmianhua_0188():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'middle')
    def test_msg_huangmianhua_0188(self):
        """通讯录-群聊-中文模糊搜索——搜索结果展示"""
        # 1.正常联网
        # 2.正常登录
        # 3.当前所在的页面是消息列表页面
        # 4、中文模糊搜索，是否可以匹配展示搜索结果
        # 5、通讯录 - 群聊
        groupchat = MessagePage()
        # Step:1、点击通讯
        groupchat.open_contacts_page()
        # Step:2、点击选择一个群
        groupchat.click_element_by_text("群聊")
        # Step: 3、点击搜索群组
        groupchat.click_element_by_text("搜索群组")
        # 进行中文模糊搜索
        global_search_group_page = GlobalSearchGroupPage()
        global_search_group_page.search("群")
        # CheckPoint：中文模糊搜索，是否可以匹配展示搜索结果
        self.assertIsNotNone(global_search_group_page.is_group_in_list("群聊"))
        self.assertTrue(global_search_group_page.is_toast_exist("无搜索结果"))

    @staticmethod
    def setUp_test_msg_huangmianhua_0189():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'middle')
    def test_msg_huangmianhua_0189(self):
        """通讯录-群聊-中文精确搜索——搜索结果展示"""
        # 1.正常联网
        # 2.正常登录
        # 3.当前所在的页面是消息列表页面
        # 4、中文精确搜索，是否可以匹配展示搜索结果
        # 5、通讯录 - 群聊
        groupchat = MessagePage()
        # Step:1、点击通讯
        groupchat.open_contacts_page()
        # Step:2、点击选择一个群
        groupchat.click_element_by_text("群聊")
        # Step: 3、点击搜索群组
        groupchat.click_element_by_text("搜索群组")
        # 进行中文精确搜索
        global_search_group_page = GlobalSearchGroupPage()
        global_search_group_page.search("群聊")
        # CheckPoint：中文精确搜索，是否可以匹配展示搜索结果
        # self.assertIsNotNone(global_search_group_page.is_group_in_list("群聊"))
        self.assertTrue(global_search_group_page.is_toast_exist("群聊"))

    @staticmethod
    def setUp_test_msg_huangmianhua_0190():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'middle')
    def test_msg_huangmianhua_0190(self):
        """通讯录-群聊-中文精确搜索——搜索结果展示"""
        # 1.正常联网
        # 2.正常登录
        # 3.当前所在的页面是消息列表页面
        # 4、中文精确搜索，不存在跟搜索条件匹配的群聊
        # 5、通讯录 - 群聊
        groupchat = MessagePage()
        # Step:1、点击通讯
        groupchat.open_contacts_page()
        # Step:2、点击选择一个群
        groupchat.click_element_by_text("群聊")
        # Step: 3、点击搜索群组
        groupchat.click_element_by_text("搜索群组")
        # Step: 4、进行中文精确搜索
        global_search_group_page = GlobalSearchGroupPage()
        global_search_group_page.search("测试")
        # CheckPoint：中文精确搜索，不存在跟搜索条件匹配的群聊
        # self.assertIsNotNone(global_search_group_page.is_group_in_list("群聊"))
        self.assertTrue(global_search_group_page.is_toast_exist("无搜索结果"))