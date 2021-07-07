// create globle variable
const stat_tr_list = document.querySelector("#stat-board-body").getElementsByTagName("tr");
let pagination_list = new Array();
let pageList = new Array();
let currentPage = 1;
const numberPerPage = 4;
let numberOfPages =  Math.ceil(stat_tr_list.length / numberPerPage);   

//make pagination
function makeList() {
	pagination_list = new Array();
	for (var i=0; i < stat_tr_list.length; i++) {
		let tr = stat_tr_list[i];
		if (tr.getAttribute("class") == ""){
			pagination_list.push(tr)
		}
	}
	//make number pageList
	numberOfPages = Math.ceil(pagination_list.length / numberPerPage);
	currentPage = 1;
	document.getElementById("statPageNumber").innerText = currentPage;
}

function nextStatPage() {
	if (currentPage < numberOfPages){
		currentPage += 1;
		document.getElementById("statPageNumber").innerText = currentPage;
		loadList();
	}
}

function previousStatPage() {
	if (currentPage > 1) {
    currentPage -= 1;
    loadList();
	document.getElementById("statPageNumber").innerText = currentPage;
	}
}

function loadList() {
    var begin = ((currentPage - 1) * numberPerPage);
    var end = begin + numberPerPage;
	
    pageList = pagination_list.slice(begin, end);
    drawList();    // draws out our data
}

function drawList() {
    for (r = 0; r < pagination_list.length; r++) {
  		pagination_list[r].setAttribute("class", "visually-hidden");
    }    
    for (r = 0; r < pageList.length; r++) {
       pageList[r].setAttribute("class", "")
	}
}


function load_board(){
	makeList();
	loadList();
}


//------------------------------------------
// make categorical feature
//------------------------------------------
function show_stat(e){
	let id = e.srcElement.getAttribute("id")
	for (var i=0; i < stat_tr_list.length; i++) {
		let tr = stat_tr_list[i];
		if (id == "all_pairs" || id == tr.getElementsByTagName("th")[0].innerText.replace("/", "")){
			tr.setAttribute("class", "");
		}
		else {
			tr.setAttribute("class", "visually-hidden");
		}
		
	}
	load_board();
}

//--------------------------------------------
//init load page 
//--------------------------------------------

// add event function in li tag in currency pairs list
const ul_list_pairs = document.querySelector("#list-pairs").getElementsByTagName("li");
for (var i=0; i < ul_list_pairs.length; i++) {
	let id = ul_list_pairs[i].getAttribute("id");	
	let obj = document.querySelector("#"+id);
	obj.addEventListener("click", show_stat);
}

//load pagination
document.getElementById("statBoardNext").addEventListener("click", nextStatPage);
document.getElementById("statBoardPrevious").addEventListener("click", previousStatPage);
document.getElementById("all_pairs").click()