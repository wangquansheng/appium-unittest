import time
from appium.webdriver.common.mobileby import MobileBy
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ChatMorePage(BasePage):
    """聊天 更多 页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.MessageDetailActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/pop_10g_window_drop_view': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/pop_10g_window_drop_view'),
                  'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
                  'com.chinasofti.rcs:id/back': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
                  'com.chinasofti.rcs:id/back_arrow': (MobileBy.ID, 'com.chinasofti.rcs:id/back_arrow'),
                  '群聊0012(3)': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
                  'com.chinasofti.rcs:id/iv_slient': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_slient'),
                  'com.chinasofti.rcs:id/action_multicall': (MobileBy.ID, 'com.chinasofti.rcs:id/action_multicall'),
                  'com.chinasofti.rcs:id/action_setting': (MobileBy.ID, 'com.chinasofti.rcs:id/action_setting'),
                  'com.chinasofti.rcs:id/view_line': (MobileBy.ID, 'com.chinasofti.rcs:id/view_line'),
                  'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
                  'com.chinasofti.rcs:id/message_editor_layout': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/message_editor_layout'),
                  'com.chinasofti.rcs:id/rv_message_chat': (MobileBy.ID, 'com.chinasofti.rcs:id/rv_message_chat'),
                  'com.chinasofti.rcs:id/imgae_fl': (MobileBy.ID, 'com.chinasofti.rcs:id/imgae_fl'),
                  'com.chinasofti.rcs:id/layout_loading': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_loading'),
                  'com.chinasofti.rcs:id/imageview_msg_image': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/imageview_msg_image'),
                  'com.chinasofti.rcs:id/svd_head': (MobileBy.ID, 'com.chinasofti.rcs:id/svd_head'),
                  'com.chinasofti.rcs:id/iv_bkg': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_bkg'),
                  'com.chinasofti.rcs:id/input_and_menu': (MobileBy.ID, 'com.chinasofti.rcs:id/input_and_menu'),
                  'com.chinasofti.rcs:id/ll_text_input': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_text_input'),
                  'com.chinasofti.rcs:id/layout_for_message': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_for_message'),
                  'com.chinasofti.rcs:id/chat_rich_media_vp': (MobileBy.ID, 'com.chinasofti.rcs:id/chat_rich_media_vp'),
                  'com.chinasofti.rcs:id/iocn_img': (MobileBy.ID, 'com.chinasofti.rcs:id/iocn_img'),
                  '文件': (MobileBy.XPATH, '//*[@text="文件"]'),
                  '文件图标': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_file'),
                  '群短信': (MobileBy.XPATH, '//*[@text="群短信"]'),
                  '位置': (MobileBy.XPATH, '//*[@text="位置"]'),
                  '红包': (MobileBy.XPATH, '//*[@text="红包"]'),
                  'com.chinasofti.rcs:id/ll_rich_panel': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_rich_panel'),
                  'com.chinasofti.rcs:id/ib_pic': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_pic'),
                  'com.chinasofti.rcs:id/ib_take_photo': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_take_photo'),
                  'com.chinasofti.rcs:id/ib_profile': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_profile'),
                  'com.chinasofti.rcs:id/ib_gif': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_gif'),
                  '关闭更多': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'),
                  'com.chinasofti.rcs:id/input_divider_inside': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/input_divider_inside'),
                  'com.chinasofti.rcs:id/input_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/input_layout'),
                  'com.chinasofti.rcs:id/fl_edit_panel': (MobileBy.ID, 'com.chinasofti.rcs:id/fl_edit_panel'),
                  '说点什么...': (MobileBy.ID, 'com.chinasofti.rcs:id/et_message'),
                  'com.chinasofti.rcs:id/ib_expression': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_expression'),
                  'com.chinasofti.rcs:id/ib_audio': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_audio'),
                  '文件1': (MobileBy.XPATH, '//*[(@resource-id="com.chinasofti.rcs:id/iocn_tv") and (@text="文件")]'),
                  '音视频通话': (MobileBy.XPATH, '//*[(@resource-id="com.chinasofti.rcs:id/iocn_tv") and (@text="音视频通话")]'),
                  # com.chinasofti.rcs:id/iocn_tv
                  '和飞信电话': (MobileBy.XPATH, '//*[(@resource-id="com.chinasofti.rcs:id/iocn_tv") and (@text="和飞信电话")]'),
                  '飞信电话': (MobileBy.XPATH, "//android.widget.TextView[@text='飞信电话']"),
                  '多方视频': (MobileBy.XPATH, "//android.widget.TextView[@text='多方视频']"),
                  # '群短信': (MobileBy.XPATH, "//android.widget.TextView[@text='群短信']"),
                  '名片': (MobileBy.XPATH, "//android.widget.TextView[@text='名片']"),
                  # '位置': (MobileBy.XPATH, "//android.widget.TextView[@text='位置']"),
                  # '红包': (MobileBy.XPATH, "//android.widget.TextView[@text='红包']"),





                  }

    @TestLogger.log()
    def click_file(self):
        """点击文件"""
        self.click_element(self.__class__.__locators["文件图标"])
        time.sleep(1)

    @TestLogger.log()
    def click_group_smss(self):
        """点击群短信"""
        self.click_element(self.__class__.__locators["群短信"])

    @TestLogger.log()
    def click_location(self):
        """点击位置"""
        self.click_element(self.__class__.__locators["位置"], default_timeout=8)

    @TestLogger.log()
    def click_red_packet(self):
        """点击红包"""
        self.click_element(self.__class__.__locators["红包"])

    @TestLogger.log()
    def close_more(self):
        """关闭更多的隐藏图标（文件，群短信，位置，红包）"""
        self.click_element(self.__class__.__locators["关闭更多"])

    @TestLogger.log()
    def click_file1(self):
        """点击文件"""
        self.click_element(self.__class__.__locators["文件1"])

    @TestLogger.log()
    def click_voice_and_video_call(self):
        """点击音视频通话"""
        self.click_element(self.__class__.__locators["音视频通话"])

    @TestLogger.log()
    def click_hefeixin_call(self):
        """点击和飞信电话"""
        self.click_element(self.__class__.__locators["和飞信电话"])

    @TestLogger.log()
    def check_all_element_is_enable(self):
        """检查元素是否存在"""
        ele_list = ['飞信电话', '多方视频', '群短信', '名片', '位置', '红包']
        for ele in ele_list:
            if not self._is_enabled(self.__locators[ele]):
                return False
        return True