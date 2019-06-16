#PART I Data manipulation
############################################################################
library(magrittr)
data_row<-read.csv(file="/Users/weijuanliang/Desktop/数据之星/3月17日/test-2.csv",header=T,sep=",",fileEncoding="gbk",stringsAsFactors = F)
#View(data_row)
dim(data_row)
#transform the Inf to NA
data_row[sapply(data_row,is.infinite)] <- NA
data <-na.omit(data_row)

data_1 <- data[which(data[,62] !="金融业"),] #delete the financial industry
data_1 <- data_1[,-c(1,62)]    #delete irrelevant information including the coding for sample and Industry name
dim(data_1)
data_1$default = data_1$default %>% as.factor
# get the x's variable and response y
y <- data_1[,1]
x <- data_1[,-1]
N <- length(y)

# depart the total sample into traning data and test data
Tra_Index <- sample(1:N, floor(0.75*N), replace = F) #3/4 traning sample
x_tra <- x[Tra_Index,]  %>% unlist %>% matrix(ncol=ncol(x))
y_tra <- y[Tra_Index] 

x_test <- x[-Tra_Index,]  %>% unlist %>% matrix(ncol=ncol(x)) 
y_test <- y[-Tra_Index]

Train_data <- data.frame(y_tra,x_tra)
names(Train_data) <- names(data_1)

Test_data <- data.frame(y_test,x_test)
names(Test_data) <- names(data_1)


#PART II:  Construct the model 
############################################################################
library("glmnet")
library(caret)
library(magrittr)
library("e1071")
library(pROC)

#Choose the best tuning parameter
cv_fit <- cv.glmnet(x_tra, y_tra, family="binomial")# k-fold cv for glmnet
plot(cv_fit)
lambda_min <- cv_fit$lambda.min  #the value of lambda that gives minmum cvm
lambda_lse <- cv_fit$lambda.1se  #largest value of lambda such that error is within 1 standard error of the minimum.

#fit the model using penalizated GLM
fit_1 <- glmnet(x_tra, y_tra, family = "binomial")
plot(fit_1, xvar = "lambda")
grid()

#Choose important variable by regularization
coef_1 <- coef.glmnet(fit_1, s = cv_fit$lambda.1se)    # extract coefficients at lambda equals to lambda.lse

#PART III:  Model evaluation 
############################################################################
pred_1 <-predict(fit_1, newx=x_test, s=cv_fit$lambda.1se, type = "class") %>% as.numeric

#Confusion Matrix
confusionMatrix(pred_1,y_test)
library(ROSE)
accuracy.meas(y_test,pred_1)#计算准确率，召回率和F测度等
roc.curve(y_test,pred_1,plotit = F)# 0.5分类效果很差

#Imbalance data manipulation
#过采样方法
data_balanced_over <- ovun.sample(default~., data = Train_data, method = "over", N=2700)$data#为0的样本是2570个，补充到正样本与负样本量一样大
table(data_balanced_over$default)

x_over_tra <- data_balanced_over[,-1] %>% as.matrix
y_over_tra <- data_balanced_over[,1] 

cv_fit_glm_over <- cv.glmnet(x_over_tra, y_over_tra, family="binomial")
plot(cv_fit_glm_over)
lambda_lse_glm_over <- cv_fit_glm_over$lambda.1se


fit_glm_over <- glmnet(x_over_tra, y_over_tra , family = "binomial")#训练
coef_glm_over <- coef.glmnet(fit_glm_over, s = lambda_lse_glm_over) 
pred_glm_over <- predict(fit_glm_over,newx = x_test, s = lambda_lse_glm_over,type = "class")

accuracy.meas(y_test,pred_glm_over)
confusionMatrix(pred_glm_over,y_test)

#欠采样方法
data_balanced_under <- ovun.sample(default~., data = Train_data, method = "under", N=100, seed = 1)$data#为1的样本量是34，两倍是68
table(data_balanced_under$default)

x_under_tra <- data_balanced_under[,-1] %>% as.matrix
y_under_tra <- data_balanced_under[,1] 

cv_fit_glm_under <- cv.glmnet(x_under_tra, y_under_tra, family="binomial")
plot(cv_fit_glm_under)
lambda_lse_glm_under <- cv_fit_glm_under$lambda.1se


fit_glm_under <- glmnet(x_under_tra, y_under_tra , family = "binomial")#训练
coef_glm_under <- coef.glmnet(fit_glm_under, s = lambda_lse_glm_under) 
pred_glm_under <- predict(fit_glm_under, newx = x_test, s = lambda_lse_glm_under, type = "class")

accuracy.meas(y_test,pred_glm_under)
confusionMatrix(pred_glm_under,y_test)



#同时进行过采样和欠采样
data_balanced_both <- ovun.sample(default~., data = Train_data, method = "both", p=0.1,N=2604,seed = 1)$data#函数的参数p代表新生成数据集中正类的比例。
table(data_balanced_both$default)

x_both_tra <- data_balanced_both[,-1] %>% as.matrix
y_both_tra <- data_balanced_both[,1] 

cv_fit_glm_both <- cv.glmnet(x_both_tra, y_both_tra, family="binomial")
plot(cv_fit_glm_both)
lambda_lse_glm_both <- cv_fit_glm_both$lambda.1se


fit_glm_both <- glmnet(x_both_tra, y_both_tra , family = "binomial")#训练
coef_glm_both <- coef.glmnet(fit_glm_both, s = lambda_lse_glm_both) 
pred_glm_both <- predict(fit_glm_both, newx = x_test, s = lambda_lse_glm_both, type = "class")

accuracy.meas(y_test,pred_glm_both)
confusionMatrix(pred_glm_both,y_test)

#人工合成法
data_balanced_syn <- ROSE(default~., data = Train_data, seed = 1)$data
table(data_balanced_syn$default)

x_syn_tra <- data_balanced_syn[,-1] %>% as.matrix
y_syn_tra <- data_balanced_syn[,1] 

cv_fit_glm_syn <- cv.glmnet(x_syn_tra, y_syn_tra, family="binomial")
plot(cv_fit_glm_syn)
lambda_lse_glm_syn <- cv_fit_glm_syn$lambda.1se


fit_glm_syn <- glmnet(x_syn_tra, y_syn_tra , family = "binomial")#训练
coef_glm_syn <- coef.glmnet(fit_glm_syn, s = lambda_lse_glm_syn) 
pred_glm_syn <- predict(fit_glm_syn, newx = x_test, s = lambda_lse_glm_syn, type = "class")

accuracy.meas(y_test,pred_glm_syn)
confusionMatrix(pred_glm_syn,y_test)

############################################################
#adaboost
############################################################
#install.packages("adabag")
library(adabag)
#训练样本
boosting_row <- boosting(default~., data = Train_data)
#预测结果
boosting_matrix_pred <- table(Train_data$default, predict(boosting_row, Train_data)$class)
boosting_matrix_pred <- table(Test_data$default,predict(boosting_row,Test_data)$class)
#计算误差率
(E_boosting=(sum(boosting_matrix_pred)-sum(diag(boosting_matrix_pred)))/sum(boosting_matrix_pred))
#0.001152074
#画出变量重要性图
barplot(boosting_row$importance)
#计算全体的误差演变
b <- errorevol(boosting_row, Train_data)
plot(b$error, type = "l",main = "AdaBoost error vs number of trees")#对误差演变进行画图

############################################################
#bagging()
############################################################
bagging_row <- bagging(default~., data = Train_data)##建立bagging分类模型
(bagging_matrix_pred <- table(Train_data$default, predict(bagging_row, Train_data)$class))
#计算误差率
(E_bagging=(sum(bagging_matrix_pred)-sum(diag(bagging_matrix_pred)))/sum(bagging_matrix_pred))
#画出变量重要性图
barplot(bagging_row$importance)
