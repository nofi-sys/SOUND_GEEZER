import spacy
import random
nlp = spacy.load("es_core_news_lg")  # o "es_core_news_lg"


# Given ontology
audioteca_claves = {
    'HUMANO': {'VOZ':['DUB'],
               'SILBIDO':[],
               'RESPIRACIÓN':['RESP'],
               'LOCOMOCIÓN':['PASOS','CORRIDA','CAMINATA','PROCESION'],
               'DIGESTIÓN':['ESTOMAGO'],
               'MANOS':['PALMA', 'APLAUSO', 'PIÑA', 'GOLPE', 'APRETON'],
               'CORAZÓN':['LATIDO'],
               'OTOACÚSTICO':[],
               'GRUPALES':['MULTITUD', 'ABUCHEO', 'APLAUSOS']},

    'ANIMAL': {'DOMÉSTICOS': ['PERRO', 'GATO', 'CANARIO'],
               'TRABAJADORES':['CABALLO', 'VACA', 'BUEY', 'TORO', 'GANSO', 'PAVO'],
               'SALVAJES':[]},
    'NATURAL': {'VIENTO':[], 'TORMENTA':[], 'AGUA':['RIO', 'MAR', 'OLA'], 'FUEGO':[]},
    'MUSICAL': {'INSTRUMENTO':[], 'GÉNERO':[], 'CONCEPTO':[], 'ROL':[], 'MOOD':[]},
    'COSAS': {'VEHÍCULOS':['AUTO', 'CAMION', 'CAMIONETA', 'TRACTOR', 'MOTO', 'CICLOMOTOR', 'SCOOTER' ],
              'MOTORES':[], 'DOMÉSTICOS':['BICICLETA', 'TRICICLO',], 'CAMPANAS':[], 'ALARMAS':[], 'MECANISMOS':['PEDAL', 'CADENA'], 'HERRAMIENTAS':[], 'EXPLOSIONES':[],
              'MADERA':[], 'VIDRIO':[], 'LÍQUIDO':[], 'MISCELANEA':[], 'IMPACTO ESPECÍFICO':[]},
    'AMBIGUOS': {'IMPACTO GENERAL':[], 'CONTACTO CON SUPERFICIE':[], 'ESTRUCTURA DEFORMABLE':[], 'ONOMATOPEYA':[], 'SILENCIO':[],
                 'OTROS':[]},
    'FÁCTICOS': {'ENTORNO':[], 'RUIDO':[], 'REPRODUCCIÓN':[]},
    'SIN CLASIFICAR': []}

estructura_audioteca = {
    'HUMANO': ['VOZ', 'SILBIDO', 'RESPIRACIÓN', 'LOCOMOCIÓN', 'DIGESTIÓN', 'MANOS', 'CORAZÓN', 'OTOACÚSTICO',
               'GRUPALES'],
    'ANIMAL': ['DOMÉSTICOS', 'TRABAJADORES', 'SALVAJES'],
    'NATURAL': ['VIENTO', 'TORMENTA', 'AGUA', 'FUEGO'],
    'MUSICAL': ['INSTRUMENTO', 'GÉNERO', 'CONCEPTO', 'ROL', 'MOOD'],
    'COSAS': ['VEHÍCULOS', 'MOTORES', 'DOMÉSTICOS', 'CAMPANAS', 'ALARMAS', 'MECANISMOS', 'HERRAMIENTAS', 'EXPLOSIONES',
              'MADERA', 'VIDRIO', 'LÍQUIDO', 'MISCELANEA', 'IMPACTO ESPECÍFICO'],
    'AMBIGUOS': ['IMPACTO GENERAL', 'CONTACTO CON SUPERFICIE', 'ESTRUCTURA DEFORMABLE', 'ONOMATOPEYA', 'SILENCIO',
                 'OTROS'],
    'FÁCTICOS': ['ENTORNO', 'RUIDO', 'REPRODUCCIÓN'],
    'SIN CLASIFICAR': []}

# Flatten the ontology to create a mapping from subject to category
subject_to_category = {}
for category, subcategories in audioteca_claves.items():
    for subcategory in subcategories:
        subjects = subcategories[subcategory]
        for subject in subjects:
            subject_to_category[subject.lower()] = subcategory.lower()

# Create a function to find alternative subjects based on the ontology
def get_alternative_subjects(subject):
    alternative_subjects = []

    for main_category, subcategories in audioteca_claves.items():
        for subcategory in subcategories:
            subjects = subcategories[subcategory]
            if subject in subjects:
                alternative_subjects = [s for s in subjects if s != subject]
                break

        # Break the outer loop if alternative_subjects is found
        if alternative_subjects:
            break

    return alternative_subjects

print(get_alternative_subjects('GATO'))

# Generate alternatives based on the given ontology and subject-to-category mapping
def get_alternatives(filename):

    doc = nlp(filename)

    # Detect subject, verb, and object using POS tagging
    subject, verb, obj = None, None, None
    for token in doc:
        print (token.pos, token.pos_, token.dep_)
        if token.pos_ == "NOUN":
            subject = token
        elif token.pos_ == "VERB":
            verb = token
        elif token.pos_ == "PROPN" or token.pos_ == "ADJ":
            obj = token

    # Generate alternatives based on the detected subject, verb, and object
    alternatives = []
    if subject and verb:
        alt_subjects = get_alternative_subjects(subject.text)
        for alt_subject in alt_subjects:
            alt_filename = f"{alt_subject} {verb.text}"
            if obj:
                alt_filename += f" {obj.text}"
            alternatives.append(alt_filename)

    return alternatives




filename = "juan pedalea"
alternatives = get_alternatives(filename)
print(alternatives)
