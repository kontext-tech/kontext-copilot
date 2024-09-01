<template>
   <component
      :is="chartComponent"
      :data="data.chartData"
      :options="data.chartOptions"
   />
</template>

<script setup lang="ts">
import type { ChartDataResponseModel } from "~/types/Schemas"
import {
   Chart as ChartJS,
   Title,
   Tooltip,
   Legend,
   BarElement,
   CategoryScale,
   LinearScale,
   Colors,
   PointElement,
   LineElement,
   ArcElement
} from "chart.js"
import type { ChartRendererProps } from "~/types/UIProps"
import { Bar, Line, Pie } from "vue-chartjs"

ChartJS.register(
   CategoryScale,
   LinearScale,
   BarElement,
   Title,
   Tooltip,
   Legend,
   Colors,
   LineElement,
   PointElement,
   ArcElement
)

const props = defineProps<{
   dataModel: ChartDataResponseModel
}>()

const chartComponents = {
   bar: Bar,
   line: Line,
   pie: Pie
}

const chartComponent = computed(() => {
   return chartComponents[props.dataModel.type] || Bar
})

const data = computed(() => toChartJsOptions(props.dataModel))

const toChartJsOptions = (
   model: ChartDataResponseModel
): ChartRendererProps => {
   const options = {
      responsive: true,
      maintainAspectRatio: true
   }
   Object.assign(options, model.options)
   const data = Object.assign({}, model.data)
   return {
      chartData: data,
      chartOptions: options,
      chartType: model.type
   }
}
</script>
