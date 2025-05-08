document.addEventListener("DOMContentLoaded", function () {
    const searchInputs = document.querySelectorAll(".search-input");

    searchInputs.forEach(input => {
        input.addEventListener("input", function () {
            const type = this.dataset.type;
            const query = this.value;
            const resultsDiv = this.closest(".search-container").querySelector(".search-results");

            // Clear previous results
            resultsDiv.innerHTML = "";

            if (query.length < 1) return;

            // Fetch suggestions from backend
            fetch(`/ajax/get-templates/?q=${encodeURIComponent(query)}&type=${encodeURIComponent(type)}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error("Network response was not ok");
                    }
                    return response.json();
                })
                .then(data => {
                    data.results.forEach(item => {
                        const div = document.createElement("div");
                        div.className = "result-item";
                        div.textContent = item;
                        div.addEventListener("click", () => {
                            this.value = item;
                            resultsDiv.innerHTML = "";
                        });
                        resultsDiv.appendChild(div);
                    });
                })
                .catch(error => {
                    console.error("Search failed:", error);
                });
        });
    });
});
