# NSTU API

## Получение ID и hash студента

```bash
curl -H "Http-Api-Key: s13dfget456DADHGWEv34g435f" \
     -H "Content-Type: application/json" \
     "https://api.ciu.nstu.ru/v1.0/tgbot/check_stud_phone?phone_number=%STUDENT_PHONE%"

```

## Получение основной информации о студенте

```bash
curl -H "Http-Api-Key: s13dfget456DADHGWEv34g435f" \
     -H "Content-Type: application/json" \
     "https://api.ciu.nstu.ru/v1.0/tgbot/stud_status?id=%STUDENT_ID%&hash=%STUDENT_HASH%"

```
