+++
date = "2018-08-11"
title = "9.1 梯度提升回归树（GBRT）"
categories = { "R语言预测实战":["ch09"] }
tags = {"common":["R语言","梯度提升"]}
+++

编写函数gbrt.build，使用训练数据以构建GBRT模型，代码如下：
```R
#建立函数构建GBRT模型
#y:响应变量
#x:输入变量数据框
#consame:当连续consame次得到的残差平方和相等时算法终止
#maxiter:迭代次数的上限
#lambda:缩放因子
gbrt.build<-function(y,x,consame=5,maxiter=1000,lambda=0.01)
{
    #加载实现二叉回归树的包
    library(rpart)
    #使平方损失函数最小化的常数值为对应数据的平均值，即以均值初始化f0
    f0<-mean(y)
    #初始化变量
    rss<-NULL
    gbrt.model.list<-list(f0=f0)
    #进入循环，当连续consame次，得到的残差平方和相等或超过最大迭代次数时终止算法
    for(m in 1:maxiter)
    {
        #计算负梯度，当损失函数为平方损失函数时，负梯度即为残差
        revals<-y-f0
        #根据残差学习一棵回归树，设置分割点满足的最小样本量为10
        rpart.mod<-rpart(
            formula(paste("revals~",paste(colnames(x),collapse="+"),sep="")),
            data=x,control=rpart.control(minsplit=10))
        #更新回归树，并生成估计结果
        gbrt.model.list=append(gbrt.model.list,list(rpart.mod))
        names(gbrt.model.list)[m+1]=paste("f",m,sep="")
        f0=f0+lambda*predict(rpart.mod,x)
        #统计残差平方和
        rss=c(rss,sum((f0-y)^2))
        #判断是否满足终止条件
        n<-length(rss)
        if(n>=consame && sd(rss[(n-consame+1):n])==0)break
    }
    return(list(m=m,rss=rss,gml=gbrt.model.list))
}

#准备基础数据
vdata=iris[,1:4]
colnames(vdata)=c("x1","x2","x3","y")
out=gbrt.build(vdata$y,vdata[,1:3])
#查看rss的统计信息
summary(out$rss)
```
```R
##    Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
##   1.362   1.688   3.189  11.700  12.200  84.960
```
```R
#根据rss绘制曲线，以直观观察残差平方和的变化趋势
plot(out$rss,type='l',xlab="迭代次数",lwd=2,col='blue',ylab='RSS')
abline(h=0,col='red',lwd=2,lty=2)
```
![image](/images/2018-08-11-16-24)
如图，随着迭代次数的增加，残差平方和RSS快速减小，并趋于平稳，且接近于0，在迭代450次左右时算法收敛并终止。
现使用R语言编写预测函数gbrt.predict，其可对新数据进行预测，代码如下：
```R
#建立预测函数，对新数据进行预测
#newdata:进行预测的新数据
#gml:即gbrt.model.list，它是GBRT的模型
#lambda:训练模型时，指定的lamda参数
gbrt.predict<-function(newdata,gml,lambda=0.01)
{
    n=length(gml)
    f0=gml[[1]]
    for(k in 2:n)
    {
        f0=f0+lambda*predict(gml[[k]],newdata)
    }
    names(f0)=NULL
    return(f0)
}

newdata=vdata[,1:4]
newdata$pred=gbrt.predict(newdata,out$gml)
sum((newdata$y-newdata$pred)^2)
```
```R
## [1] 1.362449
```
从输出结果可知，最终使用GBRT算法得到的残差平方和为1.362449

现基于R中的iris数据集，尝试使用gbm函数建立Sepal.Length、Sepal.Width、Petal.Length对Petal.Width的回归模型，代码如下：
```R
library(gbm)
#基础数据准备
vdata=iris[,1:4]
colnames(vdata)=c("x1","x2","x3","y")
#建立gbm模型
gbm.obj<-gbm(y~x1+x2+x3,data=vdata,distribution='gaussian',
             var.monotone=c(0,0,0),
             n.trees=1000,
             shrinkage=0.01,
             interaction.depth=5,
             bag.fraction=0.5,
             cv.folds=10)
#用交叉验证确定最佳迭代次数
best.iter<-gbm.perf(gbm.obj,method="cv")
best.iter
```
```R
## [1] 597
```
从输出结果可知，最佳迭代次数best.iter为597。基于建立的gbm.obj对vdata进行预测，代码如下：
```R
#进行预测
vdata$pred=predict(gbm.obj,vdata,n.trees=best.iter)
#查看前6行数据
head(vdata)
```
```R
##    x1  x2  x3   y      pred
## 1 5.1 3.5 1.4 0.2 0.2653250
## 2 4.9 3.0 1.4 0.2 0.1903269
## 3 4.7 3.2 1.3 0.2 0.1804154
## 4 4.6 3.1 1.5 0.2 0.1831213
## 5 5.0 3.6 1.4 0.2 0.2462909
## 6 5.4 3.9 1.7 0.4 0.3657279
```
```R
##    x1  x2  x3   y      pred
## 1 5.1 3.5 1.4 0.2 0.2653250
## 2 4.9 3.0 1.4 0.2 0.1903269
## 3 4.7 3.2 1.3 0.2 0.1804154
## 4 4.6 3.1 1.5 0.2 0.1831213
## 5 5.0 3.6 1.4 0.2 0.2462909
## 6 5.4 3.9 1.7 0.4 0.3657279
```
```R
## [1] 3.188981
```
从输出结果可知，残差平方和为3.188981，可基于gbm.obj进一步查看参与建模的自变量的重要性，代码为：
```R
#分析变量重要性
summary(gbm.obj,n.trees=best.iter)
```
![image](/images/2018-08-11-16-34)
```R
#   var   rel.inf
#x3  x3 96.658713
#x2  x2  1.899809
#x1  x1  1.441477
```
可见，变量x3对预测结果影响最大，变量x1和x2对预测结果的影响很小。另外，当参与建模的特征维度很大时，可以使用这种方式进行特征选择。
此外，可通过绘制边际图，查看各变量取某个值时，一点小扰动对响应变量的影响，代码如下：
```R
#绘制各变量的边际图
par(mfrow=c(1,3))
plot(gbm.obj,1,best.iter)
plot(gbm.obj,2,best.iter)
plot(gbm.obj,3,best.iter)
par(mfrow=c(1,1))
```
![image](/images/2018-08-11-16-36)
如上图，对于各自变量，在其它变量固定不变的情况下，当其取某个值时，并有一点小扰动时，将其对响应变量的影响程度绘制成曲线。
其中，变量x1对响应变量的影响较没有规律，变量x2和x3对响应变量的边际效应较为明显。
