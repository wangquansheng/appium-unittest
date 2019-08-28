import time

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.contacts.components.menu_more import MenuMore
from pages.contacts.official_account import OfficialAccountPage
from pages.contacts.official_account_detail import OfficialAccountDetailPage
from pages.contacts.search_official_account import SearchOfficialAccountPage
from preconditions.BasePreconditions import LoginPreconditions, WorkbenchPreconditions

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    'Android-XX': ''  # 用来发短信
}


class Preconditions(WorkbenchPreconditions):
    """
    分解前置条件
    """
    @staticmethod
    def take_logout_operation_if_already_login():
        """已登录状态，执行登出操作"""
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.open_me_page()

        me = MePage()
        me.scroll_to_bottom()
        me.scroll_to_bottom()
        me.scroll_to_bottom()
        me.click_setting_menu()

        setting = SettingPage()
        setting.scroll_to_bottom()
        setting.click_logout()
        setting.click_ok_of_alert()

    @staticmethod
    def reset_and_relaunch_app():
        """首次启动APP（使用重置APP代替）"""
        app_package = 'com.chinasofti.rcs'
        current_driver().activate_app(app_package)
        current_mobile().reset_app()

    @staticmethod
    def terminate_app():
        """
        强制关闭app,退出后台
        :return:
        """
        app_id = current_driver().desired_capability['appPackage']
        current_mobile().termiate_app(app_id)

    @staticmethod
    def background_app():
        """后台运行"""
        current_mobile().press_home_key()

    @staticmethod
    def init_and_enter_contacts_page():
        """预置通讯录,保证开始用例之前在通讯录页面"""
        Preconditions.make_already_in_message_page()
        mess=MessagePage()
        mess.click_contacts()
        time.sleep(1)


class ContactPage(TestCase):
    """通讯录"""
    @classmethod
    def setUpClass(cls):
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        if mess.is_on_this_page():
            WorkbenchPreconditions.enter_create_team_page2()
        # 当前为消息页面
        # 确保存在子部门
        WorkbenchPreconditions.create_sub_department()
        # 导入测试联系人、群聊
        fail_time1 = 0
        flag1 = False
        import dataproviders
        while fail_time1 < 2:
            try:
                Preconditions.make_already_in_message_page()
                required_contacts = dataproviders.get_preset_contacts()
                conts = ContactsPage()
                conts.open_contacts_page()
                if conts.is_text_present("发现SIM卡联系人"):
                    conts.click_text("显示")
                for name, number in required_contacts:
                    # 创建联系人
                    conts.create_contacts_if_not_exits_new(name, number)
                required_group_chats = dataproviders.get_preset_group_chats()
                conts.open_group_chat_list()
                group_list = GroupListPage()
                for group_name, members in required_group_chats:
                    group_list.wait_for_page_load()
                    # 创建群
                    group_list.create_group_chats_if_not_exits(group_name, members)
                group_list.click_back()
                conts.open_message_page()
                flag1 = True
            except:
                fail_time1 += 1
            if flag1:
                break

    def default_setUp(self):
        """确保每个用例执行前在通讯录-手机联系人页面"""
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        MessagePage().wait_for_page_load()
        # 联系Tab
        MessagePage().click_contacts()
        time.sleep(1)
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        time.sleep(1)

    @tags('All', 'CMCC')
    def test_contacts_quxinli_0003(self):
        """用户已加入团队时联系页面"""
        contacts = ContactsPage()
        # 顶部入口
        contacts.page_should_contain_text('搜索')
        if contacts.is_text_present('备份你的手机通讯录，联系人数据不丢失'):
            contacts.page_should_contain_text('备份你的手机通讯录，联系人数据不丢失')
        time.sleep(2)
        contacts.page_should_contain_text('群聊')
        contacts.page_should_contain_text('公众号')
        contacts.page_should_contain_text('创建团队')
        contacts.page_should_contain_text('全部团队')
        time.sleep(1)
        # 进入手机联系人页面
        ContactsPage().click_mobile_contacts()
        # 右上角
        contacts.page_contain_element_add()
        # 显示所有联系人
        contacts.is_page_contain_element('联系人名')

    @staticmethod
    def setUp_test_contacts_quxinli_0005():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.reset_and_relaunch_app()
        Preconditions.make_already_in_one_key_login_page()
        Preconditions.login_by_one_key_login()
        MessagePage().wait_for_page_load()

    @tags('All', 'CMCC_RESET')
    def test_contacts_quxinli_0005(self):
        """用户未开启联系权限首次进入联系页面"""
        MessagePage().click_contacts_only()
        contact=ContactsPage()
        time.sleep(1)
        # 权限框点击禁止,不显示联系人
        contact.page_should_contain_text('“和飞信”将访问您的通讯录')
        contact.click_forbidden()
        contact.click_sim_contact()
        time.sleep(2)
        contact.is_page_contain_element('联系人名')
        # 点击允许,显示联系人
        contact.click_message_icon()
        time.sleep(2)
        MessagePage().click_contacts_only()
        contact.page_should_contain_text('“和飞信”将访问您的通讯录')
        contact.click_always_allowed()
        contact.click_sim_contact()
        time.sleep(1)
        contact.is_page_contain_element('联系人名')

    @staticmethod
    def setUp_test_contacts_quxinli_0006():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.reset_and_relaunch_app()
        Preconditions.make_already_in_one_key_login_page()
        Preconditions.login_by_one_key_login()
        MessagePage().wait_for_page_load()

    @tags('All', 'CMCC_RESET')
    def test_contacts_quxinli_0006(self):
        """用户未开启联系权限首次进入联系页面"""
        MessagePage().click_contacts_only()
        contact = ContactsPage()
        time.sleep(1)
        # 权限框点击允许,
        contact.page_should_contain_text('“和飞信”将访问您的通讯录')
        contact.click_always_allowed()
        time.sleep(2)
        contact.click_mobile_contacts()
        time.sleep(2)
        contact.is_page_contain_element('联系人名')

    @staticmethod
    def setUp_test_contacts_quxinli_0007():

        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.reset_and_relaunch_app()
        Preconditions.make_already_in_one_key_login_page()
        Preconditions.login_by_one_key_login()
        MessagePage().wait_for_page_load()

    @tags('All', 'CMCC_RESET')
    def test_contacts_quxinli_0007(self):
        """用户未开启联系权限首次进入联系页面"""
        MessagePage().click_contacts_only()
        contact = ContactsPage()
        time.sleep(2)
        contact.page_should_contain_text('“和飞信”将访问您的通讯录')
        self.assertEquals(contact.is_exist_allow_button(), True)
        self.assertEquals(contact.is_exist_forbidden_button(), True)
        contact.click_always_allowed()
        time.sleep(1)
        contact.page_should_contain_text('群聊')
        contact.page_should_contain_text('公众号')
        contact.is_page_contain_element('创建团队')

    @tags('All', 'CMCC')
    def test_contacts_quxinli_0019(self):
        """点击搜索结果已保存到本地的RCS用户进入Profile页"""
        ContactsPage().click_search_box()
        time.sleep(3)
        # 搜索联系人:测试号码1
        ContactListSearchPage().input_search_keyword('测试号码1')
        time.sleep(3)
        ContactListSearchPage().click_contact('测试号码1')
        time.sleep(3)
        # 进入个人详情页
        # 页面包含的元素
        detailpage = ContactDetailsPage()
        detailpage.is_exists_contacts_name()
        detailpage.is_exists_contacts_number()
        if detailpage.is_text_present("公司"):
            detailpage.page_should_contain_text('公司')
        if detailpage.is_text_present("职位"):
            detailpage.page_should_contain_text('职位')
        if detailpage.is_text_present("邮箱"):
            detailpage.page_should_contain_text('邮箱')
        detailpage.page_should_contain_text('消息')
        detailpage.page_should_contain_text('电话')
        detailpage.page_should_contain_text('语音通话')
        detailpage.page_should_contain_text('视频通话')
        detailpage.page_should_contain_text('飞信电话')
        detailpage.page_should_contain_text('分享名片')
        # 点击头像查看大图
        # detailpage.click_avatar()
        # time.sleep(4)
        # detailpage.click_big_avatar()
        # 消息按钮可点击
        detailpage.click_message_icon()  # 进入消息页面
        time.sleep(2)
        if ChatWindowPage().is_text_present("用户须知"):
            # 如果存在用户须知,就点击已阅读,然后点击返回.如果不存在,就直接点击返回
            ChatWindowPage().click_already_read()
            ChatWindowPage().click_sure_icon()
            ChatWindowPage().click_back_by_android()
        else:
            ChatWindowPage().click_back_by_android()
        # 点击电话/点击语音通话/点击视频通话先不做
        # 分享名片按钮可点击
        detailpage.click_share_business_card()
        SelectContactsPage().select_local_contacts()
        SelectContactsPage().click_one_contact('大佬1')
        # SelectContactsPage().click_cantact_avatar()
        time.sleep(2)
        SelectContactsPage().click_share_card()
        # 返回通讯录页面
        detailpage.click_back_icon()
        ContactListSearchPage().click_back()

    @tags('All', 'CMCC')
    def test_contacts_quxinli_0020(self):
        """点击搜索结果已保存到本地的非RCS用户进入Profile页"""
        ContactsPage().click_search_box()
        time.sleep(3)
        # 搜索联系人:大佬1
        ContactListSearchPage().input_search_keyword('大佬10')
        time.sleep(3)
        ContactListSearchPage().click_contact('大佬10')
        time.sleep(2)
        # 进入个人详情页  页面包含的元素
        detailpage = ContactDetailsPage()
        detailpage.is_exists_contacts_name()
        detailpage.is_exists_contacts_number()
        if detailpage.is_text_present("公司"):
            detailpage.page_should_contain_text('公司')
        if detailpage.is_text_present("职位"):
            detailpage.page_should_contain_text('职位')
        if detailpage.is_text_present("邮箱"):
            detailpage.page_should_contain_text('邮箱')
        detailpage.page_should_contain_text('消息')
        detailpage.page_should_contain_text('电话')
        detailpage.page_should_contain_text('语音通话')
        detailpage.page_should_contain_text('视频通话')
        detailpage.page_should_contain_text('飞信电话')
        detailpage.page_should_contain_text('分享名片')
        # detailpage.page_should_contain_text('邀请使用')
        time.sleep(2)
        # 点击头像可查看大图
        # detailpage.click_avatar()
        # time.sleep(2)
        # detailpage.click_big_avatar()
        # 消息按钮可点击  进入消息页面
        detailpage.click_message_icon()
        time.sleep(2)
        if ChatWindowPage().is_text_present("用户须知"):
            # 如果存在用户须知,就点击已阅读,然后点击返回.如果不存在,就直接点击返回
            ChatWindowPage().click_already_read()
            ChatWindowPage().click_sure_icon()
            ChatWindowPage().click_back_by_android()
        else:
            ChatWindowPage().click_back_by_android()
        # 点击电话/点击语音通话/点击视频通话先不做
        # 点击分享名片
        detailpage.click_share_business_card()
        SelectContactsPage().select_local_contacts()
        SelectContactsPage().click_one_contact('大佬10')
        # SelectContactsPage().click_cantact_avatar()
        time.sleep(2)
        SelectContactsPage().click_share_card()
        # 邀请使用按钮可点击
        # 返回通讯录页面
        detailpage.click_back_icon()
        ContactListSearchPage().click_back()

    @staticmethod
    def setUp_test_contacts_quxinli_0021():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        time.sleep(2)
        ContactsPage().click_search_box()
        time.sleep(2)
        ContactListSearchPage().input_search_keyword('本机')
        time.sleep(1)
        if ContactListSearchPage().is_contact_in_list('本机'):
            ContactListSearchPage().click_back_by_android()
        else:
            # 创建联系人 本机
            ContactListSearchPage().click_back_by_android()
            # 进入手机联系人页面
            ContactsPage().click_mobile_contacts()
            ContactsPage().click_add()
            creat_contact2 = CreateContactPage()
            creat_contact2.click_input_name()
            creat_contact2.input_name('本机')
            creat_contact2.click_input_number()
            phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)
            creat_contact2.input_number(phone_number[0])
            creat_contact2.save_contact()
            time.sleep(1)
            ContactDetailsPage().click_back_by_android(2)

    @tags('All', 'CMCC')
    def test_contacts_quxinli_0021(self):
        """点击搜索结果已保存到本地的本机用户进入Profile页"""
        ContactsPage().click_search_box()
        time.sleep(2)
        ContactListSearchPage().input_search_keyword('本机')
        time.sleep(2)
        ContactListSearchPage().click_contact('本机')
        time.sleep(2)
        # 进入个人详情页
        # 判断页面包含的元素
        detailpage = ContactDetailsPage()
        detailpage.is_exists_contacts_name()
        detailpage.is_exists_contacts_number()
        if detailpage.is_text_present("公司"):
            detailpage.page_should_contain_text('公司')
        if detailpage.is_text_present("职位"):
            detailpage.page_should_contain_text('职位')
        if detailpage.is_text_present("邮箱"):
            detailpage.page_should_contain_text('邮箱')
        detailpage.page_should_contain_text('消息')
        detailpage.page_should_contain_text('电话')
        detailpage.page_should_contain_text('语音通话')
        detailpage.page_should_contain_text('视频通话')
        detailpage.page_should_contain_text('飞信电话')
        # 点击分享名片进入选择联系人页面，可以成功的分享给人/群
        detailpage.click_share_business_card()
        SelectContactsPage().select_local_contacts()
        SelectContactsPage().click_one_contact('大佬1')
        time.sleep(2)
        SelectContactsPage().click_share_card()
        # 消息、电话、语音视频、视频电话、副号拨打、和飞信电话置灰，不可点击
        time.sleep(2)
        detailpage.message_btn_is_clickable()
        detailpage.call_btn_is_clickable()
        detailpage.voice_btn_is_clickable()
        detailpage.video_call_btn_is_clickable()
        detailpage.hefeixin_call_btn_is_clickable()
        time.sleep(2)
        # 返回通讯录页面
        detailpage.click_back_icon()
        ContactListSearchPage().click_back()

    @staticmethod
    def setUp_test_contacts_quxinli_0065():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        time.sleep(2)
        ContactsPage().click_search_box()
        time.sleep(2)
        ContactListSearchPage().input_search_keyword('本机')
        time.sleep(1)
        if ContactListSearchPage().is_contact_in_list('本机'):
            ContactListSearchPage().click_back_by_android()
        else:
            # 创建联系人 本机
            ContactListSearchPage().click_back_by_android()
            # 进入手机联系人页面
            ContactsPage().click_mobile_contacts()
            ContactsPage().click_add()
            creat_contact2 = CreateContactPage()
            creat_contact2.click_input_name()
            creat_contact2.input_name('本机')
            creat_contact2.click_input_number()
            phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)
            creat_contact2.input_number(phone_number[0])
            creat_contact2.save_contact()
            time.sleep(1)
            ContactDetailsPage().click_back_by_android(2)

    @tags('All', 'CMCC')
    def test_contacts_quxinli_0065(self):
        """点击搜索结果已保存到本地的本机用户进入Profile页"""
        ContactsPage().click_search_box()
        time.sleep(2)
        # 搜索联系人:本机
        ContactListSearchPage().input_search_keyword('本机')
        time.sleep(2)
        ContactListSearchPage().click_contact('本机')
        time.sleep(2)
        # 进入个人详情页
        # 判断页面包含的元素
        detailpage = ContactDetailsPage()
        detailpage.is_exists_contacts_name()
        detailpage.is_exists_contacts_number()
        if detailpage.is_text_present("公司"):
            detailpage.page_should_contain_text('公司')
        if detailpage.is_text_present("职位"):
            detailpage.page_should_contain_text('职位')
        if detailpage.is_text_present("邮箱"):
            detailpage.page_should_contain_text('邮箱')
        detailpage.page_should_contain_text('消息')
        detailpage.page_should_contain_text('电话')
        detailpage.page_should_contain_text('语音通话')
        detailpage.page_should_contain_text('视频通话')
        detailpage.page_should_contain_text('飞信电话')
        detailpage.page_should_contain_text('分享名片')
        # 点击分享名片进入选择联系人页面，可以成功的分享给人/群
        detailpage.click_share_business_card()
        SelectContactsPage().select_local_contacts()
        SelectContactsPage().click_one_contact('大佬1')
        time.sleep(2)
        SelectContactsPage().click_share_card()
        # 消息、电话、语音视频、视频电话、副号拨打、和飞信电话置灰，不可点击
        time.sleep(2)
        detailpage.message_btn_is_clickable()
        detailpage.call_btn_is_clickable()
        detailpage.voice_btn_is_clickable()
        detailpage.video_call_btn_is_clickable()
        detailpage.hefeixin_call_btn_is_clickable()
        time.sleep(2)
        # 返回通讯录页面
        detailpage.click_back_by_android(2)

    @staticmethod
    def setUp_test_contacts_quxinli_0196():
        # 进入通讯录页面
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_search_box()
        time.sleep(3)
        clp = ContactListSearchPage()
        clp.input_search_keyword('大佬1')
        clp.hide_keyboard()
        time.sleep(1)
        clp.click_contact('大佬1')
        time.sleep(2)

    @tags('All', 'CMCC')
    def test_contacts_quxinli_0196(self):
        """在联系人选择器页面，选择一个群"""
        ContactListSearchPage().click_share_card()
        scp = SelectContactsPage()
        scp.click_select_one_group()
        # 搜索框文本显示'搜索群组'
        scp.is_text_present('搜索群组')
        # 不存在搜索结果时,显示"无搜索结果
        scp.click_group_search()
        scp.hide_keyboard()
        time.sleep(1)
        scp.group_search('wanduzi')
        time.sleep(3)
        SelectOneGroupPage().page_should_contain_text('无搜索结果')
        # 存在搜索结果时,搜索结果包含关键字
        time.sleep(2)
        scp.click_back_by_android()
        scp.click_group_search()
        time.sleep(3)
        scp.group_search('群聊1')
        time.sleep(3)
        scp.select_one_group_by_name2('群聊1')
        time.sleep(2)
        scp.click_share_card()
        scp.click_back_by_android(times=5)

    @staticmethod
    def setUp_test_contacts_quxinli_0197():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_search_box()
        time.sleep(3)
        clp = ContactListSearchPage()
        clp.input_search_keyword('大佬1')
        clp.hide_keyboard()
        time.sleep(1)
        clp.click_contact('大佬1')
        time.sleep(2)

    @tags('All', 'CMCC')
    def test_contacts_quxinli_0197(self):
        """在联系人选择器页面，选择一个群"""
        ContactListSearchPage().click_share_card()
        SelectContactsPage().click_select_one_group()
        SelectOneGroupPage().selecting_one_group_by_name('群聊1')
        time.sleep(1)
        SelectOneGroupPage().is_text_present('发送名片')
        SelectOneGroupPage().click_share_business_card()
        time.sleep(1)
        # 返回通讯录页面
        ContactDetailsPage().click_back_by_android(2)

    @staticmethod
    def setUp_test_contacts_quxinli_0198():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_search_box()
        time.sleep(3)
        clp = ContactListSearchPage()
        clp.input_search_keyword('大佬1')
        clp.hide_keyboard()
        time.sleep(1)
        clp.click_contact('大佬1')
        time.sleep(2)
        ContactDetailsPage().click_share_business_card()
        time.sleep(2)

    @tags('All', 'CMCC')
    def test_contacts_quxinli_0198(self):
        """在联系人选择器页面，选择本地联系人"""
        SelectContactsPage().select_local_contacts()
        SelectContactsPage().page_should_contain_text('选择联系人')
        SelectContactsPage().page_should_contain_text('搜索或输入手机号')
        # 无搜索结果时,下方是否展示：无搜索结果
        SelectContactsPage().click_search_keyword()
        time.sleep(3)
        SelectContactsPage().input_search_keyword('wanduzi')
        SelectContactsPage().is_text_present('无搜索结果')
        time.sleep(2)
        # 存在搜索结果时,判断显示是否正确
        SelectContactsPage().click_x_icon()
        time.sleep(1)
        SelectContactsPage().input_search_keyword('大佬2')
        time.sleep(2)
        SelectContactsPage().select_one_contact_by_name('大佬2')
        time.sleep(2)
        SelectContactsPage().click_share_card()
        # 返回通讯录页面
        ContactDetailsPage().click_back_by_android(2)

    @staticmethod
    def setUp_test_contacts_quxinli_0199():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_search_box()
        time.sleep(3)
        clp = ContactListSearchPage()
        clp.input_search_keyword('大佬1')
        clp.hide_keyboard()
        time.sleep(1)
        clp.click_contact('大佬1')
        time.sleep(2)

    @tags('All', 'CMCC')
    def test_contacts_quxinli_0199(self):
        """在联系人选择器页面，选择本地联系人"""
        ContactDetailsPage().click_share_business_card()
        time.sleep(2)
        select_contact = SelectContactsPage()
        select_contact.select_local_contacts()
        select_contact.click_one_contact('大佬2')
        time.sleep(2)
        select_contact.page_should_contain_text('发送名片')
        SelectOneGroupPage().click_share_business_card()
        SelectOneGroupPage().click_back_by_android(times=5)

    @staticmethod
    def setUp_test_contacts_quxinli_0208():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_search_box()
        time.sleep(3)
        clp = ContactListSearchPage()
        clp.input_search_keyword('大佬1')
        clp.hide_keyboard()
        time.sleep(1)
        clp.click_contact('大佬1')
        time.sleep(2)
        ContactDetailsPage().click_share_business_card()

    @tags('All', 'CMCC')
    def test_contacts_quxinli_0208(self):
        """在联系人选择器页面，搜索联系人"""
        select_contacts = SelectContactsPage()
        # 输入'测试'进行搜索,搜索结果显示情况
        select_contacts.click_search_keyword()
        select_contacts.input_search_keyword('给个红包')
        select_contacts.hide_keyboard()
        time.sleep(2)
        select_contacts.page_should_contain_text('搜索团队联系人')
        select_contacts.page_should_contain_text('手机联系人')
        select_contacts.page_should_contain_text('查看更多')
        select_contacts.page_should_contain_text('群聊')
        # 选择本地联系人是否会弹出弹框 #是否弹出弹框未检测
        select_contacts.click_one_contact('给个红包1')
        select_contacts.is_text_present('发送名片')
        select_contacts.click_share_card()
        # 选择群联系人是否会出现弹框  是否弹出弹框未检测
        ContactDetailsPage().click_share_business_card()
        time.sleep(1)
        select_contacts.click_search_keyword()
        select_contacts.input_search_keyword('给个红包1')
        select_contacts.hide_keyboard()
        time.sleep(3)
        select_contacts.select_one_group_by_name('给个红包1')
        select_contacts.is_text_present('发送名片')
        time.sleep(1)
        select_contacts.click_share_card()
        time.sleep(2)
        # 点击查看按钮,是否会展示折叠的搜索结果
        ContactDetailsPage().click_share_business_card()
        time.sleep(1)
        select_contacts.click_search_keyword()
        time.sleep(2)
        select_contacts.input_search_keyword('给个红包')
        time.sleep(3)
        select_contacts.click_read_more()
        time.sleep(2)
        select_contacts.page_should_contain_text('给个红包4')
        select_contacts.click_one_contact('给个红包4')
        select_contacts.click_share_card()
        # 返回通讯录页面
        ContactDetailsPage().click_back_by_android(3)

    @staticmethod
    def setUp_test_contacts_quxinli_0209():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_search_box()
        time.sleep(3)
        clp = ContactListSearchPage()
        clp.input_search_keyword('大佬1')
        clp.hide_keyboard()
        time.sleep(1)
        clp.click_contact('大佬1')
        time.sleep(2)
        ContactListSearchPage().click_share_card()

    @tags('All', 'CMCC')
    def test_contacts_quxinli_0209(self):
        """在联系人选择器页面，选择最近聊天联系人"""
        select_contacts = SelectContactsPage()
        select_contacts.select_one_recently_contact_by_name('大佬2')
        time.sleep(1)
        select_contacts.page_should_contain_text('发送名片')
        select_contacts.click_share_card()
        # 返回通讯录页面
        ContactDetailsPage().click_back_by_android(3)

    @staticmethod
    def setUp_test_contacts_quxinli_0210():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_search_box()
        time.sleep(3)
        clp = ContactListSearchPage()
        clp.input_search_keyword('大佬1')
        clp.hide_keyboard()
        time.sleep(1)
        clp.click_contact('大佬1')
        time.sleep(2)
        ContactListSearchPage().click_share_card()

    @tags('All', 'CMCC')
    def test_contacts_quxinli_0210(self):
        """在联系人选择器页面，选择最近聊天群聊"""
        select_contacts = SelectContactsPage()
        time.sleep(1)
        select_contacts.click_select_one_group()
        time.sleep(2)
        SelectOneGroupPage().click_one_contact("给个红包1")
        time.sleep(1)
        select_contacts.page_should_contain_text('发送名片')
        select_contacts.click_share_card()
        # 返回通讯录页面
        time.sleep(1)
        ContactDetailsPage().click_back_by_android(3)

    @staticmethod
    def setUp_test_contacts_quxinli_0211():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_search_box()
        time.sleep(3)
        clp = ContactListSearchPage()
        clp.input_search_keyword('大佬1')
        clp.hide_keyboard()
        time.sleep(1)
        clp.click_contact('大佬1')
        time.sleep(2)
        ContactListSearchPage().click_share_card()

    @tags('ALL','CMCC')
    def test_contacts_quxinli_0211(self):
        """在联系人选择器页面，搜索我的电脑"""
        time.sleep(1)
        SelectContactsPage().click_search_contact()
        SelectContactsPage().input_search_keyword('我的电脑')
        SelectContactsPage().hide_keyboard()
        time.sleep(2)
        # 返回通讯录页面
        SelectContactsPage().click_back_by_android(4)

    @staticmethod
    def setUp_test_contacts_quxinli_0212():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.init_and_enter_contacts_page()
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_always_allowed()
        ContactsPage().click_search_box()
        time.sleep(3)
        clp = ContactListSearchPage()
        clp.input_search_keyword('大佬1')
        clp.hide_keyboard()
        time.sleep(1)
        clp.click_contact('大佬1')
        time.sleep(2)
        ContactListSearchPage().click_share_card()

    @tags('ALL', 'CMCC')
    def test_contacts_quxinli_0212(self):
        """在联系人选择器页面，搜索11位陌生号码"""
        time.sleep(1)
        select_contact=SelectContactsPage()
        select_contact.click_search_contact()
        select_contact.input_search_keyword('15575256658')
        select_contact.hide_keyboard()
        time.sleep(2)
        select_contact.get_element_text_net_name('未知号码')
        select_contact.get_element_text_net_number('tel:+86')
        time.sleep(2)
        # 返回消息页面
        SelectContactsPage().click_back_by_android(4)

    @tags('ALL', 'CMCC')
    def test_contacts_quxinli_0322(self):
        """订阅号/服务号列表显示"""
        ContactsPage().click_official_account_icon()
        time.sleep(3)
        official_account = OfficialAccountPage()
        official_account.page_should_contain_text('中国移动10086')
        official_account.page_should_contain_text('和飞信')
        official_account.page_should_contain_text('和飞信团队')
        official_account.page_should_contain_text('和飞信新闻')
        # 返回通讯录页面
        official_account.click_back()

    @tags('ALL', 'CMCC')
    def test_contacts_quxinli_0323(self):
        """企业号列表显示为空"""
        ContactsPage().click_official_account_icon()
        official_account = OfficialAccountPage()
        official_account.click_tag("企业号")
        time.sleep(1)
        official_account.page_should_contain_text('未关注任何企业号')
        official_account.assert_enterprise_account_list_is_empty()
        #返回通讯录页面
        official_account.click_back()

    @tags('ALL', 'CMCC')
    def test_contacts_quxinli_0324(self):
        """公众号会话页面-未配置底部菜单栏的公众号"""
        ContactsPage().click_official_account_icon()
        time.sleep(1)
        OfficialAccountPage().select_one_account_by_name('和飞信新闻')
        # 公众号详情页(未配置底部菜单栏)
        official_account = OfficialAccountPage()
        time.sleep(2)
        official_account.page_should_contain_text('和飞信新闻')
        official_account.page_contain_setting()
        official_account.page_contain_input_box()
        # official_account.page_contain_expresssion()
        official_account.page_contain_send_button()
        official_account.send_btn_is_clickable()
        # 返回通讯录页面
        official_account.click_back()
        OfficialAccountPage().click_back()

    @tags('ALL', 'CMCC')
    def test_contacts_quxinli_0325(self):
        """公众号会话页面-已配置底部菜单栏的公众号"""
        ContactsPage().click_official_account_icon()
        time.sleep(1)
        OfficialAccountPage().select_one_account_by_name('和飞信')
        # 判断页面包含的元素
        official_account = OfficialAccountPage()
        time.sleep(2)
        official_account.page_should_contain_text('和飞信')
        official_account.page_contain_setting()
        official_account.page_contain_keyboard()
        official_account.page_should_contain_element_menu()
        # 点击底部菜单,可以进入到菜单详情页
        official_account.click_menu_name2()
        time.sleep(1)
        official_account.page_should_contain_text('多方电话')
        official_account.click_menu_detail_name1()
        time.sleep(4)
        official_account.click_menu_detail_back()
        # 点击键盘标志,页面显示输入框等
        official_account.click_keyboard()
        official_account.page_contain_input_box()
        # official_account.page_contain_expresssion()
        official_account.page_contain_send_button()
        official_account.send_btn_is_clickable()
        time.sleep(2)
        # 再次点击键盘,又展示底部菜单
        official_account.click_keyboard()
        official_account.page_should_contain_element_menu()
        time.sleep(2)
        # 返回消息页面
        official_account.click_back()
        OfficialAccountPage().click_back()
        ContactsPage().click_message_icon()

    @tags('ALL', 'CMCC')
    def test_contacts_quxinli_0326(self):
        ContactsPage().click_official_account_icon()
        time.sleep(1)
        OfficialAccountPage().select_one_account_by_name('和飞信新闻')
        """公众号会话页面发送文本消息"""
        official_account = OfficialAccountPage()
        official_account.click_input_box()
        official_account.input_message('和飞信')
        official_account.click_send_button()
        time.sleep(2)
        official_account.page_should_contain_text('和飞信')
        # 返回消息页面
        official_account.click_back()
        OfficialAccountPage().click_back()
        ContactsPage().click_message_icon()

    @tags('ALL', 'CMCC')
    def test_contacts_quxinli_0327(self):
        """公众号会话页面发送表情消息"""
        ContactsPage().click_official_account_icon()
        time.sleep(1)
        OfficialAccountPage().select_one_account_by_name('和飞信新闻')
        official_account = OfficialAccountPage()
        # 备注:新版本无表情
        # official_account.click_expression()
        # official_account.click_expression_detail()
        # official_account.click_send_button()
        time.sleep(2)
        # 返回通讯录页面
        official_account.click_back()
        OfficialAccountPage().click_back()

    @tags('ALL', 'CMCC')
    def test_contacts_quxinli_0328(self):
        """公众号会话页面，发送表情+信息"""
        ContactsPage().click_official_account_icon()
        time.sleep(1)
        OfficialAccountPage().select_one_account_by_name('和飞信新闻')
        official_account = OfficialAccountPage()
        official_account.click_input_box()
        official_account.input_message('和飞信')
        # 备注:新版本无表情
        # official_account.click_expression()
        # official_account.click_expression_detail()
        official_account.click_send_button()
        time.sleep(2)
        # 返回通讯录页面
        official_account.click_back()
        OfficialAccountPage().click_back()

    @tags('ALL', 'CMCC')
    def test_contacts_quxinli_0329(self):
        """公众号会话页面，发送长信息"""
        ContactsPage().click_official_account_icon()
        time.sleep(1)
        OfficialAccountPage().select_one_account_by_name('和飞信新闻')
        official_account = OfficialAccountPage()
        official_account.click_input_box()
        keyword=str("我"*255)
        official_account.input_message([keyword])
        official_account.click_send_button()
        time.sleep(2)
        # 返回通讯录页面
        official_account.click_back()
        OfficialAccountPage().click_back()

    @tags('ALL', 'CMCC')
    def test_contacts_quxinli_0330(self):
        """公众号会话页面发送链接消息"""
        ContactsPage().click_official_account_icon()
        time.sleep(1)
        OfficialAccountPage().select_one_account_by_name('和飞信新闻')
        official_account = OfficialAccountPage()
        official_account.click_input_box()
        keyword="https://www.baidu.com/"
        official_account.input_message(keyword)
        official_account.click_send_button()
        time.sleep(1)
        official_account.click_send_detail(keyword)
        time.sleep(2)
        # 返回通讯录页面
        official_account.click_back_by_android(3)

    @tags('ALL', 'CMCC')
    def test_contacts_quxinli_0331(self):
        """公众号会话页面网络异常情况下发送消息"""
        ContactsPage().click_official_account_icon()
        time.sleep(1)
        OfficialAccountPage().select_one_account_by_name('和飞信新闻')
        official_account = OfficialAccountPage()
        # 断网
        official_account.set_network_status(0)
        official_account.click_input_box()
        official_account.input_message('和飞信')
        official_account.click_send_button()
        time.sleep(2)
        official_account.page_should_contain_element_unsent()
        # 回复网络 发送成功
        official_account.set_network_status(6)
        time.sleep(3)
        official_account.click_element_unsent()
        official_account.click_sure_resent()
        time.sleep(2)
        official_account.page_not_contain_element_unsent()
        # 返回通讯录页面
        official_account.click_back_by_android(2)

    @staticmethod
    def tearDown_test_contacts_quxinli_0331():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep = MePage()
            mep.set_network_status(6)

    @tags('ALL', 'CMCC')
    def test_contacts_quxinli_0332(self):
        """公众号会话页面右上角设置按钮"""
        ContactsPage().click_official_account_icon()
        time.sleep(1)
        OfficialAccountPage().select_one_account_by_name('和飞信')
        OfficialAccountPage().click_setting()
        time.sleep(2)
        official_account_detail = OfficialAccountDetailPage()
        official_account_detail.page_contain_public_title_name()
        official_account_detail.page_contain_public_name()
        official_account_detail.page_contain_public_header()
        official_account_detail.page_contain_public_number()
        official_account_detail.page_contain_features()
        official_account_detail.page_contain_certification()
        official_account_detail.page_should_contain_text('置顶公众号')
        official_account_detail.page_should_contain_text('查看历史资讯')
        official_account_detail.page_should_contain_text('进入公众号')
        # 返回通讯录页面
        official_account_detail.click_back_by_android(3)

    @tags('ALL', 'CMCC')
    def test_contacts_quxinli_0335(self):
        """公众号详情-查看历史资讯"""
        ContactsPage().click_official_account_icon()
        official = OfficialAccountPage()
        official.click_officel_account()
        time.sleep(1)
        official.click_setting_button()
        official_detail = OfficialAccountDetailPage()

        official_detail.click_read_old_message()
        official_detail.wait_for_page_load()
        if official_detail.is_contain_old_mes():
            official_detail.page_contain_time()
        else:
            official_detail.page_should_contain_text('无历史推送资讯')

    @tags('ALL', 'CMCC')
    def test_contacts_quxinli_0336(self):
        """公众号详情-进入公众号"""
        ContactsPage().click_official_account_icon()
        time.sleep(1)
        OfficialAccountPage().select_one_account_by_name('和飞信新闻')
        OfficialAccountPage().click_setting()
        time.sleep(2)
        OfficialAccountDetailPage().click_into_public()
        time.sleep(1)
        OfficialAccountPage().page_contain_setting()
        # 返回通讯录页面
        OfficialAccountPage().click_back_by_android(3)

    @tags('ALL', 'CMCC')
    def test_contacts_quxinli_0337(self):
        """公众号详情-进入公众号-更多"""
        ContactsPage().click_official_account_icon()
        time.sleep(1)
        OfficialAccountPage().select_one_account_by_name('和飞信')
        time.sleep(2)
        if OfficialAccountPage().is_element_present_message():
            OfficialAccountPage().click_setting()
        else:
            OfficialAccountPage().click_keyboard()
            OfficialAccountPage().click_input_box()
            OfficialAccountPage().input_message('测试数据')
            OfficialAccountPage().click_send_button()
            time.sleep(2)
            OfficialAccountPage().click_setting()
        time.sleep(2)
        official_account_detail = OfficialAccountDetailPage()
        official_account_detail.click_menu_more()
        time.sleep(1)
        # 点击清空消息--取消
        menu_more=MenuMore()
        menu_more.click_clean_msg_menu()
        menu_more.click_not_clear()
        official_account_detail.click_back()
        time.sleep(2)
        OfficialAccountPage().page_contain_element_message()
        # 点击清空消息--确定
        OfficialAccountPage().click_setting()
        time.sleep(1)
        official_account_detail.click_menu_more()
        menu_more.click_clean_msg_menu()
        menu_more.click_sure_clear()
        official_account_detail.click_back()
        OfficialAccountPage().page_not_contain_element_message()
        # 点击取消关注
        OfficialAccountPage().click_setting()
        time.sleep(1)
        official_account_detail.click_menu_more()
        # 备注：没有取消关注选项
        # menu_more.click_unsubscribe_menu()
        # time.sleep(2)
        # OfficialAccountPage().is_public_in_list('和飞信')
        # 返回通讯录页面
        OfficialAccountPage().click_back_by_android(4)

    @tags('ALL', 'CMCC')
    def test_contacts_quxinli_0338(self):
        """公众号列表-右上角的+"""
        ContactsPage().click_official_account_icon()
        time.sleep(1)
        OfficialAccountPage().click_add()
        time.sleep(2)
        SearchOfficialAccountPage().page_should_contain_text('搜索公众号')
        # 返回通讯录页面
        SearchOfficialAccountPage().click_back()
        OfficialAccountPage().click_back()

    @tags('ALL', 'CMCC')
    def test_contacts_quxinli_0346(self):
        """公众号详情-清空消息"""
        ContactsPage().click_official_account_icon()
        time.sleep(2)
        OfficialAccountPage().select_one_account_by_name('中国移动10086')
        time.sleep(2)
        if OfficialAccountPage().is_element_present_message():
            OfficialAccountPage().click_setting()
        else:
            OfficialAccountPage().click_keyboard()
            OfficialAccountPage().click_input_box()
            OfficialAccountPage().input_message('测试数据')
            OfficialAccountPage().click_send_button()
            time.sleep(2)
            OfficialAccountPage().click_setting()
        time.sleep(2)
        official_account_detail = OfficialAccountDetailPage()
        official_account_detail.click_menu_more()
        time.sleep(1)
        MenuMore().click_clean_msg_menu()
        MenuMore().click_sure_clear()
        official_account_detail.click_back()
        OfficialAccountPage().page_not_contain_element_message()
        # 返回消息页面
        OfficialAccountPage().click_back_by_android(2)

    @tags('All', 'CMCC')
    def test_contacts_quxinli_0023(self):
        """点击搜索结果已保存到本地的非RCS用户进入Profile页"""
        ContactsPage().click_search_box()
        time.sleep(2)
        # 搜索联系人:大佬1
        ContactListSearchPage().input_search_keyword('大佬10')
        time.sleep(2)
        ContactListSearchPage().click_contact('大佬10')
        time.sleep(2)
        # 进入个人详情页
        # 页面包含的元素
        detailpage = ContactDetailsPage()
        detailpage.is_exists_contacts_name()
        detailpage.is_exists_contacts_number()
        if detailpage.is_text_present("公司"):
            detailpage.page_should_contain_text('公司')
        if detailpage.is_text_present("职位"):
            detailpage.page_should_contain_text('职位')
        if detailpage.is_text_present("邮箱"):
            detailpage.page_should_contain_text('邮箱')
        detailpage.page_should_contain_text('消息')
        detailpage.page_should_contain_text('电话')
        detailpage.page_should_contain_text('语音通话')
        detailpage.page_should_contain_text('视频通话')
        detailpage.page_should_contain_text('飞信电话')
        time.sleep(2)
        # 点击头像可查看大图
        # detailpage.click_avatar()
        # time.sleep(2)
        # detailpage.click_big_avatar()
        # 消息按钮可点击 进入消息页面
        detailpage.click_message_icon()
        time.sleep(2)
        if ChatWindowPage().is_text_present("用户须知"):
            # 如果存在用户须知,就点击已阅读,然后点击返回.如果不存在,就直接点击返回
            ChatWindowPage().click_already_read()
            ChatWindowPage().click_sure_icon()
            ChatWindowPage().click_back_by_android()
        else:
            ChatWindowPage().click_back_by_android()
        # 返回通讯录页面
        detailpage.click_back_by_android(2)










