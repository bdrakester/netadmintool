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

function textInputDeviceUpdate() {
  const newValue = document.createElement('input');
  newValue.className = 'form-control';
  newValue.id = 'new_value';
  newValue.name = 'new_value';
  newValue.placeholder = 'Leave empty to update from device ...';
  //newValue.oninput = manualUpdate;
  return newValue;
}

function updateButton() {
  const newButton = document.createElement('button');
  newButton.className = 'btn btn-primary';
  newButton.id = 'update_button';
  newButton.type = 'submit';
  newButton.innerHTML = 'Update';
  return newButton;
}

function updateButtonDeviceUpdate() {
  const newButton = document.createElement('button');
  newButton.className = 'btn btn-primary';
  newButton.id = 'update_button';
  newButton.innerHTML = 'Update';
  newButton.type="button";
  newButton.dataset.toggle="modal";
  newButton.dataset.target="#deviceCredentialsModal";
  return newButton;
}

function Update() {
  const attribute = document.querySelector('#attribute').value;
  console.log('Inside Update...');
  if (attribute == 'sw_version' || attribute == 'serial_number'){
    const new_value = document.querySelector('#new_value').value;
    console.log('If sw_version or serial_number...');
    if (new_value == ''){
      modal = document.querySelector('#deviceCredentialsModal');
      modal.modal("toggle");
      console.log(modal.id);
      //$("#myModal").modal()
    }
  }
}

function addInputCol() {
  const inputCol = document.createElement('div');
  inputCol.className = 'form-group col-md-4';
  inputCol.id = 'inputCol';

  const attribute = document.querySelector('#attribute').value;

  if (attribute == 'device_type_id') {
    input = deviceTypeSelector();
    //update = updateButton();
  }
  else if(attribute == 'sw_version') {
    input = textInputDeviceUpdate();
    //update = updateButtonDeviceUpdate();
  }
  else if(attribute == 'serial_number') {
    input = textInputDeviceUpdate();
    //update = updateButtonDeviceUpdate();
  }
  else {
    input = textInput();
    //update = updateButton();
  }

  inputCol.appendChild(input);
  document.querySelector('#updateRow').appendChild(inputCol);
  document.querySelector('#attribute').onchange = updateInputCol;

  //document.querySelector('#updateButtonCol').appendChild(update);

  document.querySelector('#deviceCredentialsModalAttribute').value = attribute;
};

function updateInputCol() {
  const attribute = document.querySelector('#attribute').value;

  if (attribute == 'device_type_id') {
    input = deviceTypeSelector();
    //update = updateButton();
  }
  else if(attribute == 'sw_version') {
    input = textInputDeviceUpdate();
    //update = updateButtonDeviceUpdate();
  }
  else if(attribute == 'serial_number') {
    input = textInputDeviceUpdate();
    //update = updateButtonDeviceUpdate();
  }
  else {
    input = textInput();
    //update = updateButton();
  }

  const currInput = document.querySelector('#new_value');
  const inputCol = document.querySelector('#inputCol');
  inputCol.removeChild(currInput);
  inputCol.appendChild(input);

  //const currUpdate = document.querySelector('#update_button');
  //const updateButtonCol = document.querySelector('#updateButtonCol');
  //updateButtonCol.removeChild(currUpdate);
  //updateButtonCol.appendChild(update);

  document.querySelector('#deviceCredentialsModalAttribute').value = attribute;
};
