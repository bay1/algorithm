# -*- coding: utf-8 -*-
from tools import run_time

@run_time
def minimumTotal(triangle):
    """
    :type triangle: List[List[int]]
    :rtype: int
    """
    lenList = triangle[-1]
    for numList in triangle[-2::-1]:
        for i in range(len(numList)):
            lenList[i] = numList[i] + min(lenList[i], lenList[i+1])
    print(lenList[0])

stmt=minimumTotal([[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]])