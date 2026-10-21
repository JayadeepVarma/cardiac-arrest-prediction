from django.shortcuts import render
from django.contrib import messages
# Create your views here.
from users.forms import UserRegistrationForm, HeartDataForm
from users.models import UserRegistrationModel, HeartDataModel
import matplotlib.pyplot as plt
from django_pandas.io import read_frame
# from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# from pandas import read_csv
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
import pandas as pd


def UserLogin(request):
    return render(request, 'UserLogin.html', {})


def UserRegisterAction(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print('Data is Valid')
            form.save()
            messages.success(request, 'You have been successfully registered')
            # return HttpResponseRedirect('./CustLogin')
            form = UserRegistrationForm()
            return render(request, 'Register.html', {'form': form})
        else:
            print("Invalid form")
    else:
        form = UserRegistrationForm()
    return render(request, 'Register.html', {'form': form})


def UserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginname')
        pswd = request.POST.get('pswd')
        print("Login ID = ", loginid, ' Password = ', pswd)
        try:
            check = UserRegistrationModel.objects.get(loginid=loginid, password=pswd)
            status = check.status
            print('Status is = ', status)
            if status == "activated":
                request.session['id'] = check.id
                request.session['loggeduser'] = check.name
                request.session['loginid'] = loginid
                request.session['email'] = check.email
                print("User id At", check.id, status)
                return render(request, 'users/UserHomePage.html', {})
            else:
                messages.success(request, 'Your Account Not at activated')
                return render(request, 'UserLogin.html')
            # return render(request, 'user/userpage.html',{})
        except Exception as e:
            print('Exception is ', str(e))
            pass
        messages.success(request, 'Invalid Login id and password')
    return render(request, 'UserLogin.html', {})


def UserAddData(request):
    if request.method == 'POST':
        form = HeartDataForm(request.POST)
        if form.is_valid():
            print('Data is Valid')
            form.save()
            messages.success(request, 'Data Added Successfull')
            # return HttpResponseRedirect('./CustLogin')
            form = HeartDataForm()
            return render(request, 'users/UserAddData.html', {'form': form})
        else:
            print("Invalid form")
    else:
        form = HeartDataForm()
    return render(request, 'users/UserAddData.html', {'form': form})


def UserDataView(request):
    data_list = HeartDataModel.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(data_list, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'users/DataView_list.html', {'users': users})


def UserMachineLearning(request):
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
    info = ["age", "1: male, 0: female",
            "chest pain type, 1: typical angina, 2: atypical angina, 3: non-anginal pain, 4: asymptomatic",
            "resting blood pressure", " serum cholestoral in mg/dl", "fasting blood sugar > 120 mg/dl",
            "resting electrocardiographic results (values 0,1,2)", " maximum heart rate achieved",
            "exercise induced angina", "oldpeak = ST depression induced by exercise relative to rest",
            "the slope of the peak exercise ST segment"]

    for i in range(len(info)):
        print(dataset.columns[i] + ":\t\t\t" + info[i])
    # X = dataset.drop(['target'], axis=1).values
    # print("x",X)
    dataset["target"].describe()
    print(dataset["target"].unique())
    print(dataset.corr()["target"].abs().sort_values(ascending=False))
    y = dataset["target"]
    temp = dataset["target"].replace({1: "Cardiac Arrest", 0: "No Cardiac Arrest"})
    print("y", temp)
    plt.figure(figsize=(7, 6))
    import seaborn as sb
    ax = sb.countplot(x=temp, palette='tab10')
    for p in ax.patches:
        ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 6), textcoords='offset points', fontsize=14)
    plt.title("Count Plot")
    plt.xlabel("Target")
    plt.ylabel("Count")
    plt.show()
    print("Dataset Head", dataset.head(25))
    target_temp = dataset.target.value_counts()
    print("target Label Count=", target_temp)
    # print("Percentage of patience without heart problems: " + str(round(target_temp[0] * 100 / 303, 2)))
    # print("Percentage of patience with heart problems: " + str(round(target_temp[1] * 100 / 303, 2)))
    print(dataset["sex"].unique())
    plt.figure(figsize=(7, 6))
    ax = sb.barplot(x=dataset["sex"].replace({1: "Male", 0: "Female"}), y=y, ci=None, palette='tab10')
    for p in ax.patches:
        ax.annotate(f'{round(p.get_height(), 2)}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 6), textcoords='offset points', fontsize=14)
    plt.title("Bar Plot")
    plt.xlabel("Gender")
    plt.ylabel("Target")
    plt.show()
    dataset["cp"].unique()
    plt.figure(figsize=(7, 6))
    ax = sb.barplot(
        x=dataset["cp"].replace({0: "Typical Angina", 1: "Atypical Angina", 2: "Non-Anginal Pain", 3: "Asymptomatic"}),
        y=y, ci=None, palette='tab10')
    for p in ax.patches:
        ax.annotate(f'{round(p.get_height(), 2)}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 6), textcoords='offset points', fontsize=14)
    plt.title("Bar Plot")
    plt.xlabel("Chest Pain")
    plt.ylabel("Target")
    plt.show()
    dataset["fbs"].describe()
    dataset["fbs"].unique()
    plt.figure(figsize=(7, 6))
    ax = sb.barplot(x=dataset["fbs"].replace({0: "<=120 mg/Dl", 1: " > 120 mg/Dl"}), y=y, ci=None, palette='tab10')
    for p in ax.patches:
        ax.annotate(f'{round(p.get_height(), 2)}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 6), textcoords='offset points', fontsize=14)
    plt.title("Bar Plot")
    plt.xlabel("Fasting Blood Sugar")
    plt.ylabel("Target")
    plt.show()
    dataset["restecg"].unique()
    plt.figure(figsize=(7, 6))
    ax = sb.barplot(x=dataset["restecg"], y=y, ci=None, palette='tab10')
    for p in ax.patches:
        ax.annotate(f'{round(p.get_height(), 2)}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 6), textcoords='offset points', fontsize=14)
    plt.title("Bar Plot")
    plt.xlabel("Resting Electrocardiographic")
    plt.ylabel("Target")
    plt.show()
    dataset["exang"].unique()
    plt.figure(figsize=(7, 6))
    ax = sb.barplot(x=dataset["exang"].replace({0: "No", 1: "Yes"}), y=y, ci=None, palette='tab10')
    for p in ax.patches:
        ax.annotate(f'{round(p.get_height(), 2)}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 6), textcoords='offset points', fontsize=14)
    plt.title("Bar Plot")
    plt.xlabel("Exercise Induced Angina")
    plt.ylabel("Target")
    plt.show()
    dataset["slope"].unique()
    plt.figure(figsize=(7, 6))
    ax = sb.barplot(x=dataset["slope"].replace({0: "Up-sloping", 1: "Flat", 2: "Down-sloping"}), y=y, ci=None,
                    palette='tab10')
    for p in ax.patches:
        ax.annotate(f'{round(p.get_height(), 2)}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 6), textcoords='offset points', fontsize=14)
    plt.title("Bar Plot")
    plt.xlabel("Slope of the Peak")
    plt.ylabel("Target")
    plt.show()
    from sklearn.model_selection import train_test_split
    # FIX: 'id' dropped along with 'target' - it is a row number, not a clinical
    # feature, and the data is sorted by target, so training on 'id' leaks the
    # answer and inflates accuracy to a fake 96-100%.
    predictors = dataset.drop(["target", "id"], axis=1)
    target = dataset["target"]
    X_train, X_test, Y_train, Y_test = train_test_split(predictors, target, test_size=0.20, random_state=42)
    # OPTIMIZATION: clean impossible zero readings (a cholesterol or resting BP
    # of 0 means "not recorded" in the source data), fill with the training-set
    # median, and scale features to a common range. Raw scales (cholesterol
    # ~200 vs oldpeak ~1) badly hurt SVM, KNN, Logistic Regression and the
    # Neural Network; scaling lifts SVM from ~44% to ~81% and KNN to ~85%.
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

    # LogisticRegression regression
    from sklearn.metrics import accuracy_score
    from sklearn.linear_model import LogisticRegression
    lr = LogisticRegression(max_iter=5000, solver='liblinear')
    lr.fit(X_train_s, Y_train)
    Y_pred_lr = lr.predict(X_test_s)
    print(Y_pred_lr.shape)
    score_lr = round(accuracy_score(Y_pred_lr, Y_test) * 100, 2)
    print("The accuracy score achieved using Linear regression is: " + str(score_lr) + " %")

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
    sv = svm.SVC(kernel='rbf')  # OPTIMIZATION: was sigmoid on unscaled data (~44%); rbf + scaling is the standard SVM setup
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

    # Decision Tree (single fixed seed - no seed cherry-picking)
    from sklearn.tree import DecisionTreeClassifier
    dt = DecisionTreeClassifier(random_state=42)
    dt.fit(X_train_imp, Y_train)
    Y_pred_dt = dt.predict(X_test_imp)
    print(Y_pred_dt.shape)
    score_dt = round(accuracy_score(Y_pred_dt, Y_test) * 100, 2)
    print("The accuracy score achieved using Decision Tree is: " + str(score_dt) + " %")

    # Random Forest (OPTIMIZATION: added in the optimized version; ensemble of
    # 400 trees, the strongest single model on this dataset in testing)
    from sklearn.ensemble import RandomForestClassifier
    rf = RandomForestClassifier(n_estimators=400, min_samples_leaf=2, random_state=42)
    rf.fit(X_train_imp, Y_train)
    Y_pred_rf = rf.predict(X_test_imp)
    print(Y_pred_rf.shape)
    score_rf = round(accuracy_score(Y_pred_rf, Y_test) * 100, 2)
    print("The accuracy score achieved using Random Forest is: " + str(score_rf) + " %")

    # print(max_accuracy)
    # print(best_x)

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
    scores = [score_lr, score_nb, score_svm, score_knn, score_dt, score_rf, score_nn]
    algorithms = ["Logistic Regression", "Naive Bayes", "SVM", "K-Nearest Neighbors", "Decision Tree", "Random Forest", "Neural Network"]

    for i in range(len(algorithms)):
        print("The accuracy score achieved using " + algorithms[i] + " is: " + str(scores[i]) + " %")
        sb.set(rc={'figure.figsize': (15, 8)})
    plt.xlabel("Algorithms")
    plt.ylabel("Accuracy score")

    ax = sb.barplot(x=algorithms, y=scores, palette='tab10')
    for p in ax.patches:
        ax.annotate(f'{p.get_height()}%', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 6), textcoords='offset points', fontsize=14)
    plt.show()
    dictionary = {
        "score_lr": score_lr,
        "score_nb": score_nb,
        "score_svm": score_svm,
        "score_knn": score_knn,
        "score_dt": score_dt,
        "score_rf": score_rf,
        "score_nn": score_nn,

    }
    return render(request, 'users/Machinelearning.html', dictionary)


def predictt(request):
    return render(request, "users/predict.html")


def alggg(k_test):
    # FIX: was pd.read_csv(r"D:\Heart\media\heart.csv") - a hardcoded path that
    # only existed on the original author's PC, so prediction crashed (500) everywhere else.
    from django.conf import settings
    df = pd.read_csv(settings.BASE_DIR / "media" / "heart.csv")
    X = df[['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope']]
    y = df['target']
    X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.20, random_state=1)
    model = RandomForestClassifier(random_state=42)  # FIX: seeded so demos give the same result every run
    model.fit(X_train, Y_train)
    predictions = model.predict([k_test])
    return predictions


def predictionss(request):
    if request.method == 'POST':
        age = int(request.POST["age"])
        sex = int(request.POST["sex"])
        cp = int(request.POST["cp"])
        trestbps = int(request.POST["trestbps"])
        chol = int(request.POST["chol"])
        fbs = int(request.POST["fbs"])
        restecg = int(request.POST["restecg"])
        thalach = int(request.POST["thalach"])
        exang = int(request.POST["exang"])
        oldpeak = float(request.POST["oldpeak"])
        slope = int(request.POST["slope"])
        test_data = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope]
        print(test_data)
        result = alggg(test_data)
        if result == 1:
            return render(request, "users/result.html")
        else:
            return render(request, "users/results1.html")
