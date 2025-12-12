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
            const content = await response.json();

            if (response.ok) {
                const rating = document.querySelector(`div[data-object-id=${objectType}-${objectId}]`);
                rating.textContent = content.rating;
            } else {
                alert(content.message);
            }
        });
    } else if (objectType == "answer") {
        button.addEventListener("click", async function(e) {
            const response = await setAnswerLike(objectId, isLike);
            const rating = document.querySelector(`div[data-object-id=${objectType}-${objectId}]`);
            const content = await response.json();

            if (response.ok) {
                rating.textContent = content.rating;
            } else {
                alert(content.message);
            }

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
            const content = await response.json();

            if (response.ok) {
                this.checked = content.is_correct;
            } else {
                alert(content.message);
            }
        });
    }
});