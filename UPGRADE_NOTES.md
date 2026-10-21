# UPGRADE NOTES — 303 → 918 records

This copy upgrades the fixed project from the 303-record UCI Cleveland dataset to the
918-record combined "Heart Failure Prediction" dataset (fedesoriano, Kaggle, Sep 2021),
compiled from five public sources — Cleveland (303), Hungarian (294), Switzerland (123),
Long Beach VA (200), Statlog (270) = 1,190 raw rows, 272 duplicates removed → **918 records**
(508 with heart disease, 410 without). The original fixed 303-record version is untouched.

## What had to change, and why
1. **Feature set: 13 → 11.** The combined dataset shares only 11 features; it has no
   `ca` (major vessels) or `thal` (thallium test). Removed from: the Django model
   (`HeartDataModel`, migration `users/0002`), the data-entry form, the prediction form
   (`predict.html`, `predictions.html`, `UserAddData.html`), the DataView table, the
   prediction view, and the ML code. Neural-network `input_dim` 13 → 11.
2. **Category encoding mapped to the app's existing codes** (so all labels/help text stay valid):
   Sex M/F → 1/0 · ChestPainType TA/ATA/NAP/ASY → 0/1/2/3 · RestingECG Normal/ST/LVH → 0/1/2 ·
   ExerciseAngina N/Y → 0/1 · ST_Slope Up/Flat/Down → 0/1/2.
   Converted file: `media/heart.csv`; original published form: `media/heart_918_original.csv`.
3. **Naive Bayes: MultinomialNB → GaussianNB.** The combined dataset's `Oldpeak` contains
   negative values, which MultinomialNB mathematically cannot accept (the app crashed).
   GaussianNB is the correct variant for continuous clinical features.
4. **Admin ML split seed aligned 0 → 42**, so admin and user ML pages report identical scores.
5. **Database rebuilt**: fresh migrations, 918 records loaded (508 target=1). User/doctor
   accounts start empty in this copy (register new ones; admin login is still admin/admin).

## Verified results on the 918-record dataset (80/20 split, seed 42, app's own ML page)
| Algorithm | Accuracy |
|---|---|
| Naive Bayes (Gaussian) | **83.70%** |
| Neural Network (Keras) | 83.70% |
| Logistic Regression | 83.15% |
| Decision Tree | 79.89% |
| K-Nearest Neighbors | 64.67% |
| SVM (sigmoid) | 44.02% |

End-to-end tested: Django check clean; home/user/admin/doctor pages, data-entry form,
DataView (918 records), user + admin ML pages and prediction all return 200; prediction
verified correct both ways on real dataset records. SVM/KNN remain low for the same known
reason as before — the original code never scales features (documented improvement).

## Honest data notes
- 172 records have Cholesterol = 0 and 1 has RestingBP = 0 in the published dataset
  (a known artifact of the source data — effectively unrecorded readings). They are kept
  exactly as published; nothing was silently altered.
- These are still **adult** patient records from the same public sources. A bigger adult
  dataset does not make the project a neonatal study.
- The published IJAEMA paper and the submitted college report describe the ORIGINAL
  303-record project and remain its correct historical record. This upgrade is an
  extended version for portfolio/GitHub use; if asked, describe it exactly that way.
