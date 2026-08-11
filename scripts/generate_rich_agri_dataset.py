import os
import sys
import pandas as pd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CUSTOM_AGRI_PATH = os.path.join(BASE_DIR, 'data', 'custom_agri_messages.csv')

# Explicitly written, unique, non-repetitive messages
GENUINE_MESSAGES = [
    # PM-KISAN
    "Under PM-KISAN scheme, eligible landholding farmer families receive Rs 6000 per year in three equal installments of Rs 2000 transferred directly into bank accounts via DBT. Check details on official portal pmkisan.gov.in.",
    "PM-KISAN 17th installment release date has been officially announced by the Agriculture Ministry. Farmers can check DBT status on pmkisan.gov.in.",
    "Farmers are requested to complete PM-KISAN e-KYC through OTP based authentication on pmkisan.gov.in portal or biometric authentication at nearest CSC centers.",
    "Aadhaar seed link with bank account is mandatory for PM-KISAN benefits. Visit nearest post office or bank branch for direct benefit transfer setup.",
    "PM-KISAN beneficiary status can be tracked using mobile number or registration number on pmkisan.gov.in official portal.",
    "Kisan Samman Nidhi scheme provides direct financial support to small and marginal farmer families to meet farm input expenses.",
    "Eligible farmers who have not received PM-KISAN installment can raise a grievance on pmkisan-ict@gov.in or contact district agriculture office.",
    
    # PMFBY (Crop Insurance)
    "Pradhan Mantri Fasal Bima Yojana (PMFBY) provides comprehensive crop insurance coverage against non-preventable natural risks from pre-sowing to post-harvest.",
    "PMFBY enrollment cut-off date for Kharif crops is approaching. Farmers can register at pmfby.gov.in or visit nearest bank branch or CSC center.",
    "PMFBY claims are calculated based on Crop Cutting Experiments (CCE) data and yield estimates submitted by state agriculture departments.",
    "Crop loss notification under PMFBY must be reported within 72 hours of localized calamity occurrence via Crop Insurance App or toll-free number 1800-200-5142.",
    "Farmers can check crop insurance premium calculation for different crops across districts on official portal pmfby.gov.in.",
    "PMFBY covers crop damages due to drought, flood, inundation, unseasonal rainfall, landslide, cyclone, and pest attacks.",
    
    # KCC & Credit
    "Kisan Credit Card (KCC) scheme provides adequate and timely credit support from the banking system to farmers for cultivation and farm maintenance at 4% effective interest rate.",
    "Government of India offers 2% interest subvention and 3% prompt repayment incentive on short-term crop loans up to Rs 3 lakh through KCC.",
    "Animal husbandry and fisheries farmers are also eligible for Kisan Credit Card (KCC) credit facilities up to Rs 2 lakh at concessional interest rates.",
    "Farmers can apply for Kisan Credit Card at any commercial bank, Regional Rural Bank (RRB), or Cooperative Bank branch with basic land records.",
    "KCC credit limit is fixed based on crop pattern, cultivated area, and scale of finance approved by District Level Technical Committee.",

    # e-NAM & APMC
    "The National Agriculture Market (e-NAM) is an online trading platform for agricultural commodities linking APMC mandis to create a unified national market. Portal: enam.gov.in.",
    "Farmers can check real-time commodity prices and mandi arrival trends across all states on e-NAM mobile app or official portal enam.gov.in.",
    "e-NAM platform enables online bidding, direct payment into farmer bank accounts, and assaying support for quality testing in notified APMC mandis.",
    "Mandi price transparency is facilitated by e-NAM portal linking over 1300 wholesale mandis across India.",
    
    # Soil Health & Fertilizers
    "Soil Health Card scheme assists state governments to issue Soil Health Cards containing crop-wise recommendations of nutrients and fertilizers for individual farms.",
    "Soil Health Card provides recommendations on 12 key soil parameters including N, P, K, S, Zinc, Iron, Manganese, Copper, Boron, and pH levels.",
    "PM-PRANAM scheme aims to incentivize states to promote alternative fertilizers and balanced use of chemical fertilizers to protect soil health.",
    "Farmers are advised to use Nano Urea and Nano DAP liquid sprays as per ICAR guidelines to reduce chemical fertilizer consumption and input costs.",
    "ICAR recommends soil sample collection after harvest and before sowing to get accurate fertilizer dose recommendations.",
    "Organic carbon enrichment in soil can be improved by applying farmyard manure, vermicompost, and green manure crops like dhaincha.",

    # PM-KUSUM & Solar
    "Under PM-KUSUM Component-B, individual farmers can install standalone solar agriculture pumps with up to 60 percent subsidy from central and state government.",
    "PM-KUSUM Component-C allows solarisation of grid-connected agriculture pumps enabling farmers to sell surplus solar power back to DISCOMs.",
    "Farmers can apply for solar pump subsidy under PM-KUSUM scheme only through official state nodal energy agency portals or mnre.gov.in.",
    "PM-KUSUM scheme helps farmers reduce dependence on diesel pumps and ensures reliable day-time irrigation power.",

    # SMAM, RKVY, PKVY, AIF, MIDH
    "Sub-Mission on Agricultural Mechanization (SMAM) provides financial assistance and subsidy for farm machinery procurement through official portal agrimachinery.nic.in.",
    "Paramparagat Krishi Vikas Yojana (PKVY) promotes cluster-based organic farming with financial assistance of Rs 50,000 per hectare over three years for organic inputs.",
    "Agriculture Infrastructure Fund (AIF) provides medium-long term debt financing facility with 3% interest subvention for post-harvest infrastructure projects.",
    "Mission for Integrated Development of Horticulture (MIDH) supports holistic growth of horticulture sector including fruits, vegetables, spices, and flowers.",
    "Custom Hiring Centers (CHC) established under SMAM enable small and marginal farmers to rent expensive farm equipment at affordable rates.",
    "RKVY-RAFTAAR scheme empowers states to execute location-specific agriculture development projects and support agri-startups.",

    # MSP & ICAR Advisories
    "The Cabinet Committee on Economic Affairs (CCEA) approves Minimum Support Prices (MSP) for mandated Kharif and Rabi crops based on CACP recommendations.",
    "Integrated Pest Management (IPM) techniques recommend field monitoring, pheromone traps, and bio-pesticides before applying chemical pesticide sprays.",
    "Farmers are advised to check weather updates from India Meteorological Department (IMD) Meghdoot mobile app for location-specific agricultural forecasts.",
    "Kisan Call Center operates toll-free number 1800-180-1551 providing expert agricultural advice to farmers in local languages from 6 AM to 10 PM daily.",
    "National Seeds Corporation (NSC) provides certified high-yielding seed varieties for wheat, paddy, pulses, and oilseeds via authorized portals like indiaseeds.com.",
    "Dharani portal and state land record portals provide digital land record verification for crop loan sanction and subsidy processing.",
    "System of Rice Intensification (SRI) method reduces seed rate, water requirement, and production costs in paddy cultivation.",
    "Pusa decomposer capsule developed by ICAR assists in rapid in-situ decomposition of paddy straw residue.",

    # Short Genuine Claims
    "PM-KISAN official website is pmkisan.gov.in.",
    "Crop insurance claim helpline number is 1800-200-5142.",
    "Check daily mandi rates on enam.gov.in.",
    "Soil health testing available at local KVK centers.",
    "Certified seeds available at National Seeds Corporation outlets.",
    "Kisan Credit Card interest rate is 4 percent upon timely repayment.",
    "PM Kusum scheme official solar pump application portal is mnre.gov.in.",

    # Hinglish Genuine Messages
    "PM Kisan Yojana ki 17th kist 2000 rupey direct farmer ke bank account me credit ki gayi hai. Detail ke liye official website pmkisan.gov.in par check karein.",
    "Soil Health Card banwane ke liye apne nearest Krishi Vigyan Kendra ya agriculture officer se sampark karein. Official portal: agricoop.nic.in.",
    "Kisan Credit Card (KCC) par interest rate subsidised hai. Apne bank branch me jaakar form bharein aur 4 percent interest rate ka labh uthayein.",
    "Fasal bima yojana ka claim lene ke liye 72 ghante ke andar toll free number 1800-200-5142 par complaint register karayein.",
    "PM Kusum solar pump yojana ke liye kewal official rajya government portal ya mnre.gov.in par hi aavedan karein.",
    "e-NAM portal par mandi ke taaza bhav check karne ke liye enam.gov.in website visit karein.",
    "Beej khareedne ke liye certified National Seeds Corporation ki website indiaseeds.com ka upyog karein."
]

MISLEADING_MESSAGES = [
    # Tractor Scams
    "Urgent: Government is providing 90% subsidy on buying new Mahindra tractors under PM Kisan Tractor Scheme 2026. Click here http://pmkisan-tractor-subsidy.online to apply immediately!",
    "Claim your free mini tractor! Government selected 5000 farmers for free machinery distribution. Verify your phone number at http://free-tractor-scheme.org.",
    "Government announced 95 percent discount on drone sprayers for all small farmers who submit Aadhaar details and Rs 500 processing fee to WhatsApp admin.",
    "PM Modi tractor yojana: Sabhi kisano ko mil raha hai free tractor. Aavedan ke liye link kholo http://pm-tractor-yojana.site.",
    "Free Swaraj Tractor Scheme 2026: Share this message to 10 WhatsApp groups and fill form on http://free-swaraj-tractor.info to win tractor.",
    "Government is distributing 10,000 free rotavators and harvesters. Register on http://free-farm-equipment.com before stock runs out.",

    # Cash & Bonus Scams
    "PM Modi is giving Rs 15000 cash bonus to every farmer who forwards this message to 5 WhatsApp contacts and fills out the form at http://pm-bonus-kisan.info!",
    "Special relief scheme: Every farmer with a tubewell gets Rs 50000 direct bank transfer if they click this link and enter bank OTP http://kisan-relief-fund.net.",
    "Government is paying Rs 2000 per month pension to all farmers above 18 years without any contribution. Register at http://kisan-pension-free.site.",
    "Click here to double your PM Kisan payment from Rs 6000 to Rs 12000 annually by submitting your bank PIN on http://pmkisan-double-bonus.com!",
    "Kisan Samman Nidhi bonus bonus: Govt sending Rs 4000 extra bonus tonight into bank accounts! Click http://kisan-dbt-bonus.xyz to claim.",
    "Central govt announced Rs 25,000 festival gift for all agricultural laborers. Enter bank details on http://kisan-gift-2026.online.",
    "Sabhi kisaanon ko milenge 10,000 rupey direct account me! Link par click karke aadhar number dalein http://kisan-cash-dbt.site.",

    # Phishing & Mandatory Fee Demands
    "URGENT ATTENTION: PM Kisan Scheme payment has been suspended for all farmers. To unblock your account pay Rs 250 processing fee at http://pmkisan-unblock-dbt.site within 24 hours.",
    "Mandatory eKYC update for PM Kisan: Pay Rs 99 at http://pmkisan-ekyc-now.org to avoid cancellation of your 17th installment.",
    "Alert: Government will confiscate agricultural land if farmers do not complete land link verification on http://kisan-land-verify.com before midnight!",
    "Urgent SMS: Pay Rs 150 processing fee at http://aif-infrastructure-loan.org to get instant 3% interest subvention for cold storage setup.",
    "Your PM Kisan bank account is locked! To activate DBT payment immediately click http://pmkisan-activate-dbt.info and enter OTP.",
    "Kisan Credit Card account freeze warning! Update KYC on http://kcc-kyc-verify.online within 12 hours to prevent loan cancellation.",
    "PM Kisan eKYC mandatory update: Send Rs 50 processing fee via PhonePe to UPI ID pmkisan-kyc@upi to get pending installment.",

    # Loan Waiver & Electricity Hoaxes
    "Government is waiving off all private bank tractor loans and farm credit card loans up to 10 lakhs automatically. Register your details at http://farm-loan-waiver.org now!",
    "Government announces 100% free electricity and free diesel for all tubewells across all states. Share this message to 10 WhatsApp groups to activate free power on your meter.",
    "Alert: Central government announced instant loan waiver for all Kisan Credit Card holders up to 5 lakh rupees on http://kcc-waiver-2026.net.",
    "PM Kisan Karza Mafi Scheme 2026: All farm loans up to 2 lakh completely waived off by PM Modi. Fill form on http://karza-mafi-kisan.info.",
    "Free tubewell electricity connection for life! No meter charges. Submit electricity bill copy on http://free-power-kisan.org.",

    # Fake Pest & Cultivation Advice
    "Attention farmers: Spraying concentrated salt solution on paddy crops completely destroys all insects and doubles crop yield in 3 days!",
    "Boiling neem leaves with diesel and spraying on cotton crops completely cures pink bollworm infestation overnight without damaging plants.",
    "Secret recipe revealed: Mixing detergent powder with kerosene oil and applying to wheat crops eliminates all fungal diseases instantly.",
    "Mixing salt water with vinegar and spraying on sugarcane fields doubles sugar content in 24 hours without chemical fertilizers.",
    "Guaranteed yield booster: Spraying sugar syrup mixed with urea on tomato plants increases fruit size by 300 percent in 48 hours.",
    "Bake salt and sulphur together and spread in field to permanently eliminate all weeds and pests forever.",

    # Rumors & Panic Messaging
    "Shocking news! Government has banned the sale of urea and DAP fertilizers across India starting tomorrow. Buy extra bags immediately before stock ends!",
    "Government is shutting down all APMC mandis nationwide from next Monday. Sell all your crop produce to private agents immediately at low rates!",
    "Warning: Government has banned all drip irrigation systems across India starting next week. Switch to flood irrigation immediately.",
    "Government declared all synthetic pesticides toxic and illegal starting tomorrow; farmers using chemical sprays face immediate imprisonment.",
    "Alert: Government will stop buying wheat at MSP from next season. Sell your harvest immediately to private traders.",

    # Free Seed/Tubewell Fraud
    "Government announced free seed kits distribution for wheat and rice to all farmers who pay Rs 199 shipping charge on http://free-beej-yojana.com.",
    "Government is giving free electricity transformers to every farm tubewell. Fill up form on http://free-transformer-yojana.com with your bank OTP.",
    "FPO registration fee waived off completely! Pay Rs 499 on http://fpo-india-reg.com to get instant 10 lakh government grant.",

    # Short Misleading & Deceptive Commercial Claims
    "Get 90% tractor subsidy at http://pmkisan-tractor.online.",
    "PM Kisan 10000 rupees extra bonus form at http://kisan-bonus.site.",
    "Pay Rs 99 for PM Kisan eKYC update on http://pmkisan-ekyc.info.",
    "Free solar pump without documents click http://free-solar-pump.xyz.",
    "Spray salt water and kerosene to kill paddy insects instantly.",
    "Government banning urea sales tomorrow buy stock now.",
    "KCC loan 5 lakh waived off apply at http://kcc-waiver.net.",
    "genuine agricture deal, buy from our portal agribharat.gov.in and get subsidy if eligible , first contact agricuklture ofice",
    "genuine agriculture deal buy from unverified portal and claim instant subsidy discount",
    "buy direct from our online private store to get 80 percent government subsidy refund",
    "special agriculture deal buy cheap fertilizers and pesticides from private site and claim cash back",
    "genuine farmer deal click here to buy subsidized seeds directly without government registration",
    "genuine agriculture scheme from government, jus register through our website and contact the helpline number for any doubts 7880283765",
    "contact helpline number 9876543210 for free tractor scheme registration",
    "register through our website and send payment to phone number 9123456789",

    # Hinglish Misleading Forwards
    "Sabhi kisan bhaiyo ko 90 percent subsidy par naya tractor mil raha hai. Form bharne ke liye link open karein http://kisan-tractor-subsidy.site aakhri tarikh kal hai.",
    "PM Kisan ki kist ruk gayi hai toh turant Rs 199 pay karke ekyc karein link http://pmkisan-ekyc-update.info par. 24 ghante me account block ho jayega.",
    "Kisan loan mukti yojana me 5 lakh tak ka loan maaf ho gaya hai. Apna Aadhar aur bank OTP is link http://kisan-loan-maaf.online par submit karein.",
    "Mupht tractor yojana 2026: Is WhatsApp message ko 10 logo ko bhejo aur http://free-tractor-yojana.info par apna naam darj karein.",
    "Sabhi kisano ko 15000 rupaye ki aarthik sahayata di ja rahi hai. Form bharne ke liye http://kisan-sahayata.xyz par click karein.",
    "Urea aur DAP par ban lag gaya hai kal se. Apne paas ke dukaan se saari khad abhi khareed lo warna stock khatam ho jayega."
]

def build_unique_dataset():
    records = []
    
    # Add genuine messages
    for msg in GENUINE_MESSAGES:
        records.append({
            "text": msg.strip(),
            "label": "genuine",
            "source": "Official Portal / Advisory",
            "category": "Agri Scheme / Advisory"
        })
        
    # Add misleading messages
    for msg in MISLEADING_MESSAGES:
        records.append({
            "text": msg.strip(),
            "label": "misleading",
            "source": "WhatsApp / Phishing SMS",
            "category": "Scam / Fake News"
        })
        
    df = pd.DataFrame(records)
    # Ensure no duplicates
    df = df.drop_duplicates(subset=['text']).reset_index(drop=True)
    df.to_csv(CUSTOM_AGRI_PATH, index=False)
    print(f"Generated {len(df)} 100% unique agri records in {CUSTOM_AGRI_PATH}")

if __name__ == '__main__':
    build_unique_dataset()
