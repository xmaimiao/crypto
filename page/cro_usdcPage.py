from common.contants import cro_usdcpage_dir
from page.basepage import BasePage


class Cro_usdcPage(BasePage):

    def wait_sleep(self, sleeps):
        '''
        强制等待
        '''
        self.sleep(sleeps)
        return self

    def get_Order_Book_text(self):
        '''
        获取页面文本，验证已打开该页面
        '''
        return (self.step(cro_usdcpage_dir,"get_Order_Book_text")).text