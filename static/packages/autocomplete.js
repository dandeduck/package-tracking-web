class AutocompleteField {
    constructor(input, city, street, streetNumber) {
        this.input = input;
        this.city = city;
        this.street = street;
        this.streetNumber = streetNumber;

        this.autocomplete = new google.maps.places.Autocomplete(input, {
            componentRestrictions: { country: "il" },
            types: ['address']
        });
        this.autocomplete.addListener("place_changed", () => this.fillIn(this));
        this.input.onblur = () => this.fillIn(this);
        // this.input.onfocusout = () => this.fillIn(this);
    }

    fillIn(self) {
        const place = self.autocomplete.getPlace();
        let address = new Address(place, self.input.value);

        self.input.value = address.fields['formatted'];
        self.city.value = address.fields['city'];
        self.street.value = address.fields['street'];
        self.streetNumber.value = address.fields['street_number'];
    }
}

class Address {
    constructor(place, input) {
        if (typeof place === 'undefined' || typeof place.address_components === 'undefined')
            this.fields = this.customAddressFormatting(this, input);
        else
            this.fields = this.extractAddressComponents(place);
    }

    customAddressFormatting(self, customInput) {
        let components = customInput.split(',');
        let address = {}

        if (components.length === 1)
            address['city'] = components[0];
        else {
            if (components[1].charAt(0) === ' ')
                components[1] = components[1].substring(1);

            address['city'] = components[1];
            streetDetails = self.extractStreetDetails(components[0].split(' '));

            address['street'] = streetDetails[0];
            address['street_number'] = streetDetails[1];
        }

        if (typeof address['street'] === 'undefined')
            address['street'] = '<no street>';
        if (typeof address['street_number'] === 'undefined' || isNaN(address['street_number']))
            address['street_number'] = 1;

        address['formatted'] = customInput;

        return address;
    }

    extractStreetDetails(self, detailsStr) {
        let word = "";
        let streetName = "";
        let streetNumber;

        streetDetails = detailsStr;

        for (i = 0; !self.isNumber(word); i++) {
            word = streetDetails[i];
            streetName += streetDetails + ' ';
        }

        streetName = streetName.slice(0, -1);
        streetNumber = parseInt(word);

        return [streetName, streetNumber];
    }

    isNumber(str) {
        num = parseInt(str);

        return !isNaN(num);
    }

    extractAddressComponents(place) {
        let address = {};
        let str = "";

        for (const component of place.address_components) {
            const componentType = component.types[0];

            switch (componentType) {
                case "street_number": {
                    let streetNumber = component.long_name;
                    address['street_number'] = streetNumber;
                    str = streetNumber;
                    break;
                }

                case "route": {
                    let streetName = component.short_name;
                    address['street'] = streetName;
                    str = streetName + ' ' + str + ', ';
                    break;
                }

                case "locality": {
                    let city = component.long_name;
                    address['city'] = city;
                    str += city;
                    break;
                }
            }
        }

        address['formatted'] = str;

        if (typeof address['street_number'] === 'undefined')
            address['street_number'] = 1;

        return address;
    }
}

function initAutocomplete() {
    destination = document.querySelector("#destination-address");
    destinationCity = document.querySelector('#destination-city');
    destinationStreet = document.getElementById('destination-street');
    destinationStreetNumber = document.querySelector('#destination-street-number');

    new AutocompleteField(destination, destinationCity, destinationStreet, destinationStreetNumber);

    origin = document.querySelector("#origin-address");
    originCity = document.querySelector('#origin-city');
    originStreet = document.querySelector('#origin-street');
    originStreetNumber = document.querySelector('#origin-street-number');

    new AutocompleteField(origin, originCity, originStreet, originStreetNumber);
}
