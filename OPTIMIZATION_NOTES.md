# Optimization Notes — Heart_918_Optimized (final version)

Base: Heart_Upgraded_918 (918-record combined dataset, 11 features).
Decision made 2026-10-20: apply every verified improvement and add the
strongest model, completing the extended/portfolio version of the project.
The original academic version (303 records, submitted report, published
IJAEMA paper) is unchanged.

## Changes (users/views.py and admins/views.py, UserMachineLearning / adminML)
1. Zero-cleaning: cholesterol == 0 (172 rows) and trestbps == 0 (1 row) are
   "not recorded" in the source data -> treated as missing and filled with
   the training-set median (SimpleImputer).
2. Feature scaling: StandardScaler fitted on the training split, applied to
   Logistic Regression, SVM, KNN and the Neural Network.
3. SVM kernel changed sigmoid -> RBF.
4. Random Forest added as a 7th model: 400 trees, min_samples_leaf=2,
   random_state=42. The ML results template now also displays the Decision
   Tree row (previously commented out) and the new Random Forest row.
5. Naive Bayes exception: it trains on the RAW values on purpose — GaussianNB
   models each feature's class distribution, and median imputation measurably
   hurt it (83.70% raw vs 79.35% imputed in testing).

## Measured effect (same seed-42 80/20 split, scores from the app's ML page)
| Model | Before (918) | After (optimized) |
|---|---|---|
| Random Forest | — (not present) | **88.04%** |
| SVM | 44.02% (sigmoid, unscaled) | 85.87% (RBF, scaled) |
| Neural Network | 83.70% | 85.87% |
| Logistic Regression | 83.15% | 85.33% |
| K-Nearest Neighbors | 64.67% | 84.78% |
| Naive Bayes (Gaussian) | 83.70% | 83.70% |
| Decision Tree | 79.89% | 81.52% |

Verified end-to-end in the app (Django test client): home, User/Admin/Doctor
logins, user ML page (all seven scores rendered), admin ML page, and
prediction (disease sample -> result.html, healthy sample -> results1.html)
all return 200 with correct outputs. manage.py check: no issues.
A soft-voting ensemble was also tested offline (85.33% on this split, 86.17%
±2.23 in 5-fold cross-validation) but not added — the single Random Forest
beat it on the app split and keeps the app simple and explainable.
