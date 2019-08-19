from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import NoSuchElementException
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
#import preconditions
import time


class GroupListPage(BasePage):
    """群组列表"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.GroupChatListActivity2'

    __locators = {

        '移除成员_标题':(MobileBy.ID,'com.chinasofti.rcs:id/title'),
        '搜索标签分组成员':(MobileBy.ID,'com.chinasofti.rcs:id/contact_search_bar'),
        '刪除_标签名':(MobileBy.ID,'com.chinasofti.rcs:id/ib_label_del'),
        '星标图标': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_star'),
        '星标': (MobileBy.ID, 'com.chinasofti.rcs:id/star'),
        "电话号码":(MobileBy.ID,'com.chinasofti.rcs:id/tv_phone'),
        "语音通话": (MobileBy.ID, 'com.chinasofti.rcs:id/tv_voice_call'),
        "视频通话": (MobileBy.ID, 'com.chinasofti.rcs:id/tv_video_call'),
        "分享名片": (MobileBy.ID, 'com.chinasofti.rcs:id/btn_share_card'),
        "邀请使用": (MobileBy.ID, 'com.chinasofti.rcs:id/tv_invitation_to_use'),
        "发送_邀请":(MobileBy.ID,'com.android.mms:id/right_btn'),
        "信息邀请":(MobileBy.ID,'com.android.mms:id/msg_content'),
        "修改标签名称":(MobileBy.ID,"com.chinasofti.rcs:id/label_toolbar_title"),
        "标签名称框":(MobileBy.ID,'com.chinasofti.rcs:id/edit_label_group_name'),
        "确定3":(MobileBy.ID,"com.chinasofti.rcs:id/tv_label_done"),
        "移除成员_标题":(MobileBy.ID,'com.chinasofti.rcs:id/title'),

        "多方电话提示框": (MobileBy.XPATH, "//*[@text='多方电话']"),
        "飞信电话": (MobileBy.XPATH, "//*[@text='飞信电话']"),
        "多方视频": (MobileBy.XPATH, "//*[@text='多方视频']"),
        "多方视频图标": (MobileBy.XPATH, "//*[@text='多方视频']"),
        '多方通话_图标':(MobileBy.ID,'com.chinasofti.rcs:id/action_multicall'),
        '分组联系人':(MobileBy.ID,'com.chinasofti.rcs:id/action_setting'),
        '分组联系人_标题':(MobileBy.ID,'com.chinasofti.rcs:id/title'),
        '富媒体面板': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_rich_panel'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),


        '群聊': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '新建群组': (MobileBy.ID, 'com.chinasofti.rcs:id/menu_add_btn'),
        '搜索群组': (MobileBy.XPATH, '//*[contains(@resource-id,"search")]'),
        'com.chinasofti.rcs:id/fragment_container': (MobileBy.ID, 'com.chinasofti.rcs:id/fragment_container'),
        '群列表': (MobileBy.ID, 'com.chinasofti.rcs:id/recyclerView'),
        '列表项': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_group_list_item'),
        '列表项首字母': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_index'),
        '群名': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '滚动条字符': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_index_bar_container"]/*'),
        '标题新建分组': (MobileBy.ID, 'com.chinasofti.rcs:id/label_toolbar_title'),
        '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'),
        '为你的分组创建一个名称': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_sub_title'),
        '请输入标签分组名称': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_group_name'),
        '通讯录': (MobileBy.ID, 'com.chinasofti.rcs:id/tvContact'),
        '标签分组': (MobileBy.ID, 'com.chinasofti.rcs:id/second_item'),
        '新建分组':(MobileBy.XPATH,'//*[@text="新建分组"]'),
        '知道了':(MobileBy.ID,'com.chinasofti.rcs:id/btn_cancel'),
        '设置':(MobileBy.ID,'com.chinasofti.rcs:id/iv_label_setting'),
        '删除标签':(MobileBy.XPATH,'//*[@text="删除标签"]'),
        '移除成员':(MobileBy.XPATH,'//*[@text="移除成员"]'),
        '标签名称':(MobileBy.XPATH,'//*[@text="标签名称"]'),
        '刪除按钮':(MobileBy.ID,'com.chinasofti.rcs:id/btn_ok'),
        'back_contact':(MobileBy.ID,'com.chinasofti.rcs:id/back'),
        '联系人列表': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_list_item'),

        'back_gouppage':(MobileBy.ID,'com.chinasofti.rcs:id/rl_label_left_back'),
        "back_contact2":(MobileBy.ID,'com.chinasofti.rcs:id/label_group_left_back'),
        'back_newpage':(MobileBy.ID,'com.chinasofti.rcs:id/iv_back'),
        'back_settings': (MobileBy.ID, 'com.chinasofti.rcs:id/label_setting_left_back'),


        'aaa':(MobileBy.XPATH,'//*[@text="aaa"]'),
        'bbb': (MobileBy.XPATH, '//*[@text="bbb"]'),
        '添加成员':(MobileBy.XPATH,'//*[@text="添加成员"]'),
        '添加成员菜单': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_first_colum'),
        '群发信息': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_second_colum'),
        '多方电话': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_third_colum'),
        '多方视频': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_fourth_colum'),
        '大佬1': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_name'),
        '大佬3':(MobileBy.XPATH,'//*[@text="大佬3"]'),
        '大佬2': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
        '搜索或输入手机号':(MobileBy.XPATH,"//*[@text='搜索或输入号码']"),
        '搜索框-搜索结果':(MobileBy.ID, 'com.chinasofti.rcs:id/contact_list_item'),
        '选择联系人':(MobileBy.ID,"com.chinasofti.rcs:id/title"),
        '清空搜索框': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_delect'),
        '已选择的联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/hor_contact_selection'),
        '分组联系人-姓名': (MobileBy.ID, 'com.chinasofti.rcs:id/group_member_name'),
        '分组联系人-电话号码': (MobileBy.ID, 'com.chinasofti.rcs:id/group_member_number'),
        '移除-已选择联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/image_text'),

        '选择和通讯录联系人':(MobileBy.ID,'com.chinasofti.rcs:id/text_hint'),
        '删除-搜索':(MobileBy.ID,'com.chinasofti.rcs:id/iv_delect'),
        '联系人头像':(MobileBy.ID,'com.chinasofti.rcs:id/contact_icon'),
        '允许':(MobileBy.XPATH,'//*[@text="允许"]'),
        '和飞信测试':(MobileBy.ID,'com.chinasofti.rcs:id/tv_title_department'),
        '和通讯本人': (MobileBy.ID, '	com.chinasofti.rcs:id/tv_name_personal_contactlist'),
        '中软国际科技服务有限公司':(MobileBy.XPATH,'//*[@text="中软国际科技服务有限公司"]'),
        '广州': (MobileBy.XPATH, '//*[@text="	广州"]'),
        '和通讯联系人': (MobileBy.ID,'com.chinasofti.rcs:id/img_icon_contactlist'),
        '我已阅读': (MobileBy.ID,'com.chinasofti.rcs:id/btn_check'),
        '已阅读_确定': (MobileBy.ID,'com.chinasofti.rcs:id/dialog_btn_ok'),
        '群发_输入框': (MobileBy.ID,'com.chinasofti.rcs:id/et_message'),
        '发送': (MobileBy.ID,'com.chinasofti.rcs:id/ib_send'),
        '标签设置': (MobileBy.ID, 'com.chinasofti.rcs:id/label_setting_toolbar_title'),
        '表情按钮': (MobileBy.ID,"com.chinasofti.rcs:id/ib_expression"),
        '表情_微笑': (MobileBy.XPATH,'//*[@text="[微笑1]"]'),
        '已转短信送达': (MobileBy.XPATH,'//*[@text="已转短信送达"]'),
        '添加图片': (MobileBy.ID,'com.chinasofti.rcs:id/ib_pic'),
        '选择图片': (MobileBy.ID,'com.chinasofti.rcs:id/iv_select'),
        '图片发送': (MobileBy.ID,'com.chinasofti.rcs:id/button_send'),
        '发送失败': (MobileBy.ID,'com.chinasofti.rcs:id/imageview_msg_send_failed'),
        '成员头像': (MobileBy.ID,'com.chinasofti.rcs:id/avator'),
        "确定_可用": (MobileBy.XPATH,'//*[@text="确定"]'),
        "版本更新": (MobileBy.ID,'com.chinasofti.rcs:id/dialog_title'),
        "以后再说": (MobileBy.ID,"com.chinasofti.rcs:id/btn_cancel"),
        '立即更新': (MobileBy.ID,"com.chinasofti.rcs:id/btn_ok"),
        '搜索': (MobileBy.ID,"com.chinasofti.rcs:id/edit_query"),
        '索引字母容器': (MobileBy.ID, 'com.chinasofti.rcs:id/contact_index_bar_container'),

    }


    @TestLogger.log("修改标签名称")
    def update_label_name(self,name='bbb'):
        time.sleep(1)
        self.click_element(self.__locators['标签名称'])
        time.sleep(1)
        self.click_element(self.__locators['标签名称框'])
        time.sleep(1)
        self.input_text(self.__locators['标签名称框'],name)
        time.sleep(1)
        self.click_sure_element()
        time.sleep(1)

    @TestLogger.log("移除按钮")
    def click_move_label(self):
        time.sleep(1)
        self.click_element(self.__locators['移除成员'])
        time.sleep(1)

    @TestLogger.log("清空搜索框")
    def clear_input_box(self):
        time.sleep(1)
        self.click_element(self.__locators['清空搜索框'])
        time.sleep(1)

    @TestLogger.log("清空搜索框")
    def is_element_present(self, locator='清空搜索框'):
        """判断元素是否存在,默认清空搜索框"""
        time.sleep(1)
        return self._is_element_present(self.__locators[locator])

    @TestLogger.log()
    def sure_icon_is_checkable(self):
        """确定按钮是否可点击"""
        return self._is_clickable(self.__class__.__locators['确定'])

    @TestLogger.log("点击已选择联系人头像")
    def click_selected_contacts(self):
        time.sleep(1)
        self.click_element(self.__class__.__locators['已选择的联系人'])
        time.sleep(1)


    @TestLogger.log("删除输入标签名称")
    def delete_label_name(self, name='bbb'):
        time.sleep(1)
        self.click_element(self.__locators['标签名称'])
        time.sleep(1)
        self.click_element(self.__locators['标签名称框'])
        time.sleep(1)
        self.input_text(self.__locators['标签名称框'], name)
        time.sleep(1)
        self.click_element(self.__locators['刪除_标签名'])
        time.sleep(1)

    @TestLogger.log("标签名称")
    def click_label_name(self):
        time.sleep(1)
        self.click_element(self.__locators['标签名称'])
        time.sleep(1)

    @TestLogger.log("点击设置")
    def click_settings_button(self):
        time.sleep(1)
        self.click_element(self.__locators['设置'])
        time.sleep(1)

    @TestLogger.log("点击群发信息")
    def click_send_message_to_group(self):
        time.sleep(1)
        self.click_element(self.__locators['群发信息'])
        time.sleep(1)

    @TestLogger.log("多方通话_图标")
    def click_mult_call_icon(self):
        time.sleep(1)
        self.click_element(self.__locators['多方通话_图标'])
        time.sleep(1)

    @TestLogger.log("点击分组_图标")
    def click_divide_group_icon(self):
        time.sleep(1)
        self.click_element(self.__locators['分组联系人'])
        time.sleep(1)

    @TestLogger.log('返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('点击创建群')
    def click_create_group(self):
        self.click_element(self.__locators['新建群组'])

    @TestLogger.log('搜索群')
    def click_search_input(self):
        self.click_element(self.__locators['搜索群组'])

    @TestLogger.log('判断列表是否存在群XXX')
    def is_group_in_list(self, name):
        groups = self.mobile.list_iterator(self.__locators['群列表'], self.__locators['列表项'])
        for group in groups:
            if group.find_elements(MobileBy.XPATH,
                                   '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
                                   '@text="{}"]'.format(name)):
                return True
        return False

    @TestLogger.log('点击群')
    def click_group(self, name):
        if self.is_group_in_list(name):
            self.click_element((MobileBy.XPATH,
                                '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
                                '@text="{}"]'.format(name)))
        else:
            raise NoSuchElementException('找不到群：{}'.format((MobileBy.XPATH,
                                                           '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and ' +
                                                           '@text="{}"]'.format(name))))

    @TestLogger.log('等待群聊列表页面加载')
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        self.wait_until(
            condition=lambda d: self._is_element_present(self.__locators['新建群组']),
            timeout=timeout,
            auto_accept_permission_alert=auto_accept_alerts
        )

    @TestLogger.log('创建群聊')
    def create_group_chats_if_not_exits(self, name, members_list):
        """
        导入群聊数据
        :param members_list:
        :param name:
        :return:
        """

        self.click_search_input()

        from pages import GroupListSearchPage
        group_search = GroupListSearchPage()
        group_search.input_search_keyword(name)
        if group_search.is_group_in_list(name):
            group_search.click_back()
        else:
            group_search.click_back()
            self.click_create_group()
            from pages import SelectContactPage
            select_page = SelectContactPage()
            select_page.search_and_select_contact(*members_list)

            from pages import BuildGroupChatPage
            build_page = BuildGroupChatPage()
            build_page.create_group_chat(name)

            from pages import ChatWindowPage
            chat = ChatWindowPage()
            if chat.is_tips_display():
                chat.directly_close_tips_alert()
            chat.wait_for_page_load()
            chat.click_back1()

    @TestLogger.log()
    def click_label_grouping(self):
        """点击标签分组"""
        self.click_element(self.__class__.__locators['标签分组'])

    @TestLogger.log()
    def open_contacts_page(self):
        from pages.contacts.Contacts import ContactsPage
        """切换到标签页：通讯录"""
        self.click_element(self.__locators['通讯录'])
        ContactsPage().click_sim_contact()

    @TestLogger.log()
    def check_if_contains_element(self,text="确定"):
        '''检查指定元素是否存在，默认是确定按钮'''
        return self.page_should_contain_element(self.__locators[text])

    @TestLogger.log("点击确定")
    def click_sure_element(self):
        time.sleep(2)
        if self._is_element_present(self.__class__.__locators['确定']):
            self.click_element(self.__class__.__locators['确定'])
        else:
            self.click_element(self.__class__.__locators['确定3'])

    @TestLogger.log("点击某个联系人")
    def click_contact_element(self,text='大佬3'):
        for i in range(4):
            time.sleep(2)
            if self._is_element_present(self.__class__.__locators[text]):
                self.click_element(self.__class__.__locators[text])
                return True
            else:
                self.page_up()
        return False

    @TestLogger.log("点击允许权限")
    def click_allow_button(self):
        time.sleep(2)
        if self._is_element_present(self.__class__.__locators['允许']):
            self.click_element(self.__class__.__locators['允许'])
        return True

    @TestLogger.log("点击新建分组")
    def click_new_group(self):
        self.click_element(self.__class__.__locators['新建分组'])

    @TestLogger.log("点击星标")
    def click_star_icon(self):
        self.click_element(self.__class__.__locators['星标图标'])

    @TestLogger.log("点击通讯录星标")
    def click_contact_star_icon(self):
        self.click_element(self.__class__.__locators['星标'])

    @TestLogger.log("点击输入框")
    def click_input_element(self):
        self.click_element(self.__class__.__locators['请输入标签分组名称'])

    @TestLogger.log("分享名片")
    def click_share_button(self):
        time.sleep(1)
        self.click_element(self.__class__.__locators['分享名片'])
        time.sleep(1)

    @TestLogger.log("邀请使用")
    def click_innvation_button(self):
        time.sleep(1)
        if self._is_element_present(self.__class__.__locators['邀请使用']):
            self.click_element(self.__class__.__locators['邀请使用'])
            time.sleep(1)
            self.click_element(self.__class__.__locators['发送_邀请'])
            time.sleep(2)
            if self._is_element_present(self.__class__.__locators['信息邀请']):
                self.driver.background_app(seconds=10)
                self.driver.launch_app()
                time.sleep(1)
                return True
            else:
                return False
        return True



    @TestLogger.log("发送_邀请")
    def click_send_innvation_button(self):
        time.sleep(1)
        self.click_element(self.__class__.__locators['发送_邀请'])
        time.sleep(1)

    @TestLogger.log("点击搜索框")
    def click_search_box(self,text='搜索或输入手机号'):
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log("查看删除按钮是否存在")
    def page_should_contain_element1(self, locator="删除-搜索"):
        return self.page_should_contain_element(self.__locators[locator])

    @TestLogger.log("输入搜索内容")
    def input_search_text(self,text='dalao2'):
        self.input_text(self.__class__.__locators['搜索或输入手机号'], text)

    @TestLogger.log("搜索分组成员")
    def search_menber_text(self,text='dalao2'):
        self.input_text(self.__class__.__locators['搜索标签分组成员'], text)

    @TestLogger.log("输入内容")
    def input_content(self,text='祝一路顺风幸福美满'):
        self.input_text(self.__class__.__locators['请输入标签分组名称'],text)

    # @TestLogger.log("输入内容")
    # def inputing_content(self,text):
    #     self.input_text(self.__class__.__locators['请输入标签分组名称'],text)

    @TestLogger.log("获取标签分组输入框文本")
    def get_text_of_lablegrouping_name(self):
        return self.get_text(self.__class__.__locators['请输入标签分组名称'])


    @TestLogger.log('使用坐标点击')
    def click_coordinate(self, x=1/2, y=15/16):

        width = self.driver.get_window_size()["width"]
        height = self.driver.get_window_size()["height"]
        print("width : ",width,height)
        x_start = width*x
        y_end = height*y
        self.tap_coordinate([(x_start, y_end)])

    @TestLogger.log('删除分组标签')
    def delete_group(self, name='祝一路顺风幸福美满'):
        if self.is_text_present(name):
            self.click_text(name)
            time.sleep(2)
            flag = self._is_element_present(self.__class__.__locators['知道了'])
            if flag:
                self.click_element(self.__class__.__locators['知道了'])
            time.sleep(1)
            self.click_element(self.__class__.__locators['设置'])
            time.sleep(1)
            self.click_element(self.__class__.__locators['删除标签'])
            time.sleep(1)
            self.click_element(self.__class__.__locators['刪除按钮'])
            time.sleep(2)
            if self._is_element_present(self.__class__.__locators['允许']):
                self.click_element(self.__class__.__locators['允许'])
            time.sleep(2)
        else:
            print('标签不存在')

    @TestLogger.log("确认弹框处理")
    def tap_sure_box(self, text='知道了'):
        time.sleep(2)
        flag = self._is_element_present(self.__class__.__locators['知道了'])
        if flag:
            self.click_element(self.__class__.__locators[text])
        else:
            print('标签不存在')

    @TestLogger.log()
    def click_back_by_android(self, times=1):
        """
        点击返回，通过android返回键
        """
        # times 返回次数
        for i in range(times):
            self.driver.back()
            time.sleep(1)

    @TestLogger.log('返回按钮')
    def click_back_button(self,times=1):
        for i in range(times):
            time.sleep(2)
            if self._is_element_present(self.__class__.__locators['back_contact']):
                self.click_element(self.__class__.__locators['back_contact'])
            elif self._is_element_present(self.__class__.__locators['back_gouppage']):
                self.click_element(self.__class__.__locators['back_gouppage'])
            elif self._is_element_present(self.__class__.__locators['back_contact2']):
                self.click_element(self.__class__.__locators['back_contact2'])
            elif self._is_element_present(self.__class__.__locators['back_settings']):
                self.click_element(self.__class__.__locators['back_settings'])
            else:
                self.click_element(self.__class__.__locators['back_newpage'])
            time.sleep(1)


    @TestLogger.log('获取元素y坐标')
    def get_element_text_y(self,text='新建分组'):
        element=self.get_element(self.__locators[text])
        y=element.location.get('y')

        return  y

    @TestLogger.log('获取元素y坐标')
    def get_element_text_x(self, text='新建分组'):
        element = self.get_element(self.__locators[text])
        x = element.location.get('x')

        return x

    @TestLogger.log('判断元素是否存在')
    def page_contain_element(self, locator='添加成员菜单'):
        return self.page_should_contain_element(self.__class__.__locators[locator])

    @TestLogger.log('判断元素不存在')
    def page_not_contain_element(self, locator='添加成员菜单'):
        return self.page_should_not_contain_element(self.__class__.__locators[locator])

    @TestLogger.log('判断元素颜色')
    def get_element_color(self, locator='选择联系人'):
        element = self.get_element(self.__locators[locator])
        x=self.get_element_text_x(text=locator)
        y = self.get_element_text_y(text=locator)
        print(x,y)
        x=(x+1)/1440
        y=(y+1)/2560
        color=self.get_coordinate_color_of_element(element,x=x,y=y,by_percent=True)
        print("color = ",color)
        return color

    @TestLogger.log("新建分组")
    def new_group(self,name="aaa"):
        time.sleep(1)
        self.click_new_group()
        time.sleep(1)
        self.click_input_element()
        time.sleep(1)
        self.input_content(text=name)
        time.sleep(1)
        self.click_sure_element()
        time.sleep(2)
        self.click_allow_button()
        time.sleep(1)
        self.click_back_button()
        time.sleep(2)
        self.click_back_button()
        time.sleep(2)

    @TestLogger.log("添加成员dalao")
    def add_member(self,name='dalao5',times=1):
        member='大佬5'
        time.sleep(1)
        self.click_text('添加成员')
        time.sleep(1)
        self.click_search_box()
        time.sleep(1)
        self.input_search_text(name)
        time.sleep(1)
        self.hide_keyboard()
        time.sleep(1)
        if name is 'dalao6':
            member='大佬6'
        elif name is 'dalao7':
            member='大佬7'
        elif name is 'dalao1':
            member = '大佬1'
        elif name is 'dalao2':
            member = '大佬2'
        elif name is 'dalao3':
            member = '大佬3'
        if times==1:
            self.click_text(member)
        else:
            #time=2,点击2次
            self.click_text(member)
            time.sleep(2)
            self.click_text(member)
        flag=self.is_toast_exist("该联系人不可选择")
        isExist=1  #为是第1次添加该联系人，为2是重复添加该联系人
        if flag:
            print("联系人不可选")
            time.sleep(1)
            self.click_back_button()
            time.sleep(1)
            isExist = 2

        else:
            time.sleep(1)
            self.click_sure_element()
            time.sleep(1)
            self.click_allow_button()
            time.sleep(1)
            isExist = 1

        return isExist

    @TestLogger.log("群发信息")
    def send_message_to_group(self,message='aaaa'):
        time.sleep(1)
        self.click_element(self.__class__.__locators["群发信息"])
        time.sleep(2)
        flag= self._is_element_present(self.__class__.__locators['我已阅读'])
        if flag:
            self.click_element(self.__class__.__locators['我已阅读'])
            time.sleep(1)
            self.click_element(self.__class__.__locators['已阅读_确定'])
            time.sleep(1)

        self.click_element(self.__class__.__locators["群发_输入框"])
        time.sleep(1)
        self.input_text(self.__class__.__locators["群发_输入框"],message)
        time.sleep(1)
        self.click_element(self.__class__.__locators["发送"])
        time.sleep(2)

    @TestLogger.log("发送表情")
    def send_express_to_group(self, message='aaaa'):
        time.sleep(1)
        self.click_element(self.__class__.__locators["群发信息"])
        time.sleep(2)
        flag = self._is_element_present(self.__class__.__locators['我已阅读'])
        if flag:
            self.click_element(self.__class__.__locators['我已阅读'])
            time.sleep(1)
            self.click_element(self.__class__.__locators['已阅读_确定'])
            time.sleep(1)

        self.click_element(self.__class__.__locators["表情按钮"])
        time.sleep(1)
        self.click_element(self.__class__.__locators["表情_微笑"])
        time.sleep(1)
        self.click_element(self.__class__.__locators["发送"])
        time.sleep(2)

    @TestLogger.log("发送图片")
    def send_picture_to_group(self, message='aaaa'):
        time.sleep(1)
        self.click_element(self.__class__.__locators["群发信息"])
        time.sleep(2)
        flag = self._is_element_present(self.__class__.__locators['我已阅读'])
        if flag:
            self.click_element(self.__class__.__locators['我已阅读'])
            time.sleep(1)
            self.click_element(self.__class__.__locators['已阅读_确定'])
            time.sleep(1)
        self.click_element(self.__class__.__locators["添加图片"])
        time.sleep(1)
        self.click_element(self.__class__.__locators["选择图片"])
        time.sleep(1)
        self.click_element(self.__class__.__locators["图片发送"])
        time.sleep(15)

    @TestLogger.log("群发信息")
    def enter_group_message(self, message='aaaa'):
        time.sleep(1)
        self.click_element(self.__class__.__locators["群发信息"])
        time.sleep(2)
        flag = self._is_element_present(self.__class__.__locators['我已阅读'])
        if flag:
            self.click_element(self.__class__.__locators['我已阅读'])
            time.sleep(1)
            self.click_element(self.__class__.__locators['已阅读_确定'])
            time.sleep(1)
        time.sleep(1)

    @TestLogger.log("多方电话")
    def enter_mutil_call(self, message='aaaa'):
        time.sleep(1)
        self.click_element(self.__class__.__locators["多方电话"])

    @TestLogger.log("多方视频")
    def enter_mutil_video_call(self, message='aaaa'):
        time.sleep(1)
        self.click_element(self.__class__.__locators["多方视频"])

    def page_down(self):
        """向下滑动"""
        self.swipe_by_percent_on_screen(50, 30, 50, 70, 800)

    def find_star_by_name(self, locator, name, times=10):
        """根据联系人名称查找星标"""
        if self._is_element_present(locator):
            els = self.get_elements(locator)
            if els:
                for el in els:
                    if el.text.endswith(name):
                        return el

        c = 0
        while c < times:
            # self.page_down()
            self.page_up()
            if self._is_element_present(locator):
                els = self.get_elements(locator)
                if els:
                    for el in els:
                        if el.text.endswith(name):
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
                        if el.text.endswith(name):
                            return el
            c += 1
        return None


    def page_contain_star(self, name):
        """某联系人前是否存在星标"""
        el=self.find_star_by_name((MobileBy.XPATH, '//*[contains(@text,"%s")]' % name), name)
        if el:
            return self.page_contain_element('星标图标')
        else:
            pass


    # def swipe_select_one_member_by_name(self, name):
    #     """通过人名选择一个联系人"""
    #     el=self.get_element((MobileBy.XPATH, '//*[@text ="%s"]' % name)).text
    #     if el:
    #         self.click_text(el)
    #     else:
    #         self.find_star_by_name(el)
    #         time.sleep(2)
    #         self.click_text(el)

    @TestLogger.log("输入群名")
    def input_group_name(self,text):
        self.input_text(self.__class__.__locators['搜索'], text)

    def is_element_present_result(self):
        return self._is_element_present(self.__locators['搜索结果展示'])

    @TestLogger.log()
    def is_exists_group_by_name(self, name):
        """是否存在指定群名字的搜索结果"""
        locator = (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and contains(@text, "%s")]' % name)
        return self._is_element_present(locator)

    def get_letters_index(self):
        """获取所有索引字母"""
        container_el = self.get_element(self.__class__.__locators['索引字母容器'])
        letter_els = container_el.find_elements(MobileBy.XPATH, "//android.widget.TextView")
        if not letter_els:
            raise AssertionError("No m005_contacts, please add m005_contacts in address book.")
        letters = []
        for el in letter_els:
            letters.append(el.text)
        return letters

    @TestLogger.log()
    def click_letter_index(self, letter):
        """点击字母索引"""
        container_el = self.get_element(self.__class__.__locators['索引字母容器'])
        container_el.find_element(MobileBy.XPATH, "//android.widget.TextView[@text='%s']" % letter).click()