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
                charCounter.style.color = "#f43f5e"; // Danger color
            } else {
                charCounter.style.color = "var(--text-secondary)";
            }
        };

        textarea.addEventListener("input", updateCounter);
        // Run once on load
        updateCounter();
    }

    // 2. Feedback upvote/downvote mechanism
    const feedbackButtons = document.querySelectorAll(".feedback-btn");
    feedbackButtons.forEach(btn => {
        btn.addEventListener("click", async (e) => {
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
                    // Update button UI
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
                    
                    // Show a quick success alert
                    const statusText = parent.querySelector(".feedback-status") || document.createElement("span");
                    statusText.className = "feedback-status";
                    statusText.style.fontSize = "0.85rem";
                    statusText.style.color = "var(--primary-color)";
                    statusText.style.marginLeft = "1rem";
                    statusText.textContent = "Thank you for your feedback!";
                    
                    if (!parent.querySelector(".feedback-status")) {
                        parent.appendChild(statusText);
                    }
                    
                    // Disable buttons to prevent double clicking
                    allBtns.forEach(b => b.disabled = true);
                } else {
                    console.error("Feedback error:", result.error);
                }
            } catch (err) {
                console.error("Network error saving feedback:", err);
            }
        });
    });
});
