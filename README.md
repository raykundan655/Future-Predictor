# Future Predictor

![Future Predictor Banner](https://via.placeholder.com/1200x400?text=Future+Predictor+AI) <!-- Replace with actual banner image if available -->

**Future Predictor** is a full-stack web application that harnesses AI and machine learning to deliver predictions and recommendations across education, finance, and entertainment domains. The backend, built with Flask, integrates pre-trained machine learning models for tasks such as student performance prediction, job placement analysis, budget optimization, and movie recommendations. The frontend, powered by Next.js, provides a modern, responsive interface with smooth navigation, form handling, and dynamic result displays.

## Features
- **Education Predictions**:
  - **Student Performance**: Predicts academic performance using study patterns and historical data.
  - **Placement Analysis**: Evaluates job placement likelihood based on academic and professional metrics.
- **Financial Intelligence**:
  - **Budget Analysis**: Clusters spending patterns and offers personalized savings recommendations.
- **Entertainment Recommendations**:
  - **Movie Recommendations**: Suggests movies based on genre similarity using TF-IDF and cosine similarity.
- **Technical Highlights**:
  - Stateless API with pickled ML models for efficient inference.
  - Responsive frontend with form validation, loading states, and result redirection.
  - Modular preprocessing pipelines using scikit-learn's `Pipeline` and `ColumnTransformer`.

## Table of Contents
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Usage](#usage)
  - [Running the Application](#running-the-application)
  - [API Endpoints](#api-endpoints)
  - [Frontend Features](#frontend-features)
- [ML Models and Preprocessing](#ml-models-and-preprocessing)
- [Dataset Requirements](#dataset-requirements)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Tech Stack

### Backend
- **Python 3.8+**: Core programming language.
- **Flask 3.1.1**: Lightweight web framework for API endpoints.
- **scikit-learn 1.6.1**: Machine learning models (RandomForest, KMeans, TF-IDF, etc.).
- **pandas 2.2.3 & numpy 2.2.2**: Data manipulation and preprocessing.
- **pickle**: Serialization of trained models.
- **flask-cors 6.0.1**: Cross-origin resource sharing for frontend-backend communication.

### Frontend
- **HTML5, CSS3, JavaScript (Vanilla)**: The frontend is a static web interface built with modern responsive design.
- **Custom Script (script.js)**: Handles API calls to the Flask backend and manages form submissions, validations, and result redirection.
- **Responsive UI**: Designed with mobile-first principles, featuring smooth navigation, form handling, and interactive result displays.
- **Results Page (results.html)**: Dynamically displays predictions and recommendations retrieved from the backend, styled with modern CSS.


### Tools
- **Git**: Version control.
- **Postman**: Recommended for API testing.
- **No Database**: Application is stateless; models are loaded from pickle files.

## Project Structure

```
future-predictor/
├── backend/
│   ├── app.py                       # Flask app with API endpoints
│   ├── req.txt                      # Python dependencies
│── preprocessing/               # ML training scripts
│   │   ├── Budgetrecommendations.py # KMeans clustering for budget analysis
│   │   ├── MoveRecommendation.py    # TF-IDF movie recommendation
│   │   ├── PlacementAnalysis.py     # BaggingClassifier for placement prediction
│   │   ├── StudentPerformanceAnalysis.py # RandomForest for student performance
│   │   └── StudentScore(Practice).py    # Additional practice script
│   └── models/                      # Pickled ML models (generated)
│       ├── StudentPerformance.pkl
│       ├── placementAnalysis.pkl
│       ├── BudgetScale.pkl
│       └── BudgetClusterModel.pkl
├── frontend/
│   ├── package.json                 # Node.js dependencies
│   ├── script.js                   # Client-side JavaScript for API calls and UI logic
│   ├── index.html                  # Main landing page
│   ├── results.html                # Prediction results page
│   ├── styles.css                  # Global CSS styles
│   └── public/                     # Static assets (e.g., images)
├── README.md                       # This file
└── .gitignore                      # Git ignore file
```

Note: The `preprocessing/` folder contains scripts to train models and generate pickle files. Run these scripts if you need to retrain models with new data.

## Installation

### Backend Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/raykundan655/future-predictor.git
   cd future-predictor/backend
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r req.txt
   ```

4. **Prepare ML Models**:
   - Ensure pickled models (`StudentPerformance.pkl`, `placementAnalysis.pkl`, `BudgetScale.pkl`, `BudgetClusterModel.pkl`) are in the `backend/models/` directory.
   - To regenerate models, run the respective scripts in `preprocessing/` with appropriate datasets.

### Frontend Setup
1. **Navigate to Frontend**:
   ```bash
   cd ../frontend
   ```

2. **Install Dependencies**:
   ```bash
   npm install
   ```

3. **Configure API URL**:
   - Open `script.js` and verify the `API_BASE_URL`:
     ```javascript
     const API_BASE_URL = "http://127.0.0.1:5000"; // Update if deploying
     ```

## Usage

### Running the Application

1. **Start Backend**:
   ```bash
   cd backend
   python app.py
   ```
   - Runs on `http://127.0.0.1:5000` with debug mode enabled.
   - Ensure models are in the `models/` directory.

2. **Start Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```
   - Runs on `http://localhost:3000`.
   - Access `index.html` via the Next.js dev server or serve statically.

3. **Interact with the App**:
   - Visit `http://localhost:3000` in a browser.
   - Select a category (Education, Finance, Entertainment).
   - Fill out the form for the desired prediction (e.g., Student Performance, Budget Analysis).
   - Submit to view results on `results.html` (stored in `localStorage`).

### API Endpoints
Test endpoints using Postman or curl. All POST endpoints expect JSON payloads; the movie recommendation uses a GET query parameter.

| Endpoint                     | Method | Description                          | Input Example                                                                 | Output Example                                                                 |
|------------------------------|--------|--------------------------------------|-------------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| `/`                          | GET    | Welcome message                     | None                                                                          | `"welcome to Future Predictor"`                                                |
| `/placementPrediction`       | POST   | Predict job placement               | `{"CGPA": 7.5, "Internships": 1, ...}`                                        | `{"prediction": "Placed"}`                                                     |
| `/Studentperformance`        | POST   | Predict student performance         | `{"Hours Studied": 5, "Previous Scores": 85, ...}`                            | `{"prediction": 82.5}`                                                        |
| `/BudgetAnalysis`            | POST   | Budget recommendations              | `{"Eating_Out": 3000, "Disposable_Income": 6000, ...}`                        | `{"recommendation": {"Cluster": 2, "Status": "Not meeting savings goal", ...}}` |
| `/moveRecommendation?title={title}` | GET    | Movie recommendations         | `?title=Inception`                                                            | `{"input_movie": "Inception", "recommendations": ["Interstellar", "Memento"]}` |

**Error Handling**: Returns `400` with `{"error": "message"}` for invalid/missing fields or server errors.

### Frontend Features
- **Navigation**: Smooth scrolling to sections (Home, Services, Contact).
- **Forms**: Client-side validation for required fields and numeric inputs.
- **Loading Modal**: Displays during API calls for better UX.
- **Results Page**: Displays predictions stored in `localStorage` on `results.html`.
- **Responsive Design**: Mobile-friendly with Tailwind CSS and media queries.
- **UI Components**: Leverages Radix UI for accessible forms, dropdowns, and modals.

## ML Models and Preprocessing
The backend uses pre-trained models stored as pickle files, created via scripts in `preprocessing/`:
1. **Student Performance (`StudentPerformanceAnalysis.py`)**:
   - Model: RandomForestRegressor (`n_estimators=200, max_depth=7`).
   - Preprocessing: `Pipeline` with `ColumnTransformer` (`StandardScaler` for numeric, `OneHotEncoder` for categorical).
   - Features: Hours Studied, Previous Scores, Extracurricular Activities, etc.
2. **Placement Analysis (`PlacementAnalysis.py`)**:
   - Model: BaggingClassifier with DecisionTreeClassifier (`n_estimators=300, max_depth=5`).
   - Preprocessing: Similar `Pipeline` setup.
   - Features: CGPA, Internships, AptitudeTestScore, etc.
3. **Budget Recommendations (`Budgetrecommendations.py`)**:
   - Model: KMeans (`n_clusters=4`).
   - Preprocessing: `StandardScaler` for spending features.
   - Logic: Custom `recommend_savings` function for actionable insights.
4. **Movie Recommendations (`MoveRecommendation.py`)**:
   - Model: TF-IDF vectorization + cosine similarity.
   - Features: Movie genres (`expanded-genres` column).

Run preprocessing scripts to retrain models if datasets change. Outputs are saved as `.pkl` files.

## Dataset Requirements
The following datasets are required to train models (place in `backend/`):
- **Student Performance**: `Student_Performance.csv` (columns: Hours Studied, Previous Scores, Performance Index, etc.).
- **Placement Analysis**: `placementdata.csv` (columns: CGPA, Internships, PlacementStatus, etc.).
- **Budget Analysis**: `data.csv` (columns: Eating_Out, Disposable_Income, Desired_Savings, etc.).
- **Movie Recommendations**: Hugging Face dataset `jquigl/imdb-genres` (loaded via pandas).

For movie recommendations, authenticate with Hugging Face CLI:
```bash
huggingface-cli login
```

## Deployment
### Backend
- Deploy to platforms like Heroku, PythonAnywhere, or AWS.
- Use Gunicorn for production:
  ```bash
  pip install gunicorn
  gunicorn --workers 3 app:app
  ```
- Set environment variable for model paths if needed.

### Frontend
- Deploy to Vercel or Netlify:
  ```bash
  cd frontend
  npm run build
  vercel --prod
  ```
- Update `API_BASE_URL` in `script.js` to point to the deployed backend URL.

### Notes
- Ensure CORS is configured correctly (`flask-cors` handles this).
- Use HTTPS in production for security.
- Monitor with Vercel Analytics (optional, configured in `package.json`).

## Contributing
We welcome contributions! Follow these steps:
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit changes: `git commit -m "Add feature"`.
4. Push to the branch: `git push origin feature-name`.
5. Open a Pull Request.

Please adhere to:
- **Code Style**: PEP8 for Python, ESLint for JavaScript.
- **Testing**: Test API endpoints and frontend forms before submitting.
- **Issues**: Report bugs or suggest features via GitHub Issues.

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Contact
- **Developer**: Kundan Kr Ray
- **Email**: [mahiray655@gmail.com](mailto:mahiray655@gmail.com)
- **GitHub**: [raykundan655](https://github.com/raykundan655)
- **LinkedIn**: [raykundan655](https://linkedin.com/in/raykundan655)
- **Phone**: +91 700******5

For questions, bug reports, or collaboration opportunities, open an issue or contact the developer directly.

---

*Built with ❤️ by Kundan Kr Ray. Powered by AI, Flask, and Next.js.*
