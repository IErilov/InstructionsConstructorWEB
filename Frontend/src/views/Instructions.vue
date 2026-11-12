<script setup>

import InstructionCard from "../components/card.vue"


defineProps({
    instructions: {
        type: Array,
        required: true,
    },

    loading: Boolean,
})

defineEmits(["open"])

</script>


<template>

    <main class="page">

        <section class="hero">

            <div class="container">

                <span class="eyebrow">
                    Инструкции
                </span>

                <h1>
                    Выберите инструкцию
                </h1>

                <p>
                    Пошаговые инструкции для выполнения задач.
                </p>

            </div>

        </section>


        <section class="instructions-section">

            <div class="container">

                <div
                    v-if="loading"
                    class="loading"
                >
                    Загрузка инструкций...
                </div>


                <div
                    v-else-if="instructions.length"
                    class="instructions-grid"
                >

                    <InstructionCard
                        v-for="instruction in instructions"
                        :key="instruction.id"
                        :instruction="instruction"
                        @open="$emit('open', instruction)"
                    />

                </div>


                <div
                    v-else
                    class="empty-state"
                >

                    <i class="fa-solid fa-folder-open"></i>

                    <h2>
                        Инструкций пока нет
                    </h2>

                    <p>
                        Создайте инструкцию через админ-панель.
                    </p>

                </div>

            </div>

        </section>

    </main>

</template>