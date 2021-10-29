var targetName;
var messagesContainer;
var messageInput;

$(() => {

	updateLSchatLength()
	 targetName = window.location.hash.slice(1)
	messagesContainer = $("#messages-container")
	messageInput = $("#send-message-container")
	loadMessages(targetName)
	
	setInterval(() => {
		fetch("/get-my-messages").then((res) => {return res.json()}).then((res) => {
			let tempChats = chats
			chats = res
			for (let j=0;j<tempChats.length;j++) {
				chat = tempChats[j]
				if (chat.users.includes(targetName)) {
					for (let i = 0; i < chats.length;i++){
						let element = chats[i]
						if (element.users.toString() == chat.users.toString()){
							if(chat.chat.length != chats[j].chat.length){
								messagesContainer[0].scrollTop = messagesContainer[0].scrollHeight;
								updateLSchatLength()
								loadMessages(targetName)
							}
						}
					}
				}
				
			}
		})
	},3000)

	$("#message-input")[0].addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
	sendMessage($("#message-input").val())
    }
})


	messagesContainer[0].scrollTop = messagesContainer[0].scrollHeight;


	setTimeout(()=> {
		messagesContainer[0].scrollTop = messagesContainer[0].scrollHeight;
		if(!$(".navbar-links")[1].getElementsByTagName("i")[0])return
		$(".navbar-links")[1].getElementsByTagName("i")[0].remove()
	}, 1000)
})


function updateLSchatLength(){
	fetch("/get-chat-length").then(res => res.json()).then((res) => {
		chatLength = res["res"]
		localStorage.setItem("chatLength",chatLength)
	})
}

function sanitizeString(str){
    str = str.replace(/[^a-z0-9áéíóúñü \.,_-]/gim,"");
    return str.trim();
}
	
function loadMessages(selectedName) {
	$("#messages-container").html("")
	
	if($("#mobile-user-div h3").text() != selectedName){
		$("#mobile-user-div h3").text(selectedName)
	}
	messageInput.show()
	if (selectedName == "" ||  !chats.map(e => e.users).flat(1).includes(selectedName)){
		messagesContainer.append("<h4>Select contact to see messages.")	
		messageInput.hide()
		window.location.hash = ""
		
		return
	}
	
	window.location.hash = selectedName
	targetName = selectedName
	for(let i = 0; i < chats.length; i++){
		chat = chats[i]
		if(chat.users.includes(selectedName)){
			for (let j = 0; j < chat.chat.length; j++) {
				const element = chats[i].chat[j];
				if(element[0] == accName){
					messagesContainer.append('<div class="message-me"><p>' + sanitizeString(element[1]) + '</p></div>')
				}
				else{
					messagesContainer.append('<div class="message-other"><p>' + sanitizeString(element[1]) + '</p></div>')
				}
				
			}
			

		}
	}


		messagesContainer[0].scrollTop = messagesContainer[0].scrollHeight;


		$(".contact h3").filter( function (){
			let r = $( this ).text().toLowerCase() == selectedName
			if (r) return r
			else{
				$(this).parent().css("background", "#494f6a")
			}
		}).first().parent().css("background", "#373c53")

		

}


function sendMessage(msg) {
	
	if(msg.trim() == "")return
	if(msg.length > 2000){
		iziToast.error({
			title: "Message is too long!"
		})
		return
	}
	$("#message-input").val("")
	let formData = new FormData();
	formData.append("message", msg);

	fetch("/send-message_user=" + targetName, {
		method: "POST",
		body: formData
	}).then(() => {

		fetch("/get-my-messages").then((res) => {return res.json()}).then((res) => {
				
				chats = res
				console.log(chats)
				loadMessages(targetName)
				messagesContainer[0].scrollTop = messagesContainer[0].scrollHeight;
				updateLSchatLength()
				
			})
	})

	
}


function ShowMobileContacts() {
	
	$("#contact-list").toggle()
	document.addEventListener('mouseup', function(event) {
		var isClickInsideElement = $("#contact-list")[0].contains(event.target);
		if (!isClickInsideElement) {
			$("#contact-list").hide()
		}
	});
}

function NewChat() {
	$("#signup-login-container").html(`
		<center><h3>New Chat</h3></center>
		<br>
		<input style="width:241px" type="search" placeholder="Search users"/> <button onclick="SearchUsers()" style="width: 50px;position: relative;left: 130px;top: -49px;font-size: 20px;padding: 23px;" > <i class="fa fa-search" ></i></button>
		<div style="margin-top:20px" id="new-chat-users"></div>
	`)
	$("#signup-login-container input").first().keydown(function (event) {
		if (event.key === "Enter"){
			SearchUsers()
			
		}
	
	})
	ShowAuth()
}



function SearchUsers(){
	var value = $("#signup-login-container input").first().val()
	$("#new-chat-users").html("")
	if(value.trim() == ""){
		$("#new-chat-users").html("")
		return
	}
	fetch("/search-users_q=" + value).then(res => res.json()).then((res) => {
		res = res['res']
		console.log(res)
		for (let i = 0; i < res.length; i++) {
			const user = res[i];
			if(user == accName || chats.map(e=>e.users).flat(1).includes(user))continue
			$("#new-chat-users").append(`
			<div class="contact" style="border-radius:10px" onclick="window.location.href = '/add-user-to-chat_user=${user}'"> 
				<img onclick="window.location.href = '/user/${user}'" src="static/pfps/${user}.jpg" onerror="if (this.src != 'https://api-private.atlassian.com/users/aa7543e682dff486562017fe2fedc6c0/avatar') this.src = 'https://api-private.atlassian.com/users/aa7543e682dff486562017fe2fedc6c0/avatar';">
				<h3 style="margin-left:0">${user}</h3></div>
			
			`)
			
			
			
		}
	})
}

