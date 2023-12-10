
let lightswitch = document.getElementById("lightswitch");

let morse_submit = document.getElementById("morse-submit");
let morse_text = document.getElementById("morse-text");

let forward = document.getElementById("forward");
let left = document.getElementById("left");
let right = document.getElementById("right");
let reverse = document.getElementById("reverse");


let buttons = [forward, left, right, reverse];


socket.emit("rover_active");

socket.on("rotate_users", () => {
		window.location.replace("http://" + location.host + "/mission_control");
})
/*socket.on("flash_mission_control", (flash) => {
	console.log(flash)
	try {
		existing_msg = document.getElementById("flash_msg")
		if (existing_msg) {
			existing_msg.remove()
		}
	} catch {
		console.log("no prev messages")
	}
	let flash_elem = document.createElement("div");
	flash_elem.id = "flash_msg"
	flash_elem.innerHTML = flash;
	let content = document.querySelector(".primary-content");
	content.insertBefore(flash_elem, content.children[0])
})*/


document.getElementById('morse-form').addEventListener('shown.bs.modal', function() {
  morse_text.focus();
})

morse_submit.onclick = () => {
	socket.emit("morse", morse_text.value);
	morse_text.value = "";
	morse_text.blur();
	//socket.emit("flash", {dest: "mission_control", msg: morse_text.value});	
}

morse_text.addEventListener("keydown", (ev) =>{
	if (ev.keyCode === 13) {
		morse_submit.click();
	}
});

for (const button of buttons) {

	button.addEventListener("mousedown", () => {
		socket.emit("engage", button.id);
	});

	button.addEventListener("mouseup", () => {
		socket.emit("terminate", button.id);
	});

	button.addEventListener("touchstart", () => {
		socket.emit("engage", button.id);
	});

	button.addEventListener("touchend", () => {
		socket.emit("terminate", button.id);
	});

	button.addEventListener("mouseleave", () =>{	
		socket.emit("terminate", button.id);
	});
}

lightswitch.onclick = () => {
	socket.emit("lightswitch", lightswitch.checked);
}
