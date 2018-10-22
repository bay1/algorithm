# Algorithm

杂乱的算法记录

<!-- TOC -->

- [Algorithm](#algorithm)
    - [leetcode 120. 三角形最小路径和](#leetcode-120-三角形最小路径和)
        - [**要求**](#要求)
        - [**题解**](#题解)

<!-- /TOC -->

## leetcode 120. 三角形最小路径和

### **要求**

给定一个三角形，找出自顶向下的最小路径和。每一步只能移动到下一行中相邻的结点上。

例如，给定三角形：

```
[
     [2],
    [3,4],
   [6,5,7],
  [4,1,8,3]
]
```

自顶向下的最小路径和为 11（即，2 + 3 + 5 + 1 = 11）。

说明：

如果你可以只使用 O(n) 的额外空间（n 为三角形的总行数）来解决这个问题，那么你的算法会很加分。

### **题解**

```python
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

minimumTotal([[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]])
# 通过	52 ms	python3
```