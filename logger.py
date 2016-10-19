# -*- coding: utf-8 -*-
import logging

# http://www.cnblogs.com/goodhacker/p/3355660.html
# 日志系统， 既要把日志输出到控制台， 还要写入日志文件


class Logger():

    def __init__(self, logfilename, logger):

        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        fileHandler = logging.FileHandler(logfilename)
        fileHandler.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter(
            '%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s - %(message)s')
        fileHandler.setFormatter(formatter)
        consoleHandler.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fileHandler)
        self.logger.addHandler(consoleHandler)

    def getlogger(self):
        return self.logger
