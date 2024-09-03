import duckdb

from kontext_copilot.data.schemas import (
    AggregateTypes,
    ChartDataModel,
    ChartDataRequestModel,
    ChartDataResponseModel,
    ChartTypes,
    PieChartModel,
)
from kontext_copilot.utils import ANA_DB_PATH, get_logger

logger = get_logger()


class ChartRenderer:
    def __init__(
        self,
        request: ChartDataRequestModel,
    ):
        self.chart_model = request.chart
        self.cached = request.cached
        self.cached_table_name = request.cached_table_name
        # default to sum if not provided
        self.agg_type = request.chart.aggregate_type or AggregateTypes.SUM

        if not self.cached:
            raise ValueError("Cached data not provided")

    def render(self) -> ChartDataResponseModel:
        """
        Render the chart
        """
        supported_chart_types = [ChartTypes.PIE, ChartTypes.BAR, ChartTypes.LINE]
        if self.chart_model.chart_type in supported_chart_types:
            return self.render_chart()
        else:
            raise ValueError(f"Chart type {self.chart_model.chart_type} not supported")

    def _get_title(self) -> dict:
        """
        Get the title of the chart

        Returns: dict
        """
        return {
            "title": {
                "display": True,
                "text": self.chart_model.title
                or "Chart - {self.chart_model.chart_type}",
            }
        }

    def render_chart(self) -> ChartDataResponseModel:
        """
        Render the pie chart
        """
        options = {}
        plugins = {}
        plugins.update(self._get_title())
        options.update(plugins=plugins)
        labels, dataset = self._get_chart_data()
        res = ChartDataResponseModel(
            data=ChartDataModel(labels=labels, datasets=[dataset]),
            type=self.chart_model.chart_type,
            options=options,
        )
        return res

    def _get_conn(self):
        """
        Get the connection to the database
        """
        return duckdb.connect(database=ANA_DB_PATH)

    def _get_chart_data(self):
        labels = []
        dataset = {}
        # check if x_title is provided
        if self.chart_model.chart_type == ChartTypes.PIE:
            dataset["label"] = (
                self.chart_model.x_title
                if hasattr(self.chart_model, "x_title")
                else f"{self.chart_model.data_column} via {self.agg_type}"
            )
        else:
            dataset["label"] = (
                self.chart_model.y_title
                if hasattr(self.chart_model, "y_title")
                else f" {self.agg_type}({self.chart_model.y_data_column})"
            )

        with self._get_conn() as conn:
            if isinstance(self.chart_model, PieChartModel):
                data_column_alias = self.agg_type.capitalize()
                data_column = self.chart_model.data_column
                label_column = self.chart_model.label_column
            else:
                data_column_alias = (
                    f"{self.chart_model.y_data_column} - {self.agg_type.capitalize()}"
                )
                data_column = self.chart_model.y_data_column
                label_column = self.chart_model.x_data_column

            query = f"""SELECT COALESCE("{label_column}", '(NULL)') AS "{label_column}",
            {self.agg_type}("{data_column}") AS "{data_column_alias}"
            FROM {self.cached_table_name}
            GROUP BY "{label_column}"
            ORDER BY "{label_column}"
            """

            logger.info(f"Running query: {query}")

            result = conn.execute(query).fetch_arrow_table()

            data_dict = result.to_pylist()

            for row in data_dict:
                labels.append(row[label_column])

            dataset["data"] = result[data_column_alias].to_pylist()
            dataset["label"] = data_column_alias

        return labels, dataset
