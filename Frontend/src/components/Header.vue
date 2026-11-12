<script setup>
defineEmits(["go-home"])
</script>

<template>

    <header class="app-header">

        <div class="container header-content">

            <button
                class="brand"
                @click="$emit('go-home')"
            >
                <span class="brand-icon">
                    <i class="fa-solid fa-list-check"></i>
                </span>

                <span>
                    ICW
                </span>
            </button>


            <div class="header-right">

                <span class="header-status">
                    <span class="status-dot"></span>
                    Система работает
                </span>

            </div>

        </div>

    </header>

</template>