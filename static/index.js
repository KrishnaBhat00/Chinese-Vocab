document.getElementById("next").addEventListener("click", function () {
    console.log("next");
    flashcard();
});


async function flashcard() {
    let id = document.getElementById("id").textContent;
    let char = document.getElementById("char").textContent;
    let answer = document.getElementById("answer").textContent;
    let params = new FormData();
    params.append("id", id);
    params.append("char", char);
    params.append("answer", answer);

    fetch("/flashcard", { method: "POST", body: params })
        .then(statusCheck)
        .then(resp => resp.json())
        .then(function (resp) {
            console.log(resp);
            document.getElementById("id").innerHTML = resp["id"];
            document.getElementById("char").innerHTML = resp["char"];
            document.getElementById("answer").innerHTML = resp["answer"];
        })
}

async function statusCheck(resp) {
    if (!resp.ok) {
        throw new Error(await resp.text());
    }
    return resp;
}
