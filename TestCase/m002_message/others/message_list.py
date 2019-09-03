import time
import unittest

from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, current_driver
from library.core.utils.testcasefilter import tags
from pages import *
from pages.components import BaseChatPage
from pages.contacts import OfficialAccountPage, SearchOfficialAccountPage
from preconditions.BasePreconditions import WorkbenchPreconditions


class Preconditions(WorkbenchPreconditions):
    """前置条件"""

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
    def create_message_record(messages):
        """创造消息记录"""

        for title, text in messages:
            Preconditions.enter_single_chat_page(title)
            scp = SingleChatPage()
            # 输入文本信息
            scp.input_text_message(text)
            time.sleep(2)
            scp.send_text()
            scp.click_back()

    @staticmethod
    def create_contacts_by_name(name, number):
        """检查是否存在指定联系人，没有则创建"""

        mp = MessagePage()
        mp.open_contacts_page()
        ctp = ContactsPage()
        ctp.wait_for_page_load()
        ctp.click_search_box()
        cls = ContactListSearchPage()
        cls.wait_for_page_load()
        cls.input_search_keyword(name)
        time.sleep(2)
        if cls.is_exist_contacts():
            cls.click_back()
        else:
            cls.click_back()
            ctp.wait_for_page_load()
            mess = MessagePage()
            mess.click_phone_contact()
            time.sleep(3)
            ctp.click_add()
            ccp = CreateContactPage()
            ccp.wait_for_page_load()
            ccp.input_name(name)
            time.sleep(2)
            ccp.input_number(number)
            ccp.save_contact()
            cdp = ContactDetailsPage()
            cdp.wait_for_page_load()
            cdp.click_back_icon()
            time.sleep(1)
            cdp.click_back_by_android()
            time.sleep(1)
        ctp.wait_for_page_load()
        mp.open_message_page()
        mp.wait_for_page_load()

    @staticmethod
    def create_system_message():
        """创造系统消息"""

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
        scg.select_local_contacts()
        slc = SelectLocalContactsPage()
        # 等待选择联系人->本地联系人 页面加载
        slc.wait_for_page_load()
        slc.select_local_contacts(2)
        slc.click_sure()
        # 创建群
        cgnp = CreateGroupNamePage()
        cgnp.input_group_name("群聊999")
        cgnp.click_sure()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_delete_and_exit()
        mp.wait_for_message_list_load()

    @staticmethod
    def reset_and_relaunch_app():
        """首次启动APP（使用重置APP代替）"""

        app_package = 'com.chinasofti.rcs'
        current_driver().activate_app(app_package)
        current_mobile().reset_app()

    @staticmethod
    def make_in_message_page(moible_param,reset=False):
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
    def build_one_new_group_with_number(puhone_number,group_name):
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
        #添加指定电话成员
        time.sleep(2)
        sc.input_search_keyword(puhone_number)
        time.sleep(2)
        sog.click_text("tel")
        time.sleep(2)
        # 从本地联系人中选择成员创建群
        sc.click_local_contacts()
        time.sleep(2)
        slc = SelectLocalContactsPage()
        slc.click_one_contact("飞信电话")
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


class MessageListAllTest(TestCase):
    """模块：消息列表"""

    @classmethod
    def setUpClass(cls):
        Preconditions.select_mobile('Android-移动')
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
                try:
                    if conts.is_text_present("发现SIM卡联系人"):
                        conts.click_text("显示")
                except:
                    pass
                for name, number in required_contacts:
                    # 创建联系人
                    conts.create_contacts_if_not_exits(name, number)
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
        Preconditions.select_mobile('Android-移动')
        mp = MessagePage()
        if mp.is_on_this_page():
            return
        else:
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_B_0003(self):
        """消息列表进入"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 确保当前页面不在消息列表模块
        mp.open_me_page()
        me_page = MePage()
        me_page.wait_for_me_page_load()
        time.sleep(2)
        # 进入消息列表
        mp.open_message_page()
        # 1.等待消息列表页面加载
        mp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_B_0004(self):
        """登录之后消息列表进入"""

        # 重启客户端
        current_mobile().launch_app()
        mp = MessagePage()
        # 1.登录客户端,等待消息列表页面加载
        mp.wait_for_page_load()
        # 2.底部消息图标是否高亮显示
        self.assertEquals(mp.message_icon_is_selected(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_B_0005(self):
        """消息列表载入"""
        mp = MessagePage()
        # 设置手机网络断开
        mp.set_network_status(0)
        # 1.重启客户端,等待消息列表页加载,验证页面搜索,底部tab,右上角+是否可点击
        current_mobile().launch_app()
        mp.wait_for_page_load()
        self.assertEquals(mp.search_box_is_enabled(), True)
        self.assertEquals(mp.message_icon_is_enabled(), True)
        self.assertEquals(mp.call_icon_is_enabled(), True)
        self.assertEquals(mp.workbench_icon_is_enabled(), True)
        self.assertEquals(mp.contacts_icon_is_enabled(), True)
        self.assertEquals(mp.me_icon_is_enabled(), True)
        self.assertEquals(mp.add_icon_is_enabled(), True)
        time.sleep(3)
        # 2.搜索框下方提示当前网络不可用，请检查网络设置或稍后重试
        self.assertEquals(mp.is_exist_network_anomaly2(), True)
        # 3.底部消息图标是否高亮显示
        self.assertEquals(mp.message_icon_is_selected(), True)

    @staticmethod
    def tearDown_test_msg_xiaoliping_B_0005():
        """恢复网络"""
        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_B_0006(self):
        """消息列表进入到会话页面"""
        mp = MessagePage()
        # 等待消息列表页加载
        mp.wait_for_page_load()
        # 确保消息列表有消息记录
        name = "大佬1"
        Preconditions.enter_single_chat_page(name)
        scp = SingleChatPage()
        scp.input_text_message("test_msg_xiaoliping_B_0006")
        time.sleep(2)
        scp.send_text()
        scp.click_back()
        mp.wait_for_page_load()
        # 1.进入到会话页面
        mp.choose_chat_by_name(name)
        scp.wait_for_page_load()
        # 返回消息列表页
        scp.click_back()

    @tags('ALL', 'CMCC_RESET', 'LXD_RESET')
    def test_msg_xiaoliping_B_0008(self):
        """消息列表未读消息清空"""

        # 重置当前app
        Preconditions.make_already_in_message_page(True)
        mp = MessagePage()
        mp.wait_for_message_list_load()
        # 确保消息列表有未读消息
        self.assertEquals(mp.is_exist_unread_messages(), True)
        # 清空未读消息
        mp.clear_up_unread_messages()
        # 1.验证未读消息小红点标识是否消失
        self.assertEquals(mp.is_exist_unread_messages(), False)

    @unittest.skip("暂时难以实现,跳过")
    def test_msg_xiaoliping_B_0013(self):
        """消息列表订阅号红点显示"""

        mp = MessagePage()
        # 等待消息页加载
        mp.wait_for_page_load()
        # 切换到标签页：通讯录
        mp.open_contacts_page()
        cp = ContactsPage()
        time.sleep(2)
        # 进入公众号页面
        cp.click_official_account_icon()
        oap = OfficialAccountPage()
        oap.wait_for_page_load()
        # 进入搜索公众号页面
        oap.click_add()
        soap = SearchOfficialAccountPage()
        soap.wait_for_page_load()
        name = "移周刊"
        soap.input_search_key(name)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_B_0017(self):
        """消息列表网络异常显示"""
        mp = MessagePage()
        # 设置手机网络断开
        mp.set_network_status(0)
        time.sleep(5)
        # 1.是否提示当前网络不可用，请检查网络设置或稍后重试
        self.assertEquals(mp.is_exist_network_anomaly2(), True)
        # 2.等待消息页面加载
        mp.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_xiaoliping_B_0017():
        """恢复网络"""
        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_B_0019(self):
        """消息列表显示未发送成功"""
        mp = MessagePage()
        # 确保消息页面当前没有未发送成功消息标记
        if mp.is_iv_fail_status_present():
            mp.clear_fail_in_send_message()
        # 进入聊天会话页面
        name = "大佬1"
        Preconditions.enter_single_chat_page(name)
        # 设置手机网络断开
        mp.set_network_status(0)
        scp = SingleChatPage()
        # 1.输入文本信息
        scp.input_text_message("test_msg_xiaoliping_B_0019")
        time.sleep(2)
        scp.send_text()
        # 2.是否显示消息发送失败标识
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送失败', 10)
        scp.click_back()
        mp.wait_for_page_load()
        # 3.消息预览中是否显示未发送成功消息标记
        self.assertEquals(mp.is_iv_fail_status_present(), True)

    @staticmethod
    def tearDown_test_msg_xiaoliping_B_0019():
        """恢复网络"""
        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_B_0022(self):
        """消息列表网络异常显示"""
        mp = MessagePage()
        # 设置手机网络断开
        mp.set_network_status(0)
        time.sleep(5)
        # 1.是否提示当前网络不可用，请检查网络设置或稍后重试
        # 备注：当前网络不可用，请检查网络设置
        self.assertEquals(mp.is_exist_network_anomaly2(), True)
        # 2.等待消息页面加载
        mp.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_xiaoliping_B_0022():
        """恢复网络"""
        mp = MessagePage()
        mp.set_network_status(6)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_B_0023(self):
        """导航栏-点击导航条切换页签"""
        mp = MessagePage()
        # 1.等待消息页加载
        mp.wait_for_page_load()
        # 2.切换底部标签
        # 切换通话标签
        mp.open_call_page()
        clp = CallPage()
        time.sleep(2)
        if clp.is_exist_specified_prompt():
            clp.click_multi_party_telephone()
            time.sleep(2)
        if clp.is_exist_know():
            clp.click_know()
            clp.click_back()
            time.sleep(2)
        clp.wait_for_page_load()
        # 切换工作台标签
        mp.open_workbench_page()
        wp = WorkbenchPage()
        wp.wait_for_page_load()
        # 切换通讯录标签
        mp.open_contacts_page()
        ctp = ContactsPage()
        ctp.wait_for_page_load()
        # 切换我标签
        mp.open_me_page()
        me_page = MePage()
        me_page.wait_for_me_page_load()
        # 切换消息标签
        mp.open_message_page()
        mp.wait_for_page_load()

    @tags('ALL', 'CMCC_RESET', 'LXD_RESET')
    def test_msg_xiaoliping_B_0024(self):
        """导航栏-首次进入查看导航栏"""

        # 重置当前app
        Preconditions.make_already_in_message_page(True)
        mp = MessagePage()
        # 1.等待消息页面加载
        mp.wait_for_page_load()
        # 2.导航栏是否显示有消息，通话，工作台，通讯录，我五个tab页
        self.assertEquals(mp.is_exist_message_icon(), True)
        self.assertEquals(mp.is_exist_call_icon(), True)
        self.assertEquals(mp.is_exist_workbench_icon(), True)
        self.assertEquals(mp.is_exist_contacts_icon(), True)
        self.assertEquals(mp.is_exist_me_icon(), True)
        # 消息标签是否高亮显示
        self.assertEquals(mp.message_icon_is_selected(), True)

    @tags('ALL', 'CMCC_RESET', 'LXD_RESET')
    def test_msg_xiaoliping_B_0025(self):
        """验证首次登陆和飞信，进入消息页面（聊天为空），查看页面元素"""

        # 重置当前app
        Preconditions.make_already_in_message_page(True)
        mp = MessagePage()
        # 等待消息页面加载
        mp.wait_for_page_load()
        # 1.页面顶部是否展示全局搜索框
        self.assertEquals(mp.is_exist_search_box(), True)
        # 2.右上角是否有“+”号图标
        self.assertEquals(mp.is_exist_add_icon(), True)
        # 3.页面文案是否为“图文消息，一触即发”
        self.assertEquals(mp.is_exist_words(), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_B_0027(self):
        """消息列表界面消息列表页面元素检查"""
        mp = MessagePage()
        # 1.等待消息页加载
        mp.wait_for_page_load()
        # 2.消息图标高亮显示
        self.assertEquals(mp.message_icon_is_selected(), True)
        name = "啊" * 15
        number = "13300133001"
        Preconditions.create_contacts_by_name(name, number)
        # 确保有足够的消息记录可供滑动
        messages = [("大佬1", "1"),
                    ("大佬2", "2"),
                    ("大佬3", "3"),
                    ("大佬4", "4"),
                    ("给个红包1", "5"),
                    ("给个红包2", "6"),
                    ("给个红包3", "7"),
                    ("给个红包4", "8"),
                    (name, "9")]
        Preconditions.create_message_record(messages)
        # 列表中显示消息记录，消息左侧显示头像
        mp.is_exist_message_record()
        mp.is_exist_message_img()
        # 右侧显示时间，中间显示发送人和消息预览
        mp.is_exist_message_time()
        mp.is_exist_message_name()
        mp.is_exist_message_content()
        # 滑到消息记录顶端
        mp.slide_to_the_top()
        # 验证超过一屏可以滑动展示
        self.assertEquals(mp.is_slide_message_list(), False)
        # 发送人名称全部展示在消息列表上（名称长度最多为10汉字）
        # 验证一个能显示全名和一个不能显示全名的
        mp.slide_to_the_top()
        self.assertEquals(mp.message_list_is_exist_name("大佬1"), True)
        mp.slide_to_the_top()
        self.assertEquals(mp.message_list_is_exist_name(name), True)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_B_0028(self):
        """消息列表界面新建消息页面返回操作"""

        mp = MessagePage()
        # 等待消息页加载
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击“新建消息”
        mp.click_new_message()
        slc = SelectLocalContactsPage()
        # 1.等待选择联系人页面加载
        slc.wait_for_page_load()
        # 2.退出新建消息，返回消息列表
        slc.click_back()
        mp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_B_0033(self):
        """消息列表非第一个窗口长按置顶（Android）"""

        mp = MessagePage()
        # 等待消息页加载
        mp.wait_for_page_load()
        time.sleep(5)
        # 滑到消息记录顶端
        mp.slide_to_the_top()
        # 确保当前页面至少两条记录,以便区分置顶效果
        messages = [("大佬1", "123"), ("大佬2", "456")]
        Preconditions.create_message_record(messages)
        time.sleep(2)
        # 置顶非第一条消息记录
        name = mp.top_message_recording_by_number(1)
        time.sleep(2)
        # 获取当前第一条消息名称
        top_name = mp.get_message_name_by_number(0)
        # 1.验证是否置顶成功，排在第一
        self.assertEquals(name, top_name)
        time.sleep(2)
        # 取消置顶该窗口
        mp.cancel_stick_message_recording_by_number(0)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_B_0034(self):
        """消息列表窗口长按取消置顶（Android）"""

        mp = MessagePage()
        # 等待消息页加载
        mp.wait_for_page_load()
        time.sleep(5)
        # 滑到消息记录顶端
        mp.slide_to_the_top()
        # 确保当前页面至少两条记录,以便区分取消置顶效果
        messages = [("大佬3", "111"), ("大佬4", "222")]
        Preconditions.create_message_record(messages)
        time.sleep(2)
        # 置顶第二条消息记录
        name = mp.top_message_recording_by_number(1)
        time.sleep(5)
        # 获取当前第一条消息名称
        current_top_name = mp.get_message_name_by_number(0)
        # 验证该窗口是否已被置顶
        self.assertEquals(name, current_top_name)
        # 取消置顶该窗口
        cancel_stick_name = mp.cancel_stick_message_recording_by_number(0)
        time.sleep(5)
        # 获取当前第二条消息名称
        current_second_name = mp.get_message_name_by_number(1)
        # 1.验证是否取消置顶成功
        self.assertEquals(cancel_stick_name, current_second_name)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_B_0035(self):
        """消息列表窗口长按删除（Android）"""
        mp = MessagePage()
        # 等待消息页加载
        mp.wait_for_page_load()
        # 确保消息列表有记录
        messages = [("大佬1", "111")]
        Preconditions.create_message_record(messages)
        time.sleep(2)
        # 删除指定消息记录
        mp.delete_message_record_by_name(messages[0][0])
        # 验证是否删除成功,在消息列表消失
        self.assertEquals(mp.current_message_list_is_exist_name(messages[0][0]), False)

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_B_0044(self):
        """已开启免打扰的单聊，未收到新消息"""

        mp = MessagePage()
        # 等待消息页加载
        mp.wait_for_page_load()
        # 消息列表如果已经存在消息免打扰图标,清空聊天记录
        if mp.is_exist_no_disturb_icon():
            mp.clear_message_record()
        # 确保消息列表有记录
        Preconditions.enter_single_chat_page("大佬1")
        scp = SingleChatPage()
        # 输入文本信息
        scp.input_text_message("123")
        time.sleep(2)
        scp.send_text()
        time.sleep(2)
        scp.click_setting()
        scs = SingleChatSetPage()
        scs.wait_for_page_load()
        time.sleep(2)
        # 开启消息免打扰
        if not scs.is_selected_no_disturb():
            scs.click_no_disturb()
            time.sleep(4)
        scs.click_back()
        scp.wait_for_page_load()
        # 1.单聊会话页面是否显示消息免打扰图标
        self.assertEquals(scp.is_exist_no_disturb_icon(), True)
        scp.click_back()
        mp.wait_for_page_load()
        # 2.消息列表是否显示免打扰铃铛
        self.assertEquals(mp.is_exist_no_disturb_icon(), True)
        # 3.验证免打扰铃铛拖拽是否消除
        self.assertEquals(mp.is_clear_no_disturb_icon(), False)

    @staticmethod
    def tearDown_test_msg_xiaoliping_B_0044():
        """消息免打扰关闭"""

        mess = MessagePage()
        if not mess.is_on_this_page():
            current_mobile().launch_app()
            mess.wait_for_page_load()
        Preconditions.enter_single_chat_page("大佬1")
        scp = SingleChatPage()
        scp.wait_for_page_load()
        scp.click_setting()
        scs = SingleChatSetPage()
        scs.wait_for_page_load()
        time.sleep(2)
        # 关闭消息免打扰
        if scs.is_selected_no_disturb():
            scs.click_no_disturb()
            time.sleep(4)
        scs.click_back()
        scp.wait_for_page_load()
        scp.click_back()
        mess.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_B_0048(self):
        """已开启免打扰的群聊，未收到新消息"""
        mp = MessagePage()
        # 等待消息页加载
        mp.wait_for_page_load()
        # 消息列表如果已经存在消息免打扰图标,清空聊天记录
        if mp.is_exist_no_disturb_icon():
            mp.clear_message_record()
            time.sleep(2)
        # 确保消息列表有记录
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 输入文本信息
        gcp.input_text_message("456")
        time.sleep(2)
        gcp.send_text()
        time.sleep(2)
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        time.sleep(2)
        # 开启消息免打扰
        if not gcs.get_switch_undisturb_status():
            gcs.click_switch_undisturb()
            time.sleep(4)
        gcs.click_back()
        gcp.wait_for_page_load()
        # 1.群聊会话页面是否显示消息免打扰图标
        self.assertEquals(gcp.is_exist_undisturb(), True)
        gcp.click_back()
        mp.wait_for_page_load()
        # 2.消息列表是否显示免打扰铃铛
        self.assertEquals(mp.is_exist_no_disturb_icon(), True)
        # 3.验证免打扰铃铛拖拽是否消除
        self.assertEquals(mp.is_clear_no_disturb_icon(), False)

    @staticmethod
    def tearDown_test_msg_xiaoliping_B_0048():
        """消息免打扰关闭"""
        mp = MessagePage()
        if not mp.is_on_this_page():
            current_mobile().launch_app()
            mp.wait_for_page_load()
        Preconditions.enter_group_chat_page("群聊1")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        time.sleep(2)
        # 关闭消息免打扰
        if gcs.get_switch_undisturb_status():
            gcs.click_switch_undisturb()
            time.sleep(4)
        gcs.click_back()
        gcp.wait_for_page_load()
        gcp.click_back()
        mp.wait_for_page_load()

    @unittest.skip("新版本系统消息为气泡提示，暂时跳过")
    def test_msg_xiaoliping_B_0051(self):
        """在消息列表页面，接收到新的系统消息"""

        mp = MessagePage()
        # 等待消息页加载
        mp.wait_for_page_load()
        # 消息列表如果已经存在消息红点,清空聊天记录
        if mp.is_exist_news_red_dot():
            mp.clear_message_record()
            time.sleep(2)
        # 在消息列表首页接收到新的系统消息
        Preconditions.create_system_message()
        # 1.验证是否存在红点提醒
        self.assertEquals(mp.is_exist_news_red_dot(), True)
        # 2.验证消息红点拖拽是否消除
        self.assertEquals(mp.is_clear_news_red_dot(), False)

    @staticmethod
    def tearDown_test_msg_xiaoliping_B_0051():
        """清除系统消息"""

        mp = MessagePage()
        if not mp.is_on_this_page():
            current_mobile().launch_app()
            mp.wait_for_page_load()
        if mp.current_message_list_is_exist_name("系统消息"):
            mp.choose_chat_by_name("系统消息")
            mp.click_back()
            mp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'LXD')
    def test_msg_xiaoliping_B_0052(self):
        """在消息列表页面，未接收到新的系统消息"""

        mp = MessagePage()
        # 等待消息页加载
        mp.wait_for_page_load()
        # 消息列表如果已经存在消息红点,清空聊天记录
        if mp.is_exist_news_red_dot():
            mp.clear_message_record()
            time.sleep(2)
        # 1.验证是否存在红点提醒
        self.assertEquals(mp.is_exist_news_red_dot(), False)

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_xiaoliping_B_0016(self):
        """消息列表未读气泡展示"""
        # 1、点击消息
        # 2、在消息列表页面观察消息记录
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        mess = MessagePage()
        # 等待消息页加载
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.input_search_keyword(phone_number)
        time.sleep(2)
        sc.click_text("tel")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(3)
        scp=SingleChatPage()
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        scp.input_message("嘿嘿")
        time.sleep(2)
        scp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        Preconditions.change_mobile('Android-移动')
        phone_number2 = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        mess.press_file_to_do(phone_number, "删除聊天")
        Preconditions.change_mobile('Android-移动-移动')
        mess.wait_for_page_load()
        if not mess.is_element_exit_("未读消息气泡"):
            raise AssertionError("没有未读消息气泡")
        mess.press_file_to_do(phone_number2,"删除聊天")

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_xiaoliping_B_0021(self):
        """进入到会话查看未读消息"""
        # 1、点击消息列表中的未读消息
        # 2、点击返回按钮
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        mess = MessagePage()
        # 等待消息页加载
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.input_search_keyword(phone_number)
        time.sleep(2)
        sc.click_text("tel")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(3)
        scp = SingleChatPage()
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        i=0
        while i<15:
            scp.input_message("嘿嘿")
            time.sleep(2)
            scp.send_message()
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            i+=1
        Preconditions.change_mobile('Android-移动')
        phone_number2 = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        mess.press_file_to_do(phone_number, "删除聊天")
        Preconditions.change_mobile('Android-移动-移动')
        mess.wait_for_page_load()
        if not mess.is_element_exit_("未读消息气泡"):
            raise AssertionError("没有未读消息气泡")
        mess.click_text(phone_number2)
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        scp.click_text("条新消息")
        time.sleep(2)
        if not scp.is_text_present("以下为新消息"):
            raise AssertionError("没有分割线显示以下为未读消息")
        scp.page_up()
        scp.page_up()
        if scp.is_text_present("以下为新消息"):
            raise AssertionError("下滑不可浏览")
        current_mobile().back()
        time.sleep(3)
        mess.press_file_to_do(phone_number2, "删除聊天")

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_xiaoliping_B_0036(self):
        """消息列表未读气泡窗口长按删除"""
        # 1、点击窗口长按
        # 2、选择删除
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        mess = MessagePage()
        # 等待消息页加载
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.input_search_keyword(phone_number)
        time.sleep(2)
        sc.click_text("tel")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(3)
        scp = SingleChatPage()
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        scp.input_message("嘿嘿")
        time.sleep(2)
        scp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        Preconditions.change_mobile('Android-移动')
        phone_number2 = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        mess.press_file_to_do(phone_number, "删除聊天")
        Preconditions.change_mobile('Android-移动-移动')
        mess.wait_for_page_load()
        if not mess.is_element_exit_("未读消息气泡"):
            raise AssertionError("没有未读消息气泡")
        mess.press_file_to_do(phone_number2, "删除聊天")
        if scp.is_text_present(phone_number2):
            raise AssertionError("删除窗口不成功")

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_xiaoliping_B_0043(self):
        """已开启免打扰的单聊，接收到新消息"""
        # 1.开启与A单聊的免打扰模式
        # 2.在消息列表首页接收到A发送的新消息
        # 3.拖拽红点气泡，在非原位置释放
        # 4.点击进入会话框
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        mess = MessagePage()
        # 等待消息页加载
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.input_search_keyword(phone_number)
        time.sleep(2)
        sc.click_text("tel")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(3)
        scp = SingleChatPage()
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        scp.input_message("嘿嘿")
        time.sleep(2)
        scp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        phone_number2 = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动-移动')
        mess.wait_for_page_load()
        mess.click_text(phone_number2)
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        scp.click_setting()
        scsp=SingleChatSetPage()
        scsp.wait_for_page_load()
        scsp.click_no_disturb()
        current_mobile().back()
        current_mobile().back()
        Preconditions.change_mobile('Android-移动')
        mess.wait_for_page_load()
        mess.click_text(phone_number)
        scp.wait_for_page_load()
        scp.input_message("嘿嘿")
        time.sleep(2)
        scp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        Preconditions.change_mobile('Android-移动')
        mess.press_file_to_do(phone_number, "删除聊天")
        Preconditions.change_mobile('Android-移动-移动')
        mess.wait_for_page_load()
        if not mess.is_exist_news_red_dot():
            raise AssertionError("消息红点不存在")
        mess.click_text(phone_number2)
        time.sleep(2)
        current_mobile().back()
        time.sleep(2)
        if mess.is_exist_news_red_dot():
            raise AssertionError("消息红点没有消失")
        if not mess.is_element_exit_("消息免打扰图标"):
            raise AssertionError("消息免打扰图标不在")
        # 关闭消息免打扰
        mess.click_text(phone_number2)
        scp.wait_for_page_load()
        scp.click_setting()
        scsp.wait_for_page_load()
        scsp.click_no_disturb()
        current_mobile().back()
        current_mobile().back()
        time.sleep(2)
        mess.press_file_to_do(phone_number2, "删除聊天")

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_xiaoliping_B_0045(self):
        """未开启免打扰的单聊，收到一条新消息"""
        # 1未开启免打扰模式
        # 2.在消息列表首页接收到一条新消息
        # 3.拖拽红点气泡，在非原位置释放
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        mess = MessagePage()
        # 等待消息页加载
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.input_search_keyword(phone_number)
        time.sleep(2)
        sc.click_text("tel")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(3)
        scp = SingleChatPage()
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        scp.input_message("嘿嘿")
        time.sleep(2)
        scp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        Preconditions.change_mobile('Android-移动')
        phone_number2 = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        mess.press_file_to_do(phone_number, "删除聊天")
        Preconditions.change_mobile('Android-移动-移动')
        mess.wait_for_page_load()
        if not mess.is_element_exit_("未读消息气泡"):
            raise AssertionError("没有未读消息气泡")
        scp.press_and_move_down("未读消息气泡")
        time.sleep(2)
        mess.press_file_to_do(phone_number2, "删除聊天")

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_xiaoliping_B_0046(self):
        """未开启免打扰的单聊，收到超过99条新消息"""
        # 1未开启免打扰模式
        # 2.在消息列表首页接收到超过99条新消息
        # 3.拖拽红点气泡，在非原位置释放
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        mess = MessagePage()
        # 等待消息页加载
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面
        sc = SelectContactsPage()
        sc.wait_for_page_load()
        time.sleep(2)
        sc.input_search_keyword(phone_number)
        time.sleep(2)
        sc.click_text("tel")
        time.sleep(2)
        sc.click_text("确定")
        time.sleep(3)
        scp = SingleChatPage()
        if scp.is_text_present("1元/条"):
            scp.click_i_have_read()
        scp.wait_for_page_load()
        i = 0
        while i < 101:
            scp.input_message("嘿嘿")
            time.sleep(2)
            scp.send_message()
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            i += 1
        Preconditions.change_mobile('Android-移动')
        phone_number2 = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        mess.press_file_to_do(phone_number, "删除聊天")
        Preconditions.change_mobile('Android-移动-移动')
        mess.wait_for_page_load()
        if not mess.is_element_exit_("未读消息气泡"):
            raise AssertionError("没有未读消息气泡")
        scp.press_and_move_down("未读消息气泡")
        time.sleep(2)
        mess.press_file_to_do(phone_number2, "删除聊天")

    @staticmethod
    def setUp_test_msg_xiaoliping_B_0047():
        """确保有一个多人的群聊"""
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        group_name = Preconditions.get_group_chat_name_double()
        flag = Preconditions.build_one_new_group_with_number(phone_number, group_name)
        if not flag:
            Preconditions.change_mobile('Android-移动-移动')
            mess = MessagePage()
            mess.wait_for_page_load()
            mess.click_text("系统消息")
            time.sleep(3)
            mess.click_text("同意")
        Preconditions.change_mobile('Android-移动')
        Preconditions.go_to_group_double(group_name)

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_xiaoliping_B_0047(self):
        """已开启免打扰的群聊，接收到新消息"""
        # 1.开启B群聊的免打扰模式
        # 2.在消息列表首页接收到B群内发送的新消息
        # 3.拖拽红点气泡，在非原位置释放
        # 4.点击进入会话框
        group_name = Preconditions.get_group_chat_name_double()
        Preconditions.change_mobile('Android-移动-移动')
        Preconditions.go_to_group_double(group_name)
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_switch_undisturb()
        Preconditions.change_mobile('Android-移动')
        Preconditions.go_to_group_double(group_name)
        gcp.input_text_message("嘿嘿")
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        Preconditions.delete_record_group_chat()
        Preconditions.change_mobile('Android-移动-移动')
        mess=MessagePage()
        mess.wait_for_page_load()
        if not mess.is_exist_news_red_dot():
            raise AssertionError("消息红点不存在")
        mess.click_text(group_name)
        time.sleep(2)
        current_mobile().back()
        time.sleep(2)
        if mess.is_exist_news_red_dot():
            raise AssertionError("消息红点没有消失")
        if not mess.is_element_exit_("消息免打扰图标"):
            raise AssertionError("消息免打扰图标不在")
        # 关闭消息免打扰
        mess.click_text(group_name)
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_switch_undisturb()
        Preconditions.change_mobile('Android-移动-移动')
        Preconditions.go_to_group_double(group_name)
        Preconditions.delete_record_group_chat()

    @staticmethod
    def setUp_test_msg_xiaoliping_B_0049():
        """确保有一个多人的群聊"""
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        group_name = Preconditions.get_group_chat_name_double()
        flag = Preconditions.build_one_new_group_with_number(phone_number, group_name)
        if not flag:
            Preconditions.change_mobile('Android-移动-移动')
            mess = MessagePage()
            mess.wait_for_page_load()
            mess.click_text("系统消息")
            time.sleep(3)
            mess.click_text("同意")
        Preconditions.change_mobile('Android-移动')
        Preconditions.go_to_group_double(group_name)

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_xiaoliping_B_0049(self):
        """未开启免打扰的群聊，收到一条新消息"""
        # 1未开启免打扰模式
        # 2.在消息列表首页接收到一条新消息
        # 3.拖拽红点气泡，在非原位置释放
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.input_text_message("嘿嘿")
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        group_name = Preconditions.get_group_chat_name_double()
        Preconditions.delete_record_group_chat()
        Preconditions.change_mobile('Android-移动-移动')
        mess=MessagePage()
        mess.wait_for_page_load()
        if not mess.is_element_exit_("未读消息气泡"):
            raise AssertionError("没有未读消息气泡")
        gcp.press_and_move_down("未读消息气泡")
        time.sleep(2)
        mess.press_file_to_do(group_name, "删除聊天")

    @staticmethod
    def setUp_test_msg_xiaoliping_B_0050():
        """确保有一个多人的群聊"""
        Preconditions.select_mobile('Android-移动-移动')
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        Preconditions.change_mobile('Android-移动')
        group_name = Preconditions.get_group_chat_name_double()
        flag = Preconditions.build_one_new_group_with_number(phone_number, group_name)
        if not flag:
            Preconditions.change_mobile('Android-移动-移动')
            mess = MessagePage()
            mess.wait_for_page_load()
            mess.click_text("系统消息")
            time.sleep(3)
            mess.click_text("同意")
        Preconditions.change_mobile('Android-移动')
        Preconditions.go_to_group_double(group_name)

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_xiaoliping_B_0050(self):
        """未开启免打扰的群聊，收到超过99条新消息"""
        # 1未开启免打扰模式
        # 2.在消息列表首页接收到超过99条新消息
        # 3.拖拽红点气泡，在非原位置释放
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        i = 0
        while i < 101:
            gcp.input_message("嘿嘿")
            time.sleep(2)
            gcp.send_message()
            # 验证是否发送成功
            cwp = ChatWindowPage()
            try:
                cwp.wait_for_msg_send_status_become_to('发送成功', 10)
            except TimeoutException:
                raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
            i += 1
        group_name = Preconditions.get_group_chat_name_double()
        Preconditions.delete_record_group_chat()
        Preconditions.change_mobile('Android-移动-移动')
        mess=MessagePage()
        mess.wait_for_page_load()
        if not mess.is_element_exit_("未读消息气泡"):
            raise AssertionError("没有未读消息气泡")
        gcp.press_and_move_down("未读消息气泡")
        time.sleep(2)
        mess.press_file_to_do(group_name, "删除聊天")

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_huangmianhua_0202(self):
        """消息列表——消息tab_未读消息清空"""
        # 重置当前app
        Preconditions.make_already_in_message_page(True)
        mp = MessagePage()
        mp.wait_for_message_list_load()
        # 确保消息列表有未读消息
        if mp.is_exist_unread_messages():
            # 清空未读消息
            mp.clear_up_unread_messages()
            # 1.验证未读消息小红点标识是否消失
            self.assertEquals(mp.is_exist_unread_messages(), False)
        else:
            self.assertFalse(mp.is_exist_unread_messages())

    @tags('ALL', 'CMCC_double', 'full', 'full-yyx')
    def test_msg_huangmianhua_0203(self):
        """未开启免打扰的群聊，收到一条新消息"""
        # 1未开启免打扰模式
        # 2.在消息列表首页接收到一条新消息
        # 3.拖拽红点气泡，在非原位置释放
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.input_text_message("嘿嘿")
        gcp.send_message()
        # 验证是否发送成功
        cwp = ChatWindowPage()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        group_name = Preconditions.get_group_chat_name_double()
        Preconditions.delete_record_group_chat()
        Preconditions.change_mobile('Android-移动-移动')
        mess = MessagePage()
        mess.wait_for_page_load()
        # 确保消息列表有未读消息
        if mess.is_exist_unread_messages():
            # 清空未读消息
            mess.clear_up_unread_messages()
            # 1.验证未读消息小红点标识是否消失
            self.assertEquals(mess.is_exist_unread_messages(), False)
        else:
            self.assertFalse(mess.is_exist_unread_messages())