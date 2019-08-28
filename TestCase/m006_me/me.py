import unittest
import uuid

import preconditions
from library.core.TestCase import TestCase
from library.core.utils import email_helper
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.components import ContactsSelector
from pages.components.PickGroup import PickGroupPage
from pages.components.SearchGroup import SearchGroupPage
from pages.me.NameCard import NameCardPage
from preconditions.BasePreconditions import WorkbenchPreconditions

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    'Android-XX': ''
}


class Preconditions(WorkbenchPreconditions):
    """前置条件"""


@unittest.skip("我的二维码模块先不执行")
class MeTest(TestCase):
    """我 - 我的二维码"""

    @classmethod
    def setUpClass(cls):
        Preconditions.select_mobile('Android-移动')

    @staticmethod
    def setUp_test_me_0001():
        """
        1.网络正常
        2.已登录客户端
        3.当前在我页面
        4.有群组
        :return:
        """
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        preconditions.make_already_in_message_page()
        me_page = MePage()
        me_page.open_me_page()

    @tags("ALL", "SMOKE", "CMCC")
    def test_me_0001(self):
        """我的二维码转发-选择一个群"""
        # 进入我的二维码页面
        me_page = MePage()
        me_page.click_qr_code_icon()

        # 点击转发
        qr_code = MyQRCodePage()
        # 等待加载完成
        qr_code.wait_for_loading_animation_end()
        # 解析二维码
        import time
        time.sleep(2)

        # 获取要转发的二维码（解析为链接）
        my_link = qr_code.decode_qr_code()
        print(my_link)
        qr_code.click_forward_qr_code()
        current_mobile().click_text("选择一个群", True)

        pg = PickGroupPage()
        pg.wait_for_page_load()
        pg.select_group('群聊')
        current_mobile().click_text("确定", True)

        toast = current_mobile().wait_until(
            condition=lambda d: current_mobile().get_element(['xpath', '//android.widget.Toast'])
        )
        self.assertEqual('已转发', toast.text)
        qr_code.wait_for_page_load()
        qr_code.click_back()

        me_page.open_message_page()
        current_mobile().click_text('群聊')

        chat = ChatWindowPage()
        chat.wait_for_page_load()

        # 获取截图
        screen_shot = current_mobile().get_screenshot_as_png()
        import io
        from PIL import Image
        from pyzbar import pyzbar

        # 屏幕是否包含刚刚转发的二维码（解析为文本链接）
        qrs = pyzbar.decode(Image.open(io.BytesIO(screen_shot)))
        self.assertIsNotNone(qrs)
        links = []
        for qr in qrs:
            links.append(qr.data.decode('utf-8'))
        self.assertIn(my_link, links)

    def setUp_test_me_0002(self):
        """
        1.网络正常
        2.已登录客户端
        3.当前在我页面
        4.有群组
        :return:
        """
        self.setUp_test_me_0001()

    @tags("ALL", "SMOKE", "CMCC")
    def test_me_0002(self):
        """我的二维码转发-选择本地联系人"""
        # 进入我的二维码页面
        me_page = MePage()
        me_page.click_qr_code_icon()

        # 点击转发
        qr_code = MyQRCodePage()
        # 等待加载完成
        qr_code.wait_for_loading_animation_end()
        # 解析二维码
        import time
        time.sleep(2)

        # 获取要转发的二维码（解析为链接）
        my_link = qr_code.decode_qr_code()
        print(my_link)
        qr_code.click_forward_qr_code()
        current_mobile().click_text("选择本地联系人", True)

        pg = ContactsSelector()
        pg.wait_for_page_load()
        pg.click_local_contacts('大佬1')
        current_mobile().click_text("确定", True)

        toast = current_mobile().wait_until(
            condition=lambda d: current_mobile().get_element(['xpath', '//android.widget.Toast'])
        )
        self.assertEqual('已转发', toast.text)
        qr_code.wait_for_page_load()
        qr_code.click_back()

        me_page.open_message_page()
        current_mobile().click_text('大佬1')

        chat = ChatWindowPage()
        chat.wait_for_page_load()
        # 如果弹出提示框就点击空白
        if chat.is_tips_display():
            chat.directly_close_tips_alert()

        # 获取截图
        screen_shot = current_mobile().get_screenshot_as_png()
        import io
        from PIL import Image
        from pyzbar import pyzbar

        # 屏幕是否包含刚刚转发的二维码（解析为文本链接）
        qrs = pyzbar.decode(Image.open(io.BytesIO(screen_shot)))
        self.assertIsNotNone(qrs)
        links = []
        for qr in qrs:
            links.append(qr.data.decode('utf-8'))
        self.assertIn(my_link, links)

    def setUp_test_me_0005(self):
        """
        1.网络正常
        2.已登录客户端
        3.当前在我页面
        4.有群组
        :return:
        """
        self.setUp_test_me_0001()

    @tags("ALL", "SMOKE", "CMCC")
    def test_me_0005(self):
        """我的二维码转发-选择一个群-搜索群组"""
        # 进入我的二维码页面
        me_page = MePage()
        me_page.click_qr_code_icon()

        # 点击转发
        qr_code = MyQRCodePage()
        # 等待加载完成
        qr_code.wait_for_loading_animation_end()
        # 解析二维码
        import time
        time.sleep(2)

        # 获取要转发的二维码（解析为链接）
        my_link = qr_code.decode_qr_code()
        print(my_link)
        qr_code.click_forward_qr_code()
        current_mobile().click_text("选择一个群", True)

        # 点击搜索框进入搜索群组页面
        pg = PickGroupPage()
        pg.wait_for_page_load()
        pg.search_group()

        sp = SearchGroupPage()
        sp.search('群聊')
        sp.click_group('群聊')
        current_mobile().click_text("确定", True)

        toast = current_mobile().wait_until(
            condition=lambda d: current_mobile().get_element(['xpath', '//android.widget.Toast'])
        )
        self.assertEqual('已转发', toast.text)
        qr_code.wait_for_page_load()
        qr_code.click_back()

        me_page.open_message_page()
        current_mobile().click_text('群聊')

        chat = ChatWindowPage()
        chat.wait_for_page_load()

        # 获取截图
        screen_shot = current_mobile().get_screenshot_as_png()
        import io
        from PIL import Image
        from pyzbar import pyzbar

        # 屏幕是否包含刚刚转发的二维码（解析为文本链接）
        qrs = pyzbar.decode(Image.open(io.BytesIO(screen_shot)))
        self.assertIsNotNone(qrs)
        links = []
        for qr in qrs:
            links.append(qr.data.decode('utf-8'))
        self.assertIn(my_link, links)

    def setUp_test_me_0008(self):
        """
        1.网络正常
        2.已登录客户端
        3.当前在我页面
        4.有群组
        :return:
        """
        self.setUp_test_me_0001()

    @tags("ALL", "SMOKE", "CMCC")
    def test_me_0008(self):
        """我的二维码转发-选择本地通讯录联系人-搜索已保存到本地通讯录联系人的手机号"""
        # 进入我的二维码页面
        me_page = MePage()
        me_page.click_qr_code_icon()

        # 点击转发
        qr_code = MyQRCodePage()
        # 等待加载完成
        qr_code.wait_for_loading_animation_end()
        # 解析二维码
        import time
        time.sleep(2)

        # 获取要转发的二维码（解析为链接）
        my_link = qr_code.decode_qr_code()
        print(my_link)
        qr_code.click_forward_qr_code()
        current_mobile().click_text("选择本地联系人", True)

        pg = ContactsSelector()
        pg.wait_for_page_load()
        pg.search('大佬1')
        time.sleep(1)
        pg.click_local_contacts('大佬1')
        current_mobile().click_text("确定", True)

        toast = current_mobile().wait_until(
            condition=lambda d: current_mobile().get_element(['xpath', '//android.widget.Toast'])
        )
        self.assertEqual('已转发', toast.text)
        qr_code.wait_for_page_load()
        qr_code.click_back()

        me_page.open_message_page()
        current_mobile().click_text('大佬1')

        chat = ChatWindowPage()
        chat.wait_for_page_load()
        # 如果弹出提示框就点击空白
        if chat.is_tips_display():
            chat.directly_close_tips_alert()

        # 获取截图
        screen_shot = current_mobile().get_screenshot_as_png()
        import io
        from PIL import Image
        from pyzbar import pyzbar

        # 屏幕是否包含刚刚转发的二维码（解析为文本链接）
        qrs = pyzbar.decode(Image.open(io.BytesIO(screen_shot)))
        self.assertIsNotNone(qrs)
        links = []
        for qr in qrs:
            links.append(qr.data.decode('utf-8'))
        self.assertIn(my_link, links)

    def setUp_test_me_0009(self):
        """
        1.网络正常
        2.已登录客户端
        3.当前在我页面
        4.有群组
        :return:
        """
        self.setUp_test_me_0001()

    @tags("ALL", "SMOKE", "CMCC")
    def test_me_0009(self):
        """我的二维码转发-选择本地通讯录联系人-搜索未保存到本地通讯录联系人的手机号"""
        # 进入我的二维码页面
        me_page = MePage()
        me_page.click_qr_code_icon()

        # 点击转发
        qr_code = MyQRCodePage()
        # 等待加载完成
        qr_code.wait_for_loading_animation_end()
        # 解析二维码
        import time
        time.sleep(2)

        # 获取要转发的二维码（解析为链接）
        my_link = qr_code.decode_qr_code()
        print(my_link)
        qr_code.click_forward_qr_code()
        # current_mobile().click_text("选择本地联系人", True)

        pg = ContactsSelector()
        pg.wait_for_page_load()
        pg.search('13500000000')
        time.sleep(1)
        pg.click_local_contacts('13500000000(未知号码)')
        current_mobile().click_text("确定", True)

        toast = current_mobile().wait_until(
            condition=lambda d: current_mobile().get_element(['xpath', '//android.widget.Toast'])
        )
        self.assertEqual('已转发', toast.text)
        qr_code.wait_for_page_load()
        qr_code.click_back()

        me_page.open_message_page()
        current_mobile().click_text('13500000000')

        chat = ChatWindowPage()
        chat.wait_for_page_load()
        # 如果弹出提示框就点击空白
        if chat.is_tips_display():
            chat.directly_close_tips_alert()

        # 获取截图
        screen_shot = current_mobile().get_screenshot_as_png()
        import io
        from PIL import Image
        from pyzbar import pyzbar

        # 屏幕是否包含刚刚转发的二维码（解析为文本链接）
        qrs = pyzbar.decode(Image.open(io.BytesIO(screen_shot)))
        self.assertIsNotNone(qrs)
        links = []
        for qr in qrs:
            links.append(qr.data.decode('utf-8'))
        self.assertIn(my_link, links)

    def setUp_test_me_0010(self):
        """
        1.网络正常
        2.已登录客户端
        3.当前在我页面
        4.有群组
        :return:
        """
        self.setUp_test_me_0001()

    @tags("ALL", "SMOKE", "CMCC")
    def test_me_0010(self):
        """我的二维码下载"""
        # 进入我的二维码页面
        me_page = MePage()
        me_page.click_qr_code_icon()

        # 点击转发
        qr_code = MyQRCodePage()
        # 等待加载完成
        qr_code.wait_for_loading_animation_end()
        # 解析二维码
        import time
        time.sleep(2)

        # 获取要转发的二维码（解析为链接）
        my_link = qr_code.decode_qr_code()
        print(my_link)
        qr_code.click_save_qr_code()

        toast = current_mobile().wait_until(
            condition=lambda d: current_mobile().get_element(['xpath', '//android.widget.Toast'])
        )
        self.assertEqual('已保存', toast.text)
        qr_code.click_back()
        me_page.wait_for_page_load()
        me_page.open_message_page()

    def setUp_test_me_0011(self):
        """
        1.网络正常
        2.已登录客户端
        3.当前在我页面
        4.有群组
        :return:
        """
        self.setUp_test_me_0001()

    @tags("ALL", "SMOKE", "CMCC")
    def test_me_0011(self):
        """个人资料-分享名片到群"""
        # 点击头像进入名片
        me_page = MePage()
        me_page.wait_for_head_load()
        me_page.click_head()

        # 点击分享名片
        card = NameCardPage()
        card.wait_for_page_load()
        info = card.get_name_card_info()
        print(info)
        card.click_share_btn()

        # 分享到一个群
        current_mobile().click_text("选择一个群", True)

        pg = PickGroupPage()
        pg.wait_for_page_load()
        pg.select_group('群聊')
        current_mobile().click_text("发送名片", True)

        toast = current_mobile().wait_until(
            condition=lambda d: current_mobile().get_element(['xpath', '//android.widget.Toast'])
        )
        self.assertEqual('已发送', toast.text)


@unittest.skip('用例需要重置，影响后续自动化')
class MeMsgSettingTest(TestCase):
    """模块：我-消息设置"""

    @classmethod
    def setUpClass(cls):
        Preconditions.select_mobile('Android-移动')

    @tags("ALL", "SMOKE", "CMCC_RESET")
    def test_me_msg_setting_0001(self):
        """接收139邮箱助手信息默认开启"""
        msg_setting = MessageNoticeSettingPage()
        msg_setting.wait_for_page_load()
        msg_setting.assert_menu_item_has_been_turn_on('接收139邮箱助手消息')

    @staticmethod
    def setUp_test_me_msg_setting_0001():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        preconditions.reset_and_relaunch_app()
        preconditions.make_already_in_one_key_login_page()
        preconditions.login_by_one_key_login()

        me_page = MePage()
        me_page.open_me_page()
        me_page.click_menu('设置')

        setting_page = SettingPage()
        setting_page.click_menu("消息通知")

    @tags("ALL", "SMOKE", "CMCC_RESET")
    def test_me_msg_setting_0002(self):
        """开启接收139邮箱助手信息"""
        msg_setting = MessageNoticeSettingPage()
        msg_setting.wait_for_page_load()
        msg_setting.turn_on('接收139邮箱助手消息')
        msg_setting.assert_menu_item_has_been_turn_on('接收139邮箱助手消息')
        msg_setting.click_back()

        SettingPage().click_back()
        MePage().wait_for_page_load()
        MePage().open_message_page()

        msg_page = MessagePage()
        to_address = self.login_number + '@139.com'
        email_subject, body = email_helper.send_email(to_address, '工作日报终稿', '更新内容！')
        msg_page.assert_first_message_title_in_list_is('139邮箱助手', 60)
        msg_page.click_message('139邮箱助手')

        assistant_page = EmailAssistantPage()
        assistant_page.assert_the_first_message_is('19876283465', 30)
        assistant_page.click_message('19876283465')

        email_list = EmailListPage()
        email_list.assert_the_newest_email_is(email_subject, 30)

    def setUp_test_me_msg_setting_0002(self):
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        preconditions.reset_and_relaunch_app()
        preconditions.make_already_in_one_key_login_page()
        self.login_number = preconditions.login_by_one_key_login()

        me_page = MePage()
        me_page.open_me_page()
        me_page.click_menu('设置')

        setting_page = SettingPage()
        setting_page.click_menu("消息通知")

    @tags("ALL", "SMOKE", "CMCC_RESET")
    def test_me_msg_setting_0003(self):
        """关闭接收139邮箱助手信息"""
        msg_setting = MessageNoticeSettingPage()
        msg_setting.wait_for_page_load()
        msg_setting.turn_off('接收139邮箱助手消息')
        msg_setting.assert_menu_item_has_been_turn_off('接收139邮箱助手消息')
        msg_setting.click_back()

        SettingPage().click_back()
        MePage().open_message_page()

        msg_page = MessagePage()
        to_address = self.login_number + '@139.com'
        email_helper.send_email(to_address, '工作日报终稿', '更新内容！')
        msg_page.assert_139_message_not_appear(30)

    def setUp_test_me_msg_setting_0003(self):
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        preconditions.reset_and_relaunch_app()
        preconditions.make_already_in_one_key_login_page()
        self.login_number = preconditions.login_by_one_key_login()

        me_page = MePage()
        me_page.open_me_page()
        me_page.click_menu('设置')

        setting_page = SettingPage()
        setting_page.click_menu("消息通知")

    @tags("ALL", "SMOKE", "CMCC_RESET")
    def test_me_msg_setting_0004(self):
        """接收OA消息默认开启"""
        msg_setting = MessageNoticeSettingPage()
        msg_setting.wait_for_page_load()
        msg_setting.assert_menu_item_has_been_turn_on('接收OA消息')

    @staticmethod
    def setUp_test_me_msg_setting_0004():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        preconditions.reset_and_relaunch_app()
        preconditions.make_already_in_one_key_login_page()
        preconditions.login_by_one_key_login()

        me_page = MePage()
        me_page.open_me_page()
        me_page.click_menu('设置')

        setting_page = SettingPage()
        setting_page.click_menu("消息通知")

    @tags('ALL', 'SMOKE', "CMCC_RESET")
    def test_me_msg_setting_0005(self):
        """开启接收OA消息(只验证开关，不验证消息接收)"""
        msg_setting = MessageNoticeSettingPage()
        msg_setting.turn_on('接收OA消息')
        msg_setting.assert_menu_item_has_been_turn_on('接收OA消息')

    @staticmethod
    def setUp_test_me_msg_setting_0005():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        preconditions.reset_and_relaunch_app()
        preconditions.make_already_in_one_key_login_page()
        preconditions.login_by_one_key_login()

        me_page = MePage()
        me_page.open_me_page()
        me_page.click_menu('设置')

        setting_page = SettingPage()
        setting_page.click_menu("消息通知")
        msg_setting = MessageNoticeSettingPage()
        msg_setting.wait_for_page_load()
        msg_setting.turn_off('接收OA消息')
        msg_setting.assert_menu_item_has_been_turn_off('接收OA消息')

    @tags('ALL', 'SMOKE', "CMCC_RESET")
    def test_me_msg_setting_0006(self):
        """关闭接收OA消息(只验证开关，不验证消息接收)"""
        msg_setting = MessageNoticeSettingPage()
        msg_setting.turn_off('接收OA消息')
        msg_setting.assert_menu_item_has_been_turn_off('接收OA消息')

    @staticmethod
    def setUp_test_me_msg_setting_0006():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        preconditions.reset_and_relaunch_app()
        preconditions.make_already_in_one_key_login_page()
        preconditions.login_by_one_key_login()

        me_page = MePage()
        me_page.open_me_page()
        me_page.click_menu('设置')

        setting_page = SettingPage()
        setting_page.click_menu("消息通知")
        msg_setting = MessageNoticeSettingPage()
        msg_setting.wait_for_page_load()
        msg_setting.turn_on('接收OA消息')
        msg_setting.assert_menu_item_has_been_turn_on('接收OA消息')


@unittest.skip('用例需要重置，影响后续自动化')
class MeSmsSettingTest(TestCase):
    """我-短信设置"""

    @classmethod
    def setUpClass(cls):
        Preconditions.select_mobile('Android-移动')

    @tags("ALL", "SMOKE", "CMCC_RESET")
    def test_me_sms_setting_0001(self):
        """短信设置默认关闭状态"""
        sms_setting = SmsSettingPage()
        sms_setting.assert_menu_item_has_been_turn_off('应用内收发短信')

    @staticmethod
    def setUp_test_me_sms_setting_0001():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        preconditions.reset_and_relaunch_app()
        preconditions.make_already_in_one_key_login_page()
        preconditions.login_by_one_key_login()

        me_page = MePage()
        me_page.open_me_page()
        me_page.click_menu('设置')

        setting_page = SettingPage()
        setting_page.click_menu("短信设置")

    @tags('ALL', 'SMOKE', "CMCC_RESET")
    def test_me_sms_setting_0002(self):
        """开启应用内收发短信"""
        sms_setting = SmsSettingPage()
        sms_setting.turn_on('应用内收发短信')
        sms_setting.click_button('我知道了')
        sms_setting.assert_menu_item_has_been_turn_on('应用内收发短信')
        sms_setting.click_back()

        SettingPage().click_back()
        MePage().open_message_page()

        # 切到另一台手机发短信，一定要确保配置的卡顺序与实际手机卡槽位置一致
        mobile2 = Preconditions.select_mobile('Android-XX')
        content = uuid.uuid4().__str__()
        send_number, card_type = mobile2.send_sms(self.login_number, content)

        # 切回来继续操作
        Preconditions.select_mobile('Android-移动')
        msg_page = MessagePage()
        msg_page.click_message(send_number, 15)

        chat_page = ChatWindowPage()
        if chat_page.is_tips_display():
            chat_page.directly_close_tips_alert()
        chat_page.assert_message_content_display(content)

    def setUp_test_me_sms_setting_0002(self):
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        preconditions.reset_and_relaunch_app()
        preconditions.make_already_in_one_key_login_page()
        self.login_number = preconditions.login_by_one_key_login()

        me_page = MePage()
        me_page.open_me_page()
        me_page.click_menu('设置')

        setting_page = SettingPage()
        setting_page.click_menu("短信设置")


if __name__ == '__main__':
    pass
