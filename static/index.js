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
    //change to dicts?
    destination = document.querySelector("#destination-address");
    destinationStreetNumber = document.querySelector('#destination-street-number');
    destinationStreet = document.getElementById('destination-street');
    destinationCity = document.querySelector('#destination-city');
    
    origin = document.querySelector("#origin-address");
    originStreetNumber = document.querySelector('#origin-street-number');
    originStreet = document.querySelector('#origin-street');
    originCity = document.querySelector('#origin-city');

    
    options = {
        componentRestrictions: { country: "il" },
        types: ['address']
    };

    //there is probablt a better way to do this instead of two autocompletes
    destinationAutocomplete = new google.maps.places.Autocomplete(destination, options);
    destinationAutocomplete.addListener("place_changed", fillInDestination);
    originAutocomplete = new google.maps.places.Autocomplete(origin, options);
    originAutocomplete.addListener("place_changed", fillInOrigin);
}

function fillInDestination() {
    const place = destinationAutocomplete.getPlace();
    let address = {};

    if(typeof place.address_components === 'undefined')
        address = customAddressFormatting(destination.value)
    else
        address = extractAddressComponents(place)
    
    destination.value = address['formatted'];
    destinationCity.value = address['city'];
    destinationStreet.value = address['street'];
    destinationStreetNumber.value = address['street_number'];
}

function fillInOrigin() {
    const place = originAutocomplete.getPlace();
    let address = {};

    if(typeof place.address_components === 'undefined')
        address = customAddressFormatting(origin.value)
    else
        address = extractAddressComponents(place)

    origin.value = address['formatted'];
    originCity.value = address['city'];
    originStreet.value = address['street'];
    originStreetNumber.value = address['street_number'];
}

function extractAddressComponents(place) {
    let address = {};
    let str = "";

    for (const component of place.address_components) {
        const componentType = component.types[0];

        switch (componentType) {
            case "street_number": {
                streetNumber = component.long_name;
                address['street_number'] = streetNumber;
                str = streetNumber;
                break;
            }

            case "route": {
                streetName = component.short_name;
                address['street'] = streetName;
                str = streetName + ' ' + str + ', ';
                break;
            }

            case "locality": {
                city = component.long_name;
                address['city'] = city;
                str += city;
              break;
            }
        }
    }

    address['formatted'] = str;

    if(typeof address['street_number'] === 'undefined')
        address['street_number'] = 1;

    return address;
}

function customAddressFormatting(customInput) {
    components = customInput.split(',');
    address = {}

    if(components.length === 1)
        address['city'] = components[0];

    else {
        if(components[1].charAt(0) === ' ')
            components[1] = components[1].substring(1);

        address['city'] = components[1];
        streetDetails = extractStreetDetails(components[0].split(' '));
    }
    
    address['street'] = streetDetails[0];
    address['street_number'] = streetDetails[1];

    if(typeof address['street'] === 'undefined')
        address['street'] = '<not provided>';

    if(typeof address['street_number'] === 'undefined' || isNaN(address['street_number']))
        address['street_number'] = 1;
    
    address['formatted'] = customInput;

    return address;
}

function extractStreetDetails(detailsStr) {
    let word = "";
    let streetName = "";
    let streetNumber;

    streetDetails = detailsStr;

    for(i = 0; !isNumber(word); i++) {
        word = streetDetails[i];
        streetName += streetDetails + ' ';
    }

    streetName = streetName.slice(0, -1);
    streetNumber = parseInt(word);

    return [streetName, streetNumber];
}

function isNumber(str) {
    num = parseInt(str);

    return !isNaN(num);
}