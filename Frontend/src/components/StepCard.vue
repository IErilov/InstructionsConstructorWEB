<script setup>

defineProps({
    step: {
        type: Object,
        required: true,
    },

    index: {
        type: Number,
        required: true,
    },

    active: Boolean,

    completed: Boolean,
})

defineEmits([
    "start",
    "complete",
])

</script>


<template>

    <article
        class="step-card"
        :class="{
            active,
            completed,
        }"
    >

        <div class="step-number">

            <i
                v-if="completed"
                class="fa-solid fa-check"
            ></i>

            <span v-else>
                {{ index + 1 }}
            </span>

        </div>


        <div class="step-content">

            <h3>
                {{ step.title }}
            </h3>

            <p>
                {{ step.order }}
            </p>

        </div>


        <div class="step-actions">

            <button
                v-if="!active && !completed"
                class="button secondary"
                @click="$emit('start')"
            >
                Начать
            </button>


            <button
                v-if="active && !completed"
                class="button primary"
                @click="$emit('complete')"
            >
                Завершить
            </button>


            <span
                v-if="completed"
                class="completed-label"
            >
                Выполнено
            </span>

        </div>

    </article>

</template>