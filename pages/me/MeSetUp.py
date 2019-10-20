from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger

class MeSetUpPage(BasePage):
    """我 -> 设置 页面"""
    ACTIVITY = 'com.cmicc.module_aboutme.ui.activity.SettingActivity'

    locators = {'': (MobileBy.ID, ''),
                'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                'android:id/content': (MobileBy.ID, 'android:id/content'),
                'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
                'com.chinasofti.rcs:id/back': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
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
                'com.chinasofti.rcs:id/outgoing_call_setting': (
                MobileBy.ID, 'com.chinasofti.rcs:id/outgoing_call_setting'),
                '拨号设置': (MobileBy.ID, 'com.chinasofti.rcs:id/outgoing_call_setting_text'),
                'com.chinasofti.rcs:id/multi_language_setting': (
                MobileBy.ID, 'com.chinasofti.rcs:id/multi_language_setting'),
                '多语言': (MobileBy.ID, 'com.chinasofti.rcs:id/multi_language_setting_text'),
                'com.chinasofti.rcs:id/upload_log_setting': (MobileBy.ID, 'com.chinasofti.rcs:id/upload_log_setting'),
                '参与体验改善计划': (MobileBy.ID, 'com.chinasofti.rcs:id/upload_log_setting_text'),
                'android:id/statusBarBackground': (MobileBy.ID, 'android:id/statusBarBackground'),
                'android:id/navigationBarBackground': (MobileBy.ID, 'android:id/navigationBarBackground'),
                # 设置-》退出
                '确定退出？': (MobileBy.ID, 'com.chinasofti.rcs:id/dialog_message'),
                'com.chinasofti.rcs:id/btn_container': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_container'),
                '取消': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
                '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'),
                # 设置-》短信设置

                '通话': (MobileBy.ID, 'com.chinasofti.rcs:id/call'),


                }

    @TestLogger.log()
    def click_call_setting(self, type):
        """通话》拨号方式 》优先使用和飞信电话（免费）"""
        self.click_element(self.locators['通话'])
        from pages import MeSetDialPage
        mesetdial = MeSetDialPage()
        mesetdial.click_dial_mode()
        mesetdial.select_dial_mode(type)
