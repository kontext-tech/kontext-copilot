<template>
   <Chart
      :type="data.chartType"
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
   ArcElement,
   BarController,
   LineController,
   PieController
} from "chart.js"
import type { ChartRendererProps } from "~/types/UIProps"
import { Chart } from "vue-chartjs"

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
   ArcElement,
   BarController,
   LineController,
   PieController
)

const props = defineProps<{
   dataModel: ChartDataResponseModel
}>()

// const kontextColors = [
//    "#008080",
//    "#51a6db",
//    "#db9430",
//    "#20c997",
//    "#db5c5c",
//    "#212529"
// ]

const defaultColors = [
   "#3366CC",
   "#DC3912",
   "#FF9900",
   "#109618",
   "#990099",
   "#3B3EAC",
   "#0099C6",
   "#DD4477",
   "#66AA00",
   "#B82E2E",
   "#316395",
   "#994499",
   "#22AA99",
   "#AAAA11",
   "#6633CC",
   "#E67300",
   "#8B0707",
   "#329262",
   "#5574A6",
   "#651067"
]

const colorMode = useColorMode({ selector: "html", storageKey: "theme" })

const data = computed(() => toChartJsOptions(props.dataModel, fontColor))

const fontColor = computed(() => {
   return colorMode.value === "dark" ? "#6c757d" : "#212529"
})

const emits = defineEmits(["chart-generated"])

const rendered = ref(false)

const toChartJsOptions = (
   model: ChartDataResponseModel,
   fontColor: Ref<string>
): ChartRendererProps => {
   const legend = {
      display: true,
      position: "right",
      labels: {
         color: fontColor.value
      }
   }
   const options = {
      responsive: true,
      maintainAspectRatio: true,
      color: defaultColors,
      plugins: {} as { legend: object; title: object },
      animation: {
         onComplete: function () {
            if (!rendered.value) {
               rendered.value = true
               emits("chart-generated")
            }
         }
      }
   }

   // Merge the options
   Object.assign(options, model.options)

   // Check if plugins has a legend attribtue defined
   if (!Object.hasOwn(options.plugins, "legend")) {
      options.plugins.legend = legend
   }

   const data = Object.assign({}, model.data)
   return {
      chartData: data,
      chartOptions: options,
      chartType: model.type
   }
}
</script>
