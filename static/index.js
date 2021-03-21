let destinationAutocomplete;
let destination;
let destinationStreetNumber;
let destinationStreet;
let destinationCity;

let originAutocomplete;
let origin;
let originStreetNumber;
let originStreet;
let originCity;


function initAutocomplete() {
    destination = document.querySelector("#destination-address");
    destinationStreetNumber = document.querySelector('#destination-street-number');
    destinationStreet = document.getElementById('destination-street');
    destinationCity = document.querySelector('#destination-city');
    
    origin = document.querySelector("#origin-address");
    originStreetNumber = document.querySelector('#origin-street-number');
    originStreet = document.querySelector('#origin-street');
    originCity = document.querySelector('#origin-city');

    
    options = {
        componentRestrictions: { country: "il" }
    };

    //there is probablt a better way to do this instead of two autocompletes
    destinationAutocomplete = new google.maps.places.Autocomplete(destination, options);
    destinationAutocomplete.addListener("place_changed", fillInDestination);
    originAutocomplete = new google.maps.places.Autocomplete(origin, options);
    originAutocomplete.addListener("place_changed", fillInDestination);
}

function fillInDestination() {
    const place = destinationAutocomplete.getPlace();
    let address = "";

    for (const component of place.address_components) {
        const componentType = component.types[0];

        switch (componentType) {
            case "street_number": {
                streetNumber = component.long_name;
                destinationStreetNumber.value = streetNumber;
                address = streetNumber;
                break;
            }

            case "route": {
                streetName = component.short_name;
                destinationStreet.value = streetName;
                address = streetName + ' ' + address + ', '
                break;
            }

            case "premise": {
                streetNameAndNumber = component.short_name.split(' ');
                destinationStreet.value = streetNameAndNumber[0];
                destinationStreetNumber.value = streetNameAndNumber[1];
                address = component.short_name + ', ';
                break;
            }

            case "locality": {
                city = component.long_name;
                destinationCity.value = city;
                address += city;
                break;
            }
        }
    }
    
    destination.value = address;
}

function fillInOrigin() {
    const place = originAutocomplete.getPlace();
    let address = "";

    for (const component of place.address_components) {
        const componentType = component.types[0];

        switch (componentType) {
            case "street_number": {
                streetNumber = component.long_name;
                originStreetNumber.value = streetNumber;
                address = streetNumber;
                break;
            }

            case "route": {
                streetName = component.short_name;
                originStreet.value = streetName;
                address = streetName + ' ' + address + ', ';
                break;
            }

            case "premise": {
                streetNameAndNumber = component.short_name.split(' ');
                originStreet.value = streetNameAndNumber[0];
                originStreetNumber.value = streetNameAndNumber[1];
                address = component.short_name;
                break;
            }

            case "locality": {
                city = component.long_name;
                originCity.value = city;
                address += city;
              break;
            }
        }
    }

    origin.value = address;
}

// function customAddressFormatting() {
//     return {}
// }