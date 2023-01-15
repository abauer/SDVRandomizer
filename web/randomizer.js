window.onload = function () {
	"use strict";
	var villagerSlider = document.getElementById("numVill");
	var villagerOutput = document.getElementById("villagerValue");
	villagerOutput.innerHTML = villagerSlider.value;
	villagerSlider.onchange = function(event) {
	  villagerOutput.innerHTML = villagerSlider.value;
	}
};