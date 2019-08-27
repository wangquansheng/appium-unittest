import time

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from preconditions.BasePreconditions import LoginPreconditions

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    'Android-XX': ''  # 用来发短信
}


class Preconditions(LoginPreconditions):
    """前置条件"""

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

    @staticmethod
    def get_label_grouping_name():
        """获取群名"""
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "alg" + phone_number[-4:]
        return group_name

    @staticmethod
    def reset_and_relaunch_app():
        """首次启动APP（使用重置APP代替）"""
        app_package = 'com.chinasofti.rcs'
        current_driver().activate_app(app_package)
        current_mobile().reset_app()

    @staticmethod
    def connect_mobile(category):
        """选择手机手机"""
        client = switch_to_mobile(REQUIRED_MOBILES[category])
        client.connect_mobile()
        return client

    @staticmethod
    def enter_local_file_catalog():
        """进入本地预置文件目录"""

        chat = LabelGroupingChatPage()
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
        # 进入预置文件目录，选择文件发送
        local_file.push_preset_file()
        local_file.click_preset_file_dir()

    @staticmethod
    def send_local_file(file_type):
        """发送本地文件夹文件"""
        Preconditions.enter_local_file_catalog()
        local_file=ChatSelectLocalFilePage()
        local_file.select_file(file_type)
        local_file.click_send()
        ChatWindowPage().wait_for_page_load()

    @staticmethod
    def public_open_file_network_broken(file_type):
        """断网状态在聊天会话页面打开文件"""
        chat = LabelGroupingChatPage()
        Preconditions.send_local_file(file_type)
        chat.wait_for_page_load()
        chat.set_network_status(0)
        chat.open_file_in_chat_page(file_type)
        chat.wait_for_open_file()
        chat.click_back_in_open_file_page()
        chat.wait_for_page_load()
        chat.set_network_status(6)

    @staticmethod
    def public_open_file_network_ok(file_type):
        """正常状态在聊天会话页面打开文件"""
        chat = LabelGroupingChatPage()
        Preconditions.send_local_file(file_type)
        chat.wait_for_page_load()
        chat.open_file_in_chat_page(file_type)
        chat.wait_for_open_file()
        chat.click_back_in_open_file_page()
        chat.wait_for_page_load()

    @staticmethod
    def enter_local_video_catalog():
        """进入本地视频目录"""

        # 在当前聊天会话页面，点击更多富媒体的文件按钮
        lgcp = LabelGroupingChatPage()
        lgcp.wait_for_page_load()
        lgcp.click_more()
        cmp = ChatMorePage()
        cmp.click_file()
        csfp = ChatSelectFilePage()
        # 等待选择文件页面加载
        csfp.wait_for_page_load()
        # 点击本地视频
        csfp.click_video()

    @staticmethod
    def send_large_video_file():
        """发送大型视频文件"""

        # 进入本地视频目录
        Preconditions.enter_local_video_catalog()
        local_file = ChatSelectLocalFilePage()
        # 发送大型视频文件
        flag = local_file.click_large_file()
        if not flag:
            local_file.push_preset_file()
            local_file.click_back()
            csfp = ChatSelectFilePage()
            csfp.click_video()
            local_file.click_large_file()
        local_file.click_send_button()

    @staticmethod
    def enter_local_picture_catalog():
        """进入本地照片目录"""

        # 在当前聊天会话页面，点击更多富媒体的文件按钮
        lgcp = LabelGroupingChatPage()
        lgcp.wait_for_page_load()
        lgcp.click_more()
        cmp = ChatMorePage()
        cmp.click_file()
        csfp = ChatSelectFilePage()
        # 等待选择文件页面加载
        csfp.wait_for_page_load()
        # 点击本地照片
        csfp.click_pic()

    @staticmethod
    def send_large_picture_file():
        """发送大型照片文件"""

        # 进入本地照片目录
        Preconditions.enter_local_picture_catalog()
        local_file = ChatSelectLocalFilePage()
        # 发送大型照片文件
        flag = local_file.click_large_file()
        if not flag:
            local_file.push_preset_file()
            local_file.click_back()
            csfp = ChatSelectFilePage()
            csfp.click_pic()
            local_file.click_large_file()
        local_file.click_send_button()

    @staticmethod
    def enter_local_music_catalog():
        """进入本地音乐目录"""

        # 在当前聊天会话页面，点击更多富媒体的文件按钮

        lgcp = LabelGroupingChatPage()
        lgcp.wait_for_page_load()
        lgcp.click_more()
        cmp = ChatMorePage()
        cmp.click_file()
        csfp = ChatSelectFilePage()
        # 等待选择文件页面加载
        csfp.wait_for_page_load()
        # 点击本地音乐
        csfp.click_music()
        time.sleep(2)

    @staticmethod
    def send_large_music_file():
        """发送大型音乐文件"""

        # 进入本地音乐目录
        Preconditions.enter_local_music_catalog()
        local_file = ChatSelectLocalFilePage()
        # 发送大型音乐文件
        flag = local_file.click_large_file()
        if not flag:
            local_file.push_preset_file()
            local_file.click_back()
            csfp = ChatSelectFilePage()
            csfp.click_music()
            local_file.click_large_file()
        local_file.click_send_button()


class MsgLabelGroupingAll(TestCase):
    """模块：消息-标签分组-文件"""

    @classmethod
    def setUpClass(cls):
        # 备注：脚本中已判断预支文件是否存在
        pass

    def default_setUp(self):
        """确保每个用例运行前在标签分组会话页面"""
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_label_grouping_chat_page()
            return
        chat = LabelGroupingChatPage()
        if chat.is_on_this_page():
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_label_grouping_chat_page()

    def default_tearDown(self):
        pass

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0001(self):
        """勾选本地文件内任意文件点击发送按钮"""
        # 1、在当前聊天会话页面，点击更多富媒体的文件按钮
        Preconditions.enter_local_file_catalog()
        local_file = ChatSelectLocalFilePage()
        chat = LabelGroupingChatPage()
        csf = ChatSelectFilePage()
        file = local_file.select_file(".txt")
        if file:
            local_file.click_send()
        else:
            local_file.click_back()
            time.sleep(1)
            local_file.click_back()
            time.sleep(1)
            csf.click_back()
            time.sleep(1)
        chat.wait_for_page_load()

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0002(self):
        """网络异常时勾选本地文件内任意文件点击发送按钮"""
        # 1、在当前聊天会话页面，断开网络，点击更多富媒体的文件按钮
        chat = LabelGroupingChatPage()
        chat.set_network_status(0)
        Preconditions.enter_local_file_catalog()
        local_file = ChatSelectLocalFilePage()
        csf = ChatSelectFilePage()
        file = local_file.select_file(".txt")
        if file:
            local_file.click_send()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        chat.wait_for_page_load()
        # 5.验证是否有发送失败的标示
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送失败', 10)

    @staticmethod
    def tearDown_test_msg_weifenglian_fenzu_0002():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep = MePage()
            mep.set_network_status(6)

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0003(self):
        """会话页面有文件发送失败时查看消息列表是否有消息发送失败的标识"""
        # 1、在当前聊天会话页面，断开网络，点击更多富媒体的文件按钮
        chat = LabelGroupingChatPage()
        chat.set_network_status(0)
        Preconditions.enter_local_file_catalog()
        local_file = ChatSelectLocalFilePage()
        csf = ChatSelectFilePage()
        file = local_file.select_file(".txt")
        if file:
            local_file.click_send()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        # 5.验证是否有发送失败的标示
        time.sleep(2)
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送失败', 10)
        # 6.返回消息列表是否有重发的标示
        chat = LabelGroupingChatPage()
        label_name = chat.get_label_name()
        chat.click_back()
        time.sleep(1)
        LableGroupDetailPage().click_back()
        time.sleep(1)
        LabelGroupingPage().click_back()
        time.sleep(1)
        chat.click_back_by_android()
        time.sleep(1)
        ContactsPage().click_message_icon()
        time.sleep(1)
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_text(label_name)
        cwp.wait_for_msg_send_status_become_to('发送失败', 10)

    @staticmethod
    def tearDown_test_msg_weifenglian_fenzu_0003():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep = MePage()
            mep.set_network_status(6)

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0004(self):
        """对发送失败的文件进行重发"""
        # 1、在当前聊天会话页面，断开网络，点击更多富媒体的文件按钮
        chat = LabelGroupingChatPage()
        chat.set_network_status(0)
        Preconditions.enter_local_file_catalog()
        local_file = ChatSelectLocalFilePage()
        chat = LabelGroupingChatPage()
        csf = ChatSelectFilePage()
        file = local_file.select_file(".txt")
        if file:
            local_file.click_send()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        chat.wait_for_page_load()
        # 5.验证是否有发送失败的标示
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送失败', 10)
        # 6.对发送失败的文件进行重发
        cwp.set_network_status(6)
        cwp.click_resend_button()
        cwp.click_resend_sure()
        time.sleep(2)

    @staticmethod
    def tearDown_test_msg_weifenglian_fenzu_0004():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep = MePage()
            mep.set_network_status(6)

    # #和飞信bug,未发送成功的文件联网后重新发送,返回消息列表页面,该对话框的群聊名称不显示
    @tags('和飞信有bug,跳过')
    def test_msg_weifenglian_fenzu_0005(self):
        """对发送失败的文件进行重发,发送失败的标志取消"""
        time.sleep(2)
        if ChatWindowPage().is_element_present_resend():
            while ChatWindowPage().is_element_present_resend():
                cwp = ChatWindowPage()
                cwp.click_resend_button()
                cwp.click_resend_sure()
        else:
            # 1、在当前聊天会话页面，断开网络，点击更多富媒体的文件按钮
            chat = LabelGroupingChatPage()
            chat.set_network_status(0)
            Preconditions.enter_local_file_catalog()
            local_file = ChatSelectLocalFilePage()
            chat = LabelGroupingChatPage()
            csf = ChatSelectFilePage()
            file = local_file.select_file(".txt")
            if file:
                local_file.click_send()
            else:
                local_file.click_back()
                local_file.click_back()
                csf.click_back()
            chat.wait_for_page_load()
            #恢复网络,发送文件
            cwp = ChatWindowPage()
            cwp.set_network_status(6)
            cwp.click_resend_button()
            cwp.click_resend_sure()
            time.sleep(2)
        #返回消息页面
        chat = LabelGroupingChatPage()
        label_name = chat.get_label_name()
        chat.click_back()
        LableGroupDetailPage().click_back()
        LabelGroupingPage().click_back()
        ContactsPage().click_message_icon()
        #查看是否有发送失败标志
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_text(label_name)
        ChatWindowPage().wait_for_msg_send_status_become_to('发送成功', 10)

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0006(self):
        """取消重发,页面停留在当前页面"""
        time.sleep(2)
        cwp = ChatWindowPage()
        lable_name = cwp.get_label_name()
        if ChatWindowPage().is_element_present_resend():
            cwp.click_resend_button()
            cwp.click_resend_not()
        else:
            # 1、在当前聊天会话页面，断开网络，点击更多富媒体的文件按钮
            chat = LabelGroupingChatPage()
            chat.set_network_status(0)
            Preconditions.enter_local_file_catalog()
            local_file = ChatSelectLocalFilePage()
            chat = LabelGroupingChatPage()
            csf = ChatSelectFilePage()
            file = local_file.select_file(".txt")
            if file:
                local_file.click_send()
            else:
                local_file.click_back()
                local_file.click_back()
                csf.click_back()
            chat.wait_for_page_load()
            #恢复网络,发送文件
            cwp = ChatWindowPage()
            cwp.set_network_status(6)
            cwp.click_resend_button()
            cwp.click_resend_not()
        time.sleep(2)
        LabelGroupingChatPage().page_should_contain_text(lable_name)

    @staticmethod
    def tearDown_test_msg_weifenglian_fenzu_0006():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep = MePage()
            mep.set_network_status(6)

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0007(self):
        """移动网络下,发送大于2M的文件会出现弹框"""
        # 设置网络为移动网络
        lbgc=LabelGroupingChatPage()
        lbgc.set_network_status(4)
        time.sleep(6)
        gcp = GroupChatPage()
        if gcp.is_text_present("切换"):
            gcp.click_network_switch()
            time.sleep(2)
        # 发送大于2M的文件
        Preconditions.enter_local_file_catalog()
        local_file = ChatSelectLocalFilePage()
        csf = ChatSelectFilePage()
        file = local_file.select_file("测试log文件.log")
        if file:
            local_file.click_send_button()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        # 弹出10G免流特权弹窗
        time.sleep(2)
        local_file.is_exist_continue_send()
        local_file.is_exist_free_flow_privilege()
        local_file.is_exist_no_longer_prompt()

    @staticmethod
    def tearDown_test_msg_weifenglian_fenzu_0007():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep = MePage()
            mep.set_network_status(6)

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0008(self):
        """移动网络下,发送大于2M的文件会出现弹框,继续发送"""
        #设置网络为移动网络
        lbgc=LabelGroupingChatPage()
        lbgc.set_network_status(4)
        time.sleep(6)
        gcp = GroupChatPage()
        if gcp.is_text_present("切换"):
            gcp.click_network_switch()
            time.sleep(2)
        #发送大于2M的文件
        Preconditions.enter_local_file_catalog()
        local_file = ChatSelectLocalFilePage()
        csf = ChatSelectFilePage()
        file = local_file.select_file("测试log文件.log")
        if file:
            local_file.click_send_button()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        #弹出10G免流特权弹窗
        time.sleep(2)
        local_file.is_exist_continue_send()
        local_file.click_continue_send()
        #再次发送大于2M的文件
        LabelGroupingChatPage().wait_for_page_load()
        Preconditions.enter_local_file_catalog()
        local_file = ChatSelectLocalFilePage()
        csf = ChatSelectFilePage()
        file = local_file.select_file("测试log文件.log")
        if file:
            local_file.click_send()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        #再次发送,页面仍弹出弹框
        time.sleep(2)
        local_file.is_exist_free_flow_privilege()

    @staticmethod
    def tearDown_test_msg_weifenglian_fenzu_0008():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep = MePage()
            mep.set_network_status(6)

    @tags('ALL', 'CMCC-RESET', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0009(self):
        """移动网络下,选择以后不再提示后点击发送"""
        #设置网络为移动网络
        lbgc=LabelGroupingChatPage()
        lbgc.set_network_status(4)
        time.sleep(6)
        gcp = GroupChatPage()
        if gcp.is_text_present("切换"):
            gcp.click_network_switch()
            time.sleep(2)
        #发送大于2M的文件
        Preconditions.enter_local_file_catalog()
        local_file = ChatSelectLocalFilePage()
        csf = ChatSelectFilePage()
        file = local_file.select_file("测试log文件.log")
        if file:
            local_file.click_send_button()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        #弹出10G免流特权弹窗,选择以后不再提示
        time.sleep(2)
        local_file.click_no_longer_prompt()
        local_file.click_continue_send()
        #再次发送大于2M文件
        Preconditions.enter_local_file_catalog()
        local_file = ChatSelectLocalFilePage()
        csf = ChatSelectFilePage()
        file = local_file.select_file("测试log文件.log")
        if file:
            local_file.click_send_button()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        #再次发送,查看是否存在弹框
        local_file.is_exist_free_flow_privilege()

    @staticmethod
    def tearDown_test_msg_weifenglian_fenzu_0009():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep = MePage()
            mep.set_network_status(6)

    @staticmethod
    def setUp_test_msg_weifenglian_fenzu_0010():

        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.reset_and_relaunch_app()
        Preconditions.make_already_in_one_key_login_page()
        Preconditions.login_by_one_key_login()
        MessagePage().wait_for_page_load()
        Preconditions.enter_label_grouping_chat_page()

    @tags('ALL', 'CMCC-RESET', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0010(self):
        """移动网络下,点击订购免流特权"""
        # 设置网络为移动网络
        lbgc = LabelGroupingChatPage()
        lbgc.set_network_status(4)
        time.sleep(6)
        gcp = GroupChatPage()
        if gcp.is_text_present("切换"):
            gcp.click_network_switch()
            time.sleep(2)
        # 发送大于2M的文件
        Preconditions.enter_local_file_catalog()
        local_file = ChatSelectLocalFilePage()
        csf = ChatSelectFilePage()
        file = local_file.select_file("测试log文件.log")
        if file:
            local_file.click_send_button()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        # 弹出10G免流特权弹窗,选择以后不再提示
        time.sleep(2)
        local_file.click_free_flow_privilege()
        local_file.wait_for_free_flow_privilege_page_load()
        local_file.click_return()

    @staticmethod
    def tearDown_test_msg_weifenglian_fenzu_0010():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep = MePage()
            mep.set_network_status(6)

   # Android手机无取消按钮,IOS有
    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0012(self):
        """文件列表页面-点击取消"""
        Preconditions.enter_local_file_catalog()
        local_file = ChatSelectLocalFilePage()

        local_file.select_file(".xls")
        #点击取消

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0013(self):
        """文件列表页面-选中文件后可返回到会话页面"""
        chat = LabelGroupingChatPage()
        label_name = chat.get_label_name()
        Preconditions.enter_local_file_catalog()
        local_file = ChatSelectLocalFilePage()
        time.sleep(2)
        local_file.click_back()
        local_file.click_back()
        ChatSelectFilePage().click_back()
        time.sleep(2)
        LabelGroupingChatPage().page_should_contain_text(label_name)

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0014(self):
        """文件列表页面-图片发送成功"""
        Preconditions.enter_local_picture_catalog()
        time.sleep(2)
        local_file = ChatSelectLocalFilePage()
        local_file.select_file('.jpg')
        local_file.click_send()
        #返回消息列表查看
        LabelGroupingChatPage().wait_for_page_load()
        time.sleep(2)
        chat = LabelGroupingChatPage()
        label_name = chat.get_label_name()
        chat.click_back()
        time.sleep(1)
        LableGroupDetailPage().click_back()
        time.sleep(1)
        LabelGroupingPage().click_back()
        time.sleep(1)
        chat.click_back_by_android()
        time.sleep(1)
        ContactsPage().click_message_icon()
        time.sleep(1)
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.page_should_contain_text(label_name)
        mess.page_should_contain_text('图片')

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0015(self):
        """断网发送图片不成功"""
        LabelGroupingChatPage().set_network_status(0)
        Preconditions.enter_local_picture_catalog()
        local_file = ChatSelectLocalFilePage()
        time.sleep(2)
        local_file.select_file('.jpg')
        local_file.click_send()
        #返回消息列表查看
        LabelGroupingChatPage().wait_for_page_load()
        time.sleep(2)
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送失败', 10)

    @staticmethod
    def tearDown_test_msg_weifenglian_fenzu_0015():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep = MePage()
            mep.set_network_status(6)

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0016(self):
        """断网发送图片不成功"""
        LabelGroupingChatPage().set_network_status(0)
        Preconditions.enter_local_picture_catalog()
        local_file = ChatSelectLocalFilePage()
        time.sleep(2)
        local_file.select_file('.jpg')
        local_file.click_send()
        #返回消息列表查看
        LabelGroupingChatPage().wait_for_page_load()
        time.sleep(2)
        chat = LabelGroupingChatPage()
        label_name = chat.get_label_name()
        chat.click_back()
        time.sleep(1)
        LableGroupDetailPage().click_back()
        time.sleep(1)
        LabelGroupingPage().click_back()
        time.sleep(1)
        chat.click_back_by_android()
        time.sleep(1)
        ContactsPage().click_message_icon()
        MessagePage().wait_for_page_load()
        MessagePage().is_iv_fail_status_present()
        #重新发送是否存在
        MessagePage().click_text(label_name)
        ChatWindowPage().is_element_present_resend()

    @staticmethod
    def tearDown_test_msg_weifenglian_fenzu_0016():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep = MePage()
            mep.set_network_status(6)

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0017(self):
        """重发图片成功"""
        chat=ChatWindowPage()
        chat.wait_for_page_load()
        if chat.is_element_present_resend():
            while chat.is_element_present_resend():
                chat.click_resend_button()
                chat.click_resend_sure()
                time.sleep(2)
        else:
            LabelGroupingChatPage().set_network_status(0)
            Preconditions.enter_local_picture_catalog()
            local_file = ChatSelectLocalFilePage()
            time.sleep(2)
            local_file.select_file('.jpg')
            local_file.click_send()
            #恢复网络重新发送
            chat.set_network_status(6)
            chat.click_resend_button()
            chat.click_resend_sure()
            time.sleep(2)
        #判断图片发送成功
        chat.wait_for_msg_send_status_become_to('发送成功',10)

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0018(self):
        """重发图片成功,消息列表不显示标志"""
        chat=ChatWindowPage()
        chat.wait_for_page_load()
        if chat.is_element_present_resend():
            while chat.is_element_present_resend():
                chat.click_resend_button()
                chat.click_resend_sure()
                time.sleep(2)
        else:
            LabelGroupingChatPage().set_network_status(0)
            Preconditions.enter_local_picture_catalog()
            local_file = ChatSelectLocalFilePage()
            time.sleep(2)
            local_file.select_file('.jpg')
            local_file.click_send()
            #恢复网络重新发送
            chat.set_network_status(6)
            chat.click_resend_button()
            chat.click_resend_sure()
            time.sleep(2)
        #判断图片发送成功
        chat.wait_for_msg_send_status_become_to('发送成功', 10)
        #返回消息列表
        LabelGroupingChatPage().wait_for_page_load()
        time.sleep(2)
        chat = LabelGroupingChatPage()
        chat.click_back()
        time.sleep(1)
        LableGroupDetailPage().click_back()
        time.sleep(1)
        LabelGroupingPage().click_back()
        time.sleep(1)
        chat.click_back_by_android()
        time.sleep(1)
        ContactsPage().click_message_icon()
        MessagePage().wait_for_page_load()
        MessagePage().is_iv_fail_status_present()

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0019(self):
        """点击重发按钮后,取消重发"""
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        if chat.is_element_present_resend():
            while chat.is_element_present_resend():
                chat.click_resend_button()
                chat.click_resend_not()
                time.sleep(2)
        else:
            LabelGroupingChatPage().set_network_status(0)
            Preconditions.enter_local_picture_catalog()
            local_file = ChatSelectLocalFilePage()
            time.sleep(2)
            local_file.select_file('.jpg')
            local_file.click_send()
            # 恢复网络重新发送
            chat.set_network_status(6)
            chat.click_resend_button()
            chat.click_resend_not()
            time.sleep(2)
        # 判断图片发送成功
        chat.wait_for_msg_send_status_become_to('发送失败', 10)

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0020(self):
        """移动网络下,发送大于2M的图片会出现弹框"""
        # 设置网络为移动网络
        lbgc = LabelGroupingChatPage()
        lbgc.set_network_status(4)
        time.sleep(6)
        gcp = GroupChatPage()
        if gcp.is_text_present("切换"):
            gcp.click_network_switch()
            time.sleep(2)
        Preconditions.send_large_picture_file()
        local_file = ChatSelectLocalFilePage()
        # 弹出10G免流特权弹窗
        time.sleep(2)
        local_file.is_exist_continue_send()
        local_file.is_exist_free_flow_privilege()
        local_file.is_exist_no_longer_prompt()

    @staticmethod
    def tearDown_test_msg_weifenglian_fenzu_0020():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep = MePage()
            mep.set_network_status(6)

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0021(self):
        """移动网络下,发送大于2M的图片会出现弹框,继续发送"""
        # 设置网络为移动网络
        lbgc = LabelGroupingChatPage()
        lbgc.set_network_status(4)
        time.sleep(6)
        gcp = GroupChatPage()
        if gcp.is_text_present("切换"):
            gcp.click_network_switch()
            time.sleep(2)
        # 发送大于2M的文件
        Preconditions.send_large_picture_file()
        local_file = ChatSelectLocalFilePage()

        # 弹出10G免流特权弹窗
        time.sleep(2)
        local_file.is_exist_continue_send()
        local_file.click_continue_send()
        # 再次发送大于2M的文件
        LabelGroupingChatPage().wait_for_page_load()
        Preconditions.send_large_picture_file()
        # 再次发送,页面仍弹出弹框
        time.sleep(2)
        local_file.is_exist_free_flow_privilege()

    @staticmethod
    def tearDown_test_msg_weifenglian_fenzu_0021():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep = MePage()
            mep.set_network_status(6)

    @tags('ALL', 'CMCC-RESET', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0022(self):
        """移动网络下,选择以后不再提示后点击发送"""
        # 设置网络为移动网络
        lbgc = LabelGroupingChatPage()
        lbgc.set_network_status(4)
        time.sleep(6)
        gcp = GroupChatPage()
        if gcp.is_text_present("切换"):
            gcp.click_network_switch()
            time.sleep(2)
        # 发送大于2M的文件
        Preconditions.send_large_picture_file()
        local_file = ChatSelectLocalFilePage()
        # 弹出10G免流特权弹窗,选择以后不再提示
        time.sleep(2)
        local_file.click_no_longer_prompt()
        local_file.click_continue_send()
        # 再次发送大于2M文件
        LabelGroupingChatPage().wait_for_page_load()
        Preconditions.send_large_picture_file()
        # 再次发送,查看是否存在弹框
        local_file.is_exist_free_flow_privilege()

    @staticmethod
    def tearDown_test_msg_weifenglian_fenzu_0022():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep = MePage()
            mep.set_network_status(6)

    @staticmethod
    def setUp_test_msg_weifenglian_fenzu_0023():

        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.reset_and_relaunch_app()
        Preconditions.make_already_in_one_key_login_page()
        Preconditions.login_by_one_key_login()
        MessagePage().wait_for_page_load()
        Preconditions.enter_label_grouping_chat_page()

    @tags('ALL', 'CMCC-RESET', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0023(self):
        """移动网络下,点击订购免流特权"""
        # 设置网络为移动网络
        lbgc = LabelGroupingChatPage()
        lbgc.set_network_status(4)
        time.sleep(6)
        gcp = GroupChatPage()
        if gcp.is_text_present("切换"):
            gcp.click_network_switch()
            time.sleep(2)
        # 发送大于2M的文件
        Preconditions.send_large_picture_file()
        local_file = ChatSelectLocalFilePage()
        # 点击订购免流特权
        time.sleep(2)
        local_file.click_free_flow_privilege()
        local_file.wait_for_free_flow_privilege_page_load()
        local_file.click_return()

    @staticmethod
    def tearDown_test_msg_weifenglian_fenzu_0023():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep = MePage()
            mep.set_network_status(6)

    # Android手机无取消按钮,IOS有
    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0025(self):
        """文件列表页面-点击取消"""
        chat = LabelGroupingChatPage()
        if not chat.is_open_more():
            chat.click_more()
        # 2、点击本地文件
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.push_preset_file()
        local_file.click_preset_file_dir()
        local_file.select_file(".jpg")
        # 点击取消

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0026(self):
        """文件列表页面-选中文件后可返回到会话页面"""
        chat = LabelGroupingChatPage()
        label_name = chat.get_label_name()
        Preconditions.enter_local_file_catalog()
        local_file = ChatSelectLocalFilePage()
        time.sleep(2)
        local_file.click_back()
        local_file.click_back()
        ChatSelectFilePage().click_back()
        time.sleep(2)
        LabelGroupingChatPage().page_should_contain_text(label_name)

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0028(self):
        """文件列表页面-视频发送成功"""
        Preconditions.enter_local_video_catalog()
        local_file = ChatSelectLocalFilePage()
        local_file.select_file('.mp4')
        local_file.click_send()
        #返回消息列表查看
        LabelGroupingChatPage().wait_for_page_load()
        time.sleep(2)
        chat = LabelGroupingChatPage()
        label_name = chat.get_label_name()
        chat.click_back()
        time.sleep(1)
        LableGroupDetailPage().click_back()
        time.sleep(1)
        LabelGroupingPage().click_back()
        time.sleep(1)
        chat.click_back_by_android()
        time.sleep(1)
        ContactsPage().click_message_icon()
        time.sleep(1)
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.page_should_contain_text(label_name)
        mess.page_should_contain_text('视频')

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0029(self):
        """断网发送视频不成功"""
        LabelGroupingChatPage().set_network_status(0)
        Preconditions.enter_local_video_catalog()
        local_file = ChatSelectLocalFilePage()
        local_file.select_file('.mp4')
        local_file.click_send()
        #返回对话框
        LabelGroupingChatPage().wait_for_page_load()
        time.sleep(2)
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送失败', 10)

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0030(self):
        """断网发送视频不成功,消息列表显示发送失败"""
        LabelGroupingChatPage().set_network_status(0)
        LabelGroupingChatPage().set_network_status(0)
        Preconditions.enter_local_video_catalog()
        local_file = ChatSelectLocalFilePage()
        local_file.select_file('.mp4')
        local_file.click_send()
        # 返回对话框
        LabelGroupingChatPage().wait_for_page_load()
        time.sleep(2)
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送失败', 10)
        # 返回消息列表,有发送失败标志
        time.sleep(2)
        LabelGroupingChatPage().click_back()
        time.sleep(1)
        LableGroupDetailPage().click_back()
        time.sleep(1)
        LabelGroupingPage().click_back()
        time.sleep(1)
        LabelGroupingPage().click_back_by_android()
        time.sleep(1)
        ContactsPage().click_message_icon()
        MessagePage().wait_for_page_load()
        MessagePage().is_iv_fail_status_present()

    @staticmethod
    def tearDown_test_msg_weifenglian_fenzu_0030():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep = MePage()
            mep.set_network_status(6)

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0031(self):
        """重发图片成功"""
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        if chat.is_element_present_resend():
            while chat.is_element_present_resend():
                chat.click_resend_button()
                chat.click_resend_sure()
                time.sleep(2)
        else:
            LabelGroupingChatPage().set_network_status(0)
            LabelGroupingChatPage().click_more()
            more_page = ChatMorePage()
            more_page.click_file()
            csf = ChatSelectFilePage()
            csf.wait_for_page_load()
            csf.click_local_file()
            local_file = ChatSelectLocalFilePage()
            # 进入预置文件目录，选择文件发送
            local_file.push_preset_file()
            local_file.click_preset_file_dir()
            time.sleep(2)
            local_file.select_file('.mp4')
            local_file.click_send()
            # 恢复网络重新发送
            chat.set_network_status(6)
            chat.click_resend_button()
            chat.click_resend_sure()
            time.sleep(2)
        # 判断图片发送成功
        chat.wait_for_msg_send_status_become_to('发送成功', 10)

    @staticmethod
    def tearDown_test_msg_weifenglian_fenzu_0031():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep = MePage()
            mep.set_network_status(6)

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0032(self):
        """重发图片成功,消息列表不显示标志"""
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        if chat.is_element_present_resend():
            while chat.is_element_present_resend():
                chat.set_network_status(6)
                chat.click_resend_button()
                chat.click_resend_sure()
                time.sleep(2)
        else:
            LabelGroupingChatPage().set_network_status(0)
            Preconditions.enter_local_file_catalog()
            local_file = ChatSelectLocalFilePage()
            time.sleep(2)
            local_file.select_file('.mp4')
            local_file.click_send()
            # 恢复网络重新发送
            chat.set_network_status(6)
            chat.click_resend_button()
            chat.click_resend_sure()
            time.sleep(2)
        # 判断图片发送成功
        chat.wait_for_msg_send_status_become_to('发送成功', 10)
        # 返回消息列表
        LabelGroupingChatPage().wait_for_page_load()
        time.sleep(2)
        chat = LabelGroupingChatPage()
        chat.click_back()
        time.sleep(1)
        LableGroupDetailPage().click_back()
        time.sleep(1)
        LabelGroupingPage().click_back()
        time.sleep(1)
        chat.click_back_by_android()
        time.sleep(1)
        ContactsPage().click_message_icon()
        MessagePage().wait_for_page_load()
        MessagePage().is_iv_fail_status_present()

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0033(self):
        """点击重发按钮后,取消重发"""
        chat = ChatWindowPage()
        chat.wait_for_page_load()
        if chat.is_element_present_resend():
            while chat.is_element_present_resend():
                chat.click_resend_button()
                chat.click_resend_not()
                time.sleep(2)
        else:
            LabelGroupingChatPage().set_network_status(0)
            Preconditions.enter_local_file_catalog()
            local_file = ChatSelectLocalFilePage()
            time.sleep(2)
            local_file.select_file('.mp4')
            local_file.click_send()
            # 恢复网络重新发送
            chat.set_network_status(6)
            chat.click_resend_button()
            chat.click_resend_not()
            time.sleep(2)
        # 判断图片发送成功
        chat.wait_for_msg_send_status_become_to('发送失败', 10)

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0035(self):
        """移动网络下,发送大于2M的视频会出现弹框"""
        # 设置网络为移动网络
        lbgc = LabelGroupingChatPage()
        lbgc.set_network_status(4)
        time.sleep(6)
        gcp = GroupChatPage()
        if gcp.is_text_present("切换"):
            gcp.click_network_switch()
            time.sleep(2)
        Preconditions.send_large_video_file()
        # 弹出10G免流特权弹窗
        local_file = ChatSelectLocalFilePage()
        time.sleep(2)
        local_file.is_exist_continue_send()
        local_file.is_exist_free_flow_privilege()
        local_file.is_exist_no_longer_prompt()

    @staticmethod
    def tearDown_test_msg_weifenglian_fenzu_0035():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep = MePage()
            mep.set_network_status(6)

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0036(self):
        """移动网络下,发送大于2M的视频会出现弹框,继续发送"""
        # 设置网络为移动网络
        lbgc = LabelGroupingChatPage()
        lbgc.set_network_status(4)
        time.sleep(6)
        gcp = GroupChatPage()
        if gcp.is_text_present("切换"):
            gcp.click_network_switch()
            time.sleep(2)
        Preconditions.send_large_video_file()
        # 弹出10G免流特权弹窗
        local_file = ChatSelectLocalFilePage()
        time.sleep(2)
        local_file.is_exist_continue_send()
        local_file.click_continue_send()
        LabelGroupingChatPage().wait_for_page_load()
        # 再次发送大于2M的文件
        Preconditions.send_large_video_file()
        # 再次发送,页面仍弹出弹框
        time.sleep(2)
        local_file.is_exist_continue_send()

    @staticmethod
    def tearDown_test_msg_weifenglian_fenzu_0036():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep = MePage()
            mep.set_network_status(6)

    @tags('ALL', 'CMCC-RESET', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0037(self):
        """移动网络下,选择以后不再提示后点击发送"""
        # 设置网络为移动网络
        lbgc = LabelGroupingChatPage()
        lbgc.set_network_status(4)
        time.sleep(6)
        gcp = GroupChatPage()
        if gcp.is_text_present("切换"):
            gcp.click_network_switch()
            time.sleep(2)
        # 发送大于2M的文件
        Preconditions.send_large_video_file()
        # 弹出10G免流特权弹窗,选择以后不再提示
        time.sleep(2)
        local_file = ChatSelectLocalFilePage()
        local_file.click_no_longer_prompt()
        local_file.click_continue_send()
        # 再次发送大于2M文件
        LabelGroupingChatPage().wait_for_page_load()
        Preconditions.send_large_video_file()
        # 再次发送,查看是否存在弹框
        time.sleep(2)
        local_file.is_exist_free_flow_privilege()

    @staticmethod
    def tearDown_test_msg_weifenglian_fenzu_0037():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep = MePage()
            mep.set_network_status(6)

    @staticmethod
    def setUp_test_msg_weifenglian_fenzu_0038():

        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.reset_and_relaunch_app()
        Preconditions.make_already_in_one_key_login_page()
        Preconditions.login_by_one_key_login()
        MessagePage().wait_for_page_load()
        Preconditions.enter_label_grouping_chat_page()

    @tags('ALL', 'CMCC-RESET', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0038(self):
        """移动网络下,点击订购免流特权"""
        # 设置网络为移动网络
        lbgc = LabelGroupingChatPage()
        lbgc.set_network_status(4)
        time.sleep(6)
        gcp = GroupChatPage()
        if gcp.is_text_present("切换"):
            gcp.click_network_switch()
            time.sleep(2)
        # 发送大于2M的文件
        Preconditions.send_large_video_file()
        # 点击订购免流特权
        time.sleep(2)
        local_file = ChatSelectLocalFilePage()
        local_file.click_free_flow_privilege()
        local_file.wait_for_free_flow_privilege_page_load()
        local_file.click_return()
        local_file.is_exist_free_flow_privilege()

    @staticmethod
    def tearDown_test_msg_weifenglian_fenzu_0038():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep = MePage()
            mep.set_network_status(6)

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0039(self):
        """取消选择视频"""
        # 进入本地视频页面
        Preconditions.enter_local_video_catalog()
        local_file = ChatSelectLocalFilePage()
        local_file.select_file('.mp4')
        # 点击取消(ios才有)

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0040(self):
        """选择视频后返回"""
        # 进入本地视频页面
        Preconditions.enter_local_video_catalog()
        local_file = ChatSelectLocalFilePage()
        local_file.select_file('.mp4')
        # 点击返回
        local_file.click_back()
        time.sleep(2)
        ChatSelectFilePage().page_should_contain_text('选择文件')
        # 再点击返回,进入聊天页面
        ChatSelectFilePage().click_back()
        LabelGroupingChatPage().is_on_this_page()

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0042(self):
        """音乐发送成功"""
        Preconditions.enter_local_music_catalog()
        local_file = ChatSelectLocalFilePage()
        local_file.select_file('.mp3')
        local_file.click_send()
        # 返回消息页面,查看页面显示
        LabelGroupingChatPage().wait_for_page_load()
        label_name = LabelGroupingChatPage().get_label_name()
        LabelGroupingChatPage().click_back()
        time.sleep(1)
        LableGroupDetailPage().click_back()
        time.sleep(1)
        LabelGroupingPage().click_back()
        time.sleep(1)
        LabelGroupingPage().click_back_by_android()
        time.sleep(1)
        ContactsPage().click_message_icon()
        MessagePage().wait_for_page_load()
        MessagePage().page_should_contain_text(label_name)
        MessagePage().page_should_contain_text('文件')

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0043(self):
        """断网音乐发送失败"""
        Preconditions.enter_local_music_catalog()
        #断网
        local_file = ChatSelectLocalFilePage()
        local_file.set_network_status(0)
        time.sleep(1)
        local_file.select_file('.mp3')
        local_file.click_send()
        time.sleep(2)
        #重发按钮是否存在
        ChatWindowPage().wait_for_page_load()
        ChatWindowPage().is_element_present_resend()

    @staticmethod
    def tearDown_test_msg_weifenglian_fenzu_0043():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep = MePage()
            mep.set_network_status(6)

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0044(self):
        """断网音乐发送失败,消息列表有显示"""
        chat=ChatWindowPage()
        if chat.is_element_present_resend():
            while chat.is_element_present_resend():
                chat.click_resend_button()
                chat.click_resend_sure()
                time.sleep(2)
        Preconditions.enter_local_music_catalog()
        # 断网
        local_file = ChatSelectLocalFilePage()
        local_file.set_network_status(0)
        local_file.select_file('.mp3')
        local_file.click_send()
        time.sleep(2)
        # 重发按钮是否存在
        cwp=ChatWindowPage()
        cwp.wait_for_page_load()
        cwp.is_element_present_resend()
        # 返回消息页面
        cwp.click_back_by_android()
        time.sleep(1)
        LableGroupDetailPage().click_back()
        time.sleep(1)
        LabelGroupingPage().click_back()
        time.sleep(1)
        cwp.click_back_by_android()
        time.sleep(1)
        ContactsPage().click_message_icon()
        # MessagePage().wait_for_page_load()
        time.sleep(5)
        MessagePage().is_iv_fail_status_present()

    @staticmethod
    def tearDown_test_msg_weifenglian_fenzu_0044():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep = MePage()
            mep.set_network_status(6)

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0045(self):
        """发送失败的文件,重复成功"""
        chat=ChatWindowPage()
        if chat.is_element_present_resend():
            while chat.is_element_present_resend():
                chat.click_resend_button()
                chat.click_resend_sure()
                time.sleep(2)
        else:
            LabelGroupingChatPage().set_network_status(0)
            Preconditions.enter_local_music_catalog()
            local_file = ChatSelectLocalFilePage()
            time.sleep(2)
            local_file.select_file('.mp3')
            local_file.click_send()
            #恢复网络重新发送
            chat.set_network_status(6)
            chat.click_resend_button()
            chat.click_resend_sure()
            time.sleep(2)
        #判断图片发送成功
        chat.wait_for_msg_send_status_become_to('发送成功',10)

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0046(self):
        """发送失败的文件,重复成功,返回消息列表,标志消失"""
        chat=ChatWindowPage()
        if chat.is_element_present_resend():
            while chat.is_element_present_resend():
                chat.click_resend_button()
                chat.click_resend_sure()
                time.sleep(2)
        else:
            LabelGroupingChatPage().set_network_status(0)
            Preconditions.enter_local_music_catalog()
            local_file = ChatSelectLocalFilePage()
            time.sleep(2)
            local_file.select_file('.mp3')
            local_file.click_send()
            #恢复网络重新发送
            chat.set_network_status(6)
            chat.click_resend_button()
            chat.click_resend_sure()
            time.sleep(2)
        # 判断图片发送成功
        chat.wait_for_msg_send_status_become_to('发送成功', 10)
        # 返回消息页面
        ChatWindowPage().click_back_by_android()
        time.sleep(1)
        LableGroupDetailPage().click_back()
        time.sleep(1)
        LabelGroupingPage().click_back()
        time.sleep(1)
        ChatWindowPage().click_back_by_android()
        time.sleep(1)
        ContactsPage().click_message_icon()
        MessagePage().wait_for_page_load()
        MessagePage().is_iv_fail_status_present()

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0047(self):
        """发送失败的文件,取消重发"""
        chat=ChatWindowPage()
        if chat.is_element_present_resend():
            while chat.is_element_present_resend():
                chat.click_resend_button()
                chat.click_resend_not()
                time.sleep(2)
        else:
            LabelGroupingChatPage().set_network_status(0)
            Preconditions.enter_local_music_catalog()
            local_file = ChatSelectLocalFilePage()
            time.sleep(2)
            local_file.select_file('.mp3')
            local_file.click_send()
            #恢复网络重新发送
            chat.set_network_status(6)
            chat.click_resend_button()
            chat.click_resend_not()
            time.sleep(2)
        #判断图片发送成功
        LabelGroupingChatPage().is_on_this_page()

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0048(self):
        """移动网络下,发送大于2M的音乐会出现弹框"""
        # 设置网络为移动网络
        lbgc = LabelGroupingChatPage()
        lbgc.set_network_status(4)
        time.sleep(6)
        gcp = GroupChatPage()
        if gcp.is_text_present("切换"):
            gcp.click_network_switch()
            time.sleep(2)
        Preconditions.send_large_music_file()
        local_file = ChatSelectLocalFilePage()
        # 弹出10G免流特权弹窗
        time.sleep(2)
        local_file.is_exist_continue_send()
        local_file.is_exist_free_flow_privilege()
        local_file.is_exist_no_longer_prompt()

    @staticmethod
    def tearDown_test_msg_weifenglian_fenzu_0048():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep = MePage()
            mep.set_network_status(6)

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0049(self):
        """移动网络下,发送大于2M的音乐会出现弹框,继续发送"""
        # 设置网络为移动网络
        lbgc = LabelGroupingChatPage()
        lbgc.set_network_status(4)
        time.sleep(6)
        gcp = GroupChatPage()
        if gcp.is_text_present("切换"):
            gcp.click_network_switch()
            time.sleep(2)
        # 发送大于2M的文件
        Preconditions.send_large_music_file()
        local_file = ChatSelectLocalFilePage()

        # 弹出10G免流特权弹窗
        time.sleep(2)
        local_file.is_exist_continue_send()
        local_file.click_continue_send()
        # 再次发送大于2M的文件
        LabelGroupingChatPage().wait_for_page_load()
        Preconditions.send_large_music_file()
        # 再次发送,页面仍弹出弹框
        time.sleep(2)
        local_file.is_exist_free_flow_privilege()

    @staticmethod
    def tearDown_test_msg_weifenglian_fenzu_0049():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep = MePage()
            mep.set_network_status(6)

    @tags('ALL', 'CMCC-RESET', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0050(self):
        """移动网络下,选择以后不再提示后点击发送"""
        # 设置网络为移动网络
        lbgc = LabelGroupingChatPage()
        lbgc.set_network_status(4)
        time.sleep(6)
        gcp = GroupChatPage()
        if gcp.is_text_present("切换"):
            gcp.click_network_switch()
            time.sleep(2)
        # 发送大于2M的文件
        Preconditions.send_large_music_file()
        local_file = ChatSelectLocalFilePage()
        # 弹出10G免流特权弹窗,选择以后不再提示
        time.sleep(2)
        local_file.click_no_longer_prompt()
        local_file.click_continue_send()
        # 再次发送大于2M文件
        LabelGroupingChatPage().wait_for_page_load()
        Preconditions.send_large_music_file()
        # 再次发送,查看是否存在弹框
        local_file.is_exist_free_flow_privilege()

    @staticmethod
    def tearDown_test_msg_weifenglian_fenzu_0050():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep = MePage()
            mep.set_network_status(6)

    @staticmethod
    def setUp_test_msg_weifenglian_fenzu_0051():
        Preconditions.connect_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.reset_and_relaunch_app()
        Preconditions.make_already_in_one_key_login_page()
        Preconditions.login_by_one_key_login()
        MessagePage().wait_for_page_load()
        Preconditions.enter_label_grouping_chat_page()

    @tags('ALL', 'CMCC-RESET', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0051(self):
        """移动网络下,点击订购免流特权"""
        # 设置网络为移动网络
        lbgc = LabelGroupingChatPage()
        lbgc.set_network_status(4)
        time.sleep(6)
        gcp = GroupChatPage()
        if gcp.is_text_present("切换"):
            gcp.click_network_switch()
            time.sleep(2)
        # 发送大于2M的文件
        Preconditions.send_large_music_file()
        local_file = ChatSelectLocalFilePage()
        # 点击订购免流特权
        time.sleep(2)
        local_file.click_free_flow_privilege()
        local_file.wait_for_free_flow_privilege_page_load()
        local_file.click_return()

    @staticmethod
    def tearDown_test_msg_weifenglian_fenzu_0051():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep = MePage()
            mep.set_network_status(6)

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0053(self):
        """取消选择音乐"""
        #进入本地音乐页面
        Preconditions.enter_local_music_catalog()
        local_file = ChatSelectLocalFilePage()
        local_file.select_file('.mp3')
        #点击取消(ios才有)

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0054(self):
        """返回选择音乐页面"""
        #进入本地音乐页面
        Preconditions.enter_local_music_catalog()
        #返回
        local_file = ChatSelectLocalFilePage()
        local_file.click_back()
        local_file.page_should_contain_text('选择文件')
        #再点击返回按钮
        ChatSelectFilePage().click_back()
        LabelGroupingChatPage().is_on_this_page()

    @tags('ALL','CMCC', 'DEBUG_1', 'label_grouping', 'yms')
    def test_msg_weifenglian_fenzu_0055(self):
        """标签分组天会话页面，长按文件转发到任意群"""
        chat = LabelGroupingChatPage()
        if LabelGroupingChatPage().is_element_present_file():
            chat.wait_for_page_load()
        else:
            # 1、在当前群聊天会话页面长按任意文件
            # 进入到文件选择页面
            chat = LabelGroupingChatPage()
            Preconditions.enter_local_file_catalog()
            local_file = ChatSelectLocalFilePage()
            local_file.select_file(".txt")
            local_file.click_send()
            # 2、选择转发，选择一个群
            chat.wait_for_page_load()
        chat.press_file()
        time.sleep(2)
        # 页面调起功能菜单
        chat.page_should_contain_text('转发')
        chat.page_should_contain_text('收藏')
        # chat.page_should_contain_text('撤回')
        chat.page_should_contain_text('删除')
        chat.page_should_contain_text('多选')
        # 点击转发
        chat.click_forward()
        SelectContactsPage().wait_for_page_load()
        scp = SelectContactsPage()
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        names = sogp.get_group_name()
        if sogp.is_element_present_result():
            sogp.select_one_group_by_name(names[0])
            # 3、点击确定
            time.sleep(1)
            sogp.page_should_contain_text('取消')
            sogp.page_should_contain_text('确定')
            sogp.click_sure_forward()
            flag = sogp.is_toast_exist("已转发")
        else:
            sogp.page_should_contain_text('无搜索结果')

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping', 'yms')
    def test_msg_weifenglian_fenzu_0057(self):
        """断网状态,标签分组天会话页面，长按文件转发到任意群失败"""
        if LabelGroupingChatPage().is_element_present_file():
            chat = LabelGroupingChatPage()
            chat.wait_for_page_load()
        else:
            chat = LabelGroupingChatPage()
            Preconditions.enter_local_file_catalog()
            local_file = ChatSelectLocalFilePage()
            local_file.select_file(".txt")
            local_file.click_send()
        # 长按文件转发
        chat.press_file()
        time.sleep(2)
        chat.page_should_contain_text('转发')
        chat.page_should_contain_text('收藏')
        # chat.page_should_contain_text('撤回')
        chat.page_should_contain_text('删除')
        chat.page_should_contain_text('多选')
        # 断网状态点击转发
        chat.click_forward()
        time.sleep(1)
        SelectContactsPage().set_network_status(0)
        SelectContactsPage().wait_for_page_load()
        scp = SelectContactsPage()
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        names = sogp.get_group_name()
        if sogp.is_element_present_result():
            sogp.select_one_group_by_name(names[0])
            # 3、点击确定
            time.sleep(1)
            sogp.page_should_contain_text('取消')
            sogp.page_should_contain_text('确定')
            sogp.click_sure_forward()
            flag = sogp.is_toast_exist("已转发")
            self.assertTrue(flag)
        else:
            sogp.page_should_contain_text('无搜索结果')
        # 返回消息页面,查看文件是否发送成功
        time.sleep(2)
        ChatWindowPage().click_back_by_android()
        time.sleep(1)
        LableGroupDetailPage().click_back()
        time.sleep(1)
        LabelGroupingPage().click_back()
        time.sleep(1)
        ChatWindowPage().click_back_by_android()
        time.sleep(1)
        ContactsPage().click_message_icon()
        time.sleep(2)
        MessagePage().is_iv_fail_status_present()

    @staticmethod
    def tearDown_test_msg_weifenglian_fenzu_0057():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep = MePage()
            mep.set_network_status(6)

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0059(self):
        """标签分组天会话页面，长按文件取消转发到任意群"""
        if LabelGroupingChatPage().is_element_present_file():
            chat = LabelGroupingChatPage()
            chat.wait_for_page_load()
        else:
            # 进入到文件选择页面
            chat = LabelGroupingChatPage()
            Preconditions.enter_local_file_catalog()
            local_file = ChatSelectLocalFilePage()
            local_file.select_file(".txt")
            local_file.click_send()
            # 2、选择转发，选择一个群
            chat.wait_for_page_load()
        # 2、选择转发，选择一个群
        chat.press_file()
        time.sleep(2)
        # 页面调起功能菜单
        chat.page_should_contain_text('转发')
        chat.page_should_contain_text('收藏')
        # chat.page_should_contain_text('撤回')
        chat.page_should_contain_text('删除')
        chat.page_should_contain_text('多选')
        # 点击转发
        chat.click_forward()
        SelectContactsPage().wait_for_page_load()
        scp = SelectContactsPage()
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        names = sogp.get_group_name()
        if sogp.is_element_present_result():
            sogp.select_one_group_by_name(names[0])
            # 3、点击取消
            time.sleep(1)
            sogp.page_should_contain_text('取消')
            sogp.page_should_contain_text('确定')
            sogp.click_cancel_forward()
            sogp.page_contain_element_result()
        else:
            sogp.page_should_contain_text('无搜索结果')

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0061(self):
        """长按文件转发到任意群名为文字的群"""
        chat = LabelGroupingChatPage()
        if LabelGroupingChatPage().is_element_present_file():
            chat.wait_for_page_load()
        else:
            Preconditions.enter_local_file_catalog()
            local_file = ChatSelectLocalFilePage()
            local_file.select_file(".txt")
            local_file.click_send()
        # 2、选择转发，选择一个群
        chat.press_file()
        #点击转发
        chat.click_forward()
        SelectContactsPage().wait_for_page_load()
        scp = SelectContactsPage()
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        #搜索群组
        sogp.click_search_group()
        sogp.input_search_keyword('和飞信')
        if sogp.is_element_present_result():
            sogp.click_search_result()
            # 3、点击确定
            time.sleep(1)
            sogp.page_should_contain_text('取消')
            sogp.page_should_contain_text('确定')
            sogp.click_sure_forward()
            flag = sogp.is_toast_exist("已转发")
            self.assertTrue(flag)
        else:
            sogp.page_should_contain_text('无搜索结果')

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0062(self):
        """长按文件转发到任意群名为英文的群"""
        chat = LabelGroupingChatPage()
        if LabelGroupingChatPage().is_element_present_file():
            chat.wait_for_page_load()
        else:
            Preconditions.enter_local_file_catalog()
            local_file = ChatSelectLocalFilePage()
            local_file.select_file(".txt")
            local_file.click_send()
        # 2、选择转发，选择一个群
        chat.press_file()
        #点击转发
        chat.click_forward()
        SelectContactsPage().wait_for_page_load()
        scp = SelectContactsPage()
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        #搜索群组
        sogp.click_search_group()
        sogp.input_search_keyword('hfx')
        if sogp.is_element_present_result():
            sogp.click_search_result()
            # 3、点击确定
            time.sleep(1)
            sogp.page_should_contain_text('取消')
            sogp.page_should_contain_text('确定')
            sogp.click_sure_forward()
            flag = sogp.is_toast_exist("已转发")
            self.assertTrue(flag)
        else:
            sogp.page_should_contain_text('无搜索结果')

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0063(self):
        """长按文件转发到任意群名为数字的群"""
        chat = LabelGroupingChatPage()
        if LabelGroupingChatPage().is_element_present_file():
            chat.wait_for_page_load()
        else:
            Preconditions.enter_local_file_catalog()
            local_file = ChatSelectLocalFilePage()
            local_file.select_file(".txt")
            local_file.click_send()
        # 2、选择转发，选择一个群
        chat.press_file()
        #点击转发
        chat.click_forward()
        SelectContactsPage().wait_for_page_load()
        scp = SelectContactsPage()
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        #搜索群组
        sogp.click_search_group()
        sogp.input_search_keyword('123')
        if sogp.is_element_present_result():
            sogp.click_search_result()
            # 3、点击确定
            time.sleep(1)
            sogp.page_should_contain_text('取消')
            sogp.page_should_contain_text('确定')
            sogp.click_sure_forward()
            flag = sogp.is_toast_exist("已转发")
            self.assertTrue(flag)
        else:
            sogp.page_should_contain_text('无搜索结果')

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0064(self):
        """长按文件转发到任意群名为标点符号的群"""
        chat = LabelGroupingChatPage()
        if LabelGroupingChatPage().is_element_present_file():
            chat.wait_for_page_load()
        else:
            Preconditions.enter_local_file_catalog()
            local_file = ChatSelectLocalFilePage()
            local_file.select_file(".txt")
            local_file.click_send()
        # 2、选择转发，选择一个群
        chat.press_file()
        #点击转发
        chat.click_forward()
        SelectContactsPage().wait_for_page_load()
        scp = SelectContactsPage()
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        #搜索群组
        sogp.click_search_group()
        sogp.input_search_keyword(',,,')
        if sogp.is_element_present_result():
            sogp.click_search_result()
            # 3、点击确定
            time.sleep(1)
            sogp.page_should_contain_text('取消')
            sogp.page_should_contain_text('确定')
            sogp.click_sure_forward()
            flag = sogp.is_toast_exist("已转发")
            self.assertTrue(flag)
        else:
            sogp.page_should_contain_text('无搜索结果')

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0065(self):
        """长按文件转发到任意群名为特殊字符的群"""
        chat = LabelGroupingChatPage()
        if LabelGroupingChatPage().is_element_present_file():
            chat.wait_for_page_load()
        else:
            Preconditions.enter_local_file_catalog()
            local_file = ChatSelectLocalFilePage()
            local_file.select_file(".txt")
            local_file.click_send()
        # 2、选择转发，选择一个群
        chat.press_file()
        #点击转发
        chat.click_forward()
        SelectContactsPage().wait_for_page_load()
        scp = SelectContactsPage()
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        #搜索群组
        sogp.click_search_group()
        sogp.input_search_keyword('///')
        if sogp.is_element_present_result():
            sogp.click_search_result()
            # 3、点击确定
            time.sleep(1)
            sogp.page_should_contain_text('取消')
            sogp.page_should_contain_text('确定')
            sogp.click_sure_forward()
            flag = sogp.is_toast_exist("已转发")
            self.assertTrue(flag)
        else:
            sogp.page_should_contain_text('无搜索结果')

    @tags('ALL','CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0066(self):
        """长按文件转发到任意群名为空格的群"""
        chat = LabelGroupingChatPage()
        if LabelGroupingChatPage().is_element_present_file():
            chat.wait_for_page_load()
        else:
            Preconditions.enter_local_file_catalog()
            local_file = ChatSelectLocalFilePage()
            local_file.select_file(".txt")
            local_file.click_send()
        # 2、选择转发，选择一个群
        chat.press_file()
        #点击转发
        chat.click_forward()
        SelectContactsPage().wait_for_page_load()
        scp = SelectContactsPage()
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        #搜索群组
        sogp.click_search_group()
        sogp.input_search_keyword('   ')
        if sogp.is_element_present_result():
            sogp.click_search_result()
            # 3、点击确定
            time.sleep(1)
            sogp.page_should_contain_text('取消')
            sogp.page_should_contain_text('确定')
            sogp.click_sure_forward()
            flag = sogp.is_toast_exist("已转发")
            self.assertTrue(flag)
        else:
            sogp.page_should_contain_text('无搜索结果')

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0067(self):
        """长按文件转发到任意群名为多种字符的群"""
        chat = LabelGroupingChatPage()
        if LabelGroupingChatPage().is_element_present_file():
            chat.wait_for_page_load()
        else:
            Preconditions.enter_local_file_catalog()
            local_file = ChatSelectLocalFilePage()
            local_file.select_file(".txt")
            local_file.click_send()
        # 2、选择转发，选择一个群
        chat.press_file()
        #点击转发
        chat.click_forward()
        SelectContactsPage().wait_for_page_load()
        scp = SelectContactsPage()
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        #搜索群组
        sogp.click_search_group()
        sogp.input_search_keyword('hfx123,,,///')
        if sogp.is_element_present_result():
            sogp.click_search_result()
            # 3、点击确定
            time.sleep(1)
            sogp.page_should_contain_text('取消')
            sogp.page_should_contain_text('确定')
            sogp.click_sure_forward()
            flag = sogp.is_toast_exist("已转发")
            self.assertTrue(flag)
        else:
            sogp.page_should_contain_text('无搜索结果')

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0068(self):
        """长按文件转发到任意群名为多种字符的群"""
        chat = LabelGroupingChatPage()
        if LabelGroupingChatPage().is_element_present_file():
            chat.wait_for_page_load()
        else:
            Preconditions.enter_local_file_catalog()
            local_file = ChatSelectLocalFilePage()
            local_file.select_file(".txt")
            local_file.click_send()
        # 2、选择转发，选择一个群
        chat.press_file()
        #点击转发
        chat.click_forward()
        SelectContactsPage().wait_for_page_load()
        scp = SelectContactsPage()
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        #搜索群组
        sogp.click_search_group()
        sogp.input_search_keyword('hfx123,,,///')
        if sogp.is_element_present_result():
            sogp.click_search_result()
            # 3、点击确定
            time.sleep(1)
            sogp.page_should_contain_text('取消')
            sogp.page_should_contain_text('确定')
            sogp.click_sure_forward()
            flag = sogp.is_toast_exist("已转发")
            self.assertTrue(flag)
        else:
            sogp.page_should_contain_text('无搜索结果')

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0070(self):
        """选择群后,取消转发文件"""
        chat = LabelGroupingChatPage()
        # if LabelGroupingChatPage().is_element_present_file():
        #     chat.wait_for_page_load()
        # else:
        Preconditions.enter_local_file_catalog()
        local_file = ChatSelectLocalFilePage()
        local_file.select_file(".txt")
        local_file.click_send()
        time.sleep(2)
        # 2、转发，选择一个群
        chat.press_last_file()
        #点击转发
        chat.click_forward()
        SelectContactsPage().wait_for_page_load()
        scp = SelectContactsPage()
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        #搜索群组
        sogp.click_search_group()
        sogp.input_search_keyword('给个红包1')
        time.sleep(1)
        if sogp.is_element_present_result():
            sogp.click_search_result()
            time.sleep(2)
            sogp.page_should_contain_text('取消')
            sogp.page_should_contain_text('确定')
            sogp.click_cancel_forward()

            sogp.page_contain_element_result()

        else:
            sogp.page_should_contain_text('无搜索结果')

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0071(self):
        """转发文件,根据右侧字母定位群"""
        chat = LabelGroupingChatPage()
        if LabelGroupingChatPage().is_element_present_file():
            chat.wait_for_page_load()
        else:
            Preconditions.enter_local_file_catalog()
            local_file = ChatSelectLocalFilePage()
            local_file.select_file(".txt")
            local_file.click_send()
        #点击转发
        chat.press_last_file()
        chat.click_forward()
        SelectContactsPage().wait_for_page_load()
        scp = SelectContactsPage()
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        sogp.choose_index_bar_click_element()
        time.sleep(2)
        sogp.page_should_contain_text('取消')
        sogp.page_should_contain_text('确定')
        sogp.click_sure_forward()
        flag = sogp.is_toast_exist("已转发")
        self.assertTrue(flag)

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0072(self):
        """标签分组天会话页面，长按文件转发到手机联系人"""
        chat = LabelGroupingChatPage()
        if LabelGroupingChatPage().is_element_present_file():
            chat.wait_for_page_load()
        else:
            # 1、在当前群聊天会话页面长按任意文件
            # 进入到文件选择页面
            chat = LabelGroupingChatPage()
            Preconditions.enter_local_file_catalog()
            local_file = ChatSelectLocalFilePage()
            local_file.select_file(".txt")
            local_file.click_send()
            chat.wait_for_page_load()
        # 2、选择转发，选择手机联系人
        chat.press_file()
        chat.click_forward()
        SelectContactsPage().wait_for_page_load()
        scp = SelectContactsPage()
        scp.click_phone_contact()
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        slcp.click_first_phone_contacts()
        slcp.page_should_contain_text('取消')
        slcp.page_should_contain_text('确定')
        slcp.click_sure_forward()
        slcp.is_toast_exist('已转发')

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0073(self):
        """标签分组天会话页面，长按文件取消转发到手机联系人"""
        if LabelGroupingChatPage().is_element_present_file():
            chat = LabelGroupingChatPage()
            chat.wait_for_page_load()
        else:
            # 1、在当前群聊天会话页面长按任意文件
            # 进入到文件选择页面
            chat = LabelGroupingChatPage()
            Preconditions.enter_local_file_catalog()
            local_file = ChatSelectLocalFilePage()
            local_file.select_file(".txt")
            local_file.click_send()
            chat.wait_for_page_load()
            # 2、选择转发，选择手机联系人
        chat.press_file()
        chat.click_forward()
        SelectContactsPage().wait_for_page_load()
        scp = SelectContactsPage()
        scp.click_phone_contact()
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        slcp.click_first_phone_contacts()
        slcp.page_should_contain_text('取消')
        slcp.page_should_contain_text('确定')
        slcp.click_cancel_forward()

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0074(self):
        """断网状态,标签分组天会话页面，长按文件转发到手机联系人失败"""
        if LabelGroupingChatPage().is_element_present_file():
            chat = LabelGroupingChatPage()
            chat.wait_for_page_load()
        else:
            # 1、在当前群聊天会话页面长按任意文件
            # 进入到文件选择页面
            chat = LabelGroupingChatPage()
            Preconditions.enter_local_file_catalog()
            local_file = ChatSelectLocalFilePage()
            local_file.select_file(".txt")
            local_file.click_send()
            chat.wait_for_page_load()
            # 2、选择转发，选择手机联系人
        chat.press_file()
        chat.click_forward()
        SelectContactsPage().wait_for_page_load()
        #断网
        scp = SelectContactsPage()
        scp.set_network_status(0)
        scp.click_phone_contact()
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        slcp.click_first_phone_contacts()
        slcp.page_should_contain_text('取消')
        slcp.page_should_contain_text('确定')
        slcp.click_sure_forward()
        slcp.is_toast_exist('已转发')
        # 返回消息页面,查看文件是否发送成功
        ChatWindowPage().click_back_by_android()
        time.sleep(1)
        LableGroupDetailPage().click_back()
        time.sleep(1)
        LabelGroupingPage().click_back()
        time.sleep(1)
        ChatWindowPage().click_back_by_android()
        time.sleep(1)
        ContactsPage().click_message_icon()
        MessagePage().wait_for_page_load()
        MessagePage().is_iv_fail_status_present()

    @staticmethod
    def tearDown_test_msg_weifenglian_fenzu_0074():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep = MePage()
            mep.set_network_status(6)

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0075(self):
        """长按文件转发到任意手机联系人名称为多种字符"""
        chat = LabelGroupingChatPage()
        if LabelGroupingChatPage().is_element_present_file():
            chat.wait_for_page_load()
        else:
            Preconditions.enter_local_file_catalog()
            local_file = ChatSelectLocalFilePage()
            local_file.select_file(".txt")
            local_file.click_send()
        # 2、选择转发，选择一个群
        chat.press_file()
        #点击转发
        chat.click_forward()
        SelectContactsPage().wait_for_page_load()
        scp = SelectContactsPage()
        scp.click_phone_contact()
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        slcp.click_search_box()
        slcp.input_search_keyword('给个红包1///')
        slcp.hide_keyboard()
        if slcp.is_text_present('无搜索结果'):
            pass
        else:
            slcp.click_first_phone_contacts()
            # 3、点击确定
            time.sleep(1)
            slcp.page_should_contain_text('取消')
            slcp.page_should_contain_text('确定')
            slcp.click_sure_forward()
            flag = slcp.is_toast_exist("已转发")
            self.assertTrue(flag)

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0157(self):
        """发送位置信息"""
        # Preconditions.enter_label_grouping_chat_page()
        time.sleep(2)
        chat=LabelGroupingChatPage()
        chat.click_more()
        ChatMorePage().click_location()
        location_page = ChatLocationPage()
        if location_page.is_text_present('始终允许'):
            location_page.click_allow()
        location_page.wait_for_page_load()
        time.sleep(3)
        location_page.click_send()

































