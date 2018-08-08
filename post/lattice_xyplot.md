+++
date = "2018-08-01"
title = "lattice绘图系列：xyplot"
categories = { "R语言系列":["lattice"] }
tags = {"标签":["R语言","lattice"]}
+++

<span id='home'></span>

&#9702;&nbsp;[函数原型](#hsyx)
&#9702;&nbsp;[参数说明](#cssm)
&#9702;&nbsp;[绘图案例](#htal)
&emsp;&emsp;&bull;&nbsp;[分析iris数据](#fxirissj)
&emsp;&emsp;&bull;&nbsp;[分析mtcars数据](#fxmtcarssj)
&emsp;&emsp;&bull;&nbsp;[分析states数据](#fxstatessj)
&emsp;&emsp;&bull;&nbsp;[分析gapminder数据](#fxgapmindersj)

<span id='hsyx'></span>
# [函数原型](#home)

```R
xyplot(x,
       data,
       allow.multiple = is.null(groups) || outer,
       outer = !is.null(groups),
       auto.key = FALSE,
       aspect = "fill",
       panel = lattice.getOption("panel.xyplot"),
       prepanel = NULL,
       scales = list(),
       strip = TRUE,
       groups = NULL,
       xlab,
       xlim,
       ylab,
       ylim,
       drop.unused.levels = lattice.getOption("drop.unused.levels"),
       ...,
       lattice.options = NULL,
       default.scales,
       default.prepanel = lattice.getOption("prepanel.default.xyplot"),
       subscripts = !is.null(groups),
       subset = TRUE)
```
<span id='cssm'></span>
# [参数说明](#home)

- x
x表示描述初始变量与可选条件变量的公式，形如y ~ x | g1 * g2 * ...或者 y ~ x | g1 + g2 + ...。这里的x与y是初始变量，g1、g2等是可选条件变量。该公式的意思是以x为横轴，以y为纵轴绘制图形，在设置条件变量g1、g2等的情况下，需要按g1、g2等条件变量的分组来绘制y与x的图形。如果给定的公式是y ~ x，则条件变量可忽略，函数将会在一个面板上使用所有数据绘制图形。公式中仍然可以使用sqrt()、log()等表达。

- data
表示包含以上公式中变量的data.frame对象，如果使用了groups和subset参数，其使用的变量也应该包含在该data.frame对象中。如果变量没有在data中指定或者没有批定data，这些变量将会从公式所在内存环境中寻找。

- allow.multiple
逻辑值，默认为TRUE，当公式中y1+y2作为一个和出现时，应该将参数设置为FALSE，或者使用I(y1+y2)。

- outer
逻辑值，默认为FALSE，用于控制扩展的公式接口。

- auto.key
逻辑值，或者是作为simpleKey函数的参数使用成分的列表，auto.key=TRUE等价于auto.key=list()，如果此时groups参数也设置了的话，函数将同时绘制配套的图例。以list的形多，auto.key可以修改默认产生的图例。比如auto.key=list(columns=2)将会把创建的一个图例分割成两列。

- aspect
该参数控制着面板的物理形状比例（单个图片长宽比），对所有面板通常是一样的。它可以通常一个比率或字符串来指定。如果设置为字符串，默认为"fill"，该设置将尽可能最大地绘制面板以填满可用的空间。如果设置为"xy"，它将基于45度banking rule计算面板比率。如果设置为"iso"，它将对双轴进行同标度处理。

- panel
panel函数，当数据按不同分组变量切分成不同子集之后，对应的x与y变量会传给不同的面板。实际绘制是通过指定panel函数来实现的。该参数可以是一个函数对象，或者一个预定义函数的名称。每一个高级函数都有它默认的panel函数，通常以"panel."+对应的高级函数名称，比如panel.xyplot或panel.barchart等等。

- prepanel
预处理函数，使用与panel相同的参数，并返回一个列表，可能包含xlim，ylim,dx,dy等。如果没有，则使用默认值。

- scales
list对象，决定x、y轴绘制的样式。

- groups 
data中的变量或表达式，作为划分各面板的分组变量。当groups指定后，subscripts会传给panel函数进行处理。

- xlab
x轴标签

- xlim
x轴值的范围

- ylab
y轴标签

- ylim
y轴值的范围

- drop.unused.levels
是否删除未使用的因子水平。

- lattice.options
能够用于lattice.options的list对象，这些选项在函数调用期间临时生效，函数调用完成后又会回到之前的设置。这些选项与对象一起保留，并在绘图期间重用。

- default.scales
为某高级函数给定scales默认值的list对象

- default.prepanel
当prepanel参数没有指定时，通常该参数可设置的函数或函数名称的字符串。

- subset
计算结果为逻辑或整数索引向量的表达式。

<span id='htal'></span>
# [绘图案例](#home)
<span id='fxirissj'></span>
### [分析iris数据](#home)

```R
library(lattice)
xyplot(Sepal.Length + Sepal.Width ~ Petal.Length + Petal.Width | Species,
       data = iris, scales = "free", layout = c(2, 2),
       auto.key = list(x = .6, y = .7, corner = c(0, 0)))
```
![image](/images/2018.4.13.1)

```R
xyplot(Sepal.Length ~ Petal.Length, data = iris,
       type = c("p", "g", "smooth"),
       xlab = "Sepal.Length", ylab = "Petal.Length")
```
![image](/images/2018.4.14.5)

```R
xyplot(Sepal.Length ~ Petal.Length | Species, 
       group = Species, data = iris,
       type = c("p", "smooth"),
       scales = "free")
```
![image](/images/2018.4.14.6)

<span id='fxmtcarssj'></span>
### [分析mtcars数据](#home)

```R
library(lattice)
#equal.count 将会把连续型变量x分割到区间中
displacement <- equal.count(mtcars$disp,number = 3,overlap = 0)

#自定义panel函数，定制绘图内容
#panel.xyplot()函数生成了填充圆圈（pch = 19）的散点图
#panel.rug()函数在每个面板的x轴和y轴上添加了轴须线，panel.rug(x, FALSE)或panel.rug(FALSE, y)将分别只对横轴或纵轴添加轴须
#panel.grid()函数添加了水平和竖直的网格线（使用负数强制它们与轴标签对齐）
#panel.lmline()函数添加了一条红色的（col="red"）、标准粗细（lwd = 1）的虚线（lty = 2）回归线

mypanel <- function(x,y){
  panel.xyplot(x,y,pch = 19)
  panel.rug(x,y)
  panel.grid(h = -1, v = -1)
  panel.lmline(x,y,col = "red", lwd = 1,lty = 2)

}

xyplot(mpg ~ wt|displacement, data = mtcars,
       layout = c(3,1),aspect = 1.5,panel = mypanel,
       main = "Miles per Gallon vs Weight by Engin Displacesment",xlab = "Weight",ylab = "Miles per Gallon")
```
![image](/images/2018.4.13.2)
如图所示，橙色的条形部分表示按disp划分的区间

```R
library(lattice)
#手动和自动档车辆油耗与排量的关系
mtcars$transmission <- factor(mtcars$am,levels = c(0,1),labels = c("Automatic","Manual"))
panel.smoother <- function(x,y){
  panel.grid(h = -1,v = -1)
  panel.xyplot(x,y)
  #添加平滑拟合曲线
  panel.loess(x,y)
  #添加水平均值线
  panel.abline(h = mean(y) , lwd = 2,lty = 2,col = "green")
}  

xyplot(mpg~disp|transmission,data = mtcars,scales = list(cex = .8,col = "red"),
       panel = panel.smoother,
       xlab = "Displacement",ylab = "Miles per Gallon",
       main = "MGP vs Displacement by Transmission Type",
       sub = "Dotted lines are Group Means",aspect = 1)
```
![image](/images/2018.4.14.1)

<span id='fxstatessj'></span>
### [分析states数据](#home)

```R
library(lattice)
states <- data.frame(state.x77,
                     state.name = dimnames(state.x77)[[1]],
                     state.region = state.region)
xyplot(Murder ~ Population | state.region, data = states,
       groups = state.name,
       panel = function(x, y, subscripts, groups) {
           ltext(x = x, y = y, labels = groups[subscripts], cex=1)
       }) 
```
![image](/images/2018.4.14.2)

<span id='fxgapmindersj'></span>
### [分析gapminder数据](#home)

1. 读入数据
```R
## 从URL导入数据
gdURL <- "http://www.stat.ubc.ca/~jenny/notOcto/STAT545A/examples/gapminder/data/gapminderDataFiveYear.txt"
gDat <- read.delim(file = gdURL)
```
2. 数据完整性检查
```R
str(gDat)
```
```R
## 'data.frame':    1704 obs. of  6 variables:
##  $ country  : Factor w/ 142 levels "Afghanistan",..: 1 1 1 1 1 1 1 1 1 1 ..
##  $ year     : int  1952 1957 1962 1967 1972 1977 1982 1987 1992 1997 ...
##  $ pop      : num  8425333 9240934 10267083 11537966 13079460 ...
##  $ continent: Factor w/ 5 levels "Africa","Americas",..: 3 3 3 3 3 3 3 3 ..
##  $ lifeExp  : num  28.8 30.3 32 34 36.1 ...
##  $ gdpPercap: num  779 821 853 836 740 ...
```
3. 删除只有两个国家的Oceania
```R
## 删除 Oceania
jDat <- droplevels(subset(gDat, continent != "Oceania"))
str(jDat)
```
```R
## 'data.frame':    1680 obs. of  6 variables:
##  $ country  : Factor w/ 140 levels "Afghanistan",..: 1 1 1 1 1 1 1 1 1 1 ..
##  $ year     : int  1952 1957 1962 1967 1972 1977 1982 1987 1992 1997 ...
##  $ pop      : num  8425333 9240934 10267083 11537966 13079460 ...
##  $ continent: Factor w/ 4 levels "Africa","Americas",..: 3 3 3 3 3 3 3 3 ..
##  $ lifeExp  : num  28.8 30.3 32 34 36.1 ...
##  $ gdpPercap: num  779 821 853 836 740 ...
```
4. 按continent分组，分析lifeExp和gdpPercap的关系
```R
library(lattice)
xyplot(lifeExp ~ gdpPercap, jDat,
       grid = TRUE,
       scales = list(x = list(log = 10, equispaced.log = FALSE)),
       group = continent, auto.key = list(columns = nlevels(jDat$continent)),
       type = c("p", "smooth"), lwd = 4)
```
![image](/images/2018.4.14.3)
```R
xyplot(lifeExp ~ gdpPercap | continent, jDat,
       grid = TRUE, group = continent,
       scales = list(x = list(log = 10, equispaced.log = FALSE)),
       type = c("p", "smooth"), lwd = 4)
```
![image](/images/2018.4.14.4)

