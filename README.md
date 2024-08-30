Инструкция по установке:

1) Скачиваем проект git clone git@github.com:ilya163/vacancy_hh.git
2) Переходим на vacancy_hh
3) Добавляем файл доступа .env
4) Добавляем файл авторизации Google Sheets для сервиса service_account.json 
   https://developers.google.com/sheets/api/quickstart/python?hl=ru - инструкция. При создании Credentials нужно выбрать Service Account. Использую этот вариант, потому что пользовательская авторизация требует подтвержение в оконном браузере: в docker контейнере это сделать сложнее.
5) Запускаем docker compose up. Первый раз не запускается, потому что создаются volumes без доступа. Выполняем <sudo chmod -R 777 volumes/> и снова запускаем compose.

Ознакомитсья с итогом по видео: https://drive.google.com/file/d/1jvIHHVmswcLc-P9cxfPQ005OSvSdlXHt/view?usp=sharing
