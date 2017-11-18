$('#play_cards').click(function(d) {
	var selects = $('select');
	var valid = true;
	for (i = 0; i < selects.length; i++){
		for (j = 0; j < selects.length; j++){
			if (j != i) {
				if (selects[i].value == selects[j].value) {
					valid = false;
				}
			}
		}
	}
	
	console.log(valid);
	
	if (!valid){
		$('#warning').text("A single card cannot be played in multiple provinces");
	}
	else {
		$('#warning').text("");
		$('#cards').submit();
	}
});