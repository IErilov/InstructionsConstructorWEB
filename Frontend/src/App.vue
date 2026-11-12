<script setup>

import { ref, onMounted } from "vue"

import AppHeader from "./components/Header.vue"

import InstructionsView from "./views/Instructions.vue"
import InstructionView from "./views/Instruction.vue"

import {
    getInstructions,
    getInstruction,
    startStep,
    completeStep,
} from "./api/instructions"


const instructions = ref([])

const selectedInstruction = ref(null)

const steps = ref([])

const loading = ref(false)

const activeStepId = ref(null)

const completedSteps = ref([])


async function loadInstructions() {

    try {

        loading.value = true

        instructions.value = await getInstructions()

    } catch (error) {

        console.error(error)

    } finally {

        loading.value = false

    }

}


async function openInstruction(instruction) {

    try {

        selectedInstruction.value = instruction

        const data = await getInstruction(
            instruction.id
        )

        steps.value = data.steps || []

    } catch (error) {

        console.error(error)

    }

}


async function start(step) {

    try {

        await startStep(
            selectedInstruction.value.id,
            step.id
        )

        activeStepId.value = step.id

    } catch (error) {

        console.error(error)

    }

}


async function complete(step) {

    try {

        await completeStep(
            selectedInstruction.value.id,
            step.id
        )

        completedSteps.value.push(step.id)

        activeStepId.value = null

    } catch (error) {

        console.error(error)

    }

}


function goHome() {

    selectedInstruction.value = null

    steps.value = []

}


onMounted(loadInstructions)

</script>


<template>

    <AppHeader
        @go-home="goHome"
    />


    <InstructionsView
        v-if="!selectedInstruction"
        :instructions="instructions"
        :loading="loading"
        @open="openInstruction"
    />


    <InstructionView
        v-else
        :instruction="selectedInstruction"
        :steps="steps"
        :active-step-id="activeStepId"
        :completed-steps="completedSteps"
        @back="goHome"
        @start="start"
        @complete="complete"
    />

</template>