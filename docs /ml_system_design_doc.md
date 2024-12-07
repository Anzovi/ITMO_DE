# ML System Design Doc - [RU]
## Дизайн ML системы - Система анализа эксплуатации оборудования с выявлением отклонений    

> ## Термины и пояснения  
> - Итерация - это все работы, которые совершаются до старта очередного пилота  
> - БТ - бизнес-требования 
> - EDA - Exploratory Data Analysis - исследовательский анализ данных  
> - `Data Scientist` - `Data Scientist` совмещает в себе компетенции классического `Data Scientist` с упором на исследования и `ML Engineer` & `ML Ops` роли с акцентом на продуктивизацию моделей.  
> - `Product Owner` - зказчик  
> - ТО - техническое обслуживание оборудования  
> - Предиктивное ТО - Предиктивное техническое обслуживание - комплексный подход, позволяющий определить состояние находящегося в эксплуатации оборудования и оценить, когда следует провести техническое обслуживание.  
> - ML -  Машинное обучение
> - ВР - временной ряд, в контексте данной задачи сигнал снятый с сенсора.

### 1. Цели и предпосылки 
#### 1.1. Зачем идем в разработку продукта?  

- Бизнес-цель: заключается в автоматизации процесса диагностики состояния машин и оборудования производителя круп «Увелка» в онлайн-режиме с целью выявления отклонений от номинальных режимов работы и своевременного уведомления о необходимости проведения технического обслуживания оборудования.  
- Почему станет лучше, чем сейчас, от использования ML: может помочь в более точном прогнозировании состояния оборудования, выявлении скрытых закономерностей в данных, автоматизации анализа больших объемов информации, а также в улучшении точности и скорости диагностики, что в свою очередь может снизить количество непредвиденных поломок и оптимизировать график обслуживания.  
- Что будем считать успехом итерации с точки зрения бизнеса: получение MVP системы по аналитике состояния оборудования и уведомлению об отклонениях и необходимости проведения технического обслуживания.  

#### 1.2. Бизнес-требования и ограничения  

- Краткое описание БТ и ссылки на детальные документы с бизнес-требованиями:  
  1. Модель должна, на основе собранных данных с сенсоров оборудования за определенный период времени, оповещать о необходимости проведения технического обслуживания.  
  2. Наличие самостоятельного хостинга или развертывание проекта на локальной машине.  
- Бизнес-ограничения: на данной итерации конкретные ограничения от `Product Owner` ещё не сформированы.  
- Что мы ожидаем от конкретной итерации: создание инфраструктуры для сбора данных с сенсоров, установленных на оборудовании.  
- Описание бизнес-процесса пилота: модель будет оповещать инженеров о необходимости проведения технического обслуживания.  
- Что считаем успешным пилотом? Критерии успеха и возможные пути развития проекта: предиктивное ТО успешно справляется с составлением графика проведения технических работ. Следовательно, решается задача оптимизации: соблюдается баланс между
 слишком частыми ТО (на время ТО оборудование простаивает) и не доведением оборудования до поломоки.  

#### 1.3. Что входит в скоуп проекта/итерации, что не входит   

- На закрытие каких БТ подписываемся в данной итерации: по небольшим выгрузкам данных с сенсоров провести анализ (EDA).
- Что не будет закрыто: на данной итерации не будет собрана модель предиктивного ТО, тк не достаточно данных для его реализации.
- Описание результата с точки зрения качества кода и воспроизводимости решения: на данный момент был произведен анализ по выгрузкам: в ветке main в папке /DA/Data_ForeCasting/ - тестирование различных методов прогнозирования временных рядов,
/DA/Data_fillna/ - тестирование различных способов заполнения пропусков в даенных, /DA/EDA - разведочный анализ.  
- Описание планируемого технического долга (что оставляем для дальнейшей продуктивизации): модель, которая на основе собранных за определенный период данных делает прогноз о дате проведения ТО.

#### 1.4. Предпосылки решения  

- Описание всех общих предпосылок решения, используемых в системе – с обоснованием от запроса бизнеса: какие блоки данных используем, горизонт прогноза, гранулярность модели, и др. `Data Scientist`:  
 1. Блоки данных  
    - Данные о состоянии оборудования  
       - Датчики и показания: Данные, собранные с помощью сенсоров (температура, давление, вибрация и т.д.), играют ключевую роль в оценке технического состояния оборудования.  
       - История неполадок: Записи о предыдущих авариях, ремонтах и осмотрах, которые могут помочь в выявлении паттернов и трендов.  
    - Оперативные данные  
       - Рабочие условия: Информация о нагрузке на оборудование, циклах работы и прерываниях будет способствовать более точному прогнозированию состояний.    
2. Горизонт прогноза (пока что не определен, так как пока нет данных необходимых для определения временных периодов)  
    - Краткосрочный прогноз (1 час - Сутки; пока что примерно): Используется для обнуружения неисправностей в оборудовании (anomaly detection).
    - Среднесрочный прогноз (1-3 месяца; пока что примерно): Используется для прогнозирования ТО (change point detection - обноружение изменений в временном ряде).
3. Гранулярность модели
    - Уровень агрегирования: Данные могут агрегироваться на уровне отдельного оборудования или группы оборудования, какой вариант лучше будет выясняться дальше через тестирование и консультацию с инженерами.
    - Частота обновления данных: Модель может использовать данные в реальном времени или обновляться на основе заданного графика (например, ежедневно, еженедельно).
4. Обоснование от запроса бизнеса
    - Уменьшение простоев: Бизнес-потребность в минимизации времени простоя оборудования требует точных прогнозов о его состоянии и возможных сбоях.
    - Оптимизация затрат: Понимание, когда и какое оборудование потребует обслуживания, помогает минимизировать неплановые ремонты и оптимизировать запасы запчастей.
    - Повышение надежности: Системы предиктивного ТО должны быть интегрированы в общую стратегию повышения надежности и долговечности оборудования.
    - Устойчивость к изменениям: Способность адаптироваться к изменениям в производственных условиях или в самом оборудовании требует гибкой модели, способной учитывать новые данные.

### 2. Методология `Data Scientist`     

#### 2.1. Постановка задачи  

- Что делаем с технической точки зрения: поиск аномалий (anomaly detection) и поиск точек изменения состояния (change point detection). Со временем оборудование изнашивается, что проявляется в частичных отхождениях от эталонных значений (anomaly detection: point-based и subequence-based) так и в изменении распределения сигнала (change point detection). Пока что нет достаточного количества данных, чтобы сделать вывод какая детекция даст более хороший результат в модели предиктивного ТО.

#### 2.2. Блок-схема решения    
- [Блок схема](https://github.com/Anzovi/Fault-Detection/blob/homework_1/docs/Uvelka_Plan.png) 