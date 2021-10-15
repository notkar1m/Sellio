var targetName;
var messagesContainer;
var messageInput;

$(() => {

	 targetName = window.location.hash.slice(1)
	messagesContainer = $("#messages-container")
	messageInput = $("#send-message-container")
	loadMessages(targetName)

	setInterval(() => {
		fetch("/get-my-messages").then((res) => {return res.json()}).then((res) => {
			let tempChats = chats
			chats = res
			loadMessages(targetName)
			if(tempChats[targetName].length != chats[targetName].length){
				messagesContainer[0].scrollTop = messagesContainer[0].scrollHeight;
			}
		})
	},3000)

	$("#message-input")[0].addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
	sendMessage($("#message-input").val())
    }
})


	messagesContainer[0].scrollTop = messagesContainer[0].scrollHeight;
})


function sanitizeString(str){
    str = str.replace(/[^a-z0-9áéíóúñü \.,_-]/gim,"");
    return str.trim();
}
	
function loadMessages(selectedName) {
	$("#messages-container").html("")
	

	messageInput.show()
	if (selectedName == "" || selectedName in chats == false){
		messagesContainer.append("<h4>Select contact to see messages.")	
		messageInput.hide()
		window.location.hash = ""
		
		return
	}
	
	window.location.hash = selectedName
	targetName = selectedName
	for (let i = 0; i < chats[selectedName].length; i++) {
		const element = chats[selectedName][i];
		if(element[0] == accName){
			messagesContainer.append('<div class="message-me"><p>' + sanitizeString(element[1]) + '</p></div>')
		}
		else{
			messagesContainer.append('<div class="message-other"><p>' + sanitizeString(element[1]) + '</p></div>')
		}
		
	}

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
				loadMessages(targetName)
				messagesContainer[0].scrollTop = messagesContainer[0].scrollHeight;
				
			})
	})

	
}


