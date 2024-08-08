# from flask import Flask, request, render_template
# import pandas as pd
# import pickle

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'nweub23y182u190ehnds189ye327yeh2ndiy12tey182eu28ehbds1879euj2nwd'  # Replace with a real secret key

# # Load the model
# model = pickle.load(open("flight_rf_main.pkl", "rb"))

# # Example feature lists used during training
# airlines = ['Jet Airways', 'IndiGo', 'Air India', 'Multiple carriers', 'SpiceJet', 'Vistara', 'Air Asia', 
#             'GoAir', 'Multiple carriers Premium economy', 'Jet Airways Business', 'Vistara Premium economy', 'Trujet']
# sources = ['Delhi', 'Kolkata', 'Mumbai', 'Chennai']
# destinations = ['Cochin', 'Delhi', 'New Delhi', 'Hyderabad', 'Kolkata']

# @app.route("/")
# def home():
#     return render_template("home.html")

# @app.route("/predict", methods=["POST"])
# def predict():
#     if request.method == "POST":
#         # Date_of_Journey
#         date_dep = request.form["Dep_Time"]
#         Journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
#         Journey_month = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").month)

#         # Departure
#         Dep_hour = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").hour)
#         Dep_min = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").minute)

#         # Arrival
#         date_arr = request.form["Arrival_Time"]
#         Arrival_hour = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").hour)
#         Arrival_min = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").minute)

#         # Duration
#         dur_hour = abs(Arrival_hour - Dep_hour)
#         dur_min = abs(Arrival_min - Dep_min)

#         # Total Stops
#         Total_stops = int(request.form["stops"])

#         # Airline
#         airline = request.form['airline']
#         airline_features = [1 if airline == x else 0 for x in airlines]

#         # Source
#         source = request.form["Source"]
#         source_features = [1 if source == x else 0 for x in sources]

#         # Destination
#         destination = request.form["Destination"]
#         destination_features = [1 if destination == x else 0 for x in destinations]

#         # Create feature array
#         inputs = [Total_stops, Journey_day, Journey_month, Dep_hour, Dep_min, Arrival_hour, Arrival_min, dur_hour, dur_min] + airline_features + source_features + destination_features

#         # Debug: Print the number of features and the features
#         print(f"Number of features provided: {len(inputs)}")
#         print(f"Features: {inputs}")

#         # Ensure the number of features matches the model's expectation
#         expected_features = len(airlines) + len(sources) + len(destinations) + 9  # Update this with the correct number of features
#         if len(inputs) != expected_features:
#             return render_template('home.html', prediction_text=f'Error: Expected {expected_features} features but got {len(inputs)} features.')

#         # Make the prediction using the model
#         prediction = model.predict([inputs])
        
#         # Render the prediction on the HTML page
#         return render_template('home.html', prediction_text=f'Predicted Flight Price: ₹{round(prediction[0], 2)}')

# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, request, render_template
from flask_wtf.csrf import CSRFProtect
import pickle
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nweub23y182u190ehnds189ye327yeh2ndiy12tey182eu28ehbds1879euj2nwd'  # Replace with a real secret key

# Load the model
model = pickle.load(open("flight_rf_main.pkl", "rb"))

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        try:
            # Date_of_Journey
            date_dep = request.form["Dep_Time"]
            Journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
            Journey_month = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").month)

            # Departure
            Dep_hour = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").hour)
            Dep_min = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").minute)

            # Arrival
            date_arr = request.form["Arrival_Time"]
            Arrival_hour = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").hour)
            Arrival_min = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").minute)

            # Duration
            dur_hour = abs(Arrival_hour - Dep_hour)
            dur_min = abs(Arrival_min - Dep_min)

            # Total Stops
            Total_stops = int(request.form["stops"])

            # Airline
            airline = request.form.get('airline', '')
            airlines = ['Jet Airways', 'IndiGo', 'Air India', 'Multiple carriers', 'SpiceJet', 
                        'Vistara', 'GoAir', 'Multiple carriers Premium economy', 
                        'Jet Airways Business', 'Vistara Premium economy', 'Trujet']
            airline_features = [1 if airline == x else 0 for x in airlines]

            # Source
            source = request.form.get("Source", '')
            sources = ['Delhi', 'Kolkata', 'Mumbai', 'Chennai']
            source_features = [1 if source == x else 0 for x in sources]

            # Destination
            destination = request.form.get("Destination", '')
            destinations = ['Cochin', 'Delhi', 'New Delhi', 'Hyderabad', 'Kolkata']
            destination_features = [1 if destination == x else 0 for x in destinations]

            # Create feature array
            features = [Total_stops, Journey_day, Journey_month, Dep_hour, Dep_min, 
                        Arrival_hour, Arrival_min, dur_hour, dur_min] + \
                       airline_features + source_features + destination_features

            # Ensure the number of features matches the model's expectation
            expected_features = len(airlines) + len(sources) + len(destinations) + 9
            if len(features) != expected_features:
                return render_template('home.html', prediction_text=f'Error: Expected {expected_features} features but got {len(features)} features.')

            # Make prediction
            prediction = model.predict([features])
            output = round(prediction[0], 2)

            return render_template('home.html', prediction_text=f"Your Flight price is Rs. {output}")

        except Exception as e:
            return render_template('home.html', prediction_text=f"Error: {str(e)}")

    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
