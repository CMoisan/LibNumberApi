import phonenumbers
from phonenumbers import carrier, is_valid_number, number_type, PhoneNumberType
import yaml

# Chargement de la config YAML
with open("config.yaml", "r", encoding="utf-8") as file:
    COUNTRY_CONFIG = yaml.safe_load(file)["countries"]

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

class PhoneNumberVerifier:
    def __init__(self, country_code):
        self.country_code = country_code
        self.config = COUNTRY_CONFIG.get(country_code, COUNTRY_CONFIG["FR"])  # Par défaut, FR

    def verify(self, phone_number):
        full_number = f"{self.config['default_country_code']}{phone_number}"
        
        try:
            parsed_number = phonenumbers.parse(full_number, self.country_code)

            if not is_valid_number(parsed_number):
                return {
                    "result" :{
                        "valid": False,
                        "error": "Numéro invalide",
                    },
                    "status_code": 400
                }

            phone_carrier = carrier.name_for_number(parsed_number, "fr")
            line_type_str = PHONE_TYPE_MAP.get(number_type(parsed_number), "Inconnu")

            return {
                "result" :{
                    "valid": True,
                    "number": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                    "carrier": phone_carrier,
                    "type": line_type_str,
                },
                "status_code" : 200
            }
        except phonenumbers.phonenumberutil.NumberParseException:
            return {
                "result" :{
                    "valid": False,
                    "error": "Numéro mal formaté",
                },
                "status_code": 400
            }
