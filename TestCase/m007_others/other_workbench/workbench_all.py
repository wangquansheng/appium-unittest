import warnings

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
    def get_label_grouping_name():
        """获取群名"""
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "ateam" + phone_number[-4:]
        return group_name

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

    @staticmethod
    def make_already_have_used_free_sms2():
        """确保非首次使用免费短信功能"""
        mp = MessagePage()
        mp.click_add_icon()
        mp.click_free_sms()
        time.sleep(1)
        if FreeMsgPage().is_exist_cancle_btn():
            FreeMsgPage().click_sure_btn()
            time.sleep(1)
            SelectContactsPage().click_search_contact()
            current_mobile().hide_keyboard_if_display()


class MsgAllPrior(TestCase):

    # @classmethod
    # def setUpClass(cls):
    #     warnings.simplefilter('ignore', ResourceWarning)
    #     Preconditions.select_mobile('Android-移动')
    #     # 导入测试联系人、群聊
    #     fail_time1 = 0
    #     flag1 = False
    #     import dataproviders
    #     while fail_time1 < 2:
    #         try:
    #             required_contacts = dataproviders.get_preset_contacts()
    #             conts = ContactsPage()
    #             current_mobile().hide_keyboard_if_display()
    #             Preconditions.make_already_in_message_page()
    #             conts.open_contacts_page()
    #             try:
    #                 if conts.is_text_present("发现SIM卡联系人"):
    #                     conts.click_text("显示")
    #             except:
    #                 pass
    #             for name, number in required_contacts:
    #                 # 创建联系人
    #                 conts.create_contacts_if_not_exits(name, number)
    #             required_group_chats = dataproviders.get_preset_group_chats()
    #             conts.open_group_chat_list()
    #             group_list = GroupListPage()
    #             for group_name, members in required_group_chats:
    #                 group_list.wait_for_page_load()
    #                 # 创建群
    #                 group_list.create_group_chats_if_not_exits(group_name, members)
    #             group_list.click_back()
    #             conts.open_message_page()
    #             flag1 = True
    #         except:
    #             fail_time1 += 1
    #         if flag1:
    #             break
    #
    #     # 导入团队联系人
    #     fail_time2 = 0
    #     flag2 = False
    #     while fail_time2 < 5:
    #         try:
    #             Preconditions.make_already_in_message_page()
    #             contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
    #             Preconditions.create_he_contacts(contact_names)
    #             flag2 = True
    #         except:
    #             fail_time2 += 1
    #         if flag2:
    #             break
    #
    #     # 确保有企业群
    #     fail_time3 = 0
    #     flag3 = False
    #     while fail_time3 < 5:
    #         try:
    #             Preconditions.make_already_in_message_page()
    #             Preconditions.ensure_have_enterprise_group()
    #             flag3 = True
    #         except:
    #             fail_time3 += 1
    #         if flag3:
    #             break
    #
    #     # 确保测试手机有resource文件夹
    #     name = "群聊1"
    #     Preconditions.get_into_group_chat_page(name)
    #     gcp = GroupChatPage()
    #     gcp.wait_for_page_load()
    #     cmp = ChatMorePage()
    #     cmp.click_file()
    #     csfp = ChatSelectFilePage()
    #     csfp.wait_for_page_load()
    #     csfp.click_local_file()
    #     local_file = ChatSelectLocalFilePage()
    #     # 没有预置文件，则上传
    #     local_file.push_preset_file()
    #     local_file.click_back()
    #     csfp.wait_for_page_load()
    #     csfp.click_back()
    #     gcp.wait_for_page_load()

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
        # 点击返回，并判断是否正常
        # slc = SelectContactsPage()
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

    @tags('ALL', 'CMCC', 'freemsg', "high")
    def test_msg_huangcaizui_B_0036(self):
        """转发短信"""
        # 1.网络正常，本网用户
        # 2.客户端已登录
        # 3.本机已发送短信
        Preconditions.make_already_have_used_free_sms2()
        # Step: 1、进入单聊会话页面
        slc = SelectLocalContactsPage()
        slc.selecting_local_contacts_by_name("测试号码")
        basepg = BaseChatPage()
        time.sleep(2)
        basepg.input_free_message("测试短信")
        basepg.hide_keyboard()
        time.sleep(1)
        basepg.click_send_sms()
        basepg.click_sure_send_sms()
        time.sleep(2)
        # 2、长按短信
        basepg.press_file_to_do("测试短信", "转发")
        time.sleep(2)
        # 3、点击转发按钮
        # CheckPoint: 选择转发会调起联系人选择器，转发短信成功
        basepg.page_should_contain_text("选择联系人")
        time.sleep(1)
        # 4、选择转发联系人
        SelectContactsPage().search("14775970982")
        time.sleep(3)
        SelectContactsPage().select_one_contact_by_name('测试号码')
        # 5、点击发送
        SelectLocalContactsPage().click_sure_forward()
        # CheckPoint: 选择转发会调起联系人选择器，转发短信成功
        self.assertTrue(basepg.is_toast_exist("已转发"))
        time.sleep(2)
        if basepg.is_exist_exit_sms():
            basepg.click_exit_sms()
        time.sleep(1)
        basepg.click_back_by_android()

    @staticmethod
    def tearDown_test_msg_huangcaizui_B_0036():
        Preconditions.make_already_in_message_page()
        MessagePage().clear_message_record()

    @tags('ALL', 'CMCC', 'freemsg', "high")
    def test_msg_huangcaizui_B_0037(self):
        """删除短信"""
        # 1.网络正常，本网用户
        # 2.客户端已登录
        # 3.本机已发送短信
        Preconditions.make_already_have_used_free_sms2()
        # Step: 1、进入单聊会话页面
        slc = SelectLocalContactsPage()
        slc.selecting_local_contacts_by_name("测试号码")
        time.sleep(2)
        basepg = BaseChatPage()
        basepg.input_free_message("测试短信，请勿回复")
        time.sleep(2)
        basepg.click_send_sms()
        basepg.click_sure_send_sms()
        time.sleep(2)
        # 2、长按短信
        basepg = BaseChatPage()
        basepg.press_file_to_do("测试短信，请勿回复", "删除")

    @staticmethod
    def tearDown_test_msg_huangcaizui_B_0037():
        Preconditions.make_already_in_message_page()
        MessagePage().clear_message_record()

    @tags('ALL', 'CMCC', 'freemsg', "high")
    def test_msg_huangcaizui_B_0038(self):
        """复制短信"""
        # 1.网络正常，本网用户
        # 2.客户端已登录
        # 3.本机已发送短信
        Preconditions.make_already_have_used_free_sms2()
        # Step: 1、进入单聊会话页面
        slc = SelectLocalContactsPage()
        slc.selecting_local_contacts_by_name("测试号码")
        time.sleep(2)
        basepg = BaseChatPage()
        basepg.input_free_message("测试短信，请勿回复")
        basepg.hide_keyboard()
        time.sleep(2)
        basepg.click_send_sms()
        basepg.click_sure_send_sms()
        time.sleep(2)
        # 2、长按短信
        basepg = BaseChatPage()
        basepg.press_file_to_do("测试短信，请勿回复", "复制")

    @staticmethod
    def tearDown_test_msg_huangcaizui_B_0038():
        Preconditions.make_already_in_message_page()
        MessagePage().clear_message_record()

    @tags('ALL', 'CMCC', 'freemsg', "high")
    def test_msg_huangcaizui_B_0039(self):
        """收藏短信"""
        # 1.网络正常，本网用户
        # 2.客户端已登录
        # 3.本机已发送短信
        Preconditions.make_already_have_used_free_sms2()
        # Step: 1、进入单聊会话页面
        slc = SelectLocalContactsPage()
        slc.selecting_local_contacts_by_name("测试号码")
        time.sleep(2)
        basepg = BaseChatPage()
        basepg.input_free_message("测试短信，请勿回复")
        time.sleep(2)
        basepg.click_send_sms()
        basepg.click_sure_send_sms()
        time.sleep(2)
        # 2、长按短信
        basepg = BaseChatPage()
        basepg.press_file_to_do("测试短信，请勿回复", "收藏")

    @staticmethod
    def tearDown_test_msg_huangcaizui_B_0039():
        Preconditions.make_already_in_message_page()
        MessagePage().clear_message_record()

    @tags('ALL', 'CMCC', 'freemsg', "high")
    def test_msg_huangcaizui_B_0040(self):
        """多选，批量转发与删除短信"""
        # 1.网络正常，本网用户
        # 2.客户端已登录
        # 3.本机已发送短信
        Preconditions.make_already_have_used_free_sms2()
        # Step: 1、进入单聊会话页面
        slc = SelectLocalContactsPage()
        slc.selecting_local_contacts_by_name("测试号码")
        time.sleep(2)
        basepg = BaseChatPage()
        basepg.input_free_message("测试短信，请勿回复")
        basepg.hide_keyboard()
        time.sleep(2)
        basepg.click_send_sms()
        basepg.click_sure_send_sms()
        time.sleep(2)
        # 2、长按短信
        basepg = BaseChatPage()
        basepg.press_mess("测试短信，请勿回复")
        time.sleep(2)
        # 3、点击多选按钮
        basepg.click_multiple_selection()
        time.sleep(1)

    @staticmethod
    def tearDown_test_msg_huangcaizui_B_0040():
        Preconditions.make_already_in_message_page()
        MessagePage().clear_message_record()

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
        mess = MessagePage()
        # 点击+号
        mess.click_add_icon()
        # 点击免费短信
        mess.click_free_sms()
        mess_call_page = CallPage()
        freemsg = FreeMsgPage()
        # 若存在欢迎页面
        if freemsg.is_exist_welcomepage():
            # 点击确定按钮
            freemsg.click_sure_btn()
            time.sleep(2)
            # 若存在权限控制
            if mess_call_page.is_exist_allow_button():
                # 存在提示点击允许
                mess_call_page.wait_for_freemsg_load()
        select_page = SelectContactsPage()
        # 按姓名搜索存在联系人
        select_page.search('给个红包1')
        time.sleep(1)
        mess.page_should_contain_text('手机联系人')
        mess.page_should_contain_text('给个红包1')
        mess.page_should_contain_text('13800138000')
        mess.page_should_contain_text('搜索团队联系人 : 给个红包1')
        # 按手机号搜索存在联系人
        select_page.search('13800138000')
        time.sleep(1)
        mess.page_should_contain_text('手机联系人')
        mess.page_should_contain_text('给个红包1')
        mess.page_should_contain_text('13800138000')
        mess.page_should_contain_text('搜索团队联系人 : 13800138000')
        # 按手机号搜索不存在联系人
        select_page.search('199815')
        time.sleep(1)
        mess.page_should_not_contain_text('手机联系人')
        mess.page_should_contain_text('搜索团队联系人 : 199815')
        # 无手机联系人且搜索手机号时
        select_page.search('19981512581')
        time.sleep(1)
        mess.page_should_contain_text('网络搜索')
        mess.page_should_contain_text('搜索团队联系人 : 19981512581')
        select_page.is_present_unknown_member()
        # 搜索我的电脑
        select_page.search('我的电脑')
        time.sleep(1)
        mess.page_should_not_contain_text('手机联系人')
        mess.page_should_contain_text('搜索团队联系人 : 我的电脑')

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
        Preconditions.make_already_in_message_page()
        Preconditions.enter_single_chat_page("大佬2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0125(self):
        """将自己发送的文件转发到我的电脑"""
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
        SelectContactsPage().wait_for_page_load()
        SelectContactsPage().search('我的电脑')
        SelectOneGroupPage().click_search_result()
        SelectOneGroupPage().click_sure_forward()
        flag = scp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的文件时，没有‘已转发’提示")


    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0126():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_single_chat_page("大佬2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0126(self):
        """将自己发送的文件转发到最近聊天"""
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
        SelectContactsPage().wait_for_page_load()
        select_recent_chat = SelectContactsPage()
        select_recent_chat.wait_for_page_load()
        select_recent_chat.select_recent_chat_by_number(0)
        SelectContactsPage().click_sure_forward()
        flag = scp.is_toast_exist("已转发")
        if not flag:
            raise AssertionError("在转发发送自己的文件时，没有‘已转发’提示")

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0129():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_single_chat_page("大佬2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0129(self):
        """对自己发送出去的文件消息进行删除"""
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
        # 长按删除xls文件
        ChatFilePage().delete_file('.xlsx')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0392(self):
        """会控页未创建会场成功时（12560未回呼）添加成员按钮置灰"""
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
        # callpage = CallPage()
        # aa = callpage.is_phone_in_calling_state()
        # self.assertTrue(aa)
        # # 挂断系统电话
        # callpage.hang_up_the_call()
        # time.sleep(5)
        # # checkpoint: 刚才拨打的类型为【电话】,号码包含12560
        # callpage.is_type_hefeixin(0, '电话')

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
        Preconditions.enter_single_chat_page("大佬2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0354(self):
        """单聊-位置"""
        chat_window_page = ChatWindowPage()
        chat_window_page.click_add_icon()
        chat_window_page.click_menu_icon('位置')
        # elements = chat_window_page.get_elements(
        #     (MobileBy.XPATH, '//*[@resource-id="com.lbe.security.miui:id/permission_message"]'))
        # self.assertTrue(len(elements) > 0)

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0433():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_single_chat_page("大佬2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0433(self):
        """未开启位置权限时点击位置按钮后有位置权限申请的弹窗"""
        chat_window_page = ChatWindowPage()
        chat_window_page.click_add_icon()
        chat_window_page.click_menu_icon('位置')
        # elements = chat_window_page.get_elements(
        #     (MobileBy.XPATH, '//*[@resource-id="com.lbe.security.miui:id/permission_message"]'))
        # self.assertTrue(len(elements) > 0)

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0436():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_single_chat_page("大佬2")

    def make_sure_have_loc_msg(self):
        group_chat_page = GroupChatPage()
        # group_chat_page.wait_for_page_load()
        if group_chat_page.is_exist_loc_msg():
            pass
        else:
            chat_more = ChatMorePage()
            chat_more.close_more()
            chat_more.click_location()
            location_page = ChatLocationPage()
            location_page.wait_for_page_load()
            time.sleep(1)
            # 点击发送按钮
            if not location_page.send_btn_is_enabled():
                raise AssertionError("位置页面发送按钮不可点击")
            location_page.click_send()
            # group_chat_page.wait_for_page_load()
            group_chat_page.click_more()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0436(self):
        """长按发送出去的位置消息体进行转发、删除、收藏、撤回等操作"""
        self.make_sure_have_loc_msg()
        SingleChatPage().press_message_to_do("转发")

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0437():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_single_chat_page("大佬2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0437(self):
        """点击位置消息体进入到位置详情页面，可以进行导航操作"""
        self.make_sure_have_loc_msg()
        gcp = GroupChatPage()
        gcp.click_addr_info()
        # 等待页面加载
        gcp.wait_for_location_page_load()
        # 点击右下角按钮
        gcp.click_nav_btn()
        # 判断是否有手机导航应用
        if gcp.is_toast_exist("未发现手机导航应用", timeout=5):
            pass
        else:
            time.sleep(3)
            map_flag = gcp.is_text_present("地图")
            self.assertTrue(map_flag)
            gcp.tap_coordinate([(100, 20), (100, 60), (100, 100)])
            gcp.click_location_back()
            time.sleep(2)

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0445():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_single_chat_page("大佬2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0445(self):
        """在位置搜索页面选择搜索结果，网络正常时进行发送位置消息"""
        self.make_sure_have_loc_msg()

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0450():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_single_chat_page("大佬2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0450(self):
        """在地图界面滑动地图进行定位后点击发送按钮"""
        self.make_sure_have_loc_msg()
        gcp = GroupChatPage()
        gcp.click_addr_info()
        # 等待页面加载
        gcp.wait_for_location_page_load()
        # 点击右下角按钮
        gcp.click_nav_btn()
        # 判断是否有手机导航应用
        if gcp.is_toast_exist("未发现手机导航应用", timeout=5):
            pass
        else:
            time.sleep(3)
            map_flag = gcp.is_text_present("地图")
            self.assertTrue(map_flag)
            gcp.tap_coordinate([(100, 20), (100, 60), (100, 100)])
            gcp.click_location_back()
            time.sleep(2)

    @staticmethod
    def setUp_test_msg_weifenglian_PC_0042():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_my_computer_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_PC_0042(self):
        """勾选音乐列表页面任意音乐点击发送按钮"""
        gcp = GroupChatPage()
        # 点击更多富媒体按钮
        gcp.click_more()
        # 点击文件按钮
        more_page = ChatMorePage()
        more_page.click_file()
        # 点击音乐选项
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_music()
        # 选择一个音乐文件发送
        local_file = ChatSelectLocalFilePage()
        local_file.wait_for_page_loads()
        el = local_file.select_file2("音乐")
        if el:
            local_file.click_send()
            # gcp.wait_for_page_load()
        else:
            raise AssertionError("There is no music")

    @staticmethod
    def setUp_test_msg_huangcaizui_D_0048():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_my_computer_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0048(self):
        """在我的电脑会话窗，验证点击趣图搜搜入口"""
        chat = SingleChatPage()
        gif = ChatGIFPage()
        if gif.is_gif_exist():
            gif.close_gif()
        gif.click_expression_icon()
        time.sleep(1)
        chat.click_gif()
        gif.wait_for_page_load()
        # 进入趣图选择页面
        if not gif.is_gif_exist():
            raise AssertionError("趣图页面无gif趣图")
        gif.close_gif()

    @staticmethod
    def setUp_test_msg_huangcaizui_D_0049():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_my_computer_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0049(self):
        """在我的电脑会话窗，网络正常发送表情搜搜"""
        chat = SingleChatPage()
        gif = ChatGIFPage()
        if gif.is_gif_exist():
            gif.close_gif()
        gif.click_expression_icon()
        time.sleep(1)
        chat.click_gif()
        gif.wait_for_page_load()
        # 2、选择表情点击发送
        gif.send_gif()
        gif.close_gif()
        current_mobile().hide_keyboard_if_display()
        if not chat.is_exist_pic_msg():
            raise AssertionError("发送表情后，在单聊会话窗无表情趣图存在")

    @staticmethod
    def setUp_test_msg_huangcaizui_D_0051():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_my_computer_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0051(self):
        """在我的电脑会话窗，搜索数字关键字选择发送趣图"""
        chat = SingleChatPage()
        gif = ChatGIFPage()
        if gif.is_gif_exist():
            gif.close_gif()
        gif.click_expression_icon()
        time.sleep(1)
        chat.click_gif()
        gif.wait_for_page_load()
        # 2、搜索框输入数字
        nums = ['1', '2', '6', '666', '8']
        for msg in nums:
            gif.input_message(msg)
            if not gif.is_toast_exist("无搜索结果，换个热词试试", timeout=4):
                # 3、点击选择表情
                gif.send_gif()
                gif.input_message("")
                gif.close_gif()
                current_mobile().hide_keyboard_if_display()
                if not chat.is_exist_pic_msg():
                    raise AssertionError("发送gif后，在单聊会话窗无gif")
                return

    @staticmethod
    def setUp_test_msg_huangcaizui_D_0052():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_my_computer_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'hig搜索特殊字符关键字发送趣图h')
    def test_msg_huangcaizui_D_0052(self):
        """在我的电脑会话窗，搜索特殊字符关键字发送趣图"""
        chat = SingleChatPage()
        gif = ChatGIFPage()
        if gif.is_gif_exist():
            gif.close_gif()
        gif.click_expression_icon()
        time.sleep(1)
        chat.click_gif()
        gif.wait_for_page_load()
        # 2、搜索框输入关键字
        gif.input_message('1')

    @staticmethod
    def setUp_test_msg_huangcaizui_D_0053():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_my_computer_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0053(self):
        """在我的电脑会话窗，搜索无结果的趣图"""
        chat = SingleChatPage()
        gif = ChatGIFPage()
        if gif.is_gif_exist():
            gif.close_gif()
        gif.click_expression_icon()
        time.sleep(1)
        chat.click_gif()
        gif.wait_for_page_load()
        # 2、搜索框输入关键字
        gif.input_message('appium')

    @staticmethod
    def setUp_test_msg_huangcaizui_D_0054():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_my_computer_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0054(self):
        """在我的电脑会话窗，搜索趣图过程中返回至消息列表重新进入"""
        chat = SingleChatPage()
        gif = ChatGIFPage()
        if gif.is_gif_exist():
            gif.close_gif()
        gif.click_expression_icon()
        time.sleep(1)
        chat.click_gif()
        gif.wait_for_page_load()
        # 2、搜索框输入关键字
        gif.input_message('3')

    @staticmethod
    def setUp_test_msg_huangcaizui_D_0055():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_my_computer_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0055(self):
        """在我的电脑会话窗，趣图发送成功后搜索结果依然保留"""
        chat = SingleChatPage()
        gif = ChatGIFPage()
        if gif.is_gif_exist():
            gif.close_gif()
        gif.click_expression_icon()
        time.sleep(1)
        chat.click_gif()
        gif.wait_for_page_load()
        # 2、搜索框输入关键字
        gif.input_message('2')

    @staticmethod
    def setUp_test_msg_huangcaizui_D_0057():
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.make_already_in_message_page()
        Preconditions.enter_my_computer_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_D_0057(self):
        """在我的电脑会话窗，关闭GIF搜索框"""
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
        warnings.simplefilter('ignore', ResourceWarning)

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
    def test_msg_hanjiabin_0193(self):
        """名片消息——单聊——发出名片后 - -消息界面——长按"""
        mess = MessagePage()
        Preconditions.enter_single_chat_page("大佬2")
        scp = SingleChatPage()
        scp.wait_for_page_load()
        scp.click_more()
        scp.click_profile()
        select_contacts_page = SelectContactsPage()
        time.sleep(2)
        select_contacts_page.click_one_contact_631("大佬3")
        scp.click_text_or_description("发送名片")
        scp.press_mess("大佬3")
        # time.sleep(660)
        scp.page_should_contain_text("撤回")
        # 点击消息页搜索
        # mess.click_search()
        # # 搜索关键词给个红包1
        # SearchPage().input_search_keyword("给个名片1")
        # # 选择联系人进入联系人页
        # mess.choose_chat_by_name('给个名片1')
        # # 点击消息按钮发送消息
        # ContactDetailsPage().click_message_icon()
        # chatdialog = ChatNoticeDialog()
        # # 若存在资费提醒对话框，点击确认
        # if chatdialog.is_exist_tips():
        #     chatdialog.accept_and_close_tips_alert()
        # ChatMorePage().close_more()
        # mess.click_element_by_text('名片')
        # SelectContactsPage().select_one_contact_by_name("给个名片2")
        # send_card = Send_CardNamePage()
        # send_card.click_share_btn()
        # time.sleep(660)
        # send_card.press_mess('给个名片2')
        # mess.page_should_not_contain_element((MobileBy.XPATH, '//*[@text="删除"]'))

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_hanjiabin_0194(self):
        """名片消息——单聊——发出名片后 - -消息界面——长按"""
        mess = MessagePage()
        Preconditions.enter_single_chat_page("大佬2")
        scp = SingleChatPage()
        scp.wait_for_page_load()
        scp.click_more()
        scp.click_profile()
        select_contacts_page = SelectContactsPage()
        time.sleep(2)
        select_contacts_page.click_one_contact_631("大佬3")
        scp.click_text_or_description("发送名片")
        scp.press_mess("大佬3")
        # time.sleep(660)
        scp.page_should_contain_text("删除")
        # 点击消息页搜索
        # mess.click_search()
        # # 搜索关键词给个红包1
        # SearchPage().input_search_keyword("给个名片1")
        # # 选择联系人进入联系人页
        # mess.choose_chat_by_name('给个名片1')
        # # 点击消息按钮发送消息
        # ContactDetailsPage().click_message_icon()
        # chatdialog = ChatNoticeDialog()
        # # 若存在资费提醒对话框，点击确认
        # if chatdialog.is_exist_tips():
        #     chatdialog.accept_and_close_tips_alert()
        # ChatMorePage().close_more()
        # mess.click_element_by_text('名片')
        # SelectContactsPage().select_one_contact_by_name("给个名片2")
        # send_card = Send_CardNamePage()
        # send_card.click_share_btn()
        # send_card.press_mess('给个名片2')
        # mess.click_element((MobileBy.XPATH, '//*[@text="删除"]'))
        # mess.page_should_not_contain_text('给个名片2')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0023(self):
        """最近聊天选择器：单聊内转发消息"""
        mess = MessagePage()
        mess = MessagePage()
        Preconditions.enter_single_chat_page("大佬2")
        scp = SingleChatPage()
        scp.wait_for_page_load()
        scp.click_more()
        scp.click_profile()
        select_contacts_page = SelectContactsPage()
        time.sleep(2)
        select_contacts_page.click_one_contact_631("大佬3")
        scp.click_text_or_description("发送名片")
        scp.press_mess("大佬3")
        # time.sleep(660)
        scp.click_text_or_description("转发")
        # 点击消息页搜索
        # mess.click_search()
        # # 搜索关键词给个红包1
        # SearchPage().input_search_keyword("给个红包1")
        # # 选择联系人进入联系人页
        # mess.choose_chat_by_name('给个红包1')
        # # 点击消息按钮发送消息
        # ContactDetailsPage().click_message_icon()
        # chatdialog = ChatNoticeDialog()
        # # 若存在资费提醒对话框，点击确认
        # if chatdialog.is_exist_tips():
        #     chatdialog.accept_and_close_tips_alert()
        # single = SingleChatPage()
        # # 如果当前页面不存在消息，发送一条消息
        # if not single._is_element_present((MobileBy.XPATH, '//*[@text ="测试一个呵呵"]')):
        #     single.input_text_message("测试一个呵呵")
        #     single.send_text()
        # single.press_mess("测试一个呵呵")
        # single.click_forward()
        # select_page = SelectContactPage()
        # # 判断存在选择联系人
        # select_page.is_exist_select_contact_btn()
        # # 判断存在搜索或输入手机号提示
        # select_page.is_exist_selectorinput_toast()
        # # 判断存在选择团队联系人按钮
        # single.page_should_contain_element((MobileBy.XPATH, '//*[@text ="选择一个群"]'))
        # single.page_should_contain_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
        # single.page_should_contain_element((MobileBy.XPATH, '//*[@text ="选择团队联系人"]'))

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
        Preconditions.enter_call_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0280(self):
        """从通话——拨号盘——数字搜索手机联系人——进入单聊页面"""
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0285(self):
        """联系——+号——添加联系人——进入单聊页面"""
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击“新建消息”
        mp.click_new_message()
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        # 进入单聊会话页面
        slc.selecting_local_contacts_by_name("大佬3")
        bcp = BaseChatPage()
        if bcp.is_exist_dialog():
            # 点击我已阅读
            bcp.click_i_have_read()
        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0015(self):
        """验证点击确定按钮是否是进入发送短信页面"""
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词给个红包1
        SearchPage().input_search_keyword("给个红包1")
        # 选择联系人进入联系人页
        mess.choose_enter_chat('给个红包1')
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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0016(self):
        "验证点击退出短信是否成功退出"
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词给个红包1
        SearchPage().input_search_keyword("给个红包1")
        # 选择联系人进入联系人页
        mess.choose_enter_chat('给个红包1')
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
        singlechat.click_exit_sms()
        # 判断是否进入单聊对话框
        text = singlechat.is_on_this_page()
        self.assertTrue(lambda: (text.endswith(')') and text.startswith('(')))

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_E_0022(self):
        """短信设置默认关闭状态"""
        # 打开‘我’页面
        me = MePage()
        me.open_me_page()
        time.sleep(3)
        self.assertTrue(me.is_on_this_page())
        me.click_setting_menu()
        me.click_text_or_description("消息")
        SmsSettingPage().assert_menu_item_has_been_turn_on('应用内收发短信')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangmianhua_0400(self):
        """企业群/党群在消息列表内展示——长按/左划出功能选择弹窗——iOS（左划）"""
        Preconditions.get_into_group_chat_page('测试企业群')
        Preconditions.delete_record_group_chat()
        gcp = GroupChatPage()
        # 输入信息
        gcp.input_message("哈哈")
        # 点击发送
        gcp.send_message()
        time.sleep(1)
        gcp.click_back()
        time.sleep(1)
        mess = MessagePage()
        mess.selecting_one_group_press_by_name('测试企业群')
        # 1.弹窗本身:弹窗本身样式是否正常,点击弹窗外应收回弹窗
        # 2.标为已读:无未读则不出现该选项
        time.sleep(1)
        exist = mess.is_text_present("置顶聊天")
        self.assertEqual(exist, True)
        exist = mess.is_text_present("标为已读")
        self.assertEqual(exist, False)
        gcp.click_back_by_android()
        time.sleep(1)
        exist = mess.is_text_present("置顶聊天")
        self.assertEqual(exist, False)
        # 3.置顶聊天:已置顶则显示“取消置顶”
        mess.selecting_one_group_press_by_name('测试企业群')
        time.sleep(1)
        mess.press_groupname_to_do("置顶聊天")
        # 置顶聊天后，再次显示：取消置顶
        mess.selecting_one_group_press_by_name('测试企业群')
        time.sleep(1)
        exist = mess.is_text_present("取消置顶")
        self.assertEqual(exist, True)
        # 4.删除聊天
        # 删除聊天前，取消置顶
        mess.press_groupname_to_do("取消置顶")
        time.sleep(1)
        # 再次 删除聊天
        mess.selecting_one_group_press_by_name('测试企业群')
        time.sleep(1)
        mess.press_groupname_to_do("删除聊天")
        exist = mess.is_text_present("测试企业群")
        self.assertEqual(exist, False)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0140():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_group_chat_page("给个红包3")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0140(self):
        """群主——修改群昵称"""
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        if not gcsp.is_text_present("修改群名称"):
            raise AssertionError("不可以进入到修改群名称页面")
        gcsp.click_edit_group_card_back()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(2)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0141():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_group_chat_page("给个红包3")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0141(self):
        """群主——清除旧名称——录入一个汉字"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        # 录入新群名
        gcsp.input_new_group_name("哈")
        time.sleep(1)
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        time.sleep(1)
        gcsp.click_back()
        # 恢复群名
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        gcsp.input_new_group_name("给个红包3")
        time.sleep(1)
        if not gcsp.is_enabled_of_group_name_save_button():
            raise AssertionError("页面右上角的确定按钮没有高亮展示")
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        gcsp.click_back()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0142():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_group_chat_page("给个红包3")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0142(self):
        """群主——清除旧名称——录入5个汉字"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        # 录入新群名
        gcsp.input_new_group_name("和飞信测试")
        time.sleep(1)
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        time.sleep(1)
        gcsp.click_back()
        # 恢复群名
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        gcsp.input_new_group_name("给个红包3")
        time.sleep(1)
        if not gcsp.is_enabled_of_group_name_save_button():
            raise AssertionError("页面右上角的确定按钮没有高亮展示")
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        gcsp.click_back()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0143():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_group_chat_page("给个红包3")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0143(self):
        """群主——清除旧名称——录入10个汉字"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        # 录入新群名
        gcsp.input_new_group_name("和飞信测试和飞信测试")
        time.sleep(1)
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        time.sleep(1)
        gcsp.click_back()
        # 恢复群名
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        gcsp.input_new_group_name("给个红包3")
        time.sleep(1)
        if not gcsp.is_enabled_of_group_name_save_button():
            raise AssertionError("页面右上角的确定按钮没有高亮展示")
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        gcsp.click_back()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0144():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_group_chat_page("给个红包3")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0144(self):
        """群主——清除旧名称——录入11个汉字"""
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        # 录入新群名
        gcsp.input_new_group_name("和飞信测试和飞信测试")
        time.sleep(1)
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        time.sleep(1)
        gcsp.click_back()
        # 恢复群名
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        gcsp.input_new_group_name("给个红包3")
        time.sleep(1)
        if not gcsp.is_enabled_of_group_name_save_button():
            raise AssertionError("页面右上角的确定按钮没有高亮展示")
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0145(self):
        """群主——清除旧名称——录入1个字母（不区分大、小写）"""
        Preconditions.enter_group_chat_page("给个红包3")
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        # 录入新群名
        gcsp.input_new_group_name("和飞信测试和飞信测试")
        time.sleep(1)
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        time.sleep(1)
        gcsp.click_back()
        # 恢复群名
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        gcsp.input_new_group_name("给个红包3")
        time.sleep(1)
        if not gcsp.is_enabled_of_group_name_save_button():
            raise AssertionError("页面右上角的确定按钮没有高亮展示")
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0146(self):
        """群主——清除旧名称——录入10个字母（不区分大、小写）"""
        Preconditions.enter_group_chat_page("给个红包3")
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        # 录入新群名
        gcsp.input_new_group_name("aADASasdas")
        time.sleep(1)
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        time.sleep(1)
        gcsp.click_back()
        # 恢复群名
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        gcsp.input_new_group_name("给个红包3")
        time.sleep(1)
        if not gcsp.is_enabled_of_group_name_save_button():
            raise AssertionError("页面右上角的确定按钮没有高亮展示")
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0147(self):
        """群主——清除旧名称——录入29个字母（不区分大、小写）"""
        Preconditions.enter_group_chat_page("给个红包3")
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        # 录入新群名
        gcsp.input_new_group_name("aaaaaaaaaaaaaaaaaaaaiiiiiiiii")
        time.sleep(1)
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        time.sleep(1)
        gcsp.click_back()
        # 恢复群名
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        gcsp.input_new_group_name("给个红包3")
        time.sleep(1)
        if not gcsp.is_enabled_of_group_name_save_button():
            raise AssertionError("页面右上角的确定按钮没有高亮展示")
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0148(self):
        """群主——清除旧名称——录入30个字母（不区分大、小写）"""
        Preconditions.enter_group_chat_page("给个红包3")
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        # 录入新群名
        gcsp.input_new_group_name("aaaaaaaaaaaaaaaaaaaaiiiiiiiiia")
        time.sleep(1)
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        time.sleep(1)
        gcsp.click_back()
        # 恢复群名
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        gcsp.input_new_group_name("给个红包3")
        time.sleep(1)
        if not gcsp.is_enabled_of_group_name_save_button():
            raise AssertionError("页面右上角的确定按钮没有高亮展示")
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0149(self):
        """群主——清除旧名称——录入31个字母（不区分大、小写）"""
        Preconditions.enter_group_chat_page("给个红包3")
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        # 录入新群名
        gcsp.input_new_group_name("aaaaaaaaaaaaaaaaaaaaiiiiiiiiid")
        time.sleep(1)
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        time.sleep(1)
        gcsp.click_back()
        # 恢复群名
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        gcsp.input_new_group_name("给个红包3")
        time.sleep(1)
        if not gcsp.is_enabled_of_group_name_save_button():
            raise AssertionError("页面右上角的确定按钮没有高亮展示")
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0150(self):
        """群主——清除旧名称——录入1个数字"""
        Preconditions.enter_group_chat_page("给个红包3")
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        # 录入新群名
        gcsp.input_new_group_name("1")
        time.sleep(1)
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        time.sleep(1)
        gcsp.click_back()
        # 恢复群名
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        gcsp.input_new_group_name("给个红包3")
        time.sleep(1)
        if not gcsp.is_enabled_of_group_name_save_button():
            raise AssertionError("页面右上角的确定按钮没有高亮展示")
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0151(self):
        """群主——清除旧名称——录入10个数字"""
        Preconditions.enter_group_chat_page("给个红包2")
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        # 录入新群名
        gcsp.input_new_group_name("11113335589")
        time.sleep(1)
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        time.sleep(1)
        gcsp.click_back()
        # 恢复群名
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        gcsp.input_new_group_name("给个红包2")
        time.sleep(1)
        if not gcsp.is_enabled_of_group_name_save_button():
            raise AssertionError("页面右上角的确定按钮没有高亮展示")
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0152(self):
        """群主——清除旧名称——录入30个数字"""
        Preconditions.enter_group_chat_page("给个红包2")
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        # 录入新群名
        gcsp.input_new_group_name("112233445511223344551122334455")
        time.sleep(1)
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        time.sleep(1)
        gcsp.click_back()
        # 恢复群名
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        gcsp.input_new_group_name("给个红包2")
        time.sleep(1)
        if not gcsp.is_enabled_of_group_name_save_button():
            raise AssertionError("页面右上角的确定按钮没有高亮展示")
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0153(self):
        """群主——清除旧名称——录入31个数字"""
        Preconditions.enter_group_chat_page("给个红包2")
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        # 录入新群名
        gcsp.input_new_group_name("1122334455110223344551122334455")
        time.sleep(1)
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        time.sleep(1)
        gcsp.click_back()
        # 恢复群名
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        gcsp.input_new_group_name("给个红包2")
        time.sleep(1)
        if not gcsp.is_enabled_of_group_name_save_button():
            raise AssertionError("页面右上角的确定按钮没有高亮展示")
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0154(self):
        """群主——清除旧名称——录入汉字+字母+数字"""
        Preconditions.enter_group_chat_page("给个红包2")
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        # 录入新群名
        gcsp.input_new_group_name("通栏sss1123")
        time.sleep(1)
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        time.sleep(1)
        gcsp.click_back()
        # 恢复群名
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        gcsp.input_new_group_name("给个红包2")
        time.sleep(1)
        if not gcsp.is_enabled_of_group_name_save_button():
            raise AssertionError("页面右上角的确定按钮没有高亮展示")
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0155(self):
        """群主——清除旧名称——录入特殊字符"""
        Preconditions.enter_group_chat_page("给个红包2")
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        # 录入新群名
        gcsp.input_new_group_name("@#$%%")
        time.sleep(1)
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        time.sleep(1)
        gcsp.click_back()
        # 恢复群名
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp.wait_for_page_load()
        gcsp.click_modify_group_name()
        time.sleep(1)
        gcsp.clear_group_name()
        time.sleep(1)
        gcsp.input_new_group_name("给个红包2")
        time.sleep(1)
        if not gcsp.is_enabled_of_group_name_save_button():
            raise AssertionError("页面右上角的确定按钮没有高亮展示")
        gcsp.save_group_name()
        if not gcsp.is_toast_exist("修改成功"):
            raise AssertionError("群名称更改为新名称失败")
        gcsp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0156(self):
        """群主——修改群名片"""
        Preconditions.enter_group_chat_page("给个红包4")
        gcp = GroupChatPage()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_my_card()
        time.sleep(1)
        gcsp.input_new_group_name("哈哈哈哈哈哈哈哈哈哈")
        # 判断按钮是否高亮展示
        if gcsp.is_enabled_of_group_card_save_button():
            gcsp.save_group_card_name()
            gcsp.is_toast_exist("修改成功")
            time.sleep(2)
            # 验证上面输入的名称内容都保存
            gcsp.click_my_card()
            time.sleep(1)
            if not gcsp.get_edit_query_text() == "哈哈哈哈哈哈哈哈哈哈":
                raise AssertionError("不可以保存输入的名称内容")
            gcsp.click_edit_group_card_back()
            gcsp.click_back()
        else:
            raise AssertionError("按钮不会高亮展示")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0157(self):
        """群主——清除旧名片——录入一个汉字"""
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        # 1.点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 2.点击群名片
        gcsp.click_modify_my_group_name()
        # 3.点击‘X’按钮
        gcsp.click_iv_delete_button()
        gcsp.input_my_group_card_name("哈")
        gcsp.save_group_card_name()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0158(self):
        """群主——清除旧名片——录入5个汉字"""
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        # 1.点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 2.点击群名片
        gcsp.click_modify_my_group_name()
        # 3.点击‘X’按钮
        gcsp.click_iv_delete_button()
        gcsp.input_my_group_card_name("哈哈哈哈哈")
        gcsp.save_group_card_name()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0159(self):
        """群主——清除旧名片——录入10个汉字"""
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        # 1.点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 2.点击群名片
        gcsp.click_modify_my_group_name()
        # 3.点击‘X’按钮
        gcsp.click_iv_delete_button()
        gcsp.input_my_group_card_name("哈哈哈哈哈哈哈哈哈哈")
        gcsp.save_group_card_name()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0160(self):
        """群主——清除旧名片——录入11个汉字"""

        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        # 1.点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 2.点击群名片
        gcsp.click_modify_my_group_name()
        # 3.点击‘X’按钮
        gcsp.click_iv_delete_button()
        gcsp.input_my_group_card_name("哈哈哈哈哈哈哈哈哈哈哈")
        gcsp.save_group_card_name()

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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0283(self):
        """联系——标签分组——进入单聊页面"""
        # 1.客户端已登录
        # 2.网络正常
        # 3.在联系模块
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        time.sleep(1)
        contacts.click_mobile_contacts()
        contacts.click_label_grouping()
        label_grouping = LabelGroupingPage()
        label_grouping.wait_for_page_load()
        # 不存在标签分组则创建
        group_name = Preconditions.get_label_grouping_name()
        group_names = label_grouping.get_label_grouping_names()
        time.sleep(1)
        if not group_names:
            label_grouping.click_new_create_group()
            label_grouping.wait_for_create_label_grouping_page_load()
            label_grouping.input_label_grouping_name(group_name)
            label_grouping.click_sure()
            # 选择成员
            slc = SelectLocalContactsPage()
            slc.wait_for_page_load()
            names = slc.get_contacts_name()
            if not names:
                raise AssertionError("No m005_contacts, please add m005_contacts in address book.")
            for name in names:
                slc.select_one_member_by_name(name)
            slc.click_sure()
            label_grouping.wait_for_page_load()
            label_grouping.select_group(group_name)
        else:
            # 选择一个标签分组
            label_grouping.select_group(group_names[0])
        lgdp = LableGroupDetailPage()
        time.sleep(1)
        # 标签分组成员小于2人，需要添加成员
        members_name = lgdp.get_members_names()
        if lgdp.is_text_present("该标签分组内暂无成员") or len(members_name) < 2:
            lgdp.click_add_members()
            # 选择成员
            slc = SelectLocalContactsPage()
            slc.wait_for_page_load()
            names = slc.get_contacts_name()
            if not names:
                raise AssertionError("No m005_contacts, please add m005_contacts in address book.")
            for name in names:
                slc.select_one_member_by_name(name)
            slc.click_sure()
        # 点击信息
        names = lgdp.get_members_names()
        lgdp.click_text_or_description(names[0])
        lgdp.click_text_or_description("消息")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0284(self):
        """联系——标签分组——进入单聊页面"""
        # 1.客户端已登录
        # 2.网络正常
        # 3.在联系模块
        mess = MessagePage()
        mess.open_contacts_page()
        contacts = ContactsPage()
        time.sleep(1)
        contacts.click_mobile_contacts()
        contacts.click_label_grouping()
        label_grouping = LabelGroupingPage()
        label_grouping.wait_for_page_load()
        # 不存在标签分组则创建
        group_name = Preconditions.get_label_grouping_name()
        group_names = label_grouping.get_label_grouping_names()
        time.sleep(1)
        if not group_names:
            label_grouping.click_new_create_group()
            label_grouping.wait_for_create_label_grouping_page_load()
            label_grouping.input_label_grouping_name(group_name)
            label_grouping.click_sure()
            # 选择成员
            slc = SelectLocalContactsPage()
            slc.wait_for_page_load()
            names = slc.get_contacts_name()
            if not names:
                raise AssertionError("No m005_contacts, please add m005_contacts in address book.")
            for name in names:
                slc.select_one_member_by_name(name)
            slc.click_sure()
            label_grouping.wait_for_page_load()
            label_grouping.select_group(group_name)
        else:
            # 选择一个标签分组
            label_grouping.select_group(group_names[0])
        lgdp = LableGroupDetailPage()
        time.sleep(1)
        # 标签分组成员小于2人，需要添加成员
        members_name = lgdp.get_members_names()
        if lgdp.is_text_present("该标签分组内暂无成员") or len(members_name) < 2:
            lgdp.click_add_members()
            # 选择成员
            slc = SelectLocalContactsPage()
            slc.wait_for_page_load()
            names = slc.get_contacts_name()
            if not names:
                raise AssertionError("No m005_contacts, please add m005_contacts in address book.")
            for name in names:
                slc.select_one_member_by_name(name)
            slc.click_sure()
        # 点击群发信息
        lgdp.click_send_group_info()
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()

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
        ContactsSelector().click_local_contacts('给个红包1')
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
        mess.click_message('给个红包1')
        # Checkpoint 进入短信编辑页面，可继续编辑该短信
        singe_chat.clear_inputtext()
        singe_chat.click_back()

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
        ContactsSelector().click_local_contacts('给个红包1')
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
        mess.page_should_contain_text('给个红包1')
        mess.page_should_contain_text('2条相关聊天记录')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0207():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_group_chat_page("群聊3")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0207(self):
        """群聊设置页面——查找聊天内容——英文搜索——搜索结果展示"""
        mess = MessagePage()
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
        Preconditions.enter_group_chat_page("群聊3")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0208(self):
        """群聊设置页面——查找聊天内容——特殊字符搜索——搜索结果展示"""
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
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_group_chat_page("群聊3")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0212(self):
        """群聊设置页面——查找聊天内容——特殊字符搜索——搜索结果展示"""
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
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_group_chat_page("群聊3")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0216(self):
        """群聊设置页面——关闭消息免打扰——网络断网"""
        # 1.、成功登录和飞信
        # 2、已创建或者加入群聊
        # 3、群主、普通成员
        # 4、网络断网
        # 5、消息免打扰开启状态
        # 预置群聊
        mess = MessagePage()
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
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_group_chat_page("群聊3")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0217(self):
        """群聊设置页面——关闭消息免打扰——网络断网"""
        mess = MessagePage()
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
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_group_chat_page("群聊3")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0223(self):
        """聊天设置页面——清空聊天记录"""
        mess = MessagePage()
        # 1、已成功登录和飞信
        # 2、已创建一个群聊
        # 3、群主、普通成员
        # 4、聊天会话页面存在记录
        # 预置群聊
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
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_group_chat_page("群聊3")

    @tags('ALL', 'SMOKE', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0226(self):
        """聊天设置页面——删除并退出群聊——群成员"""
        # 1、已成功登录和飞信
        # 2、已加入群聊
        # 3、普通成员
        # 4、群人数小于：3
        # 5、网络正常（4G/WIFI ）
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        # Step 在聊天设置页面
        groupchat.click_setting()
        groupset.wait_for_page_load()
        # groupset.click_delete_and_exit()
        # # Step 点击页面底部的“删除并退出”按钮
        # SearchPage().click_back_button()
        # # Checkpoint 会退出当前群聊返回到消息列表并收到一条系统消息：你已退出群
        # ContactsPage().select_people_by_name("系统消息")
        # mess.page_should_contain_text("你已退出群")
        # mess.page_should_contain_text("群聊3")

    @staticmethod
    def setUp_test_msg_xiaoqiu_0229():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_group_chat_page("群聊3")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0229(self):
        """聊天设置页面——删除并退出群聊——群主"""
        # 1、已成功登录和飞信
        # 2、已加入群聊
        # 3、群主权限
        # 4、群人数小于：3
        # 5、网络正常（4G/WIFI ）
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        # Step 在聊天设置页面
        groupchat.click_setting()
        groupset.wait_for_page_load()
        # Step 点击页面底部的“删除并退出”按钮 点击确定
        # groupset.click_delete_and_exit()
        # SearchPage().click_back_button()
        # # Checkpoint 返回到消息列表并收到一条系统消息，该群已解散
        # ContactsPage().select_people_by_name("系统消息")
        # mess.page_should_contain_text('你已退出群')
        # mess.page_should_contain_text('群聊4')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0250():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_group_chat_page("群聊3")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0250(self):
        """消息列表——群聊天会话窗口——发送的消息类型展示"""
        # 1、已成功登录和飞信
        # 2、网络正常（4G/WIFI ）
        # 3、消息列表页面
        # 4、发送消息类型展示
        gcp = GroupChatPage()
        if not gcp.is_text_present('测试一个呵呵'):
            gcp.input_text_message("测试一个呵呵")
            gcp.send_text()
        gcp.click_back()
        mess = MessagePage()
        if mess.is_on_this_page():
            mess.page_should_contain_text('群聊3')
            mess.page_should_contain_text('测试一个呵呵')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0251():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_group_chat_page('123456789012345678901234567890')

    @tags('ALL', 'SMOKE', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0251(self):
        """群名称过长时——展示"""
        # 1、已成功登录和飞信
        # 2、网络正常（4G/WIFI ）
        # 3、消息列表页面
        groupchat = GroupChatPage()
        # Checkpoint 用省略号隐藏群名称的中间名称，只展示前后名称
        self.assertEqual(groupchat.get_group_name(), '123456789012345678901234567890(1)')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0269():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_group_chat_page("给个红包1")

    @tags('ALL', 'SMOKE', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0269(self):
        """普通群——聊天会话页面——未进群联系人展示"""
        # 1、已成功登录和飞信
        # 2、网络正常（4G/WIFI ）
        # 3、群主权限
        mess = MessagePage()
        gcp = GroupChatPage()
        if not gcp.is_text_present('测试一个呵呵'):
            gcp.input_text_message("测试一个呵呵")
            gcp.send_text()
        # Checkpoint 提示：还有人未进群，再次邀请
        time.sleep(2)
        mess.page_should_contain_text('还有人未进群,再次邀请')
        # Step 再次发送3次消息
        count = 0
        while count <= 2:
            gcp.input_text_message("测试一个呵呵")
            gcp.send_text()
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
        Preconditions.enter_single_chat_page("大佬1")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0091(self):
        """一对一聊天设置创建群聊"""
        # 1.已有一对一的聊天窗口
        single = SingleChatPage()
        chat_set = SingleChatSetPage()
        single.click_setting()
        chat_set.is_on_this_page()
        chat_set.click_add_icon()
        ContactsSelector().wait_for_contacts_selector_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'middle')
    def test_msg_huangmianhua_0187(self):
        """通讯录——群聊——搜索——选择一个群"""
        # 1.正常联网
        # 2.正常登录
        # 3.当前所在的页面是消息列表页面
        # 4、存在跟搜索条件匹配的群聊
        # 5、通讯录 - 群聊
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
        sog.selecting_one_group_by_name("群聊4")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()

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
        groupchat.click_text_or_description("群聊")
        # Step: 3、点击搜索群组
        groupchat.click_text_or_description("搜索群组")
        # 进行中文模糊搜索
        global_search_group_page = GlobalSearchGroupPage()
        global_search_group_page.search("群assacasa")
        # CheckPoint：中文模糊搜索，是否可以匹配展示搜索结果
        self.assertTrue(global_search_group_page.is_text_present("无搜索结果"))

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
        self.assertTrue(global_search_group_page.is_text_present("群聊"))

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
        global_search_group_page.search("测打啊试")
        # CheckPoint：中文精确搜索，不存在跟搜索条件匹配的群聊
        # self.assertIsNotNone(global_search_group_page.is_group_in_list("群聊"))
        self.assertTrue(global_search_group_page.is_toast_exist("无搜索结果"))