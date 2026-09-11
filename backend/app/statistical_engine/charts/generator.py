from typing import Any, Dict, List, Optional
from app.statistical_engine.schemas.charts import ChartSpec, ChartAxis

class ChartGenerator:
    """
    Generates structured, frontend-agnostic chart specifications from deterministic statistical data.
    """

    def create_spec(
        self,
        chart_type: str,
        title: str,
        x_field: str,
        x_label: str,
        y_field: str,
        y_label: str,
        data: List[Dict[str, Any]],
        unit: Optional[str] = None,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ChartSpec:
        return ChartSpec(
            type=chart_type,
            title=title,
            description=description,
            xAxis=ChartAxis(field=x_field, label=x_label),
            yAxis=ChartAxis(field=y_field, label=y_label),
            data=data,
            unit=unit,
            metadata=metadata or {}
        )

    def create_cpi_trend_chart(self, years: List[int], cpi_values: List[float]) -> ChartSpec:
        data = [{"year": y, "cpi": v} for y, v in zip(years, cpi_values)]
        return self.create_spec(
            chart_type="line",
            title="Consumer Price Index Trajectory (2020-2023)",
            x_field="year",
            x_label="Calendar Year",
            y_field="cpi",
            y_label="Consumer Price Index Points",
            data=data,
            unit="index_points",
            description="Annual Consumer Price Index movement for state statistical division."
        )

    def create_commodity_weight_chart(self, categories: List[str], weights: List[float]) -> ChartSpec:
        data = [{"category": c, "weight": w} for c, w in zip(categories, weights)]
        return self.create_spec(
            chart_type="bar",
            title="Expenditure Basket Weights Distribution",
            x_field="category",
            x_label="Expenditure Category",
            y_field="weight",
            y_label="Weight Share (%)",
            data=data,
            unit="percentage"
        )

chart_generator = ChartGenerator()
