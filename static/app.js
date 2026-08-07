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
                    
                    // Show a farmer-friendly success status message
                    const container = btn.closest(".feedback-container");
                    let statusText = container.querySelector(".feedback-status");
                    if (!statusText) {
                        statusText = document.createElement("span");
                        statusText.className = "feedback-status";
                        container.appendChild(statusText);
                    }
                    statusText.textContent = "✓ Thanks for helping check!";
                    
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
});
