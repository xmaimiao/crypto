import json
import logging
from time import sleep
import yaml
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from common.contants import basepage_dir


def _get_working():
    '''
    读入配置文件,判断是启用调试端口,还是新开浏览器
    '''
    with open(basepage_dir, encoding="utf-8") as f:
        data = yaml.safe_load(f)
        working = data["switch"][data["switch_default"]]
        return working


class BasePage:
    _driver = None
    _params = {}
    _base_url = ""
    _working = _get_working()
    _chrome_options = Options()
    # 清理已有 handlers
    root_logger = logging.getLogger()
    for h in root_logger.handlers[:]:
        root_logger.removeHandler(h)
    logging.basicConfig(level=logging.INFO)

    def __init__(self, driver: WebDriver = None):

        if driver is None:
            if self._working == "port":
                # 和瀏覽器打開的調試端口進行通信，瀏覽器要使用命令 chrome --remote-debugging-port=9222 開啟調試
                self._chrome_options.debugger_address = "127.0.0.1:9222"
                self._driver = webdriver.Chrome(options=self._chrome_options)

            elif self._working == "brower":
                # 有界面方式打开浏览器
                self._driver = webdriver.Chrome()

            self._driver.maximize_window()
            self._driver.implicitly_wait(3)
        else:
            self._driver = driver

        if self._base_url != "":
            self._driver.get(self._base_url)

    def find(self, by, locator):
        # 调用find函数即打印日志
        logging.info(f"find：{locator}")
        if by == None:
            result = self._driver.find_element(*locator)
        else:
            result = self._driver.find_element(by, locator)
        return result

    def find_and_click(self, by, locator):
        logging.info(f"click：{locator}")
        self.find(by, locator).click()

    def wait_for_click(self, by, locator, timeout=10):
        ''''
        等待元素可出現且可點擊
        '''
        logging.info(f"wait_click：{locator},timeout：{timeout}")
        WebDriverWait(self._driver, timeout).until(expected_conditions.element_to_be_clickable((by, locator)))

    def wait_for_display(self, by, locator, timeout=10):
        '''
        等待元素出現，一旦出現就不斷查找元素，用於獲取toast
        '''
        logging.info(f"wait_display：{locator},timeout：{timeout}")
        stutas = WebDriverWait(self._driver, timeout).until(
            expected_conditions.visibility_of_element_located((by, locator)))
        if stutas:
            ele = self.find(by, locator)
            return ele
        return ValueError("元素不存在")

    def sleep(self, time):
        logging.info(f"sleep：{time}")
        sleep(time)

    def execute_script_scrol(self,by, locator):
        '''
        通过js滚动定位元素
        '''
        logging.info(f"execute_script_scrol：{locator}")
        target = self.find(by, locator)
        self._driver.execute_script("arguments[0].scrollIntoView();", target)

    def set_implicitly_wait(self, second):
        '''
        顯性等待
        '''
        self._driver.implicitly_wait(second)

    def close(self):
        self._driver.quit()

    def step(self, path, name):
        with open(path, encoding="utf-8") as f:
            steps = yaml.safe_load(f)[name]
        # ${}的參數轉化
        raw_data = json.dumps(steps)
        for key, value in self._params.items():
            raw_data = raw_data.replace("${" + key + "}", str(value))
        steps = json.loads(raw_data)
        for step in steps:
            if "action" in step.keys():
                action = step["action"]
                if "wait_click" == action:
                    self.wait_for_click(step["by"], step["locator"])
                if "click" == action:
                    self.find_and_click(step["by"], step["locator"])
                if "wait_display" == action:
                    ele = self.wait_for_display(step["by"], step["locator"])
                    return ele
                if "sleep" == action:
                    sleep(step["locator"])
                if "execute_js_scrol" == action:
                    self.execute_script_scrol(step["by"],step["locator"])



if __name__ == '__main__':
    BasePage()
