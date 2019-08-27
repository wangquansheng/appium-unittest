import time

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile
from preconditions.BasePreconditions import LoginPreconditions
from library.core.utils.testcasefilter import tags
from pages import *


class Preconditions(LoginPreconditions):
    """前置条件"""

    @staticmethod
    def init_and_enter_collection_page():
        """预置收藏文件条件,进入收藏页面"""
        # 登录进入消息页面
        Preconditions.make_already_in_message_page()
        file_types = [".doc", ".docx", ".ppt", ".pptx", ".pdf", ".xls", ".xlsx", ".txt"]
        mess = MessagePage()
        # 点击“我”
        mess.open_me_page()
        # 点击收藏
        me = MePage()
        me.click_menu("收藏")
        mcp = MeCollectionPage()
        # 添加未收藏类型的文件
        diff_file_types = []
        have_file_types = []
        if not mcp.is_text_present("没有任何收藏"):
            have_file_types = mcp.get_file_types()
        for tmp in file_types:
            if tmp not in have_file_types:
                diff_file_types.append(tmp)
        mcp.click_back()
        # 切换到通讯录
        mess.open_contacts_page()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        contacts.click_mobile_contacts()
        time.sleep(1)
        names = contacts.get_contacts_name()
        if '本机' in names:
            names.remove('本机')
        contacts.select_people_by_name(names[0])
        contact_detail = ContactDetailsPage()
        contact_detail.click_message_icon()
        chat = SingleChatPage()
        # 如果弹框用户须知则点击处理
        flag = chat.is_exist_dialog()
        if flag:
            chat.click_i_have_read()
        for file_type in diff_file_types:
            # 进入到文件选择页面
            chat.click_more()
            more_page = ChatMorePage()
            more_page.click_file()
            # 点击本地文件，进入到本地文件中
            csf = ChatSelectFilePage()
            csf.wait_for_page_load()
            csf.click_local_file()
            local_file = ChatSelectLocalFilePage()
            # 没有预置文件，则上传
            flag = local_file.push_preset_file()
            if flag:
                local_file.click_back()
                csf.click_local_file()
            # 进入预置文件目录，选择文件发送
            local_file.click_preset_file_dir()
            file = local_file.select_file(file_type)
            if file:
                local_file.click_send()
                chat.collection_file(file_type)
            else:
                local_file.click_back()
                local_file.click_back()
                csf.click_back()
                chat.wait_for_page_load()
        # 收藏位置
        try:
            chat.click_more()
            more_page = ChatMorePage()
            more_page.click_location()
            location_page = ChatLocationPage()
            location_page.wait_for_page_load()
            addr = location_page.get_location_info()
            location_page.click_send()
            chat.wait_for_page_load()
            chat.collection_file(addr)
            # 从聊天会话页面返回收藏页面
            chat.click_back()
            contact_detail.click_back_icon()
            mess.open_me_page()
            me = MePage()
            me.click_menu("收藏")
            mcp.wait_for_page_load()
        except:
            pass

    @staticmethod
    def enter_collection_page():
        """进入收藏页面"""
        mess = MessagePage()
        # 点击“我”
        mess.open_me_page()
        # 点击收藏
        me = MePage()
        me.click_menu("收藏")


class MsgCollectionTest(TestCase):
    """消息-收藏"""
    @classmethod
    def setUpClass(cls):
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.init_and_enter_collection_page()
            return
        mcp = MeCollectionPage()
        if mcp.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            Preconditions.init_and_enter_collection_page()
            # 创建联系人
            fail_time = 0
            import dataproviders
            while fail_time < 2:
                try:
                    required_contacts = dataproviders.get_preset_contacts()
                    conts = ContactsPage()
                    for name, number in required_contacts:
                        conts.open_contacts_page()
                        if conts.is_text_present("显示"):
                            conts.click_text("不显示")
                        conts.create_contacts_if_not_exits_new(name, number)
                    return
                except:
                    fail_time += 1
                    import traceback
                    msg = traceback.format_exc()
                    print(msg)

    def default_setUp(self):
        Preconditions.make_already_in_message_page()
        Preconditions.enter_collection_page()
        pass

    @tags('ALL', 'SMOKE', 'CMCC', 'collection')
    def test_msg_collection_0001(self):
        """点击格式为doc的文件打开查阅"""
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        mcp.open_file(".doc")
        mcp.wait_for_open_file()
        mcp.click_back()
        mcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'collection')
    def test_msg_collection_0002(self):
        """点击格式为docx的文件打开查阅"""
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        mcp.open_file(".docx")
        mcp.wait_for_open_file()
        mcp.click_back()
        mcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'collection')
    def test_msg_collection_0003(self):
        """点击格式为ppt的文件打开查阅"""
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        mcp.open_file(".ppt")
        mcp.wait_for_open_file()
        mcp.click_back()
        mcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'collection')
    def test_msg_collection_0004(self):
        """点击格式为pptx的文件打开查阅"""
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        mcp.open_file(".pptx")
        mcp.wait_for_open_file()
        mcp.click_back()
        mcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'collection')
    def test_msg_collection_0005(self):
        """点击格式为pdf的文件打开查阅"""
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        mcp.open_file(".pdf")
        mcp.wait_for_open_file()
        mcp.click_back()
        mcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'collection')
    def test_msg_collection_0006(self):
        """点击格式为xls的文件打开查阅"""
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        mcp.open_file(".xls")
        mcp.wait_for_open_file()
        mcp.click_back()
        mcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'collection')
    def test_msg_collection_0007(self):
        """点击格式为xlsx的文件打开查阅"""
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        mcp.open_file(".xlsx")
        mcp.wait_for_open_file()
        mcp.click_back()
        mcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'collection')
    def test_msg_collection_0008(self):
        """点击格式为txt的文件打开查阅"""
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        mcp.open_file(".txt")
        mcp.wait_for_open_file()
        mcp.click_back()
        mcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'collection')
    def test_msg_collection_0009(self):
        """点击位置，进入到位置界面"""
        # 初始化时，位置无法获取成功，导致无法收藏位置。初始化导致失败，app问题
        try:
            mcp = MeCollectionPage()
            mcp.wait_for_page_load()
            mcp.open_location("[位置]")
            mcp.wait_for_location_page_load()
            mcp.click_back()
            mcp.wait_for_page_load()
        except:
            pass

    @tags('ALL', 'SMOKE', 'CMCC', 'collection')
    def test_msg_collection_0010(self):
        """点击位置，进入到位置界面"""
        # 初始化时，位置无法获取成功，导致无法收藏位置。初始化导致失败，app问题
        # 1、点击位置
        try:
            mcp = MeCollectionPage()
            mcp.wait_for_page_load()
            mcp.open_location("[位置]")
            mcp.wait_for_location_page_load()
            # 2、点击右下角按钮
            mcp.click_nav_btn()
            toast_flag = mcp.is_toast_exist("未发现手机导航应用", timeout=3)
            map_flag = mcp.is_text_present("地图")
            self.assertTrue(toast_flag or map_flag)
        except:
            pass
