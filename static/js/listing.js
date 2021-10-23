var images;
var currImage;
$(() => {
	fetch("https://gist.githubusercontent.com/Fluidbyte/2973986/raw/5fda5e87189b066e11c1bf80bbfbecb556cf2cc1/Common-Currency.json").then(res => res.json()).then(res => {
		$("#price").html( res[currencyCode]["symbol"] + " " + parseInt($("#price").html()).toLocaleString())
	})
	$(".listing-images:first").show()
	$("#date").html(moment($("#date").html(),"YYYY/M/D/hh:mma").fromNow())
	
	 images = $("#item-imgs img")
	 currImage = 0;


	 if(images.length == 1){
		 $(".fa-chevron-circle-right").css({
			 "pointer-events": "none",
			 "opacity": 0.5
		 })	
		  $(".fa-chevron-circle-left").css({
			 "pointer-events": "none",
			 "opacity": 0.5
		 })
	 }


	 fetch("/get-my-favs").then((res) => {return res.json()}).then((data) =>{
		 data = data["res"]
		 if(data.includes($(".listing-images")[0].src.split("/")[5])) {
			 Fav($(".fa-heart")[0], undefined, true)
		 }
		 
	 })
	

})

	function switchImageLeft() {
		if(currImage > 0){
			currImage -=1
		}
		else{
			currImage = images.length -1
		}

		$(images[currImage]).show()
		for (let i = 0; i < images.length; i++) {
			const element = images[i];
			if(i == currImage)continue;
			$(element).hide()
			
		}

		
		
		
	}

	function switchImageRight(){
		if(currImage < images.length-1){
			currImage += 1
		}
		else {
			currImage = 0
		}
		$(images[currImage]).show()
		for (let i = 0; i < images.length; i++) {
			const element = images[i];
			if(i == currImage)continue;
			$(element).hide()
			
		}

		console.log(currImage);

	}

function Fav(ele, event, noFetch){
	if(event)event.stopPropagation();
	let parent = ele.parentElement;
	$(ele).removeClass("far")
	$(ele).addClass("fas")
	$(ele).attr("onclick", "UnFav(this, event)")
	if(noFetch){
		return

	}
	fetch("/add-to-fav_listingId=" + $(".listing-images")[0].src.split("/")[5]).then((res)=>{return res.json()}).then(
		(res)=>{
			console.log(res["res"]);
		}
		)

}


function UnFav(ele, event, noFetch){
	if(event)event.stopPropagation()
	let parent = ele.parentElement;
	$(ele).removeClass("fas")
	$(ele).addClass("far")
	$(ele).attr("onclick", "Fav(this, event)")
	if(noFetch)return
	fetch("/remove-from-fav_listingId=" + $(".listing-images")[0].src.split("/")[5]).then((res)=>{return res.json()}).then(
		(res)=>{
			console.log(res["res"]);
		}
		)


}


function DeleteListing(id){
	fetch("/remove-listing_id=" +id).then((res)=>{return res.json()}).then((res) => {
		res = res["res"]
		if (res == "success"){
			window.location.pathname = "/flash=Item Deleted!_url=userSLASH" +$("#user-name").text().split(" ")[2]
		}
		else {
			  iziToast.error({
              title: 'Error deleting item',
              message: res,
          });
		}
	})
	console.log("sdfsdf")

}


function Share() {
	$("#signup-login-container").html(`
	<input style="width: 90%;
    margin-left: 6px;font-size:15px" readonly value="Hey, check out this listing on Sellio: ${window.location.href}"/>
    <button onclick="$('#signup-login-container input')[0].select();document.execCommand('copy');iziToast.success({title:'Copied!'})"style="font-size: 30px;
    margin-top: 38px;
    padding: 30px;">Copy</button>
    <p style="text-align: center;
    text-decoration: none;
    margin-top: 20px;
    opacity: 1 !important;
    cursor: initial;">Share this link to let people know about your listing!</p>
	`)
	ShowAuth()
	$("#signup-login-container input")[0].select()
	document.execCommand('copy');
	iziToast.success({title: "Copied!"})
}



function ShowReport(){
		$("#signup-login-container").html(`

		<center><h3>Report Listing</h3></center>
		<br>
	<input id="report-reason" style="width: 90%;
    margin-left: 6px;font-size:15px" placeholder="Reason"/>

    <br>
    <br>
    <textarea  id="report-more-info" style="width: 280px;font-size: 22px;font-family: 'Poppins', sans-serif;padding: 9px;border: none;border-radius: 13px;box-shadow: 0 0 15px -4px #00000047;
    outline: none;resize:none;height:170px" placeholder="More information"></textarea>




    <button onclick="SendReport()" style="font-size: 18px;
    margin-top: 38px;">Send Report</button>



    <p style="text-align: center;
    text-decoration: none;
    margin-top: 20px;
    opacity: 1 !important;
    cursor: initial;">Report a listing if you think it has something wrong and we'll review your report.</p>
	`)
	ShowAuth()
}



function SendReport(){
	let reason = $("#report-reason").val();
	let moreInfo = $("#report-more-info").val();

	if(reason.length == 0 || moreInfo.length == 0){
		iziToast.error({
			title: "Error",
			message: "Please fill out all the fields."
		})
		return
	}
	let formData = new FormData();
	formData.append("reason", reason);
	formData.append("moreInfo", moreInfo);
	formData.append("listingId", listingId)

	fetch("/send-report", {
		method: "POST",
		body: formData,
	}).then((response) => response.text()).then((res) => {
		closeAuth();
		if (res == "success"){
			 iziToast.success({
				title: 'Success',
				message: "Report sent successfully!",
			});
		}
		else{
		iziToast.error({
			title: 'Error',
			message: "Error sending report!",
		});
		}
	})
}