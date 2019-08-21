from appium.webdriver.common.mobileby import MobileBy
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
import time


class ChatLocationPage(BasePage):
    """聊天 位置 页面"""
    ACTIVITY = 'com.cmicc.module_message.ui.activity.GDLocationActvity'

    __locators = {
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
        'com.chinasofti.rcs:id/location_back_btn': (MobileBy.ID, 'com.chinasofti.rcs:id/location_back_btn'),
        '位置': (MobileBy.ID, 'com.chinasofti.rcs:id/location_title'),
        'com.chinasofti.rcs:id/select_rl': (MobileBy.ID, 'com.chinasofti.rcs:id/select_rl'),
        '发送': (MobileBy.ID, 'com.chinasofti.rcs:id/location_ok_btn'),
        'com.chinasofti.rcs:id/map_info_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/map_info_layout'),
        'com.chinasofti.rcs:id/gd_map_view': (MobileBy.ID, 'com.chinasofti.rcs:id/gd_map_view'),
        'com.chinasofti.rcs:id/location_round_tips': (
            MobileBy.ID, 'com.chinasofti.rcs:id/location_round_tips'),
        '可选附近500米范围内的地点': (MobileBy.ID, 'com.chinasofti.rcs:id/location_round_tips_text'),
        'com.chinasofti.rcs:id/location_poi_list': (MobileBy.ID, 'com.chinasofti.rcs:id/location_poi_list'),
        'com.chinasofti.rcs:id/poi_list_item_root_view': (
            MobileBy.ID, 'com.chinasofti.rcs:id/poi_list_item_root_view'),
        '中国银行24小时自助银行(环城路)': (MobileBy.ID, 'com.chinasofti.rcs:id/poi_list_item_title'),
        '地址详细信息': (
            MobileBy.ID, 'com.chinasofti.rcs:id/poi_list_item_detail'),
        'com.chinasofti.rcs:id/poi_list_item_select': (
            MobileBy.ID, 'com.chinasofti.rcs:id/poi_list_item_select'),
        '中国铁路二十二局': (MobileBy.ID, 'com.chinasofti.rcs:id/poi_list_item_title'),
        '广东省深圳市坂田街道雪岗北路133号天安云谷对面中国铁路二十二局': (MobileBy.ID, 'com.chinasofti.rcs:id/poi_list_item_detail'),
        '博兴大厦': (MobileBy.ID, 'com.chinasofti.rcs:id/poi_list_item_title'),
        '广东省深圳市坂田街道岗头发展大厦岗头村中心围一区8号博兴大厦博兴大厦': (MobileBy.ID, 'com.chinasofti.rcs:id/poi_list_item_detail'),
        '岗头发展大厦': (MobileBy.ID, 'com.chinasofti.rcs:id/poi_list_item_title'),
        '广东省深圳市坂田街道办雪岗北路133号岗头发展大厦': (MobileBy.ID, 'com.chinasofti.rcs:id/poi_list_item_detail'),
        '选择项': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/poi_list_item_root_view"]/android.widget.ImageView'),
        '第一项': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/poi_list_item_root_view" and @index="0"]/android.widget.ImageView'),
        '其它项': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/poi_list_item_root_view" and not(android.widget.ImageView)]'),
        # 权限框
        '允许': (MobileBy.XPATH, '//android.widget.Button[@text="允许"]'),
        '拒绝': (MobileBy.XPATH, '//android.widget.Button[@text="拒绝"]'),
        '要允许 和飞信 通过网络或者卫星对您的手机定位吗？': (MobileBy.XPATH, '//*[contains(@text,"定位")] | //*[contains(@text,"位置")]'),
        '弹出框点击允许': (MobileBy.ID, 'com.android.packageinstaller:id/permission_allow_button'),
    }

    @TestLogger.log()
    def select_other_item(self):
        """选择其它项"""
        els = self.get_elements(self.__class__.__locators["其它项"])
        if els:
            els[0].click()
        else:
            print("no locations info")

    @TestLogger.log()
    def is_selected_first_item(self):
        """检查默认是否选择的是第一项"""
        els = self.get_elements(self.__class__.__locators["第一项"])
        if els:
            return True
        return False

    @TestLogger.log()
    def get_location_info(self):
        """获取发送的位置信息"""
        el = self.get_element(self.__class__.__locators["选择项"])
        addr_info = el.parent.find_element(*self.__class__.__locators["地址详细信息"]).text
        return addr_info

    @TestLogger.log()
    def click_allow(self):
        """点击允许"""
        self.click_element(self.__class__.__locators["允许"])

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def click_send(self):
        """点击发送"""
        self.click_element(self.__class__.__locators["发送"])
        time.sleep(3)

    @TestLogger.log()
    def send_btn_is_enabled(self):
        """获取发送按钮状态是否可点击"""
        return self._is_enabled(self.__class__.__locators["发送"])

    @TestLogger.log()
    def wait_for_page_load(self, timeout=60, auto_accept_alerts=True):
        """等待位置页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["位置"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def wait_for_permission_message_load(self, timeout=6, auto_accept_alerts=False):
        """等待权限允许申请弹窗加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators['要允许 和飞信 通过网络或者卫星对您的手机定位吗？'])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def click_always_allowed(self):
        """点击始终允许"""
        if self.get_elements(self.__class__.__locators['弹出框点击允许']):
            self.click_element(self.__class__.__locators['弹出框点击允许'])

