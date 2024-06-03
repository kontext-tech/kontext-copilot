<template>
    <div class="container-fluid p-0">
        <div class="row g-0 flex-nowrap">
            <Collapse :id="sideBarId" class="col-lg-2 col-md-3 d-flex flex-column 
                    flex-shrink-0 offcanvas-md offcanvas-start border-end min-vh-100">
                <div class="px-3 header-row d-flex align-items-center bg-primary">
                    <b-a toggle="collapse" class="d-flex d-md-none text-white me-3" :href="'#' + sideBarId"
                        :id="toogleId2">
                        <Icon name="material-symbols:menu" size="24" />
                    </b-a>
                    <a href="/" class="navbar-brand">
                        <img :src="logoWhite" alt="Kontext Logo" class="img-fluid" />
                    </a>
                </div>
                <Sidebar />
                <slot name="aside" />
                <div class="px-1 text-center d-none d-md-flex justify-content-center border-top py-1">
                    <small class="mt-1 mb-0 text-muted">
                        @ Kontext 2024
                    </small>
                </div>
            </Collapse>

            <div class="col-lg-10 col-md-9">
                <div class="header-row d-flex align-items-center border-bottom px-4">
                    <b-a toggle="collapse" class="d-flex d-md-none text-muted me-3" :href="'#' + sideBarId"
                        :id="toogleId1">
                        <Icon name="material-symbols:menu" size="24" />
                    </b-a>
                    <h1 class="fs-6 mb-0 pb-0 fw-bold">{{ route.meta['title'] ?? route.name }}</h1>
                </div>
                <div class="px-3">
                    <slot name="main" />
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import logo from '~/assets/images/logo.svg'
import logoWhite from '~/assets/images/logo-white.svg'
import Sidebar from '~/components/sidebar.vue'

const route = useRoute()
const appConfig = useAppConfig()

watchEffect(() => {
    useHead(
        {
            title: route.meta['title'] || appConfig.appName,
        }
    )
});

const sideBarId = 'sideBar' + useId()
const toogleId1 = 'toogle' + useId()
const toogleId2 = 'toogle' + useId()

</script>

<style scoped></style>