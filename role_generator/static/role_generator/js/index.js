let createButton = document.getElementById("create")
let joinInput = document.getElementById("join")


createButton.onclick = function(){
    console.log("creating game room...")
    window.location.href = '/create_room/'
}

joinInput.addEventListener("input", function(){
    console.log("checking join code length...")
    if (joinInput.value.length == 4) {
        console.log("looking for game room...")
        let valid_code = joinRoom(joinInput.value)
        if (valid_code) { console.log("code is valid!") } else { console.log("code is invalid!") }
    } else{
        console.log(joinInput.value.length, " is too short to be a code")
    }
})

function joinRoom(roomCode) {
    console.log("roomcode: " + roomCode.toUpperCase())

    const formData = new FormData()
    formData.append('room_code', roomCode.toUpperCase())

    const url = '/join_room/'

    fetch(url, {
        method: 'POST',
        credentials: 'same-origin',
        headers:{ 'X-CSRFToken': csrftoken },
        body: formData
    })
    .then(response => {
        if (!response.ok) { throw new Error(`HTTP error! status: ${response.status}`) }
        return response.json()
    })
    .then(data => {
        if (data.success) {
            window.location.href = data.redirect_url
        } else {
            console.error(data.error)
        }
    })
}