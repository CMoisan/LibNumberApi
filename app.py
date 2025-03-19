from flask import Flask, request, jsonify
from config import CONFIG_NAME, config_by_name
from verification import PhoneNumberVerifier

app = Flask(__name__)
app.config.from_object(config_by_name[CONFIG_NAME])

@app.route('/verify', methods=['GET'])
def verify_number():
    phone_number = request.args.get('number')
    country_code = request.args.get('country_code', "FR")

    if not phone_number:
        return jsonify({"error": "Numéro de téléphone requis"}), 400

    verifier = PhoneNumberVerifier(country_code)
    result = verifier.verify(phone_number)

    return jsonify(result.pop("result")), result.pop("status_code")

if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"])
