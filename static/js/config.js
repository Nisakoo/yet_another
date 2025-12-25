export const API_BASE_URL = "http://127.0.0.1/api";

export const ENDPOINTS = {
    setQuestionLike: `${API_BASE_URL}/questions/like`,
    setAnswerLike: `${API_BASE_URL}/answers/like`,
    setAnswerCorrect: `${API_BASE_URL}/answers/correct`,
    getBestTags: `${API_BASE_URL}/best/tags`,
    getBestMembers: `${API_BASE_URL}/best/members`,
    getSearchHint: `${API_BASE_URL}/hint`,
};