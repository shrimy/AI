// Zaktualizowanie listy badań po wybraniu lekarza
document.getElementById('doctor').addEventListener('change', function () {
    var doctorId = this.value;  // Pobieramy ID wybranego lekarza

    // Jeśli wybrano lekarza, wyślij zapytanie AJAX
    if (doctorId) {
        fetch(`/appointment/get_examinations/${doctorId}/`)  // Sprawdzamy, czy ta ścieżka jest poprawna
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error: ${response.status}`);
                }
                return response.json();  // Przekształcamy odpowiedź na JSON
            })
            .then(data => {
                var examinationSelect = document.getElementById('examination');
                examinationSelect.innerHTML = '<option value="">--Select Examination--</option>';  // Resetujemy listę

                // Jeśli są dostępne badania, dodaj je do formularza
                if (data.examinations && data.examinations.length > 0) {
                    data.examinations.forEach(function (exam) {
                        var option = document.createElement('option');
                        option.value = exam.id;
                        option.textContent = `${exam.name} - ${exam.description} (Price: ${exam.price} PLN)`;  // Wyświetlamy nazwę i cenę badania
                        examinationSelect.appendChild(option);
                    });
                } else {
                    // Jeśli brak badań, wyświetl komunikat
                    var option = document.createElement('option');
                    option.textContent = 'No examinations available for this doctor';
                    examinationSelect.appendChild(option);
                }
            })
            .catch(error => {
                console.error('Error fetching examinations:', error);
                var examinationSelect = document.getElementById('examination');
                examinationSelect.innerHTML = '<option value="">--Select Examination--</option>';
                var option = document.createElement('option');
                option.textContent = `Error: ${error.message}`;
                examinationSelect.appendChild(option);
            });
    } else {
        // Jeśli nie wybrano lekarza, resetujemy listę badań
        document.getElementById('examination').innerHTML = '<option value="">--Select Examination--</option>';
    }
});