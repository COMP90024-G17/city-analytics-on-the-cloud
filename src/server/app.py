from flask import Flask, request, url_for, jsonify, make_response, abort
import json
from flask_cors import CORS
from utils import city_info_loader

app = Flask(__name__)
CORS(app, resources=r'/*')

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/api/statistic', methods=['GET'])
def get_statistic_api():
    # http://0.0.0.0:3000/api/statistic?city=melbourne
    city = request.args.get('city')
    return _safeGetCityDataWithFunc(city, city_info_loader.safe_load_all_data_of)


@app.route('/api/v2.0/map/city/<string:city>', methods=['GET'])
def get_map(city):
    # http://0.0.0.0:3000/api/v2.0/map/city/melbourne
    return _safeGetCityDataWithFunc(city, city_info_loader.safe_load_map_of)


@app.route('/api/v2.0/analysis/city/<string:city>', methods=['GET'])
def get_city_analysis(city):
    # http://0.0.0.0:3000/api/v2.0/analysis/city/melbourne
    return _safeGetCityDataWithFunc(city, city_info_loader.safe_load_city_analysis_of)


@app.route('/api/v2.0/analysis/suburbs-of-city/<string:city>', methods=['GET'])
def get_suburbs_analysis(city):
    # http://0.0.0.0:3000/api/v2.0/analysis/suburbs-of-city/melbourne
    return _safeGetCityDataWithFunc(city, city_info_loader.safe_load_suburbs_analysis_of)


@app.route('/api/v2.0/data/<string:city>', methods=['GET'])
def get_all_data(city):
    # http://0.0.0.0:3000/api/v2.0/data/melbourne
    return _safeGetCityDataWithFunc(city, city_info_loader.safe_load_all_data_of)

@app.route('/api/v2.0/analysis/city-level/all', methods=['GET'])
def get_all_city_analysis():
    # http://0.0.0.0:3000/api/v2.0/analysis/city-level/all
    return jsonify(city_info_loader.safe_load_all_cities_analysis())


@app.route('/api/v2.0/analysis/suburb-level/all', methods=['GET'])
def get_all_analysis():
    # http://0.0.0.0:3000/api/v2.0/analysis/suburb-level/all
    return jsonify(city_info_loader.safe_load_all_analysis())
    
# Use to handle bad request and not found request
def _safeGetCityDataWithFunc(city, func):
    if (city == None):
        abort(400)
    res = func(city)
    if (res == {}):
        abort(404)
    return jsonify(res)

if __name__ == '__main__':
    app.run(debug=True, port=3000, host='0.0.0.0')
