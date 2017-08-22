# -*- coding: utf-8 -*-
#__author__="ZJL"

import os
import multiprocessing

# print(os.system("python app/flaskrun.py"))
# print(os.system("python run.py"))

def worker(str):
    os.system(str)

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=worker, args=("python app/flaskrun.py",))
    p2 = multiprocessing.Process(target=worker, args=("python run.py",))
    p3 = multiprocessing.Process(target=worker, args=("python checkout_script.py",))

    p1.start()
    p2.start()
    p3.start()
