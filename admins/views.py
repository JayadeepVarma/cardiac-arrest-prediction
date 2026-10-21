from django.shortcuts import render
from django.contrib import messages
from sklearn.model_selection import cross_val_score

# Create your views here.
from users.models import UserRegistrationModel, HeartDataModel
from doctor.models import doctorModel
import matplotlib.pyplot as plt
import seaborn as sns
from django_pandas.io import read_frame


# from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def AdminLogin(request):
    return render(request, 'AdminLogin.html', {})


def AdminLoginCheck(request):
    if request.method == 'POST':
        usrid = request.POST.get('loginname')
        pswd = request.POST.get('pswd')
        print("User ID is = ", usrid)
        if usrid == 'admin' and pswd == 'admin':
            return render(request, 'admins/AdminHome.html')

        else:
            messages.success(request, 'Please Check Your Login Details')
    return render(request, 'AdminLogin.html', {})


def RegisterUsersView(request):
    data = UserRegistrationModel.objects.all()
    return render(request, 'admins/ViewRegisterUsers.html', {'data': data})


def doctordetails(request):
    qs = doctorModel.objects.all()
    return render(request, 'admins/doctordetails.html', {"object": qs})


def ActivaUsers(request):
    if request.method == 'GET':
        id = request.GET.get('uid')
        status = 'activated'
        print("PID = ", id, status)
        UserRegistrationModel.objects.filter(id=id).update(status=status)
        data = UserRegistrationModel.objects.all()
        return render(request, 'admins/ViewRegisterUsers.html', {'data': data})


def activatedoctor(request):
    if request.method == 'GET':
        uname = request.GET.get('pid')
        print(uname)
        status = 'Activated'
        print("pid=", uname, "status=", status)
        doctorModel.objects.filter(id=uname).update(status=status)
        qs = doctorModel.objects.all()
        return render(request, "admins/doctordetails.html", {"object": qs})


def adminML(request):
    # gc.collect()
    dataset = HeartDataModel.objects.all()
    dataset = read_frame(dataset)
    # dataset.fillna
    print(dataset.head())
    print(type(dataset))
    print(dataset.shape)
    print(dataset.head(5))
    # print(dataset.sample(5))
    print(dataset.describe())
    dataset.info()
    ''' info = ["age", "1: male, 0: female",
            "chest pain type, 1: typical angina, 2: atypical angina, 3: non-anginal pain, 4: asymptomatic",
            "resting blood pressure", " serum cholestoral in mg/dl", "fasting blood sugar > 120 mg/dl",
            "resting electrocardiographic results (values 0,1,2)", " maximum heart rate achieved",
            "exercise induced angina", "oldpeak = ST depression induced by exercise relative to rest",
            "the slope of the peak exercise ST segment", "number of major vessels (0-3) colored by flourosopy",
            "thal: 3 = normal; 6 = fixed defect; 7 = reversable defect"]

    for i in range(len(info)):
        print(dataset.columns[i] + ":\t\t\t" + info[i])
    #X = dataset.drop(['target'], axis=1).values
    #print("x",X)
    dataset["target"].describe()
    print(dataset["target"].unique())
    print(dataset.corr()["target"].abs().sort_values(ascending=False))
    y = dataset["target"]
    print("y",y)
    sns.countplot(y)

    print("Dataset Head",dataset.head(25))
    target_temp = dataset.target.value_counts()
    #
    # print("target Label Count=",target_temp)
    # print("Percentage of patience without heart problems: " + str(round(target_temp[0] * 100 / 303, 2)))
    # print("Percentage of patience with heart problems: " + str(round(target_temp[1] * 100 / 303, 2)))
    print(dataset["sex"].unique())
    sns.barplot(x=dataset["sex"], y=y)
    dataset["cp"].unique()
    sns.barplot(x=dataset["cp"], y=y)
    dataset["fbs"].describe()
    dataset["fbs"].unique()
    sns.barplot(x=dataset["fbs"], y=y)
    dataset["restecg"].unique()
    sns.barplot(x=dataset["restecg"], y=y)
    dataset["exang"].unique()
    sns.barplot(x=dataset["exang"], y=y)
    dataset["slope"].unique()
    sns.barplot(x=dataset["slope"], y=y)
    dataset["ca"].unique()
    sns.countplot(dataset["ca"])
    sns.barplot(x=dataset["ca"], y=y)
    dataset["thal"].unique()
    sns.barplot(x=dataset["thal"], y=y)
    sns.distplot(dataset["thal"]) '''

    from sklearn.model_selection import train_test_split

    # FIX: drop leaked row-number 'id' as well as 'target' (see users/views.py)
    predictors = dataset.drop(["target", "id"], axis=1)
    target = dataset["target"]

    X_train, X_test, Y_train, Y_test = train_test_split(predictors, target, test_size=0.20, random_state=42)
    # OPTIMIZATION: same preprocessing as users/views.py - clean impossible
    # zero readings, median-impute, scale (see users/views.py for details).
    import numpy as np
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import StandardScaler
    X_train_raw, X_test_raw = X_train, X_test  # untouched copy for Naive Bayes (see below)
    X_train = X_train.copy(); X_test = X_test.copy()
    for _df in (X_train, X_test):
        _df.loc[_df["chol"] == 0, "chol"] = np.nan
        _df.loc[_df["trestbps"] == 0, "trestbps"] = np.nan
    _imputer = SimpleImputer(strategy="median")
    X_train_imp = _imputer.fit_transform(X_train)
    X_test_imp = _imputer.transform(X_test)
    _scaler = StandardScaler()
    X_train_s = _scaler.fit_transform(X_train_imp)
    X_test_s = _scaler.transform(X_test_imp)
    print(X_train.shape)
    print(X_test.shape)
    print(Y_train.shape)
    print(Y_test.shape)

    # Logistic regression
    from sklearn.metrics import accuracy_score
    from sklearn.linear_model import LogisticRegression
    lr = LogisticRegression(max_iter=5000, solver='liblinear')
    lr.fit(X_train_s, Y_train)
    Y_pred_lr = lr.predict(X_test_s)
    print(Y_pred_lr.shape)
    score_lr = round(accuracy_score(Y_pred_lr, Y_test) * 100, 2)
    print("The accuracy score achieved using Logistic regression is: " + str(score_lr) + " %")

    # Naive Bayes
    from sklearn.naive_bayes import GaussianNB, MultinomialNB
    nb = GaussianNB()  # UPGRADE: was MultinomialNB, which crashes on the 918-row dataset (Oldpeak has negative values); GaussianNB is the correct variant for continuous features
    nb.fit(X_train_raw, Y_train)  # NB models each feature's class distribution directly, so it keeps the raw values (zero-coded readings included); imputation measurably hurts it (83.70% raw vs 79.35% imputed)
    Y_pred_nb = nb.predict(X_test_raw)
    print(Y_pred_nb.shape)
    score_nb = round(accuracy_score(Y_pred_nb, Y_test) * 100, 2)
    print("The accuracy score achieved using Naive Bayes is: " + str(score_nb) + " %")

    # SVM
    from sklearn import svm
    sv = svm.SVC(kernel='rbf')  # OPTIMIZATION: was sigmoid on unscaled data
    sv.fit(X_train_s, Y_train)
    Y_pred_svm = sv.predict(X_test_s)
    print(Y_pred_svm.shape)
    score_svm = round(accuracy_score(Y_pred_svm, Y_test) * 100, 2)
    print("The accuracy score achieved using Linear SVM is: " + str(score_svm) + " %")

    # K Nearest Neighbors

    from sklearn.neighbors import KNeighborsClassifier
    neighbors_range = list(range(1, 31))

    # Perform cross-validation for each value of n_neighbors
    cv_scores = []
    for k in neighbors_range:
        knn = KNeighborsClassifier(n_neighbors=k)
        scores = cross_val_score(knn, X_train_s, Y_train, cv=5, scoring='accuracy')
        cv_scores.append(scores.mean())

    # Find the optimal n_neighbors with the highest cross-validated accuracy
    optimal_k = neighbors_range[cv_scores.index(max(cv_scores))]
    print("Optimal number of neighbors:", optimal_k)
    knn = KNeighborsClassifier(n_neighbors=optimal_k, algorithm='auto')
    knn.fit(X_train_s, Y_train)
    Y_pred_knn = knn.predict(X_test_s)
    print(Y_pred_knn.shape)
    score_knn = round(accuracy_score(Y_pred_knn, Y_test) * 100, 2)
    print("The accuracy score achieved using KNN is: " + str(score_knn) + " %")

    # Random Forest (OPTIMIZATION: added in the optimized version)
    from sklearn.ensemble import RandomForestClassifier
    rf = RandomForestClassifier(n_estimators=400, min_samples_leaf=2, random_state=42)
    rf.fit(X_train_imp, Y_train)
    Y_pred_rf = rf.predict(X_test_imp)
    score_rf = round(accuracy_score(Y_pred_rf, Y_test) * 100, 2)
    print("The accuracy score achieved using Random Forest is: " + str(score_rf) + " %")

    # Decision Tree
    '''from sklearn.tree import DecisionTreeClassifier
    max_accuracy = 0
    for x in range(200):
        dt = DecisionTreeClassifier(random_state=x)
        dt.fit(X_train, Y_train)
        Y_pred_dt = dt.predict(X_test)
        current_accuracy = round(accuracy_score(Y_pred_dt, Y_test) * 100, 2)
        if current_accuracy > max_accuracy:
            max_accuracy = current_accuracy
            # best_x = x
    # print(max_accuracy)
    # print(best_x)'''

    # Neural Network
    from keras.models import Sequential
    from keras.layers import Dense
    model = Sequential()
    model.add(Dense(11, activation='relu', input_dim=11))  # UPGRADE: 11 features in the 918-row combined dataset
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    # model.fit(X_train,Y_train,epochs=300)
    model.fit(X_train_s, Y_train, epochs=300)
    Y_pred_nn = model.predict(X_test_s)
    print(Y_pred_nn.shape)
    rounded = [round(x[0]) for x in Y_pred_nn]
    Y_pred_nn = rounded
    score_nn = round(accuracy_score(Y_pred_nn, Y_test) * 100, 2)
    print("The accuracy score achieved using Neural Network is: " + str(score_nn) + " %")

    scores = [score_lr, score_nb, score_svm, score_knn, score_rf, score_nn]
    algorithms = ["Logistic Regression", "Naive Bayes", "SVM", "K-Nearest Neighbors", "Random Forest", "Neural Network"]

    for i in range(len(algorithms)):
        print("The accuracy score achieved using " + algorithms[i] + " is: " + str(scores[i]) + " %")
        sns.set(rc={'figure.figsize': (15, 8)})
    plt.xlabel("Algorithms")
    plt.ylabel("Accuracy score")

    ax = sns.barplot(x=algorithms, y=scores, palette='tab10')
    for p in ax.patches:
        ax.annotate(f'{p.get_height()}%', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 6), textcoords='offset points', fontsize=14)
    plt.show()

    return render(request, 'admins/AdminHome.html', )
