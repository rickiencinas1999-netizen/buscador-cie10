# -*- coding: utf-8 -*-
"""
Catálogo curado de diagnósticos CIE-10 por especialidad.

Este archivo es la fuente de verdad del proyecto: agrupa códigos CIE-10 por
especialidad médica y categoría clínica. Lo usan tanto el generador del
póster (generar_poster.py) como el generador de datos de la app web
(generar_datos_app.py).

Cada código se valida contra data/catalogo.json (el catálogo institucional
completo) al importar este módulo: si algún código no existe en el catálogo,
o si hay códigos duplicados dentro de una misma especialidad, se imprime un
reporte de errores al importar.
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

# specialty -> list of (subcategoria, [(code, etiqueta_corta_opcional)])
SPECIALTIES = {
"Urgencias": [
 ("Cardiovascular", ["I219","I500","I10X","I639","I469","I471","I802","I209","I429","R074"]),
 ("Respiratorio", ["J189","J449","J459","J969","J81X","J690","J939","J439"]),
 ("Digestivo", ["K359","K802","K922","R104","K566","K659","K921","K920","T181","R100","K81","K85","K65","K56","K573"]),
 ("Neurológico", ["R568","G459","S069","G039","R55X","R402","G935","G936"]),
 ("Trauma / Choque", ["S720","T07X","T782","T780","T814","T140","T202","T783","T784"]),
 ("Infeccioso / Sepsis", ["A419","N390","B349","J039","A099","A46X","A970","A971"]),
 ("Metabólico", ["E149","E162","E86X","E870","E871","E876"]),
 ("Intoxicación / Psiquiátrico", ["T509","F419","T391","X499"]),
 ("Ginecológico / Urológico agudo", ["O009","R102","R33X","N832","N44X"]),
 ("ORL / Oftalmológico", ["T159","R040","R049","S022"]),
 ("Ambiental / Toxicológico", ["T632","T633","T630","T670","T673","T751","T68X","W54"]),
],
"Medicina Interna": [
 ("Cardiovascular", ["I10X","I500","I259","I489","I739","I959","I429"]),
 ("Endocrino-metabólico", ["E119","E039","E785","E669","E118","E271","E210","E232"]),
 ("Respiratorio", ["J449","J459","J189","J47X","J961","J90X"]),
 ("Renal", ["N189","N179","N390","N183","N184"]),
 ("Digestivo / Hepático", ["K766","K297","K599","K703","K219","K900","B169"]),
 ("Hematológico", ["D649","D509","D688","D693","D619","D630","D561"]),
 ("Infeccioso", ["B182","A419","U071","B159","B24X"]),
 ("Reumatológico", ["M069","M109","M549","M819","M329"]),
],
"Pediatría": [
 ("Respiratorio", ["J069","J189","J210","J459","J039","J209"]),
 ("Digestivo", ["A090","K590","R104","P929","T189","B820"]),
 ("Infeccioso / Febril", ["R509","B349","A080","J00X","A379","B059","B069","B269"]),
 ("Dermatológico", ["L309","L500","B019","L010","B86X","B850"]),
 ("Nutrición / Hematológico", ["E440","E639","R629","D509"]),
 ("Neonatal", ["P599","P073","P220"]),
 ("Otros frecuentes / Desarrollo", ["H659","N136","R51X","R560","F980","F900"]),
],
"Gineco-Obstetricia": [
 ("Embarazo / Control prenatal", ["Z349","Z359","O210","O990","O009"]),
 ("Hipertensión y diabetes gestacional", ["O13X","O140","O141","O244","O142","O243"]),
 ("Cesárea", ["O820","O821","O829","O822"]),
 ("Trabajo de parto / Parto", ["O800","O639","O369","Z370"]),
 ("Puerperio", ["O85X","O900","O909","O901","O903"]),
 ("Complicaciones obstétricas", ["O200","O470","O689","O721","O269"]),
 ("Ginecología general", ["N939","N760","N920","N872","N832","N871"]),
 ("Mama", ["N63X","D24X"]),
 ("Planificación / Climaterio", ["Z301","N951"]),
],
"Cirugía General": [
 ("Pared abdominal / Hernias", ["K409","K429","K469","K440","K449"]),
 ("Vesícula y vías biliares", ["K802","K800","K811","K830","K805"]),
 ("Apéndice", ["K359","K37X"]),
 ("Cirugía bariátrica", ["E662","E668","K911","K912","E660"]),
 ("Tejidos blandos / Piel", ["L029","L039","L722","L050"]),
 ("Tubo digestivo", ["K631","K566","K625","K640","K600"]),
 ("Postquirúrgico / Otros", ["T814","T813","K913","K915"]),
 ("Oncología quirúrgica", ["C189","C20X","C169"]),
],
"Traumatología y Ortopedia": [
 ("Fracturas miembro superior", ["S424","S525","S626","S420","S421"]),
 ("Fracturas miembro inferior", ["S720","S823","S924"]),
 ("Columna / Pelvis", ["S320","M545","S220","S222"]),
 ("Articular / Ligamentos", ["S836","M239","M754","S934","M700","S430"]),
 ("Infecciosas / Óseas", ["M865","M199","M819"]),
 ("Postquirúrgico", ["T845","Z966","Z946"]),
 ("Deformidades", ["M419","M201"]),
 ("Dolor de columna y articular no traumático", ["M543","M542","M750","M17","M705"]),
],
"Cardiología": [
 ("Isquémica", ["I219","I209","I251"]),
 ("Insuficiencia cardiaca", ["I500","I110","I270"]),
 ("Arritmias", ["I489","I472","I440","I490","I495","I499"]),
 ("Hipertensiva", ["I10X","I119","I674"]),
 ("Valvulopatías", ["I051","I340"]),
 ("Miocardio / Pericardio", ["I429","I309","I420","I421"]),
 ("Dispositivos / Postquirúrgico", ["Z950","Z955","Z951","Z952"]),
],
"Angiología": [
 ("Venas", ["I839","I832","I872","I830","I870"]),
 ("Trombosis / Embolia", ["I803","I269","I743","I801","I260"]),
 ("Arterial", ["I702","I719","I714","I709"]),
 ("Otros", ["L97X","I890","I891"]),
],
"Neumología": [
 ("Obstructivas", ["J449","J459","J439"]),
 ("Infecciosas", ["J189","A150","J159","J209"]),
 ("Intersticiales / Otras", ["J841","J938","J939"]),
 ("Neoplasias", ["C349"]),
 ("Sueño / Otros", ["G473","J960","J961","R042"]),
 ("Pleura", ["J90X","J91X"]),
],
"Gastroenterología": [
 ("Hígado", ["K766","K703","B182","B159","B169"]),
 ("Estómago / Duodeno", ["K259","K297","K219","C169"]),
 ("Intestino", ["K589","K522","K519","K900"]),
 ("Vía biliar / Páncreas", ["K810","K811","K859","K805"]),
 ("Otros", ["K579","K922","K649","K603"]),
],
"Neurología": [
 ("Cerebrovascular", ["I639","I619","G459"]),
 ("Epilepsia / Crisis", ["G409","R568","R560"]),
 ("Cefalea", ["G439","G440","G430","G431"]),
 ("Degenerativas", ["G309","G20X","G932"]),
 ("Neuropatías", ["G629","G562","G610"]),
 ("Neuroinfección / Otros", ["G039","G049","G934","G042"]),
],
"Nefrología": [
 ("Enfermedad renal crónica", ["N189","N185","N180","N183","N184"]),
 ("Agudo", ["N179","N170"]),
 ("Glomerular", ["N049","N059"]),
 ("Diálisis / Trasplante", ["Z992","Z940"]),
 ("Hidroelectrolítico / HTA renal", ["E875","E872","I120","E873","E876","I129"]),
],
"Dermatología": [
 ("Infecciosas", ["L029","B019","B350","B354","B029","B86X","L039","L030"]),
 ("Inflamatorias", ["L309","L400","L500","L405"]),
 ("Neoplasias", ["C449","D239"]),
 ("Otras", ["L708","L219","L80X","L659","B07X"]),
],
"Urología": [
 ("Infecciones", ["N390","N300","N136"]),
 ("Litiasis", ["N200","N202"]),
 ("Próstata", ["N40X","C61X"]),
 ("Genital masculino", ["I861","N459","N433","N450","N434","N432","N47X"]),
 ("Oncología urológica", ["C679","C64X"]),
 ("Otros", ["R31X","R33X","N393","N359"]),
],
"Oftalmología": [
 ("Segmento anterior", ["H108","H269","H520","H000","H110"]),
 ("Glaucoma / Retina", ["H409","H353","H330"]),
 ("Otros", ["H579","H040","H530","H501","T159","S050","H160"]),
],
"Otorrinolaringología": [
 ("Oído", ["H659","H609","H904","H810","H811"]),
 ("Nariz / Senos", ["J019","J340","J342","R040","J010","S022"]),
 ("Faringe / Laringe", ["J039","J040","J350","J351","J030","J029","J050"]),
],
"Endocrinología": [
 ("Diabetes", ["E119","E112","E149","E118"]),
 ("Tiroides", ["E039","E059","E041"]),
 ("Otros", ["E669","E785","E271","E210","E232","E790"]),
],
"Infectología": [
 ("Respiratorias", ["J189","A150","J118"]),
 ("Urinarias / Sistémicas", ["N390","A419","B182"]),
 ("Otras", ["U071","B349","A90X","B24X"]),
 ("Exantemáticas / Prevenibles por vacuna", ["B059","B069","A379"]),
],
"Terapia Intensiva": [
 ("Choque", ["R572","R570","R571","R579"]),
 ("Respiratorio crítico", ["J80X","J960","Z991","J961"]),
 ("Neurológico crítico", ["R402","G931","G936","G935","R400"]),
 ("Sepsis / SIRS", ["R650","R651","A419","R659"]),
 ("Cardiorrespiratorio", ["I460","R092","I461"]),
],
}

missing = []
dupes = []
report = {}
for spec, cats in SPECIALTIES.items():
    report[spec] = []
    seen = set()
    for subcat, codes in cats:
        for code in codes:
            name = chk(code)
            if name is None:
                missing.append((spec, subcat, code))
            if code in seen:
                dupes.append((spec, subcat, code))
            seen.add(code)
            report[spec].append((subcat, code, name))

n = sum(len(codes) for cats in SPECIALTIES.values() for _, codes in cats)
print("count", n)
print("MISSING:", len(missing))
for m in missing:
    print("MISS", m)
print("DUPES:", len(dupes))
for d in dupes:
    print("DUP", d)

REPORT_PATH = Path(__file__).resolve().parent.parent / "dist" / "report.json"
REPORT_PATH.parent.mkdir(exist_ok=True)
with open(REPORT_PATH, 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=1)
