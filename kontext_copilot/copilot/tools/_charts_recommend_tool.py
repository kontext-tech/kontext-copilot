from typing import Any, Dict

from kontext_copilot.copilot._copilot_session import CopilotSession
from kontext_copilot.copilot.tools._base_tool import BaseTool
from kontext_copilot.copilot.tools._data_analyser import DataAnalyser
from kontext_copilot.data.schemas import (
    ActionTypes,
    BarChartModel,
    ChartListModel,
    ChartTypes,
    LineChartModel,
    PieChartModel,
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
                    title=f"{num_col.column_name} by {bool_col.column_name}",
                    data_column=num_col.column_name,
                    label_column=bool_col.column_name,
                )
                charts_list.charts.append(chart)

        # Recommend bar & line charts
        for cat_col in stats.categorical_columns:
            for num_col in stats.numerical_columns:
                chart = BarChartModel(
                    chart_type=ChartTypes.BAR,
                    title=f"Bar chart ({num_col} by {cat_col})",
                    x_data_column=cat_col,
                    y_data_column=num_col,
                )
                charts_list.charts.append(chart)

                chart = LineChartModel(
                    chart_type=ChartTypes.LINE,
                    title=f"Line chart ({num_col} by {cat_col})",
                    x_data_column=cat_col,
                    y_data_column=num_col,
                )
                charts_list.charts.append(chart)

        message.add_actions(
            actions=[ActionTypes.RECOMMEND_CHARTS], data=charts_list.model_dump()
        )
