import time
import unittest

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.contacts.ContactDetails import ContactDetailsPage
from preconditions.BasePreconditions import LoginPreconditions

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
}


class Preconditions(LoginPreconditions):
    """
    分解前置条件
    """

    @staticmethod
    def connect_mobile(category):
        """选择手机手机"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.connect_mobile()
        return client

    @staticmethod
    def make_already_in_one_key_login_page():
        """
        1、已经进入一键登录页
        :return:
        """
        # 如果当前页面已经是一键登录页，不做任何操作
        one_key = OneKeyLoginPage()
        if one_key.is_on_this_page():
            return

        # 如果当前页不是引导页第一页，重新启动app
        guide_page = GuidePage()
        if not guide_page.is_on_the_first_guide_page():
            current_mobile().launch_app()
            guide_page.wait_for_page_load(20)

        # 跳过引导页
        guide_page.wait_for_page_load(30)
        guide_page.swipe_to_the_second_banner()
        guide_page.swipe_to_the_third_banner()
        guide_page.click_start_the_experience()

        # 点击权限列表页面的确定按钮
        permission_list = PermissionListPage()
        # permission_list.click_submit_button()
        permission_list.go_permission()
        one_key.wait_for_page_load(30)

    @staticmethod
    def login_by_one_key_login():
        """
        从一键登录页面登录
        :return:
        """
        # 等待号码加载完成后，点击一键登录
        one_key = OneKeyLoginPage()
        one_key.wait_for_tell_number_load(60)
        login_number = one_key.get_login_number()
        one_key.click_one_key_login()
        # one_key.click_read_agreement_detail()
        #
        # # 同意协议
        # agreement = AgreementDetailPage()
        # agreement.click_agree_button()
        agreement = AgreementDetailPage()
        time.sleep(1)
        agreement.click_agree_button()

        # 等待消息页
        message_page = MessagePage()
        message_page.wait_login_success(60)
        return login_number

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
    def create_contacts_if_not_exits(name, number):
        """
        导入联系人数据
        :param name:
        :param number:
        :return:
        """
        contacts_page = ContactsPage()
        detail_page = ContactDetailsPage()
        try:
            contacts_page.wait_for_page_load()
            contacts_page.open_contacts_page()
        except:
            Preconditions.make_already_in_message_page(reset_required=False)
            contacts_page.open_contacts_page()
        # 创建联系人
        contacts_page.click_search_box()
        contact_search = ContactListSearchPage()
        contact_search.wait_for_page_load()
        contact_search.input_search_keyword(name)
        if contact_search.is_contact_in_list(name):
            contact_search.click_back()
        else:
            contact_search.click_back()
            contacts_page.click_add()
            create_page = CreateContactPage()
            create_page.hide_keyboard_if_display()
            create_page.create_contact(name, number)
            detail_page.wait_for_page_load()
            detail_page.click_back_icon()

    @staticmethod
    def create_contacts(name, number):
        """
        导入联系人数据
        :param name:
        :param number:
        :return:
        """
        contacts_page = ContactsPage()
        detail_page = ContactDetailsPage()
        try:
            contacts_page.wait_for_page_load()
            contacts_page.open_contacts_page()
        except:
            Preconditions.make_already_in_message_page(reset_required=False)
            contacts_page.open_contacts_page()
        # 创建联系人
        contacts_page.click_search_box()
        contact_search = ContactListSearchPage()
        contact_search.wait_for_page_load()
        contact_search.input_search_keyword(name)
        contact_search.click_back()
        contacts_page.click_add()
        create_page = CreateContactPage()
        create_page.hide_keyboard_if_display()
        create_page.create_contact(name, number)
        detail_page.wait_for_page_load()
        detail_page.click_back_icon()

    @staticmethod
    def enter_label_grouping_chat_page(reset=False):
        """进入标签分组会话页面"""
        # 登录进入消息页面
        Preconditions.make_already_in_message_page(reset)
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        time.sleep(1)
        contacts.click_mobile_contacts()
        contacts.click_label_grouping()


class TagsGroupingTest(TestCase):
    """通讯录 - 标签分组"""
    # @classmethod
    # def setUpClass(cls):
    #     Preconditions.connect_mobile('Android-移动')
    #     current_mobile().hide_keyboard_if_display()
    #     Preconditions.make_already_in_message_page()
    #     # 导入测试联系人
    #     fail_time1 = 0
    #     flag1 = False
    #     import dataproviders
    #     while fail_time1 < 3:
    #         try:
    #             required_contacts = dataproviders.get_preset_contacts()
    #             conts = ContactsPage()
    #             conts.open_contacts_page()
    #             try:
    #                 if conts.is_text_present("发现SIM卡联系人"):
    #                     conts.click_text("显示")
    #             except:
    #                 pass
    #             for name, number in required_contacts:
    #                 # 创建联系人
    #                 conts.create_contacts_if_not_exits(name, number)
    #         except:
    #             fail_time1 += 1
    #             import traceback
    #             msg = traceback.format_exc()
    #             print(msg)

    def default_setUp(self):
        Preconditions.connect_mobile('Android-移动')
        Preconditions.enter_label_grouping_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_Conts_TagsGrouping_0002(self):
        """多个分组"""
        groups = [
            ['分组1'],
            ['分组2'],
            ['分组3'],
            ['分组4'],
            ['分组5'],
            ['分组6'],
            ['分组7'],
            ['分组8'],
            ['分组9'],
            ['分组10'],
            ['分组11'],
        ]
        conts_page = ContactsPage()
        lg = LabelGroupingPage()
        lg.wait_for_page_load()
        for g in groups:
            lg.create_a_group(*g)
        lg.wait_for_page_load()
        lg.delete_all_label()
        lg.wait_for_page_load()
        lg.click_back_by_android(2)
        conts_page.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_contacts_quxinli_0352(self):
        """无分组"""
        conts_page = ContactsPage()
        lg = LabelGroupingPage()
        lg.wait_for_page_load()
        lg.delete_all_label()
        lg.assert_default_status_is_right()
        lg.wait_for_page_load()
        lg.click_back_by_android(2)
        conts_page.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_contacts_quxinli_0353(self):
        """新建分组"""
        conts_page = ContactsPage()
        lg = LabelGroupingPage()
        lg.wait_for_page_load()
        lg.click_new_create_group()
        time.sleep(2)
        GroupListPage().new_group(name='给个红包1')
        lg.wait_for_page_load()
        lg.delete_all_label()
        lg.wait_for_page_load()
        lg.click_back_by_android(2)
        conts_page.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_contacts_quxinli_0372(self):
        """联系人选择器页面"""
        glp = GroupListPage()
        time.sleep(1)
        glp.delete_group(name='aaa')
        glp.new_group()
        glp.click_text('aaa')
        time.sleep(1)
        glp.click_text('添加成员')
        time.sleep(2)
        glp.page_should_contain_text('搜索或输入号码')
        glp.page_should_contain_text('选择联系人')
        glp.page_should_contain_text('确定')
        glp.page_should_contain_text('选择团队联系人')

        glp = GroupListPage()
        glp.click_back_button(times=2)
        glp.delete_group(name='aaa')

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_contacts_quxinli_0390(self):
        """群发信息"""
        glp = GroupListPage()
        time.sleep(1)
        glp.delete_group(name='aaa')
        glp.new_group(name='aaa')
        # 添加小组成员
        glp.click_text('aaa')
        time.sleep(1)
        LabelGroupingChatPage().click_text('添加成员')
        slcp = SelectLocalContactsPage()
        time.sleep(2)
        slcp.swipe_select_one_member_by_name('大佬1')
        slcp.click_sure()
        time.sleep(2)
        # 发送长文本消息
        message = 'aa aa' * 20
        glp.send_message_to_group(message)
        time.sleep(5)
        glp.page_contain_element('已转短信送达')
        # 发送纯文本
        glp.click_back_button()
        time.sleep(1)
        message = 'aaaa'
        glp.send_message_to_group(message)
        time.sleep(5)
        glp.page_contain_element('已转短信送达')
        # 发送文本 空格
        glp.click_back_button()
        time.sleep(1)
        message = 'aa aa'
        glp.send_message_to_group(message)
        time.sleep(5)
        glp.page_contain_element('已转短信送达')
        # 发送表情
        glp.click_back_button()
        time.sleep(1)
        glp.send_express_to_group()
        time.sleep(1)
        glp.page_not_contain_element('发送失败')
        # 发送图片
        glp.click_back_button()
        time.sleep(1)
        glp.send_picture_to_group()
        time.sleep(1)
        glp.page_not_contain_element('发送失败')
        time.sleep(1)

        glp = GroupListPage()
        glp.click_back_button(times=2)
        glp.delete_group(name='aaa')

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_contacts_quxinli_0397(self):
        """多方电话"""
        GroupPage = GroupListPage()
        cdp = ContactDetailsPage()
        # preconditions.launch_app()
        time.sleep(1)
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        # 进入群组,添加联系人
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        LabelGroupingChatPage().click_text('添加成员')
        slcp = SelectLocalContactsPage()
        time.sleep(2)
        slcp.swipe_select_one_member_by_name('大佬1')
        slcp.swipe_select_one_member_by_name('大佬3')
        slcp.click_sure()
        time.sleep(1)
        # 多方通话
        GroupPage.enter_mutil_call()
        time.sleep(1)
        GroupPage.click_text("大佬1")
        cdp.send_call_number()
        if GroupPage.is_text_present('我知道了'):
            time.sleep(2)
            GroupPage.click_text('我知道了')
        if GroupPage.is_text_present('发起多方电话失败'):
            pass
        else:
            # cdp.send_call_number()
            cdp.cancel_permission()
            time.sleep(3)
            cdp.cancel_hefeixin_call()
            time.sleep(2)

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_contacts_quxinli_0398(self):
        """多方视频"""
        GroupPage = GroupListPage()
        cdp = ContactDetailsPage()
        # preconditions.launch_app()
        time.sleep(2)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        # 添加成员
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        LabelGroupingChatPage().click_text('添加成员')
        slcp = SelectLocalContactsPage()
        time.sleep(1)
        slcp.swipe_select_one_member_by_name('大佬1')
        time.sleep(1)
        slcp.click_sure()
        time.sleep(1)
        # 点击多方视频
        GroupPage.enter_mutil_video_call()
        while GroupPage.is_text_present('始终允许'):
            GroupPage.click_text('始终允许')
        # if GroupPage.is_text_present('相机权限'):
        #     GroupPage.click_text('始终允许')
        time.sleep(1)
        GroupPage.click_text("大佬1")
        time.sleep(2)
        cdp.send_call_number()
        if cdp.is_text_present('暂不开启'):
            cdp.cancel_permission()
        cdp.end_video_call()

        GroupPage = GroupListPage()
        time.sleep(1)
        SelectOneGroupPage().click_back_by_android()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_contacts_quxinli_0403(self):
        """修改标签名称"""
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        GroupPage.click_settings_button()
        GroupPage.update_label_name(name='bbb')
        GroupPage.click_back_button(times=2)
        GroupPage.page_should_contain_text(text='bbb')

        GroupPage = GroupListPage()
        # GroupPage.click_back_button(times=2)
        GroupPage.delete_group(name='aaa')

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_contacts_quxinli_0411(self):
        """移除成员"""
        GroupPage = GroupListPage()
        # cdp = ContactDetailsPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        # 添加联系人
        time.sleep(2)
        GroupPage.click_text('aaa')
        time.sleep(1)
        LabelGroupingChatPage().click_text('添加成员')
        slcp = SelectLocalContactsPage()
        slcp.swipe_select_one_member_by_name('大佬3')
        time.sleep(1)
        slcp.swipe_select_one_member_by_name('大佬4')
        slcp.click_sure()
        time.sleep(2)
        #移除成员
        GroupPage.click_settings_button()
        GroupPage.click_move_label()
        GroupPage.click_text('大佬3')
        time.sleep(1)
        GroupPage.click_sure_element()
        time.sleep(1)
        GroupPage.click_move_label()
        time.sleep(1)
        GroupPage.page_should_not_contain_text("大佬3")

        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=3)
        GroupPage.delete_group(name='aaa')

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_contacts_quxinli_0415(self):
        """删除标签"""

        GroupPage = GroupListPage()
        time.sleep(1)
        LabelGroupingPage().delete_all_label()
        time.sleep(2)
        GroupPage.new_group(name='ccc')
        GroupPage.delete_group(name='ccc')
        GroupPage.click_back_by_android(times=2)
        GroupPage.page_should_not_contain_text('ccc')


class Tag_Group(TestCase):

    @classmethod
    def setUpClass(cls):
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        # 导入测试联系人
        fail_time1 = 0
        flag1 = False
        import dataproviders
        while fail_time1 < 3:
            try:
                required_contacts = dataproviders.get_preset_contacts()
                conts = ContactsPage()
                conts.open_contacts_page()
                try:
                    if conts.is_text_present("发现SIM卡联系人"):
                        conts.click_text("显示")
                except:
                    pass
                for name, number in required_contacts:
                    # 创建联系人
                    conts.create_contacts_if_not_exits(name, number)
            except:
                fail_time1 += 1
                import traceback
                msg = traceback.format_exc()
                print(msg)

    def default_setUp(self):
        Preconditions.connect_mobile('Android-移动')
        Preconditions.enter_label_grouping_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_contacts_quxinli_0352(self):
        """未添加分组"""
        conts_page = ContactsPage()
        lg = LabelGroupingPage()
        lg.wait_for_page_load()
        lg.delete_all_label()
        lg.assert_default_status_is_right()

        lg.wait_for_page_load()
        lg.click_back()
        conts_page.open_message_page()

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0353(self):
        """新建分组"""
        GroupPage=GroupListPage()
        GroupPage.click_new_group()
        time.sleep(1)
        GroupPage.check_if_contains_element('为你的分组创建一个名称')
        GroupPage.check_if_contains_element('请输入标签分组名称')
        GroupPage.check_if_contains_element('标题新建分组')
        GroupPage.check_if_contains_element()

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0354(self):
        """新建分组,标签分组名称为空"""
        GroupPage=GroupListPage()
        GroupPage.click_new_group()
        GroupPage.click_sure_element()
        time.sleep(3)
        GroupPage.check_if_contains_element()
        GroupPage.sure_icon_is_checkable()

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0355(self):
        """新建分组,标签分组名称输入空格"""
        GroupPage = GroupListPage()
        GroupPage.click_new_group()
        GroupPage.click_input_element()
        time.sleep(3)
        GroupPage.input_content(text=' ')
        time.sleep(2)
        GroupPage.check_if_contains_element()
        GroupPage.sure_icon_is_checkable()

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0356(self):
        """新建分组,标签分组名称输入9个汉字"""
        GroupPage = GroupListPage()
        GroupPage.delete_group(name='祝一路顺风幸福美满')
        GroupPage.click_new_group()
        GroupPage.click_input_element()
        time.sleep(1)
        GroupPage.input_content(text='祝一路顺风幸福美满')
        GroupPage.click_sure_element()
        time.sleep(2)
        GroupPage.click_allow_button()
        GroupPage.page_should_contain_text('选择联系人')

    def tearDown_test_contacts_quxinli_0356(self):
        Preconditions.enter_label_grouping_chat_page()
        GroupPage = GroupListPage()
        GroupPage.delete_group(name='祝一路顺风幸福美满')

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0357(self):
        """新建分组,标签分组名称输入10个汉字"""
        GroupPage = GroupListPage()
        GroupPage.click_new_group()
        GroupPage.click_input_element()
        time.sleep(3)
        GroupPage.input_content(text="祝一路顺风和幸福美满")
        GroupPage.click_sure_element()
        GroupPage.click_allow_button()
        GroupPage.page_should_contain_text('选择联系人')

    def tearDown_test_contacts_quxinli_0357(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=2)
        GroupPage.delete_group(name='祝一路顺风和幸福美满')

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0358(self):
        """新建分组,标签分组名称输入11个汉字"""
        GroupPage = GroupListPage()
        GroupPage.click_new_group()
        GroupPage.click_input_element()
        time.sleep(3)
        text="祝一路顺风和幸福美满啊"
        GroupPage.input_content(text)
        time.sleep(1)
        name=GroupPage.get_text_of_lablegrouping_name()
        self.assertNotEqual(text,name)
        self.assertTrue(len(name) == 10)
        #删除标签分组
        time.sleep(1)
        LabelGroupingPage().click_back()

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0359(self):
        """新建分组,标签分组名称输入29个数字"""
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.click_new_group()
        GroupPage.click_input_element()
        time.sleep(1)
        self.message='1'*29
        GroupPage.input_content(text=self.message)
        time.sleep(1)
        GroupPage.click_sure_element()
        GroupPage.click_allow_button()
        time.sleep(1)
        GroupPage.page_should_contain_text('选择联系人')
        GroupPage.click_back_button(times=2)

    def tearDown_test_contacts_quxinli_0359(self):
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name=self.message)

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0369(self):
        """新建分组,已添加分组后标签分组列表展示"""
        GroupPage = GroupListPage()
        time.sleep(1)
        lg = LabelGroupingPage()
        lg.wait_for_page_load()
        lg.delete_all_label()
        GroupPage.new_group(name='aaa')
        GroupPage.new_group(name='bbb')
        y0=GroupPage.get_element_text_y()
        y1=GroupPage.get_element_text_y(text='aaa')
        y2=GroupPage.get_element_text_y(text='bbb')
        self.assertTrue(y0<y1<y2)

    def tearDown_test_contacts_quxinli_0369(self):
        GroupPage = GroupListPage()
        time.sleep(2)
        GroupPage.delete_group(name='aaa')
        time.sleep(1)
        GroupPage.delete_group(name='bbb')

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0370(self):
        """点击分组列表无成员的分组"""
        GroupPage = GroupListPage()
        time.sleep(1)
        lg = LabelGroupingPage()
        lg.wait_for_page_load()
        lg.delete_all_label()
        GroupPage.new_group()
        #点击该分组
        GroupPage.click_text('aaa')
        time.sleep(2)
        GroupPage.page_should_contain_text('我知道了')
        GroupPage.page_should_contain_text('添加成员')
        #点击我知道了
        GroupPage.click_text('我知道了')
        GroupPage.page_should_not_contain_text('我知道了')
        #点击添加成员
        GroupPage.click_back_button()
        time.sleep(2)
        GroupPage.click_text('aaa')
        time.sleep(1)
        GroupPage.click_text('添加成员')
        time.sleep(2)
        GroupPage.page_should_contain_text('选择联系人')

    def tearDown_test_contacts_quxinli_0370(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=2)
        GroupPage.delete_group(name='aaa')

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0371(self):
        """新建分组,分组详情操作界面"""
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group()
        time.sleep(1)
        GroupPage.click_text('aaa')
        time.sleep(2)
        GroupPage.click_text('知道了')
        time.sleep(1)
        GroupPage.page_contain_element()
        GroupPage.page_contain_element('群发信息')
        GroupPage.page_contain_element('多方电话')
        GroupPage.page_contain_element('多方视频')
        GroupPage.page_contain_element('设置')
        GroupPage.page_contain_element('aaa')

    def tearDown_test_contacts_quxinli_0371(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button()
        GroupPage.delete_group(name='aaa')

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0372(self):
        """新建分组,标签分组添加成员页面"""
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group()
        GroupPage.click_text('aaa')
        time.sleep(1)
        GroupPage.click_text('添加成员')
        time.sleep(2)
        GroupPage.page_should_contain_text('搜索或输入号码')
        GroupPage.page_should_contain_text('选择联系人')
        GroupPage.page_should_contain_text('确定')
        SelectContactsPage().sure_icon_is_checkable()
        GroupPage.page_should_contain_text('选择团队联系人')
        GroupPage.check_if_contains_element(text='联系人列表')

    def tearDown_test_contacts_quxinli_0372(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=2)
        GroupPage.delete_group(name='aaa')

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0373(self):
        """标签分组添加成员-搜索结果页面"""
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        time.sleep(1)
        GroupPage.click_text('添加成员')
        time.sleep(1)
        GroupPage.click_search_box()
        time.sleep(1)
        GroupPage.input_search_text(text='测试')
        GroupPage.hide_keyboard()
        time.sleep(1)
        GroupPage.page_contain_element(locator='搜索框-搜索结果')
        #删除搜索文本
        GroupPage.page_should_contain_element1(locator="删除-搜索")
        GroupPage.clear_input_box()
        time.sleep(1)
        GroupPage.is_element_present()
        #再次输入内容搜索
        GroupPage.input_search_text(text='测试')
        GroupPage.hide_keyboard()
        time.sleep(1)
        GroupPage.page_contain_element(locator='搜索框-搜索结果')
        GroupPage.click_text('测试号码1')
        time.sleep(2)
        GroupPage.hide_keyboard()
        #跳转成功
        GroupPage.page_should_contain_text('搜索或输入号码')
        GroupPage.page_should_contain_text('选择联系人')
        #点击搜索结果
        SelectLocalContactsPage().swipe_select_one_member_by_name('测试号码1')
        GroupPage.is_element_present(locator='已选择的联系人')

    def tearDown_test_contacts_quxinli_0373(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=2)
        GroupPage.delete_group(name='aaa')

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0374(self):
        """标签分组添加成员-搜索陌生号码"""
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        time.sleep(1)
        GroupPage.click_text('添加成员')
        time.sleep(1)
        GroupPage.click_search_box()
        time.sleep(1)
        GroupPage.input_search_text(text='13802885230')
        GroupPage.hide_keyboard()
        time.sleep(1)
        GroupPage.page_should_contain_text('搜索团队联系人')
        GroupPage.is_element_present(locator='联系人头像')

    def tearDown_test_contacts_quxinli_0374(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=2)
        GroupPage.delete_group(name='aaa')

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0375(self):
        """标签分组添加成员-选择本地联系人"""
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        time.sleep(1)
        LabelGroupingChatPage().click_text('添加成员')
        slcp = SelectLocalContactsPage()
        slcp.swipe_select_one_member_by_name('大佬1')
        GroupPage.is_element_present(locator='已选择的联系人')
        GroupPage.sure_icon_is_checkable()
        #再次点击已选择的联系人
        slcp.swipe_select_one_member_by_name('大佬1')
        GroupPage.is_element_present(locator='已选择的联系人')
        #点击已选择联系人的头像,取消选择
        slcp.swipe_select_one_member_by_name('大佬1')
        GroupPage.click_selected_contacts()
        GroupPage.is_element_present(locator='已选择的联系人')
        #选择人员,添加成员成功
        slcp.swipe_select_one_member_by_name('大佬1')
        slcp.click_sure()
        time.sleep(1)

    def tearDown_test_contacts_quxinli_0375(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button()
        GroupPage.delete_group(name='aaa')

    @staticmethod
    def setUp_test_contacts_quxinli_0376():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        GroupListPage().open_contacts_page()
        time.sleep(2)
        ContactsPage().click_search_box()
        ContactListSearchPage().input_search_keyword('本机')
        time.sleep(1)
        if ContactListSearchPage().is_contact_in_list('本机'):
            ContactListSearchPage().click_back()
        else:
        # 创建联系人 本机
            ContactListSearchPage().click_back()
            ContactsPage().click_mobile_contacts()
            ContactsPage().click_add()
            creat_contact2 = CreateContactPage()
            creat_contact2.click_input_name()
            creat_contact2.input_name('本机')
            creat_contact2.click_input_number()
            phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)
            creat_contact2.input_number(phone_number[0])
            creat_contact2.save_contact()
            time.sleep(2)
            ContactDetailsPage().click_back_icon()

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0376(self):
        """标签分组添加成员-选择本地联系人不可选成员"""
        GroupPage = GroupListPage()
        GroupPage.click_label_grouping()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        time.sleep(1)
        LabelGroupingChatPage().click_text('添加成员')
        slcp = SelectLocalContactsPage()
        slcp.swipe_select_one_member_by_name('本机')
        slcp.page_should_contain_text('该联系人不可选择')

    def tearDown_test_contacts_quxinli_0376(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=2)
        GroupPage.delete_group(name='aaa')

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0388(self):
        """分组详情操作界面-分组只有一个人员点击群发消息"""
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        time.sleep(1)
        LabelGroupingChatPage().click_text('添加成员')
        slcp = SelectLocalContactsPage()
        slcp.swipe_select_one_member_by_name('大佬1')
        slcp.click_sure()
        time.sleep(2)
        GroupPage.send_message_to_group()
        time.sleep(1)
        SingleChatPage().is_on_this_page()
        GroupPage.page_should_contain_text('大佬1')

    def tearDown_test_contacts_quxinli_0388(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=2)
        GroupPage.delete_group(name='aaa')

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0389(self):
        """分组详情操作界面-分组有多个人员点击群发消息"""
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        # 添加联系人大佬1 大佬2
        time.sleep(2)
        GroupPage.click_text('aaa')
        time.sleep(1)
        LabelGroupingChatPage().click_text('添加成员')
        slcp = SelectLocalContactsPage()
        slcp.swipe_select_one_member_by_name('大佬1')
        time.sleep(1)
        slcp.swipe_select_one_member_by_name('大佬2')
        slcp.click_sure()
        time.sleep(2)
        #验证页面元素
        GroupPage.send_message_to_group()
        time.sleep(1)
        GroupPage.page_contain_element(locator='多方通话_图标')
        GroupPage.page_contain_element(locator='分组联系人')
        GroupPage.page_contain_element(locator='富媒体面板')
        GroupPage.page_contain_element(locator='aaa')

    def tearDown_test_contacts_quxinli_0389(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=2)
        GroupPage.delete_group(name='aaa')

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0390(self):
        """分组详情操作界面-群发消息-发送消息"""
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        #添加小组成员
        GroupPage.click_text('aaa')
        time.sleep(1)
        LabelGroupingChatPage().click_text('添加成员')
        slcp = SelectLocalContactsPage()
        time.sleep(2)
        slcp.swipe_select_one_member_by_name('大佬1')
        slcp.click_sure()
        time.sleep(2)
        message='aa aa'*20
        GroupPage.send_message_to_group(message)
        time.sleep(1)
        GroupPage.page_contain_element('已转短信送达')
        #发送纯文本
        GroupPage.click_back_button()
        time.sleep(1)
        message = 'aaaa'
        GroupPage.send_message_to_group(message)
        time.sleep(5)
        GroupPage.page_contain_element('已转短信送达')
        #发送文本 空格
        GroupPage.click_back_button()
        time.sleep(1)
        message = 'aa aa'
        GroupPage.send_message_to_group(message)
        time.sleep(5)
        GroupPage.page_contain_element('已转短信送达')
        #发送表情
        GroupPage.click_back_button()
        time.sleep(1)
        GroupPage.send_express_to_group()
        time.sleep(1)
        GroupPage.page_not_contain_element('发送失败')
        #发送图片
        GroupPage.click_back_button()
        time.sleep(1)
        GroupPage.send_picture_to_group()
        time.sleep(2)
        GroupPage.page_not_contain_element('发送失败')
        time.sleep(1)

    def tearDown_test_contacts_quxinli_0390(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=2)
        GroupPage.delete_group(name='aaa')

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0394(self):
        """分组联系人进入Profile页-星标"""
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        #添加成员
        GroupPage.click_text('aaa')
        time.sleep(2)
        LabelGroupingChatPage().click_text('添加成员')
        time.sleep(2)
        slcp = SelectLocalContactsPage()
        slcp.swipe_select_one_member_by_name('大佬1')
        time.sleep(1)
        slcp.swipe_select_one_member_by_name('大佬2')
        slcp.click_sure()
        time.sleep(1)
        #进入群发页面
        GroupPage.enter_group_message()
        GroupPage.click_divide_group_icon()
        time.sleep(1)
        GroupPage.page_contain_element(locator='分组联系人_标题')
        GroupPage.click_text("大佬1")
        # time.sleep(1)
        # GroupPage.click_star_icon()
        time.sleep(1)
        GroupPage.click_star_icon()
        if GroupPage.is_toast_exist('已成功添加为星标联系人'):
            time.sleep(2)
        else:
            time.sleep(1)
            GroupPage.click_star_icon()
            GroupPage.is_toast_exist("已成功添加为星标联系人")
        time.sleep(1)
        GroupPage.click_star_icon()
        GroupPage.is_toast_exist("已取消添加为星标联系人")
        #再次点击星标
        GroupPage.click_star_icon()
        GroupPage.click_back_button(times=3)
        time.sleep(2)
        GroupPage.click_back_button(times=2)
        time.sleep(1)
        GroupPage.page_contain_star('大佬1')

    def tearDown_test_contacts_quxinli_0394(self):
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()
        ContactsPage().click_mobile_contacts()
        #去除大佬1的星标
        ContactsPage().select_contacts_by_name('大佬1')
        GroupPage = GroupListPage()
        GroupPage.click_star_icon()
        if GroupPage.is_toast_exist('已取消添加为星标联系人'):
            time.sleep(2)
        else:
            time.sleep(1)
            GroupPage.click_star_icon()
        time.sleep(1)
        #删除群组
        GroupPage.click_back_button()
        time.sleep(2)
        GroupPage.click_label_grouping()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0395(self):
        """分组联系人进入Profile页-编辑"""
        GroupPage = GroupListPage()
        cdp=ContactDetailsPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        time.sleep(1)
        LabelGroupingChatPage().click_text('添加成员')
        slcp = SelectLocalContactsPage()
        time.sleep(2)
        slcp.swipe_select_one_member_by_name('大佬1')
        slcp.swipe_select_one_member_by_name('大佬2')
        slcp.click_sure()
        time.sleep(1)
        GroupPage.enter_group_message()
        GroupPage.click_divide_group_icon()
        time.sleep(1)
        GroupPage.page_contain_element(locator='分组联系人_标题')
        GroupPage.click_text("大佬1")
        time.sleep(2)
        cdp.click_edit_contact()
        time.sleep(1)
        number=CreateContactPage().get_contant_number()
        if number == '13800138789':
            CreateContactPage().click_back()
        else:
            cdp.change_mobile_number()
            time.sleep(1)
            cdp.click_sure_icon()
            time.sleep(1)
            GroupPage.is_toast_exist("保存成功")
            cdp.is_text_present('13800138789')

    def tearDown_test_contacts_quxinli_0395(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=2)
        GroupPage.click_back_button(times=2)
        GroupPage.delete_group(name='aaa')
        #恢复修改的联系人号码
        GroupPage.click_back_button()
        ContactsPage().select_contacts_by_name('大佬1')
        ContactDetailsPage().click_edit_contact()
        time.sleep(1)
        CreateContactPage().click_input_number()
        CreateContactPage().change_mobile_number()
        time.sleep(1)
        CreateContactPage().click_save()
        time.sleep(2)

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0396(self):
        """分组联系人进入Profile页-编辑-删除联系人"""
        GroupPage = GroupListPage()
        cdp=ContactDetailsPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        #进入分组 添加成员
        GroupPage.click_text('aaa')
        time.sleep(1)
        GroupPage.tap_sure_box()
        time.sleep(1)
        LabelGroupingChatPage().click_text('添加成员')
        slcp = SelectLocalContactsPage()
        time.sleep(2)
        slcp.swipe_select_one_member_by_name('大佬1')
        time.sleep(1)
        slcp.swipe_select_one_member_by_name('大佬2')
        slcp.click_sure()
        time.sleep(1)
        #进入群发消息页面
        GroupPage.enter_group_message()
        GroupPage.click_divide_group_icon()
        time.sleep(1)
        GroupPage.page_contain_element(locator='分组联系人_标题')
        GroupPage.click_text("大佬2")
        time.sleep(2)
        cdp.click_edit_contact()
        time.sleep(1)
        cdp.hide_keyboard()
        cdp.page_up()
        cdp.change_delete_number()
        cdp.click_sure_delete()
        time.sleep(1)
        GroupPage.is_toast_exist("删除成功")
        time.sleep(1)

    def tearDown_test_contacts_quxinli_0396(self):
        GroupPage = GroupListPage()
     #   GroupPage.click_back_button(times=2)
        GroupPage.click_back_by_android(times=2)
        GroupPage.delete_group(name='aaa')
        time.sleep(2)
        #删除该联系人后添加联系人
        LabelGroupingPage().click_back()
        time.sleep(2)
        ContactsPage().click_add()
        ccp=CreateContactPage()
        ccp.click_input_name()
        ccp.input_name('大佬2')
        ccp.click_input_number()
        ccp.input_number('13800138006')
        ccp.click_save()
        CallContactDetailPage().click_back()

    @tags('ALL', 'CONTACT', '多方通话-跳过')
    def test_contacts_quxinli_0397(self):
        """“分组详情操作”界面-多方电话"""
        GroupPage = GroupListPage()
        cdp=ContactDetailsPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        #进入群组,添加联系人
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        LabelGroupingChatPage().click_text('添加成员')
        slcp = SelectLocalContactsPage()
        time.sleep(2)
        slcp.swipe_select_one_member_by_name('大佬1')
        slcp.swipe_select_one_member_by_name('大佬3')
        slcp.click_sure()
        time.sleep(1)
        #多方通话
        GroupPage.enter_mutil_call()
        time.sleep(1)
        GroupPage.click_text("大佬1")
        cdp.send_call_number()
        if GroupPage.is_text_present('我知道了'):
            time.sleep(2)
            GroupPage.click_text('我知道了')
        if GroupPage.is_text_present('发起多方电话失败'):
            pass
        else:
            # cdp.send_call_number()
            cdp.cancel_permission()
            time.sleep(3)
            cdp.cancel_hefeixin_call()
            time.sleep(2)

    def tearDown_test_contacts_quxinli_0397(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button()
        GroupPage.delete_group(name='aaa')

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0398(self):
        """“分组详情操作”界面-多方视频"""
        GroupPage = GroupListPage()
        cdp = ContactDetailsPage()

        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')

        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        LabelGroupingChatPage().click_text('添加成员')
        slcp = SelectLocalContactsPage()
        time.sleep(1)
        slcp.swipe_select_one_member_by_name('大佬1')
        time.sleep(1)
        slcp.click_sure()
        time.sleep(1)
        GroupPage.enter_mutil_video_call()
        time.sleep(2)
        while GroupPage.is_text_present('始终允许'):
            GroupPage.click_text('始终允许')
        time.sleep(1)
        GroupPage.click_text("大佬1")
        time.sleep(2)
        cdp.send_call_number()
        if cdp.is_text_present('暂不开启'):
            cdp.cancel_permission()
        cdp.end_video_call()

    def tearDown_test_contacts_quxinli_0398(self):
        GroupPage = GroupListPage()
        time.sleep(1)
        SelectOneGroupPage().click_back_by_android()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0407(self):
        """“分组设置-特殊符号标签名称
        auther:darcy
        """
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        GroupPage.click_settings_button()
        GroupPage.update_label_name(name='*@!#')
        GroupPage.click_back_button(times=2)
        GroupPage.page_should_contain_text(text='*@!#')

    def tearDown_test_contacts_quxinli_0407(self):
        GroupPage = GroupListPage()
        GroupPage.delete_group(name='*@!#')

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0408(self):
        """“分组设置-各种标签名称
        auther:darcy
        """
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        GroupPage.click_settings_button()
        GroupPage.update_label_name(name='*@!#123好')
        GroupPage.click_back_button(times=2)
        GroupPage.page_should_contain_text(text='*@!#123好')

    def tearDown_test_contacts_quxinli_0408(self):
        GroupPage = GroupListPage()
        GroupPage.delete_group(name='*@!#123好')

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0409(self):
        """“分组设置-各种标签名称删除
        auther:darcy
        """
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        GroupPage.click_settings_button()
        GroupPage.delete_label_name(name='*@!#123好')
        GroupPage.page_should_contain_text(text="请输入标签分组名称")
        GroupPage.click_back_button(times=3)

    def tearDown_test_contacts_quxinli_0409(self):
        GroupPage = GroupListPage()
        GroupPage.delete_group(name='*@!#123好')

    @tags('ALL', 'CONTACT-debug', 'CMCC')
    def test_contacts_quxinli_0414(self):
        """分组设置-搜索移除成员
        auther:darcy
        """
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        #添加成员
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        time.sleep(1)
        LabelGroupingChatPage().click_text('添加成员')
        slcp = SelectLocalContactsPage()
        time.sleep(1)
        slcp.swipe_select_one_member_by_name('大佬1')
        slcp.click_sure()
        time.sleep(2)
        #移除成员
        GroupPage.click_settings_button()
        GroupPage.click_move_label()
        time.sleep(1)
        GroupPage.search_menber_text(text='dalao1')
        time.sleep(1)
        GroupPage.click_text('大佬1')
        time.sleep(1)
        GroupPage.click_sure_element()
        time.sleep(1)
        GroupPage.click_move_label()
        time.sleep(1)
        GroupPage.page_should_not_contain_text("大佬1")

    def tearDown_test_contacts_quxinli_0414(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=3)
        GroupPage.delete_group(name='aaa')

    @tags('ALL', 'CONTACT-debug', 'CMCC')
    def test_contacts_quxinli_0415(self):
        """分组设置-删除标签
        auther:darcy
        """
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.new_group(name='ccc')
        GroupPage.delete_group(name='ccc')
        GroupPage.click_back_by_android(times=2)

    @tags('ALL', 'CONTACT-debug', 'CMCC')
    def test_contacts_quxinli_0416(self):
        """分组详情操作页面进入Profile页"""
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        #添加成员
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        time.sleep(1)
        LabelGroupingChatPage().click_text('添加成员')
        slcp = SelectLocalContactsPage()
        time.sleep(1)
        slcp.swipe_select_one_member_by_name('大佬3')
        # slcp.select_one_member_by_name('大佬2')
        slcp.swipe_select_one_member_by_name('大佬4')
        slcp.click_sure()
        time.sleep(2)
        LableGroupDetailPage().click_send_group_info()
        time.sleep(2)
        GroupPage.click_divide_group_icon()
        time.sleep(1)
        GroupPage.page_contain_element(locator='分组联系人_标题')
        GroupPage.click_text("大佬3")
        time.sleep(1)
        GroupPage.page_contain_element(locator='语音通话')
        GroupPage.page_contain_element(locator='视频通话')
        GroupPage.page_contain_element(locator='分享名片')
        GroupPage.click_share_button()
        time.sleep(1)
        SelectContactsPage().click_select_one_group()
        time.sleep(1)
        SelectOneGroupPage().click_search_group()
        SelectOneGroupPage().input_search_keyword('给个红包1')
        SelectOneGroupPage().selecting_one_group_by_name('给个红包1')
        SelectOneGroupPage().click_share_business_card()
        time.sleep(2)

    def tearDown_test_contacts_quxinli_0416(self):
        Preconditions.enter_label_grouping_chat_page()
        time.sleep(1)
        GroupPage = GroupListPage()
        GroupPage.delete_group(name='aaa')

    @tags('ALL', 'CONTACT-debug', 'CMCC')
    def test_contacts_quxinli_0417(self):
        """分组详情操作页面进入Profile页_星标
        auther:darcy"""
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        #添加成员
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        time.sleep(1)
        LabelGroupingChatPage().click_text('添加成员')
        slcp = SelectLocalContactsPage()
        time.sleep(1)
        slcp.swipe_select_one_member_by_name('大佬3')
        slcp.swipe_select_one_member_by_name('大佬4')
        slcp.click_sure()
        time.sleep(2)

        GroupPage.enter_group_message()
        time.sleep(1)
        GroupPage.click_divide_group_icon()
        time.sleep(1)
        GroupPage.page_contain_element(locator='分组联系人_标题')
        GroupPage.click_text("大佬3")
        time.sleep(1)
        GroupPage.click_star_icon()
        GroupPage.is_toast_exist("已成功添加为星标联系人")
        time.sleep(1)
        GroupPage.click_star_icon()
        GroupPage.is_toast_exist("已取消添加为星标联系人")
        GroupPage.click_star_icon()
       # GroupPage.click_back_button(times=3)
        GroupPage.click_back_by_android(times=3)
        time.sleep(2)
       # GroupPage.click_back_button(times=2)
        GroupPage.click_back_by_android(times=2)

        time.sleep(1)
        GroupPage.page_contain_star('大佬3')

    def tearDown_test_contacts_quxinli_0417(self):
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()
        ContactsPage().click_mobile_contacts()
        #去除大佬1的星标
        ContactsPage().select_contacts_by_name('大佬3')
        time.sleep(1)
        GroupPage = GroupListPage()
        GroupPage.click_star_icon()
        if GroupPage.is_text_present('已取消添加为星标联系人'):
            GroupPage.click_back_button()
        elif GroupPage.is_text_present('已成功添加为星标联系人'):
            GroupPage.click_star_icon()
            GroupPage.click_back_button()
        #删除群组
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.click_label_grouping()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0421(self):
        """安卓手机：手机系统本地新建分组名称等于30个字符的分组
        auther:darcy"""
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        name="a"*30
        GroupPage.new_group(name=name)
        GroupPage.click_text(name)
        time.sleep(1)
        GroupPage.tap_sure_box()
        GroupPage.click_settings_button()
        GroupPage.update_label_name(name='aaa')
        GroupPage.click_back_button(times=2)
        time.sleep(1)
        GroupPage.page_should_contain_text(text='aaa')
        #添加成员
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        time.sleep(1)
        LabelGroupingChatPage().click_text('添加成员')
        slcp = SelectLocalContactsPage()
        time.sleep(1)
        slcp.swipe_select_one_member_by_name('大佬6')
        slcp.swipe_select_one_member_by_name('大佬7')
        slcp.click_sure()
        time.sleep(2)
        #进入设置界面
        GroupPage.click_settings_button()
        time.sleep(1)
        GroupPage.click_move_label()
        time.sleep(1)
        GroupPage.click_text('大佬6')
        time.sleep(1)
        GroupPage.click_sure_element()
        time.sleep(1)
        GroupPage.click_move_label()
        time.sleep(1)
        GroupPage.page_should_not_contain_text("大佬6")

    def tearDown_test_contacts_quxinli_0421(self):
        Preconditions.enter_label_grouping_chat_page()
        GroupPage = GroupListPage()
        # GroupPage.click_back_button(times=4)
        time.sleep(1)
        GroupPage.delete_group(name='aaa')

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0360(self):
        """新建分组,标签分组名称输入30个数字"""
        GroupPage = GroupListPage()
        time.sleep(1)
        LabelGroupingPage().delete_all_label()
        GroupPage.click_new_group()
        GroupPage.click_input_element()
        time.sleep(1)
        self.message1 = '2' * 30
        GroupPage.input_content(text=self.message1)
        time.sleep(1)
        GroupPage.click_sure_element()
        time.sleep(1)
        GroupPage.page_should_contain_text('选择联系人')

    def tearDown_test_contacts_quxinli_0360(self):
        GroupPage = GroupListPage()
        Preconditions.enter_label_grouping_chat_page()
        GroupPage.delete_group(name=self.message1)

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0361(self):
        """新建分组,标签分组名称输入31个数字"""
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.click_new_group()
        GroupPage.click_input_element()
        text="1"*31
        GroupPage.input_content(text)
        time.sleep(1)
        name=GroupPage.get_text_of_lablegrouping_name()
        self.assertNotEqual(text,name)
        self.assertTrue(len(name) == 30)
        #删除标签分组
        time.sleep(1)
        LabelGroupingPage().click_back()

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0362(self):
        """新建分组,标签分组名称输入29个字母"""
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.click_new_group()
        GroupPage.click_input_element()
        time.sleep(1)
        self.message = 'a' * 29
        GroupPage.input_content(text=self.message)
        time.sleep(1)
        GroupPage.click_sure_element()
        time.sleep(1)
        GroupPage.page_should_contain_text('选择联系人')

    def tearDown_test_contacts_quxinli_0362(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button()
        time.sleep(1)
        GroupPage.click_back_button()
        time.sleep(1)
        GroupPage.delete_group(name=self.message)

    @tags('ALL', 'debug', 'CMCC')
    def test_contacts_quxinli_0363(self):
        """新建分组,标签分组名称输入30个字母"""
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.click_new_group()
        GroupPage.click_input_element()
        time.sleep(1)
        self.message2 = 'c' * 30
        GroupPage.input_content(text=self.message2)
        time.sleep(1)
        GroupPage.click_sure_element()
        time.sleep(1)
        GroupPage.page_should_contain_text('选择联系人')

    def tearDown_test_contacts_quxinli_0363(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button()
        time.sleep(1)
        GroupPage.click_back_button()
        time.sleep(1)
        GroupPage.delete_group(name=self.message2)

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0364(self):
        """新建分组,标签分组名称输入31字母"""
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.click_new_group()
        GroupPage.click_input_element()
        text="a"*31
        GroupPage.input_content(text)
        time.sleep(1)
        name=GroupPage.get_text_of_lablegrouping_name()
        self.assertNotEqual(text,name)
        self.assertTrue(len(name) == 30)
        #删除标签分组
        time.sleep(1)
        LabelGroupingPage().click_back()

    @tags('ALL', 'debug', 'CMCC')
    def test_contacts_quxinli_0365(self):
        """新建分组,标签分组名称输入29个字符：汉字、数字、英文字母、空格和特殊字符组合"""
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.click_new_group()
        GroupPage.click_input_element()
        time.sleep(1)
        self.message3 = 'aa111@@@文 aaa111@@@文 aaaa'
        GroupPage.input_content(text=self.message3)
        time.sleep(1)
        GroupPage.click_sure_element()
        time.sleep(1)
        GroupPage.page_should_contain_text('选择联系人')

    def tearDown_test_contacts_quxinli_0365(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button()
        time.sleep(1)
        GroupPage.click_back_button()
        time.sleep(1)
        GroupPage.delete_group(name=self.message3)

    @tags('ALL', 'debug', 'CMCC')
    def test_contacts_quxinli_0366(self):
        """新建分组,标签分组名称输入30个字符：汉字、数字、英文字母、空格和特殊字符组合"""
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.click_new_group()
        GroupPage.click_input_element()
        time.sleep(1)
        self.message4 = 'aa111@@@文 aaa111@@@文 aaaaa'
        GroupPage.input_content(text=self.message4)
        time.sleep(1)
        GroupPage.click_sure_element()
        time.sleep(1)
        GroupPage.page_should_contain_text('选择联系人')

    def tearDown_test_contacts_quxinli_0366(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button()
        time.sleep(1)
        GroupPage.click_back_button()
        time.sleep(1)
        GroupPage.delete_group(name=self.message4)

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0367(self):
        '''
        标签分组名称输入31个字符：汉字、数字、英文字母、空格和特殊字符组合(中文占据3个字符)
        '''
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.click_new_group()
        GroupPage.click_input_element()
        text="aa111@@@文 aaa111@@@文 aaaaad"
        GroupPage.input_content(text)
        time.sleep(1)
        name=GroupPage.get_text_of_lablegrouping_name()
        self.assertNotEqual(text,name)
        self.assertTrue(len(name) == 26)
        #删除标签分组
        time.sleep(1)
        LabelGroupingPage().click_back()

    @tags('ALL', 'debug', 'CMCC')
    def test_contacts_quxinli_0368(self):
        '''
        新建分组进入选择联系人页面后点击返回，重名检查

        '''
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.click_new_group()
        GroupPage.click_input_element()
        time.sleep(1)
        self.message6 = 'aaaa'
        GroupPage.input_content(text=self.message6)
        time.sleep(1)
        GroupPage.click_sure_element()
        time.sleep(1)
        GroupPage.click_back_button()
        time.sleep(1)
        GroupPage.click_sure_element()
        LabelGroupingPage().is_group_exist_tips_popup()
        # GroupPage.is_toast_exist('群组已存在')

    def tearDown_test_contacts_quxinli_0368(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button()
        time.sleep(1)
        GroupPage.delete_group(name=self.message6)

    @tags('ALL', 'debug', 'CMCC')
    def test_contacts_quxinli_0391(self):
        """分组详情操作界面-群发消息-多方通话图标"""
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        #添加联系人大佬1 大佬2
        time.sleep(2)
        GroupPage.click_text('aaa')
        time.sleep(1)
        LabelGroupingChatPage().click_text('添加成员')
        slcp = SelectLocalContactsPage()
        slcp.swipe_select_one_member_by_name('大佬1')
        time.sleep(1)
        slcp.swipe_select_one_member_by_name('大佬2')
        slcp.click_sure()
        time.sleep(2)
        #判断页面包含的元素
        GroupPage.page_contain_element(locator='多方电话提示框')
        GroupPage.page_contain_element(locator='多方视频图标')
        GroupPage.click_coordinate(x=1 / 2, y=1 / 10)

    def tearDown_test_contacts_quxinli_0391(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=2)
        GroupPage.delete_group(name='aaa')

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0392(self):
        """分组详情操作界面-群发消息-分组联系人图标"""
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        # 添加联系人大佬1 大佬2
        time.sleep(2)
        GroupPage.click_text('aaa')
        time.sleep(1)
        LabelGroupingChatPage().click_text('添加成员')
        slcp = SelectLocalContactsPage()
        slcp.swipe_select_one_member_by_name('大佬1')
        time.sleep(1)
        slcp.swipe_select_one_member_by_name('大佬2')
        slcp.click_sure()
        time.sleep(2)
        #判断页面元素
        GroupPage.click_send_message_to_group()
        GroupPage.click_divide_group_icon()
        time.sleep(1)
        GroupPage.page_should_contain_text("分组联系人")
        GroupPage.page_should_contain_text("大佬1")
        GroupPage.page_should_contain_text("大佬2")
        GroupPage.check_if_contains_element(text='分组联系人-姓名')
        GroupPage.check_if_contains_element(text='分组联系人-电话号码')

    def tearDown_test_contacts_quxinli_0392(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=3)
        GroupPage.delete_group(name='aaa')

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0393(self):
        """分组联系人进入Profile页"""
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        # 添加联系人大佬1 大佬2
        time.sleep(2)
        GroupPage.click_text('aaa')
        time.sleep(1)
        LabelGroupingChatPage().click_text('添加成员')
        slcp = SelectLocalContactsPage()
        slcp.swipe_select_one_member_by_name('大佬1')
        time.sleep(1)
        slcp.swipe_select_one_member_by_name('大佬2')
        slcp.click_sure()
        time.sleep(2)
        #判断页面元素
        GroupPage.click_send_message_to_group()
        GroupPage.click_divide_group_icon()
        time.sleep(1)
        GroupPage.page_contain_element(locator='分组联系人_标题')
        GroupPage.click_text("大佬1")
        time.sleep(1)
        detailpage=ContactDetailsPage()
        detailpage.is_exists_contacts_name()
        detailpage.is_exists_contacts_number()
        detailpage.page_should_contain_element_first_letter()
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
        detailpage.page_should_contain_text('和飞信电话')
        detailpage.page_should_contain_text('分享名片')
        time.sleep(1)
        detailpage.click_share_business_card()
        time.sleep(1)
        SelectContactsPage().select_local_contacts()
        SelectContactsPage().click_one_contact('大佬1')
        SelectContactsPage().click_share_card()

    def tearDown_test_contacts_quxinli_0393(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button()
        GroupPage.click_back_button(times=2)
        GroupPage.delete_group(name='aaa')

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0399(self):
        """“分组设置入口"""
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        GroupPage.click_settings_button()
        GroupPage.page_contain_element("标签设置")

    def tearDown_test_contacts_quxinli_0399(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=2)
        GroupPage.delete_group(name='aaa')

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0400(self):
        """“分组设置返回，
         auther:darcy
        """
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        GroupPage.click_settings_button()
        GroupPage.click_back_button(times=1)
        GroupPage.page_not_contain_element("标签设置")

    def tearDown_test_contacts_quxinli_0400(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=1)
        GroupPage.delete_group(name='aaa')

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0401(self):
        """“分组设置界面
        auther:darcy
        """
        GroupPage = GroupListPage()

        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        GroupPage.click_settings_button()
        GroupPage.page_contain_element("标签设置")
        GroupPage.page_contain_element("删除标签")
        GroupPage.page_contain_element("移除成员")
        GroupPage.page_contain_element("标签名称")

    def tearDown_test_contacts_quxinli_0401(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=1)
        GroupPage.delete_group(name='aaa')

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0402(self):
        """“分组设置-标签名称
        auther:darcy
        """
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        GroupPage.click_settings_button()
        GroupPage.click_label_name()
        GroupPage.page_contain_element("修改标签名称")

    def tearDown_test_contacts_quxinli_0402(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=3)
        GroupPage.delete_group(name='aaa')

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0403(self):
        """“分组设置-字母标签名称
        auther:darcy
        """
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        GroupPage.click_settings_button()
        GroupPage.update_label_name(name='bbb')
        GroupPage.click_back_button(times=2)
        GroupPage.page_should_contain_text(text='bbb')

    def tearDown_test_contacts_quxinli_0403(self):
        GroupPage = GroupListPage()
        GroupPage.delete_group(name='bbb')

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0404(self):
        """“分组设置-中文标签名称
        auther:darcy
        """
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        GroupPage.click_settings_button()
        GroupPage.update_label_name(name='好记性')
        GroupPage.click_back_button(times=2)
        GroupPage.page_should_contain_text(text='好记性')

    def tearDown_test_contacts_quxinli_0404(self):
        GroupPage = GroupListPage()
        GroupPage.delete_group(name='好记性')

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0405(self):
        """“分组设置-数字标签名称
        auther:darcy
        """
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        GroupPage.click_settings_button()
        GroupPage.update_label_name(name='111')
        GroupPage.click_back_button(times=2)
        GroupPage.page_should_contain_text(text='111')

    def tearDown_test_contacts_quxinli_0405(self):
        GroupPage = GroupListPage()
        GroupPage.delete_group(name='111')

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0406(self):
        """“分组设置-符号标签名称
        auther:darcy
        """
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        GroupPage.click_settings_button()
        GroupPage.update_label_name(name='？？？')
        GroupPage.click_back_button(times=2)
        GroupPage.page_should_contain_text(text='？？？')

    def tearDown_test_contacts_quxinli_0406(self):
        GroupPage = GroupListPage()
        GroupPage.delete_group(name='？？？')

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0410(self):
        """“分组设置-移除成员入口
        auther:darcy
        """
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        GroupPage.click_settings_button()
        GroupPage.click_move_label()
        GroupPage.page_contain_element(locator="移除成员_标题")
        GroupPage.page_contain_element(locator="搜索标签分组成员")
        GroupPage.click_back_button(times=3)

    def tearDown_test_contacts_quxinli_0410(self):
        GroupPage = GroupListPage()
        GroupPage.delete_group(name='aaa')

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0411(self):
        """“分组设置-分组设置-移除成员
        auther:darcy
        """
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        GroupPage.click_text('aaa')
        GroupPage.tap_sure_box()
        GroupPage.click_settings_button()
        GroupPage.click_move_label()
        GroupPage.click_sure_element()
        GroupPage.page_contain_element(locator="移除成员_标题")

    def tearDown_test_contacts_quxinli_0411(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=3)
        GroupPage.delete_group(name='aaa')

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0412(self):
        """“分组设置-移除成员选择
        auther:darcy
        """
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        # 添加联系人大佬1 大佬2
        time.sleep(2)
        GroupPage.click_text('aaa')
        time.sleep(1)
        LabelGroupingChatPage().click_text('添加成员')
        slcp = SelectLocalContactsPage()
        slcp.swipe_select_one_member_by_name('大佬1')
        time.sleep(1)
        slcp.swipe_select_one_member_by_name('大佬2')
        slcp.click_sure()
        time.sleep(2)
        #判断页面元素
        GroupPage.click_settings_button()
        GroupPage.click_move_label()
        GroupPage.click_text('大佬2')
        time.sleep(1)
        GroupPage.page_contain_element(locator="成员头像")
        GroupPage.sure_icon_is_checkable()
        time.sleep(1)
        GroupPage.click_back_button()
        time.sleep(1)
        GroupPage.page_should_not_contain_text("大佬2")

    def tearDown_test_contacts_quxinli_0412(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=3)
        GroupPage.delete_group(name='aaa')

    @tags('ALL', 'CONTACT', 'CMCC')
    def test_contacts_quxinli_0413(self):
        """分组设置-移除成员
        auther:darcy
        """
        GroupPage = GroupListPage()
        time.sleep(1)
        GroupPage.delete_group(name='aaa')
        GroupPage.new_group(name='aaa')
        # 添加联系人大佬1 大佬2
        time.sleep(2)
        GroupPage.click_text('aaa')
        time.sleep(1)
        LabelGroupingChatPage().click_text('添加成员')
        slcp = SelectLocalContactsPage()
        slcp.swipe_select_one_member_by_name('大佬1')
        time.sleep(1)
        slcp.swipe_select_one_member_by_name('大佬2')
        slcp.click_sure()
        time.sleep(2)
        #判断页面元素
        GroupPage.click_settings_button()
        GroupPage.click_move_label()
        GroupPage.click_text('大佬2')
        time.sleep(1)
        GroupPage.click_sure_element()
        time.sleep(1)
        GroupPage.click_move_label()
        time.sleep(1)
        GroupPage.page_should_not_contain_text("大佬2")
        GroupPage.is_element_present(locator='移除-已选择联系人')

    def tearDown_test_contacts_quxinli_0413(self):
        GroupPage = GroupListPage()
        GroupPage.click_back_button(times=3)
        GroupPage.delete_group(name='aaa')


if __name__ == '__main__':
    unittest.main()
