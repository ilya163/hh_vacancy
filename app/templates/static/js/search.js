// Поиск вакансий
document.getElementById('searchButton').addEventListener('click', function() {
    const area = parseInt(document.getElementById('filterInput').getAttribute('data-id')) || 113;
    const professional_role = 11;
    const url = `/vacancies?area=${area}`;

    fetch(url)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
      })
      .then(data => {

        const vacancies = data.vacancies
        const resultTable = document.querySelector("#resultsTable tbody"); // Выбираем tbody для добавления строк

        // Очищаем таблицу перед добавлением новых данных
        resultTable.innerHTML = '';

        if (vacancies.length === 0) {
            // Если нет данных, добавляем строку с сообщением
            const noDataRow = document.createElement('tr');
            noDataRow.innerHTML = '<td colspan="5" id="no-data">Нет данных</td>'; // Подгоните количество colspan под вашу таблицу
            resultTable.appendChild(noDataRow);

            document.getElementById('exportButton').setAttribute('data-active','0')
        } else {
            vacancies.forEach(vacancy => {
                const row = document.createElement('tr');

                row.innerHTML = `
                    <td>${vacancy.title}</td>
                    <td><a href="${vacancy.link}" target="_blank">${vacancy.link}</a></td>
                    <td>${vacancy.area}</td>
                    <td>${vacancy.professional_role}</td>
                    <td>${vacancy.salary_min || 0} - ${vacancy.salary_max ? vacancy.salary_max : 'По договоренности'}</td>
                    `;

                resultTable.appendChild(row);
            });
            document.getElementById('exportButton').setAttribute('data-active','1')
        }
      })
      .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
    });
});


