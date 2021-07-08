var CHECK_CURRENT_PRICE = 0;
function update_stat_board(e) {
	let id = e.srcElement.getAttribute("id");
	
	//update current-price
	if (id == "update-cur-price-btn"){
		let list_currency = "";
		for (var i=1; i < ul_list_pairs.length; i++) { //ul_list_pairs defined in stat-board
			list_currency += ul_list_pairs[i].innerText.replace("/", "-");
			if (i + 1 < ul_list_pairs.length){
				list_currency += "+";
			}
		}
		//sent request and receive response
		$.ajax({ url: "/r",
			type: "GET",
			data: {"typeRequest":200},
			success: function(response) {
				current_price = response.cur_price_list;
				list_currency = list_currency.replaceAll("-", "/").split("+");
				show_current_price(list_currency, current_price);
				CHECK_CURRENT_PRICE = 1;
			},
			error: function(error){
				console.log("error get request id 200");
				console.log(error);
			},
		});     
		
	}
	
	if (id == "update-profit-btn") {
		if (CHECK_CURRENT_PRICE == 0) {
			window.alert("Need update Current Price!");
		}
		else {
			let stat_board_body = document.getElementById("stat-board-body").getElementsByTagName("tr");
			let data = [];
			
			for (let i=0; i < stat_board_body.length; i++){
				let tr = stat_board_body[i];
				data.push(tr.getElementsByTagName('th')[3].innerHTML);
				
			}
			data = {'typeRequest':101, "data":data};
			jsonData = JSON.stringify(data);
			// sent request
			$.ajaxPrefilter(function (options, originalOptions, jqXHR) {
				let csrf_token = document.getElementById("token").getAttribute("value");
				jqXHR.setRequestHeader('X-CSRF-Token', csrf_token);
			});
			$.ajax({ url: "/r",
				type: "POST",
				data: jsonData,
				dataType: "json",
				contentType : 'application/json',
				success: function(response) {
					profit_list = response.profit_list;
					show_exp_profit(profit_list);	
				},
			}); 
		}
	}
}

function show_current_price(list_currency, current_price){
	let stat_board_body = document.getElementById("stat-board-body").getElementsByTagName("tr");
	// just update value
	for (let i = 0; i < stat_board_body.length; i++) {
			let list_th = stat_board_body[i].getElementsByTagName("th");
			list_th[3].innerHTML = current_price[list_currency.indexOf(list_th[0].innerText)];
	}
}

function show_exp_profit(profit_list){
	let stat_board_body = document.getElementById("stat-board-body").getElementsByTagName("tr");
	// just update value
	for (let i = 0; i < stat_board_body.length; i++) {
			list_th = stat_board_body[i].getElementsByTagName("th");
			list_th[4].innerHTML = profit_list[i];
	}
	//update revenue
	sum_revenue = 0;
	for (let i = 0; i < profit_list.length; i++){
		sum_revenue += profit_list[i];
	}
	document.getElementById("revenueCard").getElementsByTagName("span")[0].innerHTML = sum_revenue.toString() + "$";
}

// addEventListener
document.getElementById("update-cur-price-btn").addEventListener("click", update_stat_board);
document.getElementById("update-profit-btn").addEventListener("click", update_stat_board);
