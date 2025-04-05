function addSuccessBtns(val, endpoint) {
    var element = document.createElement("button")
    element.textContent = val;
    element.name = val;
    element.id = val;
    element.className = "btn";
    element.onclick = function () {
        flashcard(val, endpoint)
    };
    var div = document.getElementById("success");
    div.appendChild(element);
}

function removeSuccessBtns() {
    var div = document.getElementById("success");
    while (div.firstChild) div.removeChild(div.firstChild);
}

document.getElementById("next").addEventListener("click", function () {
    endpoint = window.location.href;
    endpoint = endpoint.split("/")[3];
    flashcard(null, endpoint);

});


async function flashcard(success, endpoint) {
    let id = document.getElementById("id").textContent;
    let file = document.getElementById("audio");
    let answer = document.getElementById("answer").textContent;
    let params = new FormData();
    let char = file.textContent;
    if (file.querySelector('audio')) {
        char = file.querySelector('audio').querySelector('source').getAttribute('src');
    }
    params.append("id", id);
    params.append("audio", char);
    params.append("answer", answer);
    params.append("success", success);

    fetch("/" + endpoint, { method: "POST", body: params })
        .then(statusCheck)
        .then(resp => resp.json())
        .then(function (resp) {
            console.log(resp);
            if (resp['answer'] != '') {
                addSuccessBtns("yes", endpoint);
                addSuccessBtns("no", endpoint);
            }
            else {
                removeSuccessBtns();
            }
            document.getElementById("id").innerHTML = resp["id"];
            document.getElementById("audio").innerHTML = `<audio controls> <source src="${resp["audio"]}" type="audio/mpeg"></audio>`;
            document.getElementById("answer").innerHTML = resp["answer"];
        })
}

async function statusCheck(resp) {
    if (!resp.ok) {
        throw new Error(await resp.text());
    }
    return resp;
}
