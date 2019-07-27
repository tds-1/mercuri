// Check Off Specific Todos By Clicking
// $(".dropbtn").on("click", function(){
// 	$("#formul").toggleClass("dropdown");
// });

$(".dropbtn1").click( function() {
    $("#formul1").css("display", "block");
});
$(".dropbtn2").click( function() {
    $("#formul2").css("display", "block");
});
$(".dropbtn3").click( function() {
    $("#formul3").css("display", "block");
});

$("ul").on("click", "span", function(event){
	var result = confirm("Are you sure you want to delete?");
	if (result) {
		$(this).parent().fadeOut(500,function(){
			var todoText = (this).attributes[1].value;
			var todoT = (this).attributes[0].value;
			console.log(this)
			console.log(todoText)
			console.log(todoT)
			$(this).remove();

			$.ajax({
			    url: '/course/'+todoText,
			    type: 'DELETE',
			    data: {id:todoT},
			    success: function(result) {
					// console.log(result, this);
			    }
			});
		});
	}
	event.stopPropagation();
	
});
