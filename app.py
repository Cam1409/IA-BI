from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
from ia_sistema import predecir_clase_gbot, obtener_respuesta_gbot, intenciones_gbot
from etl import etl_process 

app = Flask(__name__)

cors = CORS(app, resources={r"/chatbot": {"origins": "http://localhost:3004"},
                            r"/run_etl_process": {"origins": "http://localhost:3004"}})


@app.route('/chatbot', methods=['POST'])
def chatbot():
    try:
        content = request.get_json()
        user_input = content['message']
        
        intents_list = predecir_clase_gbot(user_input)
        
        response = obtener_respuesta_gbot(intents_list, intenciones_gbot)
    
        return jsonify({"response": response})
    
    except KeyError:
        return jsonify({"error": "Campo 'message' no encontrado en la solicitud"}), 400
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/run_etl_process', methods=['GET'])
def run_etl_process():
    try:
        result = etl_process()
        
        return jsonify({'message': 'Proceso ETL ejecutado exitosamente', 'result': result}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
