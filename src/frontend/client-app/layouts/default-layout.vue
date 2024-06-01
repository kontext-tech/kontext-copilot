<template>
    <div class="container-fluid p-0">
        <div class="row g-0">
            <div id="sidebar" class="col-lg-2 col-md-3 d-flex flex-column 
                    flex-shrink-0 
                    py-3 bg-body-tertiary offcanvas-md offcanvas-start border-end vh-100">
                <div class="px-1">
                    <a href="/" class="navbar-brand">
                        <img src="/logo.svg" alt="Kontext Logo" class="img-fluid" />
                    </a>
                </div>
                <hr class="text-muted">
                <ul class="nav nav-pills flex-column mb-auto flex-fill">
                    <NavItem to="/" icon="material-symbols:home-outline" text="Home" />
                    <NavItem to="/chat" icon="material-symbols:chat-add-on-outline" text="Chat" />
                    <NavItem to="/settings" icon="material-symbols:settings-outline" text="Settings" />
                </ul>
                <slot name="aside" />
                <hr class="text-muted">
                <div class="px-1 text-center d-none d-md-flex">
                    <small class="mt-1 mb-0 text-muted">
                        @ Kontext 2024
                    </small>
                </div>
            </div>

            <div class="col-lg-10 col-md-9">
                <div class="p-2 d-md-none d-flex text-white bg-primary">
                    <a href="#" class="text-white" data-bs-toggle="offcanvas" data-bs-target="#sidebar">
                        <i class="fa-solid fa-bars"></i>
                    </a>
                    <a href="/" class="navbar-brand ms-3">
                        <img src="/logo-white.svg" alt="Kontext Logo" class="img-fluid" />
                    </a>
                </div>
                <div class="p-4">
                    <nav style="--bs-breadcrumb-divider:'>';font-size:14px">
                        <ol class="breadcrumb">
                            <li class="breadcrumb-item">
                                <a href="/" class="d-flex align-items-center">
                                    <Icon name="material-symbols:home-outline" size="24" />
                                    Home
                                </a>
                            </li>
                        </ol>
                    </nav>

                    <hr>
                    <div class="row">
                        <div class="col">
                            <slot name="main" />
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'DefaultLayout'
}
</script>

<style scoped></style>