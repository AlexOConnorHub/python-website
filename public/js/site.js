showPass = function() {
    if (option.value == "chat") {
        pass.classList.remove("hide");
    } else {
        pass.classList.add('hide');
    }
}

whyHere = async function() {
    if (option.value == "specialPage") {
        specialPage();
    } else if (option.value == "chat") {
        passPass();
    } else if (option.value == 'null') {
        alert("Please tell me why you are here")
    } else {
        // Stranger danger
    }
}

specialPage = async function() {
    if (validatePage('/special/' + uname.value.toLowerCase())) {
        url = "/html/special/" + uname.value.toLowerCase() + ".html";
        window.location.href = url;
    } else {
        alert("Is this really your name? (Try first name only)");
    }
}

validatePage = async function(path) {
    let resp = await fetch(path);
    if (resp.ok) {
        return true
    }
    return false
}

passPass = async function() {
    let temp = await fetch("/login", { method: "POST", body: JSON.stringify({ "pass": pass.value, "uname": uname.value }) })
        .then(res => res.json()).then();
    console.log(temp);
    if (temp.state == true) {
        localStorage.validSession = temp.cookie;
        localStorage.uname = uname.value;
        url = "/html/chat/chat.html";
        window.location.href = url;
    } else if (temp.state == false) {
        alert('Wrong password');
    } else {
        url = "/html/chat/signup.html";
        window.location.href = url;
    }
}

sendChat = async function() {
    if (userMessage.value != "") {
        let temp = await fetch("/chat/message", {
                method: "POST",
                body: JSON.stringify({ "sender": localStorage.uname, "message": userMessage.value, "cookie": localStorage.validSession })
            })
            .then(res => res.json()).then();
        userMessage.value = "";
    }
}

getChat = async function(id) {
    return await fetch("/chat/" + id.toString(), {
        method: "POST",
        body: JSON.stringify({ "cookie": localStorage.validSession, "uname": localStorage.uname })
    }).then(res => res.json()).then();
}

manageChats = async function() {
    for ([id, fetched] of Object.entries(chats)) {
        let local = [];
        if (!fetched) {
            let message = await getChat(id);
            if (message['state'] != true) {
                // failed
            } else {
                local.push(id);
                let newChat = document.getElementById("template").cloneNode(true);
                newChat.classList.remove('hide');
                if (message['sender'] == localStorage.uname) {
                    newChat.classList.add('darker');
                    newChat.childNodes[1].classList.add('right');
                    newChat.childNodes[7].classList.remove('time-right');
                    newChat.childNodes[7].classList.add('time-left');
                }
                let imgPath = '/images/profile/';
                let exts = ['.png', '.jpg', '.jpeg'];
                for (ext of exts) {
                    if (await validatePage(imgPath + message['sender'] + ext)) {
                        imgPath += message['sender'] + ext;
                        break;
                    }
                }
                if ('/images/profile/' == imgPath) {
                    imgPath += message['sender'].slice(0, 1).toLowerCase() + '.png';
                }
                newChat.childNodes[1].src = imgPath;
                newChat.childNodes[3].innerText = message['sender'] + ': ';
                newChat.childNodes[4].innerText = message['message'];
                let date = new Date(message['time']).toString()
                newChat.childNodes[7].innerText = date.slice(3, 21);
                chat.insertBefore(newChat, chat.childNodes[0]);
            }
        }
        for (id of local) {
            chats[id] = true;
        }
    }
}

loadPage = async function() {
    let chat = await fetch("/chat/onload", { method: "POST", }).then(res => res.json()).then();
    console.log(chat);
    for (id in chat) {
        chats[chat[id]] = false;
    }
    manageChats()
}

autoFill = async function() {
    cookie.value = localStorage.validSession;
    uname.value = localStorage.uname;
    unameP.value = localStorage.uname;

    let imgPath = '/images/profile/';
    let exts = ['.png', '.jpg', '.jpeg'];
    for (ext of exts) {
        if (await validatePage(imgPath + localStorage.uname + ext)) {
            imgPath += localStorage.uname + ext;
            break;
        }
    }
    if ('/images/profile/' == imgPath) {
        imgPath += localStorage.uname.slice(0, 1).toLowerCase() + '.png';
    }
    usrImage.src = imgPath;
}

fileSize = function(fileInput) {
    if (fileInput.files[0].size > 500000) {
        alert("This file is too big! Please keep it smaller than about half a MB");
        fileInput.value = "";
    }
}