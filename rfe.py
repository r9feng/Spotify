import pandas as pd 
from sklearn.feature_selection import RFE
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, auc

# load data
master = pd.read_csv('Data/master.csv')

# setting dependent and independent variables
var_names = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'key',
           'liveness', 'loudness', 'mode','speechiness', 'tempo', 'time_signature',
           'valence', 'duration_sec','lexical_richness', 
           'WPM', 'sentiment']
x = master[var_names]
y = master['isBillboard']

# Normalize all data for model
sc = StandardScaler()  
x_norm = sc.fit_transform(x) 

# create a base classifier used to evaluate a subset of attributes

# Recursively remove attributes and build a model on those attributes that remain, 
# using model accuracy to find attributes (combination of attributes)
model = LogisticRegression(penalty = 'l2')

# create the RFE model and list order of importance
rfe = RFE(model, 1)
rfe_fit = rfe.fit(x_norm, y)

# summarize the selection of the attributes
print(rfe_fit.support_)
print(rfe_fit.ranking_)


rfe_nameRank  = sorted(zip(map(lambda x: round(x, 4), rfe_fit.ranking_),var_names), reverse=False)
namesOrder = list()
for i in rfe_nameRank:
    namesOrder.append(i[1])
namesOrder



# Logistic regression model for prediction
# test/train split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=123)

# build model
lr = LogisticRegressionCV(cv = 5,
                          class_weight='balanced',
                          scoring='roc_auc',
                          max_iter=10000, verbose=0)
lr_fit = lr.fit(x_train, y_train)

pred = lr_fit.predict(x_test)

acc = pd.DataFrame()
acc['true_value'] = y_test
acc['predicted'] = pred
acc_wrong = acc[acc['true_value'] != acc['predicted']]

# computing sensitivity, specificity, AUC
fpr, tpr, thresholds = roc_curve(y_test, pred, pos_label = 0)
auc(fpr, tpr)
