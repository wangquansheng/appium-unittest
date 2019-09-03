import os
import time

from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile, current_driver
from library.core.utils.testcasefilter import tags
from pages import *
from pages.components import BaseChatPage
from preconditions.BasePreconditions import WorkbenchPreconditions
from settings import available_devices


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
        # 提示对话框-start
        cbp = CalllogBannerPage()
        if cbp.is_exist_feixin_call_tip():
            cbp.click_feixin_call_tip()
        time.sleep(3)
        cts = CallTypeSelectPage()
        if cts.is_text_present("知道了"):
            cts.click_i_know()
        # 提示对话框-end
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
    def make_already_have_my_picture():
        """确保当前页面已有图片"""

        # 1.点击输入框左上方的相册图标
        scp = SingleChatPage()
        cpp = ChatPicPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()
        if scp.is_exist_msg_image():
            return
        else:
            # 2.进入相片页面,选择一张片相发送
            time.sleep(2)
            scp.click_picture()
            cpp.wait_for_page_load()
            cpp.select_pic_fk(1)
            cpp.click_send()
            time.sleep(5)

    @staticmethod
    def reset_and_relaunch_app():
        """首次启动APP（使用重置APP代替）"""
        app_package = 'com.chinasofti.rcs'
        current_driver().activate_app(app_package)
        current_mobile().reset_app()

    @staticmethod
    def make_no_message_send_failed_status():
        """确保当前消息列表没有消息发送失败的标识影响验证结果"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 确保当前消息列表没有消息发送失败的标识影响验证结果
        if mp.is_iv_fail_status_present():
            mp.clear_fail_in_send_message()

    @staticmethod
    def if_exists_multiple_enterprises_enter_single_chat():
        """选择团队联系人时存在多个团队时返回获取当前团队名，再进入单聊转发图片"""

        shc = SelectHeContactsDetailPage()
        # 测试号码是否存在多个团队
        if not shc.is_exist_corporate_grade():
            mp = MessagePage()
            scg = SelectContactsPage()
            scp = SingleChatPage()
            shc.click_back()
            scg.wait_for_page_load()
            scg.click_back()
            scp.wait_for_page_load()
            scp.click_back()
            mp.wait_for_page_load()
            mp.open_workbench_page()
            wbp = WorkbenchPage()
            wbp.wait_for_workbench_page_load()
            time.sleep(2)
            # 获取当前团队名
            workbench_name = wbp.get_workbench_name()
            mp.open_message_page()
            mp.wait_for_page_load()
            single_name = "大佬1"
            Preconditions.enter_single_chat_page(single_name)
            scp.forward_pic()
            scg.wait_for_page_load()
            scg.click_he_contacts()
            shc.wait_for_he_contacts_page_load()
            # 选择当前团队
            shc.click_department_name(workbench_name)
            time.sleep(2)


class MsgPrivateChatWebMsgTest(TestCase):
    """单聊-图片、视频、GIF"""
    import sys
    global findExec
    findExec = 'findstr' if sys.platform == 'win32' else 'grep'

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
                contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
                Preconditions.create_he_contacts(contact_names)
                flag2 = True
            except:
                fail_time2 += 1
            if flag2:
                break

        # 确保有企业群
        fail_time3 = 0
        flag3 = False
        while fail_time3 < 2:
            try:
                Preconditions.make_already_in_message_page()
                Preconditions.ensure_have_enterprise_group()
                flag3 = True
            except:
                fail_time3 += 1
            if flag3:
                break

    def default_setUp(self):
        """
        1、成功登录和飞信
        2.确保每个用例运行前在单聊会话页面
        """
        Preconditions.select_mobile('Android-移动')
        name = "大佬1"
        mp = MessagePage()
        if mp.is_on_this_page():
            Preconditions.enter_single_chat_page(name)
            return
        scp = SingleChatPage()
        if scp.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
        else:
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.enter_single_chat_page(name)

    @staticmethod
    def send_one_web_msg_rscp(msg):
        """
        打开和飞信---选择联系人---发送一条网页消息
        :return: scp
        """
        mp = MessagePage()
        mp.set_network_status(6)
        scp = SingleChatPage()
        scp.wait_for_page_load()
        scp.input_message(msg)
        # 发送消息
        scp.send_message()
        cwp = ChatWindowPage()
        # 1.验证是否发送成功
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        return scp

    @staticmethod
    def send_one_web_msg_rcwp(msg):
        """
        打开和飞信---选择联系人---发送一条网页消息
        :return: scp
        """
        mp = MessagePage()
        mp.set_network_status(6)
        scp = SingleChatPage()
        scp.wait_for_page_load()
        scp.input_message(msg)
        # 发送消息
        scp.send_message()
        cwp = ChatWindowPage()
        # 1.验证是否发送成功
        cwp.wait_for_msg_send_status_become_to('发送成功', 30)
        return cwp

    @staticmethod
    def get_current_activity_name():
        device_config = os.environ['AVAILABLE_DEVICES_SETTING']
        device_name = available_devices.getConf(device_config)['M960BDQN229CH']['DEFAULT_CAPABILITY']['deviceName']
        cmd = 'adb -s %s shell dumpsys window | %s mCurrentFocus' % (device_name, findExec)
        res = os.popen(cmd)
        time.sleep(2)
        # 截取出activity名称 == 'com.chinasofti.rcs'为第三方软件   com.tencent.mm
        current_activity = res.read().split('u0 ')[-1].split('/')[1]
        res.close()
        return current_activity

    @tags('ALL', 'CMCC', 'WJH')
    def test_msg_hanjiabin_0229(self):
        """单聊会话页面，发送网页消息"""
        msg = 'http://www.baidu.com'
        scp = self.send_one_web_msg_rscp(msg)
        scp.click_back()
        time.sleep(2)

    @tags('ALL', 'CMCC', 'WJH')
    def test_msg_hanjiabin_0228(self):
        """网页消息——打开链接后的通用浏览器——右上角更多——刷新"""

        msg = 'http://www.baidu.com'
        cwp = self.send_one_web_msg_rcwp(msg)
        # 点击网页消息，打开网页
        cwp.click_text(msg)
        from pages.otherpages.WebMsgLoad import WebMsgLoad
        wml = WebMsgLoad()
        # 等待网页加载完毕
        wml.wait_for_loading_animation_end()
        # 点击右上角更多
        wml.click_more()
        from pages.otherpages.WebMore import WebMore
        wm = WebMore()
        # 点击刷新按钮
        wm.click_refresh()
        wml.wait_for_loading_animation_end()
        exist = wml.is_element_exist('com.chinasofti.rcs:id/btn_more')
        time.sleep(3)
        if not exist:
            raise RuntimeError('刷新失败')
        time.sleep(3)

    @tags('ALL', 'CMCC', 'WJH')
    def test_msg_hanjiabin_0227(self):
        """
        网页消息——打开链接后的通用浏览器——右上角更多——复制链接
        """

        msg = 'http://www.baidu.com'
        cwp = self.send_one_web_msg_rcwp(msg)
        # 点击网页消息，打开网页
        cwp.click_text(msg)
        from pages.otherpages.WebMsgLoad import WebMsgLoad
        wml = WebMsgLoad()
        # 等待网页加载完毕
        wml.wait_for_loading_animation_end()
        # 点击右上角更多
        wml.click_more()
        from pages.otherpages.WebMore import WebMore
        wm = WebMore()
        # 点击复制链接按钮
        wm.click_copy()
        # 1 验证是否复制成功
        exist = wm.is_toast_exist('内容已经复制到剪贴板')
        if not exist:
            raise RuntimeError('复制链接失败')
        time.sleep(3)

    @tags('ALL', 'CMCC', 'WJH')
    def test_msg_hanjiabin_0226(self):
        """
        网页消息——打开链接后的通用浏览器——右上角更多——在浏览器中打开
        """
        msg = 'http://www.baidu.com'
        cwp = self.send_one_web_msg_rcwp(msg)
        # 点击网页消息，打开网页
        cwp.click_text(msg)
        from pages.otherpages.WebMsgLoad import WebMsgLoad
        wml = WebMsgLoad()
        # 等待网页加载完毕
        wml.wait_for_loading_animation_end()
        # 点击右上角更多
        wml.click_more()
        from pages.otherpages.WebMore import WebMore
        wm = WebMore()
        # 点击在浏览器中打开链接按钮
        wm.click_open_in_browser()
        time.sleep(5)
        if wm.is_text_present("地理位置授权"):
            wm.click_text("允许")
        if not wm.is_text_present("百度一下"):
            raise RuntimeError('在浏览器中打失败！')

    @tags('ALL', 'CMCC', 'WJH')
    def test_msg_hanjiabin_0222(self):
        """网页消息——打开链接后的通用浏览器——右上角更多——转发给朋友"""
        msg = 'http://www.baidu.com'
        cwp = self.send_one_web_msg_rcwp(msg)
        # 点击网页消息，打开网页
        cwp.click_text(msg)
        from pages.otherpages.WebMsgLoad import WebMsgLoad
        wml = WebMsgLoad()
        # 等待网页加载完毕
        wml.wait_for_loading_animation_end()
        # 点击右上角更多
        wml.click_more()
        from pages.otherpages.WebMore import WebMore
        wm = WebMore()
        # 点击转发给朋友
        wm.click_send()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 3.选择最近聊天中的当前会话窗口
        contact_name = "大佬1"
        scg.select_recent_chat_by_name(contact_name)
        scg.click_sure_forward()
        # 1.验证是否发送成功
        exist = cwp.is_toast_exist('已转发')
        if not exist:
            raise RuntimeError('转发失败')
        time.sleep(2)
        wml.set_network_status(0)
        wml.click_more()
        wm.click_send()
        scg = SelectContactsPage()
        # 2.等待选择联系人页面加载
        scg.wait_for_page_load()
        # 3.选择最近聊天中的当前会话窗口
        contact_name = "大佬1"
        scg.select_recent_chat_by_name(contact_name)
        scg.click_sure_forward()
        # 1.验证是否发送成功
        exist = wm.is_toast_exist('已转发')
        if not exist:
            raise RuntimeError('转发失败')
        wml.click_back()
        scp = SingleChatPage()
        scp.click_back()
        mp = MessagePage()
        mp.wait_for_page_load()
        # 5.是否存在消息发送失败的标识
        present = mp.is_iv_fail_status_present()
        if not present:
            raise RuntimeError('转发操作失败')
        scp.set_network_status(6)
        time.sleep(2)

    @tags('ALL', 'CMCC', 'WJH')
    def test_msg_hanjiabin_0223(self):
        """
        网页消息——打开链接后的通用浏览器——右上角更多——转发给微信好友
        """

        msg = 'http://www.baidu.com'
        cwp = self.send_one_web_msg_rcwp(msg)
        # 点击网页消息，打开网页
        cwp.click_text(msg)
        from pages.otherpages.WebMsgLoad import WebMsgLoad
        wml = WebMsgLoad()
        # 等待网页加载完毕
        wml.wait_for_loading_animation_end()
        # 点击右上角更多
        wml.click_more()
        from pages.otherpages.WebMore import WebMore
        wm = WebMore()
        # 点击转发给朋友
        wm.click_send_wechat()
        exist = wm.is_toast_exist('未安装微信')
        if not exist:
            current_activity = self.get_current_activity_name()
            if 'com.chinasofti.rcs' == current_activity:
                raise RuntimeError('转发给微信好友失败！')
        time.sleep(2)

    @tags('ALL', 'CMCC', 'WJH')
    def test_msg_hanjiabin_0224(self):
        """
        网页消息——打开链接后的通用浏览器——右上角更多——转发给QQ好友
        """
        msg = 'http://www.baidu.com'
        cwp = self.send_one_web_msg_rcwp(msg)
        # 点击网页消息，打开网页
        cwp.click_text(msg)
        from pages.otherpages.WebMsgLoad import WebMsgLoad
        wml = WebMsgLoad()
        # 等待网页加载完毕
        wml.wait_for_loading_animation_end()
        # 点击右上角更多
        wml.click_more()
        from pages.otherpages.WebMore import WebMore
        wm = WebMore()
        # 点击转发给朋友
        wm.click_send_wechat()
        exist = wm.is_toast_exist('未安装QQ')
        if not exist:
            current_activity = self.get_current_activity_name()
            if 'com.chinasofti.rcs' == current_activity:
                raise RuntimeError('转发QQ给好友失败！')
        time.sleep(2)

    @tags('ALL', 'CMCC', 'WJH')
    def test_msg_hanjiabin_0225(self):
        """
        网页消息——打开链接后的通用浏览器——右上角更多——转发到朋友圈
        """
        msg = 'http://www.baidu.com'
        cwp = self.send_one_web_msg_rcwp(msg)
        # 点击网页消息，打开网页
        cwp.click_text(msg)
        from pages.otherpages.WebMsgLoad import WebMsgLoad
        wml = WebMsgLoad()
        # 等待网页加载完毕
        wml.wait_for_loading_animation_end()
        # 点击右上角更多
        wml.click_more()
        from pages.otherpages.WebMore import WebMore
        wm = WebMore()
        # 点击转发给朋友
        wm.click_send_wechat()
        exist = wm.is_toast_exist('未安装微信')
        if not exist:

            current_activity = self.get_current_activity_name()
            if 'com.chinasofti.rcs' == current_activity:
                raise RuntimeError('转发到朋友圈失败！')
        time.sleep(2)

    @tags('ALL', 'CMCC', 'WJH')
    def test_msg_huangcaizui_A_0278(self):
        ChatWindowPage().click_back1()
        mp = MessagePage()
        mp.click_calls()
        time.sleep(6)
        cbp = CalllogBannerPage()
        if cbp.is_exist_feixin_call_tip():
            cbp.click_feixin_call_tip()
        time.sleep(3)
        cts = CallTypeSelectPage()
        if cts.is_text_present("知道了"):
            cts.click_i_know()
        time.sleep(6)
        cp = CallPage()
        if cbp.is_exist_feixin_call_tip():
            cbp.click_feixin_call_tip()
        time.sleep(3)
        cts = CallTypeSelectPage()
        if cts.is_text_present("知道了"):
            cts.click_i_know()
        cp.wait_for_page_load()
        pad = cp.is_on_the_dial_pad()
        if not pad:
            cp.click_dial_pad()
            time.sleep(1)
            cp.click_three()
            cp.click_two()
            cp.click_five()
            cp.click_two()
            cp.click_six()
            cp.click_one()
            time.sleep(0.5)
        cp.click_call_profile()
        cdp = ContactDetailsPage()
        cdp.wait_for_page_load()
        cdp.click_message_icon()

    @tags('ALL', 'CMCC', 'WJH')
    def test_msg_huangcaizui_A_0282(self):
        """
            1.结果匹配到相关的团队联系人
            1.进入联系人详情页面
            2.进入单聊页面"
        """
        ChatWindowPage().click_back1()
        mp = MessagePage()
        mp.set_network_status(6)
        mp.click_contacts()
        cp = ContactsPage()
        cp.wait_for_page_load()
        cp.click_search_box()
        clsp = ContactListSearchPage()
        clsp.input_search_keyword('大佬1')
        if clsp.is_team_contact_in_list():
            clsp.click_team_contact()
            cdp = ContactDetailsPage()
            cdp.wait_for_page_load()
            cdp.click_message_icon()