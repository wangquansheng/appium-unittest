import base64
import contextlib
import functools
import hashlib
import json
import os
import re
from abc import *
from unicodedata import normalize

from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import TimeoutException, \
    NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from library.core.TestLogger import TestLogger


class MobileDriver(ABC):
    def __init__(self, alis_name, model_info, command_executor='http://127.0.0.1:4444/wd/hub',
                 desired_capabilities=None, browser_profile=None, proxy=None, keep_alive=False, card_slot=None):
        self._alis = alis_name
        self._model_info = model_info
        self._remote_url = command_executor
        self._desired_caps = self._init_capability(desired_capabilities)
        self._browser_profile = browser_profile
        self._proxy = proxy
        self._keep_alive = keep_alive
        self._card_slot = self._init_sim_card(card_slot)
        self._driver = None
        self.turn_off_reset()

    def __del__(self):
        if self.is_connection_created:
            self.driver.quit()

    @property
    def alis(self):
        return self._alis

    @property
    def model_info(self):
        return self._model_info

    @TestLogger.log('打开通知栏')
    def open_notifications(self):
        """打开通知栏"""
        if self.is_android():
            self.driver.open_notifications()
        else:
            # TODO IOS打开通知栏待实现
            pass

    def back(self):
        """返回"""
        self.driver.back()

    @property
    def driver(self):
        return self._driver

    @property
    def current_activity(self):
        return self.driver.current_activity

    @property
    def current_package(self):
        return self.driver.current_package

    @abstractmethod
    def total_card_slot(self):
        """卡槽数量，例如: 1、2"""
        raise NotImplementedError("This method must be implemented!")

    @staticmethod
    def _init_capability(caps):
        return caps

    def _init_sim_card(self, card_slot):
        """初始化手机SIM"""
        cards = []
        if not isinstance(card_slot, list):
            raise Exception('数据类型异常')
        for n in range(self.total_card_slot()):
            if n < len(card_slot):
                card = card_slot[n]
                if isinstance(card, dict):
                    if card['TYPE'] in self.supported_card_types():
                        cards.append(card)
                    else:
                        raise Exception('该手机不支持' + card_slot[n]['TYPE'] + '类型SIM卡（支持类型：{}）'
                                        .format(self.supported_card_types()))
        return cards

    @TestLogger.log('获取指定运营商类型的手机卡（不传类型返回全部配置的手机卡）')
    def get_cards(self, card_type=None):
        """返回指定类型卡手机号列表"""
        cards = [card for card in self._card_slot if card is not None]
        if card_type is None:
            return list(
                [card.get('CARD_NUMBER') for card in cards]
            )
        if not isinstance(card_type, list):
            card_type = [card_type]
        return list(
            [card.get('CARD_NUMBER') for card in self._card_slot if (card is not None) and (card['TYPE'] in card_type)]
        )

    @TestLogger.log('获取手机卡号')
    def get_card(self, index):
        """
        获取手机卡信息
        :param index: 卡槽位置
        :return: 号码、运营商类型
        """
        return self._card_slot[index].get('CARD_NUMBER'), self._card_slot[index].get('TYPE')

    @abstractmethod
    def supported_card_types(self):
        """返回手机卡支持类型列表"""
        raise NotImplementedError("This method must be implemented!")

    @property
    def is_connection_created(self):
        if self.driver is None:
            return False
        else:
            try:
                t = self.driver.find_elements('xpath', '//*')
                del t
                return True
            except Exception:  # InvalidSessionIdException or WebDriverException:
                return False

    @TestLogger.log('连接到手机')
    def connect_mobile(self):
        if self.driver is None:
            try:
                self._driver = webdriver.Remote(self._remote_url, self._desired_caps, self._browser_profile,
                                                self._proxy,
                                                self._keep_alive)
            except Exception as e:
                raise RuntimeError('无法连接到 appium server: {}'.format(self._remote_url))
        elif not self.is_connection_created:
            try:
                self.driver.quit()
            except:
                pass
            try:
                self._driver = webdriver.Remote(self._remote_url, self._desired_caps, self._browser_profile,
                                                self._proxy,
                                                self._keep_alive)
            except:
                import traceback
                msg = traceback.format_exc()
                print(msg)
                raise RuntimeError('无法连接到 appium server: {}'.format(self._remote_url))
        else:
            pass
        if self.is_android:
            app_version_info = self.get_app_version_info()
            real_model = self.get_mobile_model_info()
            network_state_info = self.get_mobile_network_connection_info()
            print(
                """
已连接到手机：
===================== Mobile Name =====================
%(mobileName)s
===================== APP Version =====================
%(appVersion)s
================= Network Status Info =================
%(networkState)s
=======================================================
                """ % dict(
                    mobileName=real_model,
                    appVersion=app_version_info,
                    networkState=network_state_info
                )
            )
        self.model_info["ReadableName"] = self.get_mobile_model_info()

    @TestLogger.log('断开手机连接')
    def disconnect_mobile(self):
        try:
            self.driver.quit()
        except:
            pass

    @TestLogger.log('打开重置APP选项（仅当手机未连接时有效）')
    def turn_on_reset(self):
        """开启重置app（在获取session之前有效）"""
        self._desired_caps['noReset'] = False

    # @TestLogger.log('关闭重置APP选项（仅当手机未连接时有效）')
    def turn_off_reset(self):
        """关闭重置app（在获取session之前有效）"""
        self._desired_caps['noReset'] = True

    @TestLogger.log('判断当前设备与传入平台名是否一致')
    def is_platform(self, platform):
        if self.is_connection_created:
            platform_name = self.driver.desired_capabilities['platformName']
        else:
            platform_name = self._desired_caps['platformName']
        return platform.lower() == platform_name.lower()

    @TestLogger.log('判断当前设备是否为IOS设备')
    def is_ios(self):
        return self.is_platform('ios')

    @TestLogger.log('判断当前设备是否为Android设备')
    def is_android(self):
        return self.is_platform('android')

    @TestLogger.log('启动默认APP')
    def launch_app(self):
        self.driver.launch_app()

    @TestLogger.log('强制结束APP进程')
    def terminate_app(self, app_id, **options):
        return self.driver.terminate_app(app_id, **options)

    @TestLogger.log('将当前打开的APP后台运行指定时间(S)')
    def background_app(self, seconds):
        self.driver.background_app(seconds)

    @TestLogger.log('激活APP')
    def activate_app(self, app_id=None):
        if not app_id:
            app_id = self.driver.desired_capabilities['appPackage']
        self.driver.activate_app(app_id)

    @TestLogger.log('重置当前打开的APP')
    def reset_app(self):
        # self.driver.reset()
        # 屏蔽所有重置操作
        pass

    @TestLogger.log('获取屏幕截图')
    def get_screenshot_as_png(self):
        """
        Gets the screenshot of the current window as a binary data.

        :Usage:
            driver.get_screenshot_as_png()
        """
        return self.driver.get_screenshot_as_png()

    @TestLogger.log('点按手机Home键')
    def press_home_key(self):
        """模拟手机HOME键"""
        if self.is_android():
            self.execute_shell_command('input', 'keyevent', 3)
            return
        elif self.is_ios():
            # TODO
            raise NotImplementedError('IOS 点击HOME键未实现')
        else:
            raise NotImplementedError('该API不支持android/ios以外的系统')

    @TestLogger.log('执行ADB shell命令')
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
        result = self.driver.execute_script('mobile:shell', script)
        print(result)
        return result

    @contextlib.contextmanager
    def listen_verification_code(self, max_wait_time=30):
        """监听验证码"""
        context = self._actions_before_send_get_code_request()
        code_container = []
        yield code_container
        code = self._actions_after_send_get_code_request(context, max_wait_time)
        if isinstance(code, list):
            code_container.append(code[0])
        elif isinstance(code, str):
            code_container.append(code)

    def _actions_before_send_get_code_request(self):
        """开始获取验证码之前的动作"""
        try:
            self.execute_shell_command('logcat', '-c')
        except Exception as e:
            print(e.__str__())

    def _actions_after_send_get_code_request(self, context, max_wait_time):
        """开始获取验证码之后的动作，结果为返回的验证码"""
        result = self.wait_until(
            condition=lambda d: re.findall(r'【登录验证】尊敬的用户：(\d+)',
                                           self.execute_shell_command('logcat', '-d', 'appium:D', 'MmsService:W', '*:S')
                                           ),
            timeout=max_wait_time
        )
        if result:
            return result[0]
        raise Exception("手机收不到验证码")

    @TestLogger.log('等待')
    def wait_until(
            self,
            condition,
            timeout=8,
            auto_accept_permission_alert=True
    ):
        wait = WebDriverWait(self.driver, timeout)
        if auto_accept_permission_alert:
            condition = self._auto_click_permission_alert_wrapper(condition)
        # if callable(unexpected):
        #     condition = self._error_listener(unexpected, *args, **kwargs)(condition)
        return wait.until(condition)

    @TestLogger.log('等待')
    def wait_until_not(
            self,
            condition,
            timeout=8,
            auto_accept_permission_alert=True
    ):
        wait = WebDriverWait(self.driver, timeout)
        if auto_accept_permission_alert:
            condition = self._auto_click_permission_alert_wrapper(condition)
        # if callable(unexpected):
        #     condition = self._error_listener(unexpected, *args, **kwargs)(condition)
        return wait.until_not(condition)

    @staticmethod
    def _error_listener(error_determine_func, *arguments, **keyword_args):
        """
        错误监听装饰器，用于等待的期间抓取可能出现的异常
        :param error_determine_func: 抓取异常的方法
        :param arguments: 抓取异常的方法的参数
        :param keyword_args: 抓取异常的方法的参数
        :return:
        """

        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    listener_feedback = error_determine_func(*arguments, **keyword_args)
                except:
                    listener_feedback = None
                if listener_feedback:
                    raise AssertionError(listener_feedback)
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def _auto_click_permission_alert_wrapper(self, func):
        """
        权限自动点击装饰器（如果手机无法自动点击权限，可以在实现类里面重写该方法）
        :param func:
        :return:
        """
        this = self

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            possible_activity = [
                'com.android.packageinstaller.permission.ui.GrantPermissionsActivity',
                '.permission.ui.GrantPermissionsActivity'
            ]
            if this.driver.current_activity in possible_activity:
                need = True
                while need:
                    try:
                        alert = this.driver.switch_to.alert
                        alert.accept()
                        continue
                    except:
                        alert = this.get_elements(
                            [MobileBy.XPATH, '//android.widget.Button[@text="始终允许" or @text="允许"]'])
                        if alert:
                            alert[0].click()
                            continue
                    break
            return func(*args, **kwargs)

        return wrapper

    @TestLogger.log('等待条件成功，并监听异常条件')
    def wait_condition_and_listen_unexpected(
            self,
            condition,
            timeout=8,
            poll=0.2,
            auto_accept_permission_alert=True,
            unexpected=None,
            *args,
            **kwargs):
        """
        等待方法返回不是 False 的值
        :param condition: 等待的方法
        :param timeout: 超时时间
        :param poll: 等待频率
        :param auto_accept_permission_alert: 如果界面弹出系统权限对话框，是否点击允许，默认为True
        :param unexpected: 等待期间监听的错误，当该方法返回值不是 False 或空值，抛出超时异常
        :param args: unexpected 方法的参数
        :param kwargs: unexpected 方法的参数
        :return: 
        """""
        wait = WebDriverWait(self.driver, timeout, poll)
        if auto_accept_permission_alert:
            condition = self._auto_click_permission_alert_wrapper(condition)
        if callable(unexpected):
            condition = self._error_listener(unexpected, *args, **kwargs)(condition)
        return wait.until(condition)

    @TestLogger.log('获取OS平台名')
    def get_platform(self):
        try:
            platform_name = self.driver.desired_capabilities['platformName']
        except Exception as e:
            raise e
        return platform_name.lower()

    @TestLogger.log('获取设备型号')
    def get_device_model(self):
        """获取设备型号"""
        platform = self.get_platform()
        if platform == 'android':
            model = self.execute_shell_command('getprop', 'ro.product.model')
            return model.strip()
        elif platform == 'ios':
            return 'ios'
        else:
            return 'other'

    @TestLogger.log('获取元素')
    def get_element(self, locator):
        return self.driver.find_element(*locator)

    @TestLogger.log('获取元素列表')
    def get_elements(self, locator):
        return self.driver.find_elements(*locator)

    @TestLogger.log('获取元素文本(支持遍历子元素并返回文本数组)')
    def get_text(self, locator):
        """获取元素文本"""
        self.wait_until(
            condition=lambda d: self.get_elements(locator)
        )
        elements = self.get_elements(locator)
        if len(elements) > 0:
            return elements[0].text
        return None

    @TestLogger.log("获取控件属性")
    def get_element_attribute(self, locator, attr, wait_time=0):
        try:
            widget = self.wait_until(
                condition=lambda d: self.get_element(locator),
                timeout=wait_time
            )
            value = widget.get_attribute(attr)
            return value
        except TimeoutException:
            raise NoSuchElementException("找不到控件：{}".format(locator))

    @TestLogger.log('判断页面是否包含指定文本')
    def is_text_present(self, text):
        text_norm = normalize('NFD', text)
        source_norm = normalize('NFD', self.get_source())
        result = text_norm in source_norm
        return result

    @TestLogger.log('判断元素是否包含在页面DOM')
    def _is_element_present(self, locator):
        elements = self.get_elements(locator)
        return len(elements) > 0

    @TestLogger.log('判断元素是否可见')
    def _is_visible(self, locator):
        elements = self.get_elements(locator)
        if len(elements) > 0:
            return elements[0].is_displayed()
        return None

    @TestLogger.log('判断元素是否可点击')
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

    @TestLogger.log('判断元素文本与期望的模式是否匹配（支持正则）')
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

    @TestLogger.log('判断元素是否可用')
    def _is_enabled(self, locator):
        element = self.get_element(locator)
        return element.is_enabled()

    @TestLogger.log('获取页面DOM文档')
    def get_source(self):
        return self.driver.page_source

    @TestLogger.log('点击坐标')
    def tap(self, positions, duration=None):
        self.driver.tap(positions, duration)

    @TestLogger.log('点击元素（默认等待5秒，且等待期间自动允许弹出权限）')
    def click_element(self, locator, default_timeout=5, auto_accept_permission_alert=True):
        try:
            self.wait_until(
                condition=lambda d: self.get_element(locator),
                timeout=default_timeout,
                auto_accept_permission_alert=auto_accept_permission_alert
            ).click()
        except TimeoutException:
            raise NoSuchElementException('找不到元素 {}'.format(locator))

    @TestLogger.log('点击文本（支持完全匹配和模糊匹配）')
    def click_text(self, text, exact_match=False, default_timeout=5, auto_accept_permission_alert=True):
        if self.get_platform() == 'ios':
            if exact_match:
                _xpath = u'//*[@value="{}" or @label="{}"]'.format(text, text)
            else:
                _xpath = u'//*[contains(@label,"{}") or contains(@value, "{}")]'.format(text, text)
            self.get_element((MobileBy.XPATH, _xpath)).click()
        elif self.get_platform() == 'android':
            if exact_match:
                _xpath = u'//*[@{}="{}"]'.format('text', text)
            else:
                _xpath = u'//*[contains(@{},"{}")]'.format('text', text)
            self.click_element((MobileBy.XPATH, _xpath), default_timeout, auto_accept_permission_alert)

    @TestLogger.log('输入文本')
    def input_text(self, locator, text, default_timeout=5):
        try:
            element = self.wait_until(
                condition=lambda d: self.get_element(locator),
                timeout=default_timeout
            )
            element.send_keys(text)
        except TimeoutException:
            raise NoSuchElementException('找不到元素：{}'.format(locator))

    @TestLogger.log('勾选可选控件')
    def select_checkbox(self, locator):
        """勾选复选框"""
        if not self.is_selected(locator):
            self.click_element(locator)

    @TestLogger.log('去勾选可选控件')
    def unselect_checkbox(self, locator):
        """去勾选复选框"""
        if self.is_selected(locator):
            self.click_element(locator)

    @TestLogger.log('判断可选控件是否为已选中状态')
    def is_selected(self, locator):
        el = self.get_element(locator)
        result = el.get_attribute("checked")
        if result.lower() == "true":
            return True
        return False

    @TestLogger.log('断言：检查checkbox是否已选中')
    def checkbox_should_be_selected(self, locator):
        # element = self.get_element(locator)
        if not self.is_selected(locator):
            raise AssertionError("Checkbox '{}' should have been selected "
                                 "but was not.".format(locator))
        return True

    @TestLogger.log('断言：检查checkbox是否未选中')
    def checkbox_should_not_be_selected(self, locator):
        # element = self.get_element(locator)
        if self.is_selected(locator):
            raise AssertionError("Checkbox '{}' should not have been selected "
                                 "but was not.".format(locator))
        return True

    @TestLogger.log('点到点滑动')
    def swipe_point_to_point(self, from_position, to_position, duration=None):
        if self.is_android():
            self.driver.swipe(
                from_position[0],
                from_position[1],
                to_position[0],
                to_position[1],
                duration
            )
        else:
            self.driver.swipe(
                from_position[0],
                from_position[1],
                to_position[0] - from_position[0],
                to_position[1] - from_position[1],
                duration
            )

    @TestLogger.log('在控件上按指定的上下左右方向滑动')
    def swipe_by_direction(self, locator, direction, duration=None):
        """
        在元素内滑动
        :param locator: 定位器
        :param direction: 方向（left,right,up,down）
        :param duration: 持续时间ms
        :return:
        """
        if isinstance(locator, (list, tuple)):
            element = self.get_element(locator)
        elif isinstance(locator, WebElement):
            element = locator
        else:
            raise TypeError('Type of {} is not a list like or WebElement'.format(locator))
        rect = element.rect
        left, right = int(rect['x']) + 1, int(rect['x'] + rect['width']) - 1
        top, bottom = int(rect['y']) + 1, int(rect['y'] + rect['height']) - 1
        width = int(rect['width']) - 2
        height = int(rect['height']) - 2

        if self.get_platform() == 'android':
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

    @TestLogger.log('按百分比在屏幕上滑动')
    def swipe_by_percent_on_screen(self, start_x, start_y, end_x, end_y, duration=None):
        width = self.driver.get_window_size()["width"]
        height = self.driver.get_window_size()["height"]
        x_start = float(start_x) / 100 * width
        x_end = float(end_x) / 100 * width
        y_start = float(start_y) / 100 * height
        y_end = float(end_y) / 100 * height
        x_offset = x_end - x_start
        y_offset = y_end - y_start
        if self.get_platform() == 'android':
            self.driver.swipe(x_start, y_start, x_end, y_end, duration)
        else:
            self.driver.swipe(x_start, y_start, x_offset, y_offset, duration)

    @TestLogger.log('断言：检查页面是否包含文本')
    def assert_screen_contain_text(self, text):
        if not self.is_text_present(text):
            raise AssertionError("Page should have contained text '{}' "
                                 "but did not".format(text))

    @TestLogger.log('断言：检查页面是否不包含文本')
    def assert_screen_should_not_contain_text(self, text):
        if self.is_text_present(text):
            raise AssertionError("Page should not have contained text '{}'".format(text))

    @TestLogger.log('断言：检查页面是否包含元素')
    def assert_screen_should_contain_element(self, locator):
        if not self._is_element_present(locator):
            raise AssertionError("Page should have contained element '{}' "
                                 "but did not".format(locator))

    @TestLogger.log('断言：检查页面是否不包含元素')
    def assert_should_not_contain_element(self, locator):
        if self._is_element_present(locator):
            raise AssertionError("Page should not have contained element {}".format(locator))

    @TestLogger.log('断言：检查元素是否禁用')
    def assert_element_should_be_disabled(self, locator):
        if self._is_enabled(locator):
            raise AssertionError("Element '{}' should be disabled "
                                 "but did not".format(locator))

    @TestLogger.log('断言：检查元素是否可用')
    def assert_element_should_be_enabled(self, locator):
        if not self._is_enabled(locator):
            raise AssertionError("Element '{}' should be enabled "
                                 "but did not".format(locator))

    @TestLogger.log('断言：检查元素是否可见')
    def assert_element_should_be_visible(self, locator):
        if not self.get_element(locator).is_displayed():
            raise AssertionError("Element '{}' should be visible "
                                 "but did not".format(locator))

    @TestLogger.log('断言：检查元素包含指定文本')
    def assert_element_should_contain_text(self, locator, expected, message=''):
        actual = self.get_text(locator)
        if expected not in actual:
            if not message:
                message = "Element '{}' should have contained text '{}' but " \
                          "its text was '{}'.".format(locator, expected, actual)
            raise AssertionError(message)

    @TestLogger.log('断言：检查元素不包含指定文本')
    def assert_element_should_not_contain_text(self, locator, expected, message=''):
        actual = self.get_text(locator)
        if expected in actual:
            if not message:
                message = "Element {} should not contain text '{}' but " \
                          "it did.".format(locator, expected)
            raise AssertionError(message)

    @TestLogger.log('断言：检查元素文本等于期望值')
    def assert_element_text_should_be(self, locator, expected, message=''):
        element = self.get_element(locator)
        actual = element.text
        if expected != actual:
            if not message:
                message = "The text of element '{}' should have been '{}' but in fact it was '{}'." \
                    .format(locator, expected, actual)
            raise AssertionError(message)

    @TestLogger.log('断言：检查元素文本与模式匹配（支持正则表达式）')
    def assert_element_text_should_match(self, locator, pattern, full_match=True, regex=False):
        """断言元素内文本，支持正则表达式"""
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
            raise AssertionError(
                "Expect is" + " match regex pattern" if regex else "" + ": " + pattern + "\n"
                                                                   + "Actual is: " + actual + '\n')

    def run_app_in_background(self, seconds=5):
        """让 app 进入后台运行seconds 秒"""
        self.driver.background_app(seconds)

    @TestLogger.log('获取网络状态（不要用，不同机型返回结果不一样，不可控制）')
    def get_network_status(self):
        """获取网络链接状态"""
        return self.driver.network_connection

    @TestLogger.log('设置网络状态')
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
        retry = 3
        while True:
            try:
                if status == 0:
                    self.turn_off_airplane_mode()
                    self.turn_off_mobile_data()
                    self.turn_off_wifi()
                    return 0
                elif status == 1:
                    self.turn_on_airplane_mode()
                    return 1
                elif status == 2:
                    self.turn_off_airplane_mode()
                    self.turn_off_mobile_data()
                    self.turn_on_wifi()
                    return 2
                elif status == 4:
                    self.turn_off_airplane_mode()
                    self.turn_on_mobile_data()
                    self.turn_off_wifi()
                    return 4
                elif status == 6:
                    self.turn_off_airplane_mode()
                    self.turn_on_wifi()
                    self.turn_on_mobile_data()
                    return 6
                else:
                    raise ValueError(
                        """
        Value (Alias)      | Data | Wifi | Airplane Mode
        -------------------------------------------------
        0 (None)           | 0    | 0    | 0
        1 (Airplane Mode)  | 0    | 0    | 1
        2 (Wifi only)      | 0    | 1    | 0
        4 (Data only)      | 1    | 0    | 0
        6 (All network on) | 1    | 1    | 0
                        """
                    )
            except Exception as err:
                if isinstance(err, ValueError):
                    raise
                else:
                    # 如果发生异常，恢复网络状态为 6 (All network on) | 1    | 1    | 0
                    # 尝试3次
                    self._reset_network(3)
                    raise err

    @TestLogger.log('恢复网络')
    def _reset_network(self, try_time=3):
        if try_time < 1:
            try_time = 1
        while try_time:
            try:
                self.connect_mobile()
                self.turn_off_airplane_mode()
                self.turn_on_wifi()
                self.turn_on_mobile_data()
                return
            except:
                try_time -= 1

    @TestLogger.log('推送文件到手机内存')
    def push_file(self, file_path, to_path):
        """推送文件到手机内存"""
        with open(file_path, 'rb') as f:
            content = f.read()
            mda = hashlib.md5(content).hexdigest()
        b64 = str(base64.b64encode(content), 'UTF-8')
        self.driver.push_file(to_path, b64)
        if self.is_android():
            # 安卓使用shell命令验证MD5
            mdb = self.execute_shell_command('md5sum', '-b', '"{}"'.format(to_path)).strip()
            if mda == mdb:
                print('Local file: {};\nPush to:{};\nSuccess!'.format(file_path, to_path))
                return True
            else:
                print('推送的文件可能已经损坏：\nlocal file md5:{};\nremote file md5:{}.'.format(mda, mdb))
        else:
            # TODO IOS MD5验证待实现
            return True

    @TestLogger.log('推送文件夹到手机内存')
    def push_folder(self, folder_path, to_path, save_name=None, force_replace=False):
        """推送文件夹到手机内存"""
        folder_path = os.path.abspath(folder_path)
        base_name = os.path.basename(folder_path)
        if not save_name:
            save_name = base_name
        if not self._is_legal_file_name(save_name):
            raise ValueError(r'文件名不能包含/\:*?<>|特殊字符')
        if to_path[-1] == '/':
            target_abspath = to_path + save_name
        else:
            target_abspath = to_path + '/' + save_name
        if os.path.isfile(folder_path):
            self.execute_shell_command('mkdir', '-p', '"{}"'.format(os.path.dirname(target_abspath)))
            self.push_file(folder_path, target_abspath)
            return True
        elif os.path.isdir(folder_path):
            # 检查目录是否存在，不存在则创建目录
            to_path = to_path + '/' + save_name
            self.execute_shell_command('mkdir', '-p', '"{}"'.format(to_path))
            files = os.listdir(folder_path)
            for f in files:
                child_path = os.path.join(folder_path, f)
                self.push_folder(child_path, to_path, f, force_replace)
            return True
        else:
            raise ValueError('找不到路径："{}"'.format(folder_path))

    @staticmethod
    def _is_legal_file_name(name):
        if isinstance(name, str):
            special_characters = r'/\:*?<>|'
            chart_set = {i for i in name}
            illegal_set = {i for i in special_characters}
            if chart_set.intersection(illegal_set):
                return False
            else:
                return True
        else:
            raise ValueError('{} is not a string!'.format(name))

    def is_keyboard_shown(self):
        return self.driver.is_keyboard_shown()

    @TestLogger.log('隐藏键盘')
    def hide_keyboard(self, key_name=None, key=None, strategy=None):
        """隐藏键盘"""
        self.driver.hide_keyboard(key_name, key, strategy)

    @TestLogger.log('如果键盘弹出，就收回键盘')
    def hide_keyboard_if_display(self):
        if self.is_keyboard_shown():
            self.hide_keyboard()

    @TestLogger.log('发送短信')
    def send_sms(self, to, content, card_index=0):
        """
        发送短信
        :param to: 目标号码
        :param content: 短信内容
        :param card_index: 使用的需要，默认使用第一张卡
        :return:
        """
        if self.is_android():
            self.terminate_app('com.android.mms')
            self.execute_shell_command('am', 'start', '-a', 'android.intent.action.SENDTO', '-d', 'sms:', '-e',
                                       'sms_body', '"{}"'.format(content), '--ez', 'exit_on_sent', 'true')
            self.execute_shell_command('input', 'text', to)
            self.click_element([MobileBy.XPATH, '//*[@content-desc="发送"]'])
            if len(self.get_cards()) > 1:
                locator = [MobileBy.XPATH,
                           '//*[contains(@text,"中国移动") or contains(@text,"中国联通") or contains(@text,"中国电信")]']
                self.wait_until(
                    condition=lambda d: len(self.get_elements(locator)) > card_index
                )
                send_bys = self.get_elements(
                    locator)
                send_bys[card_index].click()
            return self.get_card(card_index)
        elif self.is_ios():
            # TODO IOS发短信功能待实现
            pass
        else:
            pass

    def set_clipboard_text(self, text, label=None):
        self.driver.set_clipboard_text(text, label)

    @TestLogger.log("粘贴")
    def paste(self):
        if self.is_android():
            self.execute_shell_command('input', 'keyevent', 279)
            return
        elif self.is_ios():
            # TODO
            raise NotImplementedError('IOS 点击HOME键未实现')
        else:
            raise NotImplementedError('该API不支持android/ios以外的系统')

    def list_iterator(self, scroll_view_locator, item_locator):
        """
        迭代列表内容
        :param scroll_view_locator: 列表容器的定位器
        :param item_locator: 列表项定位器
        :return:
        """
        if self.get_elements(scroll_view_locator):
            scroll_view = self.get_element(scroll_view_locator)
        else:
            return

        items = self.get_elements(item_locator)
        if not items:
            return
        for i in items:

            # 判断元素位置是否已经超过滚动视图的中点
            scroll_view_center = scroll_view.location.get('y') + scroll_view.size.get('height') // 2
            if i.location.get('y') > scroll_view_center:
                pre_y = i.location.get('y')

                # 稳定的滑动最少要在press后保持600ms才能移动
                minimum_hold_time = 600
                self.swipe_by_direction(i, 'up', minimum_hold_time)
                post_y = i.location.get('y')
                if pre_y == post_y:

                    # 坐标没变化就把剩下的抛出去然后结束循环
                    yield from items[items.index(i):]
                    return
                else:

                    # 坐标变化就更新找出的列表
                    restorer = items[:items.index(i)]
                    items.clear()
                    refreshed_items = self.get_elements(item_locator)
                    if not refreshed_items:
                        return
                    for refreshed_item in refreshed_items:
                        if refreshed_item.location.get('y') == post_y:
                            the_rests = refreshed_items[refreshed_items.index(refreshed_item):]
                            restorer.extend(the_rests)
                            break
                    items.extend(restorer)
            yield i
            refreshed_items = self.get_elements(item_locator)
            refreshed_items.reverse()
            for refreshed_item in refreshed_items:
                offset = -1 - refreshed_items.index(refreshed_item)
                if abs(offset) <= len(items):
                    items[offset] = refreshed_item

    @TestLogger.log('开启数据流量')
    def turn_on_mobile_data(self):
        """
        Android系统：
            默认使用adb命令 adb shell am start -a android.settings.DATA_ROAMING_SETTINGS 打开移动网络设置页，
            通过寻找第一个checkable="true"的控件当做数据开关进行开启、关闭操作
        IOS系统：
            未实现
        如果该方法对正在使用的机型不适用，应该在具体的mobile实现类中重写该方法
        :return:
        """
        if self.is_android():
            params = 'am start -a android.settings.DATA_ROAMING_SETTINGS'.split(' ')
            self.execute_shell_command(*params)
            switch_locator = [MobileBy.XPATH, '//*[@checkable="true"]']
            if self.get_element_attribute(switch_locator, 'checked', 2) == 'false':
                self.click_element(switch_locator, auto_accept_permission_alert=False)
            try:
                self.wait_until(
                    condition=lambda d: self.get_element_attribute(switch_locator, 'checked') == 'true',
                    auto_accept_permission_alert=False
                )
            except TimeoutException:
                print(self.get_element_attribute(switch_locator, 'checked'))
                raise RuntimeError('开关的checked属性没有置为"true"')
            self.back()
            return True
        elif self.is_ios():
            # TODO IOS系统上的数据流量开关操作未实现
            raise NotImplementedError('IOS 未实现该操作')
        else:
            raise NotImplementedError('该API不支持android/ios以外的系统')

    @TestLogger.log('关闭数据流量')
    def turn_off_mobile_data(self):
        """
        Android系统：
            默认使用adb命令 adb shell am start -a android.settings.DATA_ROAMING_SETTINGS 打开移动网络设置页，
            通过寻找第一个checkable="true"的控件当做数据开关进行开启、关闭操作
        IOS系统：
            未实现
        如果该方法对正在使用的机型不适用，应该在具体的mobile实现类中重写该方法
        :return:
        """
        if self.is_android():
            params = 'am start -a android.settings.DATA_ROAMING_SETTINGS'.split(' ')
            self.execute_shell_command(*params)
            switch_locator = [MobileBy.XPATH, '//*[@checkable="true"]']
            if self.get_element_attribute(switch_locator, 'checked', 2) == 'true':
                self.click_element(switch_locator, auto_accept_permission_alert=False)
            try:
                self.wait_until(
                    condition=lambda d: self.get_element_attribute(switch_locator, 'checked') == 'false',
                    auto_accept_permission_alert=False
                )
            except TimeoutException:
                print(self.get_element_attribute(switch_locator, 'checked'))
                raise RuntimeError('开关的checked属性没有置为"false"')
            self.back()
            return True
        elif self.is_ios():
            raise NotImplementedError('IOS 未实现该操作')
        else:
            raise NotImplementedError('该API不支持android/ios以外的系统')

    @TestLogger.log('开启WIFI')
    def turn_on_wifi(self):
        """
        Android系统：
            默认使用adb命令 adb shell am start -a android.settings.WIFI_SETTINGS 打开WIFI设置页，
            通过寻找第一个checkable="true"的控件当做数据开关进行开启、关闭操作
        IOS系统：
            未实现
        如果该方法对正在使用的机型不适用，应该在具体的mobile实现类中重写该方法
        :return:
        """
        if self.is_android():
            params = 'am start -a android.settings.WIFI_SETTINGS'.split(' ')
            self.execute_shell_command(*params)
            switch_locator = [MobileBy.XPATH, '//*[@checkable="true"]']
            if self.get_element_attribute(switch_locator, 'checked') == 'false':
                self.click_element(switch_locator, auto_accept_permission_alert=False)
            try:
                self.wait_until(
                    condition=lambda d: self.get_element_attribute(switch_locator, 'checked') == 'true',
                    auto_accept_permission_alert=False
                )
            except TimeoutException:
                print(self.get_element_attribute(switch_locator, 'checked'))
                raise RuntimeError('开关的checked属性没有置为"true"')
            # try:
            #     self.wait_until(
            #         condition=lambda d: self.is_text_present('已连接'),
            #         timeout=30,
            #         auto_accept_permission_alert=False
            #     )
            # except TimeoutException:
            #     raise RuntimeError('手机WIFI 已开启，但没有自动连接到 WIFI 热点')
            self.back()
            return True
        elif self.is_ios():
            # TODO IOS系统上的数据流量开关操作未实现
            raise NotImplementedError('IOS 未实现该操作')
        else:
            raise NotImplementedError('该API不支持android/ios以外的系统')

    @TestLogger.log('关闭WIFI')
    def turn_off_wifi(self):
        """
        Android系统：
            默认使用adb命令 adb shell am start -a android.settings.WIFI_SETTINGS 打开WIFI设置页，
            通过寻找第一个checkable="true"的控件当做数据开关进行开启、关闭操作
        IOS系统：
            未实现
        如果该方法对正在使用的机型不适用，应该在具体的mobile实现类中重写该方法
        :return:
        """
        if self.is_android():
            params = 'am start -a android.settings.WIFI_SETTINGS'.split(' ')
            self.execute_shell_command(*params)
            switch_locator = [MobileBy.XPATH, '//*[@checkable="true"]']
            if self.get_element_attribute(switch_locator, 'checked') == 'true':
                self.click_element(switch_locator, auto_accept_permission_alert=False)
            try:
                self.wait_until(
                    condition=lambda d: self.get_element_attribute(switch_locator, 'checked') == 'false',
                    auto_accept_permission_alert=False
                )
            except TimeoutException:
                print(self.get_element_attribute(switch_locator, 'checked'))
                raise RuntimeError('开关的checked属性没有置为"false"')
            self.back()
            return True
        elif self.is_ios():
            raise NotImplementedError('IOS 未实现该操作')
        else:
            raise NotImplementedError('该API不支持android/ios以外的系统')

    @TestLogger.log('开启飞行模式')
    def turn_on_airplane_mode(self):
        """
        Android系统：
            默认使用adb命令 adb shell am start -a android.settings.AIRPLANE_MODE_SETTINGS 打开WIFI设置页，
            通过寻找第一个checkable="true"的控件当做数据开关进行开启、关闭操作
        IOS系统：
            未实现
        如果该方法对正在使用的机型不适用，应该在具体的mobile实现类中重写该方法
        :return:
        """
        if self.is_android():
            params = 'am start -a android.settings.AIRPLANE_MODE_SETTINGS'.split(' ')
            self.execute_shell_command(*params)
            switch_locator = [MobileBy.XPATH, '//*[@checkable="true"]']
            if self.get_element_attribute(switch_locator, 'checked') == 'false':
                self.click_element(switch_locator, auto_accept_permission_alert=False)
            try:
                self.wait_until(
                    condition=lambda d: self.get_element_attribute(switch_locator, 'checked') == 'true',
                    auto_accept_permission_alert=False
                )
            except TimeoutException:
                print(self.get_element_attribute(switch_locator, 'checked'))
                raise RuntimeError('开关的checked属性没有置为"true"')
            self.back()
            return True
        elif self.is_ios():
            # TODO IOS系统上的数据流量开关操作未实现
            raise NotImplementedError('IOS 未实现该操作')
        else:
            raise NotImplementedError('该API不支持android/ios以外的系统')

    @TestLogger.log('关闭飞行模式')
    def turn_off_airplane_mode(self):
        """
        由于appium set_network_connection接口不靠谱，所有有关网络状态的设置需要在UI层面操作
        Android系统：
            默认使用adb命令 adb shell am start -a android.settings.AIRPLANE_MODE_SETTINGS 打开WIFI设置页，
            通过寻找第一个checkable="true"的控件当做数据开关进行开启、关闭操作
        IOS系统：
            未实现
        如果该方法对正在使用的机型不适用，应该在具体的mobile实现类中重写该方法
        :return:
        """
        if self.is_android():
            params = 'am start -a android.settings.AIRPLANE_MODE_SETTINGS'.split(' ')
            self.execute_shell_command(*params)
            switch_locator = [MobileBy.XPATH, '//*[@checkable="true"]']
            if self.get_element_attribute(switch_locator, 'checked') == 'true':
                self.click_element(switch_locator, auto_accept_permission_alert=False)
            try:
                self.wait_until(
                    condition=lambda d: self.get_element_attribute(switch_locator, 'checked') == 'false',
                    auto_accept_permission_alert=False
                )
            except TimeoutException:
                print(self.get_element_attribute(switch_locator, 'checked'))
                raise RuntimeError('开关的checked属性没有置为"false"')
            self.back()
            return True
        elif self.is_ios():
            raise NotImplementedError('IOS 未实现该操作')
        else:
            raise NotImplementedError('该API不支持android/ios以外的系统')

    @TestLogger.log('获取app版本号')
    def get_app_version_info(self, package=None):
        if self.is_android():
            if not package:
                package = self._desired_caps['appPackage']
            result = self.execute_shell_command('pm', 'dump', package, '|', 'grep', '"versionName"')
            try:
                name, value = result.strip().split('=')
                del name
                return value
            except:
                return '未知版本'
        else:
            # TODO IOS平台待实现
            raise NotImplementedError('该接口目前只支持Android')

    @TestLogger.log('获取手机型号')
    def get_mobile_model_info(self):
        if self.is_android():
            try:
                result = self.execute_shell_command('getprop', 'ro.product.name')
            except:
                result = "暂无信息"
            return result.strip()
        else:
            # TODO IOS平台待实现
            raise NotImplementedError('该接口目前只支持Android')

    @TestLogger.log('获取手机IP信息')
    def get_mobile_network_connection_info(self):
        if self.is_android():
            try:
                result = self.execute_shell_command('ifconfig')
            except:
                result = "暂无信息"
            return result
        else:
            # TODO IOS平台待实现
            raise NotImplementedError('该接口目前只支持Android')

    @TestLogger.log('应用是否已安装')
    def is_app_installed(self, bundle_id):
        """
        app是否已安装
        :param bundle_id: apk包名
        :return:
        """
        return self.driver.is_app_installed(bundle_id)

    @TestLogger.log("卸载APP")
    def remove_app(self, package, **options):
        return self.driver.remove_app(package, **options)

    @TestLogger.log('安装APP')
    def install_app(self,
                    app_path,
                    replace=True,
                    timeout=60000,
                    allowTestPackages=True,
                    useSdcard=False,
                    grantPermissions=True
                    ):
        """
        安装app 魅族
        常见报错原因：
            1、Failure [INSTALL_FAILED_VERSION_DOWNGRADE]（降版本覆盖安装异常）
        :param app_path: 要安装的应用程序的本地或远程路径
        :param replace:  如果应用已存在于被测试的设备上, 是否重新安装/升级包。默认为 True
        :param timeout: 等待安装完成的时间。默认情况下为60000毫秒。
        :param allowTestPackages: 是否允许安装在清单中标记为测试的包。默认为 True
        :param useSdcard: 是否使用 sd 卡安装应用程序. 默认为 False
        :param grantPermissions: 是否在安装完成后自动授权 android 6 +。默认为 True
        :return:
        """
        try:
            self.driver.install_app(
                app_path=app_path,
                replace=replace,
                timeout=timeout,
                allowTestPackages=allowTestPackages,
                useSdcard=useSdcard,
                grantPermissions=grantPermissions
            )
        except:
            tips = '''
Tips:
如果是魅族手机，请确保 手机管家->权限管理->USB安装权限->USB安装管理开关已关闭, 以防止安装权限弹窗阻塞脚本；
            '''
            print(tips)
            raise

    @TestLogger.log('获取元素指定坐标颜色')
    def get_coordinate_color_of_element(self, element, x, y, by_percent=False, mode='RGBA') -> tuple:
        """
        以元素左上角为坐标原点, 获取元素相对坐标颜色
        :param element: 定位器、元素
        :param x: x 轴坐标/百分比
        :param y: y 轴坐标/百分比
        :param by_percent: 是否切换成百分比模式定位
        :param mode: 颜色模式（RGBA、RGB、CMYK..)
        :return:
        :rtype: tuple
        """
        if isinstance(element, WebElement):
            el = element
        else:
            el = self.get_element(element)
        import io
        with io.BytesIO(el.screenshot_as_png) as fp:
            from library.core.utils import image_util
            color = image_util.get_pixel_point_color(fp, x, y, by_percent, mode)
            return color

    @TestLogger.log('判断是否在通话界面')
    def is_phone_in_calling_state(self):
        return self.current_activity == '.InCallActivity'

    @TestLogger.log('接听电话')
    def pick_up_the_call(self):
        """接听电话"""
        command = 'input keyevent KEYCODE_CALL'
        if self.is_phone_in_calling_state():
            self.execute_shell_command(command)

    @TestLogger.log('挂断电话')
    def hang_up_the_call(self):
        """挂断电话"""
        command = 'input keyevent KEYCODE_ENDCALL'
        if self.is_phone_in_calling_state():
            return self.execute_shell_command(command)

    @TestLogger.log('点击元素的外面')
    def click_out_side_of_element(self, locator, duration=None, default_timeout=3, auto_accept_permission_alert=True):
        try:
            if isinstance(locator, (tuple, list)):
                box = self.wait_until(
                    condition=lambda d: self.get_element(locator),
                    timeout=default_timeout,
                    auto_accept_permission_alert=auto_accept_permission_alert
                )
            else:
                box = locator
        except TimeoutException:
            raise NoSuchElementException('找不到元素：{}'.format(locator))

        viewport_rect = self.driver.capabilities.get('viewportRect')
        horizontal_center = (viewport_rect.get('left') + viewport_rect.get('width')) // 2
        vertical_center = (viewport_rect.get('top') + viewport_rect.get('height')) // 2

        top_margin = abs(viewport_rect.get('top') - box.location.get('y'))
        left_margin = abs(viewport_rect.get('left') - box.location.get('y'))
        right_margin = abs(viewport_rect.get('left') + viewport_rect.get('width') - box.location.get('y'))
        bottom_margin = abs(viewport_rect.get('top') + viewport_rect.get('height') - box.location.get('y'))
        if top_margin:
            position = (horizontal_center, viewport_rect.get('top') + top_margin // 2)
        elif left_margin:
            position = (viewport_rect.get('left') + left_margin // 2, vertical_center)
        elif right_margin:
            position = (viewport_rect.get('left') + viewport_rect.get('width') - top_margin // 2, vertical_center)
        elif bottom_margin:
            position = (horizontal_center, viewport_rect.get('top') + viewport_rect.get('height') - bottom_margin // 2)
        else:
            print('元素外面没有空白位置')
            return
        print('tap position: {}'.format(position))
        self.tap([position], duration)

    def __str__(self):
        device_info = {
            # "name": self.alis,
            "手机型号": self.model_info["ReadableName"]
        }
        return json.dumps(device_info, ensure_ascii=False)
