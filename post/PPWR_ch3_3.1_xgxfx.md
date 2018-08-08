+++
date = "2018-08-09"
title = "3.1相关分析"
categories = { "R语言预测实战":["chapter3"] }
tags = {"common":["R语言","相关性"]}
+++

<span id='home'></span>
&#9702;&nbsp;[自相关分析](#zxj)
&#9702;&nbsp;[偏相关分析](#pxj)
&#9702;&nbsp;[简单相关分析](#cor)
&#9702;&nbsp;[互相关分析](#hxj)
&#9702;&nbsp;[典型相关分析](#cancor)

<span id='zxj'></span>
## [自相关分析](#home)

对airmiles数据进行自相关分析的代码如下：
```R
acf(airmiles,type='correlation',lag.max=10)
```
![image](/images/2018-08-09-06-49)
如图可知，滞后阶数为0，相关系数为1，随着滞后阶数的增加，相关系数逐渐减弱，并趋于稳定。

<span id='pxj'></span>
## [偏相关分析](#home)

对airmiles数据进行偏相关分析的代码如下：
```R
pacf(airmiles,lag.max=10)
```
![image](/images/2018-08-09-06-51)
如图可知，最小为1阶滞后，对应值为0.876，与对应的1阶自相关系数相等，随之着滞后阶数的增加（大于2阶），偏相关系数一直较小并且稳定。

<span id='cor'></span>
## [简单相关分析](#home)

散点矩阵是由变量两两组合由数据点分布图构成的矩阵，此处使用graphics包中的pairs函数绘制散点图矩阵，代码如下：
```R
pairs(~Sepal.Length+Sepal.Width+Petal.Length+Petal.Width,data=iris, main="Simple Scatterplot Matrix")
```
![image](/images/2018-08-09-06-55)
图中Petal.Length与Petal.Width对应的散点图比较接近线性，说明这两个变量的相关性较强。

接着，使用scatterplotMatrix函数绘制散点图，代码如下：
```R
library(car)
scatterplotMatrix(~Sepal.Length+Sepal.Width+Petal.Length+Petal.Width|Species, data=iris)
```
![image](/images/2018-08-09-06-59)
代码中，通过竖线指定分组变量，这里使用花色种类进行分组。对角线上的图形表示各个变量在不同花色类型下的分布情况。

如下，使用scatter3d函数绘制iris数据集的Sepal.Length，Petal.Length以及Petal.Width这三个属性在三维空间的散点图，代码如下：
```R
library(rgl)
library(car)
scatter3d(iris$Sepal.Length, iris$Petal.Length, iris$Petal.Width)
```

使用corrgram函数绘制mtcars数据的相关矩阵图，代码如下：
```R
library(corrgram)
#1、设置排序处理
corrgram(mtcars,order=TRUE)
```
![image](/images/2018-08-09-07-08)
```R
#2、设置上下三角面板形状
corrgram(mtcars,order=TRUE,lower.panel=panel.shade,upper.panel=panel.pie)
```
![image](/images/2018-08-09-07-10)
```R
#3、只显示下三角部分
corrgram(mtcars,order=TRUE,lower.panel=panel.shade,upper.panel=NULL)
```
![image](/images/2018-08-09-07-11)
```R
#4、调整面板颜色
corrgram(mtcars,order=TRUE,lower.panel=panel.shade,upper.panel=panel.pie,
         col.regions=colorRampPalette(c("darkgoldenrod4","burlywood1","white",
         "darkkhaki","darkgreen")))
```
![image](/images/2018-08-09-07-12)
使用corrplot函数绘制mtcars数据的相关矩阵图，代码如下：
```R
library(corrplot)
#1、使用不同的method绘制相关矩阵图
methods<-c("circle","square","ellipse","pie","shade","color")
par(mfrow=c(2,3))
t0=mapply(function(x){corrplot(cor(mtcars), method=x,order="AOE")},methods)
par(mfrow=c(1,1))
```
![image](/images/2018-08-09-07-15)
```R
#2、设置method=color绘制热力矩阵图
corrplot(cor(mtcars), method="color", order = "AOE",tl.col="black",tl.srt=45,
         addCoef.col="black",col=colorRampPalette(c("#7F0000","red","#FF7F00",
         "yellow","white", "cyan", "#007FFF", "blue","#00007F"))(20))
```
![image](/images/2018-08-09-07-16)
```R
#3、绘制上下三角及不同色彩的相关矩阵图
library(RColorBrewer)
par(mfrow=c(2,2))
corrplot(cor(mtcars),type="lower")
corrplot(cor(mtcars),type="lower",order="hclust",
            col=brewer.pal(n=8,name="RdYlBu"))
corrplot(cor(mtcars),type="upper",order="AOE",
            col=c("black","white"),bg="lightblue")
corrplot(cor(mtcars),type="upper",order="FPC",
            col=brewer.pal(n=8, name="PuOr"))
par(mfrow=c(1,1))
```
![image](/images/2018-08-09-07-17)
使用mtcars数据集，进行系统聚类，代码如下：
```R
d<-sqrt(1-cor(mtcars)^2)
hc<-hclust(as.dist(d))
plot(hc)
rect.hclust(hc,k=3)
```
![image](/images/2018-08-09-07-19)
我们可通过pvclust函数分析mtcars数据变量的相关性，代码如下：
```R
library(pvclust)
cluster.bootstrap <- pvclust(mtcars, nboot=1000, method.dist="correlation")
plot(cluster.bootstrap)
pvrect(cluster.bootstrap)
```
![image](/images/2018-08-09-07-21)
如图，au值即Approximately Unbiased的简写，它是通过多尺度自助重抽样法计算而来的；而bp值，即Bootstrap Probability的简写，它是通过普通自助重抽样法计算而来。函数pvrect标明了影响显著的聚类，显著的类越多，效果越好。

<span id='hxj'></span>
## [互相关分析](#home)

对airmiles和LakeHuron时序数据进行互相关分析的代码如下：
```R
ccf(airmiles,ts(LakeHuron,start=1937,end=1960),type="correlation")
```
![image](/images/2018-08-09-07-25)

<span id='cancor'></span>
## [典型相关分析](#home)

现以iris数据集为例，使用R语言说明特征值及特征向量的计算过程，代码如下：
```R
#1、提取iris的前4个数值列，并进行标准化处理
data0=scale(iris[1:4])
#2、计算这4个变量的协方差，由于经过标准化处理，这样得到的也是相关系数
M=cov(data0)
#3、将M进行分块，1:2两个变量一组，3:4是另外一组，并进行两两组合
X11=M[1:2,1:2]
X12=M[1:2,3:4]
X21=M[3:4,1:2]
X22=M[3:4,3:4]
#4、按公式求解矩阵A和B
A=solve(X11)%*%X12%*%solve(X22)%*%X21
B=solve(X22)%*%X21%*%solve(X11)%*%X12
#5、使用eigen函数求解典型相关系数如下
eV=sqrt(eigen(A)$values)
eV
```
```R
# [1] 0.9409690 0.1239369
```
```R
#6、进行验证
#...比较A与XΛX^(-1)是否相等
round(A-eigen(A)$vectors%*%diag(eigen(A)$values)%*%solve(eigen(A)$vectors),3)
```
```R
##              Sepal.Length Sepal.Width
## Sepal.Length            0           0
## Sepal.Width             0           0
```
```R
#...比较B与YΛY^(-1)是否相等
round(B-eigen(B)$vectors%*%diag(eigen(B)$values)%*%solve(eigen(B)$vectors),3)
```
```R
##              Petal.Length Petal.Width
## Petal.Length            0           0
## Petal.Width             0           0
```
```R
#...求解A对应的特征向量并计算典型向量C1
C1=data0[,1:2]%*%eigen(A)$vectors
#...验证C1对应各变量的标准差是否为1，同时查看均差
apply(C1,2,sd)
```
```R
## [1] 1.041196 0.951045
```
```R
apply(C1,2,mean)
```
```R
## [1] -4.880321e-16 -2.759430e-17
```
```R
#...由于均值为0，标准差不为1，这里对特征向量进行伸缩变换
eA=eigen(A)$vectors%*%diag(1/apply(C1,2,sd))
#...再次验证方差和均值
C1=data0[,1:2]%*%eA
apply(C1,2,sd)
```
```R
## [1] 1 1
```
```R
apply(C1,2,mean)
```
```R
## [1] -4.667693e-16 -2.745503e-17
```
```R
#...可见，特征向量已经满足要求，同理对B可得
C2=data0[,3:4]%*%eigen(B)$vectors
apply(C2,2,sd)
```
```R
## [1] 0.6291236 0.2003530
```
```R
apply(C2,2,mean)
```
```R
## [1] -1.403572e-17 -9.859870e-18
```
```R
eB=eigen(B)$vectors%*%diag(1/apply(C2,2,sd))
C2=data0[,3:4]%*%eB
apply(C2,2,sd)
```
```R
## [1] 1 1
```
```R
apply(C2,2,mean)
```
```R
# [1] -1.598186e-17  5.307097e-17
```
```R
round(cor(cbind(C1,C2)),3)
```
```R
#      [,1]  [,2]  [,3]  [,4]
#[1,] 1.000 0.000 0.941 0.000
#[2,] 0.000 1.000 0.000 0.124
#[3,] 0.941 0.000 1.000 0.000
#[4,] 0.000 0.124 0.000 1.000
```
```R
x<-as.matrix(iris[,1:2])
y<-as.matrix(iris[,3:4])
cancor(x,y)
```
```R
#$cor
#[1] 0.9409690 0.1239369
#
#$xcoef
#                    [,1]       [,2]
#Sepal.Length -0.08757435 0.04749411
#Sepal.Width   0.07004363 0.17582970
#
#$ycoef
#                    [,1]       [,2]
#Petal.Length -0.06956302 -0.1571867
#Petal.Width   0.05683849  0.3940121
#
#$xcenter
#Sepal.Length  Sepal.Width 
#    5.843333     3.057333 
#
#$ycenter
#Petal.Length  Petal.Width 
#    3.758000     1.199333 
```

