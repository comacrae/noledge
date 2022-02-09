const API_ENDPOINT = "PUT ENDPOINT HERE"
// convert answers JSON to a dict w/ three keys: answer, confidence, and url
function processAnswers(answers) {
  console.log(answers);

  let ans_arr = new Array(answers.length);

  for(var i = 0; i < answers.length; i++) {
	  const ans = answers[i];
	  const meta = ans['meta'];
	  const urlText = meta['url'];

	  const processed_ans = { answerText : ans['answer'] , 
		     context : ans['context'] ,
		     url : urlText
	  }
	ans_arr[i] = processed_ans;
  }
  return ans_arr;
}

function changeBackgroundURL(new_url) {
	let queryOptions = { active: true, currentWindow: true };
	let tab = chrome.tabs.query(queryOptions);
	chrome.tabs.update(tab.id, {url:new_url}); 
	console.log("newurl: " + new_url);

}

function generateTable(answers) {
  //generating table
  const table = document.getElementById('answerTable');
  //generating table head [ a | b | c ]
  let thead = table.createTHead();
  let row = thead.insertRow();
  // filling thead with labels [ANSWER | CONTEXT | URL]
  keys = ['ANSWER', 'CONTEXT', 'URL'];
  for (var i = 0; i < keys.length; i++) {
	  let th = document.createElement('th');
	  let text = document.createTextNode(keys[i]);
	  th.appendChild(text);
	  row.appendChild(th);
  }

  // filling body with answers
  for(var i = 0; i < answers.length; i++) {
	  ans = answers[i];
	  let row = table.insertRow();
	  for (key in ans) {
		  let cell = row.insertCell();
		  let text = document.createTextNode(ans[key]);
		  // if it's a url, add button and listener so it will react
		  if(key == "url") {
			  let text = document.createTextNode("Go to page");
			  let urlStr = "https://" + ans[key];
			  let b = document.createElement('button');
			  b.addEventListener("click",()=> changeBackgroundURL(urlStr));
			  b.appendChild(text);
			  cell.appendChild(b);
		  } else {
			  cell.appendChild(text);
		  }
	  }
  	}
}

function clearTable() {
	let table = document.getElementById("answerTable");
	table.deleteTHead();
	//for(var i = 0; i < table.row
}

window.addEventListener( "load", function () {
  
  function sendData() {
    const XHR = new XMLHttpRequest();
    XHR.responseType = "json"

    // Define what happens on successful data submission
    XHR.addEventListener( "load", function(event) {
	response = event.target.response;
	answers = processAnswers(response['answers']);
        generateTable(answers);
    } );

    // Define what happens in case of error
    XHR.addEventListener( "error", function( event ) {
      alert( 'Oops! Something went wrong.' );
    } );


    // Extract params entered from form 
    const FD = new FormData(form);
    var question = FD.get("question");
    var top_k = FD.get("top_k");
    console.log(question);
    console.log(top_k);

    const target = new URL("http://YOUR ENDPOINT HERE/query")
    var req = JSON.stringify(
    {"query": question, 
	    "params":  {"Retriever": {"top_k": Number(top_k)}, 
			"Reader": {"top_k": Number(top_k)}
	    }
    }
	 			)


    // Set up our request
    XHR.open( "POST", target.toString(), true);
	XHR.setRequestHeader("Content-Type", "application/json");
	//XHR.setRequestHeader("Access-Control-Allow-Origin", "*");
    XHR.send(req);

  }

  // Access the form element...
  const form = document.getElementById( "queryForm" );

  // ...and take over its submit event.
  form.addEventListener( "submit", function ( event ) {
    event.preventDefault();
    clearTable();
    sendData();
  } );

  const home_button = document.getElementById("home");
  const home_url = "http://STREAMLIT ENDPOINT URL"; 
  home_button.addEventListener("click",()=> changeBackgroundURL(home_url));

} );

