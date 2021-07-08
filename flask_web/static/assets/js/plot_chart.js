//-----------------------------------
function plot_chart_btn() {
	let pair = document.getElementById("inputCurrencyPair").value;
	let inputIndicator = document.getElementById("inputIndicator").getElementsByTagName("option");
	let indicators=""
	for (let i = 0; i < inputIndicator.length; i++){
		if (inputIndicator[i].selected) {
			indicators += inputIndicator[i].value.trim() + "+";
		}
	}
	indicators = indicators.substring(0, indicators.length-1);
	if (pair.length * indicators.length != 0){
		//sent request and receive response
		$.ajax({ url: "/r",
			type: "GET",
			data: {"typeRequest":201, 'pair':pair, 'indicators':indicators},
			success: function(response) {
				document.getElementById("profit-body").innerHTML= response.exp_profit + "%";
				plot_chart(JSON.parse(response.price), JSON.parse(response.signal));
			},
			error: function(error){
				console.log("error get request id 201");
			},
		});
	}
}

//-----------------------------------
let price = [];
let signals_sell = [];
let signals_buy = [];
let index = [];
let index_sell = [];
let index_buy = [];
function plot_chart(dict_price, dict_signal){

	for (i in dict_price){
		index.push(new Date(Number(i)));
		price.push(dict_price[i]);
		if (dict_signal[i] == 1){
			index_buy.push(new Date(Number(i)));
			signals_buy.push(dict_price[i]);
		}else if (dict_signal[i] == -1) {
			index_sell.push(new Date(Number(i)));
			signals_sell.push(dict_price[i]);
		}
	}
	
	//plot chart by Plotly
	let price_line = {
		x: index,
		y: price,
		mode: 'lines',
		type: 'scatter',
		name: "PRICE",
	};	
	let buy_line = {
		x: index_buy,
		y: signals_buy,
		mode: 'markers',
		type: 'scatter',
		name: "BUY",
	};	
	let sell_line = {
		x: index_sell,
		y: signals_sell,
		mode: 'markers',
		type: 'scatter',
		name: "SELL",
	};

	var data = [price_line, buy_line, sell_line];
	var layout = {title: '<h5 class="h3 text-white mb-0">Plot-title</h5>'};
	var config = {
		responsive: true, 
		showlegend: true,
		font: {size: 18},
		yaxis:{title:"Price"},
		margin: {l: 50, r: 50, b: 100, t: 100, pad: 4},
		paper_bgcolor: '#172b4d',
		plot_bgcolor: '#172b4d',
		modeBarButtonsToRemove: ['pan2d','selectLasso','lasso2d','resetScale2d',,
								'boxSelect', 'autoScale2d', 'zoom2d',  'toggle2d']
	};
	document.getElementById("chart-board").innerHTML = "";
	Plotly.newPlot('chart-board', data, layout, config);
}

//------------------------------------------------------------
// set addEventListener
document.getElementById("plot-char-btn").addEventListener("click", plot_chart_btn);