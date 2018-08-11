+++
date = "2018-08-11"
title = "8.1多元线性回归"
categories = { "R语言预测实战":["ch08"] }
tags = {"common":["R语言","线性回归"]}
+++

[mm数据集下载](/download/mm)

使用vif函数计算线性模型y~x1+x2的方差膨胀因子，代码如下：
x^2

```R
# 从文件中加载M数据集
data = read.csv("f:\\mm.csv")
colnames(data) = c("y", "x1", "x2")
library(car)
vif(lm(y ~ x1 + x2, data))
```
```R
##    x1    x2 
## 35.96 35.96
```