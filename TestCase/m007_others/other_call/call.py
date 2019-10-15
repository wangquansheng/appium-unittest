import time
from appium.webdriver.common.mobileby import MobileBy

from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile
from pages import ChatAudioPage
from pages import ChatWindowPage
from pages import GrantPemissionsPage
from pages import GroupChatPage
from pages import GroupChatSetFindChatContentPage
from pages import GroupChatSetPage
from pages import GroupNamePage
from pages import SelectContactPage
from pages.call.multipartycall import MultipartyCallPage
from pages.components import ChatNoticeDialog, BaseChatPage
from pages.components import ContactsSelector
from pages.components import SearchBar
from pages.components.SearchGroup import SearchGroupPage
from pages.message.FreeMsg import FreeMsgPage
from preconditions.BasePreconditions import LoginPreconditions, ContactsPage, CallPage, ContactSecltorPage, \
    SelectContactsPage, CalllogBannerPage, MessagePage, SearchPage, LabelGroupingPage, GroupListPage, \
    GroupListSearchPage, LableGroupDetailPage, WorkbenchPreconditions, SelectOneGroupPage, SelectLocalContactsPage, \
    CreateGroupNamePage, OneKeyLoginPage, GuidePage, PermissionListPage, AgreementDetailPage, ChatMorePage, \
    ChatSelectFilePage, ChatSelectLocalFilePage
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


class MsgAllPrior(TestCase):
    """通话---和飞信电话会控页"""

    def default_setUp(self):
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()

    @staticmethod
    def setUp_test_call_wangqiong_0057():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0057(self):
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_call_page()
        # 点击多方通话
        call_page = CallPage()
        call_page.click_free_call()
        # 进入多方通话页面选择联系人呼叫
        selectcontacts = SelectContactsPage()
        SelectContactsPage().click_one_contact_631('大佬3')
        SelectContactsPage().click_one_contact_631('大佬4')
        selectcontacts.click_sure_bottom()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0059(self):
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_call_page()
        # 点击多方通话
        call_page = CallPage()
        call_page.click_free_call()
        # 进入多方通话页面选择联系人呼叫
        selectcontacts = SelectContactsPage()
        SelectContactsPage().click_one_contact_631('大佬3')
        SelectContactsPage().click_one_contact_631('大佬4')
        selectcontacts.click_sure_bottom()
        # 是否弹框_我知道了,点击 发起呼叫
        callcontact = CalllogBannerPage()
        time.sleep(3)
        # 挂断电话返回到通话页面
        self.assertTrue(callcontact._is_element_present((MobileBy.ID, "com.chinasofti.rcs:id/btnFreeCall")))

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_call_wangqiong_0063(self):
        """网络正常，多方电话通话详情页可再次呼叫成功"""
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_call_page()
        # 点击多方通话
        call_page = CallPage()
        call_page.click_free_call()
        # 进入多方通话页面选择联系人呼叫
        selectcontacts = SelectContactsPage()
        SelectContactsPage().click_one_contact_631('大佬1')
        SelectContactsPage().click_one_contact_631('大佬2')
        time.sleep(4)
        selectcontacts.click_sure_bottom()
        # 是否弹框_我知道了,点击 发起呼叫
        callcontact = CalllogBannerPage()
        time.sleep(3)
        # 点击多方通话详情
        call_page.click_element((MobileBy.XPATH,
                                 '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.view.ViewGroup/android.support.v4.view.ViewPager/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[1]/android.widget.LinearLayout[2]'),
                                auto_accept_permission_alert=False)
        time.sleep(3)
        # 再次呼叫并接听和飞信电话
        call_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/call_again'))
        time.sleep(5)

    @staticmethod
    def setUp_test_call_wangqiong_0071():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        contacts.click_mobile_contacts()
        contacts.click_label_grouping()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0071(self):
        """网络正常，标签分组-多方电话，拨打正常 ，拨打正常"""
        labellist = LabelGroupingPage()
        labellist.click_new_create_group()
        labellist.wait_for_create_label_grouping_page_load()
        labellist.input_label_grouping_name('分组1')
        labellist.click_sure()
        time.sleep(3)
        if current_mobile().is_text_present('新建分组'):
            labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/rl_label_left_back'))
            labellist.select_group('分组1')

            # 判断标签中有无指定成员
            if labellist._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/dialog_message')):
                time.sleep(5)
                labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
                                        auto_accept_permission_alert=False)
            a = labellist.is_contacter_in_lable('大佬1')
            b = labellist.is_contacter_in_lable('大佬2')
            if not (a & b):
                labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_first_colum'),
                                        auto_accept_permission_alert=False)
                if not a:
                    SelectContactsPage().click_one_contact_631('大佬1')
                if not b:
                    SelectContactsPage().click_one_contact_631('大佬2')
                labellist.click_sure()
        else:
            SelectContactsPage().click_one_contact_631('大佬1')
            SelectContactsPage().click_one_contact_631('大佬2')
            labellist.click_sure()
            labellist.select_group('分组1')
        labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_third_colum'))
        SelectContactsPage().click_one_contact_631('大佬1')
        SelectContactsPage().click_one_contact_631('大佬2')
        time.sleep(3)
        labellist.click_sure()
        time.sleep(8)
        # 接听和飞信电话后挂断电话
        # labellist._is_element_present((MobileBy.ID, 'com.android.incallui:id/endButton'))
        # labellist.click_element((MobileBy.ID, 'com.android.incallui:id/endButton'))

    @staticmethod
    def setUp_test_call_wangqiong_0073():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        contacts.click_mobile_contacts()
        contacts.click_label_grouping()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0073(self):
        """网络正常，标签分组-群发消息-多方电话，拨打正常 ，拨打正常"""
        labellist = LabelGroupingPage()
        labellist.click_new_create_group()
        labellist.wait_for_create_label_grouping_page_load()
        labellist.input_label_grouping_name('分组1')
        labellist.click_sure()
        time.sleep(3)
        if current_mobile().is_text_present('新建分组'):
            labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/rl_label_left_back'))
            labellist.select_group('分组1')

            # 判断标签中有无指定成员
            if labellist._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/dialog_message')):
                time.sleep(5)
                labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
                                        auto_accept_permission_alert=False)
            a = labellist.is_contacter_in_lable('大佬1')
            b = labellist.is_contacter_in_lable('大佬2')
            if not (a & b):
                labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_first_colum'),
                                        auto_accept_permission_alert=False)
                if not a:
                    SelectContactsPage().click_one_contact_631('大佬1')
                if not b:
                    SelectContactsPage().click_one_contact_631('大佬2')
                labellist.click_sure()
        else:
            SelectContactsPage().click_one_contact_631('大佬1')
            SelectContactsPage().click_one_contact_631('大佬2')
            labellist.click_sure()
            labellist.select_group('分组1')
        # 进入群发消息界面并点击多方通话
        # 只有飞信电话，多方视频

        labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_second_colum'),
                                auto_accept_permission_alert=False)
        labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/action_multicall'),
                                auto_accept_permission_alert=False)
        labellist.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and ' + '@text="多方视频"]'))
        time.sleep(3)
        SelectContactsPage().click_one_contact_631('大佬1')
        SelectContactsPage().click_one_contact_631('大佬2')
        time.sleep(3)
        labellist.click_sure()
        time.sleep(8)
        # 接听和飞信电话后挂断电话
        # labellist._is_element_present((MobileBy.ID, 'com.android.incallui:id/endButton'))
        # labellist.click_element((MobileBy.ID, 'com.android.incallui:id/endButton'))

    @staticmethod
    def setUp_test_call_wangqiong_0080():
        """预置条件"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0080(self):
        """本地搜索：联系人姓名（全名）精准搜索可匹配结果"""
        mess = MessagePage()
        mess.click_search()
        # 精确搜索关键词联系人3
        SearchPage().input_search_keyword("大佬1")
        # 正确搜索出联系人
        SearchPage().assert_contact_name_display("大佬1")
        mess.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_back01'))
        time.sleep(4)
        # 多方通话搜索联系人
        call_page = CallPage()
        # 打开通话页面
        call_page.open_call_page()
        time.sleep(2)
        # 是否存在多方电话弹出提示
        if call_page.is_exist_multi_party_telephone():
            # 存在提示点击跳过
            call_page.click_multi_party_telephone()
            # 是否存在知道了弹出提示
            time.sleep(2)
            if call_page.is_exist_know():
                # 存在提示点击跳过
                call_page.click_know()
            # 是否存在授权允许弹出提示
            time.sleep(1)
            if call_page.is_exist_allow_button():
                # 存在提示点击允许
                call_page.click_allow_button(False)
            # 点击返回按钮返回通话页面
            time.sleep(1)
            call_page.click_back()
        # 等待查看通话页面是否加载
        call_page.wait_for_page_load()
        # 进入多方通话
        call_page.click_free_call()
        # 点击搜索框进行搜索
        call_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
                                auto_accept_permission_alert=False)
        time.sleep(5)
        call_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'), '大佬1')
        self.assertTrue(call_page._is_element_present(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' + '@text="大佬1"]')))

    @staticmethod
    def setUp_test_call_wangqiong_0081():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0081(self):
        """ 通讯录界面搜索姓名"""
        mess = MessagePage()
        mess.click_search()
        # 精确搜索关键词联系人3
        SearchPage().input_search_keyword("大佬3")
        # 正确搜索出联系人
        SearchPage().assert_contact_name_display("大佬3")
        mess.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_back01'))
        time.sleep(4)
        # 多方通话搜索联系人
        call_page = CallPage()
        # 打开通话页面
        call_page.open_call_page()
        time.sleep(2)
        # 是否存在多方电话弹出提示
        if call_page.is_exist_multi_party_telephone():
            # 存在提示点击跳过
            call_page.click_multi_party_telephone()
            # 是否存在知道了弹出提示
            time.sleep(2)
            if call_page.is_exist_know():
                # 存在提示点击跳过
                call_page.click_know()
            # 是否存在授权允许弹出提示
            time.sleep(1)
            if call_page.is_exist_allow_button():
                # 存在提示点击允许
                call_page.click_allow_button(False)
            # 点击返回按钮返回通话页面
            time.sleep(1)
            call_page.click_back()
        # 等待查看通话页面是否加载
        call_page.wait_for_page_load()
        # 进入多方通话
        call_page.click_free_call()
        # 点击搜索框进行搜索
        call_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
                                auto_accept_permission_alert=False)
        time.sleep(5)
        call_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'), '大佬3')
        self.assertTrue(call_page._is_element_present(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' + '@text="大佬3"]')))

    @staticmethod
    def setUp_test_call_wangqiong_0086():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0086(self):
        """本地搜索：本地联系人号码精准搜索显示正常"""
        mess = MessagePage()
        mess.click_search()
        # 精确搜索关键词联系人3
        SearchPage().input_search_keyword("13800138007")
        # 正确搜索出联系人
        SearchPage().assert_contact_name_display("大佬3")
        mess.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_back01'))
        time.sleep(4)
        # 多方通话搜索联系人
        call_page = CallPage()
        # 打开通话页面
        call_page.open_call_page()
        time.sleep(2)
        # 是否存在多方电话弹出提示
        if call_page.is_exist_multi_party_telephone():
            # 存在提示点击跳过
            call_page.click_multi_party_telephone()
            # 是否存在知道了弹出提示
            time.sleep(2)
            if call_page.is_exist_know():
                # 存在提示点击跳过
                call_page.click_know()
            # 是否存在授权允许弹出提示
            time.sleep(1)
            if call_page.is_exist_allow_button():
                # 存在提示点击允许
                call_page.click_allow_button(False)
            # 点击返回按钮返回通话页面
            time.sleep(1)
            call_page.click_back()
        # 等待查看通话页面是否加载
        call_page.wait_for_page_load()
        # 进入多方通话
        call_page.click_free_call()
        # 点击搜索框进行搜索
        call_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
                                auto_accept_permission_alert=False)
        time.sleep(5)
        call_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'), '13800138007')
        self.assertTrue(call_page._is_element_present(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' + '@text="大佬3"]')))
        call_page.click_back()
        call_page.click_back()

        # 打开拨号键
        call_page.click_call()
        call_page.dial_number('13800138007')
        self.assertTrue(current_mobile().is_text_present('大佬3'))
        # 选择联系人正常展示
        call_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tvName" and ' + '@text="大佬3"]'))

    @staticmethod
    def setUp_test_call_wangqiong_0087():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0087(self):
        """本地搜索：1-10位数字可支持模糊搜索匹配结果（和通讯录仅支持6-10位数模糊匹配）"""
        call_page = CallPage()
        # 打开通话页面
        call_page.open_call_page()
        time.sleep(3)
        # 是否存在多方电话弹出提示
        if call_page.is_exist_multi_party_telephone():
            # 存在提示点击跳过
            call_page.click_multi_party_telephone()
            # 是否存在知道了弹出提示
            time.sleep(2)
            if call_page.is_exist_know():
                # 存在提示点击跳过
                call_page.click_know()
            # 是否存在授权允许弹出提示
            time.sleep(1)
            if call_page.is_exist_allow_button():
                # 存在提示点击允许
                call_page.click_allow_button(False)
            # 点击返回按钮返回通话页面
            time.sleep(1)
            call_page.click_back()
        # 等待查看通话页面是否加载
        call_page.wait_for_page_load()
        # 进入多方通话
        call_page.click_free_call()
        # 点击搜索框进行搜索
        call_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
                                auto_accept_permission_alert=False)
        time.sleep(5)
        call_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'), '1')
        call_page.hide_keyboard()

        # 输入11位数字进行搜索
        call_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
                                auto_accept_permission_alert=False)
        time.sleep(5)
        call_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'), '13800138007')
        self.assertTrue(call_page._is_element_present(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' + '@text="大佬3"]')))
        # 点击搜素到的结果
        call_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' + '@text="大佬3"]'))

        call_page.click_back()

        # 打开拨号键
        call_page.click_call()
        call_page.dial_number('13800138007')
        self.assertTrue(current_mobile().is_text_present('大佬3'))
        # 选择联系人正常展示
        call_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tvName" and ' + '@text="大佬3"]'))

    @staticmethod
    def setUp_test_call_wangqiong_0088():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0088(self):
        """搜索11位陌生号码匹配网络搜索结果"""
        call_page = CallPage()
        # 打开通话页面
        call_page.open_call_page()
        time.sleep(3)
        # 是否存在多方电话弹出提示
        if call_page.is_exist_multi_party_telephone():
            # 存在提示点击跳过
            call_page.click_multi_party_telephone()
            # 是否存在知道了弹出提示
            time.sleep(2)
            if call_page.is_exist_know():
                # 存在提示点击跳过
                call_page.click_know()
            # 是否存在授权允许弹出提示
            time.sleep(1)
            if call_page.is_exist_allow_button():
                # 存在提示点击允许
                call_page.click_allow_button(False)
            # 点击返回按钮返回通话页面
            time.sleep(1)
            call_page.click_back()
        # 等待查看通话页面是否加载
        call_page.wait_for_page_load()
        # 进入多方通话
        call_page.click_free_call()
        # 点击搜索框进行搜索
        call_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
                                auto_accept_permission_alert=False)
        time.sleep(5)
        call_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'), '18300345678')
        call_page.hide_keyboard()

        # 校验是否搜索到未知号码
        SelectContactsPage().is_present_unknown_member()
        call_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="18300345678(未知号码)"]'))
        time.sleep(3)
        call_page.click_back()

    @staticmethod
    def setUp_test_call_wangqiong_0119():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        contactspage = ContactsPage()
        contactspage.open_contacts_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0119(self):
        """和通讯录全局搜索：联系人姓名（全名）精准搜索可匹配结果"""
        contac = ContactsPage()
        contac.click_search_box()
        from pages import ContactListSearchPage
        contact_search = ContactListSearchPage()
        contact_search.wait_for_page_load()
        contact_search.input_search_keyword('大佬3')
        self.assertTrue(contact_search.is_contact_in_list('大佬3'))
        contact_search.click_contact('大佬3')

    @staticmethod
    def setUp_test_call_wangqiong_0120():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0120(self):
        """和通讯录全局搜索：联系人姓名（非全名）模糊搜索可匹配结果"""
        contac = ContactsPage()
        contac.click_search_box()
        from pages import ContactListSearchPage
        contact_search = ContactListSearchPage()
        contact_search.wait_for_page_load()
        contact_search.input_search_keyword('大佬4')
        self.assertTrue(contact_search.is_contact_in_list('大佬4'))
        contact_search.click_contact('大佬4')

    @staticmethod
    def setUp_test_call_wangqiong_0126():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        contactspage = ContactsPage()
        contactspage.open_contacts_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0126(self):
        """和通讯录全局搜索：11位号码精准搜索显示正常"""
        contac = ContactsPage()
        contac.click_search_box()
        from pages import ContactListSearchPage
        contact_search = ContactListSearchPage()
        contact_search.wait_for_page_load()
        contact_search.input_search_keyword('13800138007')
        self.assertTrue(contact_search.is_contact_in_list('大佬3'))
        contact_search.click_contact('大佬3')

    @staticmethod
    def setUp_test_call_wangqiong_0127():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        contactspage = ContactsPage()
        contactspage.open_contacts_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0127(self):
        """和通讯录全局搜索：6-10位数字可支持模糊搜索匹配结果"""
        contac = ContactsPage()
        contac.click_search_box()
        from pages import ContactListSearchPage
        contact_search = ContactListSearchPage()
        contact_search.wait_for_page_load()
        # 输入9位数 查看是否正匹配到数据
        contact_search.input_search_keyword('123138001')
        self.assertTrue(contact_search.is_contact_in_list('xili'))
        contact_search.click_contact('xili')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_call_wangqiong_0145(self):
        """选择1个联系人可发起呼叫多方电话"""
        Preconditions.select_mobile('Android-移动')
        Preconditions.enter_call_page()
        # 点击多方通话
        call_page = CallPage()
        call_page.click_free_call()
        # 进入多方通话页面选择联系人呼叫
        selectcontacts = SelectContactsPage()
        SelectContactsPage().click_one_contact_631('大佬3')
        time.sleep(4)
        selectcontacts.click_sure_bottom()
        # 是否弹框_我知道了,点击 发起呼叫
        time.sleep(4)
        callcontact = CalllogBannerPage()
        # 是否存在请先接听“和飞信电话”，点击“我知道了”
        if callcontact._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt')):
            callcontact.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt'))
        # 是否存在设置悬浮窗，存在去设置页设置权限
        if callcontact._is_element_present((MobileBy.ID, 'android:id/button1')):
            callcontact.click_element((MobileBy.ID, 'android:id/button1'))
            current_mobile().click_element((MobileBy.ID, 'android:id/switch_widget'))
            current_mobile().click_element((MobileBy.XPATH, '//android.widget.ImageButton[@content-desc="向上导航"]'))

        # 挂断多方通话
        time.sleep(2)
        call_page.hang_up_hefeixin_call()
        time.sleep(3)
        # 查看通话类型为和飞信通话
        call_page._is_element_present((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tvName" and ' +
                                       '@text="大佬3"]'))
        call_page._is_element_present((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tvCallManner" and ' +
                                       '@text="和飞信电话"]'))
        time.sleep(3)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_call_wangqiong_0146(self):
        """选择8个联系人可发起呼叫多方电话"""
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面
        """需要预置联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits('联系人1', '18312345678')
        contactspage.create_contacts_if_not_exits('联系人2', '18323456789')
        contactspage.create_contacts_if_not_exits('联系人3', '13812345678')
        contactspage.create_contacts_if_not_exits('联系人4', '13823456789')
        contactspage.create_contacts_if_not_exits('联系人5', '13811111111')
        contactspage.create_contacts_if_not_exits('联系人6', '13822222222')
        contactspage.create_contacts_if_not_exits('联系人7', '13833333333')
        contactspage.create_contacts_if_not_exits('联系人8', '13844444444')

        Preconditions.enter_call_page()
        # 点击多方通话
        call_page = CallPage()
        call_page.click_free_call()
        # 进入多方通话页面选择联系人呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.search('联系人1')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="联系人1"]'))
        selectcontacts.search('联系人2')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="联系人2"]'))
        selectcontacts.search('联系人3')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="联系人3"]'))
        selectcontacts.search('联系人4')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="联系人4"]'))
        selectcontacts.search('联系人5')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="联系人5"]'))
        selectcontacts.search('联系人6')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="联系人6"]'))
        selectcontacts.search('联系人7')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="联系人7"]'))
        selectcontacts.search('联系人8')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="联系人8"]'))
        time.sleep(5)
        selectcontacts.click_sure_bottom()
        # 是否弹框_我知道了,点击 发起呼叫
        callcontact = CalllogBannerPage()
        # 是否存在请先接听“和飞信电话”，点击“我知道了”
        if callcontact._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt')):
            callcontact.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt'))
        # 是否存在设置悬浮窗，存在去设置页设置权限
        if callcontact._is_element_present((MobileBy.ID, 'android:id/button1')):
            callcontact.click_element((MobileBy.ID, 'android:id/button1'))
            current_mobile().click_element((MobileBy.ID, 'android:id/switch_widget'))
            current_mobile().click_element((MobileBy.XPATH, '//android.widget.ImageButton[@content-desc="向上导航"]'))

        # 挂断多方通话
        time.sleep(3)
        call_page.hang_up_hefeixin_call()
        time.sleep(3)
        # 查看通话类型为和飞信通话
        call_page._is_element_present((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tvCallTime" and ' +
                                       '@text="刚刚"]'))
        call_page._is_element_present((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tvCallManner" and ' +
                                       '@text="和飞信电话"]'))
        time.sleep(3)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_call_wangqiong_0147(self):
        """搜索陌生人+本地联系人+和通讯录联系人共8人可发起多方电话"""
        Preconditions.select_mobile('Android-移动')
        Preconditions.enter_call_page()
        # 点击多方通话
        call_page = CallPage()
        call_page.click_free_call()
        time.sleep(4)
        # 进入多方通话页面选择联系人呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.search('大佬1')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
             '@text="大佬1"]'))
        selectcontacts.search('18311111110')
        selectcontacts.click_unknown_member()
        selectcontacts.search('18322222220')
        selectcontacts.click_unknown_member()
        selectcontacts.search('18333333330')
        selectcontacts.click_unknown_member()
        selectcontacts.search('18333333330')
        selectcontacts.click_unknown_member()
        selectcontacts.search('18344444440')
        selectcontacts.click_unknown_member()
        selectcontacts.search('18355555550')
        selectcontacts.click_unknown_member()
        selectcontacts.search('18366666660')
        selectcontacts.click_unknown_member()

        time.sleep(5)
        selectcontacts.click_sure_bottom()
        # 是否弹框_我知道了,点击 发起呼叫
        callcontact = CalllogBannerPage()
        # 是否存在请先接听“和飞信电话”，点击“我知道了”
        if callcontact._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt')):
            callcontact.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt'))
        # 是否存在设置悬浮窗，存在去设置页设置权限
        if callcontact._is_element_present((MobileBy.ID, 'android:id/button1')):
            callcontact.click_element((MobileBy.ID, 'android:id/button1'))
            current_mobile().click_element((MobileBy.ID, 'android:id/switch_widget'))
            current_mobile().click_element((MobileBy.XPATH, '//android.widget.ImageButton[@content-desc="向上导航"]'))

        # 挂断多方通话
        time.sleep(4)
        # call_page.hang_up_hefeixin_call()
        time.sleep(3)
        # 查看通话类型为和飞信通话
        call_page._is_element_present((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tvCallTime" and ' +
                                       '@text="刚刚"]'))
        call_page._is_element_present((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tvCallManner" and ' +
                                       '@text="和飞信电话"]'))
        time.sleep(3)

    @staticmethod
    def setUp_test_call_wangqiong_0155():
        Preconditions.select_mobile('Android-移动')
        Preconditions.enter_group_chat_page("群聊1")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0155(self):
        """普通群聊多方电话-联系人选择器-仅支持当前群成员名称  进行搜索"""
        grouppage = GroupListPage()
        grouppage.click_mult_call_icon()
        time.sleep(3)
        grouppage.click_element((MobileBy.XPATH, "//*[@text='多方视频']"))
        # 选择成员进行多方电话
        time.sleep(10)

    @staticmethod
    def setUp_test_call_wangqiong_0157():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_group_chat_page("群聊1")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0157(self):
        """普通群聊多方电话-联系人选择器-本机号码不可选，置灰显示"""
        grouppage = GroupListPage()
        grouppage.click_mult_call_icon()
        time.sleep(3)
        grouppage.click_element((MobileBy.XPATH, "//*[@text='多方视频']"))
        contactselect = ContactsSelector()
        # 选择自己进行多方电话,弹框该联系人不可选择,呼叫按钮任然置灰
        contactselect.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/index_text'))
        current_mobile().assert_element_should_be_disabled((MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'))

    @staticmethod
    def setUp_test_call_wangqiong_0171():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        contacts.click_mobile_contacts()
        contacts.click_label_grouping()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0171(self):
        """标签分组-多方电话选择器界面显示正常"""
        labellist = LabelGroupingPage()
        labellist.click_new_create_group()
        labellist.wait_for_create_label_grouping_page_load()
        labellist.input_label_grouping_name('分组A')
        labellist.click_sure()
        time.sleep(3)
        if current_mobile().is_text_present('新建分组'):
            labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/rl_label_left_back'))
            labellist.select_group('分组A')

            # 判断标签中有无指定成员
            if labellist._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/dialog_message')):
                time.sleep(5)
                labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
                                        auto_accept_permission_alert=False)
            a = labellist.is_contacter_in_lable('联系人3')
            b = labellist.is_contacter_in_lable('联系人4')
            if not (a & b):
                labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_first_colum'),
                                        auto_accept_permission_alert=False)
                if not a:
                    SelectContactsPage().click_one_contact_631('联系人3')
                if not b:
                    SelectContactsPage().click_one_contact_631('联系人4')
                labellist.click_sure()

        # 创建标签分组
        labellist = LabelGroupingPage()
        labellist.create_group('分组A', ["A联系人", "B联系人", "C联系人"])
        # labellist.create_group('分组A', ['A联系人', 'B联系人', 'C联系人', 'D联系人', 'E联系人', 'F联系人', 'G联系人', 'H联系人', 'I联系人', 'J联系人', 'K联系人'])
        labellist.click_label_group('分组A')
        # 进入多方通话
        labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_third_colum'))
        # 查看时长
        labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs: id/multi_time_tip'))
        self.assertTrue(labellist.is_text_present((MobileBy.XPATH, '//*[contains(@text, "分钟")]')))

        # 按照字母滑动
        contact = ContactsPage()
        contact.click_element(
            ('xpath', '//*[@resource-id="com.chinasofti.rcs:id/indexbarview"]'))
        elements = contact.get_elements((MobileBy.ID, 'com.chinasofti.rcs:id/tv_name'))
        for i in range(len(elements)):
            elements[i].click()
        # 判断右侧字符是否按顺序排列
        current_mobile().is_right_letters_sorted()

    @staticmethod
    def setUp_test_call_wangqiong_0179():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        contacts.click_mobile_contacts()
        contacts.click_label_grouping()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0179(self):
        """标签分组-多方电话选择器-组员11位号码精准搜索显示正常"""
        labellist = LabelGroupingPage()
        labellist.click_new_create_group()
        labellist.wait_for_create_label_grouping_page_load()
        labellist.input_label_grouping_name('分组1')
        labellist.click_sure()
        time.sleep(3)
        if current_mobile().is_text_present('新建分组'):
            labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/rl_label_left_back'))
            labellist.select_group('分组1')

            # 判断标签中有无指定成员
            if labellist._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/dialog_message')):
                time.sleep(5)
                labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
                                        auto_accept_permission_alert=False)
            a = labellist.is_contacter_in_lable('大佬1')
            b = labellist.is_contacter_in_lable('大佬2')
            if not (a & b):
                labellist.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_first_colum'),
                                        auto_accept_permission_alert=False)
                if not a:
                    SelectContactsPage().click_one_contact_631('大佬1')
                if not b:
                    SelectContactsPage().click_one_contact_631('大佬2')
                labellist.click_sure()
        else:
            # 新建分组 选择分组成员
            SelectContactsPage().click_one_contact_631('大佬1')
            SelectContactsPage().click_one_contact_631('大佬2')
            labellist.click_sure()
            labellist.select_group('分组1')
        # 点击多方电话
        labeldeatilpage = LableGroupDetailPage()
        labeldeatilpage.click_multi_tel()

        # 通过11位号码选择联系人 看是否能精准匹配到联系人
        from pages import SelectLocalContactsPage

        selectpage = SelectLocalContactsPage()
        selectpage.search('13800138005')
        # 搜索到指定联系人选择之后 搜索栏清空 呼叫按钮可点击
        selectpage.click_element((MobileBy.XPATH, '//*[contains(@text, "大佬1")]'))
        time.sleep(3)
        selectpage.element_should_be_enabled((MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'))

        """判断输入框是否自动清空"""
        self.assertTrue(selectpage.page_should_not_contain_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_delect')))

    @staticmethod
    def setUp_test_call_wangqiong_0180():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        contacts.click_mobile_contacts()
        contacts.click_label_grouping()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0180(self):
        """标签分组-多方电话选择器-组员1-10位数字可支持模糊搜索匹配结果"""
        labelpage = LabelGroupingPage()
        if not labelpage.is_text_present('分组1'):
            labelpage.create_group('分组1', '大佬1', '大佬2')
        labelpage.click_label_group('分组1')
        # 校验里面成员是否包含联系人3&联系人4，没有则添加成员
        if labelpage._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/dialog_message')):
            time.sleep(5)
            labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
                                    auto_accept_permission_alert=False)
        a = labelpage.is_contacter_in_lable('大佬1')
        b = labelpage.is_contacter_in_lable('大佬2')
        if not (a & b):
            labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_first_colum'),
                                    auto_accept_permission_alert=False)
            if not a:
                SelectContactsPage().click_one_contact_631('大佬1')
            if not b:
                SelectContactsPage().click_one_contact_631('大佬2')
            labelpage.click_sure()
        # 进入多方通话
        labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_third_colum'))

        # 输入1位数 查看是否能模糊匹配到联系人
        from pages import SelectLocalContactsPage
        selectpage = SelectLocalContactsPage()
        selectpage.search('1')
        # 搜索到指定联系人选择之后 搜索栏清空 呼叫按钮可点击
        selectpage.click_element((MobileBy.XPATH, '//*[contains(@text, "大佬1")]'))
        time.sleep(3)
        selectpage.element_should_be_enabled((MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'))

        """判断输入框是否自动清空"""
        self.assertTrue(selectpage.page_should_not_contain_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_delect')))

    @staticmethod
    def setUp_test_call_wangqiong_0181():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        contacts.click_mobile_contacts()
        contacts.click_label_grouping()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0181(self):
        """标签分组-多方电话选择器-组员姓名（全名）精准搜索可匹配结果"""
        labelpage = LabelGroupingPage()
        if not labelpage.is_text_present('分组1'):
            labelpage.create_group('分组1', '大佬1', '大佬2')
        labelpage.click_label_group('分组1')
        # 校验里面成员是否包含联系人3&联系人4，没有则添加成员
        if labelpage._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/dialog_message')):
            time.sleep(5)
            labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
                                    auto_accept_permission_alert=False)
        a = labelpage.is_contacter_in_lable('大佬1')
        b = labelpage.is_contacter_in_lable('大佬2')
        if not (a & b):
            labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_first_colum'),
                                    auto_accept_permission_alert=False)
            if not a:
                SelectContactsPage().click_one_contact_631('大佬1')
            if not b:
                SelectContactsPage().click_one_contact_631('大佬2')
            labelpage.click_sure()
        # 进入多方通话
        labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_third_colum'))

        # 输入全名 查看是否能精准匹配到联系人
        from pages import SelectLocalContactsPage
        selectpage = SelectLocalContactsPage()
        selectpage.search('大佬1')
        time.sleep(3)
        # 搜索到指定联系人选择之后 搜索栏清空 呼叫按钮可点击
        selectpage.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' + '@text="大佬1"]'))
        time.sleep(3)
        selectpage.element_should_be_enabled((MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'))

        """判断输入框是否自动清空"""
        self.assertTrue(selectpage.page_should_not_contain_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_delect')))

    @staticmethod
    def setUp_test_call_wangqiong_0182():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        contacts.click_mobile_contacts()
        contacts.click_label_grouping()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0182(self):
        """标签分组-多方电话选择器-组员（非全名）模糊搜索可匹配结果"""
        labelpage = LabelGroupingPage()
        if not labelpage.is_text_present('分组1'):
            labelpage.create_group('分组1', '大佬1', '大佬2')
        labelpage.click_label_group('分组1')
        # 校验里面成员是否包含联系人3&联系人4，没有则添加成员
        if labelpage._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/dialog_message')):
            time.sleep(5)
            labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
                                    auto_accept_permission_alert=False)
        a = labelpage.is_contacter_in_lable('大佬1')
        b = labelpage.is_contacter_in_lable('大佬2')
        if not (a & b):
            labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_first_colum'),
                                    auto_accept_permission_alert=False)
            if not a:
                SelectContactsPage().click_one_contact_631('大佬1')
            if not b:
                SelectContactsPage().click_one_contact_631('大佬2')
            labelpage.click_sure()
        # 进入多方通话
        labelpage.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/image_third_colum'))

        # 输入非全名 查看是否能模糊匹配到联系人
        from pages import SelectLocalContactsPage
        selectpage = SelectLocalContactsPage()
        selectpage.search('联系人')
        # 搜索到指定联系人选择之后 搜索栏清空 呼叫按钮可点击
        selectpage.click_element((MobileBy.XPATH, '//*[contains(@text, "大佬1")]'))
        time.sleep(3)
        selectpage.element_should_be_enabled((MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'))

        """判断输入框是否自动清空"""
        self.assertTrue(selectpage.page_should_not_contain_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_delect')))

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_call_wangqiong_0193(self):
        """多方电话联系人选择器支持搜索保存在本地的固号呼叫"""
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_element((MobileBy.ID, "com.chinasofti.rcs:id/btnFreeCall"))
        # 选择指定联系人 点击呼叫
        selectcontacts = SelectContactsPage()
        selectcontacts.search('大佬3')
        selectcontacts.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' + '@text="大佬3"]'))
        time.sleep(4)
        selectcontacts.click_sure_bottom()
        time.sleep(3)
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        if callcontact._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt')):
            callcontact.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/andfetion_tip_bt'))
            callcontact.get_source()
        if not callcontact._is_element_present((MobileBy.XPATH, "//*[contains(@text, '我')]")):
            callcontact.click_element((MobileBy.ID, 'com.android.packageinstaller:id/permission_allow_button'), 1,
                                      False)

        # 是否存在设置悬浮窗，存在去设置页设置权限
        if callcontact._is_element_present((MobileBy.ID, 'android:id/button1')):
            callcontact.click_element((MobileBy.ID, 'android:id/button1'))
            current_mobile().click_element((MobileBy.ID, 'android:id/switch_widget'))
            current_mobile().click_element((MobileBy.XPATH, '//android.widget.ImageButton[@content-desc="向上导航"]'))

        # 挂断多方通话
        time.sleep(6)
        callpage = CallPage()
        callpage.hang_up_hefeixin_call()
        time.sleep(3)
        #
        # 挂断电话回到多方通话界面
        self.assertTrue(callcontact._is_element_present((MobileBy.ID, "com.chinasofti.rcs:id/btnFreeCall")))

    @staticmethod
    def setUp_test_call_wangqiong_0033():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0033(self):
        """本网用户各和飞信电话入口，可成功发起呼叫"""
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        # 1.在通讯录（群聊、单聊/标签分组）profile页，点击：和飞信电话（免费），发起呼叫（呼叫成功后挂断）
        contactspage.click_search_box()
        contact = ContactListSearchPage()
        contact.input_search_keyword("大佬1")
        contact.click_contact("大佬1")
        # 点击和飞信电话,呼叫成功后挂断
        callcontactdetail = CallContactDetailPage()
        callcontactdetail.click_text_or_description("飞信电话")
        # 挂断和飞信电话
        callpage = CallPage()
        time.sleep(2)
        contactdetail = ContactDetailsPage()
        contactdetail.click_back_icon()
        # 返回到联系人页面
        contact.click_back()
        time.sleep(2)
        # 3.进入通话页签 输入数字进行拨打和飞信电话
        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击拨号键，输入号码并拨打,选择'和飞信电话（免费）'
        callpage.click_call()
        callpage.dial_number('18311111111')
        time.sleep(2)
        callpage.click_call_phone()
        calltype = CallTypeSelectPage()
        calltype.click_call_by_app_631()

    @staticmethod
    def setUp_test_call_wangqiong_0172():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        contacts.click_mobile_contacts()
        contacts.click_label_grouping()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0172(self):
        """标签分组-多方电话选择器-支持组员名称号码搜索"""
        labellist = LabelGroupingPage()
        labellist.click_label_group('分组1')
        # 选择成员进行多方通话
        labellist.click_third_image_call()
        # CheckPoint： 选择成员成功发起呼叫
        labellist.select_local_contacts("大佬1", "大佬2")

    @staticmethod
    def setUp_call_wangqiong_0194():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0194(self):
        """多方电话联系人选择器支持搜索正确陌生内地固号"""
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        # callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 点击搜索框搜索联系人 查看搜索结果，点击呼叫
        contactselect = SelectContactsPage()
        contactselect.search('+860206631888')
        # checkpoint： 查看+860206631888 匹配结果，没有匹配结果
        contactselect.page_should_not_contain_text('未知号码')
        # 清空搜索栏
        contactselect.clear_serchbar_keyword()
        # checkpoint： 搜索0206631885 查看匹配结果“未知号码”、并点击呼叫
        contactselect.search('0206631885')
        contactselect.is_present_unknown_member()
        contactselect.click_unknown_member()
        # 呼叫
        time.sleep(2)
        contactselect.click_sure_bottom()

    @staticmethod
    def setUp_test_call_wangqiong_0204():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0204(self):
        """网络信号正常，发起多方电话流程正常"""
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 选择指定联系人 点击呼叫
        from pages.components import ContactsSelector
        contactselect = ContactsSelector()
        contactselect.select_local_contacts("大佬1", "大佬2", "大佬3")

    @staticmethod
    def setUp_test_call_wangqiong_0210():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0210(self):
        """多方电话呼叫中---网络正常下，会控界面显示正常"""

        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 选择指定联系人 点击呼叫
        from pages.components import ContactsSelector
        contactselect = ContactsSelector()
        contactselect.select_local_contacts("大佬1", "大佬2", "大佬3")

    @staticmethod
    def setUp_test_call_wangqiong_0211():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0211(self):
        """多方电话呼叫中时--网络正常下，会控界面点击顶部可返回至系统通话页"""
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 选择指定联系人 点击呼叫
        from pages.components import ContactsSelector
        contactselect = ContactsSelector()
        contactselect.select_local_contacts("大佬1", "大佬2", "大佬3")

    @staticmethod
    def setUp_test_call_wangqiong_0262():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0262(self):
        """会控界面：“未接听”状态的成员，可支持重新拨号、移除成员、取消成功"""
        """前置条件：保证contactnum1为真实号码 ，contactnum2为非真实现网手机"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()
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
        selectcontacts.search("大佬2")
        selectcontacts.click_contact_by_name("大佬2")
        time.sleep(2)
        selectcontacts.click_sure_bottom()
        time.sleep(2)

    @staticmethod
    def setUp_test_call_wangqiong_0266():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0266(self):
        """发起多方电话呼叫邀请中，可点击会控界面挂断按钮，结束多方电话通话"""
        # 启动App
        Preconditions.select_mobile('Android-移动')
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
        selectcontacts.search("大佬2")
        selectcontacts.click_contact_by_name("大佬2")
        time.sleep(2)
        selectcontacts.click_sure_bottom()
        time.sleep(2)

    @staticmethod
    def setUp_test_call_wangqiong_0267():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0267(self):
        """发起多方电话呼叫邀请中，可点击系统电话挂断，结束多方电话通话"""
        Preconditions.select_mobile('Android-移动')
        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击飞信电话图标
        callcontact.click_free_call()
        # 选择指定联系人 点击呼叫
        from pages.components import ContactsSelector
        contactselect = ContactsSelector()
        contactselect.select_local_contacts("大佬3")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0288(self):
        """多人的多方电话--通话记录详情页各信息显示正常。"""
        Preconditions.select_mobile('Android-移动')
        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 选择指定联系人 点击呼叫
        from pages.components import ContactsSelector
        contactselect = ContactsSelector()
        contactselect.select_local_contacts("大佬1", "大佬2")
        callpage = CallPage()
        time.sleep(3)
        callpage.click_ganggang_call_time()
        # Checkpoint：查看详情页面是否是多方电话？
        callpage.is_hefeixin_page('飞信电话')
        time.sleep(3)
        # Checkpoint：详情页是否有‘再次呼叫’、‘一键建群’
        self.assertTrue(callpage.page_should_contain_text('再次呼叫'))
        self.assertTrue(callpage.page_should_contain_text('一键建群'))

    @staticmethod
    def setUp_test_call_wangqiong_0289():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0289(self):
        """发起1人的多方电话--通话记录详情页各信息显示正常。"""

        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击飞信电话图标
        callcontact.click_free_call()
        # 选择指定联系人 点击呼叫
        from pages.components import ContactsSelector
        contactselect = ContactsSelector()
        contactselect.select_local_contacts("大佬1")
        time.sleep(3)
        callpage = CallPage()
        callpage.click_ganggang_call_time()
        # Checkpoint：查看详情页面是否是和飞信电话？
        callpage.is_hefeixin_page('飞信电话')
        time.sleep(3)
        # Checkpoint：详情页是否有‘再次呼叫’
        self.assertTrue(callpage.page_should_contain_text('再次呼叫'))

    @staticmethod
    def setUp_test_call_wangqiong_0291():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0291(self):
        """多方通话记录详情页--再次呼叫，网络正常重新呼叫多方电话"""
        Preconditions.select_mobile('Android-移动')
        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击飞信电话
        callcontact.click_free_call()
        # 选择指定联系人 点击呼叫
        from pages.components import ContactsSelector
        contactselect = ContactsSelector()
        contactselect.select_local_contacts("大佬1", "大佬2")
        callpage = CallPage()
        callpage.click_ganggang_call_time()
        # Checkpoint：查看详情页面是否是多方电话？
        callpage.is_hefeixin_page('飞信电话')
        # 点击‘再次呼叫’
        callpage.click_mutil_call_again()

    @staticmethod
    def setUp_test_call_wangqiong_0292():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0292(self):
        """发起1人的多方电话--再次呼叫，网络正常重新呼叫和飞信电话"""

        # 启动App
        Preconditions.select_mobile('Android-移动')
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
        contactselect.select_local_contacts("大佬1")
        callpage = CallPage()
        callpage.click_ganggang_call_time()
        # Checkpoint：查看详情页面是否是为飞信电话？
        callpage.is_hefeixin_page('飞信电话')
        # 点击‘再次呼叫’
        callpage.click_mutil_call_again()


    @staticmethod
    def setUp_test_msg_xiaoqiu_0282():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0282(self):
        """通讯录-群聊-英文精确搜索——搜索结果展示"""
        # 1、网络正常
        # 2、已登录和飞信
        # 3、选择一个群——群聊列表展示页面
        # 4、存在跟搜索条件匹配的群聊
        # 5、通讯录-群聊
        # Step 中文精确搜索
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

    @staticmethod
    def setUp_test_msg_xiaoqiu_0283():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0283(self):
        """通讯录-群聊-英文精确搜索——搜索结果展示"""
        # 1、网络正常
        # 2、已登录和飞信
        # 3、选择一个群——群聊列表展示页面
        # 4、存在跟搜索条件匹配的群聊
        # 5、通讯录-群聊
        # Step 中文精确搜索
        contactspage = ContactsPage()
        grouplist = GroupListPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        contactspage.click_group_chat_631()
        grouplist.click_search_input()
        group_search = GroupListSearchPage()
        group_search.input_search_keyword('fFOWEPQPW')
        # Checkpoint 可以匹配展示搜索结果
        contactspage.page_should_contain_text('无搜索结果')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0289():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0289(self):
        """群通讯录-群聊-数字精确搜索——搜索结果展示"""
        # 1、网络正常
        # 2、已登录和飞信
        # 3、选择一个群——群聊列表展示页面
        # 4、存在跟搜索条件匹配的群聊
        # 5、通讯录-群聊
        # Step 中文精确搜索
        contactspage = ContactsPage()
        grouplist = GroupListPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        contactspage.click_group_chat_631()
        grouplist.click_search_input()
        group_search = GroupListSearchPage()
        group_search.input_search_keyword('84949498416418')
        # Checkpoint 可以匹配展示搜索结果
        contactspage.page_should_contain_text('无搜索结果')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0290():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0290(self):
        """通讯录-群聊-字符精确搜索——搜索结果展示"""
        # 1、网络正常
        # 2、已登录和飞信
        # 3、选择一个群——群聊列表展示页面
        # 4、存在跟搜索条件匹配的群聊
        # 5、通讯录-群聊
        # Step 中文精确搜索
        contactspage = ContactsPage()
        grouplist = GroupListPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        contactspage.click_group_chat_631()
        grouplist.click_search_input()
        group_search = GroupListSearchPage()
        group_search.input_search_keyword('给个红包3')
        # Checkpoint 可以匹配展示搜索结果
        self.assertTrue(group_search.is_group_in_list('给个红包3'))

    @staticmethod
    def setUp_test_msg_xiaoqiu_0284():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0284(self):
        """通讯录-群聊-空格精确搜索——搜索结果展示"""
        # 1、网络正常
        # 2、已登录和飞信
        # 3、选择一个群——群聊列表展示页面
        # 4、存在跟搜索条件匹配的群聊
        # 5、通讯录-群聊
        # Step 中文精确搜索
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

    @staticmethod
    def setUp_test_msg_xiaoqiu_0285():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0285(self):
        """通讯录-群聊-空格精确搜索——搜索结果展示"""
        # 1、网络正常
        # 2、已登录和飞信
        # 3、选择一个群——群聊列表展示页面
        # 4、存在跟搜索条件匹配的群聊
        # 5、通讯录-群聊
        # Step 中文精确搜索
        contactspage = ContactsPage()
        grouplist = GroupListPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        contactspage.click_group_chat_631()
        grouplist.click_search_input()
        group_search = GroupListSearchPage()
        group_search.input_search_keyword('测  试  空  格')
        # Checkpoint 可以匹配展示搜索结果
        contactspage.page_should_contain_text('无搜索结果')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0291():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0291(self):
        """通讯录-群聊-字符精确搜索——搜索结果展示"""
        # 1、网络正常
        # 2、已登录和飞信
        # 3、选择一个群——群聊列表展示页面
        # 4、存在跟搜索条件匹配的群聊
        # 5、通讯录-群聊
        # Step 中文精确搜索
        contactspage = ContactsPage()
        grouplist = GroupListPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        contactspage.click_group_chat_631()
        grouplist.click_search_input()
        group_search = GroupListSearchPage()
        group_search.input_search_keyword('测试%^&%&*飞')
        # Checkpoint 可以匹配展示搜索结果
        contactspage.page_should_contain_text('无搜索结果')


    @staticmethod
    def setUp_test_msg_xiaoqiu_0400():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0400(self):
        """验证群主A或群成员B在设置页面——点击+邀请群成员C后——发起人收到的群消息"""
        # 1、已登录客户端
        # 2、网络正常
        # 3、当前在群会话窗口页面
        mess = MessagePage()
        groupchat = GroupChatPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        # Step 1、群主A或群成员吧在群设置页面点击+添加C
        GroupChatSetPage().click_add_number2()
        # Checkpoint 跳转到联系人选择器页面
        # Step 任意选中一个联系人，点击右上角的确定按钮
        ContactsSelector().select_local_contacts('测试短信1')
        # Step A或B返回到会话窗口页面查看
        time.sleep(2)
        # Checkpoint 收到群消息：你向C发出群邀请
        mess.page_should_contain_text("你向 测试短信1... 发出群邀请")

    @staticmethod
    def setUp_test_msg_xiaoqiu_0286():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0286(self):
        """通讯录-群聊-数字精确搜索——搜索结果展示"""
        # 1、网络正常
        # 2、已登录和飞信
        # 3、选择一个群——群聊列表展示页面
        # 4、存在跟搜索条件匹配的群聊
        # 5、通讯录-群聊
        # Step 中文精确搜索
        contactspage = ContactsPage()
        grouplist = GroupListPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        contactspage.click_group_chat_631()
        grouplist.click_search_input()
        group_search = GroupListSearchPage()
        group_search.input_search_keyword('给个红包2')
        # Checkpoint 可以匹配展示搜索结果
        self.assertTrue(group_search.is_group_in_list('给个红包2'))

    @staticmethod
    def setUp_test_msg_xiaoqiu_0402():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0402(self):
        """验证群主A点击消息列表右上角的+——发起群聊/点对点建群/点击通讯录右上角，创建群后A收到的群消息"""
        # 1、已登录客户端
        # 2、网络正常
        # 3、当前在群会话窗口页面
        mess = MessagePage()
        # Step 1、A选择联系人后进行创建群
        mess.click_add_icon()
        mess.click_group_chat()
        select_cont = SelectContactsPage()
        # Step 选择手机联系人
        select_cont.select_local_contacts()
        ContactsSelector().click_local_contacts('测试短信1')
        ContactsSelector().click_local_contacts('测试短信2')
        select_cont.click_sure_bottom()
        # Checkpoint 跳转到群名称设置页面
        GroupNamePage().wait_for_page_load_631()
        groupname = GroupNamePage()
        groupname.wait_for_page_load_631()
        groupname.clear_input_group_name()
        groupname.input_group_name_631('测试群组88')
        groupname.click_sure()
        # Step  A返回到会话窗口页面查看群消息
        GroupChatPage().wait_for_page_load()
        # Checkpoint 群消息显示：你向“XX, XX, XX...”发出群邀请（逗号为中文字符；提示语姓名不加双引号，前后用空格；...省略号后加一个空格）
        GroupChatPage().page_should_contain_text('你向 +86138********,+86138********... 发出群邀请')

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0402():
        groupset = GroupChatSetPage()
        # 建群完成以后删除
        groupset.click_group_manage()
        groupset.wait_exist_and_delete_confirmation_box_load()
        groupset.click_group_manage_disband_button()
        SingleChatPage().click_sure()


    @staticmethod
    def setUp_test_msg_xiaoqiu_0404():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0404(self):
        """在全局搜索搜索群聊时——点击进入到群会话窗口——群设置页面(重复在消息列表页已有的群聊列表进入到群这个入口进群进行测试)"""
        # 1、已登录客户端
        # 2、网络正常
        # 3、当前在消息列表页面
        mess = MessagePage()
        # Step 1、在消息列表页点击全局搜索框，进行群聊搜索
        mess.search_and_enter('给个红包4')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        # Step 2、点击右上角的群设置按钮
        groupchat.click_setting()
        # Checkpoint 2、进入到群设置页面
        groupset.wait_for_page_load()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0405():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0405(self):
        """在点击消息列表右上角的+，选择发起群聊，新成功创建的群会话窗口和群设置页面(重复在消息列表页已有的群聊列表进入到群这个入口进群进行测试)"""
        # 1、已登录客户端
        # 2、网络正常
        # 3、当前在群会话窗口页面
        mess = MessagePage()
        # Step 1、在消息列表页点击右上角的+选择发起群聊进行建群
        mess.click_add_icon()
        mess.click_group_chat()
        select_cont = SelectContactsPage()
        select_cont.select_local_contacts()
        ContactsSelector().click_local_contacts('测试短信1')
        ContactsSelector().click_local_contacts('测试短信2')
        select_cont.click_sure_bottom()
        GroupNamePage().wait_for_page_load_631()
        groupname = GroupNamePage()
        groupname.wait_for_page_load_631()
        groupname.clear_input_group_name()
        groupname.input_group_name_631('测试群组88')
        groupname.click_sure()
        # Checkpoint 1、建群成功返回到会话窗口页面
        GroupChatPage().wait_for_page_load()
        # Step 2、点击右上角的群设置按钮
        GroupChatPage().click_setting()
        # Checkpoint 2、进入到群设置页面
        GroupChatSetPage().wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0405():
        groupset = GroupChatSetPage()
        # 建群完成以后删除
        groupset.click_group_manage()
        groupset.wait_exist_and_delete_confirmation_box_load()
        groupset.click_group_manage_disband_button()
        SingleChatPage().click_sure()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0406():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0406(self):
        """在点击消息列表右上角的+，选择发起群聊选择已有群进入到群会话窗口和群设置页面(重复在消息列表页已有的群聊列表进入到群这个入口进群进行测试)"""
        # 1、已登录客户端
        # 2、网络正常
        # 3、当前在消息列表页面
        mess = MessagePage()
        # Step 1、在消息列表页点击右上角的+选择发起群聊，选择已有群，点击任意群聊
        mess.click_add_icon()
        mess.click_group_chat()
        select_cont = SelectContactsPage()
        select_cont.click_select_one_group()
        SearchGroupPage().click_group('群聊2')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        # Checkpoint 1、进入会话窗口页面
        groupchat.wait_for_page_load()
        # Step 2、点击右上角的群设置按钮
        groupchat.click_setting()
        # Checkpoint 2、进入到群设置页面
        groupset.wait_for_page_load()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0408():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0408(self):
        """点击通讯录——点击群聊——任意选中一个群——进入到群会话窗口和群设置页面"""
        # 1、已登录客户端
        # 2、网络正常
        # 3、当前在通讯录群聊页面
        # Step 1、在群聊页面点击任意群聊
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        contactspage.click_group_chat_631()
        SearchGroupPage().click_group('群聊2')
        groupchat = GroupChatPage()
        # Checkpoint 1、进入会话窗口页面
        groupchat.wait_for_page_load()
        # Step 2、点击右上角的群设置按钮
        groupchat.click_setting()
        # Checkpoint 2、进入到群设置页面
        GroupChatSetPage().wait_for_page_load()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0409():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0409(self):
        """点击通讯录——点击群聊——点击右上角创建群聊按钮——进入到会话窗口和群设置页面"""
        # 1、已登录客户端
        # 2、网络正常
        # 3、当前通讯录群聊页面
        contactspage = ContactsPage()
        grouplist = GroupListPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        contactspage.click_group_chat_631()
        grouplist.click_create_group()
        # Step 选择手机联系人
        select_cont = SelectContactsPage()
        select_cont.select_local_contacts()
        ContactsSelector().click_local_contacts('大佬2')
        select_cont.click_back()
        select_cont.click_search_keyword()
        select_cont.input_search_keyword('13901390144')
        select_cont.select_one_contact_by_name('13901390144(未知号码)')
        select_cont.click_sure_bottom()
        # Checkpoint 跳转到群名称设置页面
        groupname = GroupNamePage()
        groupname.wait_for_page_load_631()
        groupname.clear_input_group_name()
        groupname.input_group_name_631('测试群组88')
        groupname.click_sure()
        # Checkpoint 可以创建普通群聊成功
        GroupChatPage().wait_for_page_load()
        # Step 2、点击右上角的群设置按钮
        GroupChatPage().click_setting()
        # Checkpoint 2、进入到群设置页面
        GroupChatSetPage().wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0409():
        groupset = GroupChatSetPage()
        # 建群完成以后删除
        groupset.click_group_manage()
        groupset.wait_exist_and_delete_confirmation_box_load()
        groupset.click_group_manage_disband_button()
        SingleChatPage().click_sure()



    @staticmethod
    def setUp_test_msg_xiaoqiu_0534():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0534(self):
        """创建一个普通群"""
        # 1、网络正常
        # 2、已登录和飞信
        # 4、当前用户未创建任何群聊
        mess = MessagePage()
        # Step 使用创建群聊功能，创建1个普通群
        Preconditions.create_group_if_not_exist_not_enter_chat('测试群组5', "大佬1", "大佬2")
        mess.search_and_enter('测试群组5')
        groupchat = GroupChatPage()
        # Checkpoint 可以正常创建一个普通群
        groupchat.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0534():
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        # 建群完成以后删除
        groupchat.click_setting()
        groupset.wait_for_page_load()
        groupset.click_group_manage()
        groupset.wait_exist_and_delete_confirmation_box_load()
        groupset.click_group_manage_disband_button()
        SingleChatPage().click_sure()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0548():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.enter_group_chat_page("给个红包1")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0548(self):
        """ 普通群，分享群聊邀请口令"""
        # 1、网络正常
        # 2、已加入或创建普通群
        # 3、已消除红点
        # 4、群主、群成员
        # 5、仅限大陆本网和异网号码
        mess = MessagePage()
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        groupset.wait_for_page_load()
        # Step 在群聊设置页面，点击邀请微信或QQ好友进群入口
        groupset.click_avetor_qq_wechat_friend()
        # Checkpoint 小于等于15秒内加载成功，弹出：群口令分享弹窗
        groupset.wait_for_share_group_load()
        # Step 点击下次再次按钮
        groupset.click_say_next()
        # Checkpoint 弹窗消失并且返回到群聊设置页面
        groupset.wait_for_page_load()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0605():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.enter_group_chat_page("给个红包1")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0605(self):
        """开启免打扰后，在聊天页面在输入框输入内容-返回到消息列表页时，该消息列表窗口直接展示：草稿"""
        # 1、当前在群聊（普通群/企业群）会话窗口页面
        mess = MessagePage()
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        # Step 在当前页面点击右上角的设置按钮
        groupchat.click_setting()
        groupset.wait_for_page_load()
        # Step 消息免打扰开启状态
        if not groupset.get_switch_undisturb_status():
            # Checkpoint 2、开启成功
            groupset.click_switch_undisturb()
        groupset.click_back()
        # Step 返回到会话窗口，在输入框中进行输入内容，然后点击左上角的返回按钮
        groupchat.input_text_message('呵呵呵1')
        groupchat.send_text()
        groupchat.input_text_message('呵呵呵2')
        groupchat.click_back()
        SearchPage().click_back_button()
        # Step 查看该消息列表窗口显示
        mess.page_should_contain_text('测试群组1')
        # Checkpoint 该消息列表窗口直接展示：草稿
        mess.page_should_contain_text('[草稿] ')
        mess.page_should_contain_text('呵呵呵2')
        mess.delete_message_record_by_name("测试群组1")

    @staticmethod
    def setUp_test_msg_xiaoqiu_0613():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.enter_group_chat_page("给个红包1")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0613(self):
        """首次创建群聊桌面快捷方式"""
        # 1、手机存在桌面快捷方式权限
        # 2、已开启此权限或者此权限默认为开启状态
        # 3、登录和飞信
        # 4、进入到群聊设置页面
        mess = MessagePage()
        groupchat = GroupChatPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        groupset = GroupChatSetPage()
        # Step 点击创建桌面快捷方式入口，弹窗展示
        groupset.click_add_destop_link()
        # Checkpoint 弹窗内容展示为，标题：已尝试添加桌面，内容：若添加失败，请在手机系统设置中，为和飞信打开“创建桌面快捷方式”的权限，复选框选择项：不再提醒，可点击按钮我知道了
        groupset.check_element_for_add_destop_link()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0614():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.enter_group_chat_page("给个红包1")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0614(self):
        """首次创建群聊桌面快捷方式"""
        # 1、手机存在桌面快捷方式权限
        # 2、已开启此权限或者此权限默认为开启状态
        # 3、登录和飞信
        # 4、进入到群聊设置页面
        # 5、不勾选弹窗中复选框
        mess = MessagePage()
        groupchat = GroupChatPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        groupset = GroupChatSetPage()
        # Step 点击创建桌面快捷方式入口，弹窗展示
        groupset.click_add_destop_link()
        # Step 不勾选弹窗复选框，点击：我知道了
        groupset.check_element_for_add_destop_link()
        groupset.click_iknow_but()
        # Step 3、重复进行1，2.步骤
        groupset.click_add_destop_link()
        # Checkpoint 桌面快捷方式创建成功校验
        groupset.check_element_for_add_destop_link()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0427():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.enter_group_chat_page("给个红包1")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0427(self):
        """聊天会话页面——长按——撤回——发送失败的文本消息"""
        # 1、网络正常
        # 2、登录和飞信
        # 3、已加入普通群
        # 4、聊天会话页面，存在发送失败的消息
        # 5、普通群/单聊/企业群/我的电脑/标签分组
        mess = MessagePage()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_tips_display():
            chatdialog.accept_and_close_tips_alert()

        single = SingleChatPage()
        # 如果当前页面不存在消息，发送一条消息
        if not single.is_text_present('测试一个呵呵'):
            single.input_text_message("测试一个呵呵")
            single.send_text()
        time.sleep(60)
        single.press_mess("测试一个呵呵")
        single.click_recall()
        single.if_exist_i_know_click()
        time.sleep(3)
        # Checkpoint 可以成功撤回此条消息并且在会话窗口展示：你撤回了一条消息
        mess.page_should_contain_text('你撤回了一条信息')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0496():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 进入单聊页面
        Preconditions.enter_private_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0496(self):
        """仅语音模式下——语音录制中途——点击下角的发送按钮"""
        chat_window_page = ChatWindowPage()
        # 点击语音
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_audio'))
        time.sleep(3)
        try:
            ok_buttons = chat_window_page.get_elements(MobileBy.XPATH,
                                                       '//*[@resource-id="android:id/button1" and @text ="允许"]')
            if len(ok_buttons) > 0:
                ok_buttons[0].click()
        except BaseException as e:
            print(e)
        time.sleep(1)
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/recodr_audio_finish'))
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/recodr_audio_finish'))
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/select_send_voice'))
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/select_send_audio_type_confirm'))
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/recodr_audio_finish'))

    @staticmethod
    def setUp_test_msg_xiaoqiu_0504():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 进入单聊页面
        Preconditions.enter_private_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0504(self):
        """表情消息-表情发送"""
        chat_window_page = ChatWindowPage()
        chat_window_page.click_expression()
        time.sleep(3)
        element = chat_window_page.get_element(
            (MobileBy.ID, 'com.chinasofti.rcs:id/vp_expression'))
        for i in range(5):
            time.sleep(3)
            expression_images = chat_window_page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iv_expression_image"]'))
            for expression_image in expression_images:
                expression_image.click()
            chat_window_page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/vp_expression'), 'left')

        chat_window_page.click_send_button()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0528():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 进入我的电脑页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.search_and_enter("我的电脑")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0528(self):
        """仅语音模式——语音录制中途——点击右下角的发送按钮"""
        chat_window_page = ChatWindowPage()
        # 点击语音
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_audio'))
        time.sleep(3)
        try:
            ok_buttons = chat_window_page.get_elements(MobileBy.XPATH,
                                                       '//*[@resource-id="android:id/button1" and @text ="允许"]')
            if len(ok_buttons) > 0:
                ok_buttons[0].click()
        except BaseException as e:
            print(e)
        time.sleep(3)
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/recodr_audio_finish'))
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/recodr_audio_finish'))
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/select_send_voice'))
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/select_send_audio_type_confirm'))
        time.sleep(3)
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/recodr_audio_finish'))

    @staticmethod
    def setUp_test_msg_xiaoqiu_0531():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 进入我的电脑页面
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.search_and_enter("我的电脑")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0531(self):
        """仅语音模式——发送录制的语音消息"""
        chat_window_page = ChatWindowPage()
        # 点击语音
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_audio'))
        time.sleep(3)
        try:
            ok_buttons = chat_window_page.get_elements(MobileBy.XPATH,
                                                       '//*[@resource-id="android:id/button1" and @text ="允许"]')
            if len(ok_buttons) > 0:
                ok_buttons[0].click()
        except BaseException as e:
            print(e)
        time.sleep(3)
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/recodr_audio_finish'))
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/recodr_audio_finish'))
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/select_send_voice'))
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/select_send_audio_type_confirm'))
        time.sleep(11)
        chat_window_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/recodr_audio_finish'))

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0001():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0001(self):
        """进入新建消息是否正常"""
        mess = MessagePage()
        # 点击+号
        mess.click_add_icon()
        # 点击新建消息
        mess.click_new_message()
        freemsg = FreeMsgPage()
        select_page = SelectContactPage()
        # 判断存在选择联系人
        select_page.is_exist_select_contact_btn()
        # 判断存在搜索或输入手机号提示
        select_page.is_exist_selectorinput_toast()
        # 判断存在选择团队联系人按钮
        freemsg.page_should_contain_element((MobileBy.XPATH, '//*[@text ="选择团队联系人"]'))
        # 判断存在手机联系人列表
        freemsg.page_should_contain_element((MobileBy.ID, 'com.chinasofti.rcs:id/contact_list'))

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0044():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0044(self):
        """消息-消息列表进入"""
        mess = MessagePage()
        mess.page_should_contain_element((MobileBy.ID, 'com.chinasofti.rcs:id/tv_title'))

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0001():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # 下面根据用例情况进入相应的页面

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_E_0001(self):
        """消息-消息列表界面搜索框显示"""
        mess = MessagePage()
        mess.assert_search_box_is_display()

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0006():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_E_0006(self):
        """搜索关键字-精准搜索"""
        mess = MessagePage()
        mess.click_search()
        searchbar = SearchBar()
        searchbar.input_search_keyword('给个红包1')
        search = SearchPage()
        search.assert_contact_name_display('给个红包1')

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0007():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_E_0007(self):
        """搜索关键字-中文模糊搜索"""
        mess = MessagePage()
        mess.click_search()
        searchbar = SearchBar()
        searchbar.input_search_keyword('给个红包')
        search = SearchPage()
        search.assert_contact_name_display('给个红包1')
        search.assert_contact_name_display('给个红包2')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0433():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.enter_group_chat_page("给个红包2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0433(self):
        """聊天会话页面——长按——撤回——不足一分钟的语音消息"""
        # 1、网络正常
        # 2、登录和飞信
        # 3、已加入普通群
        # 4、聊天会话页面
        # 5、存在发送成功时间，小于1分钟的消息
        # 6、普通群/单聊/企业群/我的电脑/标签分组
        mess = MessagePage()
        # Step 进入群聊页面
        groupchat = GroupChatPage()
        chataudio = ChatAudioPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        # Step 清除聊天记录
        groupchat.click_setting()
        groupset.wait_for_page_load()
        groupset.click_clear_chat_record()
        groupset.wait_clear_chat_record_confirmation_box_load()
        groupset.click_determine()
        groupset.click_back()
        groupchat.click_audio_btn()
        # 若第一次进入存在选择语音模式页面，选择仅发送语音
        if chataudio.wait_for_audio_type_select_page_load(auto_accept_alerts=True):
            chataudio.click_only_voice_631()
            chataudio.click_sure()
        # 若存在语音权限申请弹框，点击允许
        if chataudio.wait_for_audio_allow_page_load():
            chataudio.click_allow()
        # 若当前在智能识别模式，录入语音3s后会弹出设置按钮，设置为仅发送语音
        if chataudio.is_exist_setting_bottom():
            chataudio.click_setting_bottom()
            chataudio.click_only_voice_631()
            chataudio.click_sure()
        time.sleep(3)
        chataudio.click_send_bottom()
        time.sleep(1)
        # Step 1、长按发送成功的消息
        groupchat.press_voice_message()
        # Checkpoint 弹出的功能列表中，存在撤回功能
        groupchat.click_recall()
        groupchat.if_exist_i_know_click()
        time.sleep(3)
        # Checkpoint 可以成功撤回此条消息并且在会话窗口展示：你撤回了一条消息
        mess.page_should_contain_text('你撤回了一条信息')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0434():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.enter_group_chat_page("给个红包2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0434(self):
        """聊天会话页面——长按撤回——超过一分钟的语音消息"""
        # 1、网络正常
        # 2、登录和飞信
        # 3、已加入普通群
        # 4、聊天会话页面
        # 5、存在发送成功时间，小于1分钟的消息
        # 6、普通群/单聊/企业群/我的电脑/标签分组
        mess = MessagePage()
        # Step 进入群聊页面
        groupchat = GroupChatPage()
        chataudio = ChatAudioPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        # Step 清除聊天记录
        groupchat.click_setting()
        groupset.wait_for_page_load()
        groupset.click_clear_chat_record()
        groupset.wait_clear_chat_record_confirmation_box_load()
        groupset.click_determine()
        groupset.click_back()
        groupchat.click_audio_btn()
        # 若第一次进入存在选择语音模式页面，选择仅发送语音
        if chataudio.wait_for_audio_type_select_page_load(auto_accept_alerts=True):
            chataudio.click_only_voice_631()
            chataudio.click_sure()
        # 若存在语音权限申请弹框，点击允许
        if chataudio.wait_for_audio_allow_page_load():
            chataudio.click_allow()
        # 若当前在智能识别模式，录入语音3s后会弹出设置按钮，设置为仅发送语音
        if chataudio.is_exist_setting_bottom():
            chataudio.click_setting_bottom()
            chataudio.click_only_voice_631()
            chataudio.click_sure()
        time.sleep(3)
        chataudio.click_send_bottom()
        time.sleep(60)
        # Step 1、长按发送成功的消息
        groupchat.press_voice_message()
        # Checkpoint 弹出的功能列表中，存在撤回功能
        groupchat.click_recall()
        groupchat.if_exist_i_know_click()
        time.sleep(3)
        # Checkpoint 可以成功撤回此条消息并且在会话窗口展示：你撤回了一条消息
        mess.page_should_contain_text('你撤回了一条信息')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0436():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.enter_group_chat_page("给个红包2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0436(self):
        """聊天会话页面——长按撤回——大于10分钟的语音消息"""
        # 1、网络正常
        # 2、登录和飞信
        # 3、已加入普通群
        # 4、聊天会话页面
        # 5、存在发送成功时间，小于1分钟的消息
        # 6、普通群/单聊/企业群/我的电脑/标签分组
        groupchat = GroupChatPage()
        chataudio = ChatAudioPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        # Step 清除聊天记录
        groupchat.click_setting()
        groupset.wait_for_page_load()
        groupset.click_clear_chat_record()
        groupset.wait_clear_chat_record_confirmation_box_load()
        groupset.click_determine()
        groupset.click_back()
        groupchat.click_audio_btn()
        # 若第一次进入存在选择语音模式页面，选择仅发送语音
        if chataudio.wait_for_audio_type_select_page_load(auto_accept_alerts=True):
            chataudio.click_only_voice_631()
            chataudio.click_sure()
        # 若存在语音权限申请弹框，点击允许
        if chataudio.wait_for_audio_allow_page_load():
            chataudio.click_allow()
        # 若当前在智能识别模式，录入语音3s后会弹出设置按钮，设置为仅发送语音
        if chataudio.is_exist_setting_bottom():
            chataudio.click_setting_bottom()
            chataudio.click_only_voice_631()
            chataudio.click_sure()
        time.sleep(3)
        chataudio.click_send_bottom()
        a = 10 * 60
        while a > 0:
            time.sleep(1)
            a -= 1
        time.sleep(2)
        # Step 1、长按发送成功的消息
        groupchat.press_voice_message()
        # Checkpoint 不可以成功此条消息（超过10分钟的消息，不能被撤回）
        mess = MessagePage()
        mess.page_should_not_contain_text('你撤回了一条信息')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0439():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.enter_group_chat_page("给个红包2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0439(self):
        """聊天会话页面——长按——不支持撤回的消息体"""
        # 1、网络正常
        # 2、登录和飞信
        # 3、已加入普通群
        # 4、聊天会话页面，
        # 5、存在发送成功时间小于10分钟的消息
        # 6、普通群/单聊/企业群/我的电脑/标签分组
        groupchat = GroupChatPage()
        chataudio = ChatAudioPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        # Step 清除聊天记录
        groupchat.click_setting()
        groupset.wait_for_page_load()
        groupset.click_clear_chat_record()
        groupset.wait_clear_chat_record_confirmation_box_load()
        groupset.click_determine()
        groupset.click_back()
        groupchat.click_audio_btn()
        # 若第一次进入存在选择语音模式页面，选择仅发送语音
        if chataudio.wait_for_audio_type_select_page_load(auto_accept_alerts=True):
            chataudio.click_only_voice_631()
            chataudio.click_sure()
        # 若存在语音权限申请弹框，点击允许
        if chataudio.wait_for_audio_allow_page_load():
            chataudio.click_allow()
        # 若当前在智能识别模式，录入语音3s后会弹出设置按钮，设置为仅发送语音
        if chataudio.is_exist_setting_bottom():
            chataudio.click_setting_bottom()
            chataudio.click_only_voice_631()
            chataudio.click_sure()
        current_mobile().set_network_status(1)
        time.sleep(3)
        chataudio.click_send_bottom()
        time.sleep(1)
        # Step 1、长按发送失败的消息
        groupchat.press_voice_message()
        # Checkpoint 2、弹出的功能列表中，不存在撤回功能（发送失败的消息，不允许进行撤回操作）
        mess = MessagePage()
        mess.page_should_not_contain_text('撤回')

    def tearDown_msg_xiaoqiu_0439(self):
        current_mobile().set_network_status(6)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0440():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.enter_group_chat_page("给个红包2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0440(self):
        """聊天会话页面——在10分钟内长按——弹出功能菜单列表——10分钟后撤回"""
        # 1、网络正常
        # 2、登录和飞信
        # 3、已加入普通群
        # 4、聊天会话页面，
        # 5、存在发送成功时间小于10分钟的消息
        # 6、普通群/单聊/企业群/我的电脑/标签分组
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        # Step 清除聊天记录
        groupchat.click_setting()
        groupset.wait_for_page_load()
        groupset.click_clear_chat_record()
        groupset.wait_clear_chat_record_confirmation_box_load()
        groupset.click_determine()
        groupset.click_back()
        groupchat.click_input_box()
        # Step 1、成功发送一条消息
        groupchat.input_text_message('测试撤回了')
        groupchat.send_text()
        # Step 2、在10分钟内，长按弹出功能菜单列表
        groupchat.press_text_message()
        # Checkpoint 2、在10分钟内，长按弹出功能菜单列表
        mess = MessagePage()
        mess.page_should_contain_text('撤回')
        # Step 3、在超过10分钟后，点击撤回功能，是否可以撤回此条消息
        a = 10 * 60
        while a > 0:
            time.sleep(1)
            a -= 1
        time.sleep(2)
        groupchat.click_recall()
        groupchat.if_exist_i_know_click()
        # Checkpoint 3、在超过10分钟后，点击撤回功能，不可以撤回此条消息
        mess.page_should_not_contain_text('你撤回了一条信息')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0441():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.enter_group_chat_page("给个红包2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0441(self):
        """（普通消息体）聊天会话页面——5分钟内——连续发送文本消息体"""
        # 1、网络正常
        # 2、登录和飞信
        # 3、已加入普通群
        # 4、聊天会话页面
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        # Step 清除聊天记录
        groupchat.click_setting()
        groupset.wait_for_page_load()
        groupset.click_clear_chat_record()
        groupset.wait_clear_chat_record_confirmation_box_load()
        groupset.click_determine()
        groupset.click_back()
        groupchat.click_input_box()
        # Step 1、5分钟内，发送方连续发送文本消息，是否不出现重复头像，消息聚合展示
        groupchat.input_text_message('测试聚合消息1')
        groupchat.send_text()
        groupchat.input_text_message('测试聚合消息2')
        groupchat.send_text()
        # Checkpoint 不出现重复头像，消息聚合展示
        self.assertTrue(groupchat.is_multi_show())

    @staticmethod
    def setUp_test_msg_xiaoqiu_0465():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.enter_group_chat_page("给个红包2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0465(self):
        """查找聊天内容页-选择搜索结果-定位到的搜索结果展示页-输入框会自动填充上一次发送出去的内容"""
        # 1、网络正常
        # 2、已登录和飞信
        # 3、已加入普通群
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        # Step 清除聊天记录
        groupchat.click_setting()
        groupset.wait_for_page_load()
        groupset.click_clear_chat_record()
        groupset.wait_clear_chat_record_confirmation_box_load()
        groupset.click_determine()
        groupset.click_back()
        groupchat.click_input_box()
        # Step 1、在群聊会话页，发送一条消息
        groupchat.input_text_message('测试聚合消息1')
        groupchat.send_text()
        # Step 2、再在输入框中，录入内容
        groupchat.input_text_message('测试聚合消息2')
        # Step 3、去到群聊设置-查找聊天内容——选择搜索结果——定位到搜索结果页
        groupchat.click_setting()
        groupset.wait_for_page_load()
        groupset.click_find_chat_record()
        search = GroupChatSetFindChatContentPage()
        search.wait_for_page_load()
        # Step 在查找聊天内容页面，输入框中，输入中文搜索条件
        search.search('测试聚合消息1')
        # Step 任意选中一条聊天记录
        search.click_search_result('测试聚合消息1')
        # Checkpoint 跳转到聊天记录对应的位置
        groupchat.is_on_this_page()
        # Checkpoint 搜索结果展示页的输入框中，不会自动填充内容
        mess = MessagePage()
        mess.page_should_contain_text('说点什么...')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0469():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.enter_group_chat_page("给个红包2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0469(self):
        """在消息列表——长按置顶的会话窗口——检查弹出窗口"""
        # 1、网络正常
        # 2、已登录和飞信
        # 3、已加入普通群
        # 4、置顶聊天开关，开启状态（安卓）
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        groupset.wait_for_page_load()
        if not groupset.get_chat_set_to_top_switch_status():
            groupset.click_chat_set_to_top_switch()
        groupset.click_back()
        groupchat.click_back()
        # ContactListSearchPage().click_back()
        mess = MessagePage()
        mess.wait_for_page_load()
        # Step 1、在消息列表长按置顶成功的会话窗口，弹出的功能列表中是否存在展示为：取消置顶的功能
        mess.cancel_message_record_stick()
        Preconditions.enter_group_chat_page("给个红包2")
        # Step 2、点击取消置顶，取消置顶成功后，去到群聊设置页面，置顶聊天的开关是否已被关闭
        groupchat.click_setting()
        groupset.wait_for_page_load()
        # Checkpoint 置顶聊天的开关已被关闭
        self.assertFalse(groupset.get_chat_set_to_top_switch_status())

    @staticmethod
    def setUp_test_msg_xiaoqiu_0550():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        Preconditions.enter_group_chat_page("给个红包2")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0550(self):
        """普通群，点击口令弹窗的立即分享按钮，分享群口令"""
        # 1、网络正常
        # 2、已加入或创建普通群
        # 3、已消除红点
        # 4、群主、群成员
        # 5、仅限大陆本网和异网号码
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        groupset.wait_for_page_load()
        groupset.click_avetor_qq_wechat_friend()
        # 2、android点击下载再说或者空白处，弹窗是否会消失
        groupset.wait_for_share_group_load()
        groupset.click_say_next()
        # Checkpoint 弹窗消失并且返回到群聊设置页面
        groupset.wait_for_page_load()


