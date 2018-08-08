+++
date = "2018-08-07"
title = "dplyr包基础用法"
categories = { "R语言系列":["dplyr"] }
tags = {"标签":["R语言","数据处理"]}
+++

dplyr包是Hadley Wickham的杰作, 专注接受dataframe对象, 大幅提高了速度, 并且提供了稳健的与其它数据库对象间的接口。
dplyr是一套数据操作的语法，它提供了一致的动作集合可以帮助你解决常见的数据操作问题，比如变量衍生、选取变量、过滤记录、聚合分析、排序等等。

本文试图对该dplyr包的一些基础且常用的功能做简要介绍。
主要包括：

<span id='home'></span>
[tbl对象](#tibble_obj)
[数据操作](#sjcz)
&emsp;&emsp;[变量筛选](#sjcz_blsx)
&emsp;&emsp;[记录过滤](#sjcz_jlgl)
&emsp;&emsp;[排序操作](#sjcz_bxcz)
&emsp;&emsp;[关联操作](#sjcz_glcz)
&emsp;&emsp;[衍生变量](#sjcz_ysbl)
&emsp;&emsp;[重命名变量](#sjcz_cmmbl)

 +  [聚合分析](#jhfx)
    + [汇总函数](#jhfx_hzhs)
    + [分组函数](#jhfx_fzhs)
    + [聚合函数](#jhfx_jhhs)
 +  [抽样函数](#cyhs)
 +  [管道操作](#gdcz)

<span id='tibble_obj'></span>

# [tbl对象](#home)

tibble包提供了一个tbl_df类，它比传统的data.frame具有更严格的检查和更好的格式。as_tibble是一个新的S3更加通用也更加高效的函数，非常适合处理matirx和data.frame对象。它可以将普通的matrix或data.frame的对象转换成tbl_df类的对象。dplyr包中的函数都是基于tbl_df对象实现的。


 - 将data.frame转换成tbl_df
 
 ```R
library(dplyr)
tbl_df(mtcars)
 ```
 ```R
## A tibble: 32 x 11
#     mpg   cyl  disp    hp  drat    wt  qsec    vs    am  gear  carb
#  * <dbl> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl>
#  1  21.0  6.00   160 110    3.90  2.62  16.5  0     1.00  4.00  4.00
#  2  21.0  6.00   160 110    3.90  2.88  17.0  0     1.00  4.00  4.00
#  3  22.8  4.00   108  93.0  3.85  2.32  18.6  1.00  1.00  4.00  1.00
#  4  21.4  6.00   258 110    3.08  3.22  19.4  1.00  0     3.00  1.00
#  5  18.7  8.00   360 175    3.15  3.44  17.0  0     0     3.00  2.00
#  6  18.1  6.00   225 105    2.76  3.46  20.2  1.00  0     3.00  1.00
#  7  14.3  8.00   360 245    3.21  3.57  15.8  0     0     3.00  4.00
#  8  24.4  4.00   147  62.0  3.69  3.19  20.0  1.00  0     4.00  2.00
#  9  22.8  4.00   141  95.0  3.92  3.15  22.9  1.00  0     4.00  2.00
# 10  19.2  6.00   168 123    3.92  3.44  18.3  1.00  0     4.00  4.00
## ... with 22 more rows
 ```
也可以使用as_tibble函数，如下：
```R
as_tibble(mtcars)
```
```R
##  A tibble: 32 x 11
#      mpg   cyl  disp    hp  drat    wt  qsec    vs    am  gear  carb
#  * <dbl> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl>
#  1  21.0  6.00   160 110    3.90  2.62  16.5  0     1.00  4.00  4.00
#  2  21.0  6.00   160 110    3.90  2.88  17.0  0     1.00  4.00  4.00
#  3  22.8  4.00   108  93.0  3.85  2.32  18.6  1.00  1.00  4.00  1.00
#  4  21.4  6.00   258 110    3.08  3.22  19.4  1.00  0     3.00  1.00
#  5  18.7  8.00   360 175    3.15  3.44  17.0  0     0     3.00  2.00
#  6  18.1  6.00   225 105    2.76  3.46  20.2  1.00  0     3.00  1.00
#  7  14.3  8.00   360 245    3.21  3.57  15.8  0     0     3.00  4.00
#  8  24.4  4.00   147  62.0  3.69  3.19  20.0  1.00  0     4.00  2.00
#  9  22.8  4.00   141  95.0  3.92  3.15  22.9  1.00  0     4.00  2.00
# 10  19.2  6.00   168 123    3.92  3.44  18.3  1.00  0     4.00  4.00
# ... with 22 more rows
```
可以看到，tbl对象直接在控制台打印输出，默认会只输出前10条，同时给出了数据规格，比如32 x 11表示32个观测样本，11个变量，此外，也给出了各变量的数据类型，dbl表示double类型，等等。

<span id='sjcz'></span>
# [数据操作](#home)

<span id='sjcz_blsx'></span>
### [变量筛选](#home)

使用select函数可筛选指定的变量，比subset函数更灵活的是，在选择变量的同时也可以重新命名变量。
我们首先将iris数据集转换成tbl对象，如下：
```R
iris <- as_tibble(iris) 
```
使用select函数，选取iris数据中以Petal开头的变量，代码如下：
```R
iris %>% select(starts_with("Petal"))
```
```R
## A tibble: 150 x 2
#   Petal.Length Petal.Width
#          <dbl>       <dbl>
# 1         1.40       0.200
# 2         1.40       0.200
# 3         1.30       0.200
# 4         1.50       0.200
# 5         1.40       0.200
# 6         1.70       0.400
# 7         1.40       0.300
# 8         1.50       0.200
# 9         1.40       0.200
#10         1.50       0.100
# ... with 140 more rows
```
使用select函数，选取iris数据中以Width结束的变量，代码如下：
```R
iris %>% select(ends_with("Width"))
```
```R
## A tibble: 150 x 2
#   Sepal.Width Petal.Width
#         <dbl>       <dbl>
# 1        3.50       0.200
# 2        3.00       0.200
# 3        3.20       0.200
# 4        3.10       0.200
# 5        3.60       0.200
# 6        3.90       0.400
# 7        3.40       0.300
# 8        3.40       0.200
# 9        2.90       0.200
#10        3.10       0.100
# ... with 140 more rows
```
使用select函数，选择iris数据中包含etal字符中的变量，代码如下：
```R
iris %>% select(contains("etal"))
```
```R
## A tibble: 150 x 2
#   Petal.Length Petal.Width
#          <dbl>       <dbl>
# 1         1.40       0.200
# 2         1.40       0.200
# 3         1.30       0.200
# 4         1.50       0.200
# 5         1.40       0.200
# 6         1.70       0.400
# 7         1.40       0.300
# 8         1.50       0.200
# 9         1.40       0.200
#10         1.50       0.100
# ... with 140 more rows
```
同理，可以starts_with、ends_with、contains前面加负号，表示排除满足条件的变量。
everything()函数可以选取数据集中的所有变量，通常可指定几个变量，再使用everything()函数以达到对亦量重新排列的效果，案例如下：
```R
iris %>% select(Species, everything())
```
```R
## A tibble: 150 x 5
#   Species Sepal.Length Sepal.Width Petal.Length Petal.Width
#   <fct>          <dbl>       <dbl>        <dbl>       <dbl>
# 1 setosa          5.10        3.50         1.40       0.200
# 2 setosa          4.90        3.00         1.40       0.200
# 3 setosa          4.70        3.20         1.30       0.200
# 4 setosa          4.60        3.10         1.50       0.200
# 5 setosa          5.00        3.60         1.40       0.200
# 6 setosa          5.40        3.90         1.70       0.400
# 7 setosa          4.60        3.40         1.40       0.300
# 8 setosa          5.00        3.40         1.50       0.200
# 9 setosa          4.40        2.90         1.40       0.200
#10 setosa          4.90        3.10         1.50       0.100
# ... with 140 more rows
```
可见，everything()函数，将数据中Species之外的所有变量提取了出来。最终达到重排列的效果。
不过，对于匹配变量，我们还可以使用正则表达式来做，请看如下代码：
```R
iris %>% select(matches(".t."))
```
```R
## A tibble: 150 x 4
#   Sepal.Length Sepal.Width Petal.Length Petal.Width
#          <dbl>       <dbl>        <dbl>       <dbl>
# 1         5.10        3.50         1.40       0.200
# 2         4.90        3.00         1.40       0.200
# 3         4.70        3.20         1.30       0.200
# 4         4.60        3.10         1.50       0.200
# 5         5.00        3.60         1.40       0.200
# 6         5.40        3.90         1.70       0.400
# 7         4.60        3.40         1.40       0.300
# 8         5.00        3.40         1.50       0.200
# 9         4.40        2.90         1.40       0.200
#10         4.90        3.10         1.50       0.100
## ... with 140 more rows
```
我们可以通过one_of函数，来选取指定的变量，代码如下：
```R
iris %>% select(one_of(c("Petal.Length", "Species")))
```
```R
## A tibble: 150 x 2
#   Petal.Length Species
#          <dbl> <fct>  
# 1         1.40 setosa 
# 2         1.40 setosa 
# 3         1.30 setosa 
# 4         1.50 setosa 
# 5         1.40 setosa 
# 6         1.70 setosa 
# 7         1.40 setosa 
# 8         1.50 setosa 
# 9         1.40 setosa 
#10         1.50 setosa 
## ... with 140 more rows
```
如果变量名称满足一定的规律，比如V1~V100，可通过num_range函数来进行变量选择，案例如下：
```R
df <- tbl_df(matrix(runif(100), nrow = 10))
df
```
```R
## A tibble: 10 x 10
#      V1      V2    V3    V4     V5      V6    V7    V8    V9    V10
#   <dbl>   <dbl> <dbl> <dbl>  <dbl>   <dbl> <dbl> <dbl> <dbl>  <dbl>
# 1 0.440 0.811   0.578 0.979 0.416  0.345   0.505 0.486 0.731 0.351 
# 2 0.235 0.345   0.736 0.418 0.765  0.936   0.936 0.208 0.716 0.309 
# 3 0.914 0.978   0.691 0.976 0.520  0.123   0.865 0.410 0.235 0.0650
# 4 0.286 0.942   0.249 0.719 0.935  0.912   0.840 0.413 0.369 0.494 
# 5 0.160 0.00493 0.568 0.809 0.382  0.00882 0.737 0.492 0.942 0.912 
# 6 0.107 0.965   0.204 0.908 0.988  0.537   0.759 0.888 0.322 0.353 
# 7 0.233 0.266   0.368 0.992 0.382  0.813   0.379 0.939 0.622 0.339 
# 8 0.624 0.290   0.174 0.703 0.785  0.419   0.498 0.762 0.155 0.0788
# 9 0.437 0.711   0.165 0.683 0.0841 0.278   0.546 0.453 0.197 0.557 
#10 0.376 0.743   0.268 0.486 0.0959 0.186   0.626 0.880 0.171 0.0135
```
```R
df %>% select(num_range("V", 4:6))
```
```R
## A tibble: 10 x 3
#      V4     V5      V6
#   <dbl>  <dbl>   <dbl>
# 1 0.979 0.416  0.345  
# 2 0.418 0.765  0.936  
# 3 0.976 0.520  0.123  
# 4 0.719 0.935  0.912  
# 5 0.809 0.382  0.00882
# 6 0.908 0.988  0.537  
# 7 0.992 0.382  0.813  
# 8 0.703 0.785  0.419  
# 9 0.683 0.0841 0.278  
#10 0.486 0.0959 0.186  
```
另外，我们还可以通过指定数据中起始和结束列名来选择变量，代码如下：
```R
mtcars %>% tbl_df %>% select(disp:wt)
```
```R
## A tibble: 32 x 4
#    disp    hp  drat    wt
# * <dbl> <dbl> <dbl> <dbl>
# 1   160 110    3.90  2.62
# 2   160 110    3.90  2.88
# 3   108  93.0  3.85  2.32
# 4   258 110    3.08  3.22
# 5   360 175    3.15  3.44
# 6   225 105    2.76  3.46
# 7   360 245    3.21  3.57
# 8   147  62.0  3.69  3.19
# 9   141  95.0  3.92  3.15
#10   168 123    3.92  3.44
## ... with 22 more rows
```

<span id='sjcz_jlgl'></span>
### [记录过滤](#home)
新建一个data.frame，并将其转换为tbl_df对象，使用filter函数进行条件筛选，代码如下：
```R
df <- data.frame(x=c('a','b','c','a','b','e','d','f'), y=1:8)
df2tbl <- tbl_df(df)
df2tbl
```
```R
##  A tibble: 8 x 2
#   x         y
#   <fct> <int>
# 1 a         1
# 2 b         2
# 3 c         3
# 4 a         4
# 5 b         5
# 6 e         6
# 7 d         7
# 8 f         8
```
```R
df2tbl %>% filter(x%in%c('a','b'))
```
```R
##  A tibble: 4 x 2
#   x         y
#   <fct> <int>
# 1 a         1
# 2 b         2
# 3 a         4
# 4 b         5
```
```R
df2tbl %>% filter(!x%in%c('a','b'))
```
```R
##  A tibble: 4 x 2
#   x         y
#   <fct> <int>
# 1 c         3
# 2 e         6
# 3 d         7
# 4 f         8
```
filter函数的第一个参数为tbl对象，第二个参数是条件向量，该函数只返回条件为TRUE的记录。

<span id='sjcz_bxcz'></span>
### [排序操作](#home)
对df2tbl数据集，使用arrange函数对y变量进行排序，代码如下：
```R
df2tbl %>% arrange(y)
```
```R
## A tibble: 8 x 2
#  x         y
#  <fct> <int>
#1 a         1
#2 b         2
#3 c         3
#4 a         4
#5 b         5
#6 e         6
#7 d         7
#8 f         8
```
arrange函数，默认对变量进行升序排列。我们可以结合desc函数对变量进行降序排列，案例如下：
```R
df2tbl %>% arrange(desc(y))
```
```R
## A tibble: 8 x 2
#  x         y
#  <fct> <int>
#1 f         8
#2 d         7
#3 e         6
#4 b         5
#5 a         4
#6 c         3
#7 b         2
#8 a         1
```

<span id='sjcz_glcz'></span>
### [关联操作](#home)
构建一个新的tbl对象df2tbl2，如下：
```R
df2tbl2 <- tbl_df(data.frame(x=c('a','b','c'),z=c('A','B','C')))
df2tbl2
```
```R
## A tibble: 3 x 2
#  x     z    
#  <fct> <fct>
#1 a     A    
#2 b     B    
#3 c     C 
```
可知，df2tbl2对象只有3条记录。现使用inner_join函数对df2tbl和df2tbl2，按x变量进行内关联，代码如下：
```R
inner_join(x=df2tbl2,y=df2tbl,by='x')
```
```R
## A tibble: 5 x 3
#  x         y z    
#  <chr> <int> <fct>
#1 a         1 A    
#2 b         2 B    
#3 c         3 C    
#4 a         4 A    
#5 b         5 B 
```
如果出现"Column `x` joining factors with different levels"这样的提示，表示关联的x字段在两个数据中具有不同的水平值。正常情况下可以忽略。也可以修改成一样的水平值，便不会报这个警告信息。
可以看到，使用inner_join函数可以将参与内关联的两个数据对象，按x变量同时出现的值进行了关联。
同理，我们还可以使用left_join、right_join、full_join函数分别进行左关联、右关联和全关联操作。
有时，我们为了简化操作，对参与关联的两个数据x和y，使用y进行关联，而直接返回x匹配上的子集，我们可以使用semi_join函数，代码如下：
```R
semi_join(x=df2tbl2,y=df2tbl,by='x')
```
```R
## A tibble: 3 x 2
#  x     z    
#  <fct> <fct>
#1 a     A    
#2 b     B    
#3 c     C   
```
该例中，返回结果只有x数据对象的，并是经过与y进行关联后得到的子集。
如果此时，我们只想提取与y不匹配的x的子集，则可以使用anti_join，案例如下：
```R
anti_join(x=df2tbl,y=df2tbl2,by='x')
```
```R
## A tibble: 3 x 2
#  x         y
#  <fct> <int>
#1 e         6
#2 d         7
#3 f         8
```
该例中，提取了x数据对象中与y数据按by变量不匹配的子集。

<span id='sjcz_ysbl'></span>
### [衍生变量](#home)
我们可以通过mutate()函数可以在原始数据集的基础上扩展新变量，类似于transform()函数
```R
df2tbl %>% mutate(z=y^2+y-10)
```
```R
## A tibble: 8 x 3
#  x         y      z
#  <fct> <int>  <dbl>
#1 a         1 - 8.00
#2 b         2 - 4.00
#3 c         3   2.00
#4 a         4  10.0 
#5 b         5  20.0 
#6 e         6  32.0 
#7 d         7  46.0 
#8 f         8  62.0 
```
```R
df2tbl %>% transmute(z=y^2+y-10)
```
```R
## A tibble: 8 x 1
#       z
#   <dbl>
#1 - 8.00
#2 - 4.00
#3   2.00
#4  10.0 
#5  20.0 
#6  32.0 
#7  46.0 
#8  62.0 
```
通过对比，可以发现，transmute函数并不会保留衍生之前的变量，而mutate函数会保留。

<span id='sjcz_cmmbl'></span>
### [重命名变量](#home)
如果需要对数据集中的某些变量进行重命名的话，可以直接使用rename()函数
```R
df2tbl %>% rename(x1=x,y2=y)
```
```R
## A tibble: 8 x 2
#  x1       y2
#  <fct> <int>
#1 a         1
#2 b         2
#3 c         3
#4 a         4
#5 b         5
#6 e         6
#7 d         7
#8 f         8
```
<span id='jhfx'></span>
# [聚合分析](#home)

<span id='jhfx_hzhs'></span>
### [汇总函数](#home)
我们可以使用summarize函数实现数据集聚合操作，其函数原型如下：
```R
summarize(.data, ...)
```
其中，.data表示用于聚合操作的tbl对象，...表示汇总函数的Name-Value对，Name是结果中变量的名称，Value则是返回单独值的表达式。
<span id='jhfx_fzhs'></span>
### [分组函数](#home)
summarize函数可以结合group_by()函数实现分组聚合，group_by()原型如下：
```R
group_by(.data, ..., add = FALSE)
```
其中，.data表示用于聚合操作的tbl对象，...表示用于分组的变量，add为TRUE表示追加到已经存在的分组中。

<span id='jhfx_jhhs'></span>
### [聚合函数](#home)
常用的聚合函数包括：
min()：返回最小值
max()：返回最大值
mean()：返回均值
sum()：返回总和
sd()：返回标准差
median()：返回中位数
IQR()：返回四分位极差
n()：返回观测个数
n_distinct()：返回不同的观测个数
first()：返回第一个观测
last()：返回最后一个观测
nth()：返回n个观测
比如，要对df2tbl对象中的y变量求最大值，则可以使用summarize函数，代码如下：
```R
df2tbl %>% summarize(max(y))
```
```R
## A tibble: 1 x 1
#  `max(y)`
#     <dbl>
#1     8.00
```
对df2tbl对象，按x进行分组，求y的最大值，代码如下：
```R
df2tbl %>% group_by(x) %>% summarize(sum(y))
```
```R
## A tibble: 6 x 2
#  x     `sum(y)`
#  <fct>    <int>
#1 a            5
#2 b            7
#3 c            3
#4 d            7
#5 e            6
#6 f            8
```

<span id='cyhs'></span>
# [抽样函数](#home)
sample_n()函数可随机选出指定个数的样本数，代码如下：
```R
df2tbl %>% sample_n(3)
```
```R
## A tibble: 3 x 2
#  x         y
#  <fct> <int>
#1 a         4
#2 c         3
#3 b         2
```
sample_frac()函数则可随机选出指定百分比的样本数，代码如下：
```R
df2tbl %>% sample_frac(0.2)
```
```R
## A tibble: 2 x 2
#  x         y
#  <fct> <int>
#1 e         6
#2 a         1
```
<span id='gdcz'></span>
# [管道操作](#home)
dplyr提供了一个符号%>%，该符号将左边的对象作为第一个参数传递到右边的函数中，这样就实现类似unix管道的编程风格，代码更易读。
