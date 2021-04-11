class AutocompleteField {
    constructor(input, city, street, streetNumber) {
        this.input = input;
        this.city = city;
        this.street = street;
        this.streetNumber = streetNumber;

        this.autocomplete = new google.maps.places.Autocomplete(input, {
            componentRestrictions: { country: 'il' },
            types: ['address']
        });
        this.autocomplete.addListener("place_changed", () => this.fillIn(this));
        this.input.onblur = () => this.fillIn(this);
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
            this.fields = this.customAddressFormatting(input);
        else
            this.fields = this.extractAddressComponents(place);
    }

    customAddressFormatting(customInput) {
        const numRegex = /\d+/;
        const wordRegex = /\w+/;

        let components = customInput.split(',');
        let address = {};

        if (components.length == 1)
            address['city'] = components[0];
        else {
            let streetNumber = components[0].match(numRegex);
            let street;
            let city;

            if (components[1].charAt(0) == ' ')
                components[1] = components[1].substring(1);

            if (streetNumber) {
                street = components[0];
                city = components[1];
            }
            else {
                streetNumber = components[1].match(numRegex);
                street = components[1];
                city = components[0];
            }

            address['street_number'] = streetNumber;
            address['street'] = street.match(wordRegex);
            address['city'] = city;
        }

        address['street'] ??= '<no street>';

        if (typeof address['street_number'] === 'undefined' || address['street_number'] == '')
            address['street_number'] = 1;

        address['formatted'] = customInput;

        return address;
    }

    extractAddressComponents(place) {
        let address = {};
        let str = '';

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
        address['street_number'] ??= 1;

        return address;
    }
}

function initAutocomplete() {
    let destination = document.querySelector("#destination-address");
    let destinationCity = document.querySelector('#destination-city');
    let destinationStreet = document.getElementById('destination-street');
    let destinationStreetNumber = document.querySelector('#destination-street-number');

    new AutocompleteField(destination, destinationCity, destinationStreet, destinationStreetNumber);

    let origin = document.querySelector("#origin-address");
    let originCity = document.querySelector('#origin-city');
    let originStreet = document.querySelector('#origin-street');
    let originStreetNumber = document.querySelector('#origin-street-number');

    new AutocompleteField(origin, originCity, originStreet, originStreetNumber);
}
