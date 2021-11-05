var allFiles = []
$(() => {
    function getCookie(name) {
        var nameEQ = name + "=";
        var ca = document.cookie.split(';');
        for(var i=0;i < ca.length;i++) {
            var c = ca[i];
            while (c.charAt(0)==' ') c = c.substring(1,c.length);
            if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
        }
        return null;
    }

    if(getCookie("inviteFriendPopUp") == "false"){
        $("#friend-invite").hide()
    }


    $("#clear-btn").hide()
	$("#clear-btn").click(() => {
        $("#result").html('') 
		document.getElementById("images-files").value = ''
        allFiles = []
		$("#plus-div").css("opacity",1)
        $("#plus-div").css("pointer-events","all")
        $("#images-files").removeAttr("disabled")
		$("#clear-btn").hide()
        
	})
	 if(window.File && window.FileList && window.FileReader)
    {
        var filesInput = document.getElementById("images-files");
        
        filesInput.addEventListener("change", function(event){
            
            var files = event.target.files; //FileList object
            var output = document.getElementById("result");
            
            for(var i = 0; i< files.length; i++)
            {
                var file = files[i];
                //Only pics
                if(!file.type.match('image')){
                    iziToast.error({title: "Error", message:"Only image files allowed!"})
                    return
                }
                
                var picReader = new FileReader();
                
                picReader.addEventListener("load",function(event){
                    
                    var picFile = event.target;
                    
                    var div = document.createElement("div");
                    
                    div.innerHTML = "<img class='thumbnail' src='" + picFile.result + "'" +
                            "title='" + picFile.name + "'/>";
                    
                    output.insertBefore(div,null);            
		$("#clear-btn").fadeIn()
		    if($("#result").children().length == 3){
				$("#plus-div").css("opacity",0.5)
				$("#plus-div").css("pointer-events","none")
				$("#images-files").attr("disabled", "disabled");
		    }
                
                });
                
                 //Read the image
                picReader.readAsDataURL(file);

                allFiles.push(file)
                console.log(allFiles)
            }                               
           
        });
    }
    else
    {
        alert("Your browser does not support File API");
    }





    function Publish(){
        let title = $("#title").val()
        let description = $("#description").val()
        let price = $("#price").val() == "" ? 0 : $("#price").val()
        let radioNew = $("#new-radio")
        let condition = radioNew.is(":checked") ? "new" : "used"
        let formData = new FormData();
        let category = $("#category").val()
        function format(date) {
            var hours = date.getHours();
            var minutes = date.getMinutes();
            var ampm = hours >= 12 ? 'PM' : 'AM';
            hours = hours % 12;
            hours = hours ? hours : 12; // the hour '0' should be '12'
            minutes = minutes < 10 ? '0'+minutes : minutes;
            var strTime = hours + ':' + minutes + ampm;
            return strTime;
        }

    time = format(new Date)
    d = new Date()
    date = `${d.getFullYear()}/${d.getMonth() + 1}/${d.getDate()}/${time}`




        if(!title || !description || !price || allFiles.length == 0 || category == "-"){
             iziToast.error({
              title: 'Error',
              message: 'Please fill out all the fields.',
          });
            return
        }

        if(title > 45){
            iziToast.error({
                title: "Title too long",
                message: "Max is 45 characters."
            })
            return
        }
        if(description > 300){
            iziToast.error({
                title: "Description too long",
                message: "Max is 300 characters."
            })
            return
        }

        if(parseInt(price) < 1 || parseInt(price) > 100000){
             iziToast.error({
              title: 'Error',
              message: `Min price is ${currency} 1 and the max is ${currency} 100,000`
          });
            return
        }

        formData.append("title", title)
        formData.append("description", description)
        formData.append("price", price)
        formData.append("condition", condition)
        formData.append("category", category)
        formData.append("date", date)

		for (let i = 0; i < allFiles.length; i++) {
            const currFile = allFiles[i];
            formData.append(`image${i+1}`, currFile)
            
        }
        // formData.append("image", $("#images-files")[0].files[0])
        // formData.append("images", $("#images-files").prop("files"))

        fetch("/add-listing", {
            method: "POST",
            body: formData
        }).then((response) => {
            return response.text()
        }).then((id) =>{
		window.location.href ="/flash=Item Published!_url=listingSLASH" + id
        })

    }

    $("#publish-btn").click(Publish)    
})


function InviteFriends() {

    $("#signup-login-container").html(`
        <center><h3>Invite Friends</h3></center>

        <input style="font-size:12px;margin-left:-10px;margin-top:21px" readonly value="Hey, check out this website! You can sell your old PC parts and buy new ones. https://sell-io.com"></input>

        <button onclick="$('#signup-login-container input')[0].select();document.execCommand('copy');DontShowFriendInvite();iziToast.success({title:'Copied!'})" style="font-size:19px;margin-top:30px">Copy</button>
        <p style="    opacity: 1 !important;
    text-decoration: none;
    cursor: initial;
    font-size: 14px;
    margin-top: 20px;
    text-align: center;">Send this to all of your friends and the more friends you invite, the more popularity you listing is going to gain.</p>
    `)
    	$("#signup-login-container input")[0].select()
	document.execCommand('copy');
	iziToast.success({title: "Copied!"})

    ShowAuth()
    

}


function DontShowFriendInvite() {
    //This adds a cookie to make it not show the popup for 2 weeks and when the cookie expires it shows it again
    var today = new Date();
    var expire = new Date();
    var cookieName = "inviteFriendPopUp"
    var cookieValue = "false"
    expire.setTime(today.getTime() + 3600000*24*14);
    document.cookie = cookieName+"="+encodeURI(cookieValue) + ";expires="+expire.toGMTString();
}