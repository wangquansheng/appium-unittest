import time
import unittest
from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.contacts import OfficialAccountDetailPage
from pages.contacts import OfficialAccountPage, SearchOfficialAccountPage
from preconditions.BasePreconditions import LoginPreconditions, WorkbenchPreconditions

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
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
    def make_sure_in_official_page():
        """确保在公众号页面"""
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        conts_page = ContactsPage()
        conts_page.open_contacts_page()
        conts_page.click_official_account_icon()


class OfficialAccountTest(TestCase):
    """通讯录-公众号模块"""

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
                required_contacts = dataproviders.get_preset_contacts()
                conts = ContactsPage()
                current_mobile().hide_keyboard_if_display()
                Preconditions.make_already_in_message_page()
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

        # 导入团队联系人
        fail_time2 = 0
        flag2 = False
        while fail_time2 < 2:
            try:
                Preconditions.make_already_in_message_page()
                contact_names = ["大佬1", "大佬2", "大佬3", "大佬4", '香港大佬', '测试号码']
                Preconditions.create_he_contacts(contact_names)
                phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
                contact_names2 = [("b测算", "13800137001"), ("c平5", "13800137002"), ('哈 马上', "13800137003"),
                                  ('陈丹丹', "13800137004"), ('alice', "13800137005"), ('郑海', "13802883296"),
                                  ('#*', '13800137006'), ('#1', '13800137007'), ('本机测试', phone_number)]
                # 将联系人添加到团队及团队子部门
                Preconditions.create_he_contacts2(contact_names2)
                WorkbenchPreconditions.create_he_contacts_for_sub_department("bm0", contact_names2)
                Preconditions.create_sub_department_by_name('测试部门1', '测试号码')
                flag2 = True
            except:
                fail_time2 += 1
            if flag2:
                break

    def default_setUp(self):
        """确保每个用例运行前在公众号页面"""
        Preconditions.make_sure_in_official_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_contacts_quxinli_0323(self):
        """企业号列表显示为空"""
        official_account = OfficialAccountPage()
        official_account.click_tag('企业号')
        official_account.assert_enterprise_account_list_is_empty()
        official_account.page_should_contain_text('未关注任何企业号')

    @unittest.skip('脚本无法操作搜索公众号页面')
    def test_Conts_OfficialAccount_0002(self):
        """搜索公众号"""
        official_account = OfficialAccountPage()
        official_account.click_tag('订阅/服务号')
        official_account.click_add()

        search = SearchOfficialAccountPage()
        search.input_search_key('1')
        search.subscribe_first_items(12)
        print('test')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0322(self):
        """订阅号/服务号列表显示"""
        conts_page = ContactsPage()
        time.sleep(2)
        conts_page.is_text_present('和飞信')
        conts_page.is_text_present('和飞信团队')
        conts_page.is_text_present('和飞信新闻')
        conts_page.is_text_present('中国移动10086')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0324(self):
        """公众号会话页面(未配置底部菜单栏)"""
        official = OfficialAccountPage()
        official.click_officel_account()
        time.sleep(2)
        official.page_contain_news()
        official.page_contain_setting()
        official.page_contain_input_box()
        # official.page_contain_expresssion()
        official.page_contain_send_button()
        official.send_btn_is_clickable()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0325(self):
        """公众号会话页面(配置底部菜单栏)"""
        official = OfficialAccountPage()
        official.select_one_account_by_name('和飞信')
        time.sleep(2)
        official.page_contain_element(text='公众号标题')
        official.page_contain_setting()
        official.page_contain_keyboard()
        official.page_should_contain_element_menu()
        # 点击键盘
        official.click_keyboard()
        time.sleep(2)
        official.page_contain_input_box()
        # official.page_contain_expresssion()
        official.page_contain_send_button()
        official.send_btn_is_clickable()
        # 再次点击键盘图标
        official.click_keyboard()
        time.sleep(2)
        official.page_should_contain_element_menu()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0326(self):
        """公众号会话页面发送文本消息"""
        official = OfficialAccountPage()
        official.click_officel_account()
        time.sleep(2)
        official.click_input_box()
        time.sleep(1)
        official.input_message('good news')
        official.click_send_button()
        time.sleep(1)
        official.page_should_not_contain_sendfail_element()
        official.page_should_contain_text('good news')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0327(self):
        """公众号会话页面发送表情消息"""
        official = OfficialAccountPage()
        official.click_officel_account()
        time.sleep(2)
        # 备注：该版本无表情
        # official.click_expression()
        # official.click_expression('[微笑1]')
        # official.click_send_button()
        # time.sleep(1)
        # official.click_expression('expression_keyboard')
        # official.page_should_not_contain_sendfail_element()
        # official.page_should_contain_text('[微笑1]')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0328(self):
        """公众号会话页面，发送表情+信息"""
        official = OfficialAccountPage()
        official.click_officel_account()
        time.sleep(2)
        official.input_message('good news')
        # official.click_expression()
        # official.click_expression('[微笑1]')
        time.sleep(2)
        official.click_send_button()
        time.sleep(1)
        # official.click_expression('expression_keyboard')
        official.page_should_not_contain_sendfail_element()
        official.page_should_contain_text('good news')
        # official.page_should_contain_text('[微笑1]')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0329(self):
        """公众号会话页面，发送长信息"""
        official = OfficialAccountPage()
        official.click_officel_account()
        time.sleep(2)
        official.click_input_box()
        mesaage = str('good news'*10)
        official.input_message([mesaage])
        official.click_send_button()
        official.page_should_not_contain_sendfail_element()
        official.page_should_contain_text(mesaage)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0330(self):
        """公众号会话页面发送链接消息"""
        official = OfficialAccountPage()
        official.click_officel_account()
        time.sleep(2)
        official.click_input_box()
        mesaage = 'www.baidu.com'
        official.input_message(mesaage)
        official.click_send_button()
        official.page_should_not_contain_sendfail_element()
        official.page_should_contain_text(mesaage)
        official.click_baidu_button()
        time.sleep(8)
        if official.is_text_present('权限'):
            official.click_always_allowed()
        official.page_should_contain_text("百度一下")

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0331(self):
        """公众号会话页面网络异常情况下发送消息"""
        conts_page = ContactsPage()
        official = OfficialAccountPage()
        official.click_officel_account()
        # 断网发送失败
        conts_page.set_network_status(0)
        time.sleep(2)
        official.click_input_box()
        official.input_message()
        official.click_send_button()
        time.sleep(1)
        official.page_should_contain_sendfail_element()
        # 恢复网络,重发成功
        conts_page.set_network_status(6)
        time.sleep(5)
        official.click_repeat_button()
        official.click_sure_button()
        time.sleep(2)
        official.page_should_not_contain_sendfail_element()

    @staticmethod
    def tearDown_test_contacts_0331():
        # 初始化,恢复网络
        conts_page = ContactsPage()
        conts_page.set_network_status(6)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0332(self):
        """公众号会话页面右上角设置按钮"""
        official = OfficialAccountPage()
        official.click_officel_account()
        official.click_setting_button()
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
        time.sleep(2)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0334(self):
        """公众号详情-置顶公众号"""
        official = OfficialAccountPage()
        official.click_officel_account()
        time.sleep(1)
        account_name = official.get_account_title()
        official.click_setting_button()
        time.sleep(1)
        # 点击置顶公众号
        official_detail = OfficialAccountDetailPage()
        official_detail.click_to_be_top()
        official.click_back_by_android(2)
        time.sleep(2)
        top_name = official.get_first_account()
        # 判断是否置顶
        time.sleep(1)
        self.assertEqual(account_name, top_name)

    @staticmethod
    def tearDown_test_contacts_quxinli_0334():
        official = OfficialAccountPage()
        # 返回公众号详情页面,取消置顶
        official.click_officel_account()
        official.click_setting_button()
        OfficialAccountDetailPage().click_to_be_top()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_quxinli_0335(self):
        """公众号详情-查看历史资讯"""
        official = OfficialAccountPage()
        official.click_officel_account()
        time.sleep(1)
        official.click_setting_button()
        time.sleep(1)
        official_detail = OfficialAccountDetailPage()
        official_detail.click_read_old_message()
        official_detail.wait_for_page_load()
        if official_detail.is_contain_old_mes():
            official_detail.page_contain_time()
        else:
            official_detail.page_should_contain_text('无历史推送资讯')


if __name__ == '__main__':
    unittest.main()
