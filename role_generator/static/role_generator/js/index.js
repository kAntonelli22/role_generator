


let createButton = document.getElementById("create")
let joinButton = document.getElementById("join")
let input = document.getElementById("code")


createButton.onclick = function(){
    console.log("creating game room...")
}

joinButton.onclick = function(){
    console.log("verifying code length...")
    if (input.value.length == 4) {
        console.log("looking for game room...")
    } else{
        console.log("incomplete code! length is " + input.value.length)
    }
}