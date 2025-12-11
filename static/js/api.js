import { ENDPOINTS } from "./config.js"

export async function setQuestionLike(questionId, isLike) {
    const response = await fetch(ENDPOINTS.setQuestionLike, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            question_id: questionId,
            is_like: isLike,
        })
    });

    const body = await response.json();

    if (!response.ok)
        alert(body.message);

    return body;
}

export async function setAnswerLike(answerId, isLike) {
    const response = await fetch(ENDPOINTS.setAnswerLike, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            answer_id: answerId,
            is_like: isLike,
        })
    });

    const body = await response.json();

    if (!response.ok)
        alert(body.message);

    return body;
}

export async function setAnswerCorrect(answerId, isCorrect) {
    const response = await fetch(ENDPOINTS.setAnswerCorrect, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            answer_id: answerId,
            is_correct: isCorrect,
        })
    });

    const body = await response.json();

    if (!response.ok)
        alert(body.message);

    return body;
}