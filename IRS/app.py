import json
from db.dbstore import DBStore
from semantic.logic import SemanticLogic
from utils.system_utils import calc_mean_score
from utils.system_settings import SystemSettings
from flask import Flask, jsonify, request, Response
from request_handler.req_handler import RequestHandler
from utils.system_security import RequestSecurityChecks


app = Flask(__name__)
@app.route('/drug_system', methods=['POST'])
def drug_system():
    # Intialize Object classes
    req_handler = RequestHandler()
    semantics = SemanticLogic()
    db_manager = DBStore()
    req_security = RequestSecurityChecks()

    # Get Request from Data
    drug_query_requests = request.get_json()

    # Pass request for security checks
    req_security.set_request(drug_query_requests)

    # if the request data does not tally with the expected formats
    if not req_security.run_request_secruity_check():
        system_response = {"message":SystemSettings.BAD_REQUEST_DATA_CONFIGURATION}
        return Response(response=json.dumps(system_response), status=400, mimetype='application/json')

    # return the pass request data, with possible augmentation
    drug_query_requests = req_security.return_passed_request()

    req_handler.set_request(drug_query_requests)
    system_results = req_handler.prepare_request()
    embedding_results = semantics.get_n_results(system_results["embed_query"], system_results["n_results"])

    
    score = calc_mean_score(embedding_results)

    # When the score is zero it means the user set n_results to 0
    if score == 0 :
        return Response(response=json.dumps(SystemSettings.NO_RESPONSE), status=200, mimetype='application/json')
    # Based on testing, when the system gets queries that have nothing to do with drugs in the data store, the probality score is always lower than the defined threshold.
    elif score < SystemSettings.THRESHOLD_SCORE:
        system_response = {"message":SystemSettings.LOW_PROBABLITY}
        return Response(response=json.dumps(system_response), status=200, mimetype='application/json') 

    user_results = db_manager.extract_drug_information(embedding_results, system_results["filters"])

    return Response(response=json.dumps(user_results), status=200, mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5000)