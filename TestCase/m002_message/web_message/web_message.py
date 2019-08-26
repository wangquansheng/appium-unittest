# from selenium.common.exceptions import TimeoutException
#
# import preconditions
# from library.core.TestCase import TestCase
# from library.core.utils.applicationcache import current_mobile
# from pages import SingleChatPage, SelectLocalContactsPage, MessagePage, ContactsPage
# from pages.components import BaseChatPage
#
# REQUIRED_MOBILES = {
#     'Android-移动': 'M960BDQN229CH',
#     'Android-XX': ''  # 用来发短信
# }
#
#
# class Preconditions(object):
#
#     @staticmethod
#     def make_already_in_message_page():
#         """确保进入消息界面"""
#         preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
#         current_mobile().hide_keyboard_if_display()
#         message_page = MessagePage()
#         if message_page.is_on_this_page():
#             return
#         try:
#             current_mobile().terminate_app('com.chinasofti.rcs', timeout=2000)
#         except:
#             pass
#         current_mobile().launch_app()
#         try:
#             message_page.wait_until(
#                 condition=lambda d: message_page.is_on_this_page(),
#                 timeout=15
#             )
#             return
#         except TimeoutException:
#             pass
#         preconditions.reset_and_relaunch_app()
#         preconditions.make_already_in_one_key_login_page()
#         preconditions.login_by_one_key_login()
#
#         @staticmethod
#         def enter_single_chat_page(name):
#             """进入单聊聊天会话页面"""
#             mp = MessagePage()
#             mp.wait_for_page_load()
#             # 点击 +
#             mp.click_add_icon()
#             # 点击“新建消息”
#             mp.click_new_message()
#             slc = SelectLocalContactsPage()
#             slc.wait_for_page_load()
#             # 进入单聊会话页面
#             slc.selecting_local_contacts_by_name(name)
#             bcp = BaseChatPage()
#             if bcp.is_exist_dialog():
#                 # 点击我已阅读
#                 bcp.click_i_have_read()
#             scp = SingleChatPage()
#             # 等待单聊会话页面加载
#             scp.wait_for_page_load()
#
# class PostWebMsg(TestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         # 创建联系人
#         fail_time = 0
#         import dataproviders
#         while fail_time < 3:
#             try:
#                 required_contacts = dataproviders.get_preset_contacts()
#                 conts = ContactsPage()
#                 preconditions.connect_mobile(REQUIRED_MOBILES['Android-移动'])
#                 current_mobile().hide_keyboard_if_display()
#                 preconditions.make_already_in_message_page()
#                 for name, number in required_contacts:
#                     conts.open_contacts_page()
#                     if conts.is_text_present("显示"):
#                         conts.click_text("不显示")
#                     conts.create_contacts_if_not_exits(name, number)
#                 return
#             except:
#                 fail_time += 1
#                 import traceback
#                 msg = traceback.format_exc()
#                 print(msg)
#
#     @classmethod
#     def tearDownClass(cls):
#         current_mobile().hide_keyboard_if_display()
#         preconditions.make_already_in_message_page()
#
#     def default_setUp(self):
#         """确保进入消息界面"""
#         Preconditions.make_already_in_message_page()