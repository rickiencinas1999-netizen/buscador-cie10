# -*- coding: utf-8 -*-
"""
Correlación aproximada CIE-10 -> CIE-9, para los diagnósticos curados de
especialidades.py.

A diferencia de src/generar_cie11.py (que usa la tabla OFICIAL de la OMS),
NO existe una tabla oficial y gratuita de equivalencia CIE-9 <-> CIE-10 para
la edición de la CIE-10 que usa este catálogo (la de la OMS/OPS, no la
"Clinical Modification" de EE. UU.): la OMS publicó un "ICD-9-ICD-10
Translator" en 1997 (WHO/HST/96.9) pero no está disponible para descargar en
ningún repositorio público; y las tablas GEMs de EE. UU. son para la
CIE-9-MC/CIE-10-CM, ediciones distintas cuyo detalle no calza código por
código con este catálogo.

Esta tabla es entonces una correlación CURADA A MANO con conocimiento
clínico general, no una fuente oficial de la OMS/OPS. Cubre los diagnósticos
más frecuentes/clásicos entre los códigos curados de especialidades.py —
donde no hay certeza razonable del código CIE-9 exacto, se deja fuera en vez
de adivinar. Cada entrada es:

    "CODIGO_CIE10": ("codigo_cie9", "Nombre breve en CIE-9"),

Cada código CIE-9 (a nivel de 3 dígitos, es decir sin el punto decimal) se
valida contra data/icd9_3digit_ref.json — el catálogo OFICIAL de categorías
de 3 dígitos de la CIE-9-MC de EE. UU. (ver generar_icd9_ref.py) — así un
número de código mal recordado se detecta como error en vez de fallar en
silencio. Esa validación solo cubre el nivel de 3 dígitos (p. ej. que "410"
sea de verdad "infarto agudo del miocardio"); el 4to/5to dígito de cada
entrada (p. ej. el ".9" en "410.9") se eligió con criterio clínico y no
tiene una lista pública para verificarse automáticamente.

Los códigos CIE-10 de la izquierda también se validan contra
data/catalogo.json al importar este módulo (igual que especialidades.py y
sinonimos.py) para detectar típos.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOGO_PATH = ROOT / "data" / "catalogo.json"
ICD9_REF_PATH = ROOT / "data" / "icd9_3digit_ref.json"

with open(CATALOGO_PATH, encoding="utf-8") as f:
    CAT = json.load(f)

try:
    with open(ICD9_REF_PATH, encoding="utf-8") as f:
        ICD9_REF = json.load(f)
except FileNotFoundError:
    ICD9_REF = None  # generar_icd9_ref.py no se ha corrido todavía


def chk(code):
    c = CAT.get(code)
    return c["nombre"] if c else None


CIE9 = {
    # --- Infecciosas ---
    "A080": ("008.6", "Enteritis debida a rotavirus"),
    "A090": ("009.2", "Gastroenteritis y colitis infecciosas de origen no especificado"),
    "A099": ("009.0", "Gastroenteritis y colitis infecciosas"),
    "A150": ("011.9", "Tuberculosis pulmonar"),
    "A379": ("033.9", "Tos ferina"),
    "A419": ("038.9", "Septicemia"),
    "A46X": ("035", "Erisipela"),
    "A90X": ("061", "Dengue"),
    "A970": ("061", "Dengue"),
    "A971": ("061", "Dengue"),
    "B019": ("052.9", "Varicela sin complicaciones"),
    "B029": ("053.9", "Herpes zoster sin complicaciones"),
    "B059": ("055.9", "Sarampión sin complicaciones"),
    "B069": ("056.9", "Rubéola sin complicaciones"),
    "B159": ("070.10", "Hepatitis viral aguda tipo A"),
    "B169": ("070.30", "Hepatitis viral aguda tipo B"),
    "B182": ("070.54", "Hepatitis crónica tipo C"),
    "B24X": ("042", "Enfermedad por VIH"),
    "B269": ("072.9", "Parotiditis sin complicaciones"),
    "B349": ("079.99", "Infección viral no especificada"),
    "B86X": ("133.0", "Escabiosis"),
    "B820": ("128.9", "Helmintiasis intestinal no especificada"),
    "B850": ("132.0", "Pediculosis del cuero cabelludo"),

    # --- Oncología ---
    "C169": ("151.9", "Tumor maligno del estómago"),
    "C189": ("153.9", "Tumor maligno del colon"),
    "C20X": ("154.1", "Tumor maligno del recto"),
    "C349": ("162.9", "Tumor maligno del bronquio o pulmón"),
    "C449": ("173.9", "Otro tumor maligno de la piel"),
    "C509": ("174.9", "Tumor maligno de la mama"),
    "C61X": ("185", "Tumor maligno de la próstata"),
    "C64X": ("189.0", "Tumor maligno del riñón"),
    "C679": ("188.9", "Tumor maligno de la vejiga urinaria"),
    "D239": ("216.9", "Tumor benigno de la piel"),
    "D24X": ("217", "Tumor benigno de la mama"),

    # --- Hematológico ---
    "D509": ("280.9", "Anemia por deficiencia de hierro"),
    "D619": ("284.9", "Anemia aplástica"),
    "D630": ("285.22", "Anemia en enfermedad neoplásica"),
    "D649": ("285.9", "Anemia no especificada"),
    "D688": ("286.9", "Otro defecto de la coagulación"),
    "D693": ("287.31", "Púrpura trombocitopénica idiopática"),

    # --- Endocrino / metabólico ---
    "E039": ("244.9", "Hipotiroidismo no especificado"),
    "E041": ("241.0", "Nódulo tiroideo solitario no tóxico"),
    "E059": ("242.90", "Tirotoxicosis sin bocio"),
    "E112": ("250.40", "Diabetes mellitus tipo 2 con complicaciones renales"),
    "E118": ("250.90", "Diabetes mellitus tipo 2 con complicaciones no especificadas"),
    "E119": ("250.00", "Diabetes mellitus tipo 2 sin complicación"),
    "E149": ("250.00", "Diabetes mellitus no especificada"),
    "E162": ("251.2", "Hipoglucemia no especificada"),
    "E210": ("252.01", "Hiperparatiroidismo primario"),
    "E639": ("269.9", "Deficiencia nutricional no especificada"),
    "E440": ("263.0", "Desnutrición proteicocalórica moderada"),
    "E660": ("278.00", "Obesidad"),
    "E668": ("278.00", "Obesidad"),
    "E669": ("278.00", "Obesidad no especificada"),
    "E785": ("272.4", "Hiperlipidemia no especificada"),
    "E86X": ("276.51", "Depleción del volumen"),
    "E870": ("276.0", "Hiperosmolaridad e hipernatremia"),
    "E871": ("276.1", "Hiposmolaridad e hiponatremia"),
    "E872": ("276.2", "Acidosis"),
    "E873": ("276.3", "Alcalosis"),
    "E875": ("276.7", "Hiperpotasemia"),
    "E876": ("276.8", "Hipopotasemia"),

    # --- Psiquiátrico ---
    "F419": ("300.00", "Trastorno de ansiedad no especificado"),
    "F900": ("314.01", "Trastorno de déficit de atención con hiperactividad"),
    "F980": ("307.6", "Enuresis no orgánica"),

    # --- Neurológico ---
    "G039": ("322.9", "Meningitis no especificada"),
    "G049": ("323.9", "Encefalitis, mielitis y encefalomielitis no especificadas"),
    "G20X": ("332.0", "Enfermedad de Parkinson"),
    "G309": ("331.0", "Enfermedad de Alzheimer"),
    "G409": ("345.90", "Epilepsia no especificada"),
    "G430": ("346.10", "Migraña sin aura"),
    "G431": ("346.00", "Migraña con aura"),
    "G439": ("346.90", "Migraña no especificada"),
    "G459": ("435.9", "Isquemia cerebral transitoria"),
    "G473": ("780.57", "Apnea del sueño"),
    "G610": ("357.0", "Síndrome de Guillain-Barré"),
    "G629": ("356.9", "Polineuropatía no especificada"),

    # --- Ojo / oído ---
    "H108": ("372.30", "Conjuntivitis no especificada"),
    "H160": ("370.00", "Úlcera de la córnea"),
    "H269": ("366.9", "Catarata no especificada"),
    "H409": ("365.9", "Glaucoma no especificado"),
    "H520": ("367.0", "Hipermetropía"),
    "H609": ("380.10", "Otitis externa"),
    "H659": ("381.4", "Otitis media no supurativa"),
    "H810": ("386.00", "Enfermedad de Meniere"),
    "H811": ("386.11", "Vértigo paroxístico benigno"),

    # --- Cardiovascular ---
    "I051": ("394.1", "Insuficiencia mitral reumática"),
    "I10X": ("401.9", "Hipertensión esencial"),
    "I110": ("402.91", "Cardiopatía hipertensiva con insuficiencia cardíaca"),
    "I119": ("401.9", "Hipertensión esencial"),
    "I120": ("403.91", "Enfermedad renal hipertensiva con insuficiencia renal"),
    "I129": ("403.90", "Enfermedad renal hipertensiva"),
    "I209": ("413.9", "Angina de pecho"),
    "I219": ("410.9", "Infarto agudo del miocardio"),
    "I251": ("414.00", "Enfermedad aterosclerótica del corazón"),
    "I259": ("414.9", "Enfermedad isquémica crónica del corazón"),
    "I260": ("415.19", "Embolia pulmonar con corazón pulmonar agudo"),
    "I269": ("415.19", "Embolia pulmonar"),
    "I270": ("416.0", "Hipertensión pulmonar primaria"),
    "I309": ("420.90", "Pericarditis aguda"),
    "I340": ("424.0", "Trastorno de la válvula mitral"),
    "I420": ("425.4", "Cardiomiopatía dilatada"),
    "I421": ("425.1", "Cardiomiopatía hipertrófica obstructiva"),
    "I429": ("425.4", "Cardiomiopatía no especificada"),
    "I440": ("426.11", "Bloqueo auriculoventricular de primer grado"),
    "I460": ("427.5", "Paro cardíaco"),
    "I461": ("427.5", "Muerte cardíaca súbita"),
    "I469": ("427.5", "Paro cardíaco"),
    "I471": ("427.0", "Taquicardia supraventricular"),
    "I472": ("427.1", "Taquicardia ventricular paroxística"),
    "I489": ("427.31", "Fibrilación auricular"),
    "I490": ("427.41", "Fibrilación y aleteo ventricular"),
    "I499": ("427.9", "Arritmia cardíaca no especificada"),
    "I500": ("428.0", "Insuficiencia cardíaca congestiva"),
    "I619": ("431", "Hemorragia intracerebral"),
    "I639": ("434.91", "Oclusión de arteria cerebral con infarto"),
    "I674": ("437.2", "Encefalopatía hipertensiva"),
    "I702": ("440.20", "Aterosclerosis de las arterias de los miembros"),
    "I709": ("440.9", "Aterosclerosis generalizada"),
    "I714": ("441.4", "Aneurisma de la aorta abdominal sin ruptura"),
    "I719": ("441.9", "Aneurisma de la aorta sin ruptura"),
    "I739": ("443.9", "Enfermedad vascular periférica no especificada"),
    "I743": ("444.22", "Embolia y trombosis de arterias de miembros inferiores"),
    "I801": ("451.11", "Flebitis y tromboflebitis de la vena femoral"),
    "I802": ("451.19", "Flebitis y tromboflebitis de otros vasos profundos"),
    "I803": ("451.2", "Flebitis y tromboflebitis de miembros inferiores"),
    "I830": ("454.0", "Venas varicosas de miembros inferiores con úlcera"),
    "I839": ("454.9", "Venas varicosas de miembros inferiores"),
    "I890": ("457.1", "Linfedema no clasificado"),
    "I891": ("457.2", "Linfangitis"),
    "I959": ("458.9", "Hipotensión no especificada"),

    # --- Respiratorio ---
    "J00X": ("460", "Rinofaringitis aguda [resfriado común]"),
    "J019": ("461.9", "Sinusitis aguda"),
    "J029": ("462", "Faringitis aguda"),
    "J039": ("463", "Amigdalitis aguda"),
    "J040": ("464.00", "Laringitis aguda"),
    "J050": ("464.4", "Crup"),
    "J069": ("465.9", "Infección aguda de vías respiratorias superiores"),
    "J118": ("487.1", "Influenza con otras manifestaciones respiratorias"),
    "J159": ("482.9", "Neumonía bacteriana no especificada"),
    "J189": ("486", "Neumonía, organismo no especificado"),
    "J209": ("466.0", "Bronquitis aguda"),
    "J210": ("466.11", "Bronquiolitis aguda debida a VSR"),
    "J350": ("474.00", "Amigdalitis crónica"),
    "J351": ("474.10", "Hipertrofia de las amígdalas"),
    "J439": ("492.8", "Enfisema"),
    "J449": ("496", "Enfermedad pulmonar obstructiva crónica"),
    "J459": ("493.9", "Asma"),
    "J47X": ("494.0", "Bronquiectasia"),
    "J690": ("507.0", "Neumonitis por aspiración de alimento o vómito"),
    "J80X": ("518.5", "Síndrome de dificultad respiratoria del adulto"),
    "J81X": ("428.1", "Edema pulmonar agudo"),
    "J841": ("515", "Fibrosis pulmonar postinflamatoria"),
    "J90X": ("511.9", "Derrame pleural"),
    "J938": ("512.8", "Otro neumotórax"),
    "J939": ("512.8", "Neumotórax no especificado"),
    "J960": ("518.81", "Insuficiencia respiratoria aguda"),
    "J961": ("518.83", "Insuficiencia respiratoria crónica"),
    "J969": ("518.8", "Insuficiencia respiratoria, no especificada"),

    # --- Digestivo ---
    "K219": ("530.81", "Reflujo gastroesofágico"),
    "K259": ("531.90", "Úlcera gástrica"),
    "K297": ("535.50", "Gastritis no especificada"),
    "K359": ("540.9", "Apendicitis aguda"),
    "K37X": ("541", "Apendicitis no especificada"),
    "K409": ("550.90", "Hernia inguinal"),
    "K429": ("553.1", "Hernia umbilical"),
    "K449": ("553.3", "Hernia diafragmática"),
    "K469": ("553.9", "Hernia abdominal no especificada"),
    "K519": ("556.9", "Colitis ulcerativa"),
    "K56": ("560.9", "Íleo paralítico y obstrucción intestinal sin hernia"),
    "K566": ("560.9", "Obstrucción intestinal no especificada"),
    "K573": ("562.11", "Diverticulitis del colon sin hemorragia"),
    "K589": ("564.1", "Síndrome del colon irritable"),
    "K590": ("564.00", "Estreñimiento"),
    "K599": ("564.9", "Trastorno funcional intestinal no especificado"),
    "K600": ("565.0", "Fisura anal"),
    "K625": ("569.3", "Hemorragia del ano y del recto"),
    "K640": ("455.0", "Hemorroides internas"),
    "K649": ("455.6", "Hemorroides no especificadas"),
    "K65": ("567.9", "Peritonitis"),
    "K659": ("567.9", "Peritonitis no especificada"),
    "K703": ("571.2", "Cirrosis hepática alcohólica"),
    "K766": ("572.3", "Hipertensión portal"),
    "K800": ("574.00", "Cálculo de vesícula biliar con colecistitis aguda"),
    "K802": ("574.20", "Cálculo de vesícula biliar sin colecistitis"),
    "K81": ("575.10", "Colecistitis"),
    "K810": ("575.00", "Colecistitis aguda"),
    "K811": ("575.10", "Colecistitis crónica"),
    "K830": ("576.1", "Colangitis"),
    "K85": ("577.0", "Pancreatitis aguda"),
    "K859": ("577.0", "Pancreatitis aguda"),
    "K900": ("579.0", "Enfermedad celíaca"),
    "K920": ("578.0", "Hematemesis"),
    "K921": ("578.1", "Melena"),
    "K922": ("578.9", "Hemorragia gastrointestinal no especificada"),

    # --- Piel ---
    "L010": ("684", "Impétigo"),
    "L029": ("682.9", "Absceso cutáneo de sitio no especificado"),
    "L030": ("681.9", "Celulitis de los dedos"),
    "L039": ("682.9", "Celulitis de sitio no especificado"),
    "L219": ("690.10", "Dermatitis seborreica"),
    "L309": ("692.9", "Dermatitis de contacto no especificada"),
    "L400": ("696.1", "Psoriasis vulgar"),
    "L500": ("708.9", "Urticaria"),
    "L708": ("706.1", "Otro acné"),
    "L80X": ("709.01", "Vitíligo"),
    "L97X": ("707.10", "Úlcera crónica de miembro inferior"),

    # --- Musculoesquelético ---
    "M069": ("714.0", "Artritis reumatoide"),
    "M109": ("274.9", "Gota"),
    "M17": ("715.16", "Gonartrosis"),
    "M170": ("715.16", "Gonartrosis primaria"),
    "M199": ("715.9", "Artrosis no especificada"),
    "M239": ("717.9", "Trastorno interno de la rodilla"),
    "M329": ("710.0", "Lupus eritematoso sistémico"),
    "M419": ("737.30", "Escoliosis"),
    "M542": ("723.1", "Cervicalgia"),
    "M543": ("724.3", "Ciática"),
    "M545": ("724.2", "Lumbago"),
    "M549": ("724.5", "Dorsalgia no especificada"),
    "M700": ("727.05", "Sinovitis crepitante crónica de mano y muñeca"),
    "M705": ("727.3", "Otras bursitis"),
    "M750": ("726.0", "Capsulitis adhesiva del hombro"),
    "M754": ("726.0", "Síndrome de abducción dolorosa del hombro"),
    "M819": ("733.00", "Osteoporosis no especificada"),
    "M865": ("730.10", "Osteomielitis crónica"),

    # --- Renal / urológico ---
    "N049": ("581.9", "Síndrome nefrótico"),
    "N059": ("583.9", "Síndrome nefrítico"),
    "N136": ("590.2", "Pionefrosis"),
    "N170": ("584.9", "Insuficiencia renal aguda con necrosis tubular"),
    "N179": ("584.9", "Insuficiencia renal aguda"),
    "N180": ("585.6", "Insuficiencia renal terminal"),
    "N183": ("585.3", "Enfermedad renal crónica, etapa 3"),
    "N184": ("585.4", "Enfermedad renal crónica, etapa 4"),
    "N185": ("585.5", "Enfermedad renal crónica, etapa 5"),
    "N189": ("585.9", "Enfermedad renal crónica no especificada"),
    "N200": ("592.0", "Cálculo del riñón"),
    "N202": ("592.0", "Cálculo del riñón con cálculo del uréter"),
    "N300": ("595.9", "Cistitis aguda"),
    "N359": ("598.9", "Estrechez uretral no especificada"),
    "N390": ("599.0", "Infección de vías urinarias"),
    "N393": ("625.6", "Incontinencia urinaria por tensión"),
    "N40X": ("600.00", "Hiperplasia de la próstata"),
    "N432": ("603.9", "Otros hidroceles"),
    "N433": ("603.9", "Hidrocele no especificado"),
    "N44X": ("608.20", "Torsión del testículo"),
    "N450": ("604.90", "Orquitis y epididimitis con absceso"),
    "N459": ("604.90", "Orquitis y epididimitis sin absceso"),
    "N47X": ("605", "Fimosis y parafimosis"),
    "N63X": ("611.72", "Masa no especificada en la mama"),
    "N760": ("616.10", "Vaginitis aguda"),
    "N832": ("620.2", "Otros quistes ováricos"),
    "N871": ("622.12", "Displasia cervical moderada"),
    "N920": ("626.2", "Menstruación excesiva y frecuente"),
    "N939": ("626.9", "Hemorragia vaginal y uterina anormal"),
    "N951": ("627.2", "Estados menopáusicos y climatéricos femeninos"),

    # --- Gineco-obstetricia ---
    "O009": ("633.90", "Embarazo ectópico"),
    "O13X": ("642.30", "Hipertensión gestacional"),
    "O140": ("642.40", "Preeclampsia leve a moderada"),
    "O141": ("642.50", "Preeclampsia severa"),
    "O200": ("640.00", "Amenaza de aborto"),
    "O210": ("643.00", "Hiperemesis gravídica leve"),
    "O244": ("648.80", "Diabetes mellitus que se origina con el embarazo"),
    "O639": ("662.10", "Trabajo de parto prolongado"),
    "O721": ("666.10", "Otras hemorragias postparto inmediatas"),
    "O800": ("650", "Parto único espontáneo"),
    "O820": ("669.70", "Parto por cesárea electiva"),
    "O821": ("669.70", "Parto por cesárea de emergencia"),
    "O829": ("669.70", "Parto por cesárea"),
    "O85X": ("670.00", "Sepsis puerperal"),
    "O909": ("674.90", "Complicación puerperal no especificada"),
    "O990": ("648.20", "Anemia que complica el embarazo"),

    # --- Neonatal ---
    "P073": ("765.10", "Otros recién nacidos pretérmino"),
    "P220": ("769", "Síndrome de dificultad respiratoria del recién nacido"),
    "P599": ("774.6", "Ictericia neonatal no especificada"),

    # --- Signos y síntomas ---
    "R040": ("784.7", "Epistaxis"),
    "R042": ("786.30", "Hemoptisis"),
    "R074": ("786.50", "Dolor en el pecho"),
    "R092": ("799.1", "Paro respiratorio"),
    "R100": ("789.00", "Abdomen agudo"),
    "R104": ("789.00", "Otros dolores abdominales"),
    "R31X": ("599.70", "Hematuria"),
    "R33X": ("788.20", "Retención de orina"),
    "R400": ("780.09", "Somnolencia"),
    "R402": ("780.01", "Coma"),
    "R509": ("780.60", "Fiebre no especificada"),
    "R51X": ("784.0", "Cefalea"),
    "R55X": ("780.2", "Síncope y colapso"),
    "R560": ("780.31", "Convulsiones febriles"),
    "R568": ("780.39", "Otras convulsiones"),
    "R570": ("785.51", "Choque cardiogénico"),
    "R571": ("785.59", "Choque hipovolémico"),
    "R572": ("785.52", "Choque séptico"),
    "R579": ("785.50", "Choque no especificado"),
    "R650": ("995.90", "Síndrome de respuesta inflamatoria sistémica (SIRS)"),
    "R651": ("995.92", "SIRS de origen infeccioso con falla orgánica (sepsis severa)"),

    # --- Trauma / envenenamiento ---
    "S069": ("854.00", "Traumatismo intracraneal no especificado"),
    "S220": ("805.2", "Fractura de vértebra torácica"),
    "S320": ("805.4", "Fractura de vértebra lumbar"),
    "S420": ("810.00", "Fractura de la clavícula"),
    "S421": ("811.00", "Fractura del omóplato"),
    "S424": ("812.40", "Fractura de la epífisis inferior del húmero"),
    "S430": ("831.00", "Luxación de la articulación del hombro"),
    "S525": ("813.42", "Fractura de la epífisis inferior del radio"),
    "S626": ("816.02", "Fractura de otro dedo de la mano"),
    "S720": ("820.8", "Fractura del cuello del fémur"),
    "S823": ("823.80", "Fractura de la epífisis inferior de la tibia"),
    "S836": ("844.9", "Esguinces y torceduras de la rodilla"),
    "S924": ("826.0", "Fractura de los huesos del dedo gordo del pie"),
    "S934": ("845.00", "Esguinces y torceduras del tobillo"),
    "T07X": ("959.9", "Traumatismos múltiples no especificados"),
    "T159": ("930.9", "Cuerpo extraño en parte externa del ojo"),
    "T509": ("977.9", "Envenenamiento por droga no especificada"),
    "T630": ("989.5", "Efecto tóxico del veneno de serpiente"),
    "T632": ("989.5", "Efecto tóxico del veneno de escorpión"),
    "T633": ("989.5", "Efecto tóxico del veneno de arañas"),
    "T670": ("992.0", "Golpe de calor e insolación"),
    "T68X": ("991.6", "Hipotermia"),
    "T751": ("994.1", "Ahogamiento y sumersión no mortal"),
    "T780": ("995.60", "Choque anafiláctico debido a alimentos"),
    "T782": ("995.0", "Choque anafiláctico no especificado"),
    "T783": ("995.1", "Edema angioneurótico"),
    "T784": ("995.3", "Alergia no especificada"),
    "T814": ("998.59", "Infección consecutiva a procedimiento"),
    "W54": ("E906.0", "Mordedura de perro"),
    "X499": ("E866.9", "Envenenamiento accidental por otros productos químicos"),
}


missing = []
bad_icd9 = []
for cie10_code, (cie9_code, name) in CIE9.items():
    if chk(cie10_code) is None:
        missing.append(cie10_code)
    if ICD9_REF is not None:
        prefix = re.split(r"[.]", cie9_code)[0]
        if not (prefix.startswith("E") or prefix.startswith("V")) and prefix not in ICD9_REF:
            bad_icd9.append((cie10_code, cie9_code))

if __name__ == "__main__":
    print("correlación CIE-9:", len(CIE9))
    print("MISSING (código CIE-10 inválido):", len(missing))
    for m in missing:
        print("MISS", m)
    if ICD9_REF is None:
        print("AVISO: no se encontró data/icd9_3digit_ref.json — corre generar_icd9_ref.py para validar los códigos CIE-9.")
    else:
        print("códigos CIE-9 sin verificar contra la referencia oficial:", len(bad_icd9))
        for b in bad_icd9:
            print("BAD_ICD9", b)
