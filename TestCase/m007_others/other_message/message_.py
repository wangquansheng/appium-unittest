import time
import unittest

from appium.webdriver.common.mobileby import MobileBy

from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile

from pages import ChatWindowPage
from pages import GroupChatPage
from pages import GroupChatSetPage
from pages import SelectContactPage
from pages.components import ChatNoticeDialog, BaseChatPage
from pages.components import ContactsSelector
from pages.message.FreeMsg import FreeMsgPage
from pages.message.Send_CardName import Send_CardNamePage
from preconditions.BasePreconditions import LoginPreconditions, ContactsPage, CallPage, ContactSecltorPage, \
    SelectContactsPage, CalllogBannerPage, MessagePage, SearchPage, LabelGroupingPage, GroupListPage, \
    GroupListSearchPage, LableGroupDetailPage, WorkbenchPreconditions, SelectOneGroupPage, SelectLocalContactsPage, \
    CreateGroupNamePage, OneKeyLoginPage, GuidePage, PermissionListPage, AgreementDetailPage, ChatMorePage, \
    ChatSelectFilePage, ChatSelectLocalFilePage, SingleChatSetPage, GroupChatSetSeeMembersPage, FindChatRecordPage
from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from preconditions.BasePreconditions import LoginPreconditions, ContactsPage, CallPage, \
     CalllogBannerPage, ContactListSearchPage, CallContactDetailPage, SingleChatPage, ContactDetailsPage\
     , CallTypeSelectPage


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
        # a = 0
        # names = {}
        # while a < 3:
        #     names = slc.get_contacts_name()
        #     num = len(names)
        #     if not names:
        #         raise AssertionError("No contacts, please add contacts in address book.")
        #     if num == 1:
        #         sog.page_up()
        #         a += 1
        #         if a == 3:
        #             raise AssertionError("联系人只有一个，请再添加多个不同名字联系人组成群聊")
        #     else:
        #         break
        # # 选择成员
        # for name in names:
        #     slc.select_one_member_by_name(name)
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
    def create_contacts_groups():

        # 创建联系人
        fail_time = 0
        import dataproviders
        while fail_time < 3:
            try:
                # 获取需要导入的联系人数据
                required_contacts = dataproviders.get_preset_contacts()[:3]
                # 连接手机
                conts = ContactsPage()
                Preconditions.select_mobile('Android-移动')
                current_mobile().hide_keyboard_if_display()
                # 导入数据
                for name, number in required_contacts:
                    Preconditions.make_already_in_message_page()
                    conts.open_contacts_page()
                    conts.create_contacts_if_not_exits_new(name, number)
                # # 创建群
                name_list = ['给个红包1', '给个红包2']
                group_name_list = ['群聊1']
                conts.open_group_chat_list()
                group_list = GroupListPage()
                for group_name in group_name_list:
                    group_list.wait_for_page_load()
                    group_list.create_group_chats_if_not_exits(group_name, name_list)
                group_list.click_back()
                conts.open_message_page()
                return
            except Exception as e:
                fail_time += 1
                print(e)


class Contacts_demo(TestCase):

    @staticmethod
    def setUp_test_msg_hanjiabin_0179():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_single_chat_page("大佬1")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_hanjiabin_0179(self):
        """名片消息——单聊——点击名片按钮进入“和通讯录+本地联系人”的联系人选择器——搜索——名称搜索"""
        ChatMorePage().close_more()
        ChatMorePage().click_card()
        SelectContactsPage().click_one_contact_631("给个名片2")
        send_card = Send_CardNamePage()
        send_card.assert_card_name_equal_to('给个名片2')
        send_card.is_present_card_phone('13800138300')
        send_card.assert_card_comp_equal_to('中软国际')
        send_card.assert_card_emailaddress_equal_to('test1234@163.com')
        send_card.assert_card_position_equal_to('软件工程师')
        send_card.click_close_btn()
        # 判断存在选择联系人
        SelectContactPage().is_exist_select_contact_btn()

    @staticmethod
    def setUp_test_msg_hanjiabin_0187():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.enter_single_chat_page("大佬2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_hanjiabin_0187(self):
        """名片消息——单聊——异常场景——发送方"""
        current_mobile().set_network_status(1)
        single = SingleChatPage()
        single.input_text_message("测试一个呵呵")
        single.send_text()
        time.sleep(2)
        chatwindow = ChatWindowPage()
        chatwindow.click_resend_button()
        current_mobile().set_network_status(6)

    @staticmethod
    def setUp_test_msg_hanjiabin_0189():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_single_chat_page("大佬1")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_hanjiabin_0189(self):
        """名片消息——单聊——发出名片后--消息界面——点击查看"""
        mess = MessagePage()
        ChatMorePage().close_more()
        ChatMorePage().click_card()
        SelectContactsPage().click_one_contact_631("给个名片2")
        send_card = Send_CardNamePage()
        send_card.click_share_btn()

    @staticmethod
    def setUp_test_msg_hanjiabin_0195():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_single_chat_page("大佬1")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_hanjiabin_0195(self):
        """名片消息——单聊——发出名片后--消息界面——长按"""
        mess = MessagePage()
        ChatMorePage().close_more()
        ChatMorePage().click_card()
        SelectContactsPage().click_one_contact_631("给个名片2")
        send_card = Send_CardNamePage()
        send_card.click_share_btn()
        send_card.press_mess('给个名片2')
        mess.click_element((MobileBy.XPATH, '//*[@text="多选"]'))
        mess.page_should_contain_element((MobileBy.XPATH, '//*[@text="删除"]'))
        mess.page_should_contain_element((MobileBy.XPATH, '//*[@text="转发"]'))
        mess.click_element((MobileBy.XPATH, '//*[@text="删除"]'))

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0022():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()

    # @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    @unittest.skip("跳过，无免费短信功能")
    def test_msg_huangcaizui_A_0022(self):
        """免费/发送短信—选择手机联系人"""
        mess = MessagePage()
        # 点击+号
        mess.click_add_icon()
        # 点击免费短信
        mess.click_free_sms()
        mess_call_page = CallPage()
        freemsg = FreeMsgPage()
        chatdialog = ChatNoticeDialog()
        # 若存在欢迎页面
        if freemsg.is_exist_welcomepage():
            # 点击确定按钮
            freemsg.click_sure_btn()
            time.sleep(2)
            # 若存在权限控制
            if mess_call_page.is_exist_allow_button():
                # 存在提示点击允许
                mess_call_page.wait_for_freemsg_load()
        mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
        # 判断存在？标志
        FreeMsgPage().wait_is_exist_wenhao()
        # 判断存在退出短信按钮
        FreeMsgPage().wait_is_exist_exit()

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0045():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0045(self):
        """消息-消息列表界面+功能页面元素检查"""
        mess = MessagePage()
        # 点击+号
        mess.click_add_icon()
        mess.page_should_contain_text('新建消息')
        mess.page_should_contain_text('发送短信')
        mess.page_should_contain_text('发起群聊')
        mess.page_should_contain_text('群发助手')
        mess.page_should_contain_text('扫一扫')

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0052():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.enter_single_chat_page("大佬2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0052(self):
        """消息-消息列表进入到会话页面"""
        single = SingleChatPage()
        single.input_text_message("测试一个呵呵")
        single.send_text()
        time.sleep(2)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0064():
        Preconditions.select_mobile('Android-移动')
        Preconditions.enter_single_chat_page("大佬2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0064(self):
        """消息—一对一消息会话—设置"""
        single = SingleChatPage()
        single.wait_for_page_load()
        single.click_setting()
        self.assertTrue(SingleChatSetPage().is_on_this_page())

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0065():
        Preconditions.select_mobile('Android-移动')
        Preconditions.enter_single_chat_page("大佬2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0065(self):
        """消息—一对一消息会话—设置页面头像转跳"""
        single = SingleChatPage()
        chat_set = SingleChatSetPage()
        single.click_setting()
        chat_set.is_on_this_page()
        chat_set.click_avatar()
        GroupChatSetSeeMembersPage().wait_for_profile_page_load()

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0070():
        Preconditions.select_mobile('Android-移动')
        Preconditions.enter_single_chat_page("大佬2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0070(self):
        """消息-一对一消息会话-设置页面查找聊天内容"""
        single = SingleChatPage()
        mess = MessagePage()
        chat_set = SingleChatSetPage()
        single.click_setting()
        chat_set.is_on_this_page()
        chat_set.search_chat_record()
        FindChatRecordPage().wait_for_page_loads()

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0072():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.enter_single_chat_page("大佬2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0072(self):
        """输入框中输入表情消息不发送，进入查找聊天内容后是否还显示草稿"""
        single = SingleChatPage()
        mess = MessagePage()
        chat_set = SingleChatSetPage()
        findchat = FindChatRecordPage()
        if not single._is_element_present((MobileBy.XPATH, '//*[@text ="呵呵哒"]')):
            single.input_text_message("呵呵哒")
            single.send_text()
        single.open_expression()
        count = 0
        while(count <= 10):
            single.select_expression()
            count = count + 1
        single.close_expression()
        single.click_setting()
        chat_set.is_on_this_page()
        chat_set.search_chat_record()
        findchat.wait_for_page_loads()
        findchat.input_search_message('呵呵哒')
        findchat.click_record()
        CallPage().wait_for_chat_page()

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0078():
        Preconditions.select_mobile('Android-移动')
        Preconditions.enter_single_chat_page("大佬2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0078(self):
        """消息-一对一消息会话-设置页面查找不存在的聊天内容"""
        single = SingleChatPage()
        mess = MessagePage()
        chat_set = SingleChatSetPage()
        findchat = FindChatRecordPage()
        single.click_setting()
        chat_set.is_on_this_page()
        chat_set.search_chat_record()
        findchat.wait_for_page_loads()
        findchat.input_search_message('ADDWOQWIQWOPPQWIDIWQDQW')
        mess.page_should_contain_element((MobileBy.XPATH, '//*[@text ="无搜索结果"]'))

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0089():
        Preconditions.select_mobile('Android-移动')
        Preconditions.enter_single_chat_page("大佬2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0089(self):
        """一对一聊天设置创建群聊"""
        single = SingleChatPage()
        mess = MessagePage()
        chat_set = SingleChatSetPage()
        single.click_setting()
        chat_set.is_on_this_page()
        chat_set.click_add_icon()
        ContactsSelector().wait_for_contacts_selector_page_load()

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0100():
        Preconditions.select_mobile('Android-移动')
        Preconditions.enter_single_chat_page("大佬2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0100(self):
        """长按消息体是否弹出多功能列表"""
        single = SingleChatPage()
        mess = MessagePage()
        # 如果当前页面不存在消息，发送一条消息
        if single._is_element_present((MobileBy.XPATH, '//*[@text ="呵呵哒"]')):
            single.press_mess('呵呵哒')
            mess.click_element((MobileBy.XPATH, '//*[@text ="删除"]'))
        single.input_text_message("呵呵哒")
        single.send_text()
        single.press_mess('呵呵哒')
        single.page_should_contain_text("复制")
        single.page_should_contain_text("转发")
        single.page_should_contain_text("收藏")
        single.page_should_contain_text("撤回")
        single.page_should_contain_text("删除")
        single.page_should_contain_text("多选")

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0151():
        Preconditions.select_mobile('Android-移动')
        Preconditions.enter_single_chat_page("大佬2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0151(self):
        """进入到单聊天会话页面，发送一条字符等于5000的文本消息"""
        single = SingleChatPage()
        mess = MessagePage()
        self.assertTrue(single.is_exist_send_audio_button())
        single.input_text_message("11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111")
        self.assertTrue(single.is_exist_send_txt_button())
        single.send_text()
        time.sleep(1)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0182():
        Preconditions.select_mobile('Android-移动')
        Preconditions.enter_single_chat_page("大佬2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0182(self):
        """自己撤回文本消息，是否会起新的头像"""
        single = SingleChatPage()
        mess = MessagePage()
        # 如果当前页面不存在消息，发送一条消息
        if single._is_element_present((MobileBy.XPATH, '//*[@text ="呵呵哒"]')):
            single.press_mess('呵呵哒')
            mess.click_element((MobileBy.XPATH, '//*[@text ="删除"]'))
        single.input_text_message("呵呵哒")
        single.send_text()
        single.press_mess('呵呵哒')
        mess.click_element((MobileBy.XPATH, '//*[@text ="撤回"]'))
        single.click_i_know()
        time.sleep(3)
        mess.page_should_contain_element((MobileBy.XPATH, '//*[@text ="你撤回了一条信息"]'))

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0184():
        Preconditions.select_mobile('Android-移动')
        Preconditions.enter_single_chat_page("大佬2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0184(self):
        """聊天会话窗口的批量选择器页面展示"""
        mess = MessagePage()
        single = SingleChatPage()
        # 如果当前页面不存在消息，发送一条消息
        if not single._is_element_present((MobileBy.XPATH, '//*[@text ="测试一个呵呵"]')):
            single.input_text_message("测试一个呵呵")
            single.send_text()
        single.press_mess("测试一个呵呵")
        single.click_multiple_selection()
        time.sleep(2)
        group_chat = GroupChatPage()
        # 勾选消息时校验页面元素
        self.assertTrue(group_chat.is_exist_multiple_selection_back())
        mess.page_should_contain_text('已选择')
        self.assertTrue(group_chat.is_exist_multiple_selection_count())
        self.assertTrue(group_chat.is_enabled_multiple_selection_delete())
        self.assertTrue(group_chat.is_enabled_multiple_selection_forward())
        # 未勾选消息时校验页面元素
        group_chat.get_multiple_selection_select_box()[0].click()
        time.sleep(1)
        self.assertTrue(group_chat.is_exist_multiple_selection_back())
        mess.page_should_contain_text('未选择')
        self.assertFalse(group_chat.is_exist_multiple_selection_count())
        self.assertFalse(group_chat.is_enabled_multiple_selection_delete())
        self.assertFalse(group_chat.is_enabled_multiple_selection_forward())