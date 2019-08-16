from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class MutiVideoPage(BasePage):
    """
    通讯录 - 标签分组 - 多方视频主叫页面
    """
    ACTIVITY = 'com.cmicc.module_call.ui.activity.MultiVideoActivity'

    __locators = {
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        'com.chinasofti.rcs:id/ll_multi_video_talking': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_multi_video_talking'),
        'com.chinasofti.rcs:id/call_setting_operation_layout': (
            MobileBy.ID, 'com.chinasofti.rcs:id/call_setting_operation_layout'),
        'com.chinasofti.rcs:id/iv_hide': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_hide'),
        '添加成员': (MobileBy.ID, 'com.chinasofti.rcs:id/multi_video_add_person'),
        'com.chinasofti.rcs:id/rv_show_video': (MobileBy.ID, 'com.chinasofti.rcs:id/rv_show_video'),
        'com.chinasofti.rcs:id/card': (MobileBy.ID, 'com.chinasofti.rcs:id/card'),
        'com.chinasofti.rcs:id/iv_item_small_switch_camera': (
            MobileBy.ID, 'com.chinasofti.rcs:id/iv_item_small_switch_camera'),
        '00:06': (MobileBy.ID, 'com.chinasofti.rcs:id/call_duration_text'),
        'com.chinasofti.rcs:id/rl_operation': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_operation'),
        'com.chinasofti.rcs:id/iv_open_self_camera': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_open_self_camera'),
        '免提图标': (MobileBy.ID, 'com.chinasofti.rcs:id/mutil_video_call_speaker_btn'),
        '静音图标': (MobileBy.ID, 'com.chinasofti.rcs:id/mutil_video_call_mute'),
        'com.chinasofti.rcs:id/end_video_call_btn': (MobileBy.ID, 'com.chinasofti.rcs:id/end_video_call_btn'),
        'com.chinasofti.rcs:id/ll_tv_hint': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_tv_hint'),
        '关闭摄像头': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_open'),
        '免提': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_multi_speaker'),
        '静音': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_multi_mute')
    }

    @TestLogger.log()
    def click_multi_video_add_person(self):
        """点击添加成员"""
        self.click_element(self.__locators["添加成员"])

    @TestLogger.log()
    def click_mutil_video_call_speaker_btn(self):
        """点击视频免提"""
        self.click_element(self.__locators["免提图标"])

    def is_selected_mutil_video_call_speaker_btn(self):
        """是否打开视频免提按钮"""
        return self.is_selected(self.__locators["免提图标"])

    @TestLogger.log()
    def click_mutil_video_call_mute(self):
        """点击静音图标"""
        self.click_element(self.__locators["静音图标"])

    def is_selected_mutil_video_call_mute(self):
        """是否打开静音图标按钮"""
        return self.is_selected(self.__locators["静音图标"])

    def wait_for_and_click_not_open(self):
        """等待暂不开启并点击"""
        try:
            if self.wait_until(timeout=5, auto_accept_permission_alert=True,
                           condition=lambda d: self.is_text_present("暂不开启")):
                self.click_text("暂不开启")
        except:
            pass

