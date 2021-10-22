$(() => {
	
})
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