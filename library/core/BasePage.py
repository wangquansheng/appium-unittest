import os
import re
import time

from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from library.core.TestLogger import TestLogger


class BasePage(object):
    """PageObject 应该从该基类继承"""
    ACTIVITY = ''

    @property
    def activity(self):
        return self.__class__.ACTIVITY

    @property
    def driver(self):
        return self.mobile.driver

    @property
    def mobile(self):
        from library.core.utils.applicationcache import current_mobile
        return current_mobile()

    @TestLogger.log('后台运行APP')
    def background_app(self, seconds):
        """
        APP 切换到后台运行一段时间，时间结束自动返回前台运行
        :param seconds: 后台运行的时间（单位S）
        :return:
        """
        self.mobile.background_app(seconds)

    @TestLogger.log('强制结束APP进程')
    def terminate_app(self, app_id, **options):
        """
        结束APP进程
        :param app_id: APP包名
        :param options:
        :return:
        """
        return self.mobile.terminate_app(app_id, **options)

    def _get_platform(self):
        try:
            platform_name = self.driver.desired_capabilities['platformName']
        except Exception as e:
            raise e
        return platform_name.lower()

    def _get_device_model(self):
        """获取设备型号"""
        platform = self._get_platform()
        if platform == 'android':
            model = self.execute_shell_command('getprop', 'ro.product.model')
            return model.strip()
        elif platform == 'ios':
            return 'ios'
        else:
            return 'other'

    @TestLogger.log('查找元素')
    def get_element(self, locator):
        return self.mobile.get_element(locator)

    @TestLogger.log('查找所有元素')
    def get_elements(self, locator):
        return self.mobile.get_elements(locator)

    @TestLogger.log('获取元素文本内容')
    def get_text(self, locator):
        return self.mobile.get_text(locator)

    @TestLogger.log("获取控件属性")
    def get_element_attribute(self, locator, attr, wait_time=0):
        return self.mobile.get_element_attribute(locator, attr, wait_time)

    @TestLogger.log()
    def is_text_present(self, text):
        """检查屏幕是否包含文本"""
        return self.mobile.is_text_present(text)

    def _is_element_present(self, locator):
        elements = self.get_elements(locator)
        return len(elements) > 0

    def _is_visible(self, locator):
        elements = self.get_elements(locator)
        if len(elements) > 0:
            return elements[0].is_displayed()
        return None

    def _is_clickable(self, locator):
        mapper = {
            'true': True,
            'false': False,
            'True': True,
            'False': False
        }
        element = self.get_element(locator)
        value = element.get_attribute('clickable')
        is_clickable = mapper[value.lower()]
        return is_clickable

    def _is_element_text_match(self, locator, pattern, full_match=True, regex=False):
        element = self.get_element(locator)
        actual = element.text
        if regex:
            if full_match:
                pt = re.compile(pattern)
                result = pt.fullmatch(actual)
            else:
                pt = re.compile(pattern)
                result = pt.search(actual)
        else:
            if full_match:
                result = pattern == actual
            else:
                result = pattern in actual
        if not result:
            return False
        return True

    def execute_shell_command(self, command, *args):
        """
        Execute ADB shell commands (requires server flag --relaxed-security to be set)

        例：execute_shell_command('am', 'start', '-n', 'com.example.demo/com.example.test.MainActivity')

        :param command: 例：am,pm 等等可执行命令
        :param args: 例：am,pm 等可执行命令的参数
        :return:
        """
        script = {
            'command': command,
            'args': args
        }
        return self.driver.execute_script('mobile:shell', script)

    def _is_enabled(self, locator):
        element = self.get_element(locator)
        return element.is_enabled()

    def get_source(self):
        return self.driver.page_source

    def click_element(self, locator, default_timeout=5, auto_accept_permission_alert=True):
        self.mobile.click_element(locator, default_timeout, auto_accept_permission_alert)

    def is_current_activity_match_this_page(self):
        return self.driver == self.__class__.ACTIVITY

    def click_text(self, text, exact_match=False):
        if self._get_platform() == 'ios':
            if exact_match:
                _xpath = u'//*[@value="{}" or @label="{}"]'.format(text, text)
            else:
                _xpath = u'//*[contains(@label,"{}") or contains(@value, "{}")]'.format(text, text)
            self.get_element((MobileBy.XPATH, _xpath)).click()
        elif self._get_platform() == 'android':
            if exact_match:
                _xpath = u'//*[@{}="{}"]'.format('text', text)
            else:
                _xpath = u'//*[contains(@{},"{}")]'.format('text', text)
            self.find_element_by_swipe((MobileBy.XPATH, _xpath))
            self.get_element((MobileBy.XPATH, _xpath)).click()
            # self.click_element((MobileBy.XPATH, _xpath))

    @TestLogger.log()
    def click_text_or_description(self, text):
        """点击指定元素"""
        try:
            locator = (MobileBy.XPATH, '//*[contains(@text,"%s")]' % text)
            self.click_element(locator)
        except:
            # 华为note 8手机-content-desc
            locator = (MobileBy.XPATH, '//*[contains(@content-desc,"%s")]' % text)
            self.click_element(locator)

    @TestLogger.log()
    def click_text_or_description2(self, text):
        """点击指定元素"""
        try:
            # 华为note 8手机-content-desc
            locator = (MobileBy.XPATH, '//*[contains(@content-desc,"%s")]' % text)
            self.click_element(locator)
        except:
            locator = (MobileBy.XPATH, '//*[contains(@text,"%s")]' % text)
            self.click_element(locator)

    def input_text(self, locator, text):
        self.mobile.input_text(locator, text)

    def select_checkbox(self, locator):
        """勾选复选框"""
        if not self.is_selected(locator):
            self.click_element(locator)

    def unselect_checkbox(self, locator):
        """去勾选复选框"""
        if self.is_selected(locator):
            self.click_element(locator)

    def is_selected(self, locator):
        el = self.get_element(locator)
        result = el.get_attribute("checked")
        if result.lower() == "true":
            return True
        return False

    def checkbox_should_be_selected(self, locator):
        # element = self.get_element(locator)
        if not self.is_selected(locator):
            raise AssertionError("Checkbox '{}' should have been selected "
                                 "but was not.".format(locator))
        return True

    def checkbox_should_not_be_selected(self, locator):
        # element = self.get_element(locator)
        if self.is_selected(locator):
            raise AssertionError("Checkbox '{}' should not have been selected "
                                 "but was not.".format(locator))
        return True

    def swipe_by_direction(self, locator, direction, duration=None):
        """
        在元素内滑动
        :param locator: 定位器
        :param direction: 方向（left,right,up,down）
        :param duration: 持续时间ms
        :return:
        """
        element = self.get_element(locator)
        rect = element.rect
        left, right = int(rect['x']) + 1, int(rect['x'] + rect['width']) - 1
        top, bottom = int(rect['y']) + 1, int(rect['y'] + rect['height']) - 1
        width = int(rect['width']) - 2
        height = int(rect['height']) - 2

        if self._get_platform() == 'android':
            if direction.lower() == 'left':
                x_start = right
                x_end = left
                y_start = (top + bottom) // 2
                y_end = (top + bottom) // 2
                self.driver.swipe(x_start, y_start, x_end, y_end, duration)
            elif direction.lower() == 'right':
                x_start = left
                x_end = right
                y_start = (top + bottom) // 2
                y_end = (top + bottom) // 2
                self.driver.swipe(x_start, y_start, x_end, y_end, duration)
            elif direction.lower() == 'up':
                x_start = (left + right) // 2
                x_end = (left + right) // 2
                y_start = bottom
                y_end = top
                self.driver.swipe(x_start, y_start, x_end, y_end, duration)
            elif direction.lower() == 'down':
                x_start = (left + right) // 2
                x_end = (left + right) // 2
                y_start = top
                y_end = bottom
                self.driver.swipe(x_start, y_start, x_end, y_end, duration)

        else:
            if direction.lower() == 'left':
                x_start = right
                x_offset = width
                y_start = (top + bottom) // 2
                y_offset = 0
                self.driver.swipe(x_start, y_start, x_offset, y_offset, duration)
            elif direction.lower() == 'right':
                x_start = left
                x_offset = width
                y_start = -(top + bottom) // 2
                y_offset = 0
                self.driver.swipe(x_start, y_start, x_offset, y_offset, duration)
            elif direction.lower() == 'up':
                x_start = (left + right) // 2
                x_offset = 0
                y_start = bottom
                y_offset = -height
                self.driver.swipe(x_start, y_start, x_offset, y_offset, duration)
            elif direction.lower() == 'down':
                x_start = (left + right) // 2
                x_offset = 0
                y_start = top
                y_offset = height
                self.driver.swipe(x_start, y_start, x_offset, y_offset, duration)

    def swipe_by_direction2(self, locator, direction, number, duration=None):
        """
        在元素内滑动
        :param locator: 定位器
        :param direction: 方向（left,right,up,down）
        :param duration: 持续时间ms
        :return:
        """
        elements = self.get_elements(locator)
        element = elements[number]
        rect = element.rect
        left, right = int(rect['x']) + 1, int(rect['x'] + rect['width']) - 1
        top, bottom = int(rect['y']) + 1, int(rect['y'] + rect['height']) - 1
        width = int(rect['width']) - 2
        height = int(rect['height']) - 2

        if self._get_platform() == 'android':
            if direction.lower() == 'left':
                x_start = right
                x_end = left
                y_start = (top + bottom) // 2
                y_end = (top + bottom) // 2
                self.driver.swipe(x_start, y_start, x_end, y_end, duration)
            elif direction.lower() == 'right':
                x_start = left
                x_end = right
                y_start = (top + bottom) // 2
                y_end = (top + bottom) // 2
                self.driver.swipe(x_start, y_start, x_end, y_end, duration)
            elif direction.lower() == 'up':
                x_start = (left + right) // 2
                x_end = (left + right) // 2
                y_start = bottom
                y_end = top
                self.driver.swipe(x_start, y_start, x_end, y_end, duration)
            elif direction.lower() == 'down':
                x_start = (left + right) // 2
                x_end = (left + right) // 2
                y_start = top
                y_end = bottom
                self.driver.swipe(x_start, y_start, x_end, y_end, duration)

        else:
            if direction.lower() == 'left':
                x_start = right
                x_offset = width
                y_start = (top + bottom) // 2
                y_offset = 0
                self.driver.swipe(x_start, y_start, x_offset, y_offset, duration)
            elif direction.lower() == 'right':
                x_start = left
                x_offset = width
                y_start = -(top + bottom) // 2
                y_offset = 0
                self.driver.swipe(x_start, y_start, x_offset, y_offset, duration)
            elif direction.lower() == 'up':
                x_start = (left + right) // 2
                x_offset = 0
                y_start = bottom
                y_offset = -height
                self.driver.swipe(x_start, y_start, x_offset, y_offset, duration)
            elif direction.lower() == 'down':
                x_start = (left + right) // 2
                x_offset = 0
                y_start = top
                y_offset = height
                self.driver.swipe(x_start, y_start, x_offset, y_offset, duration)

    def swipe_by_percent_on_screen(self, start_x, start_y, end_x, end_y, duration):
        width = self.driver.get_window_size()["width"]
        height = self.driver.get_window_size()["height"]
        x_start = float(start_x) / 100 * width
        x_end = float(end_x) / 100 * width
        y_start = float(start_y) / 100 * height
        y_end = float(end_y) / 100 * height
        x_offset = x_end - x_start
        y_offset = y_end - y_start
        if self._get_platform() == 'android':
            self.driver.swipe(x_start, y_start, x_end, y_end, duration)
        else:
            self.driver.swipe(x_start, y_start, x_offset, y_offset, duration)

    def page_should_contain_text(self, text, timeout=8):
        try:
            if not self.wait_until(condition=lambda x: self.is_text_present(text), timeout=timeout):
                raise AssertionError("Page should have contained text '{}' "
                                 "but did not" % text)
            return True
        except:
            import time
            time.sleep(3)
            return self.is_text_present(text)

    def page_should_contain_text2(self, text):
        try:
            return self.wait_until(condition=lambda x: self.is_text_present(text))
        except:
            return False

    def page_should_not_contain_text(self, text):
        if self.is_text_present(text):
            raise AssertionError("Page should not have contained text '{}'" % text)
        return True

    def page_should_contain_element(self, locator):
        if not self._is_element_present(locator):
            raise AssertionError("Page should have contained element '{}' "
                                 "but did not".format(locator))
        return True

    def page_should_not_contain_element(self, locator):
        if self._is_element_present(locator):
            raise AssertionError("Page should not have contained element {}".format(locator))
        return True

    def element_should_be_disabled(self, locator):
        if self._is_enabled(locator):
            raise AssertionError("Element '{}' should be disabled "
                                 "but did not".format(locator))
        return True

    def element_should_be_enabled(self, locator):
        if not self._is_enabled(locator):
            raise AssertionError("Element '{}' should be enabled "
                                 "but did not".format(locator))
        return True

    def element_should_be_visible(self, locator):
        if not self.get_element(locator).is_displayed():
            raise AssertionError("Element '{}' should be visible "
                                 "but did not".format(locator))
        return True

    def element_should_contain_text(self, locator, expected, message=''):
        actual = self.get_text(locator)
        if expected not in actual:
            if not message:
                message = "Element '{}' should have contained text '{}' but " \
                          "its text was '{}'.".format(locator, expected, actual)
            raise AssertionError(message)
        return True

    def element_should_not_contain_text(self, locator, expected, message=''):
        actual = self.get_text(locator)
        if expected in actual:
            if not message:
                message = "Element {} should not contain text '{}' but " \
                          "it did.".format(locator, expected)
            raise AssertionError(message)
        return True

    def element_text_should_be(self, locator, expected, message=''):
        element = self.get_element(locator)
        actual = element.text
        if expected != actual:
            if not message:
                message = "The text of element '{}' should have been '{}' but in fact it was '{}'." \
                    .format(locator, expected, actual)
            raise AssertionError(message)
        return True

    def element_text_should_match(self, locator, pattern, full_match=True, regex=False):
        """断言元素内文本，支持正则表达式"""
        return self.mobile.assert_element_text_should_match(locator, pattern, full_match, regex)

    def wait_until(self, condition, timeout=8, auto_accept_permission_alert=True):
        return self.mobile.wait_until(condition, timeout=timeout,
                                      auto_accept_permission_alert=auto_accept_permission_alert)

    def wait_condition_and_listen_unexpected(
            self,
            condition,
            timeout=8,
            poll=0.2,
            auto_accept_permission_alert=True,
            unexpected=None,
            *args,
            **kwargs
    ):
        return self.mobile.wait_condition_and_listen_unexpected(
            condition=condition,
            timeout=timeout,
            poll=poll,
            auto_accept_permission_alert=auto_accept_permission_alert,
            unexpected=unexpected,
            args=args,
            kwargs=kwargs
        )

    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """默认使用activity作为判断页面是否加载的条件，继承类应该重写该方法"""
        self.wait_until(
            lambda d: self.driver.current_activity == self.ACTIVITY,
            timeout,
            auto_accept_alerts
        )
        return self

    def _is_text_present_contains(self, locator, pattern, full_match=False, regex=False):
        element = self.get_element(locator)
        actual = element.text
        if regex:
            if full_match:
                pt = re.compile(pattern)
                result = pt.fullmatch(actual)
            else:
                pt = re.compile(pattern)
                result = pt.search(actual)
        else:
            if full_match:
                result = pattern == actual
            else:
                result = pattern in actual
        if not result:
            return False
        return True

    def run_app_in_background(self, seconds=5):
        """让 app 进入后台运行seconds 秒"""
        self.driver.background_app(seconds)

    def get_error_code_info_by_adb(self, pattern, timeout=5):
        """通过adb log 获取错误码信息"""
        os.system("adb logcat -c")
        cmd = ' adb logcat -d |findstr %s > tmp.txt' % pattern
        n = 0
        code_info = None
        while n < timeout:
            os.system(cmd)
            with open("tmp.txt", 'r', encoding="utf-8") as f:
                code_info = f.read()
                if code_info:
                    break
                else:
                    time.sleep(1)
                    n += 1
                    continue
        if os.path.exists("tmp.txt"):
            os.remove("tmp.txt")
        return code_info

    def get_network_status(self):
        """获取网络链接状态"""
        return self.mobile.get_network_status()

    def set_network_status(self, status):
        """设置网络
        Connection types are specified here:
        https://code.google.com/p/selenium/source/browse/spec-draft.md?repo=mobile#120
        Value (Alias)      | Data | Wifi | Airplane Mode
        -------------------------------------------------
        0 (None)           | 0    | 0    | 0
        1 (Airplane Mode)  | 0    | 0    | 1
        2 (Wifi only)      | 0    | 1    | 0
        4 (Data only)      | 1    | 0    | 0
        6 (All network on) | 1    | 1    | 0

        class ConnectionType(object):
            NO_CONNECTION = 0
            AIRPLANE_MODE = 1
            WIFI_ONLY = 2
            DATA_ONLY = 4
            ALL_NETWORK_ON = 6

        """
        return self.mobile.set_network_status(status)

    def is_toast_exist(self, text, timeout=30, poll_frequency=0.5):
        """is toast exist, return True or False
        :Args:
         - text   - toast文本内容
         - timeout - 最大超时时间，默认30s
         - poll_frequency  - 间隔查询时间，默认0.5s查询一次
        :Usage:
         is_toast_exist("toast的内容")
        """
        try:
            toast_loc = ("xpath", ".//*[contains(@text,'%s')]" % text)
            WebDriverWait(self.driver, timeout, poll_frequency).until(EC.presence_of_element_located(toast_loc))
            return True
        except:
            return False

    @TestLogger.log('隐藏键盘')
    def hide_keyboard(self, key_name=None, key=None, strategy=None):
        """隐藏键盘"""
        self.mobile.hide_keyboard(key_name, key, strategy)

    def press(self, el, times=3000):
        """按压操作"""
        TouchAction(self.driver).long_press(el, duration=times).wait(1).perform()

    def press_xy(self,times=3000):
        """按压操作"""
        width = self.driver.get_window_size()["width"]
        height = self.driver.get_window_size()["height"]
        x=width/2
        y=height/2
        el = None
        TouchAction(self.driver).long_press(el,x,y, duration=times).wait(1).perform()

    @TestLogger.log('获取元素指定坐标颜色')
    def get_coordinate_color_of_element(self, element, x, y, by_percent=False, mode='RGBA') -> tuple:
        return self.mobile.get_coordinate_color_of_element(element, x, y, by_percent, mode)

    @TestLogger.log("按住并向下滑动")
    def press_and_move_to_down(self, locator):
        """按住并滑动"""
        element = self.get_element(locator)
        rect = element.rect
        pointX = int(rect["x"]) + int(rect["width"])/2
        pointY = int(rect["y"]) + int(rect["height"]) * 1
        TouchAction(self.driver).long_press(element, duration=3000).move_to(element, pointX,
                                                                                    pointY).wait(1).release().perform()

    @TestLogger.log("按住并向上滑动")
    def press_and_move_to_up(self, locator):
        """按住并滑动"""
        element = self.get_element(locator)
        rect = element.rect
        pointX = int(rect["x"]) + int(rect["width"])/2
        pointY = -(int(rect["y"]) - 20)
        # pointY=0
        TouchAction(self.driver).long_press(element, duration=3000).move_to(element, pointX,
                                                                                    pointY).wait(3).release().perform()

    def tap_coordinate(self, positions):
        """模拟手指点击（最多五个手指）positions:[(100, 20), (100, 60), (100,100)]"""
        return self.mobile.tap(positions)

    @TestLogger.log('键盘是否弹起')
    def is_keyboard_shown(self):
        """判断键盘是否弹起"""
        return self.mobile.is_keyboard_shown()

    @TestLogger.log("点击返回")
    def click_back(self):
        """点击返回"""
        self.click_element((MobileBy.XPATH, "//*[contains(@resource-id, 'back')]"), 10)
        time.sleep(1)

    @TestLogger.log()
    def click_back_by_android(self, times=1):
        """android内置键返回"""
        # times 返回次数
        for i in range(times):
            self.driver.back()
            time.sleep(1)

    @TestLogger.log("下一页")
    def page_up(self):
        """向上滑动一页"""
        self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)

    @TestLogger.log("上一页")
    def page_down(self):
        """向下滑动"""
        self.swipe_by_percent_on_screen(50, 30, 50, 70, 800)

    @TestLogger.log('挂断电话')
    def hang_up_the_call(self):
        """挂断电话"""
        return self.mobile.hang_up_the_call()

    @TestLogger.log('接听电话')
    def pick_up_the_call(self):
        """接听电话"""
        return self.mobile.pick_up_the_call()

    @TestLogger.log('判断是否在通话界面')
    def is_phone_in_calling_state(self):
        """判断是否在通话界面"""
        return self.mobile.is_phone_in_calling_state()

    @TestLogger.log()
    def find_element_by_swipe(self, locator, times=20):
        """找不到元素就滑动"""
        if self._is_element_present(locator):
            return self.get_element(locator)
        else:
            c = 0
            while c < times:
                self.page_up()
                if self._is_element_present(locator):
                    return self.get_element(locator)
                c += 1
            return None

    @TestLogger.log()
    def click_one_contact(self, contactName):
        """选择特定联系人"""
        el = self.find_element_by_swipe((MobileBy.XPATH, '//*[@text="%s"]' % contactName))
        if el:
            el.click()
            return el
        else:
            print("本地联系人中无%s ，请添加此联系人再操作" % contactName)

    @TestLogger.log('模擬android电源键')
    def press_power_key(self):
        """模擬android电源键"""
        return self.execute_shell_command('input', 'keyevent', 26)

    @TestLogger.log("判断设备是否锁屏")
    def is_locked(self):
        """判断设备是否锁屏"""
        return self.driver.is_locked()

    @TestLogger.log()
    def is_exit_element_by_text_swipe(self, contactName):
        """滑动判断特定元素是否存在"""
        el = self.find_element_by_swipe((MobileBy.XPATH, '//*[@text="%s"]' % contactName))
        if el:
            return True
        else:
            return False

    def page_left(self):
        """向右滑动"""
        self.swipe_by_percent_on_screen(50, 70, 20, 70, 800)

    def page_right(self):
        """向左滑动"""
        self.swipe_by_percent_on_screen(50, 70, 80, 70, 800)


    @TestLogger.log()
    def is_element_present_on_desktop(self, text):
        max_try = 5
        current = 0
        while current < max_try:
            if self.is_text_present(text):
                return self.page_should_contain_text(text)
            current += 1
            self.page_left()

        current=0
        while current < max_try:
            if self.is_text_present(text):
                return self.page_should_contain_text(text)
            current += 1
            self.page_right()
        return False

    @TestLogger.log()
    def press_text(self, file):
        """长按指定文件进行操作"""
        el = self.get_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % file))
        self.press(el)

    @TestLogger.log()
    def push_resource_file(self):
        """上传预置文件"""
        import settings
        self.mobile.push_folder(settings.RESOURCE_FILE_PATH, "/sdcard")
