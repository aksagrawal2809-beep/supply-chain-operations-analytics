from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "daily_operations.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(DATA, parse_dates=["date"])
df["production_attainment"] = df["actual_good_units"] / df["planned_units"]
df["energy_kwh_per_good_unit"] = df["energy_kwh"] / df["actual_good_units"].replace(0, pd.NA)
df["freight_cost_per_shipment"] = df["freight_cost_inr"] / df["shipments"].replace(0, pd.NA)
df["downtime_rate_proxy"] = df["downtime_minutes"] / (df["downtime_minutes"] + 480)

kpis = pd.DataFrame({
    "metric": ["Observation days", "Planned units", "Actual good units", "Production attainment",
               "Average downtime minutes", "Average defect rate", "Energy kWh per good unit",
               "Freight cost per shipment (INR)", "On-time delivery rate"],
    "value": [len(df), df["planned_units"].sum(), df["actual_good_units"].sum(),
              df["actual_good_units"].sum()/df["planned_units"].sum(),
              df["downtime_minutes"].mean(), df["defect_rate"].mean(),
              df["energy_kwh"].sum()/df["actual_good_units"].sum(),
              df["freight_cost_inr"].sum()/df["shipments"].sum(),
              df["on_time_delivery_rate"].mean()]
})
kpis.to_csv(OUT/"overall_kpis.csv", index=False)

plant = df.groupby("plant", as_index=False).agg(
    planned_units=("planned_units","sum"),
    actual_good_units=("actual_good_units","sum"),
    downtime_minutes_avg=("downtime_minutes","mean"),
    defect_rate_avg=("defect_rate","mean"),
    energy_kwh=("energy_kwh","sum"),
    freight_cost_inr=("freight_cost_inr","sum"),
    shipments=("shipments","sum"),
    on_time_delivery_rate=("on_time_delivery_rate","mean")
)
plant["production_attainment"] = plant["actual_good_units"]/plant["planned_units"]
plant["energy_kwh_per_good_unit"] = plant["energy_kwh"]/plant["actual_good_units"]
plant["freight_cost_per_shipment"] = plant["freight_cost_inr"]/plant["shipments"]
plant.to_csv(OUT/"plant_kpis.csv", index=False)

line = df.groupby("production_line", as_index=False).agg(
    production_attainment=("production_attainment","mean"),
    downtime_minutes_avg=("downtime_minutes","mean"),
    defect_rate_avg=("defect_rate","mean"),
    energy_kwh_per_good_unit=("energy_kwh_per_good_unit","mean")
)
line.to_csv(OUT/"line_kpis.csv", index=False)

# Charts
plt.figure()
plt.bar(plant["plant"], plant["production_attainment"])
plt.ylabel("Production attainment")
plt.title("Production attainment by plant (synthetic data)")
plt.ylim(0, max(1.0, plant["production_attainment"].max()*1.1))
plt.tight_layout()
plt.savefig(OUT/"production_attainment_by_plant.png", dpi=160)
plt.close()

plt.figure()
plt.scatter(df["downtime_minutes"], df["production_attainment"], alpha=0.65)
plt.xlabel("Downtime minutes")
plt.ylabel("Production attainment")
plt.title("Downtime vs production attainment (synthetic data)")
plt.tight_layout()
plt.savefig(OUT/"downtime_vs_attainment.png", dpi=160)
plt.close()

plt.figure()
plt.bar(plant["plant"], plant["freight_cost_per_shipment"])
plt.ylabel("INR per shipment")
plt.title("Freight cost per shipment by plant (synthetic data)")
plt.tight_layout()
plt.savefig(OUT/"freight_cost_by_plant.png", dpi=160)
plt.close()

print("Analysis complete. Outputs saved to:", OUT)
print(kpis.to_string(index=False))
