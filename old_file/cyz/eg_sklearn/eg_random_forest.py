'''
sklearn 调用随机森林
https://scikit-learn.org/stable/modules/ensemble.html#forest
'''

from sklearn.ensemble import RandomForestClassifier
X = [[0, 0], [1, 1]]
Y = [0, 1]
# 设置随机森林中树的数量，增大可以减小泛化误差，超过一定数量，模型基本收敛
# 树的深度：深度过大可能出现过拟合，样本量和特征数量很多时要注意
# 函数详见 https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
clf = RandomForestClassifier(n_estimators=10)
clf = clf.fit(X, Y)
res = clf.predict([[0, 0.2]])
print(res)