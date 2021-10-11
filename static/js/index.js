var accName;
$(() => {
	 accName = $("#user-name").text().split(" ")[2]
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

				searchRes.append(`
				
				 <div class="item-listing" onclick="window.location.href='/listing/${listing.id}'">
		<img src="/static/listing_images/${listing["id"]}/0.${listing["imageType"][0]}">
		<h3>${listing["title"]}</h3>
		<br>
		<p>$${parseInt(listing["price"]).toLocaleString()}</p>
		<i class="far fa-trash-alt" onclick="DeleteListing('${listing.id}')"></i>
	      </div>
				`)
			}
			else {


				searchRes.append(`
				
				 <div class="item-listing" onclick="window.location.href='/listing/${listing.id}'">
		<img src="/static/listing_images/${listing["id"]}/0.${listing["imageType"][0]}">
		<h3>${listing["title"]}</h3>
		<br>
		<p>$${parseInt(listing["price"]).toLocaleString()}</p>
		<i class="far fa-heart" onclick="Fav(this, event)"></i>
	      </div>
				`)
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

				$("#search-res").append(`
	
				
				 <div class="item-listing" onclick="window.location.href='/listing/${listing.id}'">
		<img src="/static/listing_images/${listing["id"]}/0.${listing["imageType"][0]}">
		<h3>${listing["title"]}</h3>
		<br>
		<p>$${parseInt(listing["price"]).toLocaleString()}</p>
		<i class="far fa-trash-alt" onclick="DeleteListing('${listing.id}')"></i>
	      </div>
				`)
				
			}
			else {
				$("#search-res").append(`
	
				
				 <div class="item-listing" onclick="window.location.href='/listing/${listing.id}'">
		<img src="/static/listing_images/${listing["id"]}/0.${listing["imageType"][0]}">
		<h3>${listing["title"]}</h3>
		<br>
		<p>$${parseInt(listing["price"]).toLocaleString()}</p>
		<i class="far fa-heart" onclick="Fav(this, event)"></i>
	      </div>
				`)
			}
		});

		if($("#search-res div").length == 0){
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