$(() => {
	let logged = $("#pfp").length != 0 

	if(logged) {
		var chatLength;
		fetch("/get-chat-length").then(res => res.json()).then((res) => {
			chatLength = res["res"]

			if(!localStorage.getItem("chatLength")){
				localStorage.setItem("chatLength",chatLength)
			}
			else {
				if(chatLength > localStorage.getItem("chatLength")){
					newChatNotiCircle()
				}
			}
		})

		
		

	}
})

function newChatNotiCircle() {
	$($(".navbar-links")[1]).append('<i id="unread-circle" class="fas fa-circle"></i>')
}

function switchLoginAndSignup(){
	$("#signup-login-container #login").toggle()
	$("#signup-login-container #signup").toggle()
}

function closeAuth(){
	$("#signup-login-container").fadeOut(200)
	$("#overlay").fadeOut(200);
}
function Overlay(){
	$("#overlay").show()
}
function ShowAuth(){
	Overlay()
	$("#signup-login-container #login").hide()
	$("#signup-login-container #signup").show()

	$("#signup-login-container").show()
}
function ShowLogin(){
	Overlay()
	$("#signup-login-container #login").show()
	$("#signup-login-container #signup").hide()

	$("#signup-login-container").show()
}