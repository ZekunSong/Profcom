# -*- coding: utf-8 -*-
# 获取本地的ip
import os


class Host():

    def gethost(self):
        ip = -1
        try:
            route = [a for a in os.popen(
                'route print').readlines() if ' 0.0.0.0 ' in a]
            if len(route) > 0:
                ip = route[0].split()[-2]
        except Exception as e:
            raise e
        return ip
