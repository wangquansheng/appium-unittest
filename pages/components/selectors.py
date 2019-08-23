import time
from appium.webdriver import WebElement
from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import NoSuchElementException

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ContactsSelector(BasePage):
    """
    联系人选择器：
        标签分组-添加联系人
    """
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.ContactsSelectActivity'

    __locators = {
        'com.chinasofti.rcs:id/pop_10g_window_drop_view': (
            MobileBy.ID, 'com.chinasofti.rcs:id/pop_10g_window_drop_view'),
        'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
        '选择联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
        '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'),
        '搜索或输入手机号': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'),
        'com.chinasofti.rcs:id/contact_selection_list_view': (
            MobileBy.ID, 'com.chinasofti.rcs:id/contact_selection_list_view'),
        '联系人列表': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_list" or android.support.v7.widget.RecyclerView]'),
        '联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_list_item'),
        '选择和通讯录联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/local_contacts'),
        'com.chinasofti.rcs:id/arrow_right': (MobileBy.ID, 'com.chinasofti.rcs:id/arrow_right'),
        'com.chinasofti.rcs:id/asp_selecttion_contact_content': (
            MobileBy.ID, 'com.chinasofti.rcs:id/asp_selecttion_contact_content'),
        'G': (MobileBy.ID, ''),
        'com.chinasofti.rcs:id/select_icon': (MobileBy.ID, 'com.chinasofti.rcs:id/select_icon'),
        '联系人名称': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '联系人号码': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_number'),
        'H': (MobileBy.ID, ''),
        '字母导航栏': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_index_bar_container')
    }

    @TestLogger.log('搜索联系人')
    def search(self, name):
        self.mobile.input_text(self.__locators['搜索或输入手机号'], name)

    @TestLogger.log('点击联系人')
    def click_local_contacts(self, *name_list):
        name_list = list(name_list)

        self.wait_until(
            condition=lambda d: self._is_element_present(self.__locators['搜索或输入手机号'])
        )
        for cont in self.mobile.list_iterator(self.__locators['联系人列表'], self.__locators['联系人']):
            name = cont.find_element(*self.__locators['联系人名称']).text
            if name in name_list:
                cont.click()
                name_list.remove(name)
            if not name_list:
                break
        if name_list:
            print('没有找到以下联系人：{}'.format(name_list))
            return False
        return True

    @TestLogger.log('选择本地联系人并点击确定')
    def select_local_contacts(self, *name_list):
        name_list = list(name_list)

        self.wait_until(
            condition=lambda d: self._is_element_present(self.__locators['搜索或输入手机号'])
        )
        for cont in self.mobile.list_iterator(self.__locators['联系人列表'], self.__locators['联系人']):
            name = cont.find_element(*self.__locators['联系人名称']).text
            if name in name_list:
                cont.click()
                name_list.remove(name)
            if not name_list:
                break

        self.click_ok_button()
        if name_list:
            print('没有找到以下联系人：{}'.format(name_list))
            return False
        return True

    @TestLogger.log('选择本地联系人并点击确定')
    def select_local_contacts_search(self, *name_list):
        name_list = list(name_list)

        self.wait_until(
            condition=lambda d: self._is_element_present(self.__locators['搜索或输入手机号'])
        )
        for name in name_list:
            self.input_text(self.__locators['搜索或输入手机号'], name)
            time.sleep(0.5)
            locator = (MobileBy.XPATH, "//android.support.v7.widget.RecyclerView[@resource-id='com.chinasofti.rcs:id"
                                       "/search_rv']/android.view.ViewGroup[1]")
            if self._is_element_present(locator):
                self.get_element(locator).click()
            else:
                raise AssertionError('无此联系人')



        self.click_ok_button()
        if name_list:
            print('没有找到以下联系人：{}'.format(name_list))
            return False
        return True

    @TestLogger.log('点击确定')
    def click_ok_button(self):
        self.click_element(self.__locators['确定'])

    @TestLogger.log('检查点：输入框文案="搜索或输入手机号"')
    def assert_contacts_selector_search_box_place_holder_is_right(self):
        self.mobile.assert_element_text_should_be(self.__locators['搜索或输入手机号'], '搜索或输入手机号')

    @TestLogger.log('检查点：页面标题="选择联系人"')
    def assert_contacts_selector_page_title_is_right(self):
        self.mobile.assert_element_text_should_be(self.__locators['选择联系人'], '添加群成员')

    @TestLogger.log('检查点：右上角显示确定按钮')
    def assert_contacts_selector_page_display_ok_button(self):
        self.mobile.assert_screen_should_contain_element(self.__locators['确定'])

    @TestLogger.log('检查点：页面包含文本')
    def assert_contacts_selector_page_contains_text(self, text):
        self.mobile.assert_screen_contain_text(text)

    @TestLogger.log('检查点：右边显示字母导航')
    def assert_contacts_selector_page_contains_alphabet_nav(self):
        self.mobile.assert_screen_should_contain_element(self.__locators['字母导航栏'])

    @TestLogger.log('等待选择联系人页面加载')
    def wait_for_contacts_selector_page_load(self, default_wait_time=5):
        self.wait_until(
            condition=lambda d: self._is_element_present(self.__locators['搜索或输入手机号']),
            timeout=default_wait_time
        )


class PictureSelector(BasePage):
    """
    照片：
        标签分组-添加联系人
    """
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.GalleryActivity'

    __locators = {
        'Title': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/drop_down_image"]'),
        '下拉菜单箭头': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/drop_down_image"]'),
        '下拉菜单选项': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/albumTitle"]'),

        '列表': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/recyclerView_gallery"]'),

        '列表项': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/recyclerView_gallery"]/*['
                                '@resource-id="com.chinasofti.rcs:id/rl_img"]'),
        '选择': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iv_select"]'),
        '缩略图': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iv_gallery"]'),
        '视频图标': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/imageview_video_start"]'),
        '视频时长': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_video_time"]'),

        '预览': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_preview"]'),
        '原图': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/cb_original_photo"]'),
        '发送': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/button_send"]'),
    }

    @TestLogger.log('点击预览')
    def click_preview(self):
        """点击预览"""
        self.click_element(self.__locators['预览'])

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

    @TestLogger.log('选择指定序号的图片（视频）')
    def unselect_items_by_given_orders(self, *orders):
        orders = sorted(list(set(orders)))
        offset = 1
        for i in self.mobile.list_iterator(self.__locators['列表'], self.__locators['列表项']):
            if offset in orders:
                if self.is_list_item_selected(i):
                    el = i.find_element(*self.__locators['选择'])
                    el.click()
                orders.remove(offset)
            offset += 1
            if not orders:
                break

    @TestLogger.log('获取列表数据的类型')
    def get_list_item_type(self, item):
        if isinstance(item, (list, tuple)):
            item = self.get_element(item)
        elif isinstance(item, WebElement):
            pass
        else:
            raise ValueError('参数类型错误')
        if item.find_elements(*self.__locators['视频图标']):
            object_type = 'video'
        else:
            object_type = 'image'
        return object_type

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

    @TestLogger.log('点击发送')
    def click_send_of_img_selector(self):
        self.click_element(self.__locators['发送'])

    @TestLogger.log('选择并发送')
    def select_and_send_in_img_selector(self, mapper):
        """
        选择文件进行发送
            mapper格式：
                {
                    # 文件夹名  # 文件位置序号
                    '文件夹1': (1, 2, 3, 4, 5)
                    '文件夹2': (2, 3, 4, 5, 8)
                }
        :param mapper: 文件位置字典
        :return:
        """
        for folder_name, orders in mapper.items():
            self.switch_to_given_folder(folder_name)
            self.select_items_by_given_orders(*orders)
        self.click_send_of_img_selector()

    @TestLogger.log()
    def click_send(self, times=3):
        """点击发送"""
        self.click_element(self.__class__.__locators["发送"])
        # 发送图片需要时间
        time.sleep(times)

    @TestLogger.log()
    def click_original_photo(self):
        """点击原图"""
        self.click_element(self.__class__.__locators["原图"])
