function wirteFunc() {
 $.ajax({
	url: "/static/stubprogram.txt",
        datatype: "text",
	success: function (data) {
	console.log(data)
	$("#div1").text(data);
	}
   });
}
