# 调度器:
#     代理池开关
TEST_CYCLE = 100
GET_CYCLE = 20
TEST_ENABLED = True
GET_ENABLED = True
API_ENABLED = True

from multiprocessing import Process
from api import app
from get import Getter
from ip_pool.test import Test
import time


class Schedule():
    def schedule_test(self, cycle=TEST_CYCLE):
        """

        :param cycle: 定时测试的周期
        :return:
        """
        tester = Test()
        while True:
            print("测试开始...")
            tester.run()
            time.sleep(cycle)

    def schedule_get(self, cycle=GET_CYCLE):
        getter = Getter()
        while True:
            print("开始抓取...")
            getter.run()
            time.sleep(cycle)

    def schedule_api(self):
        app.run()

    def do(self):
        print("代理池开始运行...")
        if TEST_ENABLED:
            test_process = Process(target=self.schedule_test)
            test_process.start()

        if GET_ENABLED:
            get_process = Process(target=self.schedule_get)
            get_process.start()

        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()


if __name__ == '__main__':
    start = Schedule()
    start.do()