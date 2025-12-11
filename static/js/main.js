import {setQuestionLike, setAnswerLike, setAnswerCorrect} from './api.js'

const likeButtons = document.querySelectorAll('a[data-object-id][data-like]')

likeButtons.forEach(button => {
    const objectProperties = button.getAttribute("data-object-id").split("-");
    const objectType = objectProperties[0];
    const objectId = objectProperties[1];
    const isLike = button.getAttribute("data-like");

    if (objectType == "question") {
        button.addEventListener("click", async function(e) {
            const response = await setQuestionLike(objectId, isLike);
            const rating = document.querySelector(`div[data-object-id=${objectType}-${objectId}]`);
            rating.textContent = response.rating;

            console.log(objectType, objectId, isLike, response);
        });
    } else if (objectType == "answer") {
        button.addEventListener("click", async function(e) {
            const response = await setAnswerLike(objectId, isLike);
            const rating = document.querySelector(`div[data-object-id=${objectType}-${objectId}]`);
            rating.textContent = response.rating;

            console.log(objectType, objectId, isLike, response);
        });
    }
});

const correctCheckboxes = document.querySelectorAll("input[type=checkbox][data-object-id]");

correctCheckboxes.forEach(checkbox => {
    const objectProperties = checkbox.getAttribute("data-object-id").split("-");
    const objectType = objectProperties[0];
    const objectId = objectProperties[1];

    if (objectType == "answer") {
        checkbox.addEventListener("change", async function(e) {
            const response = await setAnswerCorrect(objectId, this.checked);
            this.checked = response.is_correct;
        });
    }
});