import time

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.SelectHeContacts import SelectHeContactsPage
from pages.contacts.EditContactPage import EditContactPage
from pages.workbench.enterprise_contacts.EnterpriseContacts import EnterpriseContactsPage
from pages.workbench.organization.OrganizationStructure import OrganizationStructurePage
from preconditions.BasePreconditions import LoginPreconditions
from preconditions.BasePreconditions import WorkbenchPreconditions

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    'Android-移动2': 'M960BDQN229CK_20',
    'Android-XX': ''  # 用来发短信
}


class Preconditions(WorkbenchPreconditions):
    """
    分解前置条件
    """
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
            Preconditions.make_already_in_message_page(reset=False)
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
    def activate_app(app_id=None):
        """激活APP"""
        if not app_id:
            app_id = current_mobile().driver.desired_capabilities['appPackage']
        current_mobile().driver.activate_app(app_id)

    @staticmethod
    def create_contacts_if_not_exits(name, number):
        """
        不存在就导入联系人数据
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
            Preconditions.make_already_in_message_page(reset=False)
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
    def create_he_contacts(names):
        """选择手机联系人----创建为团队联系人"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.open_workbench_page()
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        wbp.click_organization()
        osp = OrganizationStructurePage()
        n = 1
        # 解决工作台不稳定问题
        while not osp.page_should_contain_text2("添加联系人"):
            osp.click_back()
            wbp.wait_for_workbench_page_load()
            wbp.click_organization()
            n += 1
            if n > 20:
                break
        time.sleep(3)
        for name in names:
            if not osp.is_exist_specify_element_by_name(name):
                osp.click_specify_element_by_name("添加联系人")
                time.sleep(3)
                osp.click_specify_element_by_name("从手机通讯录添加")
                slc = SelectLocalContactsPage()
                # 等待选择联系人页面加载
                slc.wait_for_page_load()
                slc.selecting_local_contacts_by_name(name)
                slc.click_sure()
                time.sleep(2)
                osp.click_back()
        osp.click_back()
        wbp.wait_for_workbench_page_load()
        mp.open_message_page()
        mp.wait_for_page_load()

    @staticmethod
    def create_he_contacts2(contacts):
        """手动输入联系人----创建为团队联系人"""
        mp = MessagePage()
        mp.wait_for_page_load()
        mp.open_workbench_page()
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        wbp.click_organization()
        osp = OrganizationStructurePage()
        n = 1
        # 解决工作台不稳定问题
        while not osp.page_should_contain_text2("添加联系人"):
            osp.click_back()
            wbp.wait_for_workbench_page_load()
            wbp.click_organization()
            n += 1
            if n > 20:
                break
        time.sleep(3)
        osp.click_specify_element_by_name2("添加联系人")
        time.sleep(2)
        for name, number in contacts:
            osp.click_specify_element_by_name2("手动输入添加")
            osp.input_contacts_name(name)
            osp.input_contacts_number(number)
            osp.click_specify_element_by_name2("完成")
            time.sleep(3)
            if osp.is_text_present("手动输入添加"):
                continue
            else:
                osp.click_back_by_android()
        # 关闭
        osp.click_close()
        wbp.wait_for_workbench_page_load()
        mp.open_message_page()
        mp.wait_for_page_load()

    @staticmethod
    def create_sub_department_by_name(departmentName,name):
        """从消息列表开始创建子部门并添加一个部门成员"""
        WorkbenchPreconditions.enter_organization_page()
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        if osp.is_element_present_by_name(departmentName):
            time.sleep(2)
        else:
            osp.click_specify_element_by_name("添加子部门")
            osp.wait_for_sub_department_page_load()
            osp.input_sub_department_name(departmentName)
            osp.click_specify_element_by_name("完成")
            time.sleep(2)
        osp.click_specify_element_by_name("测试部门1")
        time.sleep(2)
        if osp.is_element_present_by_name(name):
            time.sleep(2)
        else:
            osp.click_specify_element_by_name("添加联系人")
            time.sleep(1)
            osp.click_specify_element_by_name("从手机通讯录添加")
            time.sleep(2)
            sc = SelectContactsPage()
            slc = SelectLocalContactsPage()
            # 选择联系人
            # names=slc.get_contacts_name_list()
            # time.sleep(2)
            sc.click_one_contact(name)
            # sc.click_one_contact(name)
            # sc.click_one_contact(name)
            # slc.click_one_contact("飞信电话")
            slc.click_sure()
            # if not slc.is_toast_exist("操作成功"):
            #     raise AssertionError("操作不成功")
        time.sleep(1)
        # 关闭
        osp.click_close()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        time.sleep(3)
        workbench.open_message_page()


class GroupcontactsSelectPage(TestCase):
    """模块:通讯录--企业联系人选择器"""

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
        """确保每个用例执行前在选择团队联系人页面"""
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        MessagePage().wait_for_page_load()
        MessagePage().click_add_icon()
        MessagePage().click_new_message()
        time.sleep(2)
        SelectContactsPage().click_group_contact()
        time.sleep(3)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0732(self):
        """顶部标题为：选择联系人"""
        select_group_contact=SelectHeContactsPage()
        title=select_group_contact.get_element_text(locator='选择联系人')
        self.assertEqual(title,'选择联系人')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0769(self):
        """搜索框默认提示语修改为：搜索或输入手机号"""
        select_group_contact=SelectHeContactsPage()
        title=select_group_contact.get_element_text(locator='搜索或输入手机号')
        self.assertEqual(title,'搜索或输入手机号')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0770(self):
        """点击搜索框，光标在搜索框时自动弹出键盘，点击其他区域后，键盘自动收起"""
        select_group_contact=SelectHeContactsPage()
        #点击搜索框,键盘弹出
        select_group_contact.click_input_box()
        select_group_contact.is_keyboard_shown()

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0771(self):
        """进入搜索状态，搜索框默认提示语“搜索”[搜索框文本应该为:搜索或输入手机号]"""
        select_group_contact=SelectHeContactsPage()
        #点击搜索框,键盘弹出
        select_group_contact.click_input_box()
        select_group_contact.input_search_keywords('大佬')
        time.sleep(2)
        select_group_contact.clear_input_box()
        text=select_group_contact.get_element_text('搜索或输入手机号')
        self.assertEqual(text,'搜索或输入手机号')

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0772(self):
        """输入框为空时，右侧不显示 一键消除 X 按钮"""
        select_group_contact=SelectHeContactsPage()
        #点击搜索框,键盘弹出
        select_group_contact.click_input_box()
        self.assertFalse(select_group_contact.is_element_present(locator='清空搜索框'))

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0773(self):
        """输入框有内容时，右侧显示 一键消除 X 按钮，点击X可清空内容"""
        select_group_contact=SelectHeContactsPage()
        #点击搜索框,键盘弹出
        select_group_contact.click_input_box()
        text='测试'
        select_group_contact.input_search_keywords(text)
        self.assertTrue(select_group_contact.is_element_present(locator='清空搜索框'))
        time.sleep(2)
        select_group_contact.clear_input_box()
        text2 = select_group_contact.get_element_text('搜索或输入手机号')
        self.assertNotEqual(text, text2)

    @tags('ALL', 'CONTACTS', 'CMCC')
    def test_contacts_chenjixiang_0724(self):
        """测试搜索输入框的X按钮是否可以清空内容"""
        select_group_contact=SelectHeContactsPage()
        #点击搜索框,键盘弹出
        select_group_contact.click_input_box()
        text='测试'
        select_group_contact.input_search_keywords(text)
        time.sleep(2)
        select_group_contact.clear_input_box()
        text2 = select_group_contact.get_element_text('搜索或输入手机号')
        self.assertNotEqual(text, text2)


class MygroupSearchPage(TestCase):
    """模块:通讯录-我的团队-搜索"""
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
        """确保每个用例执行前在我的团队首页"""
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        # 切换联系tab和工作台tab（兼容团队无法及时刷新问题）
        MessagePage().click_contacts()
        time.sleep(2)
        MessagePage().click_workbench()
        time.sleep(3)
        MessagePage().click_contacts()
        time.sleep(2)
        ContactsPage().select_group_by_name('ateam7272')

    @staticmethod
    def setUp_test_contacts_quxinli_0040():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0040(self):
        """用户未加入任何企业"""
        # 备注：无法构造 用户未加入任何企业 数据。且仅支持运行一次。
        contact = ContactsPage()
        contact.click_contact_all_team()
        time.sleep(1)
        try:
            group_names = contact.get_cur_group_name()
            exist = len(group_names) == 0
            self.assertEqual(exist, False)
        except:
            pass

    @staticmethod
    def setUp_test_contacts_quxinli_0041():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0041(self):
        """用户只在一个企业下，且在企业子一层级"""
        contact = ContactsPage()
        contact.click_contact_all_team()
        time.sleep(1)
        group_names = contact.get_all_group_name2()
        result = contact.is_contain_group_name(group_names, "ateam7272")
        self.assertTrue(result)

    @staticmethod
    def setUp_test_contacts_quxinli_0042():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0042(self):
        """用户只在一个企业下，且在企业子层级"""
        contact = ContactsPage()
        contact.click_contact_all_team()
        time.sleep(1)
        group_names = contact.get_all_group_name2()
        result = contact.is_contain_group_name(group_names, "ateam7272")
        self.assertTrue(result)
        result = contact.is_contain_group_name(group_names, "bm0")
        self.assertTrue(result)

    @staticmethod
    def setUp_test_contacts_quxinli_0043():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0043(self):
        """用户只在一个企业下，且同时在企业子一层级和子层级"""
        contact = ContactsPage()
        contact.click_contact_all_team()
        time.sleep(1)
        group_names = contact.get_all_group_name2()
        result = contact.is_contain_group_name(group_names, "ateam7272")
        self.assertTrue(result)
        result = contact.is_contain_group_name(group_names, "bm0")
        self.assertTrue(result)

    @staticmethod
    def setUp_test_contacts_quxinli_0044():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0044(self):
        """用户只在一个企业下，且同时在两个子层级"""
        contact = ContactsPage()
        contact.click_contact_all_team()
        time.sleep(1)
        group_names = contact.get_all_group_name2()
        result = contact.is_contain_group_name(group_names, "ateam7272")
        self.assertTrue(result)
        result = contact.is_contain_group_name(group_names, "bm0")
        self.assertTrue(result)

    @staticmethod
    def setUp_test_contacts_quxinli_0045():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0045(self):
        """用户在多个企业下"""
        contact = ContactsPage()
        contact.click_contact_all_team()
        time.sleep(1)
        group_names = contact.get_all_group_name2()
        self.assertTrue(len(group_names) > 1)

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0048(self):
        """子一层级下已保存到本地的RCS用户Profile(点击我的团队的企业下任一保存在本地的RCS联系人)"""
        group_contact = EnterpriseContactsPage()
        group_contact.wait_for_page_load()
        group_contact.click_contacts_by_name('香港大佬')
        detailpage = ContactDetailsPage()
        detailpage.wait_for_page_load()
        # 验证页面元素显示
        self.assertTrue(detailpage.is_exists_contacts_name())
        self.assertTrue(detailpage.is_exists_contacts_number())
        self.assertTrue(detailpage.is_exists_contacts_image())
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

        # 点击电话 拨打电话
        detailpage.click_call_icon()
        time.sleep(3)
        detailpage.cancel_call2()
        time.sleep(3)

        # 点击语音,挂断语音电话
        detailpage.click_voice_call_icon()
        time.sleep(2)
        if detailpage.is_text_present('暂不开启'):
            detailpage.click_text('暂不开启')
        time.sleep(2)
        detailpage.click_end_call()
        time.sleep(3)

        # 点击视频通话
        detailpage.click_video_call_icon()
        time.sleep(2)
        if detailpage.is_text_present('暂不开启'):
            detailpage.click_text('暂不开启')
        time.sleep(2)
        detailpage.end_video_call()
        time.sleep(3)

        # 点击飞信电话
        detailpage.click_hefeixin_call_menu()
        time.sleep(2)
        if detailpage.is_text_present('我知道了'):
            detailpage.click_text('我知道了')
        time.sleep(3)
        if detailpage.is_text_present('暂不开启'):
            detailpage.click_text('暂不开启')
        time.sleep(5)
        detailpage.cancel_hefeixin_call()
        time.sleep(2)

        # 分享名片按钮可点击
        detailpage.click_share_business_card()
        SelectContactsPage().select_local_contacts()
        SelectContactsPage().click_one_contact('大佬1')
        time.sleep(2)
        SelectContactsPage().click_share_card()
        detailpage.page_should_contain_text('已发送')

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0049(self):
        """点击搜索结果已保存到本地的本机用户进入联系人详情页"""
        group_contact=EnterpriseContactsPage()
        group_contact.wait_for_page_load()
        group_contact.click_search_box()
        time.sleep(2)
        #搜索框为空 无反应
        self.assertFalse(group_contact.is_exists_contacts_search_result())
        #搜索内容为空格
        group_contact.input_search_message(' ')
        time.sleep(2)
        self.assertFalse(group_contact.is_exists_contacts_search_result())
        #输入陈丹丹搜索
        group_contact.input_search_message('陈丹丹')
        time.sleep(2)
        group_contact.is_search_contacts_name_full_match('陈丹丹')
        #输入Alice
        group_contact.input_search_message('alice')
        time.sleep(2)
        group_contact.is_search_contacts_name_full_match('alice')
        #输入号码
        group_contact.input_search_message('13800137004')
        time.sleep(3)
        group_contact.is_search_contacts_number_full_match('13800137004')
        #输入号码
        group_contact.input_search_message('188262*')
        time.sleep(2)
        self.assertFalse(group_contact.is_exists_contacts_name())

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0054(self):
        """我的团队-非法字符搜索"""
        group_contact=EnterpriseContactsPage()
        group_contact.wait_for_page_load()
        group_contact.click_search_box()
        time.sleep(2)
        #输入非法字符搜索
        group_contact.input_search_message('#*')
        time.sleep(3)
        group_contact.is_search_contacts_name_full_match('#*')
        time.sleep(1)
        #单个输入特殊字符
        group_contact.input_search_message('#')
        time.sleep(3)
        group_contact.is_search_contacts_name_match('#')
        time.sleep(1)
        #特殊字符+数字
        group_contact.input_search_message('#1')
        time.sleep(3)
        group_contact.is_search_contacts_name_match('#1')
        time.sleep(1)

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0056(self):
        """搜索我的团队联系人结果展示"""
        group_contact=EnterpriseContactsPage()
        group_contact.wait_for_page_load()
        group_contact.click_search_box()
        time.sleep(2)
        #输入非法字符搜索
        group_contact.input_search_message('陈丹丹')
        time.sleep(3)
        self.assertTrue(group_contact.is_exists_contacts_name())
        self.assertTrue(group_contact.is_exists_contacts_number())
        self.assertTrue(group_contact.is_exists_contacts_image())
        group_contact.is_exists_contacts_department()

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0063(self):
        """点击搜索结果已保存到本地的RCS用户进入Profile页(进入联系页面-我的团队-任一企业，点击搜索框并输入关键字)"""
        group_contact=EnterpriseContactsPage()
        group_contact.wait_for_page_load()
        group_contact.click_search_box()
        time.sleep(2)
        # 选择已保存在本地的rcs用户
        group_contact.input_search_message('香港大佬')
        time.sleep(3)
        group_contact.click_contacts_by_name('香港大佬')
        detailpage = ContactDetailsPage()
        detailpage.wait_for_page_load()
        # 验证页面元素显示
        self.assertTrue(detailpage.is_exists_contacts_name())
        self.assertTrue(detailpage.is_exists_contacts_number())
        self.assertTrue(detailpage.is_exists_contacts_image())
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

        # 点击电话 拨打电话
        detailpage.click_call_icon()
        time.sleep(3)
        detailpage.cancel_call2()
        time.sleep(3)

        # 点击语音,挂断语音电话
        detailpage.click_voice_call_icon()
        time.sleep(2)
        if detailpage.is_text_present('暂不开启'):
            detailpage.click_text('暂不开启')
        time.sleep(2)
        detailpage.click_end_call()
        time.sleep(3)

        # 点击视频通话
        detailpage.click_video_call_icon()
        time.sleep(2)
        if detailpage.is_text_present('暂不开启'):
            detailpage.click_text('暂不开启')
        time.sleep(2)
        detailpage.end_video_call()
        time.sleep(3)

        # 点击飞信电话
        detailpage.click_hefeixin_call_menu()
        time.sleep(2)
        if detailpage.is_text_present('我知道了'):
            detailpage.click_text('我知道了')
        time.sleep(3)
        if detailpage.is_text_present('暂不开启'):
            detailpage.click_text('暂不开启')
        time.sleep(5)
        detailpage.cancel_hefeixin_call()
        time.sleep(2)

        # 分享名片按钮可点击
        detailpage.click_share_business_card()
        SelectContactsPage().select_local_contacts()
        SelectContactsPage().click_one_contact('大佬1')
        time.sleep(2)
        SelectContactsPage().click_share_card()
        detailpage.page_should_contain_text('已发送')

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0050(self):
        """我的团队-中文模糊搜索"""
        group_contact=EnterpriseContactsPage()
        group_contact.wait_for_page_load()
        group_contact.click_search_box()
        time.sleep(2)
        #输入陈搜索
        group_contact.input_search_message('陈')
        time.sleep(3)
        group_contact.is_search_contacts_name_match('陈')
        time.sleep(1)

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0051(self):
        """我的团队-数字模糊搜索"""
        group_contact=EnterpriseContactsPage()
        group_contact.wait_for_page_load()
        group_contact.click_search_box()
        time.sleep(2)
        #输入数字搜索
        group_contact.input_search_message('1380')
        time.sleep(3)
        group_contact.is_search_contacts_number_match('1380')
        time.sleep(1)
        # 输入数字精确搜索
        group_contact.input_search_message('13800137004')
        time.sleep(3)
        group_contact.is_search_contacts_number_full_match('13800137004')
        time.sleep(1)
        # 输入香港搜索
        group_contact.input_search_message('67656003')
        time.sleep(3)
        group_contact.is_search_contacts_number_full_match('67656003')
        time.sleep(1)

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0052(self):
        """我的团队-名字搜索"""
        group_contact = EnterpriseContactsPage()
        group_contact.wait_for_page_load()
        # group_contact.click_search_box()
        # time.sleep(2)
        contact_name = "大佬3"
        shc = SelectHeContactsDetailPage()
        shc.selecting_he_contacts_by_name(contact_name)
        # 判定点
        # 进入个人详情页 判断页面包含的元素
        detailpage = ContactDetailsPage()
        # 名字
        detailpage.is_exists_contacts_name()
        # 号码
        detailpage.is_exists_contacts_number()
        # detailpage.page_should_contain_text('B')
        if detailpage.is_text_present("公司"):
            detailpage.page_should_contain_text('公司')
        if detailpage.is_text_present("职位"):
            detailpage.page_should_contain_text('职位')
        if detailpage.is_text_present("邮箱"):
            detailpage.page_should_contain_text('邮箱')
        # 消息、电话、语音视频、视频电话、副号拨打、飞信电话置灰
        detailpage.page_should_contain_text('消息')
        detailpage.page_should_contain_text('电话')
        detailpage.page_should_contain_text('语音通话')
        detailpage.page_should_contain_text('视频通话')
        detailpage.page_should_contain_text('飞信电话')
        #detailpage.page_should_contain_text('保存到通讯录')
        detailpage.page_should_contain_text('邀请使用')
        time.sleep(2)
        # "点击头像显示大图"--新版本无法查看大图
        # detailpage.click_avatar()
        # detailpage.is_exists_big_avatar()
        # detailpage.click_big_avatar()
        # time.sleep(2)

        # """点击消息按钮进入会话界面
        detailpage.message_btn_is_clickable()

        # """点击电话弹出拨打弹出
        detailpage.call_btn_is_clickable()

        # """点击语音通话弹出语音会话弹窗
        detailpage.voice_btn_is_clickable()

        # """点击视频通话弹窗视频会话弹窗
        detailpage.video_call_btn_is_clickable()

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0053(self):
        """我的团队-英文模糊搜索"""
        group_contact=EnterpriseContactsPage()
        group_contact.wait_for_page_load()
        group_contact.click_search_box()
        time.sleep(2)
        #输入alice搜索
        group_contact.input_search_message('alice')
        time.sleep(3)
        group_contact.is_search_contacts_name_full_match('alice')
        time.sleep(1)
        #输入alice搜索
        group_contact.input_search_message('A')
        time.sleep(3)
        group_contact.is_search_contacts_name_match('a')
        time.sleep(1)

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0064(self):
        group_contact = EnterpriseContactsPage()
        group_contact.wait_for_page_load()
        group_contact.click_search_box()
        contact_name = "大佬3"
        group_contact.input_search_message(contact_name)
        time.sleep(3)
        shc = SelectHeContactsDetailPage()
        shc.selecting_he_contacts_by_name(contact_name)
        # 判定点
        # 进入个人详情页 判断页面包含的元素
        detailpage = ContactDetailsPage()
        # 名字
        detailpage.is_exists_contacts_name()
        # 号码
        detailpage.is_exists_contacts_number()
        # detailpage.page_should_contain_text('B')
        if detailpage.is_text_present("公司"):
            detailpage.page_should_contain_text('公司')
        if detailpage.is_text_present("职位"):
            detailpage.page_should_contain_text('职位')
        if detailpage.is_text_present("邮箱"):
            detailpage.page_should_contain_text('邮箱')
        # 消息、电话、语音视频、视频电话、副号拨打、飞信电话置灰，不可点击
        detailpage.page_should_contain_text('消息')
        detailpage.page_should_contain_text('电话')
        detailpage.page_should_contain_text('语音通话')
        detailpage.page_should_contain_text('视频通话')
        detailpage.page_should_contain_text('飞信电话')
        detailpage.page_should_contain_text('分享名片')
        detailpage.page_should_contain_text('邀请使用')
        time.sleep(2)
        # """点击头像显示大图-无头像联系人无法点击
        # detailpage.click_avatar()
        # detailpage.is_exists_big_avatar()
        # detailpage.click_big_avatar()
        # time.sleep(2)
        # """点击消息按钮进入会话界面
        detailpage.message_btn_is_clickable()
        # """点击电话弹出拨打弹出
        detailpage.call_btn_is_clickable()
        # """点击语音通话弹出语音会话弹窗
        detailpage.voice_btn_is_clickable()
        # """点击视频通话弹窗视频会话弹窗
        detailpage.video_call_btn_is_clickable()

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0066(self):
        group_contact = EnterpriseContactsPage()
        group_contact.wait_for_page_load()
        group_contact.click_search_box()
        contact_name = "admin"
        group_contact.input_search_message(contact_name)
        time.sleep(3)
        shc = SelectHeContactsDetailPage()
        shc.selecting_he_contacts_by_name(contact_name)
        # 判定点
        # 进入个人详情页 判断页面包含的元素
        detailpage = ContactDetailsPage()
        # 名字
        detailpage.is_exists_contacts_name()
        # 号码
        detailpage.is_exists_contacts_number()
        # detailpage.page_should_contain_text('B')
        if detailpage.is_text_present("公司"):
            detailpage.page_should_contain_text('公司')
        if detailpage.is_text_present("职位"):
            detailpage.page_should_contain_text('职位')
        if detailpage.is_text_present("邮箱"):
            detailpage.page_should_contain_text('邮箱')
        # 消息、电话、语音视频、视频电话、副号拨打、飞信电话置灰，不可点击
        detailpage.page_should_contain_text('消息')
        detailpage.page_should_contain_text('电话')
        detailpage.page_should_contain_text('语音通话')
        detailpage.page_should_contain_text('视频通话')
        detailpage.page_should_contain_text('飞信电话')
        detailpage.page_should_contain_text('保存到通讯录')
        time.sleep(2)
        # """点击头像显示大图
        # detailpage.click_avatar()
        # detailpage.is_exists_big_avatar()
        # detailpage.click_big_avatar()
        # time.sleep(2)
        # """点击消息按钮进入会话界面
        detailpage.message_btn_is_clickable()
        # """点击电话弹出拨打弹出
        detailpage.call_btn_is_clickable()
        # """点击语音通话弹出语音会话弹窗
        detailpage.voice_btn_is_clickable()
        # """点击视频通话弹窗视频会话弹窗
        detailpage.video_call_btn_is_clickable()

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0067(self):
        group_contact = EnterpriseContactsPage()
        group_contact.wait_for_page_load()
        group_contact.click_search_box()
        contact_name = "哈 马上"
        group_contact.input_search_message(contact_name)
        time.sleep(3)
        shc = SelectHeContactsDetailPage()
        shc.selecting_he_contacts_by_name(contact_name)
        # 判定点
        # 进入个人详情页 判断页面包含的元素
        detailpage = ContactDetailsPage()
        # 名字
        detailpage.is_exists_contacts_name()
        # 号码
        detailpage.is_exists_contacts_number()
        # detailpage.page_should_contain_text('B')
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
        detailpage.page_should_contain_text('保存到通讯录')
        detailpage.page_should_contain_text('邀请使用')
        time.sleep(2)
        # """点击头像显示大图
        # detailpage.click_avatar()
        # detailpage.is_exists_big_avatar()
        # 备注 无头像，没有大图
        # detailpage.click_big_avatar()
        time.sleep(2)
        # """点击消息按钮进入会话界面
        detailpage.message_btn_is_clickable()
        # """点击电话弹出拨打弹出
        detailpage.call_btn_is_clickable()
        # """点击语音通话弹出语音会话弹窗
        detailpage.voice_btn_is_clickable()
        # """点击视频通话弹窗视频会话弹窗
        detailpage.video_call_btn_is_clickable()

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0068(self):
        group_contact = EnterpriseContactsPage()
        group_contact.wait_for_page_load()
        group_contact.click_search_box()
        # 本机号码
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_contact.input_search_message(phone_number)
        time.sleep(3)
        shc = SelectHeContactsDetailPage()
        shc.selecting_he_contacts_by_number(phone_number)
        # 判定点
        # 进入个人详情页 判断页面包含的元素
        detailpage = ContactDetailsPage()
        # 名字
        detailpage.is_exists_contacts_name()
        # 号码
        detailpage.is_exists_contacts_number()
        if detailpage.is_text_present("公司"):
            detailpage.page_should_contain_text('公司')
        if detailpage.is_text_present("职位"):
            detailpage.page_should_contain_text('职位')
        if detailpage.is_text_present("邮箱"):
            detailpage.page_should_contain_text('邮箱')
        # 消息、电话、语音视频、视频电话、副号拨打、飞信电话置灰，不可点击
        detailpage.page_should_contain_text('消息')
        detailpage.page_should_contain_text('电话')
        detailpage.page_should_contain_text('语音通话')
        detailpage.page_should_contain_text('视频通话')
        detailpage.page_should_contain_text('飞信电话')
        detailpage.page_should_contain_text('保存到通讯录')
        time.sleep(2)
        detailpage.message_btn_is_clickable()
        detailpage.call_btn_is_clickable()
        detailpage.voice_btn_is_clickable()
        detailpage.video_call_btn_is_clickable()
        detailpage.hefeixin_call_btn_is_clickable()
        time.sleep(2)
        # """点击头像显示大图
        # detailpage.click_avatar()
        # detailpage.is_exists_big_avatar()
        # 备注 无头像，没有大图
        # detailpage.click_big_avatar()
        time.sleep(2)
        # """点击消息按钮进入会话界面
        detailpage.message_btn_is_clickable()
        # """点击电话弹出拨打弹出
        detailpage.call_btn_is_clickable()
        # """点击语音通话弹出语音会话弹窗
        detailpage.voice_btn_is_clickable()
        # """点击视频通话弹窗视频会话弹窗
        detailpage.video_call_btn_is_clickable()

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0093(self):
        group_contact = EnterpriseContactsPage()
        group_contact.click_sub_level_department_by_name('bm0')
        group_contact.click_search_box()
        time.sleep(2)
        # 选择已保存在本地的非rcs用户
        group_contact.input_search_message('b测算')
        group_contact.click_contacts_by_name('b测算')
        detailpage = ContactDetailsPage()
        detailpage.wait_for_page_load()
        # 验证页面元素显示
        self.assertTrue(detailpage.is_exists_contacts_name())
        self.assertTrue(detailpage.is_exists_contacts_number())
        self.assertTrue(detailpage.is_exists_contacts_image())
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
        detailpage.page_should_contain_text('邀请使用')
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

        # 点击电话 拨打电话
        detailpage.click_call_icon()
        time.sleep(3)
        detailpage.cancel_call2()
        time.sleep(6)

        # 点击语音,挂断语音电话
        detailpage.click_voice_call_icon()
        time.sleep(2)
        if detailpage.is_text_present('暂不开启'):
            detailpage.click_text('暂不开启')
        time.sleep(2)
        detailpage.end_voice_call()
        time.sleep(6)

        # 点击视频通话
        detailpage.click_video_call_icon()
        time.sleep(2)
        if detailpage.is_text_present('暂不开启'):
            detailpage.click_text('暂不开启')
        time.sleep(2)
        detailpage.end_video_call()
        time.sleep(6)

        # 点击飞信电话
        detailpage.click_hefeixin_call_menu()
        time.sleep(2)
        if detailpage.is_text_present('我知道了'):
            detailpage.click_text('我知道了')
        time.sleep(3)
        if detailpage.is_text_present('暂不开启'):
            detailpage.click_text('暂不开启')
        time.sleep(5)
        detailpage.cancel_hefeixin_call()
        time.sleep(3)

        # 分享名片按钮可点击
        if detailpage.is_text_present("分享名片"):
            detailpage.click_share_business_card()
            SelectContactsPage().select_local_contacts()
            SelectContactsPage().click_one_contact('大佬1')
            time.sleep(2)
            SelectContactsPage().click_share_card()
            detailpage.page_should_contain_text('已发送')

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0094(self):
        group_contact = EnterpriseContactsPage()
        group_contact.click_sub_level_department_by_name('bm0')
        time.sleep(1)
        # 标题栏三点
        # group_contact.click_three_points_icon2()
        # time.sleep(1)
        # contacts = ContactsPage()
        # contacts.click_text("团队管理")
        # time.sleep(1)
        # 进入部门 bm0
        # group_contact.click_sub_level_department_by_name('bm0') 界面元素修改了
        # time.sleep(1)
        # group_contact.add_phone_number_to_department('bm0')
        # time.sleep(1)
        # 进入部门 bm0
        # group_contact.click_sub_level_department_by_name('bm0')
        # 本机用户
        group_contact.click_search_box()
        time.sleep(2)
        group_contact.input_search_message('本机测试')
        time.sleep(3)
        group_contact.click_contacts_by_name('本机测试')
        detailpage = ContactDetailsPage()
        detailpage.wait_for_page_load()
        # 验证页面元素显示
        self.assertTrue(detailpage.is_exists_contacts_name())
        self.assertTrue(detailpage.is_exists_contacts_number())
        self.assertTrue(detailpage.is_exists_contacts_image())
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
        # detailpage.page_should_contain_text('分享名片')
        time.sleep(2)
        # 消息、电话、语音视频、视频电话、副号拨打、飞信电话置灰，不可点击
        detailpage.message_btn_is_clickable()
        detailpage.call_btn_is_clickable()
        detailpage.voice_btn_is_clickable()
        detailpage.video_call_btn_is_clickable()
        detailpage.hefeixin_call_btn_is_clickable()

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0095(self):
        group_contact = EnterpriseContactsPage()
        group_contact.click_sub_level_department_by_name('bm0')
        time.sleep(1)
        group_contact.click_search_box()
        time.sleep(1)
        contact_name = "本机测试"
        group_contact.input_search_message(contact_name)
        time.sleep(3)
        group_contact.click_contacts_by_name(contact_name)
        time.sleep(1)
        detailpage = ContactDetailsPage()
        detailpage.wait_for_page_load()
        # 验证页面元素显示
        self.assertTrue(detailpage.is_exists_contacts_name())
        self.assertTrue(detailpage.is_exists_contacts_number())
        self.assertTrue(detailpage.is_exists_contacts_image())
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
        detailpage.page_should_contain_text('保存到通讯录')

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0096(self):
        group_contact = EnterpriseContactsPage()
        group_contact.click_search_box()
        time.sleep(1)
        contact_name = "b测算"
        group_contact.input_search_message(contact_name)
        time.sleep(2)
        group_contact.click_contacts_by_name(contact_name)
        detailpage = ContactDetailsPage()
        detailpage.wait_for_page_load()
        # 验证页面元素显示
        self.assertTrue(detailpage.is_exists_contacts_name())
        self.assertTrue(detailpage.is_exists_contacts_number())
        self.assertTrue(detailpage.is_exists_contacts_image())
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
        detailpage.page_should_contain_text('保存到通讯录')
        detailpage.page_should_contain_text('邀请使用')
        time.sleep(2)
        # 点击头像查看大图
        # detailpage.click_avatar()
        # time.sleep(4)
        # 备注 无头像，没有大图
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

        # 点击电话 拨打电话
        detailpage.click_call_icon()
        time.sleep(3)
        detailpage.cancel_call2()
        time.sleep(3)

        # 点击语音,挂断语音电话
        detailpage.click_voice_call_icon()
        time.sleep(2)
        if detailpage.is_text_present('暂不开启'):
            detailpage.click_text('暂不开启')
        time.sleep(2)
        detailpage.end_voice_call()
        time.sleep(3)

        # 点击视频通话
        detailpage.click_video_call_icon()
        time.sleep(2)
        if detailpage.is_text_present('暂不开启'):
            detailpage.click_text('暂不开启')
        time.sleep(2)
        detailpage.end_video_call()
        time.sleep(3)

        # 点击飞信电话
        detailpage.click_hefeixin_call_menu()
        time.sleep(2)
        if detailpage.is_text_present('我知道了'):
            detailpage.click_text('我知道了')
        time.sleep(3)
        if detailpage.is_text_present('暂不开启'):
            detailpage.click_text('暂不开启')
        time.sleep(5)
        detailpage.cancel_hefeixin_call()
        time.sleep(2)

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0097(self):
        group_contact = EnterpriseContactsPage()
        group_contact.click_sub_level_department_by_name('bm0')
        time.sleep(1)
        # 标题栏三点
        # group_contact.click_three_points_icon()
        # time.sleep(1)
        # contacts = ContactsPage()
        # contacts.click_text("团队管理")
        # time.sleep(1)
        # # 进入部门 bm0
        # group_contact.click_sub_level_department_by_name('bm0')
        # time.sleep(1)
        # group_contact.add_phone_number_to_department('bm0')
        # time.sleep(1)
        # # 进入部门 bm0
        # group_contact.click_sub_level_department_by_name('bm0')
        # 本机用户
        group_contact.click_search_box()
        time.sleep(2)
        group_contact.input_search_message('本机测试')
        time.sleep(3)
        group_contact.click_contacts_by_name('本机测试')
        detailpage = ContactDetailsPage()
        detailpage.wait_for_page_load()
        # 验证页面元素显示
        self.assertTrue(detailpage.is_exists_contacts_name())
        self.assertTrue(detailpage.is_exists_contacts_number())
        self.assertTrue(detailpage.is_exists_contacts_image())
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
        # 消息、电话、语音视频、视频电话、副号拨打、飞信电话置灰，不可点击
        detailpage.message_btn_is_clickable()
        detailpage.call_btn_is_clickable()
        detailpage.voice_btn_is_clickable()
        detailpage.video_call_btn_is_clickable()
        detailpage.hefeixin_call_btn_is_clickable()

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0107(self):
        group_contact=EnterpriseContactsPage()
        group_contact.click_sub_level_department_by_name('测试部门1')
        group_contact.click_search_box()
        time.sleep(2)
        # 选择已保存在本地的rcs用户
        group_contact.input_search_message('测试号码')
        group_contact.click_contacts_by_name('测试号码')
        detailpage = ContactDetailsPage()
        detailpage.wait_for_page_load()
        # 验证页面元素显示
        self.assertTrue(detailpage.is_exists_contacts_name())
        self.assertTrue(detailpage.is_exists_contacts_number())
        self.assertTrue(detailpage.is_exists_contacts_image())
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

        # 点击电话 拨打电话
        detailpage.click_call_icon()
        time.sleep(3)
        detailpage.cancel_call2()
        time.sleep(3)

        # 点击语音,挂断语音电话
        detailpage.click_voice_call_icon()
        time.sleep(2)
        if detailpage.is_text_present('暂不开启'):
            detailpage.click_text('暂不开启')
        time.sleep(2)
        detailpage.click_end_call()
        time.sleep(3)

        # 点击视频通话
        detailpage.click_video_call_icon()
        time.sleep(2)
        if detailpage.is_text_present('暂不开启'):
            detailpage.click_text('暂不开启')
        time.sleep(2)
        detailpage.end_video_call()
        time.sleep(3)

        # 点击飞信电话
        detailpage.click_hefeixin_call_menu()
        time.sleep(2)
        if detailpage.is_text_present('我知道了'):
            detailpage.click_text('我知道了')
        time.sleep(3)
        if detailpage.is_text_present('暂不开启'):
            detailpage.click_text('暂不开启')
        time.sleep(5)
        detailpage.cancel_hefeixin_call()
        time.sleep(2)

        # 分享名片按钮可点击
        detailpage.click_share_business_card()
        SelectContactsPage().select_local_contacts()
        SelectContactsPage().click_one_contact('大佬1')
        time.sleep(2)
        SelectContactsPage().click_share_card()
        detailpage.page_should_contain_text('已发送')

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0108(self):
        group_contact = EnterpriseContactsPage()
        group_contact.click_sub_level_department_by_name('bm0')
        group_contact.click_search_box()
        time.sleep(2)
        # 选择已保存在本地的非rcs用户
        group_contact.input_search_message('b测算')
        time.sleep(3)
        group_contact.click_contacts_by_name('b测算')
        detailpage = ContactDetailsPage()
        detailpage.wait_for_page_load()
        # 验证页面元素显示
        self.assertTrue(detailpage.is_exists_contacts_name())
        self.assertTrue(detailpage.is_exists_contacts_number())
        self.assertTrue(detailpage.is_exists_contacts_image())
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
        # detailpage.page_should_contain_text('分享名片')
        # detailpage.page_should_contain_text('邀请使用')
        # 点击头像查看大图
        # detailpage.click_avatar()
        # time.sleep(4)
        # 备注 无头像，没有大图
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

        # 点击电话 拨打电话
        detailpage.click_call_icon()
        time.sleep(3)
        detailpage.cancel_call2()
        time.sleep(3)

        # 点击语音,挂断语音电话
        detailpage.click_voice_call_icon()
        time.sleep(2)
        if detailpage.is_text_present('暂不开启'):
            detailpage.click_text('暂不开启')
        time.sleep(2)
        detailpage.end_voice_call()
        time.sleep(3)

        # 点击视频通话
        detailpage.click_video_call_icon()
        time.sleep(2)
        if detailpage.is_text_present('暂不开启'):
            detailpage.click_text('暂不开启')
        time.sleep(2)
        detailpage.end_video_call()
        time.sleep(3)

        # 点击飞信电话
        detailpage.click_hefeixin_call_menu()
        time.sleep(2)
        if detailpage.is_text_present('我知道了'):
            detailpage.click_text('我知道了')
        time.sleep(3)
        if detailpage.is_text_present('暂不开启'):
            detailpage.click_text('暂不开启')
        time.sleep(5)
        detailpage.cancel_hefeixin_call()
        time.sleep(2)

        # 分享名片按钮可点击
        if detailpage.is_text_present("分享名片"):
            detailpage.click_share_business_card()
            SelectContactsPage().select_local_contacts()
            SelectContactsPage().click_one_contact('大佬1')
            time.sleep(2)
            SelectContactsPage().click_share_card()
            detailpage.page_should_contain_text('已发送')

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0109(self):
        group_contact = EnterpriseContactsPage()
        group_contact.click_sub_level_department_by_name('bm0')
        time.sleep(1)
        # # 标题栏三点
        # group_contact.click_three_points_icon()
        # time.sleep(1)
        # contacts = ContactsPage()
        # contacts.click_text("团队管理")
        # time.sleep(1)
        # # 再次进入部门 bm0
        # group_contact.click_sub_level_department_by_name('bm0')
        # time.sleep(1)
        # group_contact.add_phone_number_to_department('bm0')
        # time.sleep(1)
        # # 进入部门 bm0
        # group_contact.click_sub_level_department_by_name('bm0')
        # 本机用户
        group_contact.click_search_box()
        time.sleep(2)
        group_contact.input_search_message('本机测试')
        time.sleep(3)
        group_contact.click_contacts_by_name('本机测试')
        detailpage = ContactDetailsPage()
        detailpage.wait_for_page_load()
        # 确保本机用户已保存到本地
        if detailpage.is_exists_save_contacts_icon():
            detailpage.click_save_contacts_icon()
            detailpage = CreateContactPage()
            detailpage.wait_for_page_load()
            detailpage.save_contact()
            time.sleep(2)
        # 验证页面元素显示
        self.assertTrue(detailpage.is_exists_contacts_name())
        self.assertTrue(detailpage.is_exists_contacts_number())
        self.assertTrue(detailpage.is_exists_contacts_image())
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
        time.sleep(2)
        # 消息、电话、语音视频、视频电话、副号拨打、飞信电话置灰，不可点击
        detailpage.message_btn_is_clickable()
        detailpage.call_btn_is_clickable()
        detailpage.voice_btn_is_clickable()
        detailpage.video_call_btn_is_clickable()
        detailpage.hefeixin_call_btn_is_clickable()

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0110(self):
        group_contact = EnterpriseContactsPage()
        group_contact.click_sub_level_department_by_name('bm0')
        time.sleep(1)
        group_contact.click_search_box()
        time.sleep(2)
        # 未保存到本地的RCS用户
        group_contact.input_search_message('b测算')
        group_contact.click_contacts_by_name('b测算')
        detailpage = ContactDetailsPage()
        detailpage.wait_for_page_load()
        # 验证页面元素显示
        self.assertTrue(detailpage.is_exists_contacts_name())
        self.assertTrue(detailpage.is_exists_contacts_number())
        self.assertTrue(detailpage.is_exists_contacts_image())
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
        # detailpage.page_should_contain_text('保存到通讯录')
        # 点击头像查看大图
        # detailpage.click_avatar()
        # time.sleep(4)
        # 备注 无头像，没有大图
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
        # 点击电话 拨打电话
        detailpage.click_call_icon()
        time.sleep(3)
        detailpage.cancel_call2()
        time.sleep(3)

        # 点击语音,挂断语音电话
        detailpage.click_voice_call_icon()
        time.sleep(2)
        if detailpage.is_text_present('暂不开启'):
            detailpage.click_text('暂不开启')
        time.sleep(2)
        detailpage.end_voice_call()
        time.sleep(3)

        # 点击视频通话
        detailpage.click_video_call_icon()
        time.sleep(2)
        if detailpage.is_text_present('暂不开启'):
            detailpage.click_text('暂不开启')
        time.sleep(2)
        detailpage.end_video_call()
        time.sleep(3)

        # 点击飞信电话
        detailpage.click_hefeixin_call_menu()
        time.sleep(2)
        if detailpage.is_text_present('我知道了'):
            detailpage.click_text('我知道了')
        time.sleep(3)
        if detailpage.is_text_present('暂不开启'):
            detailpage.click_text('暂不开启')
        time.sleep(5)
        detailpage.cancel_hefeixin_call()
        time.sleep(2)

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0111(self):
        group_contact = EnterpriseContactsPage()
        group_contact.click_sub_level_department_by_name('bm0')
        time.sleep(1)
        group_contact.click_search_box()
        time.sleep(2)
        # 未保存到本地的非RCS用户
        group_contact.input_search_message('b测算')
        group_contact.hide_keyboard()
        group_contact.click_contacts_by_name('b测算')
        detailpage = ContactDetailsPage()
        # detailpage.wait_for_page_load()
        # 验证页面元素显示
        self.assertTrue(detailpage.is_exists_contacts_name())
        self.assertTrue(detailpage.is_exists_contacts_number())
        self.assertTrue(detailpage.is_exists_contacts_image())
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
        # detailpage.page_should_contain_text('保存到通讯录')
        # 点击头像查看大图
        # detailpage.click_avatar()
        # time.sleep(4)
        # 备注 无头像，没有大图
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
        # 点击电话 拨打电话
        detailpage.click_call_icon()
        time.sleep(3)
        detailpage.cancel_call2()
        time.sleep(3)

        # 点击语音,挂断语音电话
        detailpage.click_voice_call_icon()
        time.sleep(2)
        if detailpage.is_text_present('暂不开启'):
            detailpage.click_text('暂不开启')
        time.sleep(2)
        detailpage.end_voice_call()
        time.sleep(3)

        # 点击视频通话
        detailpage.click_video_call_icon()
        time.sleep(2)
        if detailpage.is_text_present('暂不开启'):
            detailpage.click_text('暂不开启')
        time.sleep(2)
        detailpage.end_video_call()
        time.sleep(3)

        # 点击飞信电话
        detailpage.click_hefeixin_call_menu()
        time.sleep(2)
        if detailpage.is_text_present('我知道了'):
            detailpage.click_text('我知道了')
        time.sleep(3)
        if detailpage.is_text_present('暂不开启'):
            detailpage.click_text('暂不开启')
        time.sleep(5)
        detailpage.cancel_hefeixin_call()
        time.sleep(2)

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0112(self):
        group_contact = EnterpriseContactsPage()
        group_contact.click_sub_level_department_by_name('bm0')
        time.sleep(1)
        # 标题栏三点
        # group_contact.click_three_points_icon()
        # time.sleep(1)
        # contacts = ContactsPage()
        # contacts.click_text("团队管理")
        # time.sleep(1)
        # # 再次进入部门 bm0
        # group_contact.click_sub_level_department_by_name('bm0')
        # time.sleep(1)
        # group_contact.add_phone_number_to_department('bm0')
        # time.sleep(1)
        # # 进入部门 bm0
        # group_contact.click_sub_level_department_by_name('bm0')
        # 本机用户
        group_contact.click_search_box()
        time.sleep(1)
        group_contact.input_search_message('本机测试')
        time.sleep(2)
        group_contact.click_contacts_by_name('本机测试')
        detailpage = ContactDetailsPage()
        detailpage.wait_for_page_load()
        # 验证页面元素显示
        self.assertTrue(detailpage.is_exists_contacts_name())
        self.assertTrue(detailpage.is_exists_contacts_number())
        self.assertTrue(detailpage.is_exists_contacts_image())
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
        # detailpage.page_should_contain_text('保存到通讯录')
        time.sleep(2)
        # 消息、电话、语音视频、视频电话、副号拨打、飞信电话置灰，不可点击
        detailpage.message_btn_is_clickable()
        detailpage.call_btn_is_clickable()
        detailpage.voice_btn_is_clickable()
        detailpage.video_call_btn_is_clickable()
        detailpage.hefeixin_call_btn_is_clickable()

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0129(self):
        group_contact = EnterpriseContactsPage()
        group_contact.click_sub_level_department_by_name('bm0')
        time.sleep(2)
        # 1.进入企业的子层级，显示子层级的用户和子部门名称
        group_contact.is_text_present('bm0')
        group_contact.is_search_contacts_name_full_match('b测算')
        # 2.显示用户头像、昵称、职位(有数据时显示)
        group_contact.is_exists_contacts_image()

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0130(self):
        """点击搜索结果已保存到本地的RCS用户进入Profile页(点击我的团队某个企业的部门下任一保存在本地的RCS联系人)"""
        group_contact=EnterpriseContactsPage()
        group_contact.click_sub_level_department_by_name('测试部门1')
        group_contact.click_contacts_by_name('测试号码')
        detailpage = ContactDetailsPage()
        detailpage.wait_for_page_load()
        # 验证页面元素显示
        self.assertTrue(detailpage.is_exists_contacts_name())
        self.assertTrue(detailpage.is_exists_contacts_number())
        self.assertTrue(detailpage.is_exists_contacts_image())
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
        # 备注 无头像，没有大图
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
        # 点击电话 拨打电话
        detailpage.click_call_icon()
        time.sleep(5)
        detailpage.cancel_call2()
        time.sleep(3)

        # 点击语音,挂断语音电话
        detailpage.click_voice_call_icon()
        time.sleep(2)
        if detailpage.is_text_present('暂不开启'):
            detailpage.click_text('暂不开启')
        time.sleep(5)
        detailpage.click_end_call()
        time.sleep(3)

        # 点击视频通话
        try:
            detailpage.click_video_call_icon()
            time.sleep(2)
            if detailpage.is_text_present('暂不开启'):
                detailpage.click_text('暂不开启')
            time.sleep(2)
            detailpage.end_video_call()
            time.sleep(3)
        except:
            pass

        # 点击飞信电话
        detailpage.click_hefeixin_call_menu()
        time.sleep(2)
        if detailpage.is_text_present('我知道了'):
            detailpage.click_text('我知道了')
        time.sleep(3)
        if detailpage.is_text_present('暂不开启'):
            detailpage.click_text('暂不开启')
        time.sleep(5)
        detailpage.cancel_hefeixin_call()
        time.sleep(2)
        # 分享名片按钮可点击
        detailpage.click_share_business_card()
        SelectContactsPage().select_local_contacts()
        SelectContactsPage().click_one_contact('大佬1')
        time.sleep(2)
        SelectContactsPage().click_share_card()
        detailpage.page_should_contain_text('已发送')


class MygroupdetailPage(TestCase):
    """通讯录-我的团队-个人详情页(profile页)"""
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
        # 导入团队联系人
        fail_time2 = 0
        flag1 = False
        while fail_time2 < 2:
            try:
                Preconditions.make_already_in_message_page()
                contact_names = ["大佬1", "大佬2", "大佬3", "大佬4", '香港大佬', '测试号码']
                Preconditions.create_he_contacts(contact_names)
                flag1 = True
            except:
                fail_time2 += 1
            if flag1:
                break

    def default_setUp(self):
        """确保每个用例执行前在团队联系人profile页"""
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()
        ContactsPage().select_group_by_name('ateam7272')
        time.sleep(2)

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0148(self):
        """进入我的团队用户的Profile页-消息"""
        group_contact = EnterpriseContactsPage()
        group_contact.click_contacts_by_name('测试号码')
        time.sleep(2)
        contact_detail = ContactDetailsPage()
        contact_detail.click_message_icon()
        time.sleep(2)
        chat=ChatWindowPage()
        if chat.is_text_present("用户须知"):
            # 如果存在用户须知,就点击已阅读,然后点击返回.如果不存在,就直接点击返回
            chat.click_already_read()
            chat.click_sure_icon()
        SingleChatPage().is_on_this_page()

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0150(self):
        """进入我的团队用户的Profile页-电话"""
        group_contact = EnterpriseContactsPage()
        group_contact.click_contacts_by_name('测试号码')
        time.sleep(2)
        contact_detail = ContactDetailsPage()
        contact_detail.click_call_icon()
        time.sleep(1)
        contact_detail.click_permission_box()
        time.sleep(2)
        result = contact_detail.is_element_present(locator='挂断电话2')
        self.assertTrue(result)
        contact_detail.cancel_call2()

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0151(self):
        """进入我的团队用户的Profile页-语音通话"""
        group_contact = EnterpriseContactsPage()
        group_contact.click_contacts_by_name('测试号码')
        time.sleep(2)
        contact_detail=ContactDetailsPage()
        contact_detail.click_voice_call_icon()
        contact_detail.click_permission_box()
        time.sleep(2)
        if contact_detail.is_text_present('暂不开启'):
            time.sleep(3)
            contact_detail.click_text('暂不开启')
        time.sleep(1)
        result = contact_detail.is_element_present(locator='结束通话')
        self.assertTrue(result)
        contact_detail.click_end_call()

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0152(self):
        """进入我的团队用户的Profile页-视频通话"""
        group_contact = EnterpriseContactsPage()
        group_contact.click_contacts_by_name('测试号码')
        time.sleep(2)
        contact_detail=ContactDetailsPage()
        contact_detail.click_video_call_icon()
        contact_detail.click_permission_box()
        time.sleep(2)
        if contact_detail.is_text_present('暂不开启'):
            contact_detail.click_text('暂不开启')
        self.assertTrue(contact_detail.is_element_present(locator='挂断视频通话'))
        contact_detail.end_video_call()

    @tags('ALL', 'CMCC-接口不稳定', 'contact', 'my_group')
    def test_contacts_quxinli_0153(self):
        """进入我的团队用户的非Profile页-语音通话"""
        group_contact = EnterpriseContactsPage()
        group_contact.click_contacts_by_name('大佬1')
        time.sleep(2)
        contact_detail=ContactDetailsPage()
        #点击语音通话
        contact_detail.click_voice_call_icon()
        contact_detail.click_permission_box()
        time.sleep(2)
        contact_detail.page_should_contain_text('对方未开通和飞信，无法拨打语音电话')
        # if contact_detail.is_text_present('暂不开启'):
        #     time.sleep(2)
        #     contact_detail.click_text('暂不开启')
        # self.assertTrue(contact_detail.is_element_present(locator='结束通话'))
        # contact_detail.click_end_call()

    @tags('ALL', 'CMCC-接口不稳定', 'contact', 'my_group')
    def test_contacts_quxinli_0154(self):
        """进入我的团队用户的非Profile页-视频通话"""
        group_contact = EnterpriseContactsPage()
        group_contact.click_contacts_by_name('大佬2')
        time.sleep(2)
        contact_detail=ContactDetailsPage()
        # 点击视频通话
        contact_detail.click_video_call_icon()
        contact_detail.click_permission_box()
        time.sleep(2)
        contact_detail.page_should_contain_text('对方未开通和飞信，无法拨打视频电话')
        # if contact_detail.is_text_present('暂不开启'):
        #     contact_detail.click_text('暂不开启')
        # self.assertTrue(contact_detail.is_element_present(locator='挂断视频通话'))
        # contact_detail.end_video_call()

    def setUp_test_contacts_quxinli_0155(self):
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.reset_and_relaunch_app()
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()
        ContactsPage().select_group_by_name('ateam7272')
        time.sleep(2)

    @tags('ALL', 'CMCC-reset', 'contact', 'my_group')
    def test_contacts_quxinli_0155(self):
        """本网登录用户进入我的团队用户的Profile页-首次拨打飞信电话"""
        group_contact = EnterpriseContactsPage()
        group_contact.click_contacts_by_name('测试号码')
        time.sleep(2)
        contact_detail=ContactDetailsPage()
        contact_detail.page_should_contain_text('飞信电话')
        # 点击飞信电话
        contact_detail.click_hefeixin_call_menu()
        time.sleep(2)
        contact_detail.page_should_contain_text('请先接听  “飞信电话”')
        if contact_detail.is_text_present('我知道了'):
            contact_detail.click_text('我知道了')
        contact_detail.click_permission_box()
        time.sleep(2)
        if contact_detail.is_text_present('暂不开启'):
            contact_detail.click_text('暂不开启')
        # 检验是否有12506回拨
        time.sleep(10)
        self.assertTrue(contact_detail.is_element_present(locator='和飞信电话-挂断电话'))
        contact_detail.cancel_hefeixin_call()

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0156(self):
        """本网登录用户进入我的团队用户的Profile页-非首次拨打飞信电话"""
        group_contact = EnterpriseContactsPage()
        group_contact.click_contacts_by_name('测试号码')
        time.sleep(2)
        contact_detail = ContactDetailsPage()
        contact_detail.page_should_contain_text('飞信电话')
        # 点击飞信电话
        contact_detail.click_hefeixin_call_menu()
        time.sleep(2)
        if contact_detail.is_text_present('我知道了'):
            contact_detail.click_text('我知道了')
        contact_detail.click_permission_box()
        time.sleep(2)
        if contact_detail.is_text_present('暂不开启'):
            contact_detail.click_text('暂不开启')
        # 检验是否有12306回拨
        time.sleep(10)
        result = contact_detail.is_element_present(locator='和飞信电话-挂断电话')
        self.assertTrue(result)
        contact_detail.cancel_hefeixin_call()

    @tags('ALL', 'CMCC-接口不稳定', 'contact', 'my_group')
    def test_contacts_quxinli_0193(self):
        """进入我的团队非RCS用户的Profile页-邀请使用"""
        group_contact = EnterpriseContactsPage()
        group_contact.click_contacts_by_name('大佬2')
        time.sleep(2)
        contact_detail=ContactDetailsPage()
        #点击邀请使用
        contact_detail.click_invitation_use()
        time.sleep(2)
        contact_detail.page_should_contain_text('最近都在用“和飞信”发消息打电话，免费短信省钱省心，多方通话一呼八应，邀请你一起畅享沟通，立即体验：http://feixin.10086.cn/rcs')

    @tags('ALL', 'CMCC-接口不稳定', 'contact', 'my_group')
    def test_contacts_quxinli_0194(self):
        """进入未保存本地的我的团队联系人Profile页-保存到通讯录"""
        group_contact = EnterpriseContactsPage()
        group_contact.click_contacts_by_name('陈丹丹')
        time.sleep(2)
        contact_detail=ContactDetailsPage()
        #点击邀请使用
        contact_detail.click_save_contacts_icon()
        time.sleep(2)
        creat=CreateContactPage()
        creat.hide_keyboard()
        time.sleep(3)
        #姓名 电话 公司自动填充
        name=creat.get_text_of_box(locator='输入姓名')
        self.assertIsNotNone(name)
        number = creat.get_text_of_box(locator='输入号码')
        self.assertIsNotNone(number)
        company = creat.get_text_of_box(locator='输入公司')
        self.assertIsNotNone(company)
        #点击保存,保存成功
        creat.click_save()
        contact_detail.page_should_contain_text('创建成功')
        contact_detail.is_on_this_page()

    @staticmethod
    def tearDown_test_contacts_quxinli_0194(self):
        Preconditions.make_already_in_message_page()
        MessagePage().click_contacts()
        contacts=ContactsPage()
        if contacts.is_contacts_exist('陈丹丹'):
            contacts.select_contacts_by_name('陈丹丹')
            ContactDetailsPage().click_edit_contact()
            edit=EditContactPage()
            edit.hide_keyboard()
            time.sleep(1)
            edit.click_delete_contact()
            edit.click_sure_delete()
        else:
            pass

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0195(self):
        """进入已保存本地的我的团队联系人的Profile页-分享名片"""
        group_contact = EnterpriseContactsPage()
        group_contact.click_contacts_by_name('测试号码')
        time.sleep(2)
        contact_detail = ContactDetailsPage()
        # 点击分享名片
        contact_detail.click_share_business_card()
        select_contact=SelectContactsPage()
        # 验证页面元素
        title=select_contact.get_element_text(locator='选择联系人')
        self.assertEqual(title,'选择联系人')
        input=select_contact.get_element_text(locator='搜索或输入手机号')
        self.assertEqual(input, '搜索或输入手机号')
        select_contact.page_should_contain_text('选择一个群')
        select_contact.page_should_contain_text('选择团队联系人')
        select_contact.page_should_contain_text('选择手机联系人')
        if select_contact.is_element_present_by_locator('最近聊天联系人'):
            select_contact.page_should_contain_text('最近聊天')

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0197(self):
        """在联系人选择器页面，选择一个群"""
        group_contact = EnterpriseContactsPage()
        group_contact.click_contacts_by_name('测试号码')
        time.sleep(2)
        contact_detail = ContactDetailsPage()
        # 点击分享名片
        contact_detail.click_share_business_card()
        select_contact = SelectContactsPage()
        select_contact.click_select_one_group()
        time.sleep(1)
        SelectOneGroupPage().selecting_one_group_by_name('给个红包1')
        SelectOneGroupPage().page_should_contain_text('发送名片')
        SelectOneGroupPage().click_share_business_card()
        SelectOneGroupPage().page_should_contain_text('已发送')

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0199(self):
        """在联系人选择器页面，选择本地联系人"""
        group_contact = EnterpriseContactsPage()
        group_contact.click_contacts_by_name('测试号码')
        time.sleep(2)
        contact_detail = ContactDetailsPage()
        # 点击分享名片
        contact_detail.click_share_business_card()
        select_contact = SelectContactsPage()
        select_contact.click_local_contacts()
        time.sleep(1)
        select_local=SelectLocalContactsPage()
        select_local.swipe_select_one_member_by_name('大佬1')
        select_local.page_should_contain_text('发送名片')
        select_local.click_share_business_card()
        contact_detail.page_should_contain_text('已发送')

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0201(self):
        """在联系人选择器页面，选择团队联系人"""
        group_contact = EnterpriseContactsPage()
        group_contact.click_contacts_by_name('测试号码')
        time.sleep(2)
        contact_detail = ContactDetailsPage()
        # 点击分享名片
        contact_detail.click_share_business_card()
        select_contact = SelectContactsPage()
        select_contact.click_he_contacts()
        time.sleep(1)
        sog = SelectOneGroupPage()
        sog.selecting_one_group_by_name2("ateam7272")
        time.sleep(1)
        SelectHeContactsDetailPage().selecting_he_contacts_by_name('陈丹丹')
        time.sleep(1)
        SelectHeContactsDetailPage().page_should_contain_text('发送名片')
        SelectHeContactsDetailPage().click_share_business_card()
        contact_detail.page_should_contain_text('已发送')

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0202(self):
        """用户未加入任何企业"""
        # 1.点击团队联系人进入我的团队页面，提示未加入任何企业
        # 2.名片分享成功
        group_contact = EnterpriseContactsPage()
        group_contact.click_contacts_by_name('测试号码')
        time.sleep(2)
        contact_detail = ContactDetailsPage()
        # 点击分享名片
        contact_detail.click_share_business_card()
        select_contact = SelectContactsPage()
        select_contact.click_he_contacts()
        time.sleep(1)
        sog = SelectOneGroupPage()
        sog.selecting_one_group_by_name2("ateam7272")
        time.sleep(1)
        SelectHeContactsDetailPage().selecting_he_contacts_by_name('大佬1')
        time.sleep(1)
        SelectHeContactsDetailPage().page_should_contain_text('发送名片')
        SelectHeContactsDetailPage().click_share_business_card()
        contact_detail.page_should_contain_text('已发送')

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0203(self):
        """用户只在一个企业下，且在企业子一层级"""
        # 1.点击团队联系人进入企业子一层级
        # 2.名片分享成功
        group_contact = EnterpriseContactsPage()
        group_contact.click_contacts_by_name('测试号码')
        time.sleep(2)
        contact_detail = ContactDetailsPage()
        # 点击分享名片
        contact_detail.click_share_business_card()
        select_contact = SelectContactsPage()
        select_contact.click_he_contacts()
        time.sleep(1)
        # select_he = SelectHeContactsPage()
        # select_he.select_one_team_by_name('bm0')
        sog = SelectOneGroupPage()
        sog.selecting_one_group_by_name2("bm0")
        time.sleep(1)
        SelectHeContactsDetailPage().selecting_he_contacts_by_name('b测算')
        time.sleep(1)
        SelectHeContactsDetailPage().page_should_contain_text('发送名片')
        SelectHeContactsDetailPage().click_share_business_card()
        contact_detail.page_should_contain_text('已发送')

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_contacts_quxinli_0207(self):
        """用户在多个企业下,分享名片"""
        group_contact = EnterpriseContactsPage()
        group_contact.click_contacts_by_name('测试号码')
        time.sleep(2)
        contact_detail = ContactDetailsPage()
        # 点击分享名片
        contact_detail.click_share_business_card()
        select_contact = SelectContactsPage()
        select_contact.click_he_contacts()
        time.sleep(1)
        select_he=SelectHeContactsPage()
        names = select_he.get_all_group_name()
        self.assertTrue(len(names) > 0)
        sog = SelectOneGroupPage()
        sog.selecting_one_group_by_name2("ateam7272")
        time.sleep(1)
        SelectHeContactsDetailPage().selecting_he_contacts_by_name('陈丹丹')
        time.sleep(1)
        SelectHeContactsDetailPage().page_should_contain_text('发送名片')
        SelectHeContactsDetailPage().click_share_business_card()
        contact_detail.page_should_contain_text('已发送')

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_msg_huangmianhua_0105(self):
        """群成员展示列表页，输入框输入号码——前3位搜索群成员"""
        group_contact = EnterpriseContactsPage()
        group_contact.click_search_box()
        time.sleep(1)
        group_contact.input_search_message("138")
        time.sleep(2)
        group_contact.hide_keyboard()
        exists = group_contact.is_exists_contacts_search_result3()
        self.assertEquals(exists, True)

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_msg_huangmianhua_0106(self):
        """群成员展示列表页，输入框输入号码——前3位搜索群成员"""
        group_contact = EnterpriseContactsPage()
        group_contact.click_search_box()
        time.sleep(1)
        group_contact.input_search_message("912")
        time.sleep(2)
        group_contact.hide_keyboard()
        exists = group_contact.is_exists_contacts_search_result3()
        self.assertEquals(exists, False)

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_msg_huangmianhua_0107(self):
        """群成员展示列表页，输入框输入——完整号码搜索群成员"""
        group_contact = EnterpriseContactsPage()
        group_contact.click_search_box()
        time.sleep(1)
        group_contact.input_search_message("13888888888")
        time.sleep(2)
        group_contact.hide_keyboard()
        exists = group_contact.is_exists_contacts_search_result3()
        self.assertEquals(exists, False)

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_msg_huangmianhua_0108(self):
        """群成员展示列表页，输入框输入——中文字符搜索群成员"""
        group_contact = EnterpriseContactsPage()
        group_contact.click_search_box()
        time.sleep(1)
        group_contact.input_search_message("群")
        time.sleep(2)
        group_contact.hide_keyboard()
        exists = group_contact.is_exists_contacts_search_result3()
        self.assertEquals(exists, False)

    @tags('ALL', 'CMCC', 'contact', 'my_group')
    def test_msg_huangmianhua_0109(self):
        """群成员展示列表页，输入框输入——英文字符搜索群成员"""
        group_contact = EnterpriseContactsPage()
        group_contact.click_search_box()
        time.sleep(1)
        group_contact.input_search_message("a")
        time.sleep(2)
        group_contact.hide_keyboard()
        exists = group_contact.is_exists_contacts_search_result3()
        self.assertEquals(exists, True)

