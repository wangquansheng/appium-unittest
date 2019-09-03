import re
import time
import uuid
import warnings

from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.components.selectors import PictureSelector
from preconditions.BasePreconditions import LoginPreconditions, REQUIRED_MOBILES, WorkbenchPreconditions


class Preconditions(WorkbenchPreconditions):
    """前置条件"""

    @staticmethod
    def enter_message_page(reset=False):
        """进入消息页面"""
        # 登录进入消息页面
        Preconditions.make_already_in_message_page(reset)

    @staticmethod
    def enter_private_chat_setting_page(reset=False):
        """进入单聊设置页面"""
        Preconditions.enter_private_chat_page(reset)
        chat = SingleChatPage()
        chat.click_setting()
        setting = SingleChatSetPage()
        setting.wait_for_page_load()

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
    def make_no_message_send_failed_status():
        """确保当前消息列表没有消息发送失败的标识影响验证结果"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        if mp.is_iv_fail_status_present():
            mp.clear_fail_in_send_message()

    @staticmethod
    def enter_label_grouping_chat_page(enterLabelGroupingChatPage=True):
        """进入标签分组会话页面"""
        # 登录进入消息页面
        Preconditions.make_already_in_message_page()
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
        # 点击群发信息
        if enterLabelGroupingChatPage:
            lgdp.click_send_group_info()
            chat = LabelGroupingChatPage()
            chat.wait_for_page_load()

    @staticmethod
    def get_label_grouping_name():
        """获取群名"""
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "alg" + phone_number[-4:]
        return group_name

    @staticmethod
    def init_contact_group_data():
        # 创建联系人
        fail_time = 0
        import dataproviders
        while fail_time < 2:
            try:
                required_contacts = dataproviders.get_preset_contacts()
                conts = ContactsPage()
                conts.open_contacts_page()
                time.sleep(1)
                mp = MessagePage()
                mp.click_phone_contact()
                time.sleep(1)
                try:
                    if conts.is_text_present("发现SIM卡联系人"):
                        conts.click_text("显示")
                except:
                    pass
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
                return
            except:
                fail_time += 1
                import traceback
                msg = traceback.format_exc()
                print(msg)


class MsgPrivateChatMsgList(TestCase):
    """模块：单聊->消息列表"""

    @classmethod
    def setUpClass(cls):
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        Preconditions.init_contact_group_data()

    def default_setUp(self):
        """确保每个用例运行前在消息页面"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_message_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0044(self):
        """消息-消息列表进入"""
        # 1、点击消息
        mess = MessagePage()
        mess.open_message_page()
        if not mess.is_on_this_page():
            raise AssertionError("未成功进入消息列表页面")

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0045(self):
        """消息-消息列表界面+功能页面元素检查"""
        # 1、点击消息
        mess = MessagePage()
        mess.open_message_page()
        # 2、点击右上角的+号按钮
        mess.click_add_icon()
        time.sleep(1)
        # 下拉出“新建消息”、“免费短信”、“发起群聊”、分组群发、“扫一扫”，入口
        mess.page_should_contain_text("新建消息")
        mess.page_should_contain_text("免费短信")
        mess.page_should_contain_text("发起群聊")
        mess.page_should_contain_text("扫一扫")
        mess.driver.back()
        mess.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0048(self):
        """消息-消息列表界面新建消息页面元素检查"""
        # 1、点击消息右上角+按钮
        mess = MessagePage()
        mess.open_message_page()
        mess.click_add_icon()
        # 2、查看新建消息页面元素
        # 左上角有返回按钮，左上角显示新建消息标题，下方有搜索输入框，
        # 和通讯录入口，全量联系人列表，左侧显示姓名首字母排序、右侧显示索引字母排序。
        mess.click_new_message()
        scp = SelectContactsPage()
        scp.wait_for_create_msg_page_load()
        scp.page_contain_element('返回')
        scp.page_contain_element('选择联系人')
        scp.page_contain_element('搜索或输入手机号')
        scp.page_contain_element('右侧字母索引')
        # if not scp.is_right_letters_sorted():
        #     raise AssertionError("右侧字母索引未排序")
        scp.page_contain_element('左侧字母索引')
        # if not scp.is_left_letters_sorted():
        #     raise AssertionError("左侧字母索引未排序")
        # 3、滑动屏幕, 搜索栏常驻顶端
        scp.page_up()
        scp.page_up()
        scp.page_contain_element('搜索或输入手机号')
        scp.click_back()
        mess.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0049(self):
        """消息-消息列表界面新建消息页面返回操作"""
        # 1、点击右上角的+号按钮，成功进入新建消息界面
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_new_message()
        # 2、点击左上角返回按钮，退出新建消息，返回消息列表
        scp = SelectContactsPage()
        scp.wait_for_create_msg_page_load()
        scp.click_back()
        mess.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0050(self):
        """消息-消息列表界面新建消息页面返回操作"""
        # 1、点击右上角的+号按钮
        mess = MessagePage()
        mess.click_add_icon()
        mess.click_new_message()
        # 2、点击手机系统内置返回返回按钮
        scp = SelectContactsPage()
        scp.wait_for_create_msg_page_load()
        scp.driver.back()
        mess.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0051(self):
        """资料页发起聊天"""
        # 1、在“联系人资料”页 点击【消息】,进入“个人会话”窗口
        Preconditions.enter_private_chat_page()
        # 返回消息列表页面
        chat = SingleChatPage()
        mess = MessagePage()
        chat.click_back_by_android()
        time.sleep(1)
        chat.click_back_by_android()
        time.sleep(1)
        chat.click_back_by_android()
        time.sleep(1)
        mess.open_message_page()
        mess.wait_for_page_load()

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0052():
        """消息列表点击消息记录前，先发送一条消息"""
        Preconditions.enter_private_chat_page()
        chat = SingleChatPage()
        chat.input_message("hello")
        chat.send_message()
        chat.click_back_by_android()
        time.sleep(1)
        chat.click_back_by_android()
        time.sleep(1)
        chat.click_back_by_android()
        time.sleep(1)
        mess = MessagePage()
        mess.open_message_page()
        mess.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0052(self):
        """消息-消息列表进入到会话页面"""
        # 1、在消息列表点击消息记录，进入到会话页面
        mess = MessagePage()
        mess.click_msg_by_content("hello")
        chat = SingleChatPage()
        chat.wait_for_page_load()
        chat.click_back()
        mess.wait_for_page_load()

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0054():
        """消息列表点击消息记录前，先发送一条消息"""
        Preconditions.enter_private_chat_page()
        chat = SingleChatPage()
        chat.input_message("hello")
        chat.send_message()
        chat.click_back_by_android()
        time.sleep(1)
        chat.click_back_by_android()
        time.sleep(1)
        chat.click_back_by_android()
        time.sleep(1)
        mess = MessagePage()
        mess.open_message_page()
        mess.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0054(self):
        """消息-消息列表-消息列表显示未发送成功"""
        # 1、 在会话页面输入文本消息
        mess = MessagePage()
        mess.click_msg_by_content("hello")
        chat = SingleChatPage()
        chat.wait_for_page_load()
        # 断网
        current_mobile().set_network_status(0)
        chat.input_message("MsgList_0010")
        # 2、点击发送
        chat.send_message()
        if not chat.is_msg_send_fail():
            raise AssertionError("断网发送消息，在聊天会话窗无发送失败标志")
        # 3、点击返回消息列表
        chat.click_back()
        mess.wait_for_page_load()
        if not mess.is_iv_fail_status_present():
            raise AssertionError("断网发送消息，在消息列表无发送失败标志")

    @staticmethod
    def tearDown_test_msg_huangcaizui_A_0054():
        """恢复网络连接"""
        current_mobile().set_network_status(6)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0056():
        """消息列表点击消息记录前，先发送一条消息"""
        Preconditions.enter_private_chat_page()
        chat = SingleChatPage()
        chat.wait_for_page_load()
        chat.clear_msg()
        chat.input_message("hello")
        chat.send_message()
        chat.click_back_by_android()
        time.sleep(1)
        chat.click_back_by_android()
        time.sleep(1)
        chat.click_back_by_android()
        time.sleep(1)
        mess = MessagePage()
        mess.open_message_page()
        mess.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0056(self):
        """消息-消息列表-消息列表显示未发送成功"""
        # 1、 在会话页面输入文本消息
        mess = MessagePage()
        mess.click_msg_by_content("hello")
        chat = SingleChatPage()
        chat.wait_for_page_load()
        # 断网
        current_mobile().set_network_status(0)
        chat.input_message("MsgList_0012")
        # 2、点击发送
        chat.send_message()
        if not chat.is_msg_send_fail():
            raise AssertionError("断网发送消息，在聊天会话窗无发送失败标志")
        # 3、点击返回消息列表
        chat.click_back()
        mess.wait_for_page_load()
        if not mess.is_iv_fail_status_present():
            raise AssertionError("断网发送消息，在消息列表无发送失败标志")
        mess.click_msg_by_content("MsgList_0012")
        # 恢复网络重发消息
        current_mobile().set_network_status(6)
        chat.repeat_send_msg()
        chat.click_sure_repeat_msg()
        chat.click_back()
        mess.wait_for_page_load()
        if mess.is_iv_fail_status_present():
            raise AssertionError("恢复网络重发消息，在消息列表依然存在发送失败标志")

    @staticmethod
    def tearDown_test_msg_huangcaizui_A_0056():
        """恢复网络连接"""
        current_mobile().set_network_status(6)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0057():
        """消息列表点击消息记录前，先发送一条消息"""
        Preconditions.enter_private_chat_page()
        chat = SingleChatPage()
        msg = "哈哈" * 30
        chat.input_message(msg)
        chat.send_message()
        chat.click_back_by_android()
        time.sleep(1)
        chat.click_back_by_android()
        time.sleep(1)
        chat.click_back_by_android()
        time.sleep(1)
        mess = MessagePage()
        mess.open_message_page()
        mess.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0057(self):
        """消息-消息列表-消息列表中文本消息预览"""
        # 1、查看消息列表中一对一文本消息记录
        mess = MessagePage()
        # 消息记录左面显示头像，右侧显示时间，中间上方显示发送消息人的名称，
        mess.page_contain_element('消息头像')
        mess.page_contain_element('消息时间')
        mess.page_contain_element('消息名称')
        # 下方显示文本内容，文本过长时以省略号显示
        mess.page_contain_element('消息简要内容')
        mess.msg_is_contain_ellipsis()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0140(self):
        """新建消息"""
        # 1、点击右上角+号 - 新建消息
        mess = MessagePage()
        mess.open_message_page()
        mess.click_add_icon()
        mess.click_new_message()
        scp = SelectContactsPage()
        scp.wait_for_create_msg_page_load()
        # 页面元素有为号码输入或搜索框，黄页通讯录列表（含名称与号码、按名称拼音首字母排列）
        scp.page_contain_element('搜索或输入手机号')
        scp.page_contain_element('local联系人')
        scp.page_contain_element('左侧字母索引')
        if not scp.is_left_letters_sorted():
            raise AssertionError("左侧字母索引未排序")
        scp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0142(self):
        """新建消息"""
        # 1、点击右上角+号 - 新建消息
        mess = MessagePage()
        mess.open_message_page()
        mess.click_add_icon()
        mess.click_new_message()
        scp = SelectContactsPage()
        scp.wait_for_create_msg_page_load()
        # 2、选中黄页内一名联系人，进入聊天窗口
        scp.click_one_local_contacts()
        chat = SingleChatPage()
        # 如果弹框用户须知则点击处理
        flag = chat.is_exist_dialog()
        if flag:
            chat.click_i_have_read()
        chat.wait_for_page_load()
        chat.click_back()


class MsgPrivateChatMsgSetting(TestCase):
    """单聊->单聊设置"""
    @classmethod
    def setUpClass(cls):
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        Preconditions.init_contact_group_data()

    def default_setUp(self):
        """确保每个用例运行前在单聊设置页面"""
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_private_chat_setting_page()
        setting = SingleChatSetPage()
        if setting.is_on_this_page():
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_private_chat_setting_page()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0064(self):
        """消息—一对一消息会话—设置"""
        setting = SingleChatSetPage()
        setting.click_back()
        chat = SingleChatPage()
        # 1.点击右上角的设置按钮,进入聊天设置页面
        chat.click_setting()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0065(self):
        """消息—一对一消息会话—设置页面头像转跳"""
        # 1. 点击联系人头像,进入到联系人详情页。
        setting = SingleChatSetPage()
        setting.click_avatar()
        detail = ContactDetailsPage()
        detail.wait_for_page_load()
        # 回到设置页面
        detail.click_message_icon()
        chat = SingleChatPage()
        chat.click_setting()
        setting.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0070(self):
        """消息-一对一消息会话-设置页面查找聊天内容"""
        # 1. 点击下方的查找聊天内容按钮, 跳到搜索页面
        setting = SingleChatSetPage()
        setting.search_chat_record()
        fcrp = FindChatRecordPage()
        fcrp.wait_for_page_loads()
        fcrp.click_back()
        setting.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0071(self):
        """消息-一对一消息会话-设置页面查找聊天内容"""
        # 先发送消息
        setting = SingleChatSetPage()
        setting.click_back()
        chat = SingleChatPage()
        msg = 'hehe'
        chat.input_message(msg)
        chat.send_message()
        chat.click_setting()
        # 1. 点击下方的查找聊天内容按钮
        setting.search_chat_record()
        # 2. 搜索已接收或发送消息的关键字
        fcrp = FindChatRecordPage()
        fcrp.wait_for_page_loads()
        fcrp.input_search_message(msg)
        self.assertTrue(fcrp.is_element_exit('发送人头像'))
        self.assertTrue(fcrp.is_element_exit('发送人名称'))
        self.assertTrue(fcrp.is_element_exit('发送的内容'))
        self.assertTrue(fcrp.is_element_exit('发送的时间'))
        # 3.点击任意一个搜索到的聊天信息
        fcrp.click_record()
        chat.click_setting()
        setting.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0078(self):
        """消息-一对一消息会话-设置页面查找不存在的聊天内容"""
        # 1. 点击下方的查找聊天内容按钮
        setting = SingleChatSetPage()
        setting.search_chat_record()
        # 2. 搜索不存在的关键字
        fcrp = FindChatRecordPage()
        times = 20
        while times > 0:
            msg = uuid.uuid4().__str__()
            fcrp.input_search_message(msg)
            try:
                fcrp.page_should_contain_text("无搜索结果")
                break
            except:
                times = times - 1
                continue
        if times == 0:
            raise AssertionError("搜索异常，页面无‘无搜索结果’文本")
        fcrp.click_back()
        setting.wait_for_page_load()

    @staticmethod
    def public_send_file(file_type):
        # 1、在当前聊天会话页面，点击更多富媒体的文件按钮
        setting = SingleChatSetPage()
        setting.click_back()
        chat = SingleChatPage()
        chat.wait_for_page_load()
        if not chat.is_open_more():
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
        time.sleep(3)

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0079(self):
        """消息-一对一消息会话-设置页面查找聊天文件"""
        self.public_send_file('.txt')
        chat = SingleChatPage()
        # 1. 点击右上角个人设置按钮
        chat.click_setting()
        setting = SingleChatSetPage()
        # 2. 点击下方的查找聊天内容按钮
        setting.search_chat_record()
        # 3.点击文件
        fcrp = FindChatRecordPage()
        fcrp.click_file()
        file = ChatFilePage()
        file.wait_for_page_loads()
        file.page_should_contain_file()
        # file.click_back()
        # fcrp.click_back()
        # setting.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0080(self):
        """消息-一对一消息会话-设置页面查找聊天文件"""
        # 1. 点击右上角个人设置按钮
        setting = SingleChatSetPage()
        # 2. 点击下方的查找聊天内容按钮
        setting.search_chat_record()
        time.sleep(2)
        # 3.点击文件
        fcrp = FindChatRecordPage()
        fcrp.click_file()
        time.sleep(2)
        file = ChatFilePage()
        file.clear_file_record()
        time.sleep(2)
        file.page_should_contain_text("暂无文件")

    @staticmethod
    def public_send_video():
        """在聊天会话页面发送一个视频"""
        setting = SingleChatSetPage()
        setting.click_back()
        chat = SingleChatPage()
        # 点击图片按钮
        chat.wait_for_page_load()
        chat.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 选择一个视频发送
        cpp.select_video()
        cpp.click_send()
        chat.wait_for_page_load()
        time.sleep(2)

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0081(self):
        """消息-一对一消息会话-设置页面查找聊天图片与视频"""
        self.public_send_video()
        chat = SingleChatPage()
        chat.click_setting()
        # 1.点击查找聊天内容
        setting = SingleChatSetPage()
        setting.search_chat_record()
        # 2.点击图片与视频
        fcrp = FindChatRecordPage()
        fcrp.click_pic_video()
        pv = PicVideoPage()
        pv.wait_for_page_load()
        if not pv.is_exist_video():
            raise AssertionError("发送视频后在聊天记录的图片与视频页面无视频")
        # pv.click_back()
        # fcrp.click_back()
        # setting.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0082(self):
        """消息-一对一消息会话-设置页面查找聊天图片与视频"""
        # 1.点击查找聊天内容
        setting = SingleChatSetPage()
        setting.search_chat_record()
        # 2.点击图片与视频
        fcrp = FindChatRecordPage()
        fcrp.click_pic_video()
        pv = PicVideoPage()
        pv.wait_for_page_load()
        pv.clear_record()
        pv.page_should_contain_text("暂无内容")
        # pv.click_back()
        # fcrp.click_back()
        # setting.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0089(self):
        """ 一对一聊天设置创建群聊 """
        # 1.点击+添加成员,进入选择成员页面
        setting = SingleChatSetPage()
        setting.click_add_icon()
        scp = SelectContactsPage()
        scp.wait_for_page_local_contact_load()
        # scp.click_back()
        # setting.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0090(self):
        """ 一对一聊天设置创建群聊 """
        setting = SingleChatSetPage()
        setting.click_back()
        # 1.进入一对一聊天窗口
        chat = SingleChatPage()
        chat.click_setting()
        # 2.点击进入聊天设置，再点击+添加成员
        setting.click_add_icon()
        # 3.点击选择一个或多个成员
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        names = slcp.get_contacts_name()
        for name in names:
            slcp.select_one_member_by_name(name)
            if not slcp.is_toast_exist("该联系人不可选择", timeout=3):
                break
        # 4.点击反回聊天设置
        slcp.click_back()
        setting.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0091(self):
        """ 一对一聊天设置创建群聊 """
        setting = SingleChatSetPage()
        setting.click_back()
        # 1.进入一对一聊天窗口
        chat = SingleChatPage()
        chat.click_setting()
        # 2.点击进入聊天设置，再点击+添加成员
        setting.click_add_icon()
        # 3.点击选择一个或多个成员
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        # 选择一个成员
        names = list(slcp.get_contacts_name())
        for name in names:
            slcp.select_one_member_by_name(name)
            if not slcp.is_toast_exist("该联系人不可选择", timeout=3):
                break
        # 4.点击确定,进入群聊名称设置
        slcp.click_sure()
        name_set = CreateGroupNamePage()
        name_set.click_back()
        slcp.click_back()
        setting.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0092(self):
        """ 一对一聊天设置创建群聊 """
        setting = SingleChatSetPage()
        setting.click_back()
        # 1.进入一对一聊天窗口
        chat = SingleChatPage()
        chat.click_setting()
        # 2.点击进入聊天设置，再点击+添加成员
        setting.click_add_icon()
        # 3.搜索选择一个或多个成员
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        names = list(slcp.get_contacts_name())
        for name in names:
            slcp.search_and_select_one_member_by_name(name)
        # 4.点击确定,进入群聊名称设置
        slcp.click_sure()
        # name_set = CreateGroupNamePage()
        # name_set.click_back()
        # slcp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0093(self):
        """ 一对一聊天设置创建群聊 """
        setting = SingleChatSetPage()
        setting.click_back()
        # 1.进入一对一聊天窗口
        chat = SingleChatPage()
        chat.click_setting()
        # 2.点击进入聊天设置，再点击+添加成员
        setting.click_add_icon()
        # 3.点击选择一个或多个成员
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        # 选择一个成员
        names = list(slcp.get_contacts_name())
        for name in names:
            slcp.select_one_member_by_name(name)
            if not slcp.is_toast_exist("该联系人不可选择", timeout=3):
                break
        # 4.点击确定进入群聊名称设置
        slcp.click_sure()
        name_set = CreateGroupNamePage()
        time.sleep(1)
        # 5.再点击返回聊天设置
        name_set.click_back()
        slcp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0094(self):
        """ 一对一聊天设置创建群聊 """
        setting = SingleChatSetPage()
        setting.click_back()
        # 1.进入一对一聊天窗口
        chat = SingleChatPage()
        chat.wait_for_page_load()
        chat.click_setting()
        # 2.点击进入聊天设置，再点击+添加成员
        setting.click_add_icon()
        # 3.搜索选择一个或多个成员
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        # 选择多个成员
        names = list(slcp.get_contacts_name())
        for name in names:
            slcp.search_and_select_one_member_by_name(name)
        # 4.点击确定进入群聊名称设置
        slcp.wait_for_page_load()
        slcp.click_sure()
        # 5.再点击返回聊天设置
        slcp.click_back()
        # current_mobile().launch_app()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0095(self):
        """ 一对一聊天设置创建群聊 """
        setting = SingleChatSetPage()
        setting.wait_for_page_load()
        cur_name = setting.get_name()
        setting.click_back()
        # 1.进入一对一聊天窗口
        chat = SingleChatPage()
        chat.click_setting()
        # 2.点击进入聊天设置，再点击+添加成员
        setting.click_add_icon()
        # 3.搜索选择一个或多个成员
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        # 选择一个成员
        names = list(slcp.get_contacts_name())
        if cur_name in names:
            names.remove(cur_name)
        if '本机' in names:
            names.remove('本机')
        for name in names:
            slcp.search_and_select_one_member_by_name(name)
            if not slcp.is_toast_exist("该联系人不可选择", timeout=3):
                if not slcp.contacts_is_selected(name):
                    raise AssertionError("联系人未被选中")
                # 4.点击左上角选择的成员名称或再次点击列表里该成员名称
                # slcp.select_one_member_by_name(name)
                # if slcp.contacts_is_selected(name):
                #     raise AssertionError("搜索选择一个成员后再次点击列表里该成员，依然是选择状态")
                break
        slcp.wait_for_page_load()
        # slcp.click_back()
        # setting.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0096(self):
        """ 一对一聊天设置创建群聊 """
        setting = SingleChatSetPage()
        cur_name = setting.get_name()
        setting.click_back()
        # 1.进入一对一聊天窗口
        chat = SingleChatPage()
        chat.click_setting()
        # 2.点击进入聊天设置，再点击+添加成员
        setting.click_add_icon()
        # 3.点击选择一个或多个成员
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        # 选择一个成员
        names = list(slcp.get_contacts_name())
        if cur_name in names:
            names.remove(cur_name)
        if '本机' in names:
            names.remove('本机')
        for name in names:
            slcp.select_one_member_by_name(name)
            if not slcp.is_toast_exist("该联系人不可选择", timeout=3):
                if not slcp.contacts_is_selected(name):
                    raise AssertionError("联系人未被选中")
                # 4.点击左上角选择的成员名称或再次点击列表里该成员名称
                # slcp.select_one_member_by_name(name)
                # if slcp.contacts_is_selected(name):
                #     raise AssertionError("搜索选择一个成员后再次点击列表里该成员，依然是选择状态")
                break
        slcp.wait_for_page_load()
        # slcp.click_back()
        # setting.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0097(self):
        """ 一对一聊天设置创建群聊,无网络 """
        setting = SingleChatSetPage()
        cur_name = setting.get_name()
        setting.click_back()
        # 1.进入一对一聊天窗口
        chat = SingleChatPage()
        chat.click_setting()
        # 2.点击进入聊天设置，再点击+添加成员
        setting.click_add_icon()
        # 3.点击选择一个或多个成员
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        names = list(slcp.get_contacts_name())
        if cur_name in names:
            names.remove(cur_name)
        if '本机' in names:
            names.remove('本机')
        for name in names:
            slcp.select_one_member_by_name(name)
            if not slcp.is_toast_exist("该联系人不可选择", timeout=3):
                break
        # 4.点击确定，再点击创建
        slcp.click_sure()
        # 断网
        current_mobile().set_network_status(0)
        name_set = CreateGroupNamePage()
        time.sleep(2)
        name_set.click_sure()
        if not name_set.is_toast_exist("网络不可用", timeout=6):
            raise AssertionError("无网络不可用提示")
        # name_set.click_back()
        # slcp.click_back()
        # setting.wait_for_page_load()

    @staticmethod
    def tearDown_test_msg_huangcaizui_A_0097():
        """恢复网络连接"""
        current_mobile().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0098(self):
        """ 一对一聊天设置创建群聊 """
        setting = SingleChatSetPage()
        cur_name = setting.get_name()
        setting.click_back()
        # 1.进入一对一聊天窗口
        chat = SingleChatPage()
        chat.click_setting()
        # 2.点击进入聊天设置，再点击+添加成员
        setting.click_add_icon()
        # 3.点击选择一个或多个成员
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        names = list(slcp.get_contacts_name())
        if cur_name in names:
            names.remove(cur_name)
        if '本机' in names:
            names.remove('本机')
        for name in names:
            slcp.select_one_member_by_name(name)
            if not slcp.is_toast_exist("该联系人不可选择", timeout=3):
                break
        # 4.点击确定，统一群聊名称，再点击创建
        slcp.click_sure()
        name_set = CreateGroupNamePage()
        time.sleep(2)
        group_name = 'testGroup'
        name_set.input_group_name(group_name)
        name_set.click_sure()
        group_chat = GroupChatPage()
        group_chat.wait_for_page_load()
        if group_name not in group_chat.get_group_name():
            raise AssertionError("群聊的名称显示不是所编辑的名称 " + group_name)
        # 清除测试数据
        group_chat.click_setting()
        group_set = GroupChatSetPage()
        group_set.click_delete_and_exit2()
        time.sleep(1)
        group_set.click_sure()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0099(self):
        """ 点对点建群"""
        setting = SingleChatSetPage()
        setting.wait_for_page_load()
        setting.click_back()
        # 1.长按文本消息
        chat = SingleChatPage()
        chat.wait_for_page_load()
        chat.clear_msg()
        chat.input_message("hello")
        chat.send_message()
        chat.press_mess("hello")
        # 弹出多功能列表，包含复制、转发、删除、撤回、收藏、（移动用户有/异网无）转为短信发送、多选
        chat.page_should_contain_text("复制")
        chat.page_should_contain_text("转发")
        chat.page_should_contain_text("删除")
        chat.page_should_contain_text("撤回")
        chat.page_should_contain_text("收藏")
        chat.page_should_contain_text("转为短信发送")
        chat.page_should_contain_text("多选")
        chat.driver.back()
        chat.click_setting()
        setting.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0072(self):
        """ 输入框中输入表情消息不发送，进入查找聊天内容后是否还显示草稿"""
        setting = SingleChatSetPage()
        setting.wait_for_page_load()
        setting.click_back()
        # 1、进入一对一聊天界面
        chat = SingleChatPage()
        chat.wait_for_page_load()
        chat.input_message("hello")
        chat.send_message()
        if not chat.is_open_expression():
            chat.open_expression()
        # 2、在聊天输入框中输入数十个表情
        chat.select_expression(n=10)
        # 3、点击设置按钮
        chat.click_setting()
        # 4.点击查找聊天内容
        setting.search_chat_record()
        # 5.输入框中输入已存在会话中的关键词
        fcrp = FindChatRecordPage()
        fcrp.wait_for_page_loads()
        fcrp.input_search_message('hello')
        # 6.点击任意一条搜索结果
        fcrp.click_record()
        chat.wait_for_page_load()
        chat.page_should_contain_text('说点什么...')
        chat.click_setting()
        setting.wait_for_page_load()

    @staticmethod
    def public_input_mess(msg):
        """Msg_PrivateChat_Setting_0034-0038共有部分提取"""
        setting = SingleChatSetPage()
        setting.click_back()
        # 1、进入一对一聊天界面
        chat = SingleChatPage()
        chat.wait_for_page_load()
        chat.input_message("hello")
        chat.send_message()
        # 2、在聊天输入框中输入msg
        chat.input_message(msg)
        # 3、点击设置按钮
        chat.click_setting()
        # 4.点击查找聊天内容
        setting.search_chat_record()
        # 5.输入框中输入已存在会话中的关键词
        fcrp = FindChatRecordPage()
        fcrp.wait_for_page_loads()
        fcrp.input_search_message('hello')
        # 6.点击任意一条搜索结果
        fcrp.click_record()
        chat.wait_for_page_load()
        chat.page_should_contain_text('说点什么...')
        chat.click_setting()
        setting.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0073(self):
        """ 输入框中输入文字不发送，进入查找聊天内容后是否还显示草稿"""
        self.public_input_mess("您好")

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0074(self):
        """ 输入框中输入数字消息不发送，进入查找聊天内容后是否还显示草稿"""
        self.public_input_mess("123456789")

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0075(self):
        """ 输入框中输入字母消息不发送，进入查找聊天内容后是否还显示草稿"""
        self.public_input_mess("abcdef")

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0076(self):
        """ 输入框中输入字符消息不发送，进入查找聊天内容后是否还显示草稿"""
        self.public_input_mess("@#$%%%^&")

    @tags('ALL', 'SMOKE', 'CMCC')
    def test_msg_huangcaizui_A_0077(self):
        """ 输入框中输入各种混合消息体不发送，进入查找聊天内容后是否还显示草稿"""
        self.public_input_mess("abc123@#$%^&")


class MsgContactSelector(TestCase):
    """单聊->联系人选择器"""

    @classmethod
    def setUpClass(cls):
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        Preconditions.init_contact_group_data()

    def default_setUp(self):
        """确保每个用例运行前在消息页面"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_huangcaizui_A_0001(self):
        """ 进入新建消息是否正常"""
        # 1.点击右上角的+
        mess = MessagePage()
        mess.click_add_icon()
        # 2.点击新建消息
        mess.click_new_message()
        # 3.查看页面展示
        scp = SelectContactsPage()
        scp.wait_for_create_msg_page_load()
        # 左上角标题：选择联系人；搜索栏缺省文字：搜索或输入手机号；
        # 选择和通讯录联系人；下方为本地联系人列表
        scp.page_should_contain_text("选择联系人")
        scp.page_should_contain_text("搜索或输入手机号")
        # scp.page_should_contain_text("选择和通讯录联系人")
        scp.page_contain_element("local联系人")
        scp.click_back()
        mess.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_huangcaizui_B_0061(self):
        """ 进入免费/发送短信查看展示页面"""
        # 1.点击右上角的+
        mess = MessagePage()
        mess.click_add_icon()
        # 2.点击免费/发送短信
        mess.click_free_sms()
        # 首次进入会弹出“欢迎使用免费短信”/“欢迎使用短信”弹框，点击确定后直接进入联系人选择器，
        # 非首次进入的直接进入联系人选择器
        try:
            time.sleep(1)
            mess.page_should_contain_text("欢迎使用免费短信")
            mess.click_text("确定")
        except:
            pass
        # 3.查看页面展示
        scp = SelectContactsPage()
        scp.wait_for_create_msg_page_load()
        # 左上角标题：选择联系人；搜索栏缺省文字：搜索或输入手机号；
        # 选择和通讯录联系人；下方为本地联系人列表
        scp.page_should_contain_text("选择联系人")
        scp.page_should_contain_text("搜索或输入手机号")
        # scp.page_should_contain_text("选择和通讯录联系人")
        scp.page_contain_element("local联系人")
        scp.click_back()
        mess.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_huangcaizui_A_0023(self):
        """ 最近聊天选择器：单聊内转发消息"""
        # 1、在聊天会话页面，长按可转发的消息，是否可以跳转到联系人选择器页面
        Preconditions.enter_private_chat_page()
        chat = SingleChatPage()
        chat.input_message("hehe")
        chat.send_message()
        chat.press_mess('hehe')
        chat.click_to_do('转发')
        result = chat.is_text_present("选择联系人")
        self.assertEqual(result, True)
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        scp.click_back()
        time.sleep(1)
        chat.click_back()
        time.sleep(1)
        ContactDetailsPage().click_back()
        time.sleep(1)
        chat.click_back_by_android()
        time.sleep(1)
        ContactsPage().open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_huangcaizui_A_0024(self):
        """ 最近聊天选择器：单聊内转发消息--选择一个群"""
        Preconditions.enter_private_chat_page()
        chat = SingleChatPage()
        chat.input_message("hello")
        chat.send_message()
        chat.press_mess('hello')
        time.sleep(1)
        chat.click_to_do('转发')
        # 1、在联系人选择器页面，点击选择一个群
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        # 2、进入到群聊列表展示页面，顶部的搜索文案是否展示为：搜索群聊
        sogp.page_should_contain_text("搜索群组")
        group_names = sogp.get_group_name()
        sogp.click_search_group()
        # 3、在顶部的搜索框中输入搜索条件，不存在搜索结果时下方展示文案是否是：无搜索结果
        times = 60
        while times > 0:
            msg = uuid.uuid4().__str__()
            sogp.input_search_keyword(msg)
            time.sleep(1)
            if sogp.is_text_present('无搜索结果'):
                break
            times -= 1
        if times == 0:
            raise AssertionError("无 ‘无搜索结果’")
        if not group_names:
            raise AssertionError('无群，请创建！')
        # 4、存在搜索结果时，展示的搜索结果是否符合需求
        sogp.input_search_keyword(group_names[0])
        time.sleep(1)
        sogp.page_should_contain_text(group_names[0])
        # 5、点击选中一个搜索结果，是否会弹出确认弹窗
        sogp.click_search_result()
        time.sleep(2)
        if not sogp.is_text_present("发送给"):
            raise AssertionError("转发消息给群组时，无含‘发送给’文本的弹窗")
        sogp.click_text("确定")
        chat.wait_for_page_load()
        chat.click_back()
        time.sleep(1)
        ContactDetailsPage().click_back()
        time.sleep(1)
        chat.click_back_by_android()
        time.sleep(1)
        ContactsPage().open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_huangcaizui_A_0025(self):
        """ 最近聊天选择器：单聊内转发消息--选择本地联系人"""
        Preconditions.enter_private_chat_page()
        chat = SingleChatPage()
        chat.input_message("hehe")
        chat.send_message()
        chat.press_mess('hehe')
        chat.click_to_do('转发')
        # 1、在联系人选择器页面，点击选择本地联系人，跳转到本地联系人列表展示页面
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        scp.select_local_contacts()
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        # 2、当前页面左上角展示的文案是否符合需求展示为：选择联系人
        slcp.page_should_contain_text("选择联系人")
        # 3、顶部搜索框中，默认展示的文案是否是：搜索或输入手机号
        slcp.page_should_contain_text('搜索或输入手机号')
        names = list(slcp.get_contacts_name())
        # 4、在搜索框中输入搜索条件，检查不存在搜索结果时，下方是否展示：无搜索结果
        times = 60
        while times > 0:
            msg = uuid.uuid4().__str__()
            slcp.search(msg)
            time.sleep(1)
            if not slcp.is_search_result(msg):
                break
            times -= 1
        if times == 0:
            raise AssertionError("无 ‘无搜索结果’")
        if not names:
            raise AssertionError('无联系人，请创建！')
        # 5、在搜索框中输入搜索条件，存在搜索结果时，下方展示的搜索结果是否符合需求
        # 6、点击选中搜索出的结果，是否会弹出确认弹窗
        slcp.search_and_select_one_member_by_name(names[0])
        time.sleep(2)
        if not slcp.is_text_present("发送给"):
            raise AssertionError("转发消息给本地联系人时，无含‘发送给’文本的弹窗")
        slcp.click_text("确定")
        chat.wait_for_page_load()
        chat.click_back()
        time.sleep(1)
        ContactDetailsPage().click_back()
        time.sleep(1)
        chat.click_back_by_android()
        time.sleep(1)
        ContactsPage().open_message_page()


class MsgPrivateChatDialog(TestCase):
    """单聊->单聊聊天会话"""
    @classmethod
    def setUpClass(cls):
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        Preconditions.init_contact_group_data()

    def default_setUp(self):
        """确保每个用例运行前在单聊会话页面"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_private_chat_page()
            return
        chat = SingleChatPage()
        if chat.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_private_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_huangcaizui_A_0102(self):
        """ 页面样式"""
        # 1、进入一对一天聊天界面,页面右下角出现表情选择按钮
        chat = SingleChatPage()
        chat.page_should_contains_element('打开表情')

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_huangcaizui_A_0103(self):
        """ 页面样式"""
        # 1、进入一对一聊天界面
        chat = SingleChatPage()
        # 2、点击聊天界面右下角的表情选择按钮
        if not chat.is_open_expression():
            chat.open_expression()
        time.sleep(1)
        chat.page_should_contains_element('表情id')
        chat.page_should_contains_element('表情集选择栏')
        chat.page_should_contains_element('翻页小圆点')
        chat.page_should_contains_element('删除表情按钮')
        # 表情‘键盘’
        chat.is_exist_element('关闭表情')
        chat.close_chat_expression()

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_huangcaizui_A_0104(self):
        """ 表情列表按钮"""
        # 1、进入一对一聊天界面
        chat = SingleChatPage()
        # 2、点击聊天界面右下角的表情选择按钮
        if not chat.is_open_expression():
            chat.open_expression()
        time.sleep(1)
        # 3、在单个表情列表中选择一个表情
        emoji_texts = chat.select_expression(n=1)
        input_msg = chat.get_input_message()
        if input_msg not in emoji_texts:
            raise AssertionError("选择表情后，消息输入框中未出现选中的表情")
        chat.close_chat_expression()
        chat.input_message('')

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_huangcaizui_A_0105(self):
        """ 表情列表按钮"""
        # 1、进入一对一聊天界面
        chat = SingleChatPage()
        # 2、点击聊天界面右下角的表情选择按钮
        if not chat.is_open_expression():
            chat.open_expression()
        time.sleep(1)
        # 3、在单个表情列表中选择一个表情
        emoji_texts = chat.select_expression(n=1)
        input_msg = chat.get_input_message()
        if input_msg not in emoji_texts:
            raise AssertionError("选择表情后，消息输入框中未出现选中的表情")
        # 4、点击删除按钮
        chat.delete_expression()
        input_msg2 = chat.get_input_message()
        if input_msg2 in emoji_texts:
            raise AssertionError("删除选择表情后，消息输入框中的表情依然存在")
        chat.close_chat_expression()
        chat.input_message('')

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_huangcaizui_A_0107(self):
        """ 表情列表按钮"""
        # 1、进入一对一聊天界面
        chat = SingleChatPage()
        # 2、点击聊天界面右下角的表情选择按钮
        if not chat.is_open_expression():
            chat.open_expression()
        time.sleep(1)
        # 3、在单个表情列表中选择一个表情
        chat.select_expression(n=1)
        # 4、点击聊天输入框
        chat.click_msg_input_box()
        time.sleep(1)
        flag = current_mobile().is_keyboard_shown()
        if not flag:
            raise AssertionError("点击聊天输入框键盘没有弹出！")
        chat.input_message('')
        current_mobile().hide_keyboard_if_display()

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_huangcaizui_A_0126(self):
        """发送超长内容处理"""
        # 1、进入一对一聊天界面
        chat = SingleChatPage()
        # 2、在聊天输入框中输入一百个文字与表情
        msg = "呵呵"*50 + '[可爱1]'
        chat.input_message(msg)
        # 3、点击发送
        chat.send_message()
        txt = chat.get_input_message()
        if '说点什么...' != txt:
            raise AssertionError("输入框文本不是 ‘说点什么...’")

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_huangcaizui_A_0127(self):
        """发送超长内容处理"""
        # 1、进入一对一聊天界面
        chat = SingleChatPage()
        # 2、在聊天输入框中输入数十个表情、文字、空格与空行
        msg = "呵呵"*10 + '[可爱1]'*10 + ' '*40 + "呵呵"*10
        chat.input_message(msg)
        # 3、点击发送
        chat.send_message()
        txt = chat.get_input_message()
        if '说点什么...' != txt:
            raise AssertionError("输入框文本不是 ‘说点什么...’")

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0128():
        Preconditions.make_already_in_message_page()
        mes = MessagePage()
        mes.click_add_icon()
        mes.click_free_sms()
        time.sleep(1)
        contacts = ContactsPage()
        names = contacts.get_contacts_name2()
        contacts.select_people_by_name(names[0])
        gcp = GroupChatPage()
        gcp.click_back()
        time.sleep(3)
        Preconditions.enter_private_chat_page()


    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_huangcaizui_A_0128(self):
        """进入发送页面"""
        # 1、进入一对一聊天界面
        chat = SingleChatPage()
        # 2、选择短信功能，进入短信发送模式
        try:
            chat.page_should_contain_text('退出短信')
            chat.click_text("退出短信")
        except:
            pass
        try:
            time.sleep(1)
            chat.page_should_contain_text("欢迎使用免费短信")
            chat.click_text("确定")
            time.sleep(2)
        except:
            pass
        chat.page_should_contain_text("发送短信")
        chat.page_should_contain_text("退出")
        chat.click_text("退出")

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0129():
        """该账号未开启过和飞信短信功能"""
        Preconditions.enter_private_chat_page(reset=True)

    @tags('ALL', 'SMOKE', 'CMCC_RESET', 'DEBUG')
    def test_msg_huangcaizui_A_0129(self):
        """进入发送页面"""
        # 1、进入一对一天界面
        chat = SingleChatPage()
        # 2、选择短信功能，进入短信发送模式
        chat.click_sms()
        time.sleep(1)
        chat.page_should_contain_text("欢迎使用免费短信")
        chat.page_should_contain_text("免费给移动用户发送短信")
        chat.page_should_contain_text("给非移动用户发短信将收取0.01元/条")
        chat.page_should_contain_text("给港澳台等境外用户发短信将收取1元/条")

    @staticmethod
    def setUp_test_msg_huangcaizui_B_0073():
        """该账号未开启过和飞信短信功能"""
        Preconditions.enter_private_chat_page(reset=True)

    @tags('ALL', 'SMOKE', 'CMCC_RESET', 'DEBUG')
    def test_msg_huangcaizui_B_0073(self):
        """进入发送页面"""
        # 1、进入一对一天界面
        chat = SingleChatPage()
        # 2、选择短信功能，进入短信发送模式
        chat.click_sms()
        time.sleep(1)
        chat.page_should_contain_text("欢迎使用免费短信")
        chat.page_should_contain_text("免费给移动用户发送短信")
        chat.page_should_contain_text("给非移动用户发短信将收取0.01元/条")
        chat.page_should_contain_text("给港澳台等境外用户发短信将收取1元/条")
        chat.click_text("确定")
        time.sleep(2)
        chat.page_should_contain_text("发送短信")
        chat.page_should_contain_text("您正在使用免费短信")
        chat.page_should_contain_text("退出短信")
        chat.click_text("退出短信")

    @staticmethod
    def setUp_test_msg_huangcaizui_B_0074():
        Preconditions.make_already_in_message_page()
        mes = MessagePage()
        mes.click_add_icon()
        mes.click_free_sms()
        time.sleep(1)
        contacts = ContactsPage()
        names = contacts.get_contacts_name2()
        contacts.select_people_by_name(names[0])
        gcp = GroupChatPage()
        gcp.click_back()
        time.sleep(3)
        Preconditions.enter_private_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_huangcaizui_B_0074(self):
        """进入发送页面"""
        # 1、进入一对一天界面
        chat = SingleChatPage()
        # 2、选择短信功能，进入短信发送模式
        try:
            chat.page_should_contain_text('退出短信')
            chat.click_text("退出短信")
        except:
            pass
        #chat.click_sms()
        try:
            time.sleep(1)
            chat.page_should_contain_text("欢迎使用免费短信")
            chat.click_text("确定")
            time.sleep(2)
        except:
            pass
        chat.page_should_contain_text("发送短信")
        chat.input_sms_message("123")
        time.sleep(1)
        chat.input_sms_message("")
        time.sleep(1)
        flag = chat.is_enabled_sms_send_btn()
        if flag:
            raise AssertionError('未输入信息时，短信发送按钮应该不可点击')
        chat.click_text("退出")

    @staticmethod
    def setUp_test_msg_huangcaizui_B_0075():
        Preconditions.make_already_in_message_page()
        mes = MessagePage()
        mes.click_add_icon()
        mes.click_free_sms()
        time.sleep(1)
        contacts = ContactsPage()
        names = contacts.get_contacts_name2()
        contacts.select_people_by_name(names[0])
        gcp = GroupChatPage()
        gcp.click_back()
        time.sleep(3)
        Preconditions.enter_private_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_huangcaizui_B_0075(self):
        """发送机制"""
        # 1、进入一对一天界面
        chat = SingleChatPage()
        # 2、选择短信功能，进入短信发送模式
        try:
            chat.page_should_contain_text('退出短信')
            chat.click_text("退出短信")
        except:
            pass
        #chat.click_sms()
        try:
            time.sleep(1)
            chat.page_should_contain_text("欢迎使用免费短信")
            chat.click_text("确定")
            time.sleep(2)
        except:
            pass
        chat.page_should_contain_text("发送短信")
        # 3、成功发送文字后，返回消息列表
        chat.input_sms_message('hello')
        chat.send_sms()
        if chat.is_present_sms_fee_remind():
            chat.click_text('发送',exact_match=True)
        # 返回消息列表则看见本条消息提示为[短信]
        chat.click_back()
        ContactDetailsPage().click_back()
        chat.click_back_by_android()
        time.sleep(1)
        mess = MessagePage()
        mess.open_message_page()
        mess.wait_for_page_load()
        mess.page_should_contain_text('[短信]')

    @staticmethod
    def setUp_test_msg_huangcaizui_B_0080():
        Preconditions.make_already_in_message_page()
        mes = MessagePage()
        mes.click_add_icon()
        mes.click_free_sms()
        time.sleep(1)
        contacts = ContactsPage()
        names = contacts.get_contacts_name2()
        contacts.select_people_by_name(names[0])
        gcp = GroupChatPage()
        gcp.click_back()
        time.sleep(3)
        Preconditions.enter_private_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_huangcaizui_B_0080(self):
        """发送机制"""
        # 1、进入一对一天界面
        chat = SingleChatPage()
        # 2、选择短信功能，进入短信发送模式
        try:
            chat.page_should_contain_text('退出短信')
            chat.click_text("退出短信")
        except:
            pass
        #chat.click_sms()
        try:
            time.sleep(1)
            chat.page_should_contain_text("欢迎使用免费短信")
            chat.click_text("确定")
            time.sleep(2)
        except:
            pass
        chat.page_should_contain_text("发送短信")
        chat.wait_for_page_load()
        # 2、断开网络
        current_mobile().set_network_status(0)
        # 3、a终端使用客户端短信状态发送一条消息
        chat.input_sms_message('hello')
        chat.send_sms()
        if chat.is_present_sms_fee_remind():
            chat.click_text('发送', exact_match=True)
        if not chat.is_msg_send_fail():
            raise AssertionError('断网发送短信，无发送失败标志！')
        chat.click_text("退出")

    @staticmethod
    def tearDown_test_msg_huangcaizui_B_0080():
        """恢复网络连接"""
        current_mobile().set_network_status(6)

    @staticmethod
    def setUp_test_msg_huangcaizui_B_0081():
        """该账号未开启过和飞信短信功能"""
        Preconditions.enter_private_chat_page(reset=True)

    @tags('ALL', 'SMOKE', 'CMCC_RESET', 'DEBUG')
    def test_msg_huangcaizui_B_0081(self):
        """发送机制"""
        # 1、进入客户端通知类短信聊天窗口
        chat = SingleChatPage()
        chat.click_sms()
        time.sleep(1)
        chat.page_should_contain_text("欢迎使用免费短信")
        chat.page_should_contain_text("免费给移动用户发送短信")
        chat.page_should_contain_text("给非移动用户发短信将收取0.01元/条")
        chat.page_should_contain_text("给港澳台等境外用户发短信将收取1元/条")
        chat.click_text("确定")
        time.sleep(2)
        chat.page_should_contain_text("发送短信")
        chat.page_should_contain_text("您正在使用免费短信")
        chat.page_should_contain_text("退出短信")
        # 2、使用短信状态发送一条聊天信息
        chat.input_sms_message('hello')
        chat.send_sms()
        if chat.is_present_sms_fee_remind():
            chat.click_text('发送', exact_match=True)
            time.sleep(2)
        chat.click_text("退出短信")
        time.sleep(1)
        chat.press_mess('hello')
        chat.page_should_contain_text('复制')
        chat.page_should_contain_text('删除')
        chat.driver.back()

    @staticmethod
    def public_send_file(file_type):
        # 1、在当前聊天会话页面，点击更多富媒体的文件按钮
        chat = SingleChatPage()
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

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_huangcaizui_A_0147(self):
        """会话窗口中点击删除文本消息"""
        self.public_send_file('.txt')
        # 1.长按文本消息
        chat = SingleChatPage()
        msg = '.txt'
        # 2.点击删除
        chat.delete_mess(msg)
        chat.page_should_not_contain_text(msg)

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0148():
        """该账号未开启过和飞信短信功能"""
        Preconditions.enter_private_chat_page(reset=True)

    @tags('ALL', 'SMOKE', 'CMCC_RESET', 'DEBUG')
    def test_msg_huangcaizui_A_0148(self):
        """会话窗口中首次点击撤回文本消息"""
        self.public_send_file('.txt')
        # 1.长按文本消息
        chat = SingleChatPage()
        msg = '.txt'
        # 2.点击撤回
        chat.recall_mess(msg)
        chat.wait_until(
            timeout=3,
            auto_accept_permission_alert=True,
            condition=lambda d: chat.is_text_present("知道了")
        )
        # 3.点击我知道了
        if not chat.is_text_present("知道了"):
            raise AssertionError('撤回文本消息，未弹出我知道了的提示')
        chat.click_i_know()
        chat.page_should_not_contain_text(msg)
        chat.page_should_contain_text("你撤回了一条信息")
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG')
    def test_msg_huangcaizui_A_0149(self):
        """会话窗口中非首次点击撤回文本消息"""
        self.public_send_file('.txt')
        # 1.长按文本消息
        chat = SingleChatPage()
        msg = '.txt'
        # 2.点击撤回
        chat.recall_mess(msg)
        time.sleep(1)
        if chat.is_text_present("知道了"):
            chat.click_i_know()
        chat.page_should_not_contain_text(msg)
        chat.page_should_contain_text("你撤回了一条信息")

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG_1')
    def test_msg_huangcaizui_A_0150(self):
        """会话窗口中点击收藏文本消息"""
        self.public_send_file('.txt')
        # 1.长按文本消息
        chat = SingleChatPage()
        msg = '.txt'
        # 2.点击收藏
        chat.collection_file(msg)
        if not chat.is_toast_exist("已收藏", timeout=10):
            raise AssertionError("收藏文件无'已收藏'提示！")

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG_1')
    def test_msg_huangcaizui_A_0151(self):
        """进入到单聊天会话页面，发送一条字符等于5000的文本消息"""
        # 1、在输入框中输入5000个字符，右边的语音按钮是否自动变为发送按钮
        chat = SingleChatPage()
        info = "呵呵" * 2500
        chat.input_message(info)
        # 2、点击发送按钮，输入框中的内容是否可以成功发送出去
        chat.page_should_contain_send_btn()
        chat.send_message()
        chat.page_should_contain_text("呵呵")

    @tags('ALL', 'SMOKE', 'CMCC', 'DEBUG_1')
    def test_msg_huangcaizui_A_0152(self):
        """进入到单聊天会话页面，发送一条字符等于5001的文本消息"""
        # 1、在输入框中输入5001个字符，是否可以可以输入此段字符
        chat = SingleChatPage()
        info = "呵呵" * 2501
        chat.input_message(info)
        chat.page_should_contain_send_btn()
        info = chat.get_input_message()
        if not len(info) == 5000:
            raise AssertionError("输入框可以输入超过5000个字符")
        chat.input_message('')


class MsgPrivateChatMyComputer(TestCase):
    """模块：单聊->图片->我的电脑"""
    @classmethod
    def setUpClass(cls):
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        Preconditions.init_contact_group_data()

    def default_setUp(self):
        """当前页面在我的电脑聊天会话页面"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            pass
        else:
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
        mess.wait_for_page_load()
        time.sleep(1)
        mess.click_search()
        # 搜索
        if SearchPage().is_text_present('始终允许'):
            SearchPage().click_text("始终允许")
        SearchPage().input_search_keyword("我的电脑")
        time.sleep(2)
        current_mobile().hide_keyboard_if_display()
        mess.click_search_my_computer()

    @tags('ALL', 'CMCC', 'yxyx')
    def test_msg_huangcaizui_D_0029(self):
        """我的电脑会话页面，编辑图片发送"""
        # 1、成功登录和飞信
        # 2、当前页面在我的电脑聊天会话页面
        cwp = ChatWindowPage()
        cwp.wait_for_page_load()
        # 1.点击输入框左上方的相册图标
        cwp.click_img_msgs()
        # 2.进入相片页面,选择一张图片
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk(1)
        # 3.点击预览
        cpg.click_preview()
        cpp = ChatPicPreviewPage()
        cpp.wait_for_page_load()
        # 4.点击编辑（预览图片）
        cpp.click_edit()
        cpe = ChatPicEditPage()
        # 5.点击文本编辑（预览图片）
        cpe.click_picture_edit()
        # 6.涂鸦动作
        cpe.click_picture_edit_crred()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # 7.马赛克动作
        cpe.click_picture_mosaic()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # 8.文本编辑动作
        cpe.click_picture_text()
        cpe.click_picture_edit_crred()
        cpe.input_picture_text("我是python测试开发工程师")
        time.sleep(1)
        # 9.点击编辑完成
        cpe.click_picture_save()
        # 10.点击发送
        cpe.click_picture_send()
        # 11.判断是否发送成功
        cwp.wait_for_msg_send_status_become_to("发送成功", 30)
        time.sleep(2)

    @tags('ALL', 'CMCC', 'yxyx')
    def test_msg_huangcaizui_D_0030(self):
        """我的电脑会话页面，编辑图片不保存发送"""
        # 1、成功登录和飞信
        # 2、当前页面在我的电脑聊天会话页面
        cwp = ChatWindowPage()
        cwp.wait_for_page_load()
        # 1.点击输入框左上方的相册图标
        cwp.click_img_msgs()
        # 2.进入相片页面,选择一张图片
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk(1)
        # 3.点击预览
        cpg.click_preview()
        cpp = ChatPicPreviewPage()
        time.sleep(1)
        # 4.点击编辑（预览图片）
        cpp.click_edit()
        cpe = ChatPicEditPage()
        # 5.点击文本编辑（预览图片）
        cpe.click_picture_edit()
        # 6.涂鸦动作
        cpe.click_picture_edit_crred()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # 7.马赛克动作
        cpe.click_picture_mosaic()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # 8.文本编辑动作
        cpe.click_picture_text()
        cpe.click_picture_edit_crred()
        cpe.input_picture_text("我是python测试开发工程师")
        time.sleep(1)
        current_mobile().hide_keyboard_if_display()
        # 点击完成
        cpe.click_picture_complete()
        # 9.点击发送
        cpe.click_picture_send()
        # 10.判断是否发送成功
        time.sleep(20)
        gcp = GroupChatPage()
        result = gcp.is_send_sucess()
        self.assertTrue(result)

    @tags('ALL', 'CMCC', 'yxyx')
    def test_msg_huangcaizui_D_0031(self):
        """我的电脑会话页面，编辑图片中途直接发送"""
        # 1、成功登录和飞信
        # 2、当前页面在我的电脑聊天会话页面
        cwp = ChatWindowPage()
        cwp.wait_for_page_load()
        # 1.点击输入框左上方的相册图标
        cwp.click_img_msgs()
        # 2.进入相片页面,选择一张图片
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk(1)
        # 3.点击预览
        cpg.click_preview()
        cpp = ChatPicPreviewPage()
        time.sleep(1)
        # 4.点击编辑（预览图片）
        cpp.click_edit()
        cpe = ChatPicEditPage()
        # 5.点击文本编辑（预览图片）
        cpe.click_picture_edit()
        # 6.涂鸦动作
        cpe.click_picture_edit_crred()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # 7.马赛克动作
        cpe.click_picture_mosaic()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # 8.文本编辑动作
        cpe.click_picture_text()
        cpe.click_picture_edit_crred()
        cpe.input_picture_text("我是python测试开发工程师")
        current_mobile().hide_keyboard_if_display()
        # 点击完成
        cpe.click_picture_complete()
        # 9.点击发送
        cpe.click_picture_send()
        # 10.判断是否发送成功
        time.sleep(20)
        gcp = GroupChatPage()
        result = gcp.is_send_sucess()
        self.assertTrue(result)

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_huangcaizui_D_0032(self):
        """我的电脑会话页面，编辑图片保存"""
        # 1、成功登录和飞信
        # 2、当前页面在我的电脑聊天会话页面
        cwp = ChatWindowPage()
        cwp.wait_for_page_load()
        # 1.点击输入框左上方的相册图标
        cwp.click_img_msgs()
        # 2.进入相片页面,选择一张图片
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk(1)
        # 3.点击预览
        cpg.click_preview()
        cpp = ChatPicPreviewPage()
        time.sleep(1)
        # 4.点击编辑（预览图片）
        cpp.click_edit()
        cpe = ChatPicEditPage()
        # 5.点击文本编辑（预览图片）
        cpe.click_picture_edit()
        # 6.涂鸦动作
        cpe.click_picture_edit_crred()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # 7.马赛克动作
        cpe.click_picture_mosaic()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # 8.文本编辑动作
        cpe.click_picture_text()
        cpe.click_picture_edit_crred()
        cpe.input_picture_text("我是python测试开发工程师")
        time.sleep(1)
        # 9.点击完成
        cpe.click_picture_save()
        # 10.点击保存
        cpe.click_picture_save()
        if not cpe.is_toast_exist("保存成功"):
            raise AssertionError("没有保存成功")

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_huangcaizui_D_0033(self):
        """我的电脑会话页面，取消编辑图片"""
        # 1、成功登录和飞信
        # 2、当前页面在我的电脑聊天会话页面
        cwp = ChatWindowPage()
        cwp.wait_for_page_load()
        # 1.点击输入框左上方的相册图标
        cwp.click_img_msgs()
        # 2.进入相片页面,选择一张图片
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk(1)
        # 3.点击预览
        cpg.click_preview()
        cpp = ChatPicPreviewPage()
        time.sleep(1)
        # 4.点击编辑（预览图片）
        cpp.click_edit()
        cpe = ChatPicEditPage()
        # 5.点击文本编辑（预览图片）
        cpe.click_picture_edit()
        # 6.涂鸦动作
        cpe.click_picture_edit_crred()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # 7.马赛克动作
        cpe.click_picture_mosaic()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # 8.文本编辑动作
        cpe.click_picture_text()
        cpe.click_picture_edit_crred()
        cpe.input_picture_text("我是python测试开发工程师")
        time.sleep(1)
        # 9.点击取消编辑
        cpe.click_cancle()
        time.sleep(2)

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_huangcaizui_D_0034(self):
        """我的电脑会话页面，取消编辑图片，点击发送按钮"""
        # 1、成功登录和飞信
        # 2、当前页面在我的电脑聊天会话页面
        cwp = ChatWindowPage()
        cwp.wait_for_page_load()
        # 1.点击输入框左上方的相册图标
        cwp.click_img_msgs()
        # 2.进入相片页面,选择一张图片
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic_fk(1)
        # 3.点击预览
        cpg.click_preview()
        cpp = ChatPicPreviewPage()
        time.sleep(1)
        # 4.点击编辑（预览图片）
        cpp.click_edit()
        cpe = ChatPicEditPage()
        # 5.点击文本编辑（预览图片）
        cpe.click_picture_edit()
        # 6.涂鸦动作
        cpe.click_picture_edit_crred()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # 7.马赛克动作
        cpe.click_picture_mosaic()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # 8.文本编辑动作
        cpe.click_picture_text()
        cpe.click_picture_edit_crred()
        cpe.input_picture_text("我是python测试开发工程师")
        time.sleep(1)
        # 9.点击取消编辑
        cpe.click_cancle()
        time.sleep(2)
        # 10.点击发送
        current_mobile().hide_keyboard_if_display()
        cpe.click_picture_send()
        time.sleep(10)
        # 10.判断是否发送成功
        cwp.wait_for_msg_send_status_become_to("发送成功")
        time.sleep(2)

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_huangcaizui_D_0035(self):
        """我的电脑会话页面，发送相册内的图片"""
        # 1、成功登录和飞信
        # 2、当前页面在我的电脑聊天会话页面
        cwp = ChatWindowPage()
        cwp.wait_for_page_load()
        # 1.点击输入框左上方的相册图标
        cwp.click_img_msgs()
        # 2.选择一张图片
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.click_pic_preview()
        cppp = ChatPicPreviewPage()
        cppp.wait_for_page_load()
        # 3、当前图片的左上角是否会展示格式为：当前图片张数/当前相册的总张数
        preview_info = cppp.get_pic_preview_info()
        self.assertIsNotNone(re.match(r'预览\(\d+/\d+\)', preview_info))
        time.sleep(3)

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_huangcaizui_D_0041(self):
        """我的电脑会话页面，使用拍照功能拍照编辑后发送照片"""
        # 1、成功登录和飞信
        # 2、当前页面在我的电脑聊天会话页面
        cwp = ChatWindowPage()
        cwp.wait_for_page_load()
        # 1.点击富媒体行拍照图标
        cwp.click_photo()
        cpp = ChatPhotoPage()
        cpp.wait_for_page_load()
        # 2.进入相机拍照页面，点击拍照
        cpp.take_photo()
        # 3.点击编辑拍摄的照片
        cpp.click_edit_pic()
        cpe = ChatPicEditPage()
        # 4.编辑照片
        cpe.click_text_edit_btn()
        cpe.click_picture_edit_crred()
        cpe.input_picture_text("编辑照片")
        time.sleep(1)
        # 5.点击编辑完成
        cpe.click_picture_save()
        # 6.点击发送
        cpe.click_send()
        cwp.wait_for_page_load()
        # 7.判断是否发送成功
        cwp.wait_for_msg_send_status_become_to("发送成功", 30)

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_huangcaizui_D_0042(self):
        """我的电脑会话页面，使用拍照功能拍照之后编辑并保存"""
        # 1、成功登录和飞信
        # 2、当前页面在我的电脑聊天会话页面
        cwp = ChatWindowPage()
        cwp.wait_for_page_load()
        # 1.点击富媒体行拍照图标
        cwp.click_photo()
        cpp = ChatPhotoPage()
        cpp.wait_for_page_load()
        # 2.进入相机拍照页面，点击拍照
        cpp.take_photo()
        # 3.点击编辑拍摄的照片
        cpp.click_edit_pic()
        cpe = ChatPicEditPage()
        # 4.编辑照片
        cpe.click_text_edit_btn()
        cpe.click_picture_edit_crred()
        cpe.input_picture_text("编辑照片")
        time.sleep(1)
        # 5.点击编辑完成
        cpe.click_picture_save()
        # 6.点击保存
        cpe.click_picture_save()
        if not cpe.is_toast_exist("保存成功"):
            raise AssertionError("没有保存成功")
        # 7.点击发送
        cpe.click_send()
        cwp.wait_for_page_load()
        # 8.判断是否发送成功
        cwp.wait_for_msg_send_status_become_to("发送成功", 30)

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_huangcaizui_D_0043(self):
        """我的电脑会话页面，使用拍照功能拍照编辑图片，再取消编辑并发送"""
        # 1、成功登录和飞信
        # 2、当前页面在我的电脑聊天会话页面
        cwp = ChatWindowPage()
        cwp.wait_for_page_load()
        # 1.点击富媒体行拍照图标
        cwp.click_photo()
        cpp = ChatPhotoPage()
        cpp.wait_for_page_load()
        # 2.进入相机拍照页面，点击拍照
        cpp.take_photo()
        # 3.点击编辑拍摄的照片
        cpp.click_edit_pic()
        cpe = ChatPicEditPage()
        # 4.编辑照片
        cpe.click_text_edit_btn()
        cpe.click_picture_edit_crred()
        cpe.input_picture_text("编辑照片")
        time.sleep(1)
        # 5.点击取消编辑
        cpe.click_cancle()
        time.sleep(2)
        # 6.点击发送
        cpe.click_picture_send()
        cwp.wait_for_page_load()
        # 7.判断是否发送成功
        cwp.wait_for_msg_send_status_become_to("发送成功", 30)

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_huangcaizui_D_0050(self):
        """在我的电脑会话窗，断网情况下发送表情搜搜"""
        # 1、网络异常
        # 2、已登录客户端
        # 3、当前页面在我的电脑聊天会话页面
        cwp = ChatWindowPage()
        cwp.set_network_status(0)
        cwp.wait_for_page_load()
        cwp.click_expression()
        time.sleep(2)
        cwp.click_gif()
        flag = cwp.is_toast_exist("网络不可用，请检查网络设置")
        if not flag:
            raise AssertionError("没有'网络异常，请重新设置网络'提示")

    @staticmethod
    def tearDown_test_msg_huangcaizui_D_0050():
        """恢复网络连接"""
        current_mobile().set_network_status(6)

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_huangcaizui_D_0056(self):
        """在我的电脑会话窗，趣图发送失败后出现重新发送按钮"""
        # 1、网络正常
        # 2、已登录客户端
        # 3、在会话窗口页面
        cwp = ChatWindowPage()
        # 1.如果当前我的电脑会话窗已有消息发送失败标识，需要先清除消息发送失败标识
        if not cwp.is_send_sucess():
            cwp.click_send_again()
        cwp.wait_for_page_load()
        # 2.点击表情
        cwp.click_expression()
        time.sleep(2)
        cwp.click_gif()
        # 3.输入框输入1
        cwp.input_gif("1")
        cwp.wait_for_gif_ele_load()
        # 4.断开网络
        cwp.set_network_status(0)
        # 断网后gif图片无法加载,不能点击gif图片发送
        # cwp.click_1_gif()
        # 点击发送
        cwp.click_send_button()
        # 5.检验发送失败的标识
        if cwp.is_send_sucess():
            raise AssertionError("没有显示消息发送失败标识")
        cwp.wait_for_msg_send_status_become_to('发送失败', 30)
        # 6.重新连接网络
        cwp.set_network_status(6)
        # 7.点击重发
        cwp.click_send_again()
        # 8.验证是否发送成功
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_xiaoqiu_0532(self):
        """我的电脑聊天会话页面——放大发送一段表情文本内容"""
        # 1、网络正常
        # 2、已登录和飞信
        # 3、我的电脑会话窗口
        cwp = ChatWindowPage()
        cwp.wait_for_page_load()
        # 1.点击表情
        cwp.click_expression()
        # 2.选择1个表情正常发送，获取文本宽度
        cwp.select_expression()
        cwp.click_send_button()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        time.sleep(1)
        cwp.click_expression()
        cwp.hide_keyboard()
        time.sleep(2)
        width1 = cwp.get_width_of_last_msg_of_text()
        time.sleep(1)
        # 3.选择1个表情放大发送，获取文本宽度
        cwp.click_expression()
        cwp.select_expression()
        time.sleep(1)
        cwp.press_and_move_up('发送按钮')
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        cwp.click_expression()
        cwp.hide_keyboard()
        time.sleep(2)
        width2 = cwp.get_width_of_last_msg_of_text()
        # 5.判断是否放大
        if not width2 > width1:
            raise AssertionError("表情没有放大展示")

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_xiaoqiu_0533(self):
        """我的电脑聊天会话页面——缩小发送一段表情文本内容"""
        # 1、网络正常
        # 2、已登录和飞信
        # 3、我的电脑会话窗口
        cwp = ChatWindowPage()
        cwp.wait_for_page_load()
        # 1.点击表情
        cwp.click_expression()
        # 2.选择1个表情正常发送，获取文本宽度
        cwp.select_expression()
        cwp.click_send_button()
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        time.sleep(1)
        cwp.click_expression()
        cwp.hide_keyboard()
        width1 = cwp.get_width_of_last_msg_of_text()
        time.sleep(1)
        # 3.选择1个表情缩小发送，获取文本宽度
        cwp.click_expression()
        cwp.select_expression()
        time.sleep(1)
        cwp.press_and_move_down('发送按钮')
        try:
            cwp.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        cwp.click_expression()
        cwp.hide_keyboard()
        width2 = cwp.get_width_of_last_msg_of_text()
        # 5.判断是否缩小
        if not width2 < width1:
            raise AssertionError("表情没有缩小展示")

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_weifenglian_PC_0336(self):
        """我的电脑发送位置成功"""
        # 1、网络正常
        # 2、已开启手机定位
        # 3、当前在我的电脑会话窗口页面
        cwp = ChatWindowPage()
        cwp.wait_for_page_load()
        # 1.点击更多
        cwp.click_add_icon()
        # 2.点击位置
        cwp.click_location()
        # 备注：地图位置加载不出来
        try:
            clp = ChatLocationPage()
            clp.wait_for_page_load(20)
            time.sleep(1)
            # 3.点击发送按钮
            if not clp.send_btn_is_enabled():
                raise AssertionError("位置页面发送按钮不可点击")
            clp.click_send()
            # 4.判断在消息聊天窗口是否展示缩略位置消息体
            self.assertTrue(cwp.is_address_text_present())
        except:
            pass

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_huangcaizui_D_0005(self):
        """在我的电脑面板点击发消息到我的电脑按钮后进入我的电脑会话窗口"""
        # 1、当前页面在我的电脑面板
        cwp = ChatWindowPage()
        cwp.wait_for_page_load()
        # 1.验证是否在我的电脑会话窗口
        self.assertTrue(cwp.is_text_present("我的电脑"))
        # 2.验证各个功能是否正常显示
        self.assertTrue(cwp.is_page_contain_element())
        time.sleep(2)


class MsgPrivateChatPicture(TestCase):
    """单聊->图片过大发送逻辑优化"""

    @classmethod
    def setUpClass(cls):
        warnings.simplefilter('ignore', ResourceWarning)
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        Preconditions.init_contact_group_data()

    def default_setUp(self):
        """确保每个用例运行前在单聊会话页面"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_private_chat_page()
            return
        chat = SingleChatPage()
        if chat.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_private_chat_page()

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_xiaoliping_C_0211(self):
        """在会话窗口点击图片按钮进入相册，都选原图再选择一张大于20M的照片，然后进行发送"""
        # 1、网络正常
        # 2、当前在单聊会话窗口页面
        scp = SingleChatPage()
        scp.wait_for_page_load()
        # 1.点击输入框左上方的相册图标
        scp.click_picture()
        time.sleep(1)
        scp.switch_to_given_folder("pic")
        # 2.点击原图
        scp.click_original_photo()
        # 3.选择大于20M的图片
        scp.select_items_by_given_orders(1)
        cpp = ChatPicPreviewPage()
        # 4.点击发送
        cpp.click_picture_send()
        # 5.判断存在发送失败按钮
        # self.assertTrue(scp.is_send_sucess())
        # 6.点击图片
        scp.click_msg_image(0)
        time.sleep(2)
        # 7.长按图片
        scp.press_xy()
        time.sleep(3)
        # 8.判断是否出现编辑选项
        result = scp.is_exist_picture_edit_page()
        self.assertTrue(result)
        # 9.点击图片编辑
        scp.click_edit()
        cpe = ChatPicEditPage()
        # 10.点击文本编辑（预览图片）
        cpe.click_picture_edit()
        # 11.涂鸦动作
        cpe.click_picture_edit_crred()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # 12.马赛克动作
        cpe.click_picture_mosaic()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # 13.文本编辑动作
        cpe.click_picture_text()
        cpe.click_picture_edit_crred()
        cpe.input_picture_text("图片编辑")
        time.sleep(1)

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_xiaoliping_C_0212(self):
        """在会话窗口点击图片按钮进入相册，选择一张大于20M的照片，进入图片预览页面勾选原图，然后进行发送"""
        # 1、网络正常
        # 2、当前在单聊会话窗口页面
        scp = SingleChatPage()
        scp.wait_for_page_load()
        # 1.点击输入框左上方的相册图标
        scp.click_picture()
        time.sleep(1)
        # 2.选择大于20M的图片
        scp.switch_to_given_folder("pic")
        scp.select_items_by_given_orders(1)
        # 3.点击预览
        scp.click_preview()
        time.sleep(1)
        cpp = ChatPicPreviewPage()
        # 4.点击原图
        scp.click_original_photo()
        # 5.点击发送
        cpp.click_picture_send()
        # 6.判断是否存在发送失败按钮
        # self.assertTrue(scp.is_send_sucess())
        # 7.点击图片
        scp.click_msg_image(0)
        time.sleep(2)
        # 8.长按图片
        scp.press_xy()
        time.sleep(3)
        # 9.判断是否出现编辑选项
        self.assertTrue(scp.is_exist_picture_edit_page())
        # 10.点击图片编辑
        scp.click_edit()
        cpe = ChatPicEditPage()
        # 11.点击文本编辑（预览图片）
        cpe.click_picture_edit()
        # 12.涂鸦动作
        cpe.click_picture_edit_crred()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # 13.马赛克动作
        cpe.click_picture_mosaic()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # 14.文本编辑动作
        cpe.click_picture_text()
        cpe.click_picture_edit_crred()
        cpe.input_picture_text("图片编辑")
        time.sleep(1)

    @staticmethod
    def setUp_test_msg_xiaoliping_C_0306():
        """确保当前页面在标签分组会话页面"""
        Preconditions.select_mobile('Android-移动')
        # 确保应用在消息页面
        Preconditions.make_already_in_message_page()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status()
        # 进入标签分组会话页面
        Preconditions.enter_label_grouping_chat_page()

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_xiaoliping_C_0306(self):
        """在会话窗口点击图片按钮进入相册，直接勾选原图，选择一张等于20M的照片进行发送"""
        # 1、网络正常
        # 2、当前在标签分组会话窗口页面
        lgcp = LabelGroupingChatPage()
        # 1.点击输入框左上方照片
        lgcp.click_picture()
        ps = PictureSelector()
        time.sleep(1)
        # 2.选择大于20M的图片
        ps.switch_to_given_folder("pic")
        ps.select_items_by_given_orders(1)
        cpp = ChatPicPreviewPage()
        # 3.点击原图
        cpp.click_original_photo()
        # 4.点击发送
        cpp.click_picture_send()
        # 5.判断存在发送失败按钮
        # self.assertFalse(lgcp.is_send_sucess())
        # 6.点击返回消息列表
        lgcp.click_back()
        lgp = LabelGroupingPage()
        lgp.click_back()
        cdp = ContactDetailsPage()
        cdp.click_back()
        contacts = ContactsPage()
        contacts.click_back()
        contacts.click_message_icon()
        mess = MessagePage()
        mess.wait_for_page_load()
        # 7.判断是否显示消息发送失败的标识
        if mess.is_iv_fail_status_present():
            raise AssertionError("消息列表显示消息发送失败标识")

    @staticmethod
    def setUp_test_msg_xiaoliping_C_0307():
        """确保当前页面在标签分组会话页面"""
        Preconditions.select_mobile('Android-移动')
        # 确保应用在消息页面
        Preconditions.make_already_in_message_page()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status()
        # 进入标签分组会话页面
        Preconditions.enter_label_grouping_chat_page()

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_xiaoliping_C_0307(self):
        """在会话窗口点击图片按钮进入相册，直接勾选原图，选择一张等于20M的照片进行发送"""
        # 1、网络正常
        # 2、当前在标签分组会话窗口页面
        lgcp = LabelGroupingChatPage()
        # 1.点击输入框左上方照片
        lgcp.click_picture()
        ps = PictureSelector()
        time.sleep(1)
        # 2.选择等于20M的图片
        ps.switch_to_given_folder("pic")
        ps.select_items_by_given_orders(1)
        cpp = ChatPicPreviewPage()
        # 3.点击原图
        cpp.click_original_photo()
        # 4.点击发送
        cpp.click_picture_send()
        # 5.判断是否发送成功
        lgcp.wait_for_msg_send_status_become_to("发送成功", 30)
        time.sleep(2)

    @staticmethod
    def setUp_test_msg_xiaoliping_C_0308():
        """确保当前页面在标签分组会话页面"""
        Preconditions.select_mobile('Android-移动')
        # 确保应用在消息页面
        Preconditions.make_already_in_message_page()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status()
        # 进入标签分组会话页面
        Preconditions.enter_label_grouping_chat_page()

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_xiaoliping_C_0308(self):
        """在会话窗口点击图片按钮进入相册，选择一张等于20M的照片，进入图片预览页面勾选原图，然后进行发送"""
        # 1、网络正常
        # 2、当前在标签分组会话窗口页面
        lgcp = LabelGroupingChatPage()
        # 1.点击输入框左上方照片
        lgcp.click_picture()
        ps = PictureSelector()
        time.sleep(1)
        # 2.选择等于20M的图片
        ps.switch_to_given_folder("pic")
        ps.select_items_by_given_orders(1)
        # 3.点击预览
        ps.click_preview()
        cpp = ChatPicPreviewPage()
        # 4.点击原图
        cpp.click_original_photo()
        # 5.点击发送
        cpp.click_picture_send()
        # 6.判断是否发送成功
        lgcp.wait_for_msg_send_status_become_to("发送成功", 30)
        time.sleep(2)

    @staticmethod
    def setUp_test_msg_xiaoliping_C_0309():
        """确保当前页面在标签分组会话页面"""
        Preconditions.select_mobile('Android-移动')
        # 确保应用在消息页面
        Preconditions.make_already_in_message_page()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status()
        # 进入标签分组会话页面
        Preconditions.enter_label_grouping_chat_page()

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_xiaoliping_C_0309(self):
        """在会话窗口点击图片按钮进入相册，直接勾选原图，选择一张小于20M的照片进行发送"""
        # 1、网络正常
        # 2、当前在标签分组会话窗口页面
        lgcp = LabelGroupingChatPage()
        # 1.点击输入框左上方照片
        lgcp.click_picture()
        ps = PictureSelector()
        time.sleep(1)
        # 2.选择小于20M的图片
        ps.switch_to_given_folder("pic")
        ps.select_items_by_given_orders(1)
        cpp = ChatPicPreviewPage()
        # 3.点击原图
        cpp.click_original_photo()
        # 4.点击发送
        cpp.click_picture_send()
        # 5.判断是否发送成功
        lgcp.wait_for_msg_send_status_become_to("发送成功", 30)
        time.sleep(2)

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_xiaoliping_C_0310(self):
        """在会话窗口点击图片按钮进入相册，选择一张小于20M的照片，进入图片预览页面勾选原图，然后进行发送"""
        # 1、网络正常
        # 2、当前在标签分组会话窗口页面
        lgcp = LabelGroupingChatPage()
        # 1.点击输入框左上方照片
        lgcp.click_picture()
        ps = PictureSelector()
        time.sleep(1)
        # 2.选择小于20M的图片
        ps.switch_to_given_folder("pic")
        ps.select_items_by_given_orders(1)
        # 3.点击预览
        ps.click_preview()
        cpp = ChatPicPreviewPage()
        # 4.点击原图
        cpp.click_original_photo()
        # 5.点击发送
        cpp.click_picture_send()
        # 6.判断是否发送成功
        lgcp.wait_for_msg_send_status_become_to("发送成功", 30)
        time.sleep(2)

    @staticmethod
    def setUp_test_msg_xiaoliping_C_0311():
        """确保当前页面在标签分组会话页面"""
        Preconditions.select_mobile('Android-移动')
        # 确保应用在消息页面
        Preconditions.make_already_in_message_page()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        Preconditions.make_no_message_send_failed_status()
        # 进入标签分组会话页面
        Preconditions.enter_label_grouping_chat_page()

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_xiaoliping_C_0311(self):
        """在会话窗口点击图片按钮进入相册，直接勾选原图，选择多张大于20M的照片进行发送"""
        # 1、网络正常
        # 2、当前在标签分组会话窗口页面
        lgcp = LabelGroupingChatPage()
        # 1.点击输入框左上方照片
        lgcp.click_picture()
        ps = PictureSelector()
        time.sleep(1)
        # 2.选择多张大于20m的图片
        ps.switch_to_given_folder("pic")
        ps.select_items_by_given_orders(1, 2)
        # 3.点击预览
        ps.click_preview()
        cpp = ChatPicPreviewPage()
        # 4.点击原图
        cpp.click_original_photo()
        # 5.点击发送
        cpp.click_picture_send()
        # 6.判断存在发送失败按钮
        # self.assertFalse(lgcp.is_send_sucess())
        lgcp.press_picture()
        time.sleep(3)
        # 7.判断是否出现编辑选项
        self.assertTrue(lgcp.is_exist_edit_page())
        lgcp.click_edit()
        cpe = ChatPicEditPage()
        # 8.点击文本编辑（预览图片）
        cpe.click_picture_edit()
        # 9.涂鸦动作
        cpe.click_picture_edit_crred()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # 10.马赛克动作
        cpe.click_picture_mosaic()
        cpe.click_picture_edit_switch()
        time.sleep(1)
        # 11.文本编辑动作
        cpe.click_picture_text()
        cpe.click_picture_edit_crred()
        cpe.input_picture_text("图片编辑")
        time.sleep(1)

