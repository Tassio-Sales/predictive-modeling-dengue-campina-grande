"""
Clinical vocabulary aligned with SINAN dengue notification forms
and real-world dataset column names.

Vocabulary strategy:
- Official SINAN term
- Column name observed in dataset
- Common abbreviations / truncations
"""

SYMPTOMS = {
    "fever": [
        "FEBRE",
    ],

    "myalgia": [
        "MIALGIA",
    ],

    "headache": [
        "CEFALEIA",
        "CEFAL",
    ],

    "rash": [
        "EXANTEMA",
    ],

    "vomiting": [
        "VOMITO",
    ],

    "nausea": [
        "NAUSEA",
    ],

    "back_pain": [
        "DOR_COSTAS",
        "LOMBALGIA",
    ],

    "conjunctivitis": [
        "CONJUNTIVITE",
    ],

    "arthritis": [
        "ARTRITE",
    ],

    "severe_arthralgia": [
        "ARTRALGIA",
        "ARTRALGIA_INTENSA",
    ],

    "petechiae": [
        "PETEQUIA",
        "PETEQUIA_N",
    ],

    "leukopenia": [
        "LEUCOPENIA",
    ],

    "tourniquet_test": [
        "LACO",
        "PROVA_LACO",
        "LACO_N",
    ],

    "retroorbital_pain": [
        "DOR_RETRO",
        "DOR_RETROORBITAL",
    ],
}

COMORBIDITIES = {
    "diabetes": [
        "DIABETES",
        "DIABET",
    ],

    "hematologic_disease": [
        "HEMATOLOG",
        "HEMAT",
    ],

    "liver_disease": [
        "HEPATOPAT",
        "HEPAT",
    ],

    "chronic_renal_disease": [
        "RENAL",
    ],

    "hypertension": [
        "HIPERTENSA",
        "HIPERT",
        "HAS",
    ],

    "acid_peptic_disease": [
        "ACIDO_PEPT",
        "ACIDOPEPT",
    ],

    "autoimmune_disease": [
        "AUTO_IMUNE",
        "AUTOIMUNE",
    ],
}

ALARM_SIGNS = {
    "postural_hypotension_lipotimia": [
        "ALRM_HIPOT",
        "HIPOTENSAO_POSTURAL",
        "LIPOTIMIA",
    ],

    "platelet_drop": [
        "ALRM_PLAQ",
        "PLAQUET",
        "PLAQUETOPENIA",
    ],

    "persistent_vomiting": [
        "ALRM_VOM",
        "VOMITOS_PERSISTENTES",
    ],

    "severe_abdominal_pain": [
        "ALRM_ABDOM",
        "DOR_ABDOMINAL",
    ],

    "lethargy_irritability": [
        "ALRM_LETAR",
        "LETARGIA",
        "IRRITABILIDADE",
    ],

    "mucosal_bleeding": [
        "ALRM_SANG",
        "SANGRAMENTO",
        "HEMORRAGIA",
    ],

    "hematocrit_increase": [
        "ALRM_HEMAT",
        "HEMATOCRITO",
    ],

    "hepatomegaly": [
        "ALRM_HEPAT",
        "HEPATOMEGALIA",
    ],

    "fluid_accumulation": [
        "ALRM_LIQ",
        "ACUMULO_LIQUIDOS",
        "DERRAME",
    ],
}

SEVERITY_SIGNS = {
    "weak_pulse": [
        "GRAV_PULSO",
        "PULSO_DEBIL",
    ],

    "narrow_pulse_pressure": [
        "GRAV_CONV",
        "PA_CONVERGENTE",
    ],

    "capillary_refill_delay": [
        "GRAV_ENCH",
        "ENCHIMENTO_CAPILAR",
    ],

    "fluid_with_respiratory_failure": [
        "GRAV_INSUF",
        "INSUF_RESP",
        "INSUFICIENCIA_RESPIRATORIA",
    ],

    "tachycardia": [
        "GRAV_TAQUI",
        "TAQUICARDIA",
    ],

    "cold_extremities": [
        "GRAV_EXTRE",
        "EXTREMIDADES_FRIAS",
    ],

    "late_hypotension": [
        "GRAV_HIPOT",
        "HIPOTENSAO_TARDIA",
    ],

    "hematemesis": [
        "GRAV_HEMAT",
        "HEMATEMESE",
    ],

    "melena": [
        "GRAV_MELEN",
        "MELENA",
    ],

    "severe_metrorrhagia": [
        "GRAV_METRO",
        "METRORRAGIA",
    ],

    "cns_bleeding": [
        "GRAV_SANG",
        "SANGRAMENTO_SNC",
    ],

    "liver_failure": [
        "GRAV_AST",
        "AST",
        "ALT",
    ],

    "myocarditis": [
        "GRAV_MIOC",
        "MIOCARDITE",
    ],

    "altered_consciousness": [
        "GRAV_CONSC",
        "ALTERACAO_CONSCIENCIA",
    ],

    "other_organ_failure": [
        "GRAV_ORGAO",
        "OUTROS_ORGAOS",
    ],
}