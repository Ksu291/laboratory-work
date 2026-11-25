# Расчёт показателей
import pandas as pd


def analyze_data(trips, trips_full, plan, analysis_month):
    # Количество рейсов и выручка по перевозчикам
    by_carrier = trips.groupby("carrier").agg(
        trips_count=("trip_id", "count"),
        revenue=("cost_rub", "sum")
    ).reset_index()

    # Выручка по месяцам и типам груза
    by_month_cargo = trips.groupby(["month", "cargo_type"]).agg(
        revenue=("cost_rub", "sum")
    ).reset_index()

    # Выручка по сегментам клиентов
    by_segment = trips_full.groupby("segment").agg(
        revenue=("cost_rub", "sum")
    ).reset_index()

    # Сводная таблица по перевозчикам и месяцам
    pivot_carrier_month = pd.pivot_table(
        trips, values="cost_rub", index="carrier",
        columns="month", aggfunc="sum", fill_value=0
    )

    # Выбираем рейсы за нужный месяц
    month_trips = trips[trips["month"] == analysis_month]

    # Считаем фактическое количество рейсов и выручку по маршрутам
    fact = month_trips.groupby("route").agg(
        fact_trips=("trip_id", "count"),
        fact_revenue=("cost_rub", "sum")
    ).reset_index()

    # Сравниваем план и факт
    plan_fact = plan.merge(fact, on="route", how="left")
    plan_fact[["fact_trips", "fact_revenue"]] = plan_fact[
        ["fact_trips", "fact_revenue"]
    ].fillna(0)

    plan_fact["trips_done_pct"] = (
        plan_fact["fact_trips"] / plan_fact["plan_trips"] * 100
    ).round(2)
    plan_fact["revenue_done_pct"] = (
        plan_fact["fact_revenue"] / plan_fact["plan_revenue"] * 100
    ).round(2)

    # Общие показатели
    summary = {
        "Количество рейсов": len(trips),
        "Выручка за два месяца": round(trips["cost_rub"].sum(), 2),
        "Средняя стоимость рейса": round(trips["cost_rub"].mean(), 2),
        "Средняя задержка": round(trips["delay_h"].mean(), 2),
        "Выполнение плана по рейсам, %": round(
            plan_fact["fact_trips"].sum() / plan_fact["plan_trips"].sum() * 100, 2
        ),
        "Выполнение плана по выручке, %": round(
            plan_fact["fact_revenue"].sum() / plan_fact["plan_revenue"].sum() * 100, 2
        )
    }

    return by_carrier, by_month_cargo, by_segment, pivot_carrier_month, plan_fact, summary
