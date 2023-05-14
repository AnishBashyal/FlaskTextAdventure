
function handleRadioButtonClick(radioButton) {
    var formOptionSection = document.getElementById('formOptionSection');
    formOptionSection.style.display = (radioButton.value === 'none') ? 'block' : 'none';

}
