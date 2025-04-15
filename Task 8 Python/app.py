from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load model
model = joblib.load("logistic_model.pkl")

# Load X_train columns - replace with your actual way of loading them
X_train_columns = joblib.load("X_train_columns.pkl")

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    clean_product_names = [col.replace("Product_", "").replace("_", " ") for col in X_train_columns if col.startswith('Product_')]

    if request.method == 'POST':
        try:
            quantity = float(request.form['quantity'])
            product = request.form['product']

            # Build input data with all product columns set to 0
            input_data = {col: 0 for col in X_train_columns}

            # Set the appropriate product column to 1
            full_col = f"Product_{product.replace(' ', '_')}"
            if full_col in input_data:
                input_data[full_col] = 1
            else:
                raise ValueError("Invalid product name entered.")

            # Add raw quantity
            input_data['Quantity'] = quantity

            # Convert to DataFrame and predict
            input_df = pd.DataFrame([input_data])
            prediction = model.predict(input_df)[0]

        except Exception as e:
            prediction = f"Error: {e}"

    return render_template('index.html', prediction=prediction, products=clean_product_names)

if __name__ == '__main__':
    app.run(debug=True)