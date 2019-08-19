import os
import time

from appium.webdriver.common.mobileby import MobileBy

import settings
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from . import ChatSelectFilePage


class ChatSelectLocalFilePage(BasePage):
    """选择本地文件页面聊天"""
    ACTIVITY = 'com.cmicc.module_message.ui.activity.ChooseLocalFileActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/pop_10g_window_drop_view': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/pop_10g_window_drop_view'),
                  'com.chinasofti.rcs:id/select_picture_custom_toolbar': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
                  'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn'),
                  'SD卡内存': (MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_title_text'),
                  '列表容器': (MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'),
                  'com.chinasofti.rcs:id/lv_choose': (MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'),
                  'com.chinasofti.rcs:id/rl_sd_file': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_sd_file'),
                  'com.chinasofti.rcs:id/iv_icon_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_icon_layout'),
                  'com.chinasofti.rcs:id/iv_icon': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_icon'),
                  'sogou': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_file_name'),
                  'Xiaomi': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_file_name'),
                  '2018-11-09 11-06-18-722582.log': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_file_name'),
                  '410.0B': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_file_size'),
                  '10:18': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_create_time'),
                  'com.chinasofti.rcs:id/cb_choose_icon': (MobileBy.ID, 'com.chinasofti.rcs:id/cb_choose_icon'),
                  'ReleaseChannel.txt': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_file_name'),
                  '14.0B': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_file_size'),
                  '11-09 10:07': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_create_time'),
                  'test_video.mp4': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_file_name'),
                  '2.2M': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_file_size'),
                  '文件大小': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_file_size'),
                  '选择文件大小': (MobileBy.XPATH, "//android.widget.CheckBox[@checked='true']/preceding-sibling::android.widget.RelativeLayout/*[@resource-id='com.chinasofti.rcs:id/textview_file_size']"),
                  '10:19': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_create_time'),
                  'txt文件': (MobileBy.XPATH, '//*[contains(@text,".txt")]'),
                  'jpg文件': (MobileBy.XPATH, '//*[contains(@text,".jpg")]'),
                  'xlsx文件': (MobileBy.XPATH, '//*[contains(@text,".xlsx")]'),
                  'pdf文件': (MobileBy.XPATH, '//*[contains(@text,".pdf")]'),
                  'mp4文件': (MobileBy.XPATH, '//*[contains(@text,".mp4")]'),
                  'docx文件': (MobileBy.XPATH, '//*[contains(@text,".docx")]'),
                  'avi文件': (MobileBy.XPATH, '//*[contains(@text,".avi")]'),
                  'BPG文件': (MobileBy.XPATH, '//*[contains(@text,".BPG")]'),
                  'com.chinasofti.rcs:id/rl_panel': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_panel'),
                  '已选: 2.2M': (MobileBy.XPATH, '//*[contains(@text,"已选:")]'),
                  '发送': (MobileBy.ID, 'com.chinasofti.rcs:id/button_send'),
                  '继续发送': (MobileBy.XPATH, '//*[@text="继续发送"]'),
                  # 视频选择页面
                  '视频': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_file_name'),
                  # 照片选择页面
                  '照片': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_file_name'),
                  # 音乐选择页面
                  '音乐': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_file_name'),
                  # 每月10G免流特权弹窗
                  '继续发送按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/continue_call'),
                  '订购免流特权': (MobileBy.ID, 'com.chinasofti.rcs:id/get_mian_liu_permission'),
                  '以后不再提示': (MobileBy.ID, 'com.chinasofti.rcs:id/pop_window_not_pop_btn'),
                  '返回上一级': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
                  '文件显示大小':(MobileBy.ID, 'com.chinasofti.rcs:id/textview_select_file_size'),
                  '文件按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/cb_choose_icon')
                  }

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])
        time.sleep(1)

    @TestLogger.log("下一页")
    def page_up(self):
        """向上滑动一页"""
        self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)

    @TestLogger.log()
    def find_element_by_swipe(self, locator, times=15):
        """找不到元素就滑动"""
        if self._is_element_present(locator):
            return self.get_element(locator)
        else:
            c = 0
            while c < 15:
                self.page_up()
                if self._is_element_present(locator):
                    return self.get_element(locator)
                c += 1
            d=0
            while d < 15:
                self.page_down()
                if self._is_element_present(locator):
                    return self.get_element(locator)
                d += 1
            return None

    def swipe_page_up(self):
        """向上滑动"""
        self.swipe_by_percent_on_screen(50, 70, 50, 50, 800)

    def page_down(self):
        """向下滑动"""
        self.swipe_by_percent_on_screen(50, 30, 50, 70, 800)

    def find_file_by_type(self, locator, file_type, times=10):
        """根据文件类型查找文件"""
        if self._is_element_present(locator):
            els = self.get_elements(locator)
            if els:
                for el in els:
                    if el.text.endswith(file_type):
                        return el
        c = 0
        while c < times:
            # self.page_down()
            self.page_up()
            if self._is_element_present(locator):
                els = self.get_elements(locator)
                if els:
                    for el in els:
                        if el.text.endswith(file_type):
                            return el
            c += 1
        c = 0
        while c < times:
            # self.page_up()
            self.page_down()
            if self._is_element_present(locator):
                els = self.get_elements(locator)
                if els:
                    for el in els:
                        if el.text.endswith(file_type):
                            return el
            c += 1
        return None

    @TestLogger.log()
    def get_file_size(self):
        """获取选择的文件大小"""
        try:
            file_size = self.get_element(self.__class__.__locators['选择文件大小']).text
        except:
            # 获取不到大小向上滑动一点
            self.swipe_page_up()
            file_size = self.get_element(self.__class__.__locators['选择文件大小']).text
        return file_size

    @TestLogger.log()
    def get_selected_file_size(self):
        """获取已选文件大小信息"""
        el = self.get_element(self.__class__.__locators['已选: 2.2M'])
        return el.text

    @TestLogger.log()
    def select_file(self, file_type):
        """选择文件"""
        el = self.find_file_by_type((MobileBy.XPATH, '//*[contains(@text,"%s")]' % file_type), file_type)
        if el:
            el.click()
            return el
        else:
            self.make_file_into_sdcard(file_type)
            # raise AssertionError("在SD卡 无%s类型的文件，请预置相应类型文件" % file_type)

    @TestLogger.log()
    def select_file2(self, file_type):
        """选择文件"""
        els = self.get_elements(self.__class__.__locators[file_type])
        if els:
            els[0].click()
            return els[0]
        else:
            raise AssertionError("在SD卡 无%s类型的文件 或者 页面未加载出来。" % file_type)

    @TestLogger.log()
    def click_preset_file_dir(self):
        """进入预置文件的目录"""
        base_dir = os.path.basename(settings.RESOURCE_FILE_PATH)
        el = self.find_element_by_swipe((MobileBy.XPATH, '//*[@text="%s"]' % base_dir))
        if el:
            el.click()
            time.sleep(1)
            return el
        else:
            print("在SD卡根目录无%s 文件夹，请将预置文件放入此处" % base_dir)

    @TestLogger.log()
    def push_preset_file(self):
        """如果没有预置文件，则上传"""
        base_dir = os.path.basename(settings.RESOURCE_FILE_PATH)
        el = self.find_element_by_swipe((MobileBy.XPATH, '//*[@text="%s"]' % base_dir))
        if el:
            return False
        else:
            self.mobile.push_folder(settings.RESOURCE_FILE_PATH, "/sdcard")
            return True


    @TestLogger.log()
    def send_btn_is_enabled(self):
        """获取发送按钮状态是否可点击"""
        return self._is_enabled(self.__class__.__locators["发送"])

    @TestLogger.log()
    def click_send(self, timeout=4):
        """点击发送"""
        self.click_element(self.__class__.__locators["发送"])
        time.sleep(1)
        if self._is_element_present(self.__class__.__locators['继续发送']):
            self.click_element(self.__class__.__locators['继续发送'])
        time.sleep(timeout)

    @TestLogger.log()
    def is_exist_continue_send(self):
        """是否存在继续发送"""
        return self._is_element_present(self.__class__.__locators["继续发送按钮"])

    @TestLogger.log()
    def is_exist_free_flow_privilege(self):
        """是否存在免流特权"""
        return self._is_element_present(self.__class__.__locators["订购免流特权"])

    @TestLogger.log()
    def is_exist_no_longer_prompt(self):
        """是否存在不再提示"""
        return self._is_element_present(self.__class__.__locators["以后不再提示"])

    @TestLogger.log()
    def click_large_file(self):
        """点击大型文件"""
        locator = self.__class__.__locators["文件大小"]
        if self._is_element_present(locator):
            els = self.get_elements(locator)
            for el in els:
                text = el.text
                if "M" in text:
                    if float(text[0:-1]) > 3:
                        el.click()
                        return True
        times = 10
        c = 0
        while c < times:
            self.page_down()
            if self._is_element_present(locator):
                els = self.get_elements(locator)
                for el in els:
                    text = el.text
                    if "M" in text:
                        if float(text[0:-1]) > 3:
                            el.click()
                            return True
            c += 1
        c = 0
        while c < times:
            self.page_up()
            if self._is_element_present(locator):
                els = self.get_elements(locator)
                for el in els:
                    text = el.text
                    if "M" in text:
                        if float(text[0:-1]) > 3:
                            el.click()
                            return True
            c += 1
        return False

    @TestLogger.log()
    def click_send_button(self):
        """点击发送"""
        self.click_element(self.__class__.__locators["发送"])

    @TestLogger.log()
    def click_continue_send(self):
        """点击继续发送"""
        self.click_element(self.__class__.__locators["继续发送按钮"])

    @TestLogger.log()
    def click_free_flow_privilege(self):
        """点击订购免流特权"""
        self.click_element(self.__class__.__locators["订购免流特权"])

    @TestLogger.log()
    def click_no_longer_prompt(self):
        """点击不再提示"""
        self.click_element(self.__class__.__locators["以后不再提示"])

    @TestLogger.log()
    def wait_for_free_flow_privilege_page_load(self, timeout=30, auto_accept_alerts=True):
        """等待免流订购页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self.is_text_present("0元订购")
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def wait_for_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待 选择本地文件页面聊天 页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["发送"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def click_return(self):
        """点击返回上一级"""
        self.click_element(self.__class__.__locators["返回上一级"])

    @TestLogger.log()
    def click_picture(self):
        """点击照片"""
        self.click_element(self.__class__.__locators["照片"])

    @TestLogger.log()
    def click_video(self):
        """点击视频"""
        self.click_element(self.__class__.__locators["视频"])

    @TestLogger.log()
    def click_music(self):
        """点击音乐"""
        self.click_element(self.__class__.__locators["音乐"])

    @TestLogger.log()
    def wait_for_page_loads(self, timeout=60):
        """等待 页面加载"""
        try:
            self.wait_until(
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__class__.__locators["照片"]),
                timeout=timeout
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log("进入预置文件的目录")
    def enter_preset_file_dir(self):
        base_dir = os.path.basename(settings.RESOURCE_FILE_PATH)
        el = self.find_element_by_swipe((MobileBy.XPATH, '//*[@text="%s"]' % base_dir))
        if el:
            el.click()
            return el
        else:
            self.mobile.push_folder(settings.RESOURCE_FILE_PATH, "/sdcard")
            self.click_back()
            ChatSelectFilePage().click_local_file()
            self.enter_preset_file_dir()

    def make_file_into_sdcard(self, file_type):
        times = 3
        while times > 0:
            self.click_back()
            self.mobile.push_folder(settings.RESOURCE_FILE_PATH, "/sdcard")
            self.enter_preset_file_dir()
            el = self.find_file_by_type((MobileBy.XPATH, '//*[contains(@text,"%s")]' % file_type), file_type)
            if el:
                el.click()
                return
            else:
                times -= 1
        print("在SD卡 无%s类型的文件，请预置相应类型文件" % file_type)

    @TestLogger.log("当前页面是否在文件选择页")
    def is_on_this_page(self):
        try:
            self.wait_until(
                timeout=15,
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__class__.__locators["发送"])
            )
            return True
        except:
            return False

    @TestLogger.log("10G免流特权弹窗")
    def check_10G_free_data_page(self):
        self.wait_until(condition=lambda x: self.is_text_present('继续发送'), auto_accept_permission_alert=False)
        check_text = ['每月10G免流特权','继续发送','订购免流特权','以后不再提示']
        for check in check_text:
            if not self.is_text_present(check):
                return False
        return True

    # 继续发送  com.chinasofti.rcs:id/continue_call
    @TestLogger.log("点击订购免流特权")
    def click_free_data_button(self):
        self.click_element(("id","com.chinasofti.rcs:id/get_mian_liu_permission"))

    @TestLogger.log("只点击发送")
    def click_single_send(self):
        self.click_element(self.__class__.__locators["发送"])

    @TestLogger.log("点击订购免流返回")
    def click_free_data_back(self):
        self.click_element(("id","com.chinasofti.rcs:id/btn_back_actionbar"))

    @TestLogger.log("点击弹窗外面的元素关闭弹窗")
    def click_outside_element(self):
        self.mobile.click_out_side_of_element(('id', 'com.chinasofti.rcs:id/pop_window_for_10g_main_view'))

    @TestLogger.log("检测元素是否可以点击")
    def check_element_is_enable(self, locator):
        return self._is_enabled((self.__locators[locator]))

    @TestLogger.log("检测元素是否存在")
    def check_element_is_exist(self, locator):
        return self._is_element_present(self.__locators[locator])

    @TestLogger.log()
    def select_file_by_text(self, file_type):
        """选择文件"""
        el = self.find_element_by_swipe((MobileBy.XPATH, '//*[contains(@text,"%s")]' % file_type), file_type)
        if el:
            el.click()
            return el
        else:
            self.make_file_into_sdcard(file_type)


