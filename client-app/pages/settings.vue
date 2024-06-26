<template>
    <NuxtLayout>
        <DefaultLayout>
            <NavList nav="tabs" tablist margin="b-3" class="px-4 mt-3 w-100">
                <NavItem>
                    <NavLink :id="'navtab-' + generalTabId" active toggle="tab" :tab="'#' + generalTabId"
                        class="d-flex align-items-center cursor-pointer">
                        <Icon name="material-symbols:settings" size="20" /><span class="ms-1">General</span>
                    </NavLink>
                </NavItem>
                <NavItem>
                    <NavLink :id="'navtab-' + llmsTabId" toggle="tab" :tab="'#' + llmsTabId"
                        class="d-flex align-items-center cursor-pointer">
                        <Icon name="material-symbols:neurology-outline" size="20" /><span class="ms-1">LLMs</span>
                    </NavLink>
                </NavItem>
            </NavList>
            <TabContent :id="tabContentId" class="px-4 w-100">
                <TabPane :id="generalTabId" active>
                    <div class="d-flex justify-content-between align-items-center">
                        <div class="col-md-8">
                            <h6>Theme</h6>
                            <span class="text-muted">Customize color theme.</span>
                        </div>
                        <ThemeToggle class="col-md-4" />
                    </div>
                    <hr />
                    <div class="d-flex justify-content-between align-items-center">
                        <div class="col-md-8">
                            <h6>Name</h6>
                            <span class="text-muted">Your name.</span>
                        </div>
                        <div class="col-md-4">
                            <BFormInput id="username" v-model="username" />
                        </div>
                    </div>
                    <hr />

                </TabPane>

                <TabPane :id="llmsTabId">
                    <LlmSettings />
                </TabPane>
            </TabContent>
        </DefaultLayout>
    </NuxtLayout>
</template>

<script setup lang="ts">
import DefaultLayout from '~/layouts/default-layout.vue';

const id = useId()
const generalTabId = 'tab-general-' + id
const llmsTabId = 'tab-llms-' + id
const tabContentId = 'tab-content-' + id

usePageTitle()

const username = useUsername()

</script>
