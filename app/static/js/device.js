document.addEventListener('DOMContentLoaded', () => {
  document.querySelector('#attribute').onchange = addInputCol;
});

function deviceTypeSelector() {
  const newValueSelector = document.createElement('select');
  newValueSelector.className = 'form-control';
  newValueSelector.id = 'new_value'
  newValueSelector.name = 'new_value'
  const defaultOpt = document.createElement('option');
  defaultOpt.value = '';
  defaultOpt.innerHTML = '--- Please choose ---';
  newValueSelector.appendChild(defaultOpt);
  for (var i = 0, size = device_types.length; i < size; i++){
    var option = document.createElement('option');
    option.value = device_types[i].id;
    option.innerHTML = device_types[i].make + ' ' + device_types[i].model;
    newValueSelector.appendChild(option)
  }
  return newValueSelector;
};

function textInput() {
  const newValue = document.createElement('input');
  newValue.className = 'form-control';
  newValue.id = 'new_value';
  newValue.name = 'new_value';
  newValue.placeholder = 'Leave empty to update from device ...';

  return newValue;
};

function addInputCol() {
  const inputCol = document.createElement('div');
  inputCol.className = 'form-group col-md-4';
  inputCol.id = 'inputCol';

  if (document.querySelector('#attribute').value == 'device_type_id') {
    input = deviceTypeSelector();
  }
  else {
    input = textInput()
  }

  inputCol.appendChild(input);
  document.querySelector('#updateRow').appendChild(inputCol);
  document.querySelector('#attribute').onchange = updateInputCol;
};

function updateInputCol() {
  if (document.querySelector('#attribute').value == 'device_type_id'){
    input = deviceTypeSelector();
  }
  else {
    input = textInput();
  }

  const currInput = document.querySelector('#new_value');
  const inputCol = document.querySelector('#inputCol');
  inputCol.removeChild(currInput);
  inputCol.appendChild(input);
};
