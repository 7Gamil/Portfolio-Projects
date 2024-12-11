# Handle Imbalanced Dataset
Used the [Indian Liver Patient Imbalanced Dataset](https://archive.ics.uci.edu/dataset/225/ilpd+indian+liver+patient+dataset)

## Steps
* Address imbalanced data using SMOTE-ENN
* Utilize GridSearchCV and k-Fold Cross Validation for model validation 
  * Train K-Nearest Neighbors (K-NN)
  * Train Random Forest
  * Train XGBoost
 
## Hyperparameters

**SMOTE-ENN:**
- SMOTE nearest neighbors = `3, 5, 7`
- ENN nearest neighbors = `3, 5, 7`

**k-NN:**
- Nearest neighbors = `1, 3, 5, ..., 𝑘𝑚𝑎𝑥`
  where `𝑘𝑚𝑎𝑥` ≤ √(number of training data)

**Random Forest:**
- n estimators = `1, 2, 3, ..., 200`
- criterion = `‘gini’, ‘entropy’`

**Extreme Gradient Boosting (XGBoost):**
- n estimators = `1, 2, 3, ..., 150`
- subsample = `0.7, 0.8, 0.9`
- depth = `3, 4, 5, ..., 30, 31`

Please check `Handle Imbalanced Dataset.ipynb` Jupyter file for more details.

## Prerequisites
Before using Jupyter notebook, ensure you have installed the required libraries
`pip install -r requirments.txt`