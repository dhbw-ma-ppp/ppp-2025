import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import matthews_corrcoef

#Loading the Data using pandas
data = pd.read_csv('data/titanic.csv')

#Analysing if any values are missing
print("Missing Values:\n", data.isnull().sum())

#Visualising the data that is missing, using Seaborn Library (Extension on Matplotlib)
sns.heatmap(data.isnull(), cbar=False)
plt.title("Missing Values")
plt.show()

#Visualising the difference of two data sets colliding with each other -> shows their dependancies to each other
corr = data.corr(numeric_only=True)
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title("Dependancy Heatmap")
plt.show()

#Survival by Sex and Pclassf
sns.barplot(x='Sex', y='Survived', data=data)
plt.title("Survival Rate by Sex")
plt.show()

#Second part of the exercise
#Drop the columns (discard) that isnt important because Cabin Data mostly misses and Ticket and Name isnt very important in the survived data
data = data.drop(['Cabin', 'Ticket', 'Name'], axis=1)
#Split the dataset Survived with all the others ones because thats what were targeting
X = data.drop('Survived', axis=1)
y = data['Survived']

#Split numerical columns and columns made of chars
categorical_cols = ['Sex', 'Embarked'] #chars
numeric_cols = [col for col in X.columns if col not in categorical_cols] #numerical, all the other ones except for Sex and Embarked and Survival

#Filling in missing values with the median
numeric_transformer = SimpleImputer(strategy='median')
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

#Apply the right value (numerical or categorical) to each column type
preprocessor = ColumnTransformer([
    ('num', numeric_transformer, numeric_cols),
    ('cat', categorical_transformer, categorical_cols)
])

#Create the Model
model = RandomForestClassifier(random_state=42)
#Create a pipeline and put the preprocessing of the data from above and the Model in the same pipeline, so it works together (Data gets seperated and prepared first, then the model is trained)
clf = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', model)
])

#Train_test_split of the Model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Training the model and finding the matthew corrcoef
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
mcc = matthews_corrcoef(y_test, y_pred)
print("MCC:", mcc)
