from flask import Flask,request,jsonify
from flask_cors import CORS
import recommendation

app = Flask(__name__)
CORS(app)

@app.route('/perfume', methods=['GET'])
def recommend_perfumes():
    res = recommendation.results(request.args.get('features'))
    return jsonify(res)


if __name__ == '__main__':
    app.run(port=5000, debug=True)