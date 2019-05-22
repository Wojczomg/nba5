
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import cross_val_score
from sklearn.metrics import precision_score
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
exec(open("nba20182019.py").read())
over34=np.where(mainstat.loc[:,[4,5,6,7]].sum(axis=1)<mainstat.loc[:,[8,9,10,11]].sum(axis=1),1,0)
Xtrain,Xtest,ytrain,ytest=train_test_split(X,over34,test_size=0.25,stratify=over34)
pca=PCA()
pca.fit(Xtrain)
nvar=pca.explained_variance_ratio_
nvar=list(nvar)
nvar.sort(reverse=True)
for i in range(len(nvar)):
	print(sum(nvar[:i]))

paramgrid={'bootstrap': [True, False],
 'max_depth': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, None],
 'max_features': ['auto', 'sqrt'],
 'min_samples_leaf': [1, 2, 4],
 'min_samples_split': [2, 5, 10],
 'n_estimators': [8,10,20,30,40,50,80,100,150,200,300,400]}

 grid=GridSearchCV(RandomForestClassifier(),param_grid=paramgrid,cv=8)
 grid.fit(Xtrain,ytrain)
 grid.best_score_

paramgridsvc=[{"kernel":["rbf"],
"C":[0.00001,0.0001,0.001,0.01,0.1,1,10,100],
"gamma":[0.00001,0.0001,0.001,0.01,0.1,1,10]},
{"kernel":["poly"],
"gamma":[0.00001,0.0001,0.001,0.01,0.1,1,10],
"C":[0.00001,0.0001,0.001,0.01,0.1,1,10,100],
"degree":[2,3,4,5,6,7,8,9]}]

sc=StandardScaler()
Xtrainstd=sc.fit_transform(Xtrain)

# grid2=GridSearchCV(SVC(max_iter=500),param_grid=paramgridsvc,cv=8)
# grid2.fit(Xtrainstd,ytrain)
# grid2.best_score_

pca=PCA(n_components=20)
Xtrainpca=pca.fit_transform(Xtrain)
scpca=StandardScaler()
Xtrainpcastd=scpca.fit_transform(Xtrainpca)

grid2pca=GridSearchCV(SVC(max_iter=1000),param_grid=paramgridsvc,cv=8)
grid2pca.fit(Xtrainpcastd,ytrain)
grid2pca.best_score_

svc=SVC(kernel="rbf",C=100,gamma=0.001)
svc.fit(Xtrainpcastd,ytrain)
accuracy_score(ytrain,cross_val_predict(svc,Xtrainpcastd,ytrain,cv=10))
precision_score(ytrain,cross_val_predict(svc,Xtrainpcastd,ytrain,cv=10))

decfun=svc.decision_function(Xtrainpcastd)
precision_score(ytrain,np.where(decfun > 1,1,0))
confusion_matrix(ytrain,np.where(decfun > 1,1,0))

precision_score(np.where(ytrain == 0,1,0),np.where(decfun < -1,1,0))
confusion_matrix(np.where(ytrain == 0,1,0),np.where(decfun < -1,1,0))


