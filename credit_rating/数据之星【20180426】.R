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
library(ROSE)

#path <- getwd()
setwd("/Users/weijuanliang/Desktop/数据之星/3月17日")

data_row<-read.csv(file="test-2.csv",header=T,sep=",",fileEncoding="gbk",stringsAsFactors = F)
#View(data_row)
#dim(data_row)
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

# #PART III：replicate
# ############################################################################
Rep <- function(iii){
  M = 1/(n2/n1) # 不平衡比例
  sample_yes_index = sample(n2, floor(n*0.4) , replace = T)
  
  data_balance_yes = data_1_yes[sample_yes_index,]
  data_balance_no = data_1_no
  data_balance_total <- rbind(data_balance_no, data_balance_yes)
  
  
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
  
  #Choose the best tuning parameter
  cv_fit <- cv.glmnet(x_tra, y_tra,  family = "binomial",nfolds=5, type.measure="class")# k-fold cv for glmnet
  lambda_lse <- cv_fit$lambda.1se  #largest value of lambda such that error is within 1 standard error of the minimum.
  
  #fit the model using penalizated GLM
  fit_1 <- glmnet(x_tra, y_tra,family="binomial")
  
  #Choose important variable by regularization
  coef_1 <- coef.glmnet(fit_1, s = cv_fit$lambda.1se)    # extract coefficients at lambda equals to lambda.lse
  
  #PART III:  Model evaluation 
  ############################################################################
  pred_1 <-predict(fit_1, newx=x_test, s=cv_fit$lambda.1se, type = "class") %>% as.numeric
  #Confusion Matrix
  #confusionMatrix(pred_1 %>% as.factor ,y_test %>% as.factor)
  #accuracy.meas(y_test,pred_1)#计算准确率，召回率和F测度
  roc.curve(y_test ,pred_1,plotit = F)$auc # 0.5分类效果很差
}

lapply(1,Rep)
