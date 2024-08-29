document.getElementById('exportButton').addEventListener('click', function() {
    const buttonActive = document.getElementById('exportButton').getAttribute('data-active')
    if (buttonActive == '0') {
        console.log("Данных нет")
        return;
    }

    let progressBar = document.getElementById('progress-bar');
    let notification = document.getElementById('notification');
    let width = 0;
    let interval;


    progressBar.classList.remove('hidden');

    // Начать прогресс-бар
    fetch("/time_processing_sheets", {"method": "POST"})
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.text();
      })
      .then(progress_time => {
        const duration = parseInt(progress_time, 10); // Время в секундах
        const interval_time = (duration * 1000 * 1.15) / 100; // Миллисекунды для 1% прогресса

        interval = setInterval(function() {
            if (width >= 100) {
                clearInterval(interval);
            } else {
                width += 1; // Увеличение ширины на 1% каждую интервал времени
                progressBar.style.width = width + '%'; // Обновляем ширину прогресс-бара
                progressBar.textContent = width + '%'; // Обновляем текст внутри прогресс-бара
            }
        }, interval_time); // Интервал обновления в миллисекундах

        // Запускаем запись в Google Sheets
        return fetch("/google_sheets", {"method": "POST"});
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
      })
      .then(data => {
        if (data.status === 'success') {
          notification.textContent = data.msg;
          notification.className = 'notification success'; // Устанавливаем класс для успешного сообщения
        } else if (data.status === 'error') {
          notification.textContent = data.msg;
          notification.className = 'notification error'; // Устанавливаем класс для сообщения об ошибке
        }


        notification.classList.remove('hidden'); // Показываем оповещение

        // Останавливаем прогресс-бар после завершения записи
        clearInterval(interval);
        progressBar.style.width = '100%';
        progressBar.textContent = '100%';

        // Скрываем оповещение через 3 секунды
        setTimeout(() => {
            notification.classList.add('hidden'); // Скрываем оповещение после показа
        }, 5000);
      })
      .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);

        notification.textContent = 'Произошла ошибка при выполнении запроса.';
        notification.className = 'notification error';
        notification.classList.remove('hidden');

        // Останавливаем прогресс-бар при ошибке
        clearInterval(interval);
        progressBar.style.width = '0%';
        progressBar.textContent = '0%';
      });
});
