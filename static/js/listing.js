var images;
var currImage;
$(() => {
	$("#price").html("$" +parseInt($("#price").html()).toLocaleString())
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