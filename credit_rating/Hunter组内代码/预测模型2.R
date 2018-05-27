#PART I Data manipulation
############################################################################
#install.packages("magrittr")
#install.packages("glmnet")
#install.packages("caret")
#install.packages("e1071")
#install.packages("pROC")
#install.packages("ROSE")

library(magrittr)
library(glmnet)
library(caret)
library(magrittr)
library(e1071)
library(pROC)

path <- getwd()
setwd("/Users/weijuanliang/Desktop/数据之星/3月17日")

data_row<-read.csv(file="test-2.csv",header=T,sep=",",fileEncoding="gbk",stringsAsFactors = F)
#View(data_row)
dim(data_row)
#transform the Inf to NA
data_row[sapply(data_row,is.infinite)] <- NA
data <-na.omit(data_row)

data_1<-data[which(data$industry_name!="金融业"),]#delete the financial industry
data_1 <-data_1[,-c(1,62)]#delete irrelevant information including the coding for sample and Industry name
#View(data_1)

data_1_no<-data_1[which(data_1$default==0),]
data_1_yes<-data_1[which(data_1$default!=0),]

(n<-dim(data_1)[1])
(n1<-dim(data_1_no)[1])
(n2<-dim(data_1_yes)[1])

#小类平衡法
#Sample the data
set.seed(100)
M = 1/(n2/n1) # 不平衡比例
sample_yes_index = sample(n2, floor(n*1.3) , replace = T)

data_balance_yes = data_1_yes[sample_yes_index,]
data_balance_no = data_1_no
#View(data_balance_no)
#View(data_balance_yes)
nrow(data_balance_yes)
nrow(data_balance_no)

data_balance_total <- rbind(data_balance_no, data_balance_yes)
#View(data_balance_total)
#nrow(data_balance_total)

#depart the data into training sample and testing sample
n_balance <- nrow(data_balance_total)
sample_index <- sample(n_balance, floor(0.75*n_balance), replace = F)
data_tra <- data_balance_total[sample_index,]
data_test <- data_balance_total[-sample_index,]

nc <- ncol(data_tra)
nr <- length(sample_index)
x_tra <- data_tra[,2:nc] %>% unlist %>% as.numeric %>% matrix(nrow=nr,ncol=(nc-1))
y_tra <- data_tra[,1] %>% unlist %>% as.numeric 

x_test <- data_test[,2:nc] %>% unlist %>% as.numeric %>% matrix(nrow = (n_balance-nr),ncol = (nc-1))
y_test <- data_test[,1] %>% unlist %>% as.numeric
table(y_tra)
table(y_test)








# #PART II:  Construct the model 
# ############################################################################


#Choose the best tuning parameter
cv_fit <- cv.glmnet(x_tra, y_tra,  family = "binomial",nfolds=5, type.measure="class")# k-fold cv for glmnet
plot(cv_fit)
lambda_min <- cv_fit$lambda.min  #the value of lambda that gives minmum cvm
lambda_lse <- cv_fit$lambda.1se  #largest value of lambda such that error is within 1 standard error of the minimum.

#fit the model using penalizated GLM
fit_1 <- glmnet(x_tra, y_tra,family="binomial")
plot(fit_1, xvar = "lambda")
grid()


#Choose important variable by regularization
coef_1 <- coef.glmnet(fit_1, s = cv_fit$lambda.1se)    # extract coefficients at lambda equals to lambda.lse

#PART III:  Model evaluation 
############################################################################
pred_1 <-predict(fit_1, newx=x_test, s=cv_fit$lambda.1se, type = "class") %>% as.numeric
table(pred_1)
table(y_test)
#Confusion Matrix
confusionMatrix(pred_1 %>% as.factor ,y_test %>% as.factor)
library(ROSE)
accuracy.meas(y_test,pred_1)#计算准确率，召回率和F测度
roc.curve(y_test ,pred_1,plotit = F)# 0.5分类效果很差




############################################################
#adaboost
############################################################
#install.packages("adabag")
train <- cbind(y_tra, x_tra) %>% as.data.frame
names(train) <- names(data_1_no)
train$default <- as.factor(train$default)


test <- cbind(y_test, x_test) %>% as.data.frame
names(test) <- names(data_1_no)
test$default <- as.factor(test$default)

library(adabag)
#训练样本
boosting_row <- boosting(default~., data = train)
#预测结果
boosting_matrix_pred <- table(train$default, predict(boosting_row, train)$class)
boosting_matrix_pred <- table(test$default,predict(boosting_row,test)$class)
#计算误差???
(E_boosting=(sum(boosting_matrix_pred)-sum(diag(boosting_matrix_pred)))/sum(boosting_matrix_pred))
#0.001152074
#画出变量重要性图
barplot(boosting_row$importance)
#计算全体的误差演???
b <- errorevol(boosting_row, train)
plot(b$error, type = "l",main = "AdaBoost error vs number of trees")#对误差演变进行画???

############################################################
#bagging()
############################################################
bagging_row <- bagging(default~., data = train)##建立bagging分类模型
(bagging_matrix_pred <- table(train$default, predict(bagging_row, train)$class))
#计算误差???
(E_bagging=(sum(bagging_matrix_pred)-sum(diag(bagging_matrix_pred)))/sum(bagging_matrix_pred))
#画出变量重要性图
barplot(bagging_row$importance)


setwd(path)
