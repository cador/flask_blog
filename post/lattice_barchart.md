+++
date = "2018-08-01"
title = "lattice绘图系列：barchart"
categories = { "R语言系列":["lattice"] }
tags = {"标签":["R语言","lattice"]}
+++

<span id='home'></span>

&#9702;&nbsp;[函数原型](#hsyx)
&#9702;&nbsp;[参数说明](#cssm)
&#9702;&nbsp;[绘图案例](#htal)
&emsp;&emsp;&bull;&nbsp;[分析mtcars数据](#fxmtcarsdata)
&emsp;&emsp;&bull;&nbsp;[分析barley数据](#fxbarleydata)
&emsp;&emsp;&bull;&nbsp;[分析diamonds数据](#fxdiamondsdata)

<span id='hsyx'></span>
# [函数原型](#home)

```R
barchart(x,
         data,
         panel = lattice.getOption("panel.barchart"),
         default.prepanel = lattice.getOption("prepanel.default.barchart"),
         box.ratio = 2,
         ...)
```
<span id='cssm'></span>
# [参数说明](#home)
- x
表示描述初始变量与可选条件变量的公式，形如y ~ x | g1 * g2 * ...或者 y ~ x | g1 + g2 + ...。这里的x与y是初始变量，g1、g2等是可选条件变量。该公式的意思是以x为横轴，以y为纵轴绘制图形，在设置条件变量g1、g2等的情况下，需要按g1、g2等条件变量的分组来绘制y与x的图形。如果给定的公式是y ~ x，则条件变量可忽略，函数将会在一个面板上使用所有数据绘制图形。公式中仍然可以使用sqrt()、log()等表达。

- data
表示包含以上公式中变量的data.frame对象，如果使用了groups和subset参数，其使用的变量也应该包含在该data.frame对象中。如果变量没有在data中指定或者没有批定data，这些变量将会从公式所在内存环境中寻找。

- panel
panel函数，当数据按不同分组变量切分成不同子集之后，对应的x与y变量会传给不同的面板。实际绘制是通过指定panel函数来实现的。该参数可以是一个函数对象，或者一个预定义函数的名称。每一个高级函数都有它默认的panel函数，通常以"panel."+对应的高级函数名称，比如panel.xyplot或panel.barchart等等。

- default.prepanel
当prepanel参数没有指定时，通常该参数可设置的函数或函数名称的字符串。

- box.ratio
用于确定长方形的宽度对应内部长方形空间的比例。

<span id='htal'></span>
# [绘图案例](#home)
<span id='fxmtcarsdata'></span>
### [分析mtcars数据](#home)

```R
library(lattice)
mtcars$cars <- rownames(mtcars)
barchart(cars ~ mpg | factor(cyl), data=mtcars,
   main="barchart",
   scales=list(cex=0.5),
   layout=c(3, 1)
)
```
![image](/images/2018.4.14.13)
<span id='fxbarleydata'></span>
### [分析barley数据](#home)

```R
barchart(yield ~ variety | site, data = barley,
         groups = year, layout = c(1,6), origin = 0,
         ylab = "Barley Yield (bushels/acre)",
         scales = list(x = list(abbreviate = TRUE,
                                minlength = 5)))
```
![image](/images/2018.4.15.1)

```R
barchart(yield ~ variety | site, data = barley,
         groups = year, main = "Bar Chart in R EXample",
         xlab = "Yield Value",  stack = TRUE,
         auto.key = list(space = "right"),
         scales = list(x = list(rot = 45)))
```
![image](/images/2018.4.15.2)


```R
barchart(yield ~ variety | site, data = barley,
         groups = year, main = "Bar Chart in R EXample",
         ylab = "Yield Value",  stack = TRUE,
         auto.key = list(space = "right"),
         scales = list(x = list(rot = 45)),
         layout = c(1,6))
```
![image](/images/2018.4.15.3)

```R
barchart(yield ~ variety | site, data = barley,
 		 main = "Bar Chart in R EXample",
         xlab = "Yield Value",  stack = TRUE,
         auto.key = list(space = "right"),
         scales = list(x = list(rot = 45)))
```
![image](/images/2018.4.15.4)
如图所示，有的条形很完整，有的条形有重叠，为何呢？<br>
这里，取几组数据来看。

```R
barley[barley$site=='University Farm' & barley$variety=='Svansota',]
```

```R
##       yield  variety year            site
## 13 35.13333 Svansota 1931 University Farm
## 73 27.43334 Svansota 1932 University Farmv
```
该数据对应上图中右下小图中的第一个条形，条形有明显重叠。
```R
barley[barley$site=='University Farm' & barley$variety=='No. 475',]
```

```R
##        yield variety year            site
## 49  24.66667 No. 475 1931 University Farm
## 109 30.00000 No. 475 1932 University Farm
```
该数据对应上图中右下小图中的第四个条形，条件无重叠。<br>
通过对比，我们可以知道，barchart在绘制图时，是按记录进行绘制的，首先会将第一个匹配的记录画上去，依次第二个、第三个...。所以，如果第二个值较大时，会覆盖掉第一个值画出来的条形。也就是说，在绘制时，需要提前做好统计，再进行绘制。
<span id='fxdiamondsdata'></span>
### [分析diamonds数据](#home)
1. 读取diamonds.small数据

```R
library(ggplot2)
data(diamonds)
diamonds.small <- diamonds[1:200, ]
head(diamonds.small)
```
```R
## # A tibble: 6 x 10
##   carat cut       color clarity depth table price     x     y     z
##   <dbl> <ord>     <ord> <ord>   <dbl> <dbl> <int> <dbl> <dbl> <dbl>
## 1 0.230 Ideal     E     SI2      61.5   55.   326  3.95  3.98  2.43
## 2 0.210 Premium   E     SI1      59.8   61.   326  3.89  3.84  2.31
## 3 0.230 Good      E     VS1      56.9   65.   327  4.05  4.07  2.31
## 4 0.290 Premium   I     VS2      62.4   58.   334  4.20  4.23  2.63
## 5 0.310 Good      J     SI2      63.3   58.   335  4.34  4.35  2.75
## 6 0.240 Very Good J     VVS2     62.8   57.   336  3.94  3.96  2.48
```
2. 分析不同颜色的钻石，其切工质量与价格的关系

```R
barchart(cut ~ price | color, data = diamonds.small)
```
![image](/images/2018.4.15.5)
3. 调整布局

```R
barchart(cut ~ price | color, data = diamonds.small,as.table = TRUE)
```
![image](/images/2018.4.15.6)
4. 使用两个条件变量

```R
barchart(cut ~ price | color + clarity, data = diamonds.small)
```
![image](/images/2018.4.15.7)
5. 自定义条形图

```R
barchart(cut ~ price | color + clarity, 
	data = diamonds.small,
	panel = function(x, y, ...) {
	panel.abline(v = min(x), lty = 2)
	panel.barchart(x, y, ..., 
		col = ifelse(y == "Premium",  "red", "blue"))
	}, 
	ylab = "quality", xlab = "price", 
	box.ratio = 1, as.table = TRUE)
```
![image](/images/2018.4.15.8)

