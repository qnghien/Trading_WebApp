//make pagination of transaction log board
const transaction_log_list = document.querySelector("#transactionLogBoard").getElementsByTagName("tr");
let pageLogList = new Array();
let currentlogPage = 1;
const numberPerPage = 4;
let numberOfPages = Math.ceil(transaction_log_list.length / numberPerPage)
//make pagination
function initPagination() {
	numberOfPages = Math.ceil(transaction_log_list.length / numberPerPage);
	currentLogPage = 1;
}

function nextLogPage() {
	if (currentLogPage < numberOfPages){
		currentLogPage += 1;
		document.getElementById("logPageNumber").innerText = currentlogPage;
		loadLogList();
	}
}

function previousLogPage() {
	if (currentlogPage > 1) {
		currentLogPage -= 1;
		document.getElementById("logPageNumber").innerText = currentlogPage;
		loadLogList();
	}
}

function loadLogList() {
	for (i = 0; i < transaction_log_list.length; i++) {
		if (i >= (currentlogPage - 1) * numberPerPage && i < currentlogPage * numberPerPage){
			
			transaction_log_list[i].setAttribute("class", "");
		}
		else{
			transaction_log_list[i].setAttribute("class", "visually-hidden");
		}
		
    }   
}

function load_logboard(){
	initPagination();
	loadLogList();
}

//load pagination
document.getElementById("transactionLogNext").addEventListener("click", nextLogPage);
document.getElementById("transactionLogPrevious").addEventListener("click", previousLogPage);
load_logboard();