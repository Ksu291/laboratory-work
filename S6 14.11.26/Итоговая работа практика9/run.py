# Главный файл. Запускает весь проект.
import config
from src.load import load_data
from src.prepare import prepare_data
from src.analyze import analyze_data


def main():
    # Создаём папки для результатов, если их ещё нет
    config.RESULT_DIR.mkdir(parents=True, exist_ok=True)
    config.REPORT_DIR.mkdir(parents=True, exist_ok=True)

    print("1/3 Загрузка исходных данных")
    april, may, carriers, clients, plan = load_data()

    print("2/3 Подготовка и объединение")
    trips, trips_full = prepare_data(april, may, carriers, clients)

    print("3/3 Расчёт показателей.")
    by_carrier, by_month_cargo, by_segment, pivot, plan_fact, summary = analyze_data(
        trips, trips_full, plan, config.ANALYSIS_MONTH
    )

    # Сохраняем полученные таблицы в CSV
    trips.to_csv(config.RESULT_DIR / "trips.csv", index=False, encoding="utf-8-sig")
    by_carrier.to_csv(config.RESULT_DIR / "by_carrier.csv", index=False, encoding="utf-8-sig")
    by_month_cargo.to_csv(config.RESULT_DIR / "by_month_cargo.csv", index=False, encoding="utf-8-sig")
    by_segment.to_csv(config.RESULT_DIR / "by_segment.csv", index=False, encoding="utf-8-sig")
    pivot.to_csv(config.RESULT_DIR / "pivot_carrier_month.csv", encoding="utf-8-sig")
    plan_fact.to_csv(config.RESULT_DIR / "plan_fact.csv", index=False, encoding="utf-8-sig")

    # Создаём простой текстовый отчёт
    report = "ОТЧЁТ ПО ПРАКТИКЕ 9\n\n"
    report += f"Месяц анализа: {config.ANALYSIS_MONTH}\n\n"
    report += "ОСНОВНЫЕ ПОКАЗАТЕЛИ\n"
    for name, value in summary.items():
        report += f"{name}: {value}\n"

    report += "\nВЫПОЛНЕНИЕ ПЛАНА ПО МАРШРУТАМ\n"
    report += plan_fact.to_string(index=False)

    report += "\n\nВЫВОД\n"
    report += "План по выручке выполнен на "
    report += str(summary["Выполнение плана по выручке, %"]) + "%.\n"
    report += "Таблицы с результатами находятся в папке data/processed."

    with open(config.REPORT_DIR / "report.txt", "w", encoding="utf-8") as file:
        file.write(report)

    print("Готово! Результаты сохранены в папках data/processed и reports.")
    print("Выполнение плана по выручке:", summary["Выполнение плана по выручке, %"], "%")


if __name__ == "__main__":
    main()
