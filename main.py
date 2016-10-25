# coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
from easyprocess import EasyProcess
from random_str import *
import time

from utils import *


class Erya(object):

    url = 'http://passport2.chaoxing.com/login?fid=1479&refer=http://i.mooc.chaoxing.com'

    def __init__(self, userID=None, pwd=None, id=None, end_id=None):
        if not userID or not pwd:
            print('No information')
        self.__userID = userID
        self.__pwd = pwd
        self.id = id
        self.end_id = end_id
        self.driver = webdriver.Firefox()
        # 不支持PhantomJS,其他浏览器未测试
        # self.driver = webdriver.PhantomJS()
        self.wait = WebDriverWait(self.driver, 30)

    def login(self):
        self.driver.get(Erya.url)
        try:
            span = self.wait.until(
                EC.visibility_of_element_located((By.ID, "nameNoteId")))
            span.click()
        except:
            print('EC error')
        unameId = self.wait.until(
            EC.visibility_of_element_located((By.ID, "unameId")))
        unameId.clear()
        unameId.send_keys(self.__userID)

        passwordId = self.wait.until(
            EC.visibility_of_element_located((By.ID, "passwordId")))
        passwordId.clear()
        passwordId.send_keys(self.__pwd)

        self.driver.set_window_size(1166, 741)

        vcode_path = './main.png'
        vcode_out_path = './main-cut.png'
        self.driver.save_screenshot(vcode_path)
        cut_vcode(vcode_path, vcode_out_path, 430, 343, 502, 374)
        try:
            EasyProcess('tesseract main-cut.png ./CAPTCHA').call()
            aha = True
        except:
            print('没检测到tesseract，手动输入验证码，登录')
            try:
                WebDriverWait(self.driver, 5).until(
                    lambda x: x.find_element_by_id("space_nickname"))
            except:
                return False
            aha = False
        if aha:
            with open('./CAPTCHA.txt') as f:
                CAPTCHA = f.read()
            numcode = self.driver.find_element_by_id('numcode')
            numcode.clear()
            numcode.send_keys(CAPTCHA)
            try:
                WebDriverWait(self.driver, 5).until(
                    lambda x: x.find_element_by_id("space_nickname"))
            except:
                return False
        try:
            name = self.driver.find_element_by_class_name('personname')
            print('你好，{}!'.format(name.text.encode("utf-8")))
            return True
        except:
            print('登录失败,正在尝试重新登录。')
            return False

    def get_cur(self):
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(
            (By.TAG_NAME, "iframe")))
        lession = self.driver.find_element_by_class_name('clearfix')
        print(
            '你已选择课程[{}]\n----------------------------------'.format(lession.text.encode("utf-8")))
        duration = self.driver.find_element_by_xpath(
            '/html/body/div/div[2]/div[2]/ul/li[1]/div[2]/p[4]')
        print(duration.text)
        url = lession.find_elements_by_tag_name(
            'a')[0].get_attribute('href').encode("utf-8")
        self.driver.get(url)
        a = self.driver.find_element_by_class_name('articlename')
        a.click()

    def find_and_play(self):
        num = int(self.end_id.split('cur')[-1]) - int(self.id.split('cur')[-1])
        for i in xrange(num + 1):
            ncells = self.driver.find_element_by_id(self.id)
            print('当前页面：{}: {}'.format(ncells.text.encode(
                'utf-8').split(' ')[0], ncells.text.encode('utf-8').split(' ')[2]))
            ncells.click()
            self.get_video()
            if self.is_finished():
                print('已完成，跳转中')
            else:
                print('正在看视频')
                self.play()
                self.is_finished()
            self.id = 'cur{}'.format(int(self.id.split('cur')[-1]) + 1)

    def get_video(self):
        self.driver.implicitly_wait(1)
        tag = self.driver.find_element_by_class_name(
            'tabtags').find_element_by_id('dct1')
        if len(tag.text.encode('utf-8')) > 10:
            tag = self.driver.find_element_by_class_name(
                'tabtags').find_element_by_id('dct2')
            tag.click()

    def is_finished(self):
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(
            (By.TAG_NAME, "iframe")))
        self.wait.until(EC.visibility_of_element_located(
            (By.TAG_NAME, "iframe")))
        # self.driver.implicitly_wait(10)
        time.sleep(2)
        self.driver.switch_to_default_content()
        vcode_path = './main.png'
        vcode_out_path = './main-cut.png'
        self.driver.save_screenshot(vcode_path)
        cut_vcode(vcode_path, vcode_out_path, 165, 265, 182, 274)
        RGB = get_color(vcode_out_path)
        if RGB == (110, 162, 47):
            return True
        elif RGB == (248, 179, 0):
            return False
        else:
            print(RGB)
            exit()

    def play(self):
        # 播放
        self.driver.switch_to_frame(
            self.driver.find_element_by_tag_name("iframe"))
        self.driver.switch_to_frame(
            self.driver.find_element_by_tag_name("iframe"))
        self.driver.implicitly_wait(10)
        reader = self.driver.find_element_by_id('reader')
        reader.click()
        # To do
        # 检测回答问题，播放暂停，播放结束，自动跳转
        self.driver.implicitly_wait(60 * 24)

    def fill_in_discuss(self):
        pass

if __name__ == '__main__':
    userID = 15262057000
    pwd = ''
    begin_id = 'cur86883496'
    end_id = 'cur86883558'

    erya = Erya(userID, pwd)
    # login
    is_logined = erya.login()
    while(not is_logined):
        is_logined = erya.login()

    # 获得课程
    erya.get_cur()
    erya.id = begin_id
    erya.end_id = end_id
    # 找到未完成的视频
    erya.find_and_play()

    erya.driver.close()
