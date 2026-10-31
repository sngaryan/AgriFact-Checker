# Sample Flyer Datasets for Evaluation & OCR Testing

This directory contains real-world agricultural poster and flyer samples categorized into **deceptive/fake flyers** and **official government scheme infographics** for testing the Multimodal Image Text Extractor (OCR) and verifying claims.

---

### 🚨 Fake / Scam Flyers (Expected: Likely Misleading)

1. **`fake_flyer_1_upi_scam.jpg`**
   - **Context:** Fraudulent poster misusing the Ministry of Agriculture emblem, promising ₹2,00,000 annually and instructing farmers to send advance deposit money to a personal UPI number.
   - **Key Detection Signal:** Private mobile number / unauthorized UPI payment request.
   - **Expected Verdict:** **Likely Misleading** with private mobile/UPI scam warning.

2. **`fake_flyer_2_canada_visa_scam.jpg`**
   - **Context:** Deceptive overseas farm work mass recruitment advertisement demanding a steep processing fee (JMD $60,000) via card at a seafood restaurant venue.
   - **Key Detection Signal:** Advance processing fee, unofficial recruitment agency, non-governmental scheme.
   - **Expected Verdict:** **Likely Misleading / Commercial Promo**.

---

### 🛡️ Official Government Flyers (Expected: Likely Genuine)

3. **`official_flyer_1_kcc_subsidy.jpg`**
   - **Context:** Authentic announcement poster from the Ministry of Agriculture & Farmers Welfare detailing ₹11,593.96 Crore credit subsidy disbursed under the Modified Interest Subvention Scheme (MISS) through Kisan Credit Card (KCC).
   - **Key Detection Signal:** Official ministry emblems, verified scheme references (KCC, MISS, RuPay).
   - **Expected Verdict:** **Likely Genuine** with Kisan Credit Card scheme matching.

4. **`official_flyer_2_natural_farming.jpg`**
   - **Context:** Official Hindi infographic for the National Natural Farming Mission (राष्ट्रीय प्राकृतिक खेती मिशन) announcing ₹4,000 per acre financial assistance for 2 years.
   - **Key Detection Signal:** Verified national mission terminology, Ministry emblem, authentic extension advice.
   - **Expected Verdict:** **Likely Genuine** with bilingual Devanagari Hindi OCR text extraction.

---

### How to Test in the Web Application:
1. Open **`http://127.0.0.1:5000`**.
2. Click **📁 Choose Flyer Image** and select any of the 4 flyers above.
3. Click **Check message**.
4. The system automatically performs bilingual OCR (Hindi + English), extracts the claim, and classifies it.
