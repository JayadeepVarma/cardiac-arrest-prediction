# HOW TO RUN THIS PROJECT
**Cardiac Arrest Prediction — Django + Machine Learning (final optimized version: 918 records, 7 models, best accuracy 88.04%)**

Follow these steps in order. Everything below is for the **final version** of the code:
- If you downloaded **Heart_918_Optimized.zip** → unzip it and open the `Heart_918_Optimized` folder.
- If you downloaded **Heart_Project_Complete.zip** → unzip it and open `Heart Disease\Project FIle\Heart`.

That folder (the one containing `manage.py`) is the project folder. All commands below are run inside it.

---

## Step 1 — Install Python (one time only)
- Python **3.11 or 3.12** (the project was verified on Python 3.12; 3.11 also works — that is the installer in your project files).
- During installation on Windows, tick **"Add python.exe to PATH"**.
- Check it worked: open Command Prompt and type `python --version`

## Step 2 — Open a terminal in the project folder
- Windows: open the project folder in File Explorer, click the address bar, type `cmd`, press Enter. A Command Prompt opens already inside the folder.
- (macOS/Linux: open Terminal and `cd` into the project folder.)

## Step 3 — Create a virtual environment (one time only)
```
python -m venv venv
```
Activate it:
- Windows: `venv\Scripts\activate`
- macOS/Linux: `source venv/bin/activate`

You should now see `(venv)` at the start of the line. Do this activation every time you open a new terminal for this project.

## Step 4 — Install the required packages (one time only)
```
pip install -r requirements.txt
```
This installs Django 5.0.1, pandas, scikit-learn, TensorFlow/Keras and the rest.
**Note:** TensorFlow is a large download (a few hundred MB) — this step can take several minutes on a slow connection. That is normal.

## Step 5 — Prepare the database (one time only)
```
python manage.py migrate
```
The project already ships with `db.sqlite3` containing all **918 patient records**, so this is just a safety check — it should say most migrations are already applied ("OK" / no changes needed). **Do not delete `db.sqlite3`** — the patient data lives in it. User and doctor accounts start empty (see Step 7).

## Step 6 — Start the server
```
python manage.py runserver
```
Open your browser and go to: **http://127.0.0.1:8000/**

You should see the home page ("CARDIAC ARREST"). Leave the terminal running while you use the app. To stop the server later: press **Ctrl + C** in the terminal.

---

## Step 7 — Logins: how the accounts work
There are three modules. **New User and Doctor accounts cannot log in until the Admin activates them** — this is by design.

**Admin (works immediately):**
- Go to **Admin Login** and sign in with username `admin`, password `admin`.
- The Admin can view registered users/doctors and **activate** them.

**User (do this once):**
1. Go to **User Register** and fill the form (choose any login ID and password), submit.
2. Log in as **Admin** (above), open the registered-users page, and **activate** your user account.
3. Log out of Admin, go to **User Login**, and sign in with your login ID and password.

**Doctor (same pattern):**
1. Register on the **Doctor Register** page.
2. As Admin, open doctor details and activate the doctor.
3. Sign in on the **Doctor Login** page using the doctor's **email** and password.

## Step 8 — What to try inside the app (User login)
- **Add Data** — adds one patient record (11 values: age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope). Codes are the same as the dataset (e.g. sex: 1 = male, 0 = female; cp: 0–3).
- **Data View** — shows the patient records from the database, 10 per page (918 records are pre-loaded).
- **Machine Learning** — trains all 7 models live and shows their accuracies. **This page takes about 30–60 seconds to open** because the models (including the neural network) are trained fresh on every visit — that delay is normal, not a hang. Expected scores:

  | Model | Accuracy |
  |---|---|
  | Random Forest | **88.04%** |
  | SVM (RBF) | 85.87% |
  | Neural Network | 85.87% |
  | Logistic Regression | 85.33% |
  | K-Nearest Neighbors | 84.78% |
  | Naive Bayes | 83.70% |
  | Decision Tree | 81.52% |

  (The Neural Network score may differ slightly on some runs, e.g. 85.33% — its starting weights are not seeded. All other scores are identical every run.)
- **Predictions** — enter one patient's 11 values and submit. You get one of two result pages: **"OUTPUT PREDICTED AS CARDIAC ARREST"** or **"OUTPUT PREDICTED AS NOT CARDIAC ARREST"**.
  - Try this sample (a disease record from the dataset): age 49, sex 0, cp 2, trestbps 160, chol 180, fbs 0, restecg 0, thalach 156, exang 0, oldpeak 1.0, slope 1 → **Cardiac Arrest**
  - Try this sample (a healthy record): age 40, sex 1, cp 1, trestbps 140, chol 289, fbs 0, restecg 0, thalach 172, exang 0, oldpeak 0.0, slope 0 → **Not Cardiac Arrest**

## Data files (inside the project folder)
- `db.sqlite3` — the database (918 patient records + accounts).
- `media\heart.csv` — the same 918 records as a CSV file; the **Prediction** feature reads this file directly.
- `media\heart_918_original.csv` — the dataset in its original published form (kept for reference; the app does not use it).

---

## Troubleshooting
| Problem | Fix |
|---|---|
| `python` is not recognized | Reinstall Python and tick "Add python.exe to PATH", or use `py` instead of `python` in the commands. |
| `No module named 'django'` | You forgot Step 3's activation. Run `venv\Scripts\activate`, then `pip install -r requirements.txt`. |
| "That port is already in use" | Another server is running. Stop it (Ctrl+C in its terminal) or run `python manage.py runserver 8001` and open http://127.0.0.1:8001/ |
| Machine Learning page is slow | Normal — models train live (30–60 s). Don't refresh repeatedly; each refresh restarts the training. |
| Login says account not activated | Log in as Admin and activate the account first (Step 7). |
| Prediction page shows an error | Make sure all 11 fields are filled with numbers, and that `media\heart.csv` is present in the project folder. |

---
*Verified end-to-end on the final code (October 2026): all pages load, both prediction samples give the results shown above, and the Machine Learning page shows exactly the scores in the table.*
