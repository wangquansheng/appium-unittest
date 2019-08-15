from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import NoSuchElementException

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class SettingPage(BasePage):
    """设置页面"""
    ACTIVITY = 'com.cmicc.module_aboutme.ui.activity.SettingActivity'

    __locators = {
        '菜单区域': (MobileBy.CLASS_NAME, 'android.widget.ScrollView'),
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
        '返回上一页': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
        '设置': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
        'com.chinasofti.rcs:id/setting_sms': (MobileBy.ID, 'com.chinasofti.rcs:id/setting_sms'),
        '短信设置': (MobileBy.ID, 'com.chinasofti.rcs:id/setting_sms_text'),
        'com.chinasofti.rcs:id/default_SMS_app': (MobileBy.ID, 'com.chinasofti.rcs:id/default_SMS_app'),
        '消息通知': (MobileBy.ID, 'com.chinasofti.rcs:id/default_sms_text'),
        'com.chinasofti.rcs:id/callControl': (MobileBy.ID, 'com.chinasofti.rcs:id/callControl'),
        '来电管理': (MobileBy.ID, 'com.chinasofti.rcs:id/incoming_call_text'),
        'com.chinasofti.rcs:id/andNumberControl': (MobileBy.ID, 'com.chinasofti.rcs:id/andNumberControl'),
        '副号管理': (MobileBy.ID, 'com.chinasofti.rcs:id/second_number_text'),
        'com.chinasofti.rcs:id/manage_contact': (MobileBy.ID, 'com.chinasofti.rcs:id/manage_contact'),
        '联系人管理': (MobileBy.ID, 'com.chinasofti.rcs:id/manage_contact_text'),
        'com.chinasofti.rcs:id/font_setting': (MobileBy.ID, 'com.chinasofti.rcs:id/font_setting'),
        '字体大小': (MobileBy.ID, 'com.chinasofti.rcs:id/font_setting_text'),
        'com.chinasofti.rcs:id/outgoing_call_setting': (MobileBy.ID, 'com.chinasofti.rcs:id/outgoing_call_setting'),
        # '拨号设置': (MobileBy.ID, 'com.chinasofti.rcs:id/outgoing_call_setting_text'),
        '拨号设置': (MobileBy.ID, 'com.chinasofti.rcs:id/call_setting_text'),
        # com.chinasofti.rcs:id/call_setting_text
        'com.chinasofti.rcs:id/multi_language_setting': (MobileBy.ID, 'com.chinasofti.rcs:id/multi_language_setting'),
        '多语言': (MobileBy.ID, 'com.chinasofti.rcs:id/multi_language_setting_text'),
        'com.chinasofti.rcs:id/upload_log_setting': (MobileBy.ID, 'com.chinasofti.rcs:id/upload_log_setting'),
        'android:id/statusBarBackground': (MobileBy.ID, 'android:id/statusBarBackground'),
        '参与体验改善计划': (MobileBy.ID, 'com.chinasofti.rcs:id/upload_log_setting_text'),
        'com.chinasofti.rcs:id/logout': (MobileBy.ID, 'com.chinasofti.rcs:id/logout'),
        '退出': (MobileBy.ID, 'com.chinasofti.rcs:id/login_out_text'),

        '确定退出？': (MobileBy.ID, 'com.chinasofti.rcs:id/dialog_message'),
        '取消': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
        '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'),
        # 打开参与体验改善计划
		'消息': (MobileBy.ID, 'com.chinasofti.rcs:id/message'),
        '上传日志': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_send')

    }

    @TestLogger.log('点击返回上一页图标')
    def click_back(self):
        self.click_element(self.__locators['返回上一页'])

    @TestLogger.log("点击菜单")
    def click_menu(self, menu):
        # 找到就直接点击
        menu_locator = [MobileBy.XPATH, '//android.widget.TextView[@text="{}"]'.format(menu)]
        self._find_menu(menu_locator)
        self.click_element(menu_locator)

    @TestLogger.log("""检查是否包含XXX菜单项""")
    def assert_list_contains_menu(self, menu):
        # 找到就直接点击
        if self.is_text_present(menu):
            return
            # 找不到就翻页找到菜单再点击，
        self.scroll_to_top()
        max_try = 10
        current = 0
        while current < max_try:
            if self.is_text_present(menu):
                break
            current += 1
            self.page_down()
            if self.is_text_present(menu):
                break
            if self._is_element_present(self.__locators['退出']):
                raise AssertionError('找不到菜单项：{}'.format(menu))
        return

    def _is_on_the_start_of_menu_view(self):
        """判断是否在菜单开头"""
        return self._is_element_present(self.__locators['短信设置'])

    def _is_on_the_end_of_menu_view(self):
        """判断是否在菜单开头"""
        return self._is_element_present(self.__locators['退出'])

    @TestLogger.log("下一页")
    def page_down(self):
        self.wait_until(
            condition=lambda d: self.get_element(self.__locators['菜单区域'])
        )
        self.swipe_by_direction(self.__locators['菜单区域'], 'up')

    @TestLogger.log("下一页")
    def page_up(self):
        self.wait_until(
            condition=lambda d: self.get_element(self.__locators['菜单区域'])
        )
        self.swipe_by_direction(self.__locators['菜单区域'], 'down')

    @TestLogger.log()
    def scroll_to_top(self):
        self.wait_until(
            condition=lambda d: self.get_element(self.__locators['菜单区域'])
        )
        # 如果找到“短信设置”菜单，则当作已经滑到底部
        if self._is_element_present(self.__locators['短信设置']):
            return True
        max_try = 5
        current = 0
        while current < max_try:
            current += 1
            self.page_up()
            if self._is_element_present(self.__locators['短信设置']):
                break
        return True

    @TestLogger.log("滑到菜单底部")
    def scroll_to_bottom(self):
        """滑到菜单底部"""
        self.wait_until(
            condition=lambda d: self.get_element(self.__locators['菜单区域'])
        )
        # 如果找到“退出”菜单，则当作已经滑到底部
        if self._is_element_present(self.__locators['退出']):
            return True
        max_try = 5
        current = 0
        while current < max_try:
            current += 1
            self.page_down()
            if self._is_element_present(self.__locators['退出']):
                break
        return True

    @TestLogger.log("点击退出")
    def click_logout(self):
        """点击退出"""
        self.scroll_to_bottom()
        self.click_element(self.__locators['退出'])

    @TestLogger.log("点击弹框的确定按钮")
    def click_ok_of_alert(self):
        """点击弹框的确定按钮"""
        self.wait_until(
            condition=lambda d: self.get_element(self.__locators['确定'])
        ).click()

    @TestLogger.log()
    def _find_menu(self, locator):
        if not self._is_element_present(locator):
            # 找不到就翻页找到菜单再点击，
            self.scroll_to_top()
            if self._is_element_present(locator):
                return
            max_try = 5
            current = 0
            while current < max_try:
                current += 1
                self.page_down()
                if self._is_element_present(locator):
                    return
                if self._is_on_the_end_of_menu_view():
                    raise NoSuchElementException('页面找不到元素：{}'.format(locator))

    @TestLogger.log("检查页面包含文本")
    def page_contain_texts(self, menu):
        for text in menu:
            self.assert_list_contains_menu(text)
        return True


    @TestLogger.log("切换语言")
    def change_system_language(self,language):
        self.execute_shell_command('adb shell "am start -n  com.android.providers.settings/.SettingsProvider"')
        self.is_current_activity_match_this_page()

    @TestLogger.log('点击拨号设置')
    def click_dial_setting(self):
        self.click_element(self.__locators['拨号设置'])

    @TestLogger.log('点击消息')
    def click_message_setting(self):
        self.click_element(self.__locators['消息'])