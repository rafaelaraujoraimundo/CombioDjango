// static/js/autocomplete.js

document.addEventListener("DOMContentLoaded", function () {
    function setupAutocomplete(inputElement, suggestionsListElement, data, hiddenFieldId) {
        inputElement.addEventListener("input", function () {
            const query = this.value.toLowerCase();
            suggestionsListElement.innerHTML = "";
            if (query) {
                const filteredData = data.filter(item => 
                    item.display.toLowerCase().includes(query)
                );
                filteredData.forEach(item => {
                    const li = document.createElement("li");
                    li.textContent = item.display;
                    li.classList.add("suggestion-item");
                    li.addEventListener("mousedown", function () {
                        inputElement.value = item.display;
                        document.getElementById(hiddenFieldId).value = item.value;
                        suggestionsListElement.style.display = "none";
                    });
                    suggestionsListElement.appendChild(li);
                });
                suggestionsListElement.style.display = "block";
            } else {
                suggestionsListElement.style.display = "none";
            }
        });

        // Ocultar sugestões ao perder o foco
        inputElement.addEventListener("blur", function () {
            setTimeout(() => { suggestionsListElement.style.display = "none"; }, 100);
        });

        // Mostrar sugestões ao focar, se houver texto
        inputElement.addEventListener("focus", function () {
            if (this.value) {
                suggestionsListElement.style.display = "block";
            }
        });
    }
    // Configuração dos campos com sugestões dinâmicas
    window.initializeAutocomplete = function (fieldData) {
        fieldData.forEach(({ inputId, listId, dataList, hiddenFieldId }) => {
            const inputElement = document.getElementById(inputId);
            const suggestionsListElement = document.getElementById(listId);
            if (inputElement && suggestionsListElement) {
                setupAutocomplete(inputElement, suggestionsListElement, dataList, hiddenFieldId);
            }
        });
    };
});