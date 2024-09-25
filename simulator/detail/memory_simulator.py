# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 13:21:31 2020

@author: sinof
"""

def Memory_sim(operation, mem, add):
    if (operation == "w0"):
        mem[add] = '0'
    if (operation == "w1"):
        mem[add] = '1'
    if (operation == "r0" and mem[add] == '1'):
        return 1
    if (operation == "r1" and mem[add] == '0'):
        return 1
    else:
        return 0