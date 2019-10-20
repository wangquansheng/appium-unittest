import time
import unittest
import warnings

from pages.components import BaseChatPage, ContactsSelector
from pages.components.SearchGroup import SearchGroupPage
from preconditions.BasePreconditions import LoginPreconditions, WorkbenchPreconditions
from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import *


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

    def press_group_file(self):
        group_chat_page = GroupChatPage()
        if group_chat_page.is_exist_msg_file():
            pass
        else:
            group_chat_page = GroupChatPage()
            group_chat_page.click_file()
            select_file_type = ChatSelectFilePage()
            select_file_type.wait_for_page_load()
            select_file_type.click_local_file()
            local_file = ChatSelectLocalFilePage()
            local_file.click_preset_file_dir()
            local_file.select_file(".xlsx")
            local_file.click_send()

    def public_forward_mobile_phone_contacts(self):
        self.press_group_file()
        ChatFilePage().forward_file('.xlsx')
        SelectContactsPage().wait_for_page_load()
        SelectContactsPage().select_local_contacts()
        SelectLocalContactsPage().wait_for_page_load()


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

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'middle')
    def test_msg_huangmianhua_0191(self):
        """通讯录-群聊-英文精确搜索——搜索结果展示"""
        # 1.正常联网
        # 2.正常登录
        # 3.当前所在的页面是消息列表页面
        # 4、英文精确搜索，存在跟搜索条件匹配的群聊
        # 5、通讯录 - 群聊
        contactspage = ContactsPage()
        grouplist = GroupListPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        contactspage.click_group_chat_631()
        grouplist.click_search_input()
        group_search = GroupListSearchPage()
        group_search.input_search_keyword('Aweqwqw')
        # Checkpoint 可以匹配展示搜索结果
        self.assertTrue(group_search.is_group_in_list('Aweqwqw'))

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0431(self):
        """聊天会话页面——长按——撤回——发送失败的语音消息"""
        Preconditions.enter_group_chat_page("群聊2")
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        if gcp.is_text_present("始终允许"):
            audio.click_allow()
        time.sleep(3)
        # 断网
        gcp.set_network_status(0)
        audio.click_send_bottom()
        time.sleep(1)
        gcp.hide_keyboard()
        gcp.press_message_longclick()
        if gcp.is_text_present("撤回"):
            raise AssertionError("撤回-功能按钮-有显示")

    def tearDown_msg_xiaoqiu_0431(self):
        current_mobile().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'middle')
    def test_msg_huangmianhua_0192(self):
        """通讯录-群聊-英文精确搜索——搜索结果展示"""
        # 1.正常联网
        # 2.正常登录
        # 3.当前所在的页面是消息列表页面
        # 4、英文精确搜索，不存在跟搜索条件匹配的群聊
        # 5、通讯录 - 群聊
        contactspage = ContactsPage()
        grouplist = GroupListPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        contactspage.click_group_chat_631()
        grouplist.click_search_input()
        group_search = GroupListSearchPage()
        group_search.input_search_keyword('dsssszwvzz')
        self.assertTrue(group_search.is_text_present("无搜索结果"))

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'middle')
    def test_msg_huangmianhua_0193(self):
        """通讯录-群聊-空格精确搜索——搜索结果展示"""
        contactspage = ContactsPage()
        grouplist = GroupListPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        contactspage.click_group_chat_631()
        grouplist.click_search_input()
        group_search = GroupListSearchPage()
        group_search.input_search_keyword('a a')
        # Checkpoint 可以匹配展示搜索结果
        self.assertTrue(group_search.is_group_in_list('a a'))

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'middle')
    def test_msg_huangmianhua_0194(self):
        """通讯录-群聊-空格精确搜索——搜索结果展示"""
        # 1.正常联网
        # 2.正常登录
        # 3.当前所在的页面是消息列表页面
        # 4、不存在跟搜索条件匹配的群聊
        # 5、通讯录 - 群聊
        contactspage = ContactsPage()
        grouplist = GroupListPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        contactspage.click_group_chat_631()
        grouplist.click_search_input()
        group_search = GroupListSearchPage()
        group_search.input_search_keyword('1aa aa')
        self.assertTrue(group_search.is_text_present("无搜索结果"))

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'middle')
    def test_msg_huangmianhua_0195(self):
        """通讯录-群聊-数字精确搜索——搜索结果展示"""
        # 1.正常联网
        # 2.正常登录
        # 3.当前所在的页面是消息列表页面
        # 4、存在跟搜索条件匹配的群聊
        # 5、通讯录 - 群聊
        contactspage = ContactsPage()
        grouplist = GroupListPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        contactspage.click_group_chat_631()
        grouplist.click_search_input()
        group_search = GroupListSearchPage()
        group_search.input_search_keyword('138138138')
        self.assertTrue(group_search.is_group_in_list('138138138'))

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'middle')
    def test_msg_huangmianhua_0196(self):
        """通讯录-群聊-数字精确搜索——搜索结果展示"""
        # 1.正常联网
        # 2.正常登录
        # 3.当前所在的页面是消息列表页面
        # 4、不存在跟搜索条件匹配的群聊
        # 5、通讯录 - 群聊
        contactspage = ContactsPage()
        grouplist = GroupListPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        contactspage.click_group_chat_631()
        grouplist.click_search_input()
        group_search = GroupListSearchPage()
        group_search.input_search_keyword('5845544')
        self.assertTrue(group_search.is_text_present('无搜索结果'))

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'middle')
    def test_msg_huangmianhua_0197(self):
        """通讯录-群聊-数字精确搜索——搜索结果展示"""
        # 1.正常联网
        # 2.正常登录
        # 3.当前所在的页面是消息列表页面
        # 4、存在跟搜索条件匹配的群聊
        # 5、通讯录 - 群聊
        contactspage = ContactsPage()
        grouplist = GroupListPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        contactspage.click_group_chat_631()
        grouplist.click_search_input()
        group_search = GroupListSearchPage()
        group_search.input_search_keyword('138138138')
        self.assertTrue(group_search.is_group_in_list('138138138'))

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'middle')
    def test_msg_huangmianhua_0198(self):
        """通讯录-群聊-数字精确搜索——搜索结果展示"""
        # 1.正常联网
        # 2.正常登录
        # 3.当前所在的页面是消息列表页面
        # 4、不存在跟搜索条件匹配的群聊
        # 5、通讯录 - 群聊
        contactspage = ContactsPage()
        grouplist = GroupListPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        contactspage.click_group_chat_631()
        grouplist.click_search_input()
        group_search = GroupListSearchPage()
        group_search.input_search_keyword('46784321')
        self.assertTrue(group_search.is_text_present('无搜索结果'))

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'middle')
    def test_msg_huangmianhua_0197(self):
        """通讯录-群聊-字符精确搜索——搜索结果展示"""
        # 1.正常联网
        # 2.正常登录
        # 3.当前所在的页面是消息列表页面
        # 4、存在跟搜索条件匹配的群聊
        # 5、通讯录 - 群聊
        contactspage = ContactsPage()
        grouplist = GroupListPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        contactspage.click_group_chat_631()
        grouplist.click_search_input()
        group_search = GroupListSearchPage()
        group_search.input_search_keyword('138138138')
        self.assertTrue(group_search.is_group_in_list('138138138'))

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'middle')
    def test_msg_huangmianhua_0200(self):
        """通讯录-群聊-字符精确搜索——搜索结果展示"""
        # 1.正常联网
        # 2.正常登录
        # 3.当前所在的页面是消息列表页面
        # 4、不存在跟搜索条件匹配的群聊
        # 5、通讯录 - 群聊
        contactspage = ContactsPage()
        grouplist = GroupListPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        contactspage.click_group_chat_631()
        grouplist.click_search_input()
        group_search = GroupListSearchPage()
        group_search.input_search_keyword('群聊安神诀德克士')
        self.assertTrue(group_search.is_text_present('无搜索结果'))

    # @tags('ALL', 'SMOKE', 'group_chat', 'prior', 'high')
    @unittest.skip("跳过")
    def test_msg_xiaoqiu_0411(self):
        """长按——识别群二维码——进入群会话窗口和群设置页面"""
        # 1、已登录客户端
        # 2、网络正常
        # 3、当前消息列表页面
        mess = MessagePage()
        Preconditions.enter_group_chat_page("群聊1")
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        contactsel = ContactsSelector()
        sel_con = SelectContactsPage()
        groupchat.wait_for_page_load()
        # Step 进入群聊设置页面
        groupchat.click_setting()
        groupset.wait_for_page_load()
        groupset.click_group_avatars()
        # Step 点击左下角的分享按钮
        groupset.click_qecode_share_button()
        # Checkpoint 跳转到联系人选择器页面
        contactsel.wait_for_contacts_selector_page_load()
        # Step 点击选择一个群
        sel_con.click_select_one_group()
        # Step 搜索选中一个群
        time.sleep(2)
        SearchGroupPage().click_group('测试群组2')
        # Step 点击确定
        SingleChatPage().click_sure()
        # Checkpoint 弹出toast提示：已转发
        mess.is_toast_exist("已转发")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0431(self):
        """聊天会话页面——长按——撤回——发送失败的语音消息"""
        # 1、网络正常
        # 2、登录和飞信
        # 3、已加入普通群
        # 4、聊天会话页面，存在发送失败的消息
        # 5、普通群/单聊/企业群/我的电脑/标签分组
        Preconditions.enter_group_chat_page("群聊2")
        gcp = GroupChatPage()
        Preconditions.delete_record_group_chat()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            # 点击只发送语言模式
            audio.click_only_voice()
            audio.click_sure()
        # 权限申请允许弹窗判断
        time.sleep(1)
        if gcp.is_text_present("始终允许"):
            audio.click_allow()
        time.sleep(3)
        # 断网
        gcp.set_network_status(0)
        audio.click_send_bottom()
        time.sleep(1)
        gcp.hide_keyboard()
        gcp.press_message_longclick()
        if gcp.is_text_present("撤回"):
            raise AssertionError("撤回-功能按钮-有显示")

    def tearDown_msg_xiaoqiu_0431(self):
        current_mobile().set_network_status(6)
















