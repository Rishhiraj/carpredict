from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import svm

app = Flask(__name__)

# Load your dataset
car_ds = pd.read_csv('car_data.csv')

# Convert 'Gender' to 0 and 1
car_ds['Gender'] = car_ds['Gender'].map({'Male': 1, 'Female': 0})

# Drop the 'User ID' feature
car_ds = car_ds.drop(columns='User ID')

# Separate the data and label
X = car_ds.drop(columns='Purchased')
Y = car_ds['Purchased']

# Standardize the data
scaler = StandardScaler()
scaler.fit(X)
standardized_data = scaler.transform(X)

# Train-Test Split
X_train, X_test, Y_train, Y_test = train_test_split(standardized_data, Y, test_size=0.2, stratify=Y, random_state=2)

# Training the model
classifier = svm.SVC(kernel='linear')
classifier.fit(X_train, Y_train)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()  # Get JSON data from the request
        if 'gender' in data and 'age' in data and 'annualIncome' in data:
            gender = data['gender']
            age = float(data['age'])
            annualIncome = float(data['annualIncome'])

            # Map gender to integer values
            gender_mapping = {'male': 1, 'female': 0}
            gender = gender_mapping.get(gender.lower())

            if gender is not None:
                # Standardize the user input
                input_data = [gender, age, annualIncome]

                # Make predictions
                prediction = classifier.predict([input_data])

                return jsonify({'prediction': int(prediction[0])})
            else:
                return jsonify({'error': 'Invalid gender input. Please enter "male" or "female".'})
        else:
            return jsonify({'error': 'Invalid request data. Required fields are missing.'})
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
