import phonenumbers
from phonenumbers import carrier, is_valid_number, number_type, PhoneNumberType
from flask import Flask, request, jsonify
from config import CONFIG_NAME,config_by_name


app = Flask(__name__)
app.config.from_object(config_by_name[CONFIG_NAME]) 

PHONE_TYPE_MAP = {
    PhoneNumberType.MOBILE: "Mobile",
    PhoneNumberType.FIXED_LINE: "Fixe",
    PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixe ou mobile",
    PhoneNumberType.TOLL_FREE: "Numéro gratuit",
    PhoneNumberType.PREMIUM_RATE: "Numéro à tarification spéciale",
    PhoneNumberType.SHARED_COST: "Coût partagé",
    PhoneNumberType.VOIP: "VoIP",
    PhoneNumberType.PERSONAL_NUMBER: "Numéro personnel",
    PhoneNumberType.PAGER: "Bip",
    PhoneNumberType.UAN: "Numéro d'accès unifié",
    PhoneNumberType.VOICEMAIL: "Messagerie vocale",
}

@app.route('/verify', methods=['GET'])
def verify_number():
    phone_number = request.args.get('number')
    country_code = request.args.get('country_code', app.config["DEFAULT_COUNTRY_CODE"])

    if not phone_number:
        return jsonify({"error": "Numéro de téléphone requis"}), 400

    try:
        parsed_number = phonenumbers.parse(phone_number, country_code)

        if not is_valid_number(parsed_number):
            return jsonify({"valid": False, "error": "Numéro invalide"}), 400

        phone_carrier = carrier.name_for_number(parsed_number, "fr")

        line_type_str = PHONE_TYPE_MAP.get(number_type(parsed_number), "Inconnu")

        return jsonify({
            "valid": True,
            "number": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
            "carrier": phone_carrier,
            "type": line_type_str
        })

    except phonenumbers.phonenumberutil.NumberParseException:
        return jsonify({"valid": False, "error": "Numéro mal formaté"}), 400

if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"])
