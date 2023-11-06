<script>
    // JavaScript for making the prediction request and updating the page
    const predictButton = document.getElementById('predictButton');
    const predictionResult = document.getElementById('predictionResult');
    const mlForm = document.getElementById('mlForm');

    predictButton.addEventListener('click', () => {
        const gender = document.getElementById('gender').value;
        const age = document.getElementById('age').value;
        const annualIncome = document.getElementById('annualIncome').value;

        const data = {
            "gender": gender,
            "age": age,
            "annualIncome": annualIncome
        };

        fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                predictionResult.innerHTML = `<p class="error">${data.error}</p>`;
            } else {
                predictionResult.innerHTML = `<p>Prediction: ${data.prediction === 1 ? 'Purchased' : 'Not Purchased'}</p>`;
            }
        })
        .catch(error => {
            predictionResult.innerHTML = `<p class="error">An error occurred: ${error.message}</p>`;
        });
    });
</script>
