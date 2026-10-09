-- SQL examples for SQLite / MySQL. Adjust data types for your SQL engine.
CREATE TABLE daily_operations (
  date DATE,
  plant VARCHAR(50),
  production_line VARCHAR(20),
  planned_units INT,
  actual_good_units INT,
  downtime_minutes DECIMAL(8,1),
  defect_rate DECIMAL(6,4),
  energy_kwh DECIMAL(12,1),
  material_cost_inr DECIMAL(14,2),
  labor_hours DECIMAL(8,1),
  shipments INT,
  avg_route_km INT,
  freight_cost_inr DECIMAL(14,2),
  on_time_delivery_rate DECIMAL(6,4)
);

-- 1. Plant-level operating scorecard
SELECT plant,
       SUM(actual_good_units) / NULLIF(SUM(planned_units), 0) AS production_attainment,
       AVG(downtime_minutes) AS avg_downtime_minutes,
       AVG(defect_rate) AS avg_defect_rate,
       SUM(energy_kwh) / NULLIF(SUM(actual_good_units), 0) AS energy_per_good_unit,
       SUM(freight_cost_inr) / NULLIF(SUM(shipments), 0) AS freight_cost_per_shipment,
       AVG(on_time_delivery_rate) AS avg_on_time_delivery
FROM daily_operations
GROUP BY plant
ORDER BY production_attainment ASC;

-- 2. Find high-downtime observations for root-cause review
SELECT date, plant, production_line, downtime_minutes, planned_units, actual_good_units
FROM daily_operations
WHERE downtime_minutes >= 90
ORDER BY downtime_minutes DESC;

-- 3. Monthly trend (syntax may vary by database)
SELECT SUBSTR(CAST(date AS CHAR), 1, 7) AS month,
       SUM(actual_good_units) AS good_units,
       SUM(planned_units) AS planned_units,
       AVG(defect_rate) AS avg_defect_rate,
       AVG(on_time_delivery_rate) AS avg_on_time_delivery
FROM daily_operations
GROUP BY SUBSTR(CAST(date AS CHAR), 1, 7)
ORDER BY month;

-- 4. Logistics: identify expensive long-distance routes for review
SELECT plant, avg_route_km,
       SUM(freight_cost_inr) / NULLIF(SUM(shipments), 0) AS cost_per_shipment,
       AVG(on_time_delivery_rate) AS on_time_delivery
FROM daily_operations
GROUP BY plant, avg_route_km
HAVING SUM(shipments) >= 5
ORDER BY cost_per_shipment DESC;
