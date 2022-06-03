from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from colect import data_by_city, data_by_location
from list_to_dict import list_to_dict
from current_aqi import current_aqi_prov

app = Flask(__name__)
  
# load model
model = load_model("Model/lstm_6_3_e50/my_model.h5")

@app.route("/")
def index():
  return "Welcome to Airmonitor Forecast APIs"

# /by_city?city=Jakarta&key=8ad9eca88a2e4330a022ad816a7d9886
@app.route("/by_city")
def by_city():
  kota = request.args.get('city', default = "Jakarta", type = str)
  weatherbit_key = request.args.get('key', default = "8ad9eca88a2e4330a022ad816a7d9886", type = str)
  # collect data
  a = data_by_city(kota, weatherbit_key)

  # scaling and reshape
  scaler = MinMaxScaler()
  data = scaler.fit_transform(a)
  data = data.reshape(1,6,7)

  # predictions
  predictions = model.predict(data)
  predictions = predictions.reshape(3,7)
  predictions = scaler.inverse_transform(predictions)
  predictions = predictions.tolist()
  predictions = list_to_dict(predictions)
  
  # history last 3 hour
  history = a[:3]
  history = history.values.tolist()
  history = list_to_dict(history)

  #return f'{predictions}'
  return f"forecast for the next 3 hours in {kota} is \n\n\n {predictions} \n\n\n history last 3 hours is {history}"

# /by_location?lat=35&lon=-78&key=8ad9eca88a2e4330a022ad816a7d9886
@app.route("/by_location")
def by_location():
  lat = request.args.get('lat', default = 35, type = float)
  lon = request.args.get('lon', default = -78, type = float)
  weatherbit_key = request.args.get('key', default = "8ad9eca88a2e4330a022ad816a7d9886", type = str)

  # collect data
  a = data_by_location(lat, lon, weatherbit_key)

  # scaling and reshape
  scaler = MinMaxScaler()
  data = scaler.fit_transform(a)
  data = data.reshape(1,6,7)

  # predictions
  predictions = model.predict(data)
  predictions = predictions.reshape(3,7)
  predictions = scaler.inverse_transform(predictions)
  predictions = predictions.tolist()
  predictions = list_to_dict(predictions)
  
  # history last 3 hour
  history = a[:3]
  history = history.values.tolist()
  history = list_to_dict(history)

  #return jsonify(predictions)
  return f"forecast for the next 3 hours in lat {lat}is \n\n\n {predictions} \n\n\n history last 3 hours is {history}"

# /current?key=8ad9eca88a2e4330a022ad816a7d9886
@app.route("/current")
def current():
  weatherbit_key = request.args.get('key', default = "8ad9eca88a2e4330a022ad816a7d9886", type = str)

  data = current_aqi_prov(weatherbit_key)
  #data = list_to_dict(data)
    
  return f'{data}'

if __name__ == "__main__":
    app.run()