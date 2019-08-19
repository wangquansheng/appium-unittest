from appium.webdriver.common.mobileby import MobileBy
import time
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ChatGIFPage(BasePage):
    """聊天gif页面"""
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
                  'com.chinasofti.rcs:id/ll_gif_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_gif_layout'),
                  '关闭gif': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_cancel_gif'),
                  '所有gif': (MobileBy.XPATH, "//*[@resource-id='com.chinasofti.rcs:id/stickers_container']/android.widget.ImageView"),
                  'com.chinasofti.rcs:id/bqss_hscrollview': (MobileBy.ID, 'com.chinasofti.rcs:id/bqss_hscrollview'),
                  'com.chinasofti.rcs:id/stickers_container': (MobileBy.ID, 'com.chinasofti.rcs:id/stickers_container'),
                  'com.chinasofti.rcs:id/ll_text_input': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_text_input'),
                  'com.chinasofti.rcs:id/layout_for_message': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_for_message'),
                  'com.chinasofti.rcs:id/input_divider_inside': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/input_divider_inside'),
                  'com.chinasofti.rcs:id/input_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/input_layout'),
                  'com.chinasofti.rcs:id/fl_edit_panel': (MobileBy.ID, 'com.chinasofti.rcs:id/fl_edit_panel'),
                  '趣图搜搜...': (MobileBy.ID, 'com.chinasofti.rcs:id/et_message'),
                  'com.chinasofti.rcs:id/ib_expression': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_expression'),
                  '表情按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_expression'),
                  '语音按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_audio'),
                  '发送按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_send'),
                  }

    @TestLogger.log('')
    def is_on_this_page(self):
        el = self.get_elements(self.__class__.__locators['所有gif'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log()
    def wait_for_page_load(self, timeout=60, auto_accept_alerts=True):
        """等待聊天gif页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["所有gif"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def click_expression_icon(self):
        """点击表情按钮"""
        self.click_element(self.__class__.__locators["表情按钮"])

    @TestLogger.log()
    def input_message(self, message):
        """输入搜索信息"""
        self.input_text(self.__class__.__locators["趣图搜搜..."], message)
        time.sleep(1)
        return self

    @TestLogger.log()
    def send_message(self):
        """发送聊天信息"""
        self.click_element(self.__class__.__locators["发送按钮"])
        time.sleep(1)

    @TestLogger.log()
    def close_gif(self):
        """关闭gif"""
        self.click_element(self.__class__.__locators["关闭gif"])
        time.sleep(1)

    @TestLogger.log()
    def send_gif(self, n=0):
        """发送第n个gif"""
        els = self.get_elements(self.__class__.__locators["所有gif"])
        if els and n < len(els):
            els[n].click()
            time.sleep(3)
        else:
            raise AssertionError("There is no %s gif." % n)

    @TestLogger.log()
    def is_gif_exist(self):
        """gif是否打开"""
        return self._is_element_present(self.__class__.__locators["关闭gif"])

    @TestLogger.log()
    def is_gif_head_exist(self):
        """检验会话窗口是否有gif头像"""
        return self.page_should_contain_element(self.__class__.__locators["com.chinasofti.rcs:id/svd_head"])

