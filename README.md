Инструкция по запуску
```
git clone https://github.com/xddprog/TestWork098.git
cd TestWork098
```
После этого нужно установить переменные окружения внутри папки backend в файле .env (в файле .env.example приведен пример переменных)
Запуск с помощью Docker'а
```
docker-compose up -d --build
```

Sqagger будет доступен по http://localhost:8000/docs
