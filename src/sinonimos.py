# -*- coding: utf-8 -*-
"""
Diccionario de sinónimos / palabras clave para la búsqueda "inteligente" de
la app web.

La app ya busca por código y por nombre exacto del diagnóstico. Este
archivo agrega una tercera vía de búsqueda: términos coloquiales,
abreviaturas médicas y síntomas comunes que el personal usa en la práctica
diaria pero que no coinciden textualmente con el nombre oficial del CIE-10.
Por ejemplo, buscar "dolor de pecho" o "IAM" debe encontrar el código I21.9
(infarto agudo del miocardio) aunque esas palabras no estén en su nombre
oficial.

Cada entrada es: "término de búsqueda" -> [lista de códigos CIE-10].
Los códigos se validan contra data/catalogo.json al importar este módulo
(igual que especialidades.py), así que un código mal escrito se reporta
como error en vez de fallar en silencio.

No hace falta que los términos estén acentuados de forma consistente ni en
minúsculas: la búsqueda en la app normaliza (minúsculas, sin acentos) tanto
la consulta del usuario como estas llaves antes de compararlas.
"""
import json
from pathlib import Path

CATALOGO_PATH = Path(__file__).resolve().parent.parent / "data" / "catalogo.json"

with open(CATALOGO_PATH, encoding="utf-8") as f:
    CAT = json.load(f)


def chk(code):
    c = CAT.get(code)
    if not c:
        return None
    return c['nombre']


# término coloquial / abreviatura -> [códigos CIE-10]
SYNONYMS = {
    # --- Abreviaturas y siglas médicas de uso diario ---
    "iam": ["I219"],
    "infarto": ["I219"],
    "ataque al corazon": ["I219"],
    "evc": ["I639"],
    "acv": ["I639"],
    "embolia cerebral": ["I639"],
    "derrame cerebral": ["I639"],
    "isquemia cerebral": ["I639"],
    "hta": ["I10X"],
    "presion alta": ["I10X"],
    "tension alta": ["I10X"],
    "dm2": ["E119"],
    "dm": ["E119"],
    "diabetes": ["E119"],
    "azucar alta": ["E149"],
    "glucosa alta": ["E149"],
    "epoc": ["J449"],
    "erc": ["N189"],
    "irc": ["N189"],
    "insuficiencia renal": ["N189"],
    "ivu": ["N390"],
    "itu": ["N390"],
    "infeccion urinaria": ["N390"],
    "infeccion de orina": ["N390"],
    "tvp": ["I803"],
    "trombosis": ["I803", "I269"],
    "tep": ["I269"],
    "embolia pulmonar": ["I269"],
    "ic": ["I500"],
    "icc": ["I500"],
    "insuficiencia cardiaca": ["I500"],
    "sica": ["I219"],
    "tce": ["S069"],
    "traumatismo craneoencefalico": ["S069"],
    "golpe en la cabeza": ["S069"],
    "fa": ["I489"],
    "fibrilacion auricular": ["I489"],
    "sdra": ["J80X"],
    "ira": ["N170"],
    "epi": ["N760"],

    # --- Síntomas comunes en Urgencias ---
    "dolor de pecho": ["I219", "I200", "R074"],
    "dolor en el pecho": ["I219", "I200", "R074"],
    "dolor toracico": ["I219", "I200", "R074"],
    "dolor de cabeza": ["G439", "R51X"],
    "cefalea": ["G439", "R51X"],
    "falta de aire": ["R062", "J449"],
    "dificultad para respirar": ["R062", "J449"],
    "ahogo": ["R062", "J449"],
    "fiebre": ["R509"],
    "calentura": ["R509"],
    "dolor de estomago": ["R104"],
    "dolor de panza": ["R104"],
    "dolor abdominal": ["R104"],
    "vomito": ["R11X"],
    "nauseas": ["R11X"],
    "diarrea": ["A090", "K529"],
    "mareo": ["R42X"],
    "mareos": ["R42X"],
    "convulsion": ["R568", "G409"],
    "convulsiones": ["R568", "G409"],
    "ataque epileptico": ["G409"],
    "desmayo": ["R55X"],
    "perdida del conocimiento": ["R55X"],
    "se desmayo": ["R55X"],
    "dolor de espalda": ["M545"],
    "dolor lumbar": ["M545"],
    "tos": ["R05X"],
    "ronchas": ["L500", "L298"],
    "comezon": ["L500", "L298"],
    "picazon": ["L500", "L298"],
    "quemadura": ["T300"],
    "esguince": ["S936"],
    "torcedura": ["S936"],
    "gripa": ["J00X", "J111"],
    "resfriado": ["J00X"],
    "catarro": ["J00X"],
    "anginas": ["J039"],
    "dolor de garganta": ["J039"],
    "colico renal": ["N200"],
    "piedra en el rinon": ["N200"],
    "piedras en la vesicula": ["K802"],
    "calculos biliares": ["K802"],
    "apendicitis": ["K359"],
    "hernia": ["K409"],
    "varices": ["I839"],
    "anemia": ["D649"],
    "deshidratacion": ["E86X"],
    "intoxicacion": ["T509"],
    "envenenamiento": ["T509"],

    # --- Diagnósticos crónicos / frecuentes por especialidad ---
    "asma": ["J459"],
    "bronquitis": ["J209", "J40X"],
    "neumonia": ["J189"],
    "pulmonia": ["J189"],
    "gastritis": ["K297"],
    "colitis": ["K529"],
    "estrenimiento": ["K590"],
    "constipacion": ["K590"],
    "hemorroides": ["K649"],
    "almorranas": ["K649"],
    "prostata inflamada": ["N40X"],
    "obesidad": ["E668"],
    "colesterol alto": ["E785"],
    "otitis": ["H659"],
    "dolor de oido": ["H659"],
    "conjuntivitis": ["H108"],
    "ojo rojo": ["H108"],
    "vertigo": ["H810"],
    "cataratas": ["H269"],
    "glaucoma": ["H409"],
    "varicela": ["B019"],
    "sarampion": ["B059"],
    "rubeola": ["B069"],
    "tos ferina": ["A379"],

    # --- Gineco-obstetricia ---
    "embarazo": ["Z349"],
    "parto": ["O800"],
    "cesarea": ["O829"],
    "quiste de ovario": ["N832"],
    "quiste ovarico": ["N832"],
    "sangrado vaginal": ["N939"],
    "sangrado transvaginal": ["N939"],

    # --- Urología ---
    "dolor al orinar": ["N390"],
    "ardor al orinar": ["N390"],
    "sangre en la orina": ["R31X"],
    "orina con sangre": ["R31X"],
    "no puede orinar": ["R33X"],
    "retencion urinaria": ["R33X"],

    # --- Pediatría ---
    "desnutricion": ["E440"],
    "bajo peso": ["E440"],
    "convulsion febril": ["R560"],
    "convulsiones febriles": ["R560"],

    # --- Picaduras, mordeduras y emergencias ambientales ---
    "picadura de alacran": ["T632"],
    "piquete de alacran": ["T632"],
    "picadura de escorpion": ["T632"],
    "mordedura de arana": ["T633"],
    "picadura de arana": ["T633"],
    "mordedura de vibora": ["T630"],
    "mordedura de serpiente": ["T630"],
    "mordedura de culebra": ["T630"],
    "golpe de calor": ["T670"],
    "insolacion": ["T670"],
    "agotamiento por calor": ["T673"],
    "casi ahogamiento": ["T751"],
    "cuasi ahogamiento": ["T751"],
    "ahogamiento": ["T751"],
    "hipotermia": ["T68X"],
    "frio extremo": ["T68X"],

    # --- Dolor osteomuscular no traumático ---
    "ciatica": ["M543"],
    "dolor de nervio ciatico": ["M543"],
    "dolor de cuello": ["M542"],
    "dolor de hombro": ["M750"],
    "hombro congelado": ["M750"],
    "dolor de rodilla": ["M17"],
    "rodilla inflamada": ["M705"],

    # --- ORL frecuentes ---
    "sinusitis": ["J010"],
    "dolor de senos paranasales": ["J010"],
    "amigdalitis": ["J030"],
    "faringitis": ["J029"],
    "garganta irritada": ["J029"],
    "crup": ["J050"],
    "tos perruna": ["J050"],
    "laringitis obstructiva": ["J050"],

    # --- Piel, urología pediátrica, neurología e infecciosas ---
    "celulitis infecciosa": ["L039"],
    "piel infectada": ["L039"],
    "infeccion de los dedos": ["L030"],
    "hidrocele": ["N432"],
    "hinchazon en el testiculo": ["N432"],
    "fimosis": ["N47X"],
    "prepucio apretado": ["N47X"],
    "migrana": ["G430"],
    "migrana con aura": ["G431"],
    "dengue": ["A970", "A971"],
    "dengue con signos de alarma": ["A971"],
    "fiebre por dengue": ["A970"],

    # --- Fracturas frecuentes ---
    "fractura de cadera": ["S720"],
    "fractura de pierna": ["S82"],
    "se rompio la pierna": ["S82"],
    "fractura de brazo": ["S42"],
    "fractura de muneca": ["S525"],
    "se rompio la muneca": ["S525"],
    "fractura de mano": ["S62"],
    "fractura de tobillo": ["S823"],

    # --- Emergencias graves / choque ---
    "choque septico": ["R572"],
    "paro cardiaco": ["I469"],
    "paro cardiorespiratorio": ["I469"],
    "paro respiratorio": ["R092"],
    "choque anafilactico": ["T782"],
    "anafilaxia": ["T782"],
    "reaccion alergica severa": ["T782"],
    "alergia": ["T784"],

    # --- Abdomen agudo ---
    "colecistitis": ["K81"],
    "vesicula inflamada": ["K81"],
    "pancreatitis": ["K85"],
    "peritonitis": ["K65"],
    "obstruccion intestinal": ["K56"],
    "diverticulitis": ["K573"],

    # --- Signos vitales / cardiovascular ---
    "angina de pecho": ["I209"],
    "taquicardia": ["R000"],
    "bradicardia": ["R001"],
    "crisis hipertensiva": ["I119"],

    # --- Neurológico / psiquiátrico ---
    "meningitis": ["G039"],
    "encefalitis": ["A86X"],
    "delirio": ["F059"],
    "estado confusional": ["F059"],
    "ansiedad": ["F419"],
    "crisis de ansiedad": ["F410"],
    "ataque de panico": ["F410"],
    "depresion": ["F329"],
    "intoxicacion alcoholica": ["Y910"],

    # --- Piel ---
    "forunculo": ["L029"],
    "absceso en la piel": ["L029"],
    "impetigo": ["L010"],
    "herpes zoster": ["B02"],
    "culebrilla": ["B02"],
    "herpes labial": ["B00"],
    "escabiosis": ["B86X"],
    "sarna": ["B86X"],
    "piojos": ["B852"],
    "pediculosis": ["B852"],
    "tina": ["B359"],
    "hongos en la piel": ["B359"],
    "dermatitis atopica": ["L20"],
    "eczema": ["L20"],
    "una encarnada": ["L600"],

    # --- ORL / ojo ---
    "cuerpo extrano en el ojo": ["T150"],
    "otitis media": ["H650"],
    "otitis externa": ["H609"],

    # --- Endocrino ---
    "hipoglucemia": ["E162"],
    "cetoacidosis diabetica": ["E141"],
    "hipotiroidismo": ["E03"],
    "hipertiroidismo": ["E05"],
    "bocio": ["E04"],

    # --- Urológico / ginecológico ---
    "torsion testicular": ["N44X"],
    "orquiepididimitis": ["N459"],
    "vulvovaginitis": ["N771"],

    # --- Trauma ---
    "luxacion de hombro": ["S430"],
    "mordedura de perro": ["W54"],
    "ataque de perro": ["W54"],
    "politraumatismo": ["T07X"],
    "tetanos": ["A35X"],
    "rabia": ["A82"],

    # --- Infecciosas ---
    "vih": ["B24X"],
    "sida": ["B24X"],
    "hepatitis": ["B159"],
    "covid": ["U071"],
    "influenza": ["J10"],
    "gripe": ["J10"],

    # --- Oncología ---
    "leucemia": ["C910"],
    "cancer de mama": ["C509"],
    "cancer de prostata": ["C61X"],
    "cancer de colon": ["C189"],
    "cancer de pulmon": ["C349"],

    # --- Otros signos ---
    "asfixia": ["R090"],
    "cianosis": ["R230"],
    "ictericia": ["R17X"],
    "hidrocefalia": ["G919"],

    # --- Ajustes por investigación de catálogos hospitalarios reales ---
    # (crisis hipertensiva grave con daño de órgano blanco; el catálogo
    # institucional no incluye la categoría I16 de la CIE-10-CM, así que se
    # usa el código más cercano disponible en este catálogo)
    "encefalopatia hipertensiva": ["I674"],
    "hiperglucemia": ["E149"],
    "abrasion corneal": ["S050"],
    "rasguno en el ojo": ["S050"],
    "ulcera corneal": ["H160"],
    "ulcera en la cornea": ["H160"],

    # --- Términos clásicos / de otras clasificaciones (CIE-9 y lenguaje
    # médico clásico) que siguen usándose de palabra pero ya no son el
    # nombre oficial del diagnóstico en la CIE-10 ---
    "anasarca": ["R601"],
    "edema generalizado": ["R601"],
    "corea": ["G255"],
    "flatulencia": ["R14X"],
    "meteorismo": ["R14X"],
    "anuria": ["R34X"],
    "oliguria": ["R34X"],
    "disuria": ["R300"],
    "tenesmo vesical": ["R301"],
    "epistaxis": ["R040"],
    "sangrado de nariz": ["R040"],
    "sangrado nasal": ["R040"],
    "hemoptisis": ["R042"],
    "toser sangre": ["R042"],
    "astenia": ["R53X"],
    "adinamia": ["R53X"],
    "fatiga": ["R53X"],
    "hipo": ["R066"],
    "singulto": ["R066"],
    "tisis": ["A169"],
    "tuberculosis pulmonar": ["A169"],
    "hematemesis": ["K920"],
    "vomito con sangre": ["K920"],
    "melena": ["K921"],
    "heces negras": ["K921"],
}


missing = []
for term, codes in SYNONYMS.items():
    for code in codes:
        if chk(code) is None:
            missing.append((term, code))

print("sinonimos:", len(SYNONYMS))
print("MISSING:", len(missing))
for m in missing:
    print("MISS", m)
