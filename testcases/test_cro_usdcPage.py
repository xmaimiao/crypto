import allure
import pytest
import yaml

from common.contants import basepage_dir, test_cro_usdcPage_dir
from page.basepage import _get_working
from page.main import Main


def get_env():
    '''
    获取环境变量：uat、dev
    '''
    with open(basepage_dir, encoding="utf-8") as f:
        datas = yaml.safe_load(f)
        # 获取basepage.yaml中设置的环境变量
        env =  datas["default"]
        return env


def get_data(option):
    '''
    获取yaml测试数据
    '''
    with open(test_cro_usdcPage_dir, encoding="utf-8") as f:
        datas = yaml.safe_load(f)[option]
        return datas

@allure.feature("测试Cro_usdc模块")
class TestCro_usdcPage:

    user_env = get_env()
    # 启用调试端口,还是新开浏览器
    _working = _get_working()

    if _working == "port":
        def setup(self):
            '''
            開啓調試端口啓用
            '''
            self.main = Main()
    else:
        def setup_class(self):
            '''
            非調試端口用
            '''
            self.main = Main()

        def teardown_class(self):
            '''
            非調試端口啓用
            '''
            self.main.close()

    @allure.title("验证打开了cro_usdc页面")
    @pytest.mark.parametrize('data', get_data("test_into_cro_usdc"))
    def test_into_cro_usdc(self,data):
        result = self.main.goto_USDC().click_CRO().get_Order_Book_text()
        assert result == data["expect"]
