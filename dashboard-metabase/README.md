# Metabase dashboard

> Metabase платформа для реализации BI  

## Развертывание  

После развертывания основного репозитория 

1. Создать папку metabase и добавить туда [metabase.jar](https://www.metabase.com/start/oss/jar)  

```bash  
cd metabase  
```  

2. Установка metabase  
```bash  
java --add-opens java.base/java.nio=ALL-UNNAMED -jar metabase.jar  
```  

3. Загрузить плагин для поддержки ClickHouse [clickhouse.metabase-driver.jar](https://github.com/clickhouse/metabase-clickhouse-driver/releases/tag/1.51.0)  
Положить файл clickhouse.metabase-driver.jar в папку plugins внутри папки metabase  

4. Запустить сервер  
```bash  
java -jar metabase.jar  
```
5. Зайти на http://localhost:3000/ и зарегистрировать пользователя  

## Требования  
- Java Runtime Environment (JRE) (11,17,21+)  

## Тестирование  
1. Запуск сервера  

```bash  
java -jar metabase.jar  
```  

2. Зайти на http://localhost:3000/ и ввести свой логин и пароль  

3. Открыть 

## Пример
Пример dashboard:
![](https://github.com/Anzovi/ITMO_DE/blob/main/imgs/MetabaseBI_example.png)