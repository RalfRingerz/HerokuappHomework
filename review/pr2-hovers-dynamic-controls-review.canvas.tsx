import {
  Callout,
  Card,
  CardBody,
  CardHeader,
  Divider,
  Grid,
  H1,
  H2,
  H3,
  Pill,
  Row,
  Stack,
  Stat,
  Table,
  Text,
} from "cursor/canvas";

export default function Pr2ReviewCanvas() {
  return (
    <Stack gap={24}>
      <Stack gap={8}>
        <H1>PR #2 — ревью Hovers и Dynamic Controls</H1>
        <Text tone="secondary">
          vapavlenko → RalfRingerz/HerokuappHomework master · HEAD
          1a0f81f · CI: lint + chromium + firefox green
        </Text>
        <Row gap={8} wrap>
          <Pill tone="success" active>
            Задание выполнено
          </Pill>
          <Pill tone="success">PR в master</Pill>
          <Pill tone="success">CI green</Pill>
          <Pill tone="warning">Approve with comments</Pill>
        </Row>
      </Stack>

      <Grid columns={4} gap={12}>
        <Stat value="Да" label="Наследование BasePage" tone="success" />
        <Stat value="6 / 6" label="Тест-функций на страницу" tone="success" />
        <Stat value="10 + 8" label="Собранных тестов Hovers / DC" />
        <Stat value="3 / 3" label="CI jobs на HEAD" tone="success" />
      </Grid>

      <Callout tone="success" title="Вердикт">
        Формальные требования закрыты: Page Object от BasePage, фикстуры в
        том же стиле, по тест-кейсу на страницу, ≥5 тестов, PR в master со
        всем кодом. Блокирующих дефектов нет. Ниже — замечания по конвенциям
        репозитория и пробелам покрытия.
      </Callout>

      <H2>Чеклист задания</H2>
      <Table
        headers={["Требование", "Статус", "Где видно"]}
        columnAlign={["left", "left", "left"]}
        rowTone={["success", "success", "success", "success", "success", "success"]}
        rows={[
          [
            "Изучить фреймворк (POM, fixtures, expect)",
            "Сделано",
            "pages/*, tests/*, conftest.py",
          ],
          [
            "Наследоваться от BasePage",
            "Сделано",
            "HoversPage, DynamicControlsPage",
          ],
          [
            "1 тест-кейс на страницу",
            "Сделано",
            "docs/test-task.md Scenario 4 и 5",
          ],
          [
            "≥5 тестов на страницу",
            "Сделано",
            "6 функций / 10 и 8 collected",
          ],
          [
            "PR со всеми изменениями в master",
            "Сделано",
            "github.com/.../pull/2, mergeable",
          ],
          [
            "Линтер после первого комментария",
            "Исправлено",
            "commit style: fix linting issues",
          ],
        ]}
      />

      <H2>Что сделано хорошо</H2>
      <Grid columns={2} gap={12}>
        <Card>
          <CardHeader>Архитектура как в master</CardHeader>
          <CardBody>
            <Text>
              path + open(), фикстуры уже открывают страницу, assert только в
              тестах, parametrize с id, expect() для UI, без sleep.
            </Text>
          </CardBody>
        </Card>
        <Card>
          <CardHeader>Сильные проверки</CardHeader>
          <CardBody>
            <Text>
              Hovers: hidden до hover, только активная карточка, unhover.
              Dynamic Controls: лоадер, disabled кнопки, сохранение текста в
              input после Disable.
            </Text>
          </CardBody>
        </Card>
      </Grid>

      <H2>Замечания для правки</H2>
      <Table
        headers={["Приоритет", "Файл", "Проблема", "Зачем править"]}
        columnAlign={["left", "left", "left", "left"]}
        rowTone={["warning", "warning", "warning", "info", "info", "neutral"]}
        rows={[
          [
            "Средний",
            "dynamic_controls_page.py",
            "wait_for(visible/hidden) + #loading:visible",
            "В проекте UI-состояние ждётся через expect(); промежуточный spinner может флаковать",
          ],
          [
            "Средний",
            "test_hovers.py",
            "Нет реального switch hover 0 → 1",
            "Свой же Scenario 4: caption switching",
          ],
          [
            "Средний",
            "conftest.py",
            "_page_from_item без новых POM",
            "Скриншот Allure на critical не сработает",
          ],
          [
            "Низкий",
            "оба POM",
            "Магические строки, CSS .figure",
            "Конвенция 10-python-playwright.mdc",
          ],
          [
            "Низкий",
            "README.md",
            "Покрытие и /users/N = 404 не описаны",
            "Как в master для расхождений с ТЗ",
          ],
          [
            "Низкий",
            "оба test_*.py",
            "hidded в имени теста; у value нет type hint",
            "Единообразие с остальными тестами",
          ],
        ]}
      />

      <Divider />

      <H3>Покрытие vs страница</H3>
      <Grid columns={2} gap={12}>
        <Card>
          <CardHeader trailing={<Pill tone="success">10 collected</Pill>}>
            Hovers
          </CardHeader>
          <CardBody>
            <Stack gap={6}>
              <Text>Есть: 3 аватара, caption hidden/visible, href, unhover, URL профиля</Text>
              <Text tone="secondary">
                Нет: смена hover между карточками, картинки, 404 на /users/N,
                ссылка с главной
              </Text>
            </Stack>
          </CardBody>
        </Card>
        <Card>
          <CardHeader trailing={<Pill tone="success">8 collected</Pill>}>
            Dynamic Controls
          </CardHeader>
          <CardBody>
            <Stack gap={6}>
              <Text>
                Есть: init, check/uncheck, remove, add, enable+fill, disable+value
              </Text>
              <Text tone="secondary">
                Нет: ввод в disabled input, независимость секций, enabled кнопки
                после Add
              </Text>
            </Stack>
          </CardBody>
        </Card>
      </Grid>
    </Stack>
  );
}
