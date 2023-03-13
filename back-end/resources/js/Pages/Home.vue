<script setup>
    import { Head, Link } from "@inertiajs/vue3";
    import CurrentStatus from '@/Components/CurrentStatus.vue'
    import HomeData from '@/Components/HomeData.vue'

    defineProps({
        canLogin: Boolean,
        canRegister: Boolean,
        laravelVersion: String,
        phpVersion: String,
    });

</script>

<template>
    <Head title="Welcome" />

    <div class="content">
        <div class="drawer drawer-mobile">
            <input id="my-drawer-2" type="checkbox" class="drawer-toggle" />
            <div
                class="drawer-content relative flex flex-col justify-center"
            >
                <div class="h-5/6 flex flex-col items-center gap-60">
                    <CurrentStatus />
                    <div class="w-full flex-1">
                        <HomeData />
                    </div>
                </div>
                <!-- Page content here -->
                <label
                    for="my-drawer-2"
                    class="btn btn-primary drawer-button lg:hidden absolute right-5 top-5"
                    >Open drawer</label
                >
            </div>
            <div class="drawer-side">
                <label for="my-drawer-2" class="drawer-overlay"></label>
                <div class="w-80 flex items-center pl-5">
                    <ul
                        class="menu p-4 rounded-xl h-5/6 w-80 bg-base-100 text-white bg-transparent backdrop-blur-lg"
                    >
                        <!-- Sidebar content here -->
                        <div v-if="canLogin">
                            <li v-if="$page.props.auth.user">
                                <Link
                                    :href="route('dashboard')"
                                    class="justify-center"
                                >
                                    Dashboard
                                </Link>
                            </li>
                            <template v-else>
                                <li>
                                    <Link
                                        class="justify-center"
                                        :href="route('login')"
                                        >Log in
                                    </Link>
                                </li>
                                <li>
                                    <Link @msg="msg => executeFunction(msg)"
                                        v-if="canRegister"
                                        :href="route('register')"
                                        class="justify-center"
                                        >
                                        Register
                                    </Link>
                                </li>
                            </template>
                        </div>
                    </ul>
                </div>
            </div>
        </div>
    </div>


</template>

<style>
    .content {
        background-image: url("https://unsplash.com/photos/wmsZZgIxqiA/download?ixid=MnwxMjA3fDB8MXxzZWFyY2h8Mnx8c2xreXxlc3wwfHx8fDE2Nzg3MDgwMzE&force=true&w=2400");
        background-position: center center;
        background-size: cover;
        background-repeat: no-repeat;
    }

    a:hover {
        background-color: #3D3D3D40;
    }
</style>
