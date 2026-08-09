const TRANSLATIONS = {
    en: {
        "logo": "🌿 AgriFact Check",
        "subtitle": "Check farm-scheme and farming messages before you trust them.",
        "sr-verify": "Verify advisory or scheme",
        "form-title": "Is this message reliable?",
        "form-helper": "Paste a WhatsApp forward, headline, or farming tip.",
        "placeholder": "Paste message here...",
        "submit-btn": "Check message",
        "disclaimer-top": "<strong>Please note:</strong> For important scheme decisions, confirm details on official government portals.",
        "badge-genuine": "Likely Genuine",
        "badge-misleading": "Likely Misleading",
        "confidence-score": "Model confidence: {val}%",
        "exp-genuine": "This message matches patterns of reliable farming advice or official government schemes.",
        "exp-misleading": "This message contains claims or wording patterns frequently found in unverified offers or rumors.",
        "words-influenced": "Words that influenced this result",
        "domain-verified": "Official-portal list: {domain} is recognised",
        "domain-none": "Domain check: No link was found in this message",
        "domain-warning": "Domain check: This site is not in the configured official-portal list (detected: {domain})",
        "final-disclaimer": "This is an automated guide, not an official fact-check or scheme-eligibility decision.",
        "feedback-question": "Was this check helpful?",
        "feedback-yes": "👍 Yes",
        "feedback-no": "👎 No",
        "feedback-thanks": "✓ Thanks for helping check!",
        "history-title": "Recent checks",
        "empty-history": "Your recent checks will appear here.",
        "footer-text": "Designed to help farmers spot fake news, suspicious tips, and fraudulent subsidy offers. Always double check with official government departments before making financial decisions.",
        "char-counter-suffix": "/ 5000 characters",
        "history-meta": "{confidence}% confidence • {date}"
    },
    hi: {
        "logo": "🌿 एग्रीफैक्ट चेक",
        "subtitle": "कृषि योजनाओं और खेती से जुड़े संदेशों पर विश्वास करने से पहले उनकी जांच करें।",
        "sr-verify": "सलाह या योजना की जाँच करें",
        "form-title": "क्या यह संदेश विश्वसनीय है?",
        "form-helper": "व्हाट्सएप फॉरवर्ड, हेडलाइन, या खेती से जुड़े संदेश यहां पेस्ट करें।",
        "placeholder": "संदेश को यहाँ पेस्ट करें...",
        "submit-btn": "संदेश की जांच करें",
        "disclaimer-top": "<strong>कृपया ध्यान दें:</strong> महत्वपूर्ण योजना निर्णयों के लिए, आधिकारिक सरकारी पोर्टलों पर विवरण की पुष्टि करें।",
        "badge-genuine": "विश्वसनीय होने की संभावना",
        "badge-misleading": "गुमराह करने वाला होने की संभावना",
        "confidence-score": "मॉडल का विश्वास: {val}%",
        "exp-genuine": "यह संदेश विश्वसनीय खेती की सलाह या आधिकारिक सरकारी योजनाओं के पैटर्न से मेल खाता है।",
        "exp-misleading": "इस संदेश में ऐसे दावे या शब्द पैटर्न हैं जो अक्सर असत्यापित ऑफ़र या अफवाहों में पाए जाते हैं।",
        "words-influenced": "वे शब्द जिन्होंने इस परिणाम को प्रभावित किया",
        "domain-verified": "आधिकारिक पोर्टल सूची: {domain} मान्यता प्राप्त है",
        "domain-none": "डोमेन जांच: इस संदेश में कोई लिंक नहीं मिला",
        "domain-warning": "डोमेन जांच: यह साइट आधिकारिक पोर्टल सूची में नहीं है (पाया गया: {domain})",
        "final-disclaimer": "यह एक स्वचालित मार्गदर्शिका है, कोई आधिकारिक तथ्य-जांच या योजना-पात्रता निर्णय नहीं।",
        "feedback-question": "क्या यह जांच मददगार थी?",
        "feedback-yes": "👍 हाँ",
        "feedback-no": "👎 नहीं",
        "feedback-thanks": "✓ जांच में मदद करने के लिए धन्यवाद!",
        "history-title": "हाल ही की जांच",
        "empty-history": "आपकी हाल ही की जांच यहां दिखाई देगी।",
        "footer-text": "किसानों को फर्जी खबरों, संदिग्ध सुझावों और धोखाधड़ी वाले सब्सिडी प्रस्तावों को पहचानने में मदद करने के लिए डिज़ाइन किया गया है। वित्तीय निर्णय लेने से पहले हमेशा आधिकारिक सरकारी विभागों से दोबारा जांच करें।",
        "char-counter-suffix": "/ 5000 अक्षर",
        "history-meta": "{confidence}% विश्वास • {date}"
    }
};

document.addEventListener("DOMContentLoaded", () => {
    // 1. Textarea character counter
    const textarea = document.getElementById("text-input");
    const charCounter = document.getElementById("char-counter-val");
    const maxChars = 5000;

    if (textarea && charCounter) {
        const updateCounter = () => {
            const len = textarea.value.length;
            charCounter.textContent = len;
            if (len > maxChars) {
                charCounter.style.color = "var(--misleading-text)";
                charCounter.style.fontWeight = "bold";
            } else {
                charCounter.style.color = "var(--text-secondary)";
                charCounter.style.fontWeight = "normal";
            }
        };

        textarea.addEventListener("input", updateCounter);
        // Run once on load to update counter with prefilled text (if any)
        updateCounter();
    }

    // 2. Feedback upvote/downvote AJAX mechanism
    const feedbackButtons = document.querySelectorAll(".feedback-btn");
    feedbackButtons.forEach(btn => {
        btn.addEventListener("click", async () => {
            const checkId = btn.dataset.checkId;
            const vote = btn.dataset.vote; // 'upvote' or 'downvote'
            
            if (!checkId || !vote) return;
            
            try {
                const response = await fetch(`/feedback/${checkId}`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ vote: vote })
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    // Update button active classes
                    const parent = btn.parentElement;
                    const allBtns = parent.querySelectorAll(".feedback-btn");
                    
                    allBtns.forEach(b => {
                        b.classList.remove("active-up", "active-down");
                    });
                    
                    if (vote === "upvote") {
                        btn.classList.add("active-up");
                    } else {
                        btn.classList.add("active-down");
                    }
                    
                    // Show a farmer-friendly success status message in current language
                    const container = btn.closest(".feedback-container");
                    let statusText = container.querySelector(".feedback-status");
                    if (!statusText) {
                        statusText = document.createElement("span");
                        statusText.className = "feedback-status";
                        container.appendChild(statusText);
                    }
                    const currentLang = localStorage.getItem("preferred_language") || "en";
                    statusText.textContent = TRANSLATIONS[currentLang]["feedback-thanks"];
                    
                    // Disable feedback buttons to prevent multiple clicks
                    allBtns.forEach(b => b.disabled = true);
                } else {
                    console.error("Feedback error:", result.error);
                }
            } catch (err) {
                console.error("Network error saving feedback:", err);
            }
        });
    });

    // 3. Language Selector Setup
    const updateActiveLanguageButton = (lang) => {
        const buttons = document.querySelectorAll(".lang-toggle-btn");
        buttons.forEach(btn => {
            if (btn.getAttribute("data-lang") === lang) {
                btn.classList.add("active");
            } else {
                btn.classList.remove("active");
            }
        });
    };

    const setLanguage = (lang) => {
        localStorage.setItem("preferred_language", lang);
        updateActiveLanguageButton(lang);

        // Update elements with data-i18n
        const i18nElements = document.querySelectorAll("[data-i18n]");
        i18nElements.forEach(el => {
            const key = el.getAttribute("data-i18n");
            if (TRANSLATIONS[lang] && TRANSLATIONS[lang][key]) {
                if (key === 'domain-verified' || key === 'domain-warning' || key === 'disclaimer-top' || key === 'logo') {
                    let text = TRANSLATIONS[lang][key];
                    if (el.dataset.domain) {
                        text = text.replace('{domain}', el.dataset.domain);
                    }
                    el.innerHTML = text;
                } else if (key === 'confidence-score') {
                    const conf = el.dataset.confidence;
                    el.textContent = TRANSLATIONS[lang][key].replace('{val}', conf);
                } else {
                    el.textContent = TRANSLATIONS[lang][key];
                }
            }
        });

        // Update placeholders
        const placeholders = document.querySelectorAll("[data-i18n-placeholder]");
        placeholders.forEach(el => {
            const key = el.getAttribute("data-i18n-placeholder");
            if (TRANSLATIONS[lang] && TRANSLATIONS[lang][key]) {
                el.setAttribute("placeholder", TRANSLATIONS[lang][key]);
            }
        });

        // Update badges (history)
        const badges = document.querySelectorAll("[data-i18n-badge]");
        badges.forEach(el => {
            const val = el.getAttribute("data-i18n-badge");
            if (val === 'genuine') {
                el.textContent = lang === 'hi' ? '🛡️ असली' : '🛡️ Genuine';
            } else {
                el.textContent = lang === 'hi' ? '⚠️ गुमराह करने वाला' : '⚠️ Misleading';
            }
        });

        // Update history meta
        const metas = document.querySelectorAll("[data-i18n-meta]");
        metas.forEach(el => {
            const conf = el.getAttribute("data-confidence");
            const date = el.getAttribute("data-date");
            let text = TRANSLATIONS[lang]["history-meta"];
            text = text.replace("{confidence}", conf).replace("{date}", date);
            el.textContent = text;
        });
    };

    // Attach toggle listeners
    const buttons = document.querySelectorAll(".lang-toggle-btn");
    buttons.forEach(btn => {
        btn.addEventListener("click", () => {
            const lang = btn.getAttribute("data-lang");
            setLanguage(lang);
        });
    });

    // Load preferred or default language on load
    const preferred = localStorage.getItem("preferred_language") || "en";
    setLanguage(preferred);
});
