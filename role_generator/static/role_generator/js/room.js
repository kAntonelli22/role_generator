let editButton = document.getElementById("participant-edit")
let input = editButton.previousElementSibling
let username = input.previousElementSibling

let userlist = document.getElementById("box1")

editButton.onclick = function(){
    console.log("changing name...")
    if (input.style.display == 'block') {
        input.style.display = 'none'
    } else {
        input.style.display = 'block'
        input.value == username
    }
}


function update_participants(participant_data) {
    console.log("data: ", participant_data)
    console.log("participants: ")
    let html = ''
    for (let participant of participant_data) {
        console.log("\tname: " + participant.name)
        let hostHTML = participant.is_host ? '<span id="host">HOST</span>' : ''
        let editHTML = participant.is_user ? '<div id="participant-edit">Change Name</div>' : ''
        let participantHTML = `
        <div class=participant>
            <div class=participant-name>
                ${participant.name}
                ${hostHTML}
            </div>
            <input id="participant-input">
            ${editHTML}
        </div>`

        html += participantHTML
    }
    userlist.innerHTML = html
}

function pollServer() {
    console.log("polling server...")
    const url = "update_user/"

    fetch(url)
    .then(response => {
        if (!response.ok) {
            throw new Error('AJAX Polling failed')
        }
        return response.json()
    })
    .then(data => {
        update_participants(data.participants)
    })
    .catch(error => {
        console.error('AJAX Polling error: ', error)
    })
}

setInterval(pollServer, 3000)