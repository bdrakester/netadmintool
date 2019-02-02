document.addEventListener('DOMContentLoaded', () => {
  document.querySelector('#attribute').onchange = addInputCol;
});

function deviceTypeSelector() {
  const newValueSelector = document.createElement('select');
  newValueSelector.className = 'form-control';
  newValueSelector.id = 'new_value';
  newValueSelector.name = 'new_value';
  const defaultOpt = document.createElement('option');
  defaultOpt.value = '';
  defaultOpt.innerHTML = '--- Please choose ---';
  newValueSelector.appendChild(defaultOpt);
  for (var i = 0, size = device_types.length; i < size; i++){
    var option = document.createElement('option');
    option.value = device_types[i].id;
    option.innerHTML = device_types[i].make + ' ' + device_types[i].model;
    newValueSelector.appendChild(option);
  }
  return newValueSelector;
};

function textInput() {
  const newValue = document.createElement('input');
  newValue.className = 'form-control';
  newValue.id = 'new_value';
  newValue.name = 'new_value';
  return newValue;
};

function updateTextInput(checkbox) {
  if (checkbox.checked) {
    textInput = document.querySelector('#new_value');
    textInput.setAttribute('readonly', 'readonly');
    textInput.value = '';
    update = updateButtonDeviceUpdate();
  }
  else {
    document.querySelector('#new_value').removeAttribute('readonly', 'readonly');
    update = updateButton();
  }

  const currUpdate = document.querySelector('#update_button');
  const updateButtonCol = document.querySelector('#updateButtonCol');
  updateButtonCol.removeChild(currUpdate);
  updateButtonCol.appendChild(update);
};

function queryDeviceCheckCol() {
  const newCheckboxCol = document.createElement('div');
  newCheckboxCol.className = 'form-group form-check-inline';
  newCheckboxCol.id = 'checkboxCol';

  const newCheck = document.createElement('input');
  newCheck.className = "form-check-input";
  newCheck.type = 'checkbox';
  newCheck.id = 'queryDeviceCheckbox';
  newCheck.onchange = function() { updateTextInput(this); };

  const newLabel = document.createElement('label');
  newLabel.className = 'form-check-label';
  newLabel.for = 'queryDeviceCheckbox';
  newLabel.innerHTML = 'Query Device';

  newCheckboxCol.appendChild(newCheck);
  newCheckboxCol.appendChild(newLabel);

  return newCheckboxCol;
};

function updateButton() {
  const newButton = document.createElement('button');
  newButton.className = 'btn btn-primary';
  newButton.id = 'update_button';
  newButton.type = 'submit';
  newButton.innerHTML = 'Update';
  return newButton;
};

function updateButtonDeviceUpdate() {
  const newButton = document.createElement('button');
  newButton.className = 'btn btn-primary';
  newButton.id = 'update_button';
  newButton.innerHTML = 'Update';
  newButton.type="button";
  newButton.dataset.toggle="modal";
  newButton.dataset.target="#deviceCredentialsModal";
  return newButton;
};

function addInputCol() {
  const inputCol = document.createElement('div');
  inputCol.className = 'form-group col-md-4';
  inputCol.id = 'inputCol';

  const attribute = document.querySelector('#attribute').value;

  if (attribute == 'device_type_id') {
    input = deviceTypeSelector();
  }
  else {
    input = textInput();
  }

  inputCol.appendChild(input);

  const updateRow = document.querySelector('#updateRow');
  updateRow.appendChild(inputCol);

  if (attribute == 'sw_version' || attribute == 'serial_number') {
    const checkBoxCol = queryDeviceCheckCol();
    updateRow.appendChild(checkBoxCol);
  }

  document.querySelector('#attribute').onchange = updateInputCol;
  document.querySelector('#deviceCredentialsModalAttribute').value = attribute;
};


function updateInputCol() {
  const attribute = document.querySelector('#attribute').value;

  if (attribute == 'device_type_id') {
    input = deviceTypeSelector();
  }
  else {
    input = textInput();
  }

  const inputCol = document.querySelector('#inputCol');
  const currInput = document.querySelector('#new_value');
  inputCol.removeChild(currInput);
  inputCol.appendChild(input);

  const updateRow = document.querySelector('#updateRow');

  const oldCheckboxCol = document.querySelector('#checkboxCol');
  if (oldCheckboxCol != null){
    updateRow.removeChild(checkboxCol);
  }

  if (attribute == 'sw_version' || attribute == 'serial_number') {
    const checkBoxCol = queryDeviceCheckCol();
    updateRow.appendChild(checkBoxCol);
  }

  document.querySelector('#deviceCredentialsModalAttribute').value = attribute;
};
