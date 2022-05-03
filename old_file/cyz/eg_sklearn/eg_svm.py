'''
scikit-learn SVM 支持向量机调用示例
https://scikit-learn.org/stable/modules/svm.html#svm-classification
'''

from sklearn import svm
'''
SVC, NuSVC and LinearSVC take as input two arrays: 
an array X of shape (n_samples, n_features) holding the training samples 
an array y of class labels (strings or integers), of shape (n_samples)
'''
x_train = [[0,0], [1,1]]
y = [0, 1]

classifer = svm.SVC() # svm.NuSVC() # svm.LinearSVC()
classifer.fit(x_train, y)
# 测试数据shape (n_samples, n_features)
x_test = [[0,0.5], [1,2]]
# 测试数据得分
dec = classifer.decision_function(x_test)
print("Decision:",dec)
# 测试数据分类
res = classifer.predict(x_test)
print("Result:", res)

# 多类别分类器，分类结果 one-versus-one
multi_clf = svm.SVC(decision_function_shape='ovo')

# 多类别分类器，分类结果 one-vs-the-rest
multi_clf = svm.SVC(decision_function_shape='ovr')