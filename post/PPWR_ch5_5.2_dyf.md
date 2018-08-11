+++
date = "2018-08-11"
title = "5.2单元法"
categories = { "R语言预测实战":["chapter5"] }
tags = {"common":["R语言","特征选择"]}
+++

# Pearson相关系数

使用cor.test函数，分析iris数据集中Sepal.Length与Petal.Length的相关性，同时可计算出两个变量的Pearson相关系数，代码如下：
```R
cor.test(iris$Sepal.Length,iris$Petal.Length)
```
```R
## 
##  Pearson's product-moment correlation
## 
## data:  iris$Sepal.Length and iris$Petal.Length
## t = 21.646, df = 148, p-value < 2.2e-16
## alternative hypothesis: true correlation is not equal to 0
## 95 percent confidence interval:
##  0.8270363 0.9055080
## sample estimates:
##       cor 
## 0.8717538
```
计算出来的Pearson相关系数r=0.8717538，假设检验的P值小于0.01，拒绝原假设，说明Sepal.Length与Petal.Length的相关性很强。
Pearson相关系数虽然简单好用，但是它也有缺点，就是只对线性关系敏感，如果两变量是非线性关系，会导致计算结果趋于0，代码如下：
```R
x=runif(100,-1,1)
y=x^2
plot(x,y)
```
![image](/images/2018-08-11-11-43)
```R
cor.test(x,y)
```
```R
## 
##  Pearson's product-moment correlation
## 
## data:  x and y
## t = 0.65787, df = 98, p-value = 0.5122
## alternative hypothesis: true correlation is not equal to 0
## 95 percent confidence interval:
##  -0.1318261  0.2593492
## sample estimates:
##        cor 
## 0.06630892
```
此种情况下，虽然x与y存在着一一对应的关系，但是Pearson相关系数的结果为0.06630892，趋近于0，且P值大于0.05，x与y不相关。

# 距离相关系数

下面通过一个实例，来说明距离相关系数在R语言中的使用方法。我们使用energy包中的dcor函数，针对Pearson相关系数分析非线性的情况再做一次验证，代码如下：

```R
library(energy)
x=runif(100,-1,1)
y=x^2
dcor(x,y)
```
```R
## [1] 0.5044376
```
可以看到，在使用Pearson相关系数时，相关度为0.06，而使用距离相关系数时，其相关度达到了0.5。所以针对非线性的相关问题，使用距离相关系数是比较合适的选择，但是针对线性相关的问题，Pearson相关系数还是很强大的。

# 单因素方差分析

下面使用R语言编写一个实现单因素方差分析的函数OneWayAnova，并用iris数据集中的Species作为因素，Sepal.Width作为观测值，进行单因素方差分析，代码如下：
```R
#单因素方差分析
#xdata：data.frame，至少包含因素列和指标列
#factorNo:a numeric，因素列下标
#NumNo:a numeric，指标列下标
OneWayAnova<-function(xdata,factorNo,NumNo)
{
    pnormTest<-NULL
    homoTest<-NULL
    #将因素水平对应字段转成因子类型
    xdata[,factorNo]<-as.factor(xdata[,factorNo])
    #正态性检验
    Lvls<-levels(xdata[,factorNo])
    for(i in 1:length(Lvls))
    {
        tmp<-shapiro.test(xdata[xdata[,factorNo]==Lvls[i],NumNo])
        res<-NULL
        if(tmp$p.value<0.01)
        {
            pnormTest<-c(pnormTest,paste("水平 - ",Lvls[i]," , 正态检测的P值 : ", tmp$p.value, "显著性差异，不服从正态分布。",sep=""))
        }
        else
        {
            pnormTest<-c(pnormTest,paste("水平 - ",Lvls[i]," , 正态检测的P值 : ", tmp$p.value,"差异不显著，服从正态分布。",sep=""))
        }
    }

    #方差齐性检验
    tmp<-bartlett.test(xdata[,NumNo],xdata[,factorNo])
    homoTest<-paste("方差齐性检验 - P值 : ",tmp$p.value,sep="")
    if(tmp$p.value<0.01)
    {
        homoTest<-paste(homoTest,paste("显著性差异，方差不是齐性的。",sep=""))
    }
    else
    {
        homoTest<-paste(homoTest,paste("差异不显著，方差是齐性的。",sep=""))
    }
    
    #单因素方差分析
    E<-aov(xdata[,NumNo]~xdata[,factorNo],data=xdata)
    return(list(pnormTest,homoTest,summary(E)))
}

OneWayAnova(iris,5,2)
```
```R
## [[1]]
## [1] "水平-setosa,正态检测的P值 : 0.271526393904差异不显著，服从正态分布。"    
## [2] "水平-versicolor,正态检测的P值 : 0.337995108260差异不显著，服从正态分布。"
## [3] "水平-virginica,正态检测的P值 : 0.18089604036差异不显著，服从正态分布。"  
## 
## [[2]]
## [1] "方差齐性检验 - P值 : 0.351502800415803 差异不显著，方差是齐性的。"
## 
## [[3]]
##                    Df Sum Sq Mean Sq F value Pr(>F)    
## xdata[, factorNo]   2  11.35   5.672   49.16 <2e-16 ***
## Residuals         147  16.96   0.115                   
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
```
由运行结果可知，F检验的P值小于0.01，说明Species对Sepal.Width的影响显著。

# 信息增益

R语言中，程序包discretization中的chiM和mdlp函数实现了ChihMerge和MDLP算法。此处，使用chiM函数对iris的数值型数据进行离散化处理，代码如下：
```R
library(discretization)
disc=chiM(iris,alpha=0.05)
str(disc)
```
```R
## List of 2
##  $ cutp     :List of 4
##   ..$ : num [1:3] 5.45 5.75 7.05
##   ..$ : num [1:2] 2.95 3.35
##   ..$ : num [1:3] 2.45 4.75 5.15
##   ..$ : num [1:2] 0.8 1.75
##  $ Disc.data:'data.frame':   150 obs. of  5 variables:
##   ..$ Sepal.Length: int [1:150] 1 1 1 1 1 1 1 1 1 1 ...
##   ..$ Sepal.Width : int [1:150] 3 2 2 2 3 3 3 3 1 2 ...
##   ..$ Petal.Length: int [1:150] 1 1 1 1 1 1 1 1 1 1 ...
##   ..$ Petal.Width : int [1:150] 1 1 1 1 1 1 1 1 1 1 ...
##   ..$ Species     : Factor w/ 3 levels "setosa","versicolor",..: 
##                     1 1 1 1 1 1 1 1 1 1 ...
```
```R
summary(disc$Disc.data)
```
```R
##   Sepal.Length    Sepal.Width     Petal.Length   Petal.Width   
##  Min.   :1.000   Min.   :1.000   Min.   :1.00   Min.   :1.000  
##  1st Qu.:1.000   1st Qu.:1.000   1st Qu.:1.00   1st Qu.:1.000  
##  Median :3.000   Median :2.000   Median :2.00   Median :2.000  
##  Mean   :2.247   Mean   :1.867   Mean   :2.26   Mean   :1.973  
##  3rd Qu.:3.000   3rd Qu.:2.000   3rd Qu.:3.00   3rd Qu.:3.000  
##  Max.   :4.000   Max.   :3.000   Max.   :4.00   Max.   :3.000  
##        Species  
##  setosa    :50  
##  versicolor:50  
##  virginica :50  
```
```R
head(disc$Disc.data)
```
```R
##   Sepal.Length Sepal.Width Petal.Length Petal.Width Species
## 1            1           3            1           1  setosa
## 2            1           2            1           1  setosa
## 3            1           2            1           1  setosa
## 4            1           2            1           1  setosa
## 5            1           3            1           1  setosa
## 6            1           3            1           1  setosa
```

使用R语言，编写给定U和V时的信息增益计算代码，如下:
```R
#该函数用于计算U作为信源信号、V作为接收信号时的信息增益
#u：信源信号，分类向量或因子
#v：接收信号，分类向量或因子
gains <- function(u,v)
{
    #0、预处理，将u、v强制转换成因子类型
    u <- as.factor(u)
    v <- as.factor(v)
    #1、计算u的概率向量
    u_pv <- table(u)/length(u)
    #2、计算Ent(U)
    ent_u <- (-1)*sum(u_pv*log2(u_pv))
    #3、计算v的概率向量
    v_pv <- table(v)/length(u)
    #4、计算v到u的条件概率矩阵
    v0 <- as.matrix(table(v,u))
    cpm <- v0/apply(v0,1,sum)
    #5、计算Ent(U|V)
    ent_uv <- sum(v_pv*apply(cpm,1,function(x){
                 x <- x[x>0]
                 return(-sum(x*log2(x)))
              }))
    #6、计算信息增益
    gains_uv <- (ent_u - ent_uv)
    return(gains_uv)
}
library(discretization)
disc=chiM(iris,alpha=0.05)
u=disc$Disc.data$Species
v=disc$Disc.data$Sepal.Length
out=gains(u,v)
out
```
```R
## [1] 0.7285454
```
```R
s2=disc$Disc.data$Sepal.Width
p1=disc$Disc.data$Petal.Length
p2=disc$Disc.data$Petal.Width
gains_us2=gains(u,s2)
gains_up1=gains(u,p1)
gains_up2=gains(u,p2)
gains_us2
```
```R
## [1] 0.3855963
```
```R
gains_up1
```
```R
## [1] 1.418003
```
```R
gains_up2
```
```R
## [1] 1.378403
```
使用R语言自定义求解信息增益率的函数gainsR，并计算各输入变量的信息增益率，代码如下：
```R
#该函数用于计算U作为信源信号、V作为接收信号时的信息增益率
#u：信源信号，分类向量或因子
#v：接收信号，分类向量或因子
gainsR <- function(u,v)
{
    #0、预处理，将u、v强制转换成因子类型
    u <- as.factor(u)
    v <- as.factor(v)
    #1、计算u的概率向量
    u_pv <- table(u)/length(u)
    #2、计算Ent(U)
    ent_u <- (-1)*sum(u_pv*log2(u_pv))
    #3、计算v的概率向量
    v_pv <- table(v)/length(u)
    #4、计算v到u的条件概率矩阵
    v0 <- as.matrix(table(v,u))
    cpm <- v0/apply(v0,1,sum)
    #5、计算Ent(U|V)
    ent_uv <- sum(v_pv*apply(cpm,1,function(x){
                 x <- x[x>0]
                 return(-sum(x*log2(x)))
              }))
    #6、计算Ent(V)
    ent_v <- (-1)*sum(v_pv*log2(v_pv))
    #7、计算信息增益率
    gainsR_uv <- (ent_u - ent_uv)/ent_v
    return(gainsR_uv)
}
u=disc$Disc.data$Species
s1=disc$Disc.data$Sepal.Length
s2=disc$Disc.data$Sepal.Width
p1=disc$Disc.data$Petal.Length
p2=disc$Disc.data$Petal.Width
ent_us1=gainsR(u,s1)
ent_us2=gainsR(u,s2)
ent_up1=gainsR(u,p1)
ent_up2=gainsR(u,p2)
ent_us1
```
```R
## [1] 0.4184032
```
```R
ent_us2
```
```R
## [1] 0.2472972
```
```R
ent_up1
```
```R
## [1] 0.733996
```
```R
ent_up2
```
```R
## [1] 0.8713692
```
使用FSelector包的两个函数分别计算各输入变量的信息增益和信息增益率，代码如下：
```R
library(discretization)
disc=chiM(iris,alpha=0.05)
library(FSelector)
#计算信息增益
wt1 <- information.gain(Species~.,data=disc$Disc.data)
wt1
```
```R
##              attr_importance
## Sepal.Length       0.4608686
## Sepal.Width        0.2672750
## Petal.Length       0.9402853
## Petal.Width        0.9554360
#计算信息增益率
```
```R
wt2 <- gain.ratio(Species~.,data=disc$Disc.data)
wt2
```
```R
##              attr_importance
## Sepal.Length       0.4679736
## Sepal.Width        0.2472972
## Petal.Length       0.8584937
## Petal.Width        0.8713692
```
# 卡方检验

使用R语言自带程序包stats中的chisq.test函数进行卡方检验，同样对离散化的iris数据集，分析Sepal.Width对Species的影响，代码如下：
```R
library(discretization)
disc=chiM(iris,alpha=0.05)
chisq.test(disc$Disc.data$Sepal.Width,disc$Disc.data$Species)
```
```R
##  Pearson's Chi-squared test
## 
## data:  disc$Disc.data$Sepal.Width and disc$Disc.data$Species
## X-squared = 72.683, df = 4, p-value = 6.156e-15
```

R语言包FSelector中的chi.squared函数实现了通过卡方检验对特征的重要性打分的功能，并且包含了缺失值的处理。现使用chi.squared函数对离散化的iris数据集进行分析，代码如下：
```R
library(discretization)
disc=chiM(iris,alpha=0.05)
library(FSelector)
#基于卡方检验计算特征重要性
chi.squared(Species~.,data=disc$Disc.data)
```
```R
##              attr_importance
## Sepal.Length       0.6398741
## Sepal.Width        0.4922162
## Petal.Length       0.9346311
## Petal.Width        0.9432359
```
```R
chi.squared
```
```R
## function (formula, data) 
## {
##     new_data = get.data.frame.from.formula(formula, data)
##     new_data = discretize.all(formula, new_data)
##     class_data = new_data[[1]]
##     new_data = new_data[-1]
##     results = sapply(new_data, function(w) {
##         cont = table(class_data, w)
##         row_sums = apply(cont, 1, sum)
##         col_sums = apply(cont, 2, sum)
##         all_sum = sum(col_sums)
##         expected_matrix = t(as.matrix(col_sums) %*% t(as.matrix(row_sums)))
##                            /all_sum
##         chis = sum((cont - expected_matrix)^2/expected_matrix)
##         if (chis == 0 || length(col_sums) < 2 || length(row_sums) < 
##             2) {
##             return(0)
##         }
##         else {
##             return(sqrt(chis/(all_sum * min(length(col_sums) - 
##                 1, length(row_sums) - 1))))
##         }
##     })
##     attr_names = dimnames(new_data)[[2]]
##     return(data.frame(attr_importance = results, row.names = attr_names))
## }
## <environment: namespace:FSelector>
```
如代码所示，chi.squared函数的输出包含了各输入变量的重要性得分，同时注意到chi.squared函数的源码，discretize.all实现了对连续值的离散化处理，所以针对连续性的变量，该方法仍然适用。

# Gini系数

这里使用iris数据集，建立rpart模型，并得出各变量的得要性得分，代码如下：
```R
library(rpart)
library(maptree)
## Loading required package: cluster
rpart.fit <- rpart(Species~.,data=iris)
draw.tree(rpart.fit)
```
![image](/images/2018-08-11-12-12)

```R
rpart.fit$variable.importance
```
```R
##  Petal.Width Petal.Length Sepal.Length  Sepal.Width 
##     88.96940     81.34496     54.09606     36.01309
```
```R
barplot(rpart.fit$variable.importance)
```
![image](/images/2018-08-11-12-13)
