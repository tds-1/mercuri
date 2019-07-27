// <<<<<<< HEAD

// =======
// correct answer
// >>>>>>> 25b0026bb6bb5287ca3322f915f9f6a7be3a244f

// console.log("connecteed");
var y

// list item delete
$(".next").on("click",function(){
	console.log(y)	
	var redir=this.baseURI
	console.log(redir)
	
	$.ajax({
        type: "POST",
        url: redir,
        success: function(){},
        data: {title: "none", select:"none",res: y},
        success:function(response){
        	console.log("response")
            document.write(response); 
       }

    });
//	event.stopPropagation();

});

$("ul").one("click", "li", function(event){
	var title=this.attributes[2].value
	var redir=this.baseURI
	var select=this.attributes[1].value
	var x=this
	var righ;
	// console.log(redir)
	$.ajax({
		url: redir,
	    type: "POST",
	    data: {title: title, select: select, res:-1},
	    error: function (request, error) {
	        // console.log(arguments);
	        alert(" Can't do because: " + error);
	    },
	    success: function(result) {
	    	// console.log("Hurray!!!!!!",result)
	    	// console.log(x)
	    	// console.log(result.right ,result.submi)
	    	if (result.right==result.submi){
	    		 console.log("correct")
	    		$(x).toggleClass('correct');
	    		y=1
	    	}
	    	else{
	    		// console.log("incorrect")
	    		$(x).toggleClass('incorrect');
	    		functionA();	
	   			y=0
	   		}
		}
	});
	$(".formul").css("display", "block");

//	event.stopPropagation();
	
});


// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
function functionA() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}
