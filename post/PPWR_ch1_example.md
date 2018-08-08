+++
date = "2018-08-08"
title = "R语言预测初步"
categories = { "R语言预测实战":["Chapter1"] }
tags = {"common":["R语言","预测"]}
+++

本例使用forecast包中自带的数据集wineind，它表示从1980年1月到1994年8月，由葡萄酒生产商销售的容量不到1升的澳大利亚酒的总量。
数据如下：
```R
library(forecast)
wineind
```
```R
#       Jan   Feb   Mar   Apr   May   Jun   Jul   Aug   Sep   Oct   Nov   Dec
#1980 15136 16733 20016 17708 18019 19227 22893 23739 21133 22591 26786 29740
#1981 15028 17977 20008 21354 19498 22125 25817 28779 20960 22254 27392 29945
#1982 16933 17892 20533 23569 22417 22084 26580 27454 24081 23451 28991 31386
#1983 16896 20045 23471 21747 25621 23859 25500 30998 24475 23145 29701 34365
#1984 17556 22077 25702 22214 26886 23191 27831 35406 23195 25110 30009 36242
#1985 18450 21845 26488 22394 28057 25451 24872 33424 24052 28449 33533 37351
#1986 19969 21701 26249 24493 24603 26485 30723 34569 26689 26157 32064 38870
#1987 21337 19419 23166 28286 24570 24001 33151 24878 26804 28967 33311 40226
#1988 20504 23060 23562 27562 23940 24584 34303 25517 23494 29095 32903 34379
#1989 16991 21109 23740 25552 21752 20294 29009 25500 24166 26960 31222 38641
#1990 14672 17543 25453 32683 22449 22316 27595 25451 25421 25288 32568 35110
#1991 16052 22146 21198 19543 22084 23816 29961 26773 26635 26972 30207 38687
#1992 16974 21697 24179 23757 25013 24019 30345 24488 25156 25650 30923 37240
#1993 17466 19463 24352 26805 25236 24735 29356 31234 22724 28496 32857 37198
#1994 13652 22784 23565 26323 23779 27549 29660 23356  
```
从数据中可知，这是典型的时间序列数据，一行表示一年，12列表示一年的12个月，按顺序整理的数据。将时间序列数据进行绘制，得到下图。
![image](/images/Ts010808)
从图中明显可以看出，该时间序列数据呈明显地周期性变化。

## 数据读入及处理
加载forecast包，使用自带数据集wineind。使用ACF函数查看wineind数据的自相关性，代码如下:
```R
acf(wineind,lag.max = 100)
```
得到自相关性分析图表，如下：
![image](/images/Ts01acf0808)
红点部分为自相关性比较明显的位置，可以初步使用近1、4、6、8、12期的数值建立指标，作为预测基础数据。另外，通过观察确定wineind的数据周期为一年，将1980年到1993年每年按月的曲线图在一张图中，进一步观察，相应代码为：
```R
#观察曲线簇
N <- length(wineind)
years <- ceiling(N/12)
index <- rep(1:years,rep(12,years))[1:N]
plot(1:12,ylim=range(wineind)+c(-100,100),col='white', xlab="Month", ylab="Sales")
lapply(1:years,function(year){
    points(wineind[index == year])
    lines(wineind[index == year],lty=2)
})
```
![image](/images/Ts010343x)
由图可知，月份与销量线性关系明显，应该考虑进建模基础数据，用于预测。至此，需要将wineind的原始数据，处理成如下格式，输出建模基础数据集。

## 基础数据集属性定义
 - ID	
 > 唯一标识,R语言自动生成
 - Month	
 > 预测月月份
 - DstValue	
 > 预测月销量
 - RecentVal1	
 > 近1月销量
 - RecentVal4	
 > 近4月销量
 - RecentVal6	
 >近6月销量
 - RecentVal8	
 >近8月销量
 - RecentVal12	
 >近12月销量,去年同期

数据转换的代码如下：
```R
#对数据按指定格式进行转换
Month=NULL
DstValue=NULL
RecentVal1=NULL
RecentVal4=NULL
RecentVal6=NULL
RecentVal8=NULL
RecentVal12=NULL
#替换掉太大或太小的值
wineind[wineind<18000]=18000
wineind[wineind>38000]=38000
for(i in (12+1):(length(wineind)-1))
{
  Month<-c(Month,i%%12+1)
  DstValue<-c(DstValue, wineind[i+1])
  RecentVal1<-c(RecentVal1,wineind[i])
  RecentVal4<-c(RecentVal4,wineind[i-3])
  RecentVal6<-c(RecentVal6,wineind[i-5])
  RecentVal8<-c(RecentVal8,wineind[i-7])
  RecentVal12<-c(RecentVal12,wineind[i-11])
}
preData=data.frame(Month,DstValue,RecentVal1,RecentVal4,RecentVal6,RecentVal8,RecentVal12)
head(preData)
```
```R
##   Month DstValue RecentVal1 RecentVal4 RecentVal6 RecentVal8 RecentVal12
## 1     2    18000      18000      22591      23739      19227       18000
## 2     3    20008      18000      26786      21133      22893       20016
## 3     4    21354      20008      29740      22591      23739       18000
## 4     5    19498      21354      18000      26786      21133       18019
## 5     6    22125      19498      18000      29740      22591       19227
## 6     7    25817      22125      20008      18000      26786       22893
```
```R
#画出散点矩阵图
plot(preData)
```
![image](/images/Ts03209dfsa)
注意到第二行最后一列的图中，有两个孤立点，在建模之前需要去掉这两个点，因为这样杠杆点很影响线性模型的建模效果。建立DstValue与RecentVal12的线性模型，通过cooks.distance函数计算每行记录对模拟的影响度量，代码如下：
```R
#使用DstValue与RecentVal12拟合线性模型
lm.fit=lm(DstValue~RecentVal12,data=preData)
cook<-cooks.distance(lm.fit)
plot(cook)
abline(h=0.15,lty=2,col='red')
```
![image](/images/Ts0342jkljfkldja)
如图，存在两个明显的杠杆点，需要进行分离。代码如下：
```R
cook[cook>0.15]
##        79       123 
## 0.1706335 0.2433219
#去掉79和123行记录
preData=preData[-c(123,79),]
```
## 建立模型
根据上一步输出的基础数据，提取150行作为训练数据，剩下的数据作为测试数据。数据分割及建模的代码如下：
```R
#分离训练集与测试集
trainData=preData[1:150,]
testData=preData[151:163,]

#建立模型
lm.fit<-lm(DstValue~Month+RecentVal1+RecentVal4+RecentVal6+RecentVal8+RecentVal12,data=trainData)
summary(lm.fit)
```
```R
# Call:
# lm(formula = DstValue ~ Month + RecentVal1 + RecentVal4 + RecentVal6 + 
#    RecentVal8 + RecentVal12, data = trainData)
#
# Residuals:
#     Min      1Q  Median      3Q     Max 
# -4806.5 -1549.1  -171.8  1368.7  6763.3 
#
#Coefficients:
#              Estimate Std. Error t value Pr(>|t|)    
#(Intercept)  2.214e+03  1.987e+03   1.114  0.26714    
#Month        3.855e+02  8.955e+01   4.305 3.08e-05 ***
#RecentVal1  -2.964e-03  3.354e-02  -0.088  0.92971    
#RecentVal4   7.227e-02  3.567e-02   2.026  0.04463 *  
#RecentVal6  -1.825e-02  3.759e-02  -0.486  0.62804    
#RecentVal8   1.123e-01  3.903e-02   2.876  0.00464 ** 
#RecentVal12  6.701e-01  5.921e-02  11.316  < 2e-16 ***
#---
#Signif. codes:  
#0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
#
#Residual standard error: 1989 on 143 degrees of freedom
#Multiple R-squared:  0.848,	Adjusted R-squared:  0.8416 
#F-statistic:   133 on 6 and 143 DF,  p-value: < 2.2e-16
```









#分离训练集与测试集
trainData=preData[1:150,]
testData=preData[151:163,]

#建立模型
lm.fit<-lm(DstValue~Month+RecentVal1+RecentVal4+RecentVal6+RecentVal8+RecentVal12,data=trainData)
summary(lm.fit)

#对Month、RecentVal4、RecentVal8三个变量按5次多项式进行衍生
lm.fit<-lm(DstValue~Month+I(Month^2)+I(Month^3)+I(Month^4)+I(Month^5)+ RecentVal1+RecentVal4+I(RecentVal4^2)+I(RecentVal4^3)+I(RecentVal4^4)+I(RecentVal4^5)+ RecentVal6+RecentVal8+I(RecentVal8^2)+I(RecentVal8^3)+I(RecentVal8^4)+I(RecentVal8^5)+ RecentVal12,data=trainData)
summary(lm.fit)

#由于涉及到变量太多，使用逐步回归删除掉影响小的变量
lm.fit<-step(lm.fit)
summary(lm.fit)

lm.fit<-lm(formula = DstValue ~ Month + I(Month^4) + I(Month^5) + RecentVal6 + 
             RecentVal8 + I(RecentVal8^2) + I(RecentVal8^3) + I(RecentVal8^4) + 
             I(RecentVal8^5) + RecentVal12, data = trainData)
summary(lm.fit)

#对新数据进行预测
testData$pred=predict(lm.fit,testData)
#计算百分误差率
testData$diff=abs(testData$DstValue-testData$pred)/testData$DstValue
testData

summary(testData)