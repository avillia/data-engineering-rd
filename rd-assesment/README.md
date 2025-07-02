# Фінальний проект
---
## Пояснювальна записка

## 1. `process_sales` pipeline

При трансфері даних в `silver` їх було приведено до правильного вигляду за допомогою:

```python
filter("client_id is not null and purchase_date is not null")
```

Застосувати жодну з методик доповнення даних не можливо через характер пропусків
(рандомізувати id покупця? інтерполювати дату покупки? це немає сенсу), 
тому було вирішено їх просто позбутися - таких записів вже і не така велика кількість,
і вони не особливо вплинуть на повноту картини.

## 2. `process_customers` pipeline

Оскільки таблиця аккумулює дані: 

> кожен наступний день містить дані за всі попередні дні.

то для зменшення надлишковості було вирішено прибрати повтори дедуплікацією
за головним ключем (персональні дані не мають здатності 
особливо сильно оновлюватися протягом дня):

```python
dropDuplicates(["client_id"])
```

## 3. `process_user_profiles` pipeline

Банальне переміщення, адже, за завданням:
> Дані мають ідеальну якість.

## 4. `enrich_user_profiles` pipeline

`MERGE` для мене виявився закрутим (розберуся наступним разом якось із ним), 
тому було вирішено написати через старий добрий JOIN:

```python
    select(
        "c.client_id",
        # надати перевагу customers.silver, якщо не вийде - взяті дані з profiles.silver
        coalesce("c.first_name", "p.first_name").alias("first_name"),  
        coalesce("c.last_name", "p.last_name").alias("last_name"),
        # взяти з customers
        "c.email",
        "c.registration_date",
        coalesce("c.state", "p.state").alias("state"),
        # взяти з profiles.silver
        "p.phone_number",
        "p.age",
    )
```