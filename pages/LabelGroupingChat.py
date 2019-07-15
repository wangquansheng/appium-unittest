from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from library.core.TestLogger import TestLogger
from pages.components.BaseChat import BaseChatPage


class LabelGroupingChatPage(BaseChatPage):
    """标签分组会话页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.MessageDetailActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/pop_10g_window_drop_view': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/pop_10g_window_drop_view'),
                  'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
                  'com.chinasofti.rcs:id/back': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/back_arrow'),
                  'com.chinasofti.rcs:id/chat_mode_content': (MobileBy.ID, 'com.chinasofti.rcs:id/chat_mode_content'),
                  'lab2': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
                  '多方通话': (MobileBy.ID, 'com.chinasofti.rcs:id/action_multicall'),
                  'com.chinasofti.rcs:id/action_setting': (MobileBy.ID, 'com.chinasofti.rcs:id/action_setting'),
                  'com.chinasofti.rcs:id/view_line': (MobileBy.ID, 'com.chinasofti.rcs:id/view_line'),
                  'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
                  'com.chinasofti.rcs:id/message_editor_layout': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/message_editor_layout'),
                  'com.chinasofti.rcs:id/rv_message_chat': (MobileBy.ID, 'com.chinasofti.rcs:id/rv_message_chat'),
                  '刚刚': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_time'),
                  'com.chinasofti.rcs:id/ll': (MobileBy.ID, 'com.chinasofti.rcs:id/ll'),
                  '你好': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_message'),
                  'com.chinasofti.rcs:id/svd_head': (MobileBy.ID, 'com.chinasofti.rcs:id/svd_head'),
                  'com.chinasofti.rcs:id/input_and_menu': (MobileBy.ID, 'com.chinasofti.rcs:id/input_and_menu'),
                  'com.chinasofti.rcs:id/ll_text_input': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_text_input'),
                  'com.chinasofti.rcs:id/layout_for_message': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_for_message'),
                  'com.chinasofti.rcs:id/ll_rich_panel': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_rich_panel'),
                  'com.chinasofti.rcs:id/ib_pic': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_pic'),
                  'com.chinasofti.rcs:id/ib_take_photo': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_take_photo'),
                  'com.chinasofti.rcs:id/ib_profile': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_profile'),
                  'com.chinasofti.rcs:id/ib_gif': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_gif'),
                  'com.chinasofti.rcs:id/ib_more': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'),
                  'com.chinasofti.rcs:id/base_input_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/base_input_layout'),
                  'com.chinasofti.rcs:id/input_divider_inside': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/input_divider_inside'),
                  'com.chinasofti.rcs:id/input_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/input_layout'),
                  'com.chinasofti.rcs:id/fl_edit_panel': (MobileBy.ID, 'com.chinasofti.rcs:id/fl_edit_panel'),
                  '说点什么...': (MobileBy.ID, 'com.chinasofti.rcs:id/et_message'),
                  'com.chinasofti.rcs:id/ib_expression': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_expression'),
                  'com.chinasofti.rcs:id/ib_audio': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_audio'),
                  "文件名": (MobileBy.ID, 'com.chinasofti.rcs:id/textview_file_name'),
                  # 消息长按弹窗
                  '收藏': (MobileBy.XPATH, "//*[contains(@text, '收藏')]"),
                  '转发': (MobileBy.XPATH, "//*[contains(@text, '转发')]"),
                  '撤回': (MobileBy.XPATH, "//*[contains(@text, '撤回')]"),
                  '删除': (MobileBy.XPATH, "//*[contains(@text, '删除')]"),
                  '复制': (MobileBy.XPATH, "//*[contains(@text, '复制')]"),
                  '多选': (MobileBy.XPATH, "//*[contains(@text, '多选')]"),
                  '编辑': (MobileBy.XPATH, "//*[contains(@text, '编辑')]"),
                  '照片': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_pic'),
                  '下拉菜单箭头': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/drop_down_image"]'),
                  '下拉菜单选项': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/albumTitle"]'),
                  '列表': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/recyclerView_gallery"]'),
                  '列表项': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/recyclerView_gallery"]/*['
                                          '@resource-id="com.chinasofti.rcs:id/rl_img"]'),
                  '选择': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iv_select"]'),
                  '原图': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/cb_original_photo"]'),
                  '预览': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_preview"]'),
                  '发送失败标识': (MobileBy.ID, 'com.chinasofti.rcs:id/imageview_msg_send_failed'),
                  '保存图片': (MobileBy.XPATH, "//*[contains(@text, '保存图片')]"),
                  '发送': (MobileBy.ID, "com.chinasofti.rcs:id/button_send"),
                  '消息根节点': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/rv_message_chat"]/*'),
                  '超过20M图片': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_loading'),
                  }

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在群聊天页"""
        el = self.get_elements(self.__locators['多方通话'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log()
    def wait_for_page_load(self, timeout=20, auto_accept_alerts=True):
        """等待标签分组会话页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["多方通话"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def click_back(self):
        """点击返回按钮"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def get_label_name(self):
        """获取标题名称"""
        el = self.get_element(self.__locators["lab2"])
        return el.text

    @TestLogger.log('文件是否存在')
    def is_element_present_file(self):
        return self._is_element_present(self.__locators['文件名'])

    @TestLogger.log()
    def press_file(self):
        """长按文件"""
        el = self.get_element(self.__class__.__locators['文件名'])
        self.press(el)

    @TestLogger.log()
    def press_last_file(self):
        """长按最后一个文件"""
        el = self.get_elements(self.__class__.__locators['文件名'])[-1]
        self.press(el)

    @TestLogger.log("删除当前分组发送的文件")
    def delete_group_all_file(self):
        msg_file = self.get_elements(('id', 'com.chinasofti.rcs:id/ll_msg'))
        if msg_file:
            for file in msg_file:
                self.press(file)
                self.click_element(self.__class__.__locators['删除'])
        else:
            raise AssertionError('当前窗口没有可以删除的消息')

    @TestLogger.log("撤回当前分组发送的文件")
    def recall_group_all_file(self):
        msg_file = self.get_elements(('id', 'com.chinasofti.rcs:id/ll_msg'))
        if msg_file:
            for file in msg_file:
                self.press(file)
                self.click_element(self.__class__.__locators['撤回'])
        else:
            raise AssertionError('当前窗口没有可以撤回的消息')

    @TestLogger.log()
    def get_file_name(self):
        """获取文件名称"""
        el = self.get_element(self.__locators["文件名"])
        return el.text

    @TestLogger.log()
    def get_one_file_name(self,type):
        """获取文件名称"""
        el = self.get_element(self.__locators["文件名"],type)
        return el.text

    @TestLogger.log()
    def click_picture(self):
        """点击照片"""
        self.click_element(self.__class__.__locators["照片"])

    @TestLogger.log('切换到指定文件夹')
    def switch_to_given_folder(self, path):
        import re
        if not self.get_elements(self.__locators['下拉菜单选项']):
            self.click_element(self.__locators['下拉菜单箭头'])
        menu_list = ['xpath', '//*[@resource-id="com.chinasofti.rcs:id/list_select"]']
        self.swipe_by_direction(menu_list, 'down', 600)
        menu_item = ['xpath', '//*[@resource-id="com.chinasofti.rcs:id/list_select"]/*']
        for i in self.mobile.list_iterator(menu_list, menu_item):
            del i
            menus = self.get_elements(self.__locators['下拉菜单选项'])
            for menu in menus:
                menu_text = menu.text
                assert re.match(r'.+\(\d+\)', menu_text), r'Assert menu text match Regex:."+\(\d+\)"'
                display_name, total = re.findall(r'(.+)\((\d+)\)', menu_text)[0]
                if len(display_name) > 3:
                    result = re.findall(r'(.+)([.]{3})$', display_name)
                    if result:
                        if path.find(result[0][0]) == 0:
                            menu.click()
                            return result[0][0], int(total)
                    else:
                        if path.find(display_name) == 0:
                            menu.click()
                            return display_name, int(total)
                else:
                    if display_name == path:
                        menu.click()
                        return path, int(total)
        raise NoSuchElementException('下拉菜单没有找到名称为"{}"的目录'.format(path))

    @TestLogger.log('选择指定序号的图片（视频）')
    def select_items_by_given_orders(self, *orders):
        orders = sorted(list(set(orders)))
        offset = 1
        for i in self.mobile.list_iterator(self.__locators['列表'], self.__locators['列表项']):
            if offset in orders:
                if not self.is_list_item_selected(i):
                    el = i.find_element(*self.__locators['选择'])
                    el.click()
                orders.remove(offset)
            offset += 1
            if not orders:
                break

    @TestLogger.log('获取列表项已选状态')
    def is_list_item_selected(self, item):
        if isinstance(item, (list, tuple)):
            item = self.get_element(item)
        elif isinstance(item, WebElement):
            pass
        else:
            raise ValueError('参数类型错误')

        selector = item.find_element(*self.__locators['选择'])
        color = self.get_coordinate_color_of_element(selector, 5, 50, True)
        white = (255, 255, 255, 255)
        blue = (21, 124, 248, 255)
        if color == white:
            # 未选择状态为不透明白色
            return False
        elif color == blue:
            # 已选状态为不透明蓝色
            return True
        else:
            raise RuntimeError('RGBA颜色{}无法识别勾选状态'.format(color))

    @TestLogger.log('点击预览')
    def click_preview(self):
        """点击预览"""
        self.click_element(self.__locators['预览'])

    @TestLogger.log()
    def is_send_sucess(self):
        """当前页面是否有发送失败标识"""
        el = self.get_elements(self.__locators['发送失败标识'])
        if len(el) > 0:
            return False
        return True

    @TestLogger.log()
    def click_msg_image(self, number):
        """点击图片消息"""
        els = self.get_elements(self.__class__.__locators["消息图片"])
        els[number].click()

    @TestLogger.log()
    def is_exist_picture_edit_page(self):
        """长按消息"""
        for option in ["转发", "编辑", "保存图片"]:
            el = self.get_elements(self.__locators[option])
            if len(el) == 0:
                return False
        return True

    @TestLogger.log()
    def click_edit(self):
        """点击编辑"""
        self.click_element(self.__class__.__locators["编辑"])

    @TestLogger.log()
    def click_original_photo(self):
        """点击原图"""
        self.click_element(self.__class__.__locators["原图"])

    @TestLogger.log('等待消息在指定时间内状态变为“加载中”、“发送失败”、“发送成功”中的一种')
    def wait_for_msg_send_status_become_to(self, expected, max_wait_time=3, most_recent_index=1):
        self.wait_until(
            condition=lambda d: self.get_msg_status(msg=self.__locators['消息根节点'],
                                                    most_recent_index=most_recent_index) == expected,
            timeout=max_wait_time
        )

    @TestLogger.log('获取消息发送状态')
    def get_msg_status(self, msg, most_recent_index=1):
        """
        获取消息的发送状态，如：
            1、加载中
            2、已发送
            3、发送失败
        如果传入的是定位器，默认寻找最新一条消息，没有则抛出 NoSuchElementException 异常
        :param msg: 消息（必须传入消息根节点元素或者元素的定位器）
        :param most_recent_index: 消息在列表中的序号，从消息列表底部往上数，从1开始计数
        :return:
        """
        if not isinstance(msg, WebElement):
            msgs = self.get_elements(msg)
            if msgs:
                msg = msgs[-most_recent_index]
            else:
                raise NoSuchElementException('找不到元素：{}'.format(msg))
        # 找加载中
        if msg.find_elements('xpath', '//*[@resource-id="com.chinasofti.rcs:id/progress_send_small"]'):
            return '加载中'
        elif msg.find_elements('xpath', '//*[@resource-id="com.chinasofti.rcs:id/imageview_msg_send_failed"]'):
            return '发送失败'
        else:
            return '发送成功'

    @TestLogger.log()
    def press_picture(self):
        """长按消息"""
        els = self.get_elements(self.__locators['超过20M图片'])
        self.press(els[-1])

    @TestLogger.log()
    def is_exist_edit_page(self):
        """长按消息"""
        for option in ["收藏", "转发", "多选", "编辑", "删除"]:
            el = self.get_elements(self.__locators[option])
            if len(el) == 0:
                return False
        return True