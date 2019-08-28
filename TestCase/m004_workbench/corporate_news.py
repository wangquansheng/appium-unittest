import unittest

from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.utils.applicationcache import current_mobile, current_driver
from library.core.utils.testcasefilter import tags
from pages import *
from pages.workbench.corporate_news.CorporateNews import CorporateNewsPage
import time

from pages.workbench.corporate_news.CorporateNewsDetails import CorporateNewsDetailsPage
from pages.workbench.corporate_news.CorporateNewsImageText import CorporateNewsImageTextPage
from pages.workbench.corporate_news.CorporateNewsLink import CorporateNewsLinkPage
from pages.workbench.corporate_news.CorporateNewsNoNews import CorporateNewsNoNewsPage
from preconditions.BasePreconditions import WorkbenchPreconditions

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    # 'Android-移动': 'single_mobile',
    'IOS-移动': '',
    'Android-电信': 'single_telecom',
    'Android-联通': 'single_union',
    'Android-移动-联通': 'mobile_and_union',
    'Android-移动-电信': '',
    'Android-移动-移动': 'double_mobile',
    'Android-XX-XX': 'others_double',
}


class Preconditions(WorkbenchPreconditions):
    """前置条件"""

    @staticmethod
    def make_already_in_message_page(reset_required=False):
        """确保应用在消息页面"""

        if not reset_required:
            message_page = MessagePage()
            if message_page.is_on_this_page():
                return
            else:
                try:
                    current_mobile().terminate_app('com.chinasofti.rcs', timeout=2000)
                except:
                    pass
                current_mobile().launch_app()
            try:
                message_page.wait_until(
                    condition=lambda d: message_page.is_on_this_page(),
                    timeout=3
                )
                return
            except TimeoutException:
                pass
        Preconditions.reset_and_relaunch_app()
        Preconditions.make_already_in_one_key_login_page()
        Preconditions.login_by_one_key_login()

    @staticmethod
    def reset_and_relaunch_app():
        """首次启动APP（使用重置APP代替）"""

        app_package = 'com.chinasofti.rcs'
        current_driver().activate_app(app_package)
        current_mobile().reset_app()

    @staticmethod
    def enter_corporate_news_page():
        """进入企业新闻首页"""

        mp = MessagePage()
        mp.wait_for_page_load()
        mp.click_workbench()
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        # 查找并点击所有展开元素
        wbp.find_and_click_open_element()
        wbp.click_add_corporate_news()

    @staticmethod
    def create_unpublished_image_news(news):
        """创建未发新闻(图文新闻)"""

        cnp = CorporateNewsPage()
        cnp.wait_for_page_load()
        for title, content in news:
            # 点击发布新闻
            cnp.click_release_news()
            cnitp = CorporateNewsImageTextPage()
            cnitp.wait_for_page_load()
            time.sleep(2)
            # 输入图文新闻标题
            cnitp.input_news_title(title)
            # 输入图文新闻内容
            cnitp.input_news_content(content)
            # 点击保存
            cnitp.click_save()
            time.sleep(2)
            # 点击确定
            cnitp.click_sure()
            cnp.wait_for_page_load()

    @staticmethod
    def release_corporate_image_news(titles):
        """发布企业新闻(图文新闻)"""

        cnp = CorporateNewsPage()
        cnp.wait_for_page_load()
        for title in titles:
            # 点击发布新闻
            cnp.click_release_news()
            cnitp = CorporateNewsImageTextPage()
            cnitp.wait_for_page_load()
            time.sleep(2)
            # 输入图文新闻标题
            cnitp.input_news_title(title)
            # 输入图文新闻内容
            cnitp.input_news_content("123")
            time.sleep(1)
            # 点击发布
            cnitp.click_release()
            time.sleep(2)
            # 点击确定
            cnitp.click_sure()
            cnp.wait_for_page_load()


class CorporateNewsTest(TestCase):
    """工作台->企业新闻"""

    @classmethod
    def setUpClass(cls):
        Preconditions.select_mobile('Android-移动')

    def default_setUp(self):
        """
        1、成功登录和飞信
        2、当前页面在企业新闻应用首页
        """

        Preconditions.select_mobile('Android-移动')
        mp = MessagePage()
        if mp.is_on_this_page():
            Preconditions.enter_corporate_news_page()
            return
        cnp = CorporateNewsPage()
        if cnp.is_on_corporate_news_page():
            current_mobile().hide_keyboard_if_display()
        else:
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.enter_corporate_news_page()

    def default_tearDown(self):
        pass

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYXW_0034(self):
        """保存新闻"""

        cnp = CorporateNewsPage()
        # 等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 点击发布新闻
        cnp.click_release_news()
        cnitp = CorporateNewsImageTextPage()
        cnitp.wait_for_page_load()
        # 点击链接发布
        cnitp.click_link_publishing()
        cnlp = CorporateNewsLinkPage()
        cnlp.wait_for_page_load()
        time.sleep(2)
        # 输入链接新闻标题
        cnlp.input_news_title("测试新闻0034")
        # 输入链接新闻网址
        cnlp.input_link_url("https://10086.com")
        # 点击保存
        cnlp.click_save()
        # 点击确定
        cnlp.click_sure()
        # 1.是否提示保存成功,等待企业新闻首页加载
        self.assertEquals(cnlp.is_exist_save_successfully(), True)
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYXW_0019(self):
        """管理员删除未发布新闻，删除成功"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 点击未发新闻
        cnp.click_no_news()
        cnnp = CorporateNewsNoNewsPage()
        # 3.等待未发新闻页加载
        cnnp.wait_for_page_load()
        time.sleep(2)
        cnnp.clear_no_news()
        # 确保未发新闻列表存在数据
        news = [("测试新闻0019", "测试内容0019")]
        cnnp.click_close()
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        wbp.click_company_news()
        Preconditions.create_unpublished_image_news(news)
        cnp.click_no_news()
        cnnp.wait_for_page_load()
        # 点击未发新闻
        title = cnnp.click_no_news_by_number(0)
        time.sleep(2)
        cndp = CorporateNewsDetailsPage()
        # 4.等待未发布新闻详情页加载
        cndp.wait_for_page_load()
        time.sleep(2)
        # 点击删除
        cndp.click_delete()
        # 5.点击确定
        cndp.click_sure()
        # 6.是否提示删除成功，未发新闻列表不存在该记录信息
        self.assertEquals(cndp.is_exist_delete_successfully(), True)
        cnnp.wait_for_page_load()
        self.assertEquals(cnnp.is_exist_no_news_by_name(title), False)


class CorporateNewsAllTest(TestCase):
    """工作台->企业新闻"""

    @classmethod
    def setUpClass(cls):
        Preconditions.select_mobile('Android-移动')

    def default_setUp(self):
        """
        1、成功登录和飞信
        2、当前页面在企业新闻应用首页
        """

        Preconditions.select_mobile('Android-移动')
        mp = MessagePage()
        if mp.is_on_this_page():
            Preconditions.enter_corporate_news_page()
            return
        cnp = CorporateNewsPage()
        if cnp.is_on_corporate_news_page():
            current_mobile().hide_keyboard_if_display()
        else:
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.enter_corporate_news_page()

    def default_tearDown(self):
        pass

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYXW_0001(self):
        """检查企业新闻入口是否正确进入企业新闻首页"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 确保企业新闻首页不存在新闻
        cnp.clear_corporate_news()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYXW_0002(self):
        """检查点击返回按钮控件【<】"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        wbp = WorkbenchPage()
        if cnp.is_exist_close_button():
            cnp.click_close()
            wbp.wait_for_workbench_page_load()
            wbp.click_company_news()
            cnp.wait_for_page_load()
        # 点击【<】
        cnp.click_back()
        # 3.等待工作台页面加载
        wbp.wait_for_workbench_page_load()
        wbp.click_company_news()
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYXW_0003(self):
        """检查点击关闭按钮控件【X】"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 确保有控件【X】
        cnp.click_no_news()
        cnnp = CorporateNewsNoNewsPage()
        cnnp.wait_for_page_load()
        # 点击【X】
        cnnp.click_close()
        # 3.等待工作台页面加载
        wbp = WorkbenchPage()
        wbp.wait_for_workbench_page_load()
        wbp.click_company_news()
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYXW_0004(self):
        """管理员进入企业新闻初始页，检查页面元素"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 确保企业新闻首页不存在新闻
        cnp.clear_corporate_news()
        # 3.是否存在提示语,“发布新闻”、“未发新闻”按钮
        self.assertEquals(cnp.is_exist_words(), True)
        self.assertEquals(cnp.is_exist_release_news_button(), True)
        self.assertEquals(cnp.is_exist_no_news_button(), True)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYXW_0005(self):
        """管理员进入企业新闻页，新闻列表按发布时间倒序排序"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        cnp.clear_corporate_news()
        # 确保存在多条已发布的企业新闻
        titles = ["测试新闻00051", "测试新闻00052", "测试新闻00053", "测试新闻00054"]
        Preconditions.release_corporate_image_news(titles)
        time.sleep(3)
        # 3.企业新闻列表是否按发布时间倒序排序
        self.assertEquals(cnp.get_corporate_news_titles(), titles)

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYXW_0006(self):
        """管理员下线自己发布的企业新闻，下线成功"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 确保存在已发布的企业新闻
        if not cnp.is_exist_corporate_news():
            titles = ["测试新闻0006"]
            Preconditions.release_corporate_image_news(titles)
        # 3.选择一条企业新闻
        cnp.click_corporate_news_by_number(0)
        cndp = CorporateNewsDetailsPage()
        # 等待企业新闻详情页加载
        cndp.wait_for_page_load()
        # 4.点击下线
        cndp.click_offline()
        # 5.点击确定，是否提示下线成功
        cndp.click_sure()
        self.assertEquals(cndp.is_exist_offline_successfully(), True)
        # 等待企业新闻首页加载
        cnp.wait_for_page_load()

    @unittest.skip("暂时难以实现,跳过")
    def test_QYXW_0008(self):
        """管理员按英文搜索企业新闻"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        cnp.clear_corporate_news()
        # 确保存在多条已发布的企业新闻
        titles = ["testnews", "测试新闻0008", "news"]
        Preconditions.release_corporate_image_news(titles)
        cnp.click_search_icon()
        cnp.input_search_content("testnews")
        cnp.click_search_button()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYXW_0017(self):
        """管理员发布新闻成功"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 点击发布新闻
        cnp.click_release_news()
        cnitp = CorporateNewsImageTextPage()
        # 3.等待发布新闻-图文发布页加载
        cnitp.wait_for_page_load()
        # 4.点击链接发布
        cnitp.click_link_publishing()
        time.sleep(2)
        cnlp = CorporateNewsLinkPage()
        cnlp.wait_for_page_load()
        # 5.输入链接新闻标题、内容
        cnlp.input_news_title("测试新闻0017")
        cnlp.input_link_url("https://10086.com")
        # 6.点击发布
        cnlp.click_release()
        # 点击确定
        cnlp.click_sure()
        # 7.是否提示发布成功
        self.assertEquals(cnlp.is_exist_release_successfully(), True)
        # 等待企业新闻首页加载
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYXW_0018(self):
        """管理员取消发布新闻成功"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 点击发布新闻
        cnp.click_release_news()
        cnitp = CorporateNewsImageTextPage()
        # 3.等待发布新闻-图文发布页加载
        cnitp.wait_for_page_load()
        # 4.点击链接发布
        cnitp.click_link_publishing()
        cnlp = CorporateNewsLinkPage()
        cnlp.wait_for_page_load()
        time.sleep(2)
        # 5.输入链接新闻标题、内容
        cnlp.input_news_title("测试新闻0018")
        cnlp.input_link_url("https://10086.com")
        # 6.点击发布
        cnlp.click_release()
        # 7.取消发布新闻
        cnlp.click_cancel()
        cnlp.click_back()
        # 等待企业新闻首页加载
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYXW_0020(self):
        """管理员发布未发布新闻，发布成功"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 点击未发新闻
        cnp.click_no_news()
        cnnp = CorporateNewsNoNewsPage()
        # 3.等待未发新闻页加载
        cnnp.wait_for_page_load()
        # 确保存在未发布的企业新闻
        if not cnnp.is_exist_no_news():
            cnnp.click_back()
            cnp.wait_for_page_load()
            news = [("测试新闻0020", "测试内容0020")]
            Preconditions.create_unpublished_image_news(news)
            cnp.click_no_news()
            cnnp.wait_for_page_load()
        # 点击一条未发新闻
        cnnp.click_no_news_by_number(0)
        cndp = CorporateNewsDetailsPage()
        # 4.等待企业新闻详情页加载
        cndp.wait_for_page_load()
        # 5.点击发布
        cndp.click_release()
        # 6.点击确定，是否提示发布成功
        cndp.click_sure()
        self.assertEquals(cndp.is_exist_release_successfully(), True)
        # 等待企业新闻首页加载
        cnp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'workbench', 'LXD')
    def test_QYXW_0030(self):
        """检验统计新闻浏览人数功能是否正确"""

        cnp = CorporateNewsPage()
        # 1、2.等待企业新闻首页加载
        cnp.wait_for_page_load()
        # 确保存在多条已发布的企业新闻
        titles = ["测试新闻00301", "测试新闻00302"]
        Preconditions.release_corporate_image_news(titles)
        number = 0
        # 访问前的浏览量
        amount = cnp.get_corporate_news_page_view_by_number(number)
        # 3.进入新闻详情页
        cnp.click_corporate_news_by_number(number)
        cndp = CorporateNewsDetailsPage()
        cndp.wait_for_page_load()
        cndp.click_back()
        cnp.wait_for_page_load()
        # 访问后的浏览量
        news_amount = cnp.get_corporate_news_page_view_by_number(number)
        # 4.验证每次用户查看新闻详情再返回到列表之后，浏览数量是否+1
        self.assertEquals(amount + 1, news_amount)
