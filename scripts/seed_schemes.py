import os
import sqlite3
import sys

# Ensure project root is in sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import config

# Comprehensive list of official schemes (Central + State specific)
SCHEMES_DATA = [
    # --- CENTRAL SCHEMES ---
    {
        "name": "PM Kisan Samman Nidhi",
        "name_hi": "पीएम किसान सम्मान निधि",
        "state": "Central",
        "official_url": "https://pmkisan.gov.in",
        "description": "Central government scheme providing ₹6,000 per year in three equal installments of ₹2,000 directly into the bank accounts of all landholding farmers.",
        "description_hi": "केंद्र सरकार की योजना जो सभी भूमिधारक किसानों के बैंक खातों में सीधे ₹2,000 की तीन समान किश्तों में प्रति वर्ष ₹6,000 प्रदान करती है।",
        "keywords": "pm kisan pm-kisan 6000 2000 samman nidhi installments direct benefit transfer kisan dbt cash support kisan card पीएम किसान सम्मान निधि किश्त सहायता राशि"
    },
    {
        "name": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
        "name_hi": "प्रधानमंत्री फसल बीमा योजना (PMFBY)",
        "state": "Central",
        "official_url": "https://pmfby.gov.in",
        "description": "Financial crop insurance scheme protecting farmers against crop loss due to natural calamities, pests, and severe weather with minimal premium rates.",
        "description_hi": "प्राकृतिक आपदाओं, कीटों और खराब मौसम के कारण फसल के नुकसान के खिलाफ न्यूनतम प्रीमियम दरों पर किसानों को सुरक्षा प्रदान करने वाली वित्तीय फसल बीमा योजना।",
        "keywords": "pmfby crop insurance fasal bima yojana crop loss premium claim weather risk dry rain flood policy फसल बीमा योजना क्लेम नुकसान मौसम"
    },
    {
        "name": "Kisan Credit Card (KCC)",
        "name_hi": "किसान क्रेडिट कार्ड (KCC)",
        "state": "Central",
        "official_url": "https://www.myscheme.gov.in/schemes/kcc",
        "description": "Provides credit support and short-term agricultural bank loans to farmers for seeds, fertilizer, and crop cultivation at heavily subsidized interest rates.",
        "description_hi": "किसानों को रियायती ब्याज दरों पर बीज, खाद और फसल की खेती के लिए ऋण सहायता और अल्पकालिक कृषि बैंक ऋण प्रदान करता है।",
        "keywords": "kcc kisan credit card crop loan bank loan interest subsidy nabard short term credit limit crop credit किसान क्रेडिट कार्ड ऋण ब्याज छूट बैंक लोन"
    },
    {
        "name": "PM Kusum Scheme",
        "name_hi": "पीएम कुसुम योजना",
        "state": "Central",
        "official_url": "https://www.myscheme.gov.in/schemes/pmkssy",
        "description": "Enables farmers to install solar agriculture water pumps with up to 60% subsidy support, replacing diesel generators and reducing irrigation costs.",
        "description_hi": "किसानों को सिंचाई लागत कम करने के लिए डीजल जनरेटर के स्थान पर 60% तक सब्सिडी पर सोलर कृषि जल पंप स्थापित करने में सक्षम बनाता है।",
        "keywords": "pm kusum solar pump water pump irrigation solar panels subsidy standalone grid tube well tubewell कुसुम योजना सोलर पंप सिंचाई जल"
    },
    {
        "name": "Soil Health Card Scheme",
        "name_hi": "मृदा स्वास्थ्य कार्ड योजना",
        "state": "Central",
        "official_url": "https://www.myscheme.gov.in/schemes/shc",
        "description": "Assists states to issue Soil Health Cards that provide detailed recommendations on appropriate nutrient/fertilizer application for individual farms.",
        "description_hi": "राज्यों को मृदा स्वास्थ्य कार्ड जारी करने में सहायता करती है जो व्यक्तिगत खेतों के लिए उचित पोषक तत्व/उर्वरक आवेदन पर विस्तृत सिफारिशें प्रदान करते हैं।",
        "keywords": "soil health card test testing lab fertilizer application recommendation nitrogen phosphorus potassium npk soil health card मृदा स्वास्थ्य कार्ड मिट्टी जांच खाद की मात्रा"
    },
    {
        "name": "National Agriculture Market (e-NAM)",
        "name_hi": "राष्ट्रीय कृषि बाजार (e-NAM)",
        "state": "Central",
        "official_url": "https://enam.gov.in",
        "description": "An online unified digital trading platform linking physical APMC mandis across India to help farmers find better buyers and transparent prices.",
        "description_hi": "एक ऑनलाइन एकीकृत डिजिटल ट्रेडिंग प्लेटफॉर्म जो किसानों को बेहतर खरीदार और पारदर्शी मूल्य खोजने में मदद करने के लिए भारत भर की भौतिक APMC मंडियों को जोड़ता है।",
        "keywords": "enam e-nam apmc mandi online trade crop price digital auction unified market transparent selling ई-नाम मंडी बोली मूल्य फसल"
    },

    # --- CHHATTISGARH SCHEMES ---
    {
        "name": "Godhan Nyay Yojana",
        "name_hi": "गोधन न्याय योजना",
        "state": "Chhattisgarh",
        "official_url": "https://cgstate.gov.in/scheme/detail/17",
        "description": "Chhattisgarh state scheme focused on purchasing cow dung (gobar) and cattle waste from registered cattle rearers to produce organic vermicompost.",
        "description_hi": "छत्तीसगढ़ राज्य की योजना जो जैविक केंचुआ खाद बनाने के लिए पंजीकृत पशुपालकों से गोबर और कंडे खरीदने पर केंद्रित है।",
        "keywords": "chhattisgarh cg gobar kande cow dung dung selling organic fertilizer godhan nyay gobar khareed kande bechna गोबर कंडे छत्तीसगढ़ गोधन न्याय पशुपालन"
    },
    {
        "name": "Rajiv Gandhi Kisan Nyay Yojana (RGKNY)",
        "name_hi": "राजीव गांधी किसान न्याय योजना",
        "state": "Chhattisgarh",
        "official_url": "https://cgstate.gov.in",
        "description": "Provides crop input subsidies of up to ₹9,000 per acre to farmers cultivating paddy, maize, sugarcane, kodo-kutki, and pulses in Chhattisgarh.",
        "description_hi": "छत्तीसगढ़ में धान, मक्का, गन्ना, कोदो-कुटकी और दलहन की खेती करने वाले किसानों को ₹9,000 प्रति एकड़ तक की इनपुट सब्सिडी सहायता प्रदान करती है।",
        "keywords": "rajiv gandhi kisan nyay rgkny paddy dhan bonus crop subsidy maize sugarcane pulses chhattisgarh cg input subsidy छत्तीसगढ़ धान बोनस मक्का गन्ना दलहन राजीव गांधी"
    },

    # --- JHARKHAND SCHEMES ---
    {
        "name": "Jharkhand Krishi Karj Mafi Yojana (JKKMY)",
        "name_hi": "झारखंड कृषि ऋण माफी योजना",
        "state": "Jharkhand",
        "official_url": "https://jkcmy.jharkhand.gov.in",
        "description": "Jharkhand state government scheme waiving off short-term agricultural loans up to ₹50,000 for standard landholding farmers.",
        "description_hi": "झारखंड राज्य सरकार की योजना जो मानक भूमिधारक किसानों के लिए ₹50,000 तक के अल्पकालिक कृषि ऋण को माफ करती है।",
        "keywords": "jharkhand jk karj mafi loan waiver crop loan waiver farm debt relief rin mafi ऋण माफी कर्ज माफी झारखंड बैंक ऋण"
    },
    {
        "name": "Mukhyamantri Sookha Rahat Yojana (MSRY)",
        "name_hi": "मुख्यमंत्री सूखा राहत योजना",
        "state": "Jharkhand",
        "official_url": "https://jrfry.jharkhand.gov.in",
        "description": "Drought relief assistance scheme in Jharkhand providing immediate financial support of ₹3,500 to farmers affected by severe crop failure and dry monsoon spells.",
        "description_hi": "झारखंड में सूखा राहत सहायता योजना जो गंभीर फसल विफलता और सूखे मानसून से प्रभावित किसानों को ₹3,500 की तत्काल वित्तीय सहायता प्रदान करती है।",
        "keywords": "sookha rahat drought relief jharkhand jk 3500 msry dry crop loss compensation सूखा राहत झारखंड सूखाड़ वित्तीय सहायता मुख्यमंत्री"
    },

    # --- MAHARASHTRA SCHEMES ---
    {
        "name": "Namo Shetkari Mahasanman Nidhi Yojana",
        "name_hi": "नमो शेतकारी महासन्मान निधी योजना",
        "state": "Maharashtra",
        "official_url": "https://maharashtra.gov.in",
        "description": "State scheme in Maharashtra providing an additional ₹6,000 per year in matching installments of ₹2,000 directly to PM-Kisan beneficiary farmers.",
        "description_hi": "महाराष्ट्र सरकार की योजना जो पीएम-किसान लाभार्थी किसानों को सीधे प्रति वर्ष अतिरिक्त ₹6,000 (₹2,000 की किश्तों में) प्रदान करती है।",
        "keywords": "namo shetkari mahasanman nidhi maharashtra mh shetkari samman matching 6000 shetkari pension नमो शेतकारी महासन्मान महाराष्ट्र किसान"
    },

    # --- RAJASTHAN SCHEMES ---
    {
        "name": "Mukhyamantri Krishak Sathi Yojana",
        "name_hi": "मुख्यमंत्री कृषक साथी योजना",
        "state": "Rajasthan",
        "official_url": "https://rajasthan.gov.in",
        "description": "Rajasthan government umbrella scheme offering insurance payouts, subsidies for farm ponds, wire fencing, and organic fertilizer distribution.",
        "description_hi": "राजस्थान सरकार की योजना जो कृषि तालाबों, तारबंदी (तार फेंसिंग) और जैविक खाद वितरण के लिए बीमा भुगतान और सब्सिडी प्रदान करती है।",
        "keywords": "krishak sathi rajasthan rj pond subsidy fencing wire fencing organic inputs farm assistance कृषक साथी राजस्थान फेंसिंग तारबंदी तालाब"
    },

    # --- KARNATAKA SCHEMES ---
    {
        "name": "Krishi Bhagya Yojana",
        "name_hi": "कृषि भाग्य योजना",
        "state": "Karnataka",
        "official_url": "https://karnataka.gov.in",
        "description": "Rainwater harvesting scheme in Karnataka supporting dryland farmers with subsidies to construct farm ponds, install diesel pumps, and purchase micro-sprinklers.",
        "description_hi": "कर्नाटक में वर्षा जल संचयन योजना जो शुष्क भूमि के किसानों को कृषि तालाब बनाने, डीजल पंप और स्प्रिंकलर स्थापित करने के लिए सब्सिडी देती है।",
        "keywords": "krishi bhagya rain harvesting farm pond pond subsidy karnataka ka dryland farming water irrigation krishi bhagya कृषि भाग्य कर्नाटक तालाब"
    },

    # --- UTTAR PRADESH SCHEMES ---
    {
        "name": "UP Crop Loan Redemption Scheme",
        "name_hi": "उत्तर प्रदेश फसल ऋण मोचन योजना",
        "state": "Uttar Pradesh",
        "official_url": "https://upkisankarjmafi.cgg.gov.in",
        "description": "Uttar Pradesh scheme waiving off agricultural crop loans up to ₹1 Lakh for small and marginal landholding farmers from institutional banks.",
        "description_hi": "उत्तर प्रदेश सरकार की योजना जो संस्थागत बैंकों से लघु और सीमांत किसानों के लिए ₹1 लाख तक के कृषि फसल ऋण को माफ करती है।",
        "keywords": "up karj mafi kisan loan waiver crop loan redemption uttar pradesh lakh waiver ऋण मोचन कर्ज माफी उत्तर प्रदेश लघु किसान"
    },

    # --- ODISHA SCHEMES ---
    {
        "name": "KALIA Scheme",
        "name_hi": "कालिया योजना (KALIA)",
        "state": "Odisha",
        "official_url": "https://www.myscheme.gov.in/schemes/kalia",
        "description": "Krushak Assistance for Livelihood and Income Augmentation scheme in Odisha providing seed capital, crop loan waivers, and insurance cover to farmers and landless laborers.",
        "description_hi": "ओडिशा में किसानों और भूमिहीन कृषि श्रमिकों को कार्यशील पूंजी, ब्याज मुक्त फसल ऋण और जीवन बीमा कवर प्रदान करने वाली वित्तीय सहायता योजना।",
        "keywords": "kalia odisha orissa income augmentation landless labor seed money credit assistance financial aid कालिया ओडिशा भूमिहीन श्रमिक"
    }
]

def seed_schemes():
    db_path = config.DATABASE_PATH
    print(f"Connecting to database at {db_path}...")
    
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='schemes_search'")
    if not cursor.fetchone():
        print("Error: schemes_search virtual table does not exist. Initializing database schema first...")
        from services.database import init_db
        init_db()
        
    print("Clearing existing schemes from schemes_search...")
    cursor.execute("DELETE FROM schemes_search")
    
    print(f"Seeding {len(SCHEMES_DATA)} agricultural schemes...")
    for scheme in SCHEMES_DATA:
        cursor.execute('''
            INSERT INTO schemes_search (name, name_hi, state, official_url, description, description_hi, keywords)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            scheme["name"],
            scheme["name_hi"],
            scheme["state"],
            scheme["official_url"],
            scheme["description"],
            scheme["description_hi"],
            scheme["keywords"]
        ))
        
    conn.commit()
    conn.close()
    print("Database seeding completed successfully!")

if __name__ == "__main__":
    seed_schemes()
