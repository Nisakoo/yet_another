import { ENDPOINTS } from "./config.js"

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export async function setQuestionLike(questionId, isLike) {
    const csrftoken = getCookie('csrftoken');
    const response = await fetch(ENDPOINTS.setQuestionLike, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            question_id: questionId,
            is_like: isLike,
        })
    });

    return response;
}

export async function setAnswerLike(answerId, isLike) {
    const csrftoken = getCookie('csrftoken');
    const response = await fetch(ENDPOINTS.setAnswerLike, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            answer_id: answerId,
            is_like: isLike,
        })
    });

    return response;
}

export async function setAnswerCorrect(answerId, isCorrect) {
    const csrftoken = getCookie('csrftoken');
    const response = await fetch(ENDPOINTS.setAnswerCorrect, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            answer_id: answerId,
            is_correct: isCorrect,
        })
    });

    return response;
}

export async function getBestTags() {
    const response = await fetch(ENDPOINTS.getBestTags, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    });

    return response;
}

export async function getBestMembers() {
    const response = await fetch(ENDPOINTS.getBestMembers, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    });

    return response;
}

export async function getSearchHint(query) {
    console.log(query);
    const response = await fetch(
        ENDPOINTS.getSearchHint + `?query=${encodeURIComponent(query)}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    });

    return response;
}