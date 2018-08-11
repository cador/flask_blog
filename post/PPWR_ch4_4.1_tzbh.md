+++
date = "2018-08-11"
title = "4.1特征变换"
categories = { "R语言预测实战":["chapter4"] }
tags = {"common":["R语言",特征变换"]}
+++

[boys Data 数据下载](/article/boys_data)

# 概念分层

这里使用荷兰男孩的身体发育数据boys Data，通过编写R代码说明概念分层的使用方法，代码如下:
```R
#加载数据集，这里使用荷兰男孩的身体发育数据boysData
boysData<-read.csv("boys.csv")
head(boysData)
```
```R
##     age  hgt   wgt   bmi   hc  gen  phb tv   reg
## 1 0.035 50.1 3.650 14.54 33.7 <NA> <NA> NA south
## 2 0.038 53.5 3.370 11.77 35.0 <NA> <NA> NA south
## 3 0.057 50.0 3.140 12.56 35.2 <NA> <NA> NA south
## 4 0.060 54.5 4.270 14.37 36.7 <NA> <NA> NA south
## 5 0.062 57.5 5.030 15.21 37.3 <NA> <NA> NA south
## 6 0.068 55.5 4.655 15.11 37.0 <NA> <NA> NA south
```
```R
summary(boysData)
```
```R
##       age              hgt              wgt              bmi       
##  Min.   : 0.035   Min.   : 50.00   Min.   :  3.14   Min.   :11.77  
##  1st Qu.: 1.581   1st Qu.: 84.88   1st Qu.: 11.70   1st Qu.:15.90  
##  Median :10.505   Median :147.30   Median : 34.65   Median :17.45  
##  Mean   : 9.159   Mean   :132.15   Mean   : 37.15   Mean   :18.07  
##  3rd Qu.:15.267   3rd Qu.:175.22   3rd Qu.: 59.58   3rd Qu.:19.53  
##  Max.   :21.177   Max.   :198.00   Max.   :117.40   Max.   :31.74  
##                   NA's   :20       NA's   :4        NA's   :21     
##        hc          gen        phb            tv           reg     
##  Min.   :33.70   G1  : 56   P1  : 63   Min.   : 1.00   city : 73  
##  1st Qu.:48.12   G2  : 50   P2  : 40   1st Qu.: 4.00   east :161  
##  Median :53.00   G3  : 22   P3  : 19   Median :12.00   north: 81  
##  Mean   :51.51   G4  : 42   P4  : 32   Mean   :11.89   south:191  
##  3rd Qu.:56.00   G5  : 75   P5  : 50   3rd Qu.:20.00   west :239  
##  Max.   :65.00   NA's:503   P6  : 41   Max.   :25.00   NA's :  3  
##  NA's   :46                 NA's:503   NA's   :522
```
```R
#这里根据BMI指数，将泛化成体重类型的wtype字段
#通过summary的结果得知bmi字段存在21个缺失值与总量748相比远小于5%，这里将其删除
boysData<-boysData[!is.na(boysData$bmi),]
#设置变换规则
typeUp<-c(18.5,24.99,25,28,32,100)
typeDown<-c(0,18.5,20,25,28,32)
typeName<-c("过轻","正常","适中","过重","肥胖","非常肥胖")
boysData$wtype<-typeName[unlist(mapply(function(x){
    tmp<-intersect(which(typeDown<x),which(typeUp>=x))
    #如果同时满足正常和适中，则默认为适中
    return(tmp[length(tmp)])
},boysData$bmi))]
head(boysData)
```
```R
##     age  hgt   wgt   bmi   hc  gen  phb tv   reg wtype
## 1 0.035 50.1 3.650 14.54 33.7 <NA> <NA> NA south  过轻
## 2 0.038 53.5 3.370 11.77 35.0 <NA> <NA> NA south  过轻
## 3 0.057 50.0 3.140 12.56 35.2 <NA> <NA> NA south  过轻
## 4 0.060 54.5 4.270 14.37 36.7 <NA> <NA> NA south  过轻
## 5 0.062 57.5 5.030 15.21 37.3 <NA> <NA> NA south  过轻
## 6 0.068 55.5 4.655 15.11 37.0 <NA> <NA> NA south  过轻
```
```R
barplot(table(boysData$wtype),col=rainbow(9),border='gray')
```
![image](/images/2018-08-11-10-31)
