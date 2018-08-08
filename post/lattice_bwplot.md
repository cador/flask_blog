+++
date = "2018-08-01"
title = "lattice绘图系列：bwplot"
categories = { "R Language Series":["lattice"] }
tags = {"common":["R语言","lattice"]}
+++

<span id='home'></span>

&#9702;&nbsp;[函数原型](#hsyx)
&#9702;&nbsp;[参数说明](#cssm)
&#9702;&nbsp;[绘图案例](#htal)
&emsp;&emsp;&bull;&nbsp;[分析ToothGrowth数据](#fxtoothgrowthdata)
&emsp;&emsp;&bull;&nbsp;[两因素分组](#lysfz)



<span id='hsyx'></span>
# [函数原型](#home)

```R
bwplot(x,
       data,
       allow.multiple = is.null(groups) || outer,
       outer = FALSE,
       auto.key = FALSE,
       aspect = "fill",
       panel = lattice.getOption("panel.bwplot"),
       prepanel = NULL,
       scales = list(),
       strip = TRUE,
       groups = NULL,
       xlab,
       xlim,
       ylab,
       ylim,
       box.ratio = 1,
       horizontal = NULL,
       drop.unused.levels = lattice.getOption("drop.unused.levels"),
       ...,
       lattice.options = NULL,
       default.scales,
       default.prepanel = lattice.getOption("prepanel.default.bwplot"),
       subscripts = !is.null(groups),
       subset = TRUE)
```
<span id='cssm'></span>
# [参数说明](#home)

- x
表示描述初始变量与可选条件变量的公式，形如y ~ x | g1 * g2 * ...或者 y ~ x | g1 + g2 + ...。这里的x与y是初始变量，g1、g2等是可选条件变量。该公式的意思是以x为横轴，以y为纵轴绘制图形，在设置条件变量g1、g2等的情况下，需要按g1、g2等条件变量的分组来绘制y与x的图形。如果给定的公式是y ~ x，则条件变量可忽略，函数将会在一个面板上使用所有数据绘制图形。公式中仍然可以使用sqrt()、log()等表达。

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

- strip
逻辑值或一个函数，如果设置为FALSE，绘图的时候不会画条带，否则条带将使用strip函数来绘制，默认是strip.default。

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

- box.ratio
用于确定长方形的宽度对应内部长方形空间的比例。

- horizontal
逻辑值，指定使用x或y作为一个因子。如果设置为TRUE，则是y,否则是x。默认为FALSE。

- drop.unused.levels
是否删除未使用的因子水平。

- lattice.options
能够用于lattice.options的list对象，这些选项在函数调用期间临时生效，函数调用完成后又会回到之前的设置。这些选项与对象一起保留，并在绘图期间重用。

- default.scales
为某高级函数给定scales默认值的list对象。

- default.prepanel
当prepanel参数没有指定时，通常该参数可设置的函数或函数名称的字符串。


- subscripts
逻辑值，用于确定命名为subscripts的向量是否传给panel函数，默认是FALSE。

- subset
计算结果为逻辑或整数索引向量的表达式。

<span id='htal'></span>
# [绘图案例](#home)
<span id='fxtoothgrowthdata'></span>
### [分析ToothGrowth数据](#home)
1. 数据说明<br>
该数据包含在datasets包中，记录了60只豚鼠的实验数据，主要有三个指标：len(成牙质细胞的长度)、supp(补充物类型，两种补充物分别为VC、OJ)、dose（剂量）
2. 将dose转正因子类型

```R
ToothGrowth$dose <- as.factor(ToothGrowth$dose)
head(ToothGrowth)
```
```R
##    len supp dose
## 1  4.2   VC  0.5
## 2 11.5   VC  0.5
## 3  7.3   VC  0.5
## 4  5.8   VC  0.5
## 5  6.4   VC  0.5
## 6 10.0   VC  0.5
```
3. 分析不同dose对应len的分布特征

```R
library(lattice)
bwplot(len ~ dose,  data = ToothGrowth,
       xlab = "Dose", ylab = "Length")
```
![image](/images/2018.4.14.7)


```R
library(lattice)
bwplot(len ~ dose,  data = ToothGrowth,
       panel = panel.violin,
       xlab = "Dose", ylab = "Length")
```
![image](/images/2018.4.14.8)
4. 按不同的dose分组，不同supp下的len分布特征

```R
library(lattice)
bwplot(len ~ supp | dose,  data = ToothGrowth,
       layout = c(3, 1),
       xlab = "Dose", ylab = "Length")
```
![image](/images/2018.4.14.9)

```R
library(lattice)
bwplot(len ~ supp | dose,  data = ToothGrowth,
       layout = c(3, 1), panel = panel.violin,
       xlab = "Dose", ylab = "Length")
```
![image](/images/2018.4.14.10)

<span id='lysfz'></span>
### [两因素分组](#home)
1. 构建数据集

```R
mydat <- data.frame(response=rnorm(400,mean=1),
         p = factor(sample(rep(1:4,each=100))),
         sub = factor(rep(sprintf("sub%i",1:4),each=100)), 
         seas=factor(rep(sprintf("seas%i",1:4),100)))
head(mydat)
```

```R
##    response p  sub  seas
## 1 2.0645807 3 sub1 seas1
## 2 1.2292406 3 sub1 seas2
## 3 0.1485345 2 sub1 seas3
## 4 0.5620492 2 sub1 seas4
## 5 2.8343915 3 sub1 seas1
## 6 1.4003081 1 sub1 seas2
```

```R
library(lattice)
cbPalette <- c("#F0E442", "#0072B2", "#D55E00", "#CC79A7")
bwout = bwplot(response~factor(p)|factor(sub)+factor(seas),data=mydat,
    par.settings = list(strip.background=list(col = c("skyblue","gold"))),
    fill = cbPalette,xlab="xlab",ylab="ylab")
bwout
```
![image](/images/2018.4.14.11)

```R
useOuterStrips(bwout)
```
![image](/images/2018.4.14.12)

