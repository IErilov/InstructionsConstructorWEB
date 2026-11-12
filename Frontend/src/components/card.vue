<script setup>

defineProps({
    instruction: {
        type: Object,
        required: true,
    },
})

defineEmits(["open"])

</script>


<template>

    <article
        class="instruction-card"
        @click="$emit('open', instruction)"
    >

        <div class="instruction-card-icon">
            <i class="fa-solid fa-book-open"></i>
        </div>


        <div class="instruction-card-content">

            <h3>
                {{ instruction.name }}
            </h3>

            <p>
                {{ instruction.description || "Инструкция для выполнения задачи" }}
            </p>

        </div>


        <div class="instruction-card-arrow">
            <i class="fa-solid fa-chevron-right"></i>
        </div>

    </article>

</template>