import os
import sys
import pandas as pd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CUSTOM_AGRI_PATH = os.path.join(BASE_DIR, 'data', 'custom_agri_messages.csv')

# Base templates and variations for 1000 dataset expansion
GENUINE_TEMPLATES = [
    # PM-KISAN
    ("Under PM-KISAN scheme, eligible landholding farmer families receive Rs 6000 per year in three equal installments of Rs 2000 transferred directly into bank accounts via DBT. Check details on official portal pmkisan.gov.in.", "Official Government Portal", "Scheme Info"),
    ("PM-KISAN installment {num} for year {year} has been released by Prime Minister. Farmers can check DBT credit status on pmkisan.gov.in or Mobile App.", "Ministry Release", "Scheme Update"),
    ("Farmers are requested to complete PM-KISAN e-KYC through OTP based authentication on pmkisan.gov.in portal or biometric authentication at nearest CSC centers.", "Official Government Portal", "Scheme Info"),
    ("Aadhaar seed link with bank account is mandatory for PM-KISAN benefits. Visit nearest post office or bank branch for direct benefit transfer setup.", "Official Advisory", "Compliance"),
    
    # PMFBY (Crop Insurance)
    ("Pradhan Mantri Fasal Bima Yojana (PMFBY) provides comprehensive crop insurance coverage against non-preventable natural risks from pre-sowing to post-harvest.", "Official Agriculture Ministry", "Insurance"),
    ("PMFBY enrollment cut-off date for Kharif crops is approaching. Farmers can register at pmfby.gov.in or visit nearest bank branch or CSC center.", "PMFBY Portal", "Insurance"),
    ("PMFBY claims are calculated based on Crop Cutting Experiments (CCE) data and yield estimates submitted by state agriculture departments.", "Ministry Guidelines", "Insurance"),
    ("Crop loss notification under PMFBY must be reported within 72 hours of localized calamity occurrence via Crop Insurance App or toll-free number 1800-200-5142.", "PMFBY Advisory", "Insurance"),
    
    # KCC & Credit
    ("Kisan Credit Card (KCC) scheme provides adequate and timely credit support from the banking system to farmers for cultivation and farm maintenance at 4% effective interest rate.", "NABARD / RBI", "Credit"),
    ("Government of India offers 2% interest subvention and 3% prompt repayment incentive on short-term crop loans up to Rs 3 lakh through KCC.", "Reserve Bank Bulletin", "Credit Subvention"),
    ("Animal husbandry and fisheries farmers are also eligible for Kisan Credit Card (KCC) credit facilities up to Rs 2 lakh at concessional interest rates.", "Ministry Advisory", "Credit"),
    
    # e-NAM & APMC
    ("The National Agriculture Market (e-NAM) is an online trading platform for agricultural commodities linking APMC mandis to create a unified national market. Portal: enam.gov.in.", "Official Portal", "e-NAM"),
    ("Farmers can check real-time commodity prices and mandi arrival trends across all states on e-NAM mobile app or official portal enam.gov.in.", "e-NAM Portal", "Market Price"),
    ("e-NAM platform enables online bidding, direct payment into farmer bank accounts, and assaying support for quality testing in notified APMC mandis.", "Ministry Release", "Market Info"),
    
    # Soil Health Card & Fertilizers
    ("Soil Health Card scheme assists state governments to issue Soil Health Cards containing crop-wise recommendations of nutrients and fertilizers for individual farms.", "Official Portal", "Soil Health"),
    ("Soil Health Card provides recommendations on 12 key soil parameters including N, P, K, S, Zinc, Iron, Manganese, Copper, Boron, and pH levels.", "ICAR Advisory", "Soil Health"),
    ("PM-PRANAM scheme aims to incentivize states to promote alternative fertilizers and balanced use of chemical fertilizers to protect soil health.", "Ministry of Fertilizers", "Fertilizer Scheme"),
    ("Farmers are advised to use Nano Urea and Nano DAP liquid sprays as per ICAR guidelines to reduce chemical fertilizer consumption and input costs.", "ICAR Advisory", "Fertilizer"),

    # PM-KUSUM & Solar
    ("Under PM-KUSUM Component-B, individual farmers can install standalone solar agriculture pumps with up to 60 percent subsidy from central and state government.", "MNRE Official Scheme", "Solar Scheme"),
    ("PM-KUSUM Component-C allows solarisation of grid-connected agriculture pumps enabling farmers to sell surplus solar power back to DISCOMs.", "MNRE Portal", "Solar Scheme"),
    ("Farmers can apply for solar pump subsidy under PM-KUSUM scheme only through official state nodal energy agency portals or mnre.gov.in.", "MNRE Advisory", "Solar Verification"),
    
    # Submissions (SMAM, RKVY, MIDH, AIF, PKVY)
    ("Sub-Mission on Agricultural Mechanization (SMAM) provides financial assistance and subsidy for farm machinery procurement through official portal agrimachinery.nic.in.", "Ministry of Agriculture", "Mechanization"),
    ("Paramparagat Krishi Vikas Yojana (PKVY) promotes cluster-based organic farming with financial assistance of Rs 50,000 per hectare over three years for organic inputs.", "Official Ministry Portal", "Organic Farming"),
    ("Agriculture Infrastructure Fund (AIF) provides medium-long term debt financing facility with 3% interest subvention for post-harvest infrastructure projects.", "Ministry Release", "Infrastructure"),
    ("Mission for Integrated Development of Horticulture (MIDH) supports holistic growth of horticulture sector including fruits, vegetables, spices, and flowers.", "Horticulture Department", "Horticulture"),
    
    # MSP & ICAR Pest/Crop Advisories
    ("The Cabinet Committee on Economic Affairs (CCEA) approves Minimum Support Prices (MSP) for mandated Kharif and Rabi crops based on CACP recommendations.", "Press Information Bureau", "MSP"),
    ("Integrated Pest Management (IPM) techniques recommend field monitoring, pheromone traps, and bio-pesticides before applying chemical pesticide sprays.", "ICAR Extension Bulletin", "Pest Management"),
    ("Farmers are advised to check weather updates from India Meteorological Department (IMD) Meghdoot mobile app for location-specific agricultural forecasts.", "IMD Advisory", "Weather Advisory"),
    ("Kisan Call Center operates toll-free number 1800-180-1551 providing expert agricultural advice to farmers in local languages from 6 AM to 10 PM daily.", "Ministry Support Line", "Kisan Helpline"),
    ("National Seeds Corporation (NSC) provides certified high-yielding seed varieties for wheat, paddy, pulses, and oilseeds via authorized portals like indiaseeds.com.", "NSC Portal", "Certified Seeds"),
    
    # Hinglish Genuine Bulletins
    ("PM Kisan Yojana ki 17th kist 2000 rupey direct farmer ke bank account me credit ki gayi hai. Detail ke liye official website pmkisan.gov.in par check karein.", "Government Notice Hinglish", "Scheme Update"),
    ("Soil Health Card banwane ke liye apne nearest Krishi Vigyan Kendra ya agriculture officer se sampark karein. Official portal: agricoop.nic.in.", "KVK Advisory", "Soil Info"),
    ("Kisan Credit Card (KCC) par interest rate subsidised hai. Apne bank branch me jaakar form bharein aur 4 percent interest rate ka labh uthayein.", "Bank Notice Hinglish", "KCC Info")
]

MISLEADING_TEMPLATES = [
    # Tractor & Machinery Scams
    ("Urgent: Government is providing 90% subsidy on buying new Mahindra tractors under PM Kisan Tractor Scheme {year}. Click here http://pmkisan-tractor-subsidy.online to apply immediately!", "WhatsApp Forward", "Scheme Scam"),
    ("Claim your free mini tractor! Government selected 5000 farmers for free machinery distribution. Verify your phone number at http://free-tractor-scheme.org.", "WhatsApp Scam", "Scam"),
    ("Government announced 95 percent discount on drone sprayers for all small farmers who submit Aadhaar details and Rs 500 processing fee to WhatsApp admin.", "WhatsApp Forward", "Phishing Scam"),
    
    # Cash & Pension Scams
    ("PM Modi is giving Rs 15000 cash bonus to every farmer who forwards this message to 5 WhatsApp contacts and fills out the form at http://pm-bonus-kisan.info!", "WhatsApp Forward", "Viral Scam"),
    ("Special relief scheme: Every farmer with a tubewell gets Rs 50000 direct bank transfer if they click this link and enter bank OTP http://kisan-relief-fund.net.", "Phishing Scam", "Phishing Scam"),
    ("Government is paying Rs 2000 per month pension to all farmers above 18 years without any contribution. Register at http://kisan-pension-free.site.", "WhatsApp Forward", "Fake Scheme"),
    ("Click here to double your PM Kisan payment from Rs 6000 to Rs 12000 annually by submitting your bank PIN on http://pmkisan-double-bonus.com!", "Phishing Scam", "Phishing Scam"),
    
    # Phishing & Mandatory Fee Demands
    ("URGENT ATTENTION: PM Kisan Scheme payment has been suspended for all farmers. To unblock your account pay Rs 250 processing fee at http://pmkisan-unblock-dbt.site within 24 hours.", "Phishing SMS", "Phishing Scam"),
    ("Mandatory eKYC update for PM Kisan: Pay Rs 99 at http://pmkisan-ekyc-now.org to avoid cancellation of your {num}th installment.", "Phishing SMS", "Phishing Scam"),
    ("Alert: Government will confiscate agricultural land if farmers do not complete land link verification on http://kisan-land-verify.com before midnight!", "Phishing SMS", "Panic Phishing"),
    ("Urgent SMS: Pay Rs 150 processing fee at http://aif-infrastructure-loan.org to get instant 3% interest subvention for cold storage setup.", "Phishing SMS", "Loan Scam"),

    # Loan Waiver & Free Electricity Hoaxes
    ("Government is waiving off all private bank tractor loans and farm credit card loans up to 10 lakhs automatically. Register your details at http://farm-loan-waiver.org now!", "WhatsApp Forward", "Loan Scam"),
    ("Government announces 100% free electricity and free diesel for all tubewells across all states. Share this message to 10 WhatsApp groups to activate free power on your meter.", "Viral Chain Message", "Viral Scam"),
    ("Alert: Central government announced instant loan waiver for all Kisan Credit Card holders up to 5 lakh rupees on http://kcc-waiver-{year}.net.", "Phishing SMS", "Loan Scam"),
    
    # Fake Pest & Cultivation Advice
    ("Attention farmers: Spraying concentrated salt solution on paddy crops completely destroys all insects and doubles crop yield in 3 days!", "Social Media Advice", "Fake Pest Advice"),
    ("Boiling neem leaves with diesel and spraying on cotton crops completely cures pink bollworm infestation overnight without damaging plants.", "WhatsApp Advisory", "Fake Advisory"),
    ("Secret recipe revealed: Mixing detergent powder with kerosene oil and applying to wheat crops eliminates all fungal diseases instantly.", "Social Media Advice", "Fake Advisory"),
    ("Mixing salt water with vinegar and spraying on sugarcane fields doubles sugar content in 24 hours without chemical fertilizers.", "Social Media Advice", "Fake Advisory"),

    # Rumors & Panic Messaging
    ("Shocking news! Government has banned the sale of urea and DAP fertilizers across India starting tomorrow. Buy extra bags immediately before stock ends!", "Social Media Rumor", "Fertilizer Rumor"),
    ("Government is shutting down all APMC mandis nationwide from next Monday. Sell all your crop produce to private agents immediately at low rates!", "Panic Messaging", "Panic Rumor"),
    ("Warning: Government has banned all drip irrigation systems across India starting next week. Switch to flood irrigation immediately.", "Social Media Rumor", "Panic Messaging"),
    ("Government declared all synthetic pesticides toxic and illegal starting tomorrow; farmers using chemical sprays face immediate imprisonment.", "Social Media Rumor", "Panic Rumor"),

    # Free Seed/Tubewell Fraud
    ("Government announced free seed kits distribution for wheat and rice to all farmers who pay Rs 199 shipping charge on http://free-beej-yojana.com.", "WhatsApp Scam", "Scam"),
    ("Government is giving free electricity transformers to every farm tubewell. Fill up form on http://free-transformer-yojana.com with your bank OTP.", "WhatsApp Scam", "Phishing Scam"),
    ("FPO registration fee waived off completely! Pay Rs 499 on http://fpo-india-reg.com to get instant 10 lakh government grant.", "WhatsApp Scam", "Scam"),

    # Hinglish Misleading Forwards
    ("Sabhi kisan bhaiyo ko 90 percent subsidy par naya tractor mil raha hai. Form bharne ke liye link open karein http://kisan-tractor-subsidy.site aakhri tarikh kal hai.", "Hinglish WhatsApp Scam", "Scam"),
    ("PM Kisan ki kist ruk gayi hai toh turant Rs 199 pay karke ekyc karein link http://pmkisan-ekyc-update.info par. 24 ghante me account block ho jayega.", "Hinglish Phishing SMS", "Phishing Scam"),
    ("Kisan loan mukti yojana me 5 lakh tak ka loan maaf ho gaya hai. Apna Aadhar aur bank OTP is link http://kisan-loan-maaf.online par submit karein.", "Hinglish Scam", "Loan Scam")
]

def generate_1000_dataset():
    records = []
    
    # 500 Genuine records
    count = 0
    years = ['2024', '2025', '2026']
    nums = ['15', '16', '17', '18', '19']
    crops = ['Wheat', 'Paddy', 'Cotton', 'Sugarcane', 'Mustard', 'Maize', 'Soybean', 'Pulses']
    states = ['Punjab', 'Haryana', 'Uttar Pradesh', 'Madhya Pradesh', 'Rajasthan', 'Bihar', 'Maharashtra', 'Gujarat', 'Karnataka', 'Telangana']
    
    while count < 500:
        for text_tmpl, source, category in GENUINE_TEMPLATES:
            text = text_tmpl.format(year=years[count % len(years)], num=nums[count % len(nums)])
            if count % 3 == 0:
                text += f" Applicable across {states[count % len(states)]} state agriculture regions for {crops[count % len(crops)]} growers."
            records.append({
                "text": text,
                "label": "genuine",
                "source": source,
                "category": category
            })
            count += 1
            if count >= 500:
                break
                
    # 500 Misleading records
    count = 0
    while count < 500:
        for text_tmpl, source, category in MISLEADING_TEMPLATES:
            text = text_tmpl.format(year=years[count % len(years)], num=nums[count % len(nums)])
            if count % 4 == 0:
                text += f" Urgent notification for all farmers in {states[count % len(states)]} state!"
            records.append({
                "text": text,
                "label": "misleading",
                "source": source,
                "category": category
            })
            count += 1
            if count >= 500:
                break
                
    df = pd.DataFrame(records)
    df.to_csv(CUSTOM_AGRI_PATH, index=False)
    print(f"Successfully generated {len(df)} agri dataset records in {CUSTOM_AGRI_PATH}")

if __name__ == '__main__':
    generate_1000_dataset()
