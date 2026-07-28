# UI automation "the-internet" ресурса

Набор тестов на Playwright + Pytest, покрывающий три сценария 
из тестового задания /docs/test-task.md

## Требования

- Python 3.13
- Поддерживаемый браузер, устанавливаемый через Playwright (см. ниже)

## Установка

```bash
python -m venv .venv
source .venv/bin/activate        
pip install -r requirements.txt
playwright install chromium      # or: playwright install
```

## Запуск тестов

```bash
pytest                           # full suite, headless Chromium
pytest --headed --slowmo 300     # watch it run
pytest -m smoke                  # happy paths / fast feedback
pytest -m negative               # invalid credentials / error paths
pytest -m "smoke and critical"   # must-pass subset of smoke
pytest -m security               # cookies, protected routes, injection
pytest -m "login and auth"       # login / session scenarios
pytest --browser firefox         # or webkit
pytest -n auto                   # parallel (needs pytest-xdist)
```

Маркеры объявлены в `pytest.ini` (`--strict-markers`: неизвестный маркер = ошибка)

### Allure-отчёт (critical)

Прогон только must-pass тестов с записью результатов Allure:

```bash
pytest -m critical --alluredir=allure-results
```

HTML-отчёт (нужен [Allure Commandline](https://allurereport.org/docs/install/)):

```bash
allure serve allure-results              # сгенерировать и открыть в браузере
# или:
allure generate allure-results -o allure-report --clean
allure open allure-report
```

У тестов с `@pytest.mark.critical` в отчёте severity = CRITICAL. При падении
прикладывается скриншот страницы. Каталоги `allure-results/` и `allure-report/`
в `.gitignore`.

В CI HTML-отчёт собирается автоматически (`allure generate`) и кладётся в
артефакт `allure-report-<browser>`. Cкачать и открыть `index.html` в браузере

### Ручная отладка

По умолчанию браузер запускается в headless режиме. Чтобы смотреть прогон
визуально, раскомментируй в `pytest.ini` строки `--headed` и `--slowmo 500`, тогда
откроется окно Chromium с паузой 500 мс между действиями. В CI эти флаги не используются!!!

Скриншоты, видео и трейсы упавших тестов сохраняются в `artifacts/`.
Открыть трейс можно так:

```bash
playwright show-trace artifacts/<test-name>/trace.zip
```

## Указание другого окружения

Базовый URL нигде не захардкожен в тестах. Приоритет, от высшего к низшему:

```bash
pytest --base-url https://staging.example.com   # 1. CLI option
BASE_URL=https://staging.example.com pytest      # 2. environment variable
                                                 # 3. default, see config.py
```

Учётные данные настраиваются аналогично:

```bash
APP_USERNAME=someone APP_PASSWORD=secret pytest
```

В `.gitignore` игнорируется только `.env`. Паттерны вроде `.env.local` /
`.env.*.local` намеренно не добавлены: в рамках тестового задания используются
публичные демо креды (`tomsmith` / `SuperSecretPassword!`), отдельных секретов
для локальной разработки нет

## Структура проекта

```
config.py                  конфигурация окружения (URL, учётные данные)
conftest.py                фикстуры: base_url, credentials, page objects
pages/
  base_page.py             общие хелперы навигации для всех страниц
  main_page.py             главная страница
  login_page.py            форма аутентификации
  secure_page.py           защищённая область после входа
tests/
  test_main_page.py        сценарий 1
  test_login_negative.py   сценарий 2
  test_login_flow.py       сценарий 3
.github/workflows/tests.yml  CI: lint (ruff) + Playwright + Allure HTML
```

PageObjects содержат локаторы и действия, но не содержат assert'ов — упавший
тест всегда указывает на требование, а не на вспомогательный код. Проверки
используют `expect` из Playwright с ретраями, фиксированных пауз в наборе нет.

## Покрытие

**Сценарий 1 — главная страница.** URL совпадает с base URL, заголовок документа,
лента «Fork me on GitHub» видима и ведёт на репозиторий. В каталоге 44 ссылки,
среди них «Form Authentication» ->`/login`, всего 46 `<a>` на странице, у пунктов
каталога непустые уникальные подписи и непустые `href`

**Сценарий 2 — страница входа.** Переход с главной по «Form Authentication» с
проверкой структуры формы (heading, кнопка Login, `password` type=`password`);
параметризованный прогон неверных учёток (unknown/wrong/empty/case/spaces/
injection). Каждый кейс: flash с классом `error`, остаёмся на `/login`, форма на
месте. Два strict-кейса дополнительно проверяют exact-текст flash и очистку полей.
Отдельно: после failed login `/secure` недоступен, прямой заход без сессии
редиректит на login.

**Сценарий 3 — вход и выход.** Успешный вход -> `/secure` с flash `success` (exact
текст), title/heading/content, Logout (`href=/logout`, enabled); в контексте есть
HttpOnly `rack.session`. Выход -> `/login` с exact flash logout и сменой значения
сессионной cookie; `/secure` после logout недоступен; повторный login снова
открывает secure area.

## !!! Замечания по ТЗ !!!

Три пункта в описании задания не совпадают с приложением. Все зафиксированы в
коде и здесь, а не замалчиваются:

1. **Маршрут защищённой страницы.** В задании указано «assert user is on the /security
   page»; приложение отдаёт страницу по `/secure`. Проверено вручную через
   Playwright: после успешного входа URL — `https://the-internet.herokuapp.com/secure`.
   Тесты проверяют реальный маршрут.
2. **Количество ссылок.** В задании ожидается 44 ссылки. Пересчётом подтверждено:
   селектор `#content ul li a` даёт ровно 44. Подсчёт всех `<a>` на странице
   дал бы 46 за счёт риббона (ленты) `GitHub` и ссылки в футере. Константа
   `EXPECTED_EXAMPLE_LINKS` проверяет каталог. Отдельный тест фиксирует разницу
   через `footer_links` и общий счётчик ссылок.
3. **Элемент Logout.** В задании — «Assert page has "Logout" button». На странице
   это `<a href="/logout">`, стилизованный под кнопку (проверено через
   Playwright). Локатор — `get_by_role("link", name="Logout")`: семантика роли
   важнее тега.

## Наблюдение по безопасности

Приложение различает сообщения об ошибке в зависимости от того, существует ли
логин:

- неизвестный логин (даже с правильным паролем) -> `Your username is invalid!`
- известный логин с неверным паролем -> `Your password is invalid!`

Это **username enumeration**: по тексту ответа можно перебором выяснить,
какие логины зарегистрированы, не зная ни одного пароля. В продакшене обычно
отвечают единым сообщением вида «Invalid username or password». Тесты фиксируют
текущее поведение приложения, а не одобряют его как безопасное.

## CI

`.github/workflows/tests.yml` при push / pull request в `master` и вручную
(**Run workflow**):

1. **lint** — `ruff check .` (статический анализ, отдельный job)
2. **playwright** — matrix Chromium / Firefox: `pytest -n auto`, запись
   Allure results, генерация HTML (`allure generate`), upload артефактов
   (`artifacts/` при fail, `allure-results-*`, `allure-report-*`)

Ручной запуск принимает опциональный `base_url`.




## Применяемые агенты и роли

- **Composer 2.5** — правки по линтерам и докстрингам
- **Fable 5, Opus 4.8 (Anthropic)** — план, рефакторинг структуры, архитектурные советы
- **Cursor Grok 4.5** — кодинг: тесты, page objects, Allure, CI, маркеры
- **Кирилл** — структура проекта, плагины, настройка IDE, выбор агентов;
  постановка задач и пошаговая приёмка; сверка с ТЗ; решения по scope
  (маркеры, CI, Allure, параметризация); локальный прогон тестов и просмотр
  отчётов; финальное ревью кода и README

Инструменты рядом с агентами:

- **Playwright MCP** — проверка реального поведения приложения (URL `/secure`, лента GitHub, flash, Logout как link), а не «по памяти»
- **Context7** — сверка API библиотек (Playwright, Allure) с версиями из `requirements.txt`
- **Cursor rules** (`.cursor/rules/`) — договорённости по архитектуре POM, ожиданиям и git-потоку
