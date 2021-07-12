import yaml
from common.contants import basepage_dir, main_dir
from page.basepage import BasePage, _get_working
from page.cro_usdcPage import Cro_usdcPage


class Main(BasePage):
    '''
    首頁面po
    '''
    _working = _get_working()

    with open(basepage_dir, encoding="utf-8") as f:
        env = yaml.safe_load(f)
        if _working != "port":
            _base_url = env["docker_env"][env["default"]]

    def wait_sleep(self, sleeps):
        '''
        强制等待
        '''
        self.sleep(sleeps)
        return self

    def goto_USDC(self):
        '''
        点击USDC标签
        '''
        self.step(main_dir,'goto_USDC')
        return self

    def click_CRO(self):
        '''
        点击CRO/USDC
        '''
        self.step(main_dir,'click_CRO')
        return Cro_usdcPage(self._driver)