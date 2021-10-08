function Search(val) {
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
			searchRes.append(`
			
			 <div class="item-listing" onclick="window.location.href='/listing/${listing.id}'">
        <img src="/static/listing_images/${listing["id"]}/0.${listing["imageType"][0]}">
        <h3>${listing["title"]}</h3>
        <br>
        <p>$${parseInt(listing["price"]).toLocaleString()}</p>
      </div>
			`)
			
		}
	})
	


}