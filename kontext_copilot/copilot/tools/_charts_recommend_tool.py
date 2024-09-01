from typing import Any, Dict

from kontext_copilot.copilot._copilot_session import CopilotSession
from kontext_copilot.copilot.tools._base_tool import BaseTool
from kontext_copilot.copilot.tools._data_analyser import DataAnalyser
from kontext_copilot.data.schemas import (
    ActionsDataKeys,
    ActionTypes,
    BarChartModel,
    ChartListModel,
    ChartTypes,
    ColumnStatsModel,
    LineChartModel,
    PieChartModel,
    QueryStatsModel,
    SessionMessageModel,
)


class ChartsRecommendTool(BaseTool):
    """Recommend charts based on SQL query"""

    def __init__(self, session: CopilotSession) -> None:
        super().__init__("Charts Recommendation", session)

    def execute(self, message: SessionMessageModel) -> None:
        """Recommend charts based on SQL query"""
        data = self.session.get_shared_data(message, self.RUN_SQL_RESULT_DATA_KEY)
        if data:
            self._recommend_charts(message, data)

    def _get_col_stats(self, col_name: str, stats: QueryStatsModel) -> ColumnStatsModel:
        """
        Get column stats
        """
        for col_stat in stats.column_stats:
            if col_stat.column_name == col_name:
                return col_stat

    def _recommend_charts(
        self, message: SessionMessageModel, data: list[Dict[str, Any]]
    ) -> None:
        """Recommend charts based on SQL query"""

        data_analyser = DataAnalyser(message, data)
        stats = data_analyser.analyse()

        # Recommend charts based on stats
        self._logger.debug("Recommend charts based on stats")
        self._logger.debug(stats)

        charts_list = ChartListModel(charts=[])

        # Recommend pie charts
        for bool_col in stats.boolean_columns:
            for num_col in stats.numerical_columns:
                chart = PieChartModel(
                    chart_type=ChartTypes.BAR,
                    title=f"{num_col} by {bool_col}",
                    data_column=num_col,
                    label_column=bool_col,
                )
                charts_list.charts.append(chart)

        # Recommend pie charts for category columns
        for cat_col in stats.categorical_columns:
            for num_col in stats.numerical_columns:
                # find out the only column stats for num_col
                column_stats = self._get_col_stats(cat_col, stats)

                if column_stats.approx_unique <= 10:
                    chart = PieChartModel(
                        chart_type=ChartTypes.PIE,
                        title=f"{num_col} by {cat_col}",
                        data_column=num_col,
                        label_column=cat_col,
                    )
                    charts_list.charts.append(chart)

        # Recommend bar & line charts
        for cat_col in stats.categorical_columns:
            for num_col in stats.numerical_columns:
                chart = BarChartModel(
                    chart_type=ChartTypes.BAR,
                    title=f"{num_col} by {cat_col}",
                    x_data_column=cat_col,
                    y_data_column=num_col,
                )
                charts_list.charts.append(chart)

                chart = LineChartModel(
                    chart_type=ChartTypes.LINE,
                    title=f"{num_col} by {cat_col}",
                    x_data_column=cat_col,
                    y_data_column=num_col,
                )
                charts_list.charts.append(chart)

        charts_list.cached = stats.cached
        charts_list.cached_table_name = stats.cache_table_name
        message.add_actions(
            actions=[ActionTypes.RECOMMEND_CHARTS],
            data={ActionsDataKeys.RECOMMENDED_CHARTS: charts_list},
        )
