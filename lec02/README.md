# Як запустити?

## Через Docker (рекомендовано):

Для цього проєкту сконфігурований `docker-compose.yaml` файл 
разом з окремими `Dockerfile`-ами для автотестів та для самих 
застосунків (`job1` та `job2`). Достатньо просто запустити:

```shell
docker compose up job_runner
```

Це по ідеї має створити образ контейнера, на якому паралельно 
запустяться обидва застосунки, та відкрити порти `8081` і `8082` 
для доступу з-під `localhost`. Готово! Насолоджуйтеся!

## Зібрати середовище самостійно:

1. [Створити окреме віртуальне середовище в Python](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/).
2. Встановити для нього залежності: 
```shell
python -m pip install -r requirements.txt
```
3. Запустити в різних вікнах терміналу різні job-и:
```shell
python extractor_job.py
```
```shell
python loader_job.py
```