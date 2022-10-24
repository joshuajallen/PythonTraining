import pandas as pd                                   # For dataframes
import numpy as np                                    # For various functions
import matplotlib.pyplot as plt                       # For plotting functions
import seaborn as sns                                 # For additional plotting functions
from sklearn.decomposition import PCA  # For PCA
from sklearn.model_selection import train_test_split  # For train/test splits
from sklearn.manifold import TSNE  # For tSNE
import os
from palmerpenguins import load_penguins  # For penguins dataset
from sklearn.cluster import AgglomerativeClustering      # For clustering
from scipy.cluster.hierarchy import dendrogram, linkage  # For clustering and visualization
from sklearn.model_selection import GridSearchCV     # For parameter optimization
from sklearn.neighbors import KNeighborsClassifier   # For kNN classification
from sklearn.metrics import plot_confusion_matrix    # Evaluation measure

base_dir = 'C:/Users/328576/source/python/'
df = pd.read_csv(os.path.join(base_dir, 'DataMining/data/optdigits_raw.csv'))
df.columns = ["P" + str(i) for i in range(0, len(df.columns) - 1)] + ["y"]
spam = pd.read_csv(os.path.join(base_dir, 'DataMining/data/spambase_raw.csv'), header=None)
# Imports the training data
trn = pd.read_csv(os.path.join(base_dir, 'DataMining/data/optdigits_trn.csv'))
# Separates the attributes P0-P63 into X_trn
X_trn = trn.filter(regex='\d')
# Separates the class variable into y_trn
y_trn = trn.y
# Imports the testing data
tst = pd.read_csv(os.path.join(base_dir, 'DataMining/data/optdigits_tst.csv'))
# Separates the attributes P0-P63 into X_tst
X_tst = tst.filter(regex='\d')

# Renames columns
X_trn, X_tst, y_trn, y_tst = train_test_split(
    df.filter(regex='\d'),
    df.y,
    test_size=0.30,
    random_state=1)

# Creates the training dataset, trn
trn = X_trn
trn["y"] = y_trn

# Creates the testing dataset, tst
tst = X_tst
tst["y"] = y_tst

# Sets up a grid for the images
fig, ax = plt.subplots(
    nrows=1,
    ncols=20,
    figsize=(15, 3.5),
    subplot_kw=dict(xticks=[], yticks=[]))

# Plots 20 digits
for i in np.arange(20):
    ax[i].imshow(X_trn.to_numpy()[i, 0:-1].reshape(8, 8), cmap=plt.cm.gray)

plt.show()

# Creates a grid using Seaborn's PairGrid()
g = sns.PairGrid(
    trn,
    vars=["P25", "P30", "P45", "P60"],
    hue="y",
    diag_sharey=False,
    palette=["red", "green", "blue"])

# Adds histograms on the diagonal
g.map_diag(plt.hist)

# Adds density plots above the diagonal
g.map_upper(sns.kdeplot)

# Adds scatterplots below the diagonal
g.map_lower(sns.scatterplot)

# Adds a legend
g.add_legend()

# PCA analysis

# Sets up the PCA object
pca = PCA()

# Transforms the training data ('tf' = 'transformed')
trn_tf = pca.fit_transform(X_trn)

# Plot the variance explained by each component
plt.plot(pca.explained_variance_ratio_)

# Plots the projected data set on the first two principal components and colors by class
sns.scatterplot(
    x=trn_tf[:, 0],
    y=trn_tf[:, 1],
    style=y_trn,
    hue=y_trn,
    palette=['red', 'green', 'blue'])

# Gets the average log likelihood score of training data (with two decimal places)
print("%.2f" % pca.score(X_trn))


# TSNSE

df = pd.read_csv(os.path.join(base_dir, 'DataMining/data/optdigits.csv'))
# Separates the attributes P0-P63 into X
X = df.filter(regex='\d')
# Separates the class variable into y
y = df.y

# Sets up the t-SNE object with 2 components
tsne = TSNE(
    n_components=2,
    random_state=1)

tsne.get_params()

# Sets up t-SNE with perplexity = 1
tsne = TSNE(
    n_components=2,
    perplexity=50,
    random_state=1)

# Transforms the attribute data
X_tf = tsne.fit_transform(X)

# Creates a scatterplot of the data embedding
sns.scatterplot(
    x=X_tf[:, 0],
    y=X_tf[:, 1],
    style=y,
    hue=y,
    palette=['red', 'green', 'blue'])


# clustering data

# Loads the penguins dataset
df = load_penguins()

# Drop variables and NaN cases, rename variable
df = df.drop(['island', 'year', 'sex'], axis=1) \
    .dropna() \
    .rename(columns={'species': 'y'})

sns.countplot(x='y', data=df)

df.to_csv(os.path.join(base_dir, 'DataMining/data/penguins.csv'), sep=',', index=False)
df = df.sample(n=75, random_state=1)
y = df.y

hc = linkage(df, method='ward', metric='euclidean')

# Sets the figure size
fig = plt.figure(figsize=(15, 15))

# Displays the dendogram
# The lambda function sets the labels of each leaf
dn = dendrogram(
    hc,
    leaf_label_func=lambda id: y.values[id],
    leaf_font_size=10)

# classification examples

spam.columns = ['X' + str(i) for i in range(0, len(spam.columns) - 1)] + ['y']
# Specifies X by filtering all columns with a number in name
X_trn, X_tst, y_trn, y_tst = train_test_split(
    df.filter(regex='\d'),
    df.y,
    test_size=0.30,
    random_state=1)

# Creates the training dataset, trn
trn = X_trn
trn['y'] = y_trn

# Creates the testing dataset, tst
tst = X_tst
tst['y'] = y_tst

sns.countplot(x='y', data=trn)

# KNN

# Imports the training data
trn = pd.read_csv(os.path.join(base_dir, 'DataMining/data/spambase_trn.csv'))
X_trn = trn.filter(regex='\d')
y_trn = trn.y
tst = pd.read_csv(os.path.join(base_dir, 'DataMining/data/spambase_tst.csv'))
X_tst = tst.filter(regex='\d')
y_tst = tst.y

# Class labels
spam = ['Not Spam','Spam']

knn = KNeighborsClassifier(n_neighbors=5) \
    .fit(X_trn, y_trn)

print(
    'Accuracy on training data: '
    + str("{:.2%}".format(knn.score(X_trn, y_trn))))

# Sets up the kNN classifier object
knn = KNeighborsClassifier()

# Search parameters
param = range(3, 15, 2)

# Sets up GridSearchCV object and stores it in grid variable
grid = GridSearchCV(
    knn,
    {'n_neighbors': param})

# Fits the grid object and gets the best model
best_knn = grid \
    .fit(X_trn,y_trn) \
    .best_estimator_

# Displays the optimum model
best_knn.get_params()

# Plots mean_test_scores vs. total neighbors
plt.plot(
    param,
    grid.cv_results_['mean_test_score'])

# Adds labels to the plot
plt.xticks(param)
plt.ylabel('Mean CV Score')
plt.xlabel('n_neighbors')

# Draws a vertical line where the best model is
plt.axvline(
    x=best_knn.n_neighbors,
    color='red',
    ls='--')

plot_confusion_matrix(
    best_knn, X_tst, y_tst,
    display_labels=spam,
    normalize='true')