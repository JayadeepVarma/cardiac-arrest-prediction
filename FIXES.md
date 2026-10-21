# ALL FIXES — Cardiac Arrest Prediction Project
Consolidated list from a full audit (Oct 2026) of every project file: 4 code versions,
the report chapters, paper, published journal version, review decks, screenshots and poster.
Base version used: **Heart (New)** — the only good-to-go copy.

## A. CODE FIXES — ✅ already applied in this repo
1. **Prediction crashed on every PC except the author's.**
   `users/views.py` read the dataset from hardcoded `D:\Heart\media\heart.csv`.
   → Now `settings.BASE_DIR / "media" / "heart.csv"`. Verified: prediction HTTP 500 → 200.
2. **Data leak inflating accuracy to 96–100%.**
   Training used the row-number `id` column as a predictor, and the dataset is sorted
   by target (id↔target correlation −0.86), so the model was cheating.
   → `id` dropped in `users/views.py` **and** `admins/views.py`.
3. **Neural network input size wrong after the leak fix.**
   `Dense(..., input_dim=14)` counted the leaked `id`. → Corrected to **13** real features.
4. **Decision Tree score was always blank.**
   The template expects `score_dt`, but the DT code was commented out — and the original
   version cherry-picked the best of 200 random seeds to inflate its score.
   → Restored as a single honest `DecisionTreeClassifier(random_state=42)`; score now displays.
5. **Non-reproducible results.** ML train/test split and the prediction Random Forest
   had no seed, so scores/predictions changed every run. → Seeded (`random_state=42`).
6. **Broken on modern seaborn.** `seaborn.distplot` was removed in seaborn ≥ 0.14.
   → Replaced with `histplot(..., kde=True)`.
7. **Unusable requirements.** ~60 unpinned package names (mostly TensorFlow transitive deps).
   → Pinned, minimal `requirements.txt` with only what the code imports
   (Django 5.0.1, scikit-learn 1.4.2, TensorFlow 2.16.2, Keras 3.3.3, …).
8. **Repo hygiene.** Removed `.idea/` and all `__pycache__/*.pyc`; added `.gitignore`.

### Verified after fixes (test-run end-to-end)
- `python manage.py check` → **0 issues**
- Home / User / Admin / Doctor login / Predict / DataView pages → **all 200**
- Prediction → correct result pages both ways (arrest / not arrest)
- ML page → 200, all six scores rendered

### Honest verified scores (80/20 split, seed 42, 13 features)
| Algorithm | Accuracy |
|---|---|
| Logistic Regression | **86.89%** |
| Naive Bayes | 85.25% |
| Neural Network (Keras) | 83.61% |
| Decision Tree | 75.41% |
| K-Nearest Neighbors | 65.57% |
| SVM (sigmoid) | 52.46% |

SVM/KNN are low because features are never scaled — known improvement, not hidden.

## B. VERSION DECISIONS — ✅ already decided for you
- **Heart (Backup) Original — DO NOT USE.** Database is empty (0 records); ML and DataView are dead.
- **Heart (Old) — DO NOT USE.** Django 2.2-era, ancient pinned deps that won't install today,
  304 DB rows including one stray test row (age 12).
- **Heart (New) — the base.** Django 5.0.1, exactly 303 DB rows, latest work (May 2024).
- **Heart.zip (re-sent during the audit) — ignore.** It is the fixed version re-zipped under
  the folder name "Heart" with the older short README; this repo folder supersedes it.

## C. DOCUMENT / CONTENT FIXES — ⚠️ YOU must apply these wherever you still use the old text
1. **Resume — Cardiac project description is wrong.** It claims "neonates, 5,000+ newborn
   records, 92% accuracy, ~30% faster emergency response." The code/data support none of that
   (UCI adult heart dataset, 303 records). Replace with: UCI Heart Disease dataset (303 records),
   6 ML models compared, best Logistic Regression 86.89%, Django web app with User/Doctor/Admin roles.
2. **Resume — add your publication (currently missing).**
   "Predictive Analytics for Cardiac Arrest Identification in Neonates with Machine Learning
   Framework", IJAEMA, ISSN 0886-9367, Vol XV Issue XII, Dec 2023, p.599.
3. **Resume — add the GitHub repo link** after you push (recruiters check it).
4. **Poster / infographic — do not publish as-is.** It repeats the same unsupported claims
   (5,000 records, 92%, 30% response-time reduction, a doctor-alert popup and "standardization"
   that don't exist in the code, and a decorative fake confusion matrix). Either correct the
   numbers/features to the verified ones above, or keep it only as a college poster.
5. **Report CONCLUSION says "KNN is best" — wrong.** On the verified run KNN is 65.57% and
   Logistic Regression is best (86.89%). Don't quote the conclusion's claim in interviews/viva prep
   without this correction.
6. **Report MODULES says "73% training / 37% testing" — typo** (sums to 110%). The code uses 80/20.
7. **Old Abstract.docx and INTRODUCTION.docx are copied** from Singh & Kumar, ICE3-2020
   ("Heart Disease Prediction Using Machine Learning Algorithms"). Do not reuse that text publicly;
   your own abstract is Abstract_new (= your paper's abstract) — already used in the README.
8. **SAMPLE_CODE.docx is outdated** (old Django 2.2 code, KNN n=7, seed-cherry-picked DT).
   The repo code replaces it — never copy code from that document.
9. **Literature survey / bibliography contain an irrelevant "Swarm Robotics" entry**
   (template filler). Already removed from the README references; remove it anywhere else you reuse them.

## D. FILE-BY-FILE: WHAT GOES TO GITHUB
**Upload (already packaged in this repo):**
- Fixed code (this folder), `README.md`, `FIXES.md`, `requirements.txt`, `.gitignore`
- `docs/Published_Paper_IJAEMA_2023.pdf` — your published paper
- `docs/diagrams/` — system design diagrams extracted from SYSTEM_DESIGN.docx

**Never upload publicly (keep private):**
- The two external papers (Singh & Kumar 2020; Gupta et al. IEEE Access 2023) — cite them, don't host them
- SCREENSHOTS docx images — from a 2020 demo, showing other people's names, mobile numbers, email
  → use fresh screenshots captured from the fixed app instead
- Phase-1 paperwork: consent form, E6 Major Project Certificate, review formats
- Review decks (Phase I & II, Reviews 1–3) and review PPTs — internal college material
- E6 similarity report (30% overall) — internal
- Instruction_For_Documentation.docx + documentation_format.docx — college templates
- ROAD_SHOW_FEED_BACK.pdf — internal feedback form
- Full report docx/pdf — optional; if you want it public, the published paper already covers it

## E. WHEN YOU PUSH IT YOURSELF (later)
```bash
unzip Heart_GitHub_Ready.zip   # or use this folder directly
cd Heart_New_Fixed
git init -b main
git add -A
git commit -m "Cardiac arrest prediction Django app — fixed, verified results"
gh auth login                       # one-time, your account
gh repo create cardiac-arrest-prediction --public --source=. --push
```
Suggested repo name: **cardiac-arrest-prediction**, **public** (recruiters must be able to open it).
After pushing, add the repo URL to your resume project section (see C3).
