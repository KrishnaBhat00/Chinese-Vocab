function addSuccessBttns(val) {
    var element = document.createElement("button")
    element.textContent = val;
    element.name = val;
    element.id = val;
    element.className = "btn";
    element.onclick = function () {
        flashcard(val)
    };
    var div = document.getElementById("success");
    div.appendChild(element);
}

function removeSuccessBttns() {
    var div = document.getElementById("success");
    while (div.firstChild) div.removeChild(div.firstChild);
}

document.getElementById("next").addEventListener("click", function () {
    console.log("next");
    flashcard(null);
});


async function flashcard(success) {
    let id = document.getElementById("id").textContent;
    let char = document.getElementById("char").textContent;
    let answer = document.getElementById("answer").textContent;
    let params = new FormData();
    params.append("id", id);
    params.append("char", char);
    params.append("answer", answer);
    params.append("success", success);

    fetch("/flashcard", { method: "POST", body: params })
        .then(statusCheck)
        .then(resp => resp.json())
        .then(function (resp) {
            console.log(resp);
            if (resp['answer'] != '') {
                addSuccessBttns("yes");
                addSuccessBttns("no");
            }
            else {
                removeSuccessBttns();
            }
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