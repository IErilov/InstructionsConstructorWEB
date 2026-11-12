const API_URL = "/api"


async function request(url, options = {}) {
    const response = await fetch(url, {
        credentials: "include",
        ...options,
    })

    if (!response.ok) {
        const errorText = await response.text()

        throw new Error(
            errorText || `Ошибка API: ${response.status}`
        )
    }

    return response.json()
}


/*
|--------------------------------------------------------------------------
| Instructions
|--------------------------------------------------------------------------
*/

export async function getInstructions() {
    return request(
        `${API_URL}/instructions`
    )
}


export async function getInstruction(instructionId) {
    return request(
        `${API_URL}/instructions/${instructionId}`
    )
}


/*
|--------------------------------------------------------------------------
| Steps
|--------------------------------------------------------------------------
*/

export async function startStep(instructionId, stepId) {
    return request(
        `${API_URL}/instructions/${instructionId}/steps/${stepId}/start`,
        {
            method: "POST",
        }
    )
}


export async function completeStep(instructionId, stepId) {
    return request(
        `${API_URL}/instructions/${instructionId}/steps/${stepId}/complete`,
        {
            method: "POST",
        }
    )
}


/*
|--------------------------------------------------------------------------
| Analytics
|--------------------------------------------------------------------------
*/

export async function getAnalytics(instructionId) {
    return request(
        `${API_URL}/instructions/${instructionId}/analytics`
    )
}