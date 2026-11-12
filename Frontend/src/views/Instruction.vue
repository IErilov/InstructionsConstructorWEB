<script setup>

import StepCard from "../components/StepCard.vue"


defineProps({
    instruction: {
        type: Object,
        required: true,
    },

    steps: {
        type: Array,
        required: true,
    },

    activeStepId: String,

    completedSteps: {
        type: Array,
        required: true,
    },
})


defineEmits([
    "back",
    "start",
    "complete",
])

</script>


<template>

    <main class="page">

        <div class="container">

            <button
                class="back-button"
                @click="$emit('back')"
            >
                <i class="fa-solid fa-arrow-left"></i>

                Все инструкции
            </button>


            <section class="instruction-header">

                <span class="eyebrow">
                    Инструкция
                </span>

                <h1>
                    {{ instruction.name }}
                </h1>

                <p>
                    {{ instruction.description }}
                </p>

            </section>


            <section class="steps">

                <StepCard
                    v-for="(step, index) in steps"
                    :key="step.id"
                    :step="step"
                    :index="index"
                    :active="activeStepId === step.id"
                    :completed="completedSteps.includes(step.id)"
                    @start="$emit('start', step)"
                    @complete="$emit('complete', step)"
                />

            </section>

        </div>

    </main>

</template>