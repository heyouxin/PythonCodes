data_row<-read.csv(file="test-2.csv",header=T,sep=",",fileEncoding="gbk",stringsAsFactors = F)
View(data_row)
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
Null_func <- function(pp){
  set.seed(pp)
  #M = 1/(n2/n1) # 不平衡比例
  sample_yes_index = sample(n2, floor(n*pp) , replace = T)
  
  data_balance_yes = data_1_yes[sample_yes_index,]
  data_balance_no = data_1_no
  #View(data_balance_no)
  #View(data_balance_yes)
  #nrow(data_balance_yes)
  #nrow(data_balance_no)
  
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
  #View(x_tra)
  x_tra <- data_tra[,2:nc] %>% unlist %>% as.numeric %>% matrix(nrow=nr,ncol=(nc-1))
  y_tra <- data_tra[,1] %>% unlist %>% as.numeric 
  
  x_test <- data_test[,2:nc] %>% unlist %>% as.numeric %>% matrix(nrow = (n_balance-nr),ncol = (nc-1))
  y_test <- data_test[,1] %>% unlist %>% as.numeric
  #table(y_tra)
  #table(y_test)
  
  # #PART II:  Construct the model 
  # ############################################################################
  #Choose the best tuning parameter
  cv_fit <- cv.glmnet(x_tra, y_tra,  family = "binomial",nfolds=5, type.measure="class")# k-fold cv for glmnet
  #plot(cv_fit)
  #lambda_min <- cv_fit$lambda.min  #the value of lambda that gives minmum cvm
  lambda_lse <- cv_fit$lambda.1se  #largest value of lambda such that error is within 1 standard error of the minimum.
  
  #fit the model using penalizated GLM
  fit_1 <- glmnet(x_tra, y_tra,family="binomial")
  
  # plot(fit_1, xvar = "lambda")
  #grid()
  
  
  #Choose important variable by regularization
  #coef_1 <- coef.glmnet(fit_1, s = exp(-4)) 
  #coef_index <- which(coef_1 != 0)[-1]-1
  # coef_1 <- coef.glmnet(fit_1, s = cv_fit$lambda.1se)    # extract coefficients at lambda equals to lambda.lse
  
  #PART III:  Model evaluation 
  ############################################################################
  pred_1 <-predict(fit_1, newx=x_test, s=cv_fit$lambda.1se, type = "class") %>% as.numeric
  #table(pred_1)
  #table(y_test)
  #Confusion Matrix
  kappa_1 = confusionMatrix(pred_1 %>% as.factor ,y_test %>% as.factor)$overall[c(1,2)]
  #library(ROSE)
  #accuracy.meas(y_test,pred_1)#计算准确率，召回率和F测度
  AUC = roc.curve(y_test ,pred_1,plotit = F)$auc# 0.5分类效果很差
  list("Accuarcy_kappa" =  kappa_1, "AUC" = AUC)
}
pp = seq(0.1, 1, by=0.05)

result_auc = lapply(pp,Null_func)
result_vector = result_auc %>% unlist
n_t = length(result_vector)

Acc = result_vector[seq(1,n_t,by=3)]
Kappa = result_vector[seq(2, n_t, by = 3)]
AUC = result_vector[seq(3, n_t, by = 3)]

Ac = data.frame(c(Acc,Kappa,AUC))


Ac$fac = c(rep("Acc",n_t/3), rep("Kappa", n_t/3), rep("AUC", n_t/3))
View(Ac)
names(Ac)

#ggplot()
#boxplot(c.Acc..Kappa..AUC.~., data = Ac, col=c(2,3,4))
#grid()
ggplot(Ac, aes(x = factor(fac), y = c.Acc..Kappa..AUC., fill = factor(fac))) +
  # 箱线图函数
  geom_boxplot() +
  # 颜色标尺
  scale_fill_brewer(palette = "Pastel2")
