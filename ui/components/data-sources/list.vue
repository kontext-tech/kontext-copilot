<template>
    <template v-if="dataSources">
        <div v-if="dataSources.length > 0">
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Type</th>
                            <th>Description</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="dataSource in dataSources" :key="dataSource.id">
                            <td>{{ dataSource.id }}</td>
                            <td>{{ dataSource.name }}</td>
                            <td>
                                <BBadge variant="light">{{ dataSource.type }}</BBadge>
                            </td>
                            <td>{{ dataSource.description }}</td>
                            <td></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        <div class="alert alert-warning" v-else>
            No data sources found.
        </div>
    </template>
    <template v-else>
        <div class="w-100 h-100">
            <BSpinner label="Loading data sources..." />
        </div>
    </template>

</template>

<script setup lang="ts">
import type { DataSourceModel } from '~/types/Schemas';

defineProps<{
    dataSources: DataSourceModel[] | undefined
}>()

</script>
