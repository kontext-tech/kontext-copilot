<template>
    <NavList nav="tabs" tablist margin="b-3">
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
    <TabContent :id="tabContentId">
        <TabPane :id="generalTabId" active>
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <h6>Theme</h6>
                    <span class="text-muted">Customize color theme.</span>
                </div>
                <ThemeToggle />
            </div>
            <hr />

        </TabPane>

        <TabPane :id="llmsTabId">
            <p>
                TBA
            </p>
        </TabPane>
    </TabContent>

</template>

<script setup lang="ts">
const id = useId()
const generalTabId = 'tab-general-' + id
const llmsTabId = 'tab-llms-' + id
const tabContentId = 'tab-content-' + id

definePageMeta({
    title: 'Settings',
})


</script>
