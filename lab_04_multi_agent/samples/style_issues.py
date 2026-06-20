"""Sample: Utility module with style and readability problems."""

def f(x,y,z,a,b,c,d,e):
    return ((x+y)*z-a)/b+c*d-e

class dataProcessor:
    def __init__(self):
        self.d = []
        self.r = None
        self.t = 0

    def doStuff(self, input):
        self.d = input
        self.r = []
        for i in range(len(self.d)):
            if self.d[i] != None:
                if self.d[i] != "":
                    if len(self.d[i]) > 0:
                        self.r.append(self.d[i].strip())
        self.t = len(self.r)
        return self.r

    def Process(self, data, flag1, flag2, flag3, mode, output_type, verbose, strict):
        result = []
        if flag1:
            for item in data:
                result.append(item.upper())
        if flag2:
            temp = []
            for item in result:
                if item not in temp:
                    temp.append(item)
            result = temp
        if flag3:
            result = sorted(result)
        if mode == "reverse":
            result = result[::-1]
        if output_type == "string":
            result = ",".join(result)
        if verbose:
            print(result)
        if strict:
            assert len(result) > 0
        return result

def calc(n):
    # calculate something
    x = n * 2
    x = x + 10
    x = x / 2
    x = x - 5
    # more calculation
    y = x * x
    y = y + x
    y = y - 1
    return y

import os, sys, json, re, time, datetime, random, math, collections, itertools

def unused_imports_example():
    return "hello"
