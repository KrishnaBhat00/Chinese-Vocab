function addSuccessBttns(val, endpoint) {
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

function removeSuccessBttns() {
    var div = document.getElementById("success");
    while (div.firstChild) div.removeChild(div.firstChild);
}

document.getElementById("next").addEventListener("click", function () {
    endpoint = window.location.pathname.substring(1);
    // endpoint = endpoint.split("/")[3];
    flashcard(null, endpoint);

});


async function flashcard(success, endpoint) {
    let id = document.getElementById("id").textContent;
    let char = document.getElementById("char").textContent;
    let answer = document.getElementById("answer").textContent;
    let params = new FormData();
    params.append("id", id);
    params.append("char", char);
    params.append("answer", answer);
    params.append("success", success);

    fetch("/" + endpoint, { method: "POST", body: params })
        .then(statusCheck)
        .then(resp => resp.json())
        .then(function (resp) {
            console.log(resp);
            if (resp['answer'] != '') {
                addSuccessBttns("yes", endpoint);
                addSuccessBttns("no", endpoint);
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
