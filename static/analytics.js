let table = document.getElementById("table")

fetch("/analytics", { method: "POST", body: {} })
    .then(statusCheck)
    .then(resp => resp.json())
    .then(function (resp) {
        console.log(resp)
        console.log(resp['rows'].length)
        for (let i = 0; i < resp['rows'].length; i++) {
            console.log(table.length)
            var row = table.insertRow();
            var idCell = row.insertCell(0);
            idCell.innerHTML = resp['rows'][i]['ID'];
            var charCell = row.insertCell(1);
            charCell.innerHTML = resp['rows'][i]['Char'];
            var pyCell = row.insertCell(2);
            pyCell.innerHTML = resp['rows'][i]['PinYin'];
            var defCell = row.insertCell(3);
            defCell.innerHTML = resp['rows'][i]['Definition'];
            var appCell = row.insertCell(4);
            appCell.innerHTML = resp['rows'][i]['Appearances'];
            var correctCell = row.insertCell(5);
            correctCell.innerHTML = resp['rows'][i]['Correct'];
        }
    })

async function statusCheck(resp) {
    if (!resp.ok) {
        throw new Error(await resp.text());
    }
    return resp;
}
