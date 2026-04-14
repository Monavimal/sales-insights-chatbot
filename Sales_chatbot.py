from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load dataset once
df = pd.read_excel("sales_data.xlsx")

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True)

    if not req:
        return jsonify({"fulfillmentText": "No request received"})

    intent = req.get('queryResult', {}).get('intent', {}).get('displayName', '').lower()

    # 🔹 TOTAL SALES
    if intent == "total_sales":
        total = df['Sales'].sum()
        return jsonify({
            "fulfillmentText": f"Total sales is ₹{int(total):,}"
        })

    # 🔹 TOP PRODUCT
    elif intent == "top_products":
        top_product = df.groupby('Product')['Sales'].sum().idxmax()
        return jsonify({
            "fulfillmentText": f"Top product is {top_product}"
        })

    # 🔹 SALES BY REGION
    elif intent == "sales_by_region":
        region_sales = df.groupby('Region')['Sales'].sum()
        result = "\n".join([f"{region}: ₹{int(value):,}" for region, value in region_sales.items()])
        return jsonify({
            "fulfillmentText": f"Sales by region:\n{result}"
        })

    # 🔹 GREETING
    elif intent == "greet":
        return jsonify({
            "fulfillmentText": "Hello! Ask me about sales 📊"
        })

    else:
        return jsonify({
            "fulfillmentText": "Sorry, I didn't understand"
        })

if __name__ == '__main__':
    app.run(port=5000)