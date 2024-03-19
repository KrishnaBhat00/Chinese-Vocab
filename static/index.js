document.getElementById("next").addEventListener("click", function () {
    console.log("next");
    flashcard();
});


async function flashcard() {
    let char = document.getElementById("char").textContent;
    let answer = document.getElementById("answer").textContent;
    let params = new FormData();
    params.append("char", char);
    params.append("answer", answer);

    fetch("/flashcard", { method: "POST", body: params })
        .then(statusCheck)
        .then(resp => resp.text())
        .then(function (resp) {
            console.log(resp);
            if (document.getElementById("char").innerHTML = resp);
        })
}

async function statusCheck(resp) {
    if (!resp.ok) {
        throw new Error(await resp.text());
    }
    return resp;
}
