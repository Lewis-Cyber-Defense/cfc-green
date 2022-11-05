function toggleInputs(state) {
	$("#contactName").prop("disabled", state);
	$("#contactEmail").prop("disabled", state);
	$("#contactPhoneNumber").prop("disabled", state);
	$("#contactFile").prop("disabled", state);
}


async function fakemail() {

	toggleInputs(true);

	let card = $("#resp-msg");
	card.attr("class", "alert alert-info");
	card.hide();

	let name = $("#contactName").val();
	let email = $("#contactEmail").val();
	let phone = $("#contactPhoneNumber").val();

	// https://stackoverflow.com/questions/5587973/javascript-upload-file
	let file = document.getElementById("contactFile").files[0];
	let formData = new FormData();

	if ($.trim(name) === '' || $.trim(email) === '' || $.trim(phone) === '' || $.trim(file) === '') {
		toggleInputs(false);
		card.text("Please input all required fields first!");
		card.attr("class", "alert alert-danger");
		card.show();
		return;
	}

	const data = {
		contactName: name,
		contactEmail: email,
		contactPhone: phone
	};

	await fetch(`/api/contact`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(data),
		})
		.then((response) => response.json()
			.then((resp) => {
				card.attr("class", "alert alert-danger");
				if (response.status == 200 && intent == "login") {
					card.attr("class", "alert alert-success");
                    return;
				}
				else if(response.status == 200){
					card.text(resp.message);
					card.attr("class", "alert alert-success");
					card.show();
					return;
				}
				card.text(resp.message);
				card.show();
			}))
		.catch((error) => {
			card.text(error);
			card.attr("class", "alert alert-danger");
			card.show();
		});

	formData.append("file", file);
	await fetch('/api/upload', {method: "POST", body: formData})
	//	.catch((error) => {
	//		card.text(error);
	//		card.attr("class", "alert alert-danger");
	//		card.show();
	//	});

	toggleInputs(false);
}