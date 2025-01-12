from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import numpy as np
from sklearn.linear_model import LinearRegression

app = Flask(__name__)
CORS(app)

# Mock database of sneakers
SNEAKER_DB = {
    "nike": {
        "air-force-1": {
            "name": "Nike Air Force 1",
            "base_price": 130,
            "variants": [
                {
                    "sku": "CW2288-111",
                    "color": "White/White",
                    "release_date": "2020-11-25"
                },
                {
                    "sku": "CT2302-002",
                    "color": "Black/Black",
                    "release_date": "2020-12-07"
                }
            ]
        },
        "air-jordan-1": {
            "name": "Nike Air Jordan 1",
            "base_price": 170,
            "variants": [
                {
                    "sku": "555088-134",
                    "color": "University Blue/White",
                    "release_date": "2021-03-06"
                },
                {
                    "sku": "555088-063",
                    "color": "Shadow 2.0",
                    "release_date": "2021-05-15"
                }
            ]
        }
    },
    "adidas": {
        "ultraboost": {
            "name": "Adidas Ultraboost",
            "base_price": 180,
            "variants": [
                {
                    "sku": "FY2298",
                    "color": "Core Black/Core Black/Active Red",
                    "release_date": "2020-12-02"
                },
                {
                    "sku": "FY2900",
                    "color": "Cloud White/Cloud White/Core Black",
                    "release_date": "2020-12-02"
                }
            ]
        },
        "yeezy-boost-350-v2": {
            "name": "Adidas Yeezy Boost 350 V2",
            "base_price": 220,
            "variants": [
                {
                    "sku": "FZ5000",
                    "color": "Ash Pearl",
                    "release_date": "2021-03-20"
                },
                {
                    "sku": "GW3773",
                    "color": "Beluga Reflective",
                    "release_date": "2021-12-18"
                }
            ]
        }
    }
}

def generate_price_history(base_price, days=90):
    dates = [(datetime.now() - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(days, -1, -1)]
    # Generate slightly random prices with an upward trend
    volatility = base_price * 0.15  # 15% volatility
    trend = base_price * 0.001  # 0.1% daily trend
    prices = [base_price + i * trend + np.random.normal(0, volatility) for i in range(len(dates))]
    return [{"date": date, "price": max(round(price, 2), 0)} for date, price in zip(dates, prices)]

def predict_future_price(history_data, days=30):
    X = np.arange(len(history_data)).reshape(-1, 1)
    y = np.array([d["price"] for d in history_data])
    model = LinearRegression()
    model.fit(X, y)
    
    future_dates = [(datetime.now() + timedelta(days=x)).strftime('%Y-%m-%d') for x in range(1, days+1)]
    future_X = np.arange(len(history_data), len(history_data) + days).reshape(-1, 1)
    predictions = model.predict(future_X)
    
    return [{"date": date, "price": max(round(price, 2), 0)} for date, price in zip(future_dates, predictions)]

@app.route('/api/sneakers', methods=['GET'])
def get_sneakers():
    return jsonify(SNEAKER_DB)

@app.route('/api/market-data', methods=['GET'])
def get_market_data():
    brand = request.args.get('brand', 'nike')
    model = request.args.get('model', 'dunk-low')
    
    if brand not in SNEAKER_DB or model not in SNEAKER_DB[brand]:
        return jsonify({"error": "Sneaker not found"}), 404
        
    sneaker = SNEAKER_DB[brand][model]
    history = generate_price_history(sneaker["base_price"])
    predictions = predict_future_price(history)
    
    return jsonify({
        "status": "success",
        "data": {
            "sneaker": sneaker,
            "history": history,
            "predictions": predictions,
            "statistics": {
                "current_price": history[-1]["price"],
                "price_change_7d": round((history[-1]["price"] - history[-7]["price"]) / history[-7]["price"] * 100, 2),
                "price_change_30d": round((history[-1]["price"] - history[-30]["price"]) / history[-30]["price"] * 100, 2),
                "highest_price": max(h["price"] for h in history),
                "lowest_price": min(h["price"] for h in history)
            }
        },
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("Server starting on http://localhost:8000")
    app.run(debug=True, host='0.0.0.0', port=8000)