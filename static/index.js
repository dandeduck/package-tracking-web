let destinationAutocomplete;
let originAutocomplete;
let origin;
let detination;

function initAutocomplete() {
    origin = document.querySelector("#origin-address");
    destination = document.querySelector("#destination-address");
    
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
    
    destination.value = extractAddress(place);
}

function fillInOrigin() {
    const place = originAutocomplete.getPlace();
    
    origin.value = extractAddress(place);
}

function extractAddress(place) {
    let address = ""

    for (const component of place.address_components) {
        const componentType = component.types[0];

        switch (componentType) {
            case "street_number": {
                address = component.long_name
                break;
            }

            case "route": {
                address = component.short_name + ' ' + address + ', '
                break;
            }

            case "premise": {
                address = component.short_name + ' ' + address +  ', ' 
                break;
            }

            case "locality": {
                address += component.long_name
              break;
            }
        }
    }

    return address
}