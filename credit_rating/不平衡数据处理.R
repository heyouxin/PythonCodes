#install.packages("ROSE")
library(ROSE)
data(hacide)
str(hacide.train)
table(hacide.train$cls)
prop.table(table(hacide.train$cls))

#建立决策树模型
#install.packages("rpart")
library(rpart)
treeimb <- rpart(cls~., data=hacide.train)
pred.treeimb <- predict(treeimb, newdata = hacide.test)
#看一下模型的预测精度
accuracy.meas(hacide.test$cls, pred.treeimb[,2])
roc.curve(hacide.test$cls, pred.treeimb[,2], plotit = F)

#使用过采样技术
data_balanced_over <- ovun.sample(cls~., data = hacide.train, method = "over",N=1960)$data
table(data_balanced_over$cls)#N代表最终平衡数据集包含的样本点，本例中我们有980个原始负类样本，所以我们要通过过采样法把正类样本也补充到980个，数据集共有1960个观测。

#使用欠采样方法
data_balanced_under <- ovun.sample(cls~., data = hacide.train, method = "under", N=40,seed=1)$data
table(data_balanced_under$cls)
#欠采样后数据是平衡了，但由于只剩下了40个样本，我们损失了太多信息。
#我们还可以同时采取这两类方法，只需要把参数改为method = “both”。这时，对小类样本会进行有放回的过采样而对大类样本则进行无放回的欠采样。
data_balanced_both <- ovun.sample(cls~., data = hacide.train, method = "both",p=0.5,N=1000, seed = 1)$data
table(data_balanced_both$cls)
#函数的参数p代表新生成数据集中正类的比例
#但前文已经提过两类采样法都有自身的缺陷，欠采样会损失信息，过采样容易导致过拟合，因而ROSE包也提供了ROSE()函数来合成人工数据，它能提供关于原始数据的更好估计。
data.rose <-ROSE(cls~., data = hacide.train, seed = 1)$data
table(data.rose$cls)
#这里生成的数据量和原始数据集相等(1000个观测)。

#下面用四种方法来分别建立决策树
#训练决策树
tree.rose <- rpart(cls~., data = data.rose)
tree.over <- rpart(cls~., data = data_balanced_over)
tree.under <- rpart(cls~., data = data_balanced_under)
tree.both <- rpart(cls~., data = data_balanced_both)

#在测试集上做预测
pred.tree.rose <- predict(tree.rose,newdata = hacide.test)
pred.tree.over <- predict(tree.over,newdata = hacide.test)
pred.tree.under <- predict(tree.under,newdata = hacide.test)
pred.tree.both <- predict(tree.both,newdata = hacide.test)
roc.curve(hacide.test$cls,pred.tree.rose[,2])
roc.curve(hacide.test$cls,pred.tree.under[,2])
roc.curve(hacide.test$cls,pred.tree.both[,2])
roc.curve(hacide.test$cls,pred.tree.over[,2])

#这个包为我们提供了一些基于holdout和bagging的模型评估方法，这有助于我们判断预测结果是否有太大的方差。
ROSE.holdout <- ROSE.eval(cls~., data = hacide.train, learner = rpart, method.assess = "holdout",
                          extr.pred = function(obj)obj[,2],seed = 1)
ROSE.holdout
