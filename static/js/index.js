var accName;
$(() => {
	 accName = $("#user-name").text().split(" ")[2]
	$("#mobile-nav").hide()
	 for (var i = 0; i < $("#latest-listings-res div").length;i++)	{
			const listing = $("#latest-listings-res div")[i]
			fetch("/get-my-favs").then((response) => {
					       return response.json()
				       }).then((response) => {
					       response = response["res"]
					       if(response.includes(listing.getElementsByTagName("img")[0].src.split("/")[5])){
						       Fav(listing.getElementsByTagName("i")[0], undefined, true)
					       }
				       })

	 }


	 for (let i = 0; i < $(".latest-listings-listing-price").length; i++) {
		 	fetch("https://gist.githubusercontent.com/Fluidbyte/2973986/raw/5fda5e87189b066e11c1bf80bbfbecb556cf2cc1/Common-Currency.json").then(res => res.json()).then(res => {
				 const element = $(".latest-listings-listing-price")[i];
				 let currencyCode = $(element).text().split(" ")[0]
				 let priceNum = $(element).text().split(" ")[1]
				 $(element).text(res[currencyCode]["symbol"] + " " + parseInt(priceNum).toLocaleString())
				 
		})
		 
	 }
})
function Search(val) {
	$("#search-res h2").remove()
	if(val == ""){
		
		$("#search-res").html("<h3 style=\"font-size: 40px;top:-77px;font-weight: 300;position: absolute;left: 9%;\">Search results</h3>")
		$("#search-res").hide()
		$(".component-selection").show();
		return
	}

	let searchRes = $("#search-res")

	searchRes.show();
	$(".component-selection").hide()

	let formData = new FormData();
	formData.append("text", val)
	fetch("/search", {
		method: "POST",
		body: formData,
	}).then((response) => {
		return response.json()
	}).then((res) => {
		res = res["res"]
		$("#search-res").html("<h3 style=\"font-size: 40px;top:-77px;font-weight: 300;position: absolute;left: 9%;\">Search results</h3>")
		if(res.length == 0) {
			searchRes.append("<span style=\"font-size:30px;margin-top:69px;\">No results found. </span>")
			return
		}
		for (let i = 0; i <res.length; i++) {
			const listing = res[i];
			if(listing.owner == accName){

		fetch("https://gist.githubusercontent.com/Fluidbyte/2973986/raw/5fda5e87189b066e11c1bf80bbfbecb556cf2cc1/Common-Currency.json").then(res => res.json()).then(res => {

			searchRes.append(`
			
			 <div class="item-listing" onclick="window.location.href='/listing/${listing.id}'">
	<img src="/static/listing_images/${listing["id"]}/0.${listing["imageType"][0]}">
	<h3>${listing["title"]}</h3>
	<br>
		<p>${res[listing.currency]["symbol"] + " " +parseInt(listing["price"]).toLocaleString()}</p>
	<i class="far fa-trash-alt" onclick="DeleteListing('${listing.id}', event)"></i>
      </div>
			`)
			})

			}
			else {

				if(logged){

		fetch("https://gist.githubusercontent.com/Fluidbyte/2973986/raw/5fda5e87189b066e11c1bf80bbfbecb556cf2cc1/Common-Currency.json").then(res => res.json()).then(res => {

			searchRes.append(`
			
			 <div class="item-listing" onclick="window.location.href='/listing/${listing.id}'">
	<img src="/static/listing_images/${listing["id"]}/0.${listing["imageType"][0]}">
	<h3>${listing["title"]}</h3>
	<br>
			<p>${res[listing.currency]["symbol"] + " " +parseInt(listing["price"]).toLocaleString()}</p>
	<i class="far fa-heart" onclick="Fav(this, event)"></i>
      </div>
			`)
				})

				}
				else{

		fetch("https://gist.githubusercontent.com/Fluidbyte/2973986/raw/5fda5e87189b066e11c1bf80bbfbecb556cf2cc1/Common-Currency.json").then(res => res.json()).then(res => {
			searchRes.append(`
			
			 <div class="item-listing" onclick="window.location.href='/listing/${listing.id}'">
	<img src="/static/listing_images/${listing["id"]}/0.${listing["imageType"][0]}">
	<h3>${listing["title"]}</h3>
	<br>
		<p>${res[listing.currency]["symbol"] + " " +parseInt(listing["price"]).toLocaleString()}</p>
      </div>
			`)
				})
				}
			}
			
			fetch("/get-my-favs").then((response) => {
				return response.json()
			}).then((response) => {
				response = response["res"]
				if(response.includes(listing["id"])){
					Fav($(".item-listing")[i].getElementsByTagName("i")[0], undefined, true)
				}
			})
			
		}
	})
	


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
	if(!parent.getElementsByTagName("img")[0]){
			fetch("/add-to-fav_listingId=" + $(".listing-images")[0].src.split("/")[5]).then((res)=>{return res.json()}).then(
		(res)=>{
			console.log(res["res"]);
		}
		)
		return
	}
	fetch("/add-to-fav_listingId=" + parent.getElementsByTagName("img")[0].src.split("/")[5]).then((res)=>{return res.json()}).then(
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
	if(!parent.getElementsByTagName("img")[0]){
		fetch("/remove-from-fav_listingId=" + $(".listing-images")[0].src.split("/")[5]).then((res)=>{return res.json()}).then(
		(res)=>{
			console.log(res["res"]);
		}
		)
		return
	}
	fetch("/remove-from-fav_listingId=" + parent.getElementsByTagName("img")[0].src.split("/")[5]).then((res)=>{return res.json()}).then(
		(res)=>{
			console.log(res["res"]);
		}
		)


}



function chooseCategory(category){
	$("#search-res").show()
	$("#search-res div").remove()
	$("#search-res h3").remove()
	$("#search-res span").remove()
	$("#search-res").prepend(`<h3 style="font-size: 40px;top:-77px;font-weight: 300;position: absolute;left: 9%;"><i class="fas fa-arrow-left" onclick="BackFromCategory()"></i> ${category}</h3>`)
	$("#search-res h2").html(category)
	fetch("/search-with-category_cat=" + category).then((response) => {return response.json()}).then((data) => {
		data = data["res"]

		data.forEach(listing => {
			if(listing.owner == accName){
				fetch("https://gist.githubusercontent.com/Fluidbyte/2973986/raw/5fda5e87189b066e11c1bf80bbfbecb556cf2cc1/Common-Currency.json").then(res => res.json()).then(res => {
						$("#search-res").append(`
			
						
						 <div class="item-listing" onclick="window.location.href='/listing/${listing.id}'">
				<img src="/static/listing_images/${listing["id"]}/0.${listing["imageType"][0]}">
				<h3>${listing["title"]}</h3>
				<br>
				<p>${res[listing.currency]["symbol"] + " " +parseInt(listing["price"]).toLocaleString()}</p>
				<i class="far fa-trash-alt" onclick="DeleteListing('${listing.id}', event)"></i>
			      </div>
						`)
			})

				
			}
			else {
				
				if(logged){

				fetch("https://gist.githubusercontent.com/Fluidbyte/2973986/raw/5fda5e87189b066e11c1bf80bbfbecb556cf2cc1/Common-Currency.json").then(res => res.json()).then(res => {
					$("#search-res").append(`
		
					
					 <div class="item-listing" onclick="window.location.href='/listing/${listing.id}'">
			<img src="/static/listing_images/${listing["id"]}/0.${listing["imageType"][0]}">
			<h3>${listing["title"]}</h3>
			<br>
			<p>${res[listing.currency]["symbol"] + " " +parseInt(listing["price"]).toLocaleString()}</p>
			<i class="far fa-heart" onclick="Fav(this, event)"></i>
		      </div>
					`)
				})

				}
				else{
						fetch("https://gist.githubusercontent.com/Fluidbyte/2973986/raw/5fda5e87189b066e11c1bf80bbfbecb556cf2cc1/Common-Currency.json").then(res => res.json()).then(res => {
							$("#search-res").append(`
				
							
								<div class="item-listing" onclick="window.location.href='/listing/${listing.id}'">
					<img src="/static/listing_images/${listing["id"]}/0.${listing["imageType"][0]}">
					<h3>${listing["title"]}</h3>
					<br>
					<p>${res[listing.currency]["symbol"] + " " +parseInt(listing["price"]).toLocaleString()}</p>
					</div>
							`)
						})

				}
			}
		});
		// setTimeout(() => {
		// 	if($("#search-res div").length == 0){
		// 		$("#search-res").append("<span style=\"font-size:30px;margin-top:69px;\">No results found. </span>")
		// 	}
		// }, 600)
			if(data.length == 0){
				$("#search-res").append("<span style=\"font-size:30px;margin-top:69px;\">No results found. </span>")
			}
	})


}


function BackFromCategory() {
	$("#search-res").hide()
	$(".component-selection").show()
}
$(() => {
	$(".component").toArray().forEach(element => {
		let categoryName = element.getElementsByTagName("span")[0].innerText
		element.onclick = () => {
			$(".component-selection").hide()
			chooseCategory(categoryName)

		}
		
	});
})



function DeleteListing(id, event){
	if(event)event.stopPropagation();
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

}


function BringUpMobileNavBar() {
	$("#mobile-nav").fadeIn();
	$(document).mouseup(function(e) 
	{
	var container = $("#mobile-nav");
	// if the target of the click isn't the container nor a descendant of the container
	if (!container.is(e.target) && container.has(e.target).length === 0) 
	{
		container.fadeOut();
		$('#user-opts').hide()
	}
	});
		
}



function ContactUs() {
	$("#signup-login-container").html(`

		<center><h3>Contact us</h3></center>
		<br>
	
    <br>
    <textarea  id="contact-us-message" style="width: 280px;font-size: 22px;font-family: 'Poppins', sans-serif;padding: 9px;border: none;border-radius: 13px;box-shadow: 0 0 15px -4px #00000047;
    outline: none;resize:none;height:170px" placeholder="Message"></textarea>




    <button onclick="SendFromContactUs()" style="font-size: 18px;
    margin-top: 38px;">Send</button>



    <p style="text-align: center;
    text-decoration: none;
    margin-top: 20px;
    opacity: 1 !important;
    cursor: initial;">Give us feedback, give us a suggestion, advice, tell us anything! </p>
	`)
	ShowAuth()
}


function SendFromContactUs() {
	let message = $("#contact-us-message").val()
	let formData = new FormData()
	formData.append("message", message)
	formData.append("username", accName)

	fetch("https://sellio-feedback.karimk123.repl.co/", { 
		method: "POST",
		body:formData,
		mode: "no-cors"
	}).then(() => {
		iziToast.success({
			title:"We received your message and will get back to you soon!"
		})
		closeAuth()
	})
}