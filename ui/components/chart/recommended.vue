<template>
   <div v-if="chartList.length > 0" class="card shadow-sm my-3">
      <div class="card-header d-flex gap-1">
         <Icon name="material-symbols:auto-graph" class="text-primary" />
         <b>Recommended charts</b>
      </div>
      <div class="card-body">
         <div class="d-flex gap-1">
            <BFormSelect
               v-if="chartList.length > 0"
               v-model="chartIndex"
               :options="chartTypeOptions"
               value-field="index"
               text-field="text"
               @change="fetchData"
            />

            <BFormSelect
               v-model="aggType"
               :options="aggTypeOptions"
               @change="fetchData"
            />
         </div>
         <div v-if="chartDataFetchState.loading" class="text-center">
            <BSpinner variant="primary" />
         </div>
         <BAlert v-else-if="chartDataFetchState.error" variant="danger" show>
            {{ chartDataFetchState.error }}
         </BAlert>
         <ChartRenderer
            v-else-if="chartResponseData"
            :data-model="chartResponseData"
            @chart-generated="handleChartGenerated"
         />
      </div>
   </div>
</template>

<script lang="ts" setup>
import {
   ActionsDataKeys,
   type ChartDataResponseModel,
   AggregateTypes,
   type ChartListModel
} from "~/types/Schemas"
import type { ChartRecommendedProps } from "~/types/UIProps"

import type CopilotClientService from "~/services/CopilotClientService"

const props = defineProps<ChartRecommendedProps>()

const chartTypeOptions = computed(() => {
   return chartList.value.map((chart, i) => {
      return {
         text: `${chart.title} (${chart.chartType})`,
         chart: chart,
         index: i
      }
   })
})

const chartListModel = computed(() => {
   return (props.message.actions?.data?.[ActionsDataKeys.RECOMMENDED_CHARTS] ??
      null) as ChartListModel
})

const chartList = computed(() => {
   return chartListModel.value.charts
})

const chartIndex = ref(0)

const chart = computed(() => {
   return chartList.value[chartIndex.value]
})

const aggTypeOptions = computed(() => {
   return Object.values(AggregateTypes).map((value) => {
      return {
         text: value,
         value: value
      }
   })
})

const aggType = ref<AggregateTypes>(AggregateTypes.SUM)

const copilotClient = inject<CopilotClientService>(COPLIOT_CLIENT_KEY)

const chartResponseData = ref<ChartDataResponseModel | null>(null)

const chartDataFetchState = reactive({
   loading: false,
   error: null as string | null
})

const emits = defineEmits(["chart-generated"])
const handleChartGenerated = () => {
   emits("chart-generated", props.message.id)
}

const fetchData = async () => {
   if (copilotClient && props.dataSourceId && chartList.value.length > 0) {
      chartDataFetchState.loading = true
      chartDataFetchState.error = null
      chart.value.aggregateType = aggType.value
      try {
         const data = await copilotClient.getChartData(
            chart.value,
            props.dataSourceId,
            props.schemaSelector?.schema,
            chartListModel.value.cached,
            chartListModel.value.cachedTableName,
            props.message.id
         )
         chartResponseData.value = data
         chartDataFetchState.error = null
      } catch (error) {
         chartDataFetchState.error = String(error)
      } finally {
         chartDataFetchState.loading = false
      }
   }
}

onMounted(() => {
   fetchData()
})
</script>
