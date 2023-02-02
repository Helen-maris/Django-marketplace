const chatSocket = new WebSocket("ws://" + window.location.host + "/ads/");
	chatSocket.onopen = function (e) {
		console.log("The connection was setup successfully !");
	};
	chatSocket.onclose = function (e) {
		console.log("Something unexpected happened !");
	};
	document.querySelector("#id_message_send_input").focus();
	document.querySelector("#id_message_send_input").onkeyup = function (e) {
		if (e.keyCode == 13) {
		document.querySelector("#id_message_send_button").click();
		}
	};
	document.querySelector("#id_message_send_button").onclick = function (e) {
		var messageInput = document.querySelector(
		"#id_message_send_input"
		).value;
		chatSocket.send(JSON.stringify({ message: messageInput}));
	};
	chatSocket.onmessage = function (e) {
		const data = JSON.parse(e.data);
		document.querySelector("#id_message_send_input").value = "";
		var result = data.result
		if (result == null)
		{
			var a = document.getElementById("id_search_result");
			a.removeAttribute('href')
			a.innerHTML = "Объявление не найдено"

		} else {
			var a = document.getElementById("id_search_result");
			a.href = data.result;
			a.innerHTML = data.message;
		}
	};