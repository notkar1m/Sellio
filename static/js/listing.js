var images;
var currImage;
$(() => {
	$("#price").html("$" +parseInt($("#price").html()).toLocaleString())
	$(".listing-images:first").show()

	
	 images = $("#item-imgs img")
	 currImage = 0;
	
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