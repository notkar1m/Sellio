var allFiles = []
$(() => {
    $("#clear-btn").hide()
	$("#clear-btn").click(() => {
        $("#result").html('') 
		document.getElementById("images-files").value = ''
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
                if(!file.type.match('image'))
                  continue;
                
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
        let price = $("#price").val()
        let radioNew = $("#new-radio")
        let condition = radioNew.is(":checked") ? "new" : "used"
        let formData = new FormData();
        let category = $("#category").val()




        if(!title || !description || !price || allFiles.length == 0 || category == "-"){
             iziToast.error({
              title: 'Error',
              message: 'Please fill out all the fields.',
          });
            return
        }
        formData.append("title", title)
        formData.append("description", description)
        formData.append("price", price)
        formData.append("condition", condition)
        formData.append("category", category)

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
		window.location.href ="/flash=Item%20Published!_url=listingSLASH" + id
        })

    }

    $("#publish-btn").click(Publish)    
})