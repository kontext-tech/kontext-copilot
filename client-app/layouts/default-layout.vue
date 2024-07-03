<template>
    <div class="position-fixed d-flex overflow-x-hidden overflow-y-hidden inset-0 w-100">
        <Collapse :id="sideBarId"
            class="position-relative-md sidebar-col d-md-flex flex-column align-items-stretch offcanvas-md offcanvas-start border-end flex-shrink-0 bg-body-tertiary">
            <div class="px-4 header-primary d-flex align-items-center bg-primary flex-shrink-0">
                <b-a toggle="collapse" class="d-flex d-md-none text-white me-3" :href="'#' + sideBarId" :id="toogleId2">
                    <Icon name="material-symbols:menu" size="24" />
                </b-a>
                <a href="/" class="navbar-brand">
                    <img :src="logoWhite" alt="Kontext Logo" class="img-fluid" />
                </a>
            </div>
            <div class="d-flex flex-column w-100 flex-grow-1 flex-shrink-1 position-relative overflow-y-hidden">
                <div class="flex-grow-1 d-flex flex-column">
                    <Sidebar class="flex-grow-1 flex-shrink-1" />
                    <div class="flex-grow-1 flex-shrink-1">
                        <slot name="aside" />
                    </div>
                    <div class="px-1 text-center d-flex flex-shrink-0 justify-content-center border-top py-1">
                        <small class="mt-1 mb-0 text-muted">
                            @ Kontext 2024
                        </small>
                    </div>
                </div>
            </div>
        </Collapse>
        <div class="d-flex flex-grow-1 flex-shrink-1 w-100">
            <div class="flex-column align-items-stretch position-relative w-100 flex-grow-1 flex-shrink-1 d-flex">
                <div class="header-primary d-flex align-items-center border-bottom px-4 flex-shrink-0">
                    <b-a toggle="collapse" class="d-flex d-md-none text-muted me-3" :href="'#' + sideBarId"
                        :id="toogleId1">
                        <Icon name="material-symbols:menu" size="24" />
                    </b-a>
                    <h1 class="fs-6 mb-0 pb-0 fw-bold">{{ route.meta['title'] ?? route.name }}</h1>
                    <ThemeToggle class="ms-auto" />
                </div>
                <div v-if="$slots['header-secondary']"
                    class="header-secondary d-flex align-items-center border-bottom flex-shrink-0 px-4 d-grid gap-2 flex-wrap">
                    <slot name="header-secondary" />
                </div>
                <div class="flex-grow-1 flex-shrink-1 d-flex flex-column overflow-y-auto default-area">
                    <slot name="default" />
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

const sideBarId = 'sidebar-' + useId()
const toogleId1 = 'toogle1-' + useId()
const toogleId2 = 'toogle2-' + useId()

</script>

<style scoped></style>
