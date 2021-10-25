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
			loadMessages(targetName)
			for (let chat in tempChats) {
				if (chat.split("$").includes(targetName)) {
					if(tempChats[chat].length != chats[chat].length){
						messagesContainer[0].scrollTop = messagesContainer[0].scrollHeight;
						updateLSchatLength()
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
	if (selectedName == "" ||  !Object.keys(chats).map(e => e.split("$")).flat(1).includes(selectedName)){
		messagesContainer.append("<h4>Select contact to see messages.")	
		messageInput.hide()
		window.location.hash = ""
		
		return
	}
	
	window.location.hash = selectedName
	targetName = selectedName
	for(let chat in chats){
		if(chat.split("$").includes(selectedName)){
			for (let i = 0; i < chats[chat].length; i++) {
				const element = chats[chat][i];
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
				$(this).parent().css("background", "#373c53")
			}
		}).first().parent().css("background", "#494f6a")

		

}


function sendMessage(msg) {

	if(msg.trim() == "")return
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


