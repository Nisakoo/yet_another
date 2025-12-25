import {setQuestionLike, setAnswerLike, setAnswerCorrect, getBestTags, getBestMembers, getSearchHint} from './api.js'

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
                this.checked = !this.checked;
            }
        });
    }
});


async function loadBestTags() {
    const container = document.getElementById("popular-tags");
    const template = document.getElementById("popular-tags-template");

    container.innerHTML = "";

    try {
        const response = await getBestTags();

        if (!response.ok)
            throw new Error("Error occur");

        const bestTags = await response.json();

        const fragment = document.createDocumentFragment();

        bestTags.tags.forEach(tag => {
            const clone = template.content.cloneNode(true);

            clone.querySelector(".tag-link").textContent = tag.name;
            clone.querySelector(".tag-link").href = tag.url;

            fragment.append(clone);
        });

        container.append(fragment);
    } catch (error) {
        console.error(error);
        container.textContent = "Error while loading";
    }
}

loadBestTags();

async function loadBestMembers() {
    const container = document.getElementById("popular-members");
    const template = document.getElementById("popular-members-template");

    container.innerHTML = "";

    try {
        const response = await getBestMembers();

        if (!response.ok)
            throw new Error("Error occur");

        const bestMembers = await response.json();

        const fragment = document.createDocumentFragment();

        bestMembers.members.forEach(member => {
            const clone = template.content.cloneNode(true);

            clone.querySelector(".member-link").textContent = member;

            fragment.append(clone);
        });

        container.append(fragment);
    } catch (error) {
        console.error(error);
        container.textContent = "Error while loading";
    }
}

loadBestMembers();

const searchInput = document.getElementById("search-input");

searchInput.addEventListener("click", function(e) {
    const hintsBox = document.getElementById("hints");
    hintsBox.style.display = "block";
});

searchInput.addEventListener('keypress', function(event) {
    if (event.key == "Enter") {
        event.preventDefault();
        const query = searchInput.value.trim();
        
        if (query) {
            window.location.href = `/search?query=${encodeURIComponent(query)}`;
        }
    }
});

let debounceTimer;

searchInput.addEventListener("input", async function(e) {
    const query = e.target.value.trim();
    const hintsBox = document.getElementById("hints");

    clearTimeout(debounceTimer);

    hintsBox.style.display = "block";

    debounceTimer = setTimeout(async () => {
        const results = await fetchHints(query);
        await displayResults(results);
    }, 300);
})

async function fetchHints(query) {
    const response = await getSearchHint(query);

    if (!response.ok)
        throw new Error("Error while loading hints");

    const content = await response.json();
    return content.result;
}

function truncateString(s, shrinkTo) {
    if (s.length > shrinkTo) {
        return s.substring(0, shrinkTo) + "...";
    }

    return s;
}

async function displayResults(results) {
    const hintsBox = document.getElementById("hints");
    const template = document.getElementById("search-hint-template");

    hintsBox.innerHTML = "";

    const fragment = document.createDocumentFragment();

    if (results.length === 0) {
        const clone = template.content.cloneNode(true);

        clone.querySelector(".hint-result").textContent = "No results";
        clone.querySelector(".hint-result").href = "#";

        fragment.append(clone);
    }
    
    results.forEach(hint => {
        const clone = template.content.cloneNode(true);

        clone.querySelector(".hint-result").textContent = truncateString(hint.title, 50);
        clone.querySelector(".hint-result").href = hint.url;

        fragment.append(clone);
    });

    hintsBox.append(fragment);
}

document.addEventListener("click", function(e) {
    const hintsBox = document.getElementById("hints");
    const searchInput = document.getElementById("search-input");

    if (!searchInput.contains(e.target) && !hintsBox.contains(e.target)) {
        hintsBox.style.display = "none";
    }
});