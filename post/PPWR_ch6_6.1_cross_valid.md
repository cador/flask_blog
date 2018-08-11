+++
date = "2018-08-11"
title = "6.1交叉验证"
categories = { "R语言预测实战":["ch06"] }
tags = {"common":["R语言","交叉验证"]}
+++

这里使用R语言实现分割样本的函数sampleSplit，代码如下：
```R
#本函数实现对样本的分割
#df:data.frame对象
#k:分割数量
#return:带有I_kvalue属性的完整数据集
sampleSplit <- function(df,k)
{
    df$I_kvalue <- sample(1+((1:dim(df)[1])%%k),dim(df)[1])
    return(df)
}
out=sampleSplit(iris,k=10)
table(out$I_kvalue)
```
```R
##  1  2  3  4  5  6  7  8  9 10 
## 15 15 15 15 15 15 15 15 15 15
```
为了进一步说明交叉验证确认参数的过程，这里使用iris数据集，建立Sepal.Length、Sepal.Width、Petal.Width对Petal.Width的线性回归模型，代码如下：
```R
#1、使用交叉验证得到的参数
set.seed(1234)
k=10
out=sampleSplit(iris,k)
#初始化最小均方误差minError
minError=100
#初始化最佳拟合结果finalfit
finalfit=NULL
for(i in 1:k)
{
    #选择第i个子样本之外的其它所有样本作为训练集
    trainset=out[out$I_kvalue!=i,1:(dim(out)[2]-2)]
    #选择第i个子样本作为测试集
    testset=out[out$I_kvalue==i,1:(dim(out)[2]-2)]
    #拟合线性回归模型
    lm.fit=lm(Petal.Width~Sepal.Length+Sepal.Width+Petal.Length,data=trainset)
    #基于测试集得出预测结果
    testset$pred=predict(lm.fit,testset)
    #计算均方误差
    error=mean((testset$Petal.Width-testset$pred)^2)
    #判断是否最小均方误差
    if(error<minError)
    {
        minError=error
        finalfit=lm.fit
    }
}
minError
```
```R
## [1] 0.009822179
```
```R
finalfit$coefficients
```
```R
##  (Intercept) Sepal.Length  Sepal.Width Petal.Length 
##   -0.2488242   -0.1977551    0.2176520    0.5157144
```
```R
#2、使用一般方法得到的参数
lm.fit=lm(Petal.Width~Sepal.Length+Sepal.Width+Petal.Length,data=iris)
lm.fit$coefficients
```
```R
##  (Intercept) Sepal.Length  Sepal.Width Petal.Length 
##   -0.2403074   -0.2072661    0.2228285    0.5240831
```


