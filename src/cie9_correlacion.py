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

Los códigos se validan contra data/catalogo.json al importar este módulo
(igual que especialidades.py y sinonimos.py) para detectar típos.
"""
import json
from pathlib import Path

CATALOGO_PATH = Path(__file__).resolve().parent.parent / "data" / "catalogo.json"

with open(CATALOGO_PATH, encoding="utf-8") as f:
    CAT = json.load(f)


def chk(code):
    c = CAT.get(code)
    return c["nombre"] if c else None


# CIE-10 -> (CIE-9, nombre breve)
CIE9 = {
    # --- Cardiovascular ---
    "I219": ("410.9", "Infarto agudo del miocardio"),
    "I10X": ("401.9", "Hipertensión esencial"),
    "I500": ("428.0", "Insuficiencia cardíaca congestiva"),
    "I489": ("427.31", "Fibrilación auricular"),
    "I639": ("434.91", "Oclusión de arteria cerebral con infarto"),
    "I619": ("431", "Hemorragia intracerebral"),
    "I209": ("413.9", "Angina de pecho"),
    "I802": ("453.40", "Trombosis venosa profunda"),
    "I269": ("415.19", "Embolia pulmonar"),
    "I429": ("425.4", "Miocardiopatía"),
    "I110": ("402.91", "Cardiopatía hipertensiva con insuficiencia cardíaca"),

    # --- Respiratorio ---
    "J189": ("486", "Neumonía, organismo no especificado"),
    "J449": ("496", "Obstrucción crónica de vías respiratorias"),
    "J459": ("493.9", "Asma"),
    "J00X": ("460", "Rinofaringitis aguda [resfriado común]"),
    "J039": ("463", "Amigdalitis aguda"),
    "J029": ("462", "Faringitis aguda"),
    "J209": ("466.0", "Bronquitis aguda"),
    "J690": ("507.0", "Neumonía por aspiración"),

    # --- Digestivo ---
    "K359": ("540.9", "Apendicitis aguda, no especificada"),
    "K802": ("574.20", "Cálculo de vesícula biliar sin colecistitis"),
    "K297": ("535.50", "Gastritis, no especificada"),
    "K219": ("530.81", "Reflujo gastroesofágico"),
    "K590": ("564.00", "Estreñimiento"),
    "K529": ("558.9", "Gastroenteritis y colitis no infecciosa"),
    "K649": ("455.6", "Hemorroides, no especificadas"),
    "K409": ("550.90", "Hernia inguinal"),
    "K811": ("575.10", "Colecistitis crónica"),
    "K85": ("577.0", "Pancreatitis aguda"),
    "K65": ("567.9", "Peritonitis, no especificada"),

    # --- Endocrino / metabólico ---
    "E119": ("250.00", "Diabetes mellitus tipo 2"),
    "E149": ("250.00", "Diabetes mellitus, no especificada"),
    "E162": ("251.2", "Hipoglucemia, no especificada"),
    "E141": ("250.10", "Diabetes con cetoacidosis"),
    "E039": ("244.9", "Hipotiroidismo, no especificado"),
    "E05": ("242.90", "Tirotoxicosis [hipertiroidismo]"),
    "E86X": ("276.51", "Deshidratación"),
    "E66": ("278.00", "Obesidad"),
    "E785": ("272.4", "Hiperlipidemia, no especificada"),

    # --- Renal / urinario ---
    "N390": ("599.0", "Infección de vías urinarias, sitio no especificado"),
    "N189": ("585.9", "Enfermedad renal crónica, no especificada"),
    "N180": ("585.6", "Enfermedad renal en etapa terminal"),
    "N179": ("584.9", "Insuficiencia renal aguda"),
    "N200": ("592.0", "Cálculo del riñón"),

    # --- Neurológico ---
    "G409": ("345.90", "Epilepsia, no especificada"),
    "G439": ("346.9", "Migraña, no especificada"),
    "G030": ("322.9", "Meningitis, no especificada"),

    # --- Infeccioso ---
    "A419": ("038.9", "Septicemia, no especificada"),
    "B182": ("070.54", "Hepatitis crónica tipo C"),
    "B159": ("070.10", "Hepatitis aguda tipo A"),
    "B24X": ("042", "Enfermedad por VIH"),
    "A90X": ("061", "Fiebre del dengue [clásico]"),
    "A379": ("033.9", "Tos ferina, no especificada"),

    # --- Piel ---
    "L029": ("682.9", "Absceso cutáneo, sitio no especificado"),
    "L039": ("682.9", "Celulitis, sitio no especificado"),
    "B019": ("052.9", "Varicela, sin complicación"),

    # --- Trauma / envenenamiento ---
    "S069": ("854.00", "Traumatismo intracraneal, no especificado"),
    "S720": ("820.8", "Fractura del cuello del fémur"),
    "T509": ("977.9", "Envenenamiento por droga no especificada"),

    # --- Gineco-obstetricia ---
    "O800": ("650", "Parto único espontáneo"),
    "O829": ("669.70", "Cesárea, no especificada"),
    "N939": ("626.9", "Trastorno menstrual, no especificado"),
    "N832": ("620.2", "Quiste de ovario"),

    # --- ORL / oftalmología ---
    "H659": ("382.9", "Otitis media, no especificada"),
    "H108": ("372.30", "Conjuntivitis, no especificada"),
    "J019": ("461.9", "Sinusitis aguda, no especificada"),

    # --- Urología / genital masculino ---
    "N40X": ("600.00", "Hiperplasia de la próstata"),
    "N459": ("604.90", "Orquitis y epididimitis, sin absceso"),

    # --- Musculoesquelético ---
    "M545": ("724.2", "Lumbago"),
    "M543": ("724.3", "Ciática"),
    "M542": ("723.1", "Cervicalgia"),
    "M170": ("715.16", "Gonartrosis primaria"),

    # --- Hematológico / oncológico ---
    "D649": ("285.9", "Anemia, no especificada"),
    "C349": ("162.9", "Tumor maligno del pulmón"),
    "C509": ("174.9", "Tumor maligno de la mama"),
    "C61X": ("185", "Tumor maligno de la próstata"),
    "C189": ("153.9", "Tumor maligno del colon"),
}


missing = []
for cie10_code, (cie9_code, name) in CIE9.items():
    if chk(cie10_code) is None:
        missing.append(cie10_code)

if __name__ == "__main__":
    print("correlación CIE-9:", len(CIE9))
    print("MISSING (código CIE-10 inválido):", len(missing))
    for m in missing:
        print("MISS", m)
