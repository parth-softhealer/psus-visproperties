odoo.define("sh_wsale_address_google_place.custom", function (require) {
    "use strict";

    var publicWidget = require("web.public.widget");
    var ajax = require("web.ajax");
    var core = require("web.core");
    var _t = core._t;
    var concurrency = require("web.concurrency");

    publicWidget.registry.WebsiteSaleAddressAutoComplete = publicWidget.Widget.extend({
        selector: ".js_cls_address_input_div",

        /**
         *
         * @override
         */
        init: function () {
            this._super.apply(this, arguments);
            this.google_api_key = false;
        },

        /**
         * @override
         */
        async start() {
            var self = this;
            await this._super(...arguments);

            if (typeof google !== "object" || typeof google.maps !== "object") {
                // The animation will be restarted for all maps as soon as the
                // google map script has been executed.
                return;
            }

            var address1Field = this.el.querySelector('input[name="address"]');
            // Create the autocomplete object, restricting the search predictions to
            // addresses in the US and Canada.
            this.autocomplete = new google.maps.places.Autocomplete(address1Field, {
                // componentRestrictions: { country: ["us", "ca"] },
                fields: ["address_components", "geometry"],
                types: ["address"],
            });
            //address1Field.focus();
            google.maps.event.addListener(this.autocomplete, "place_changed", this._onPlaceChanged.bind(this));
            // When the user selects an address from the drop-down, populate the
            // address fields in the form.
            // autocomplete.addListener("place_changed", fillInAddress);
        },

        /**
         *
         * @override
         */
        willStart: function () {
            return this._super.apply(this, arguments).then(() => Promise.all([this._fetchData()]));
        },

        /**
         * Fetches the data.
         * Google Map API key
         * @private
         */
        async _fetchData() {
            const res = await this._rpc({
                route: "/sh_get_google_api_key",
                params: {},
            });
            this.google_api_key = res.api_key || false;
            await this.loadLibs();
        },

        /**
         * Loads the google libraries.
         *
         */
        async loadLibs() {
            if (this.google_api_key) {
                var URL = "https://maps.googleapis.com/maps/api/js?v=3&key=" + this.google_api_key + "&sensor=false&libraries=places";
                this._google_map_ready = await ajax.loadJS(URL);
            }
            return false;
        },

        /**
         * @private
         * @param {Event} ev
         */
        _onPlaceChanged(ev) {
			var self = this;
			var portal_profile = self.$target.hasClass('sh_portal_profile')
            let street = "";
            let postcode = "";
            let city = "";
            let state = "";
            let street2 = "";
            const gmapPlace = this.autocomplete.getPlace();
            if (gmapPlace.address_components !== undefined && !portal_profile) {
                for (const component of gmapPlace.address_components) {
                    // @ts-ignore remove once typings fixed
                    const componentType = component.types[0];
                    
                    switch (componentType) {
                        case "street_number": {
                            street += component.long_name;
                            break;
                        }
                        case "route": {
                            if(street){
								street += " "+component.long_name;	
							}
							else{
								street += component.long_name;
							}
                            break;
                        }
                        case "sublocality_level_3": {
                            if(street){
								street += ", " + component.long_name;	
							}
							else{
								street += component.long_name;
							}
                            break;
                        }
                        case "sublocality_level_2": {
                            if(street){
								street += ", " + component.long_name;	
							}
							else{
								street += component.long_name;
							}
                            break;
                        }

                        case "sublocality_level_1":
                            street2 = component.long_name;
                            break;
                        case "locality":
                            city = component.long_name;
                            break;
                        case "postal_town":
                            if(!city){
                                city = component.long_name;
                            }
                            break;
                        case "country":
                            this._rpc({
                                route: "/sh_get_country_state_code",
                                params: {
                                    country_name: component.long_name,
                                },
                            }).then(function (data) {
                                if (data.country_code) {
                                    $('select[name="country_id"]').val(data.country_code);
                                }
                                $('select[name="country_id"]').trigger("change");
                            });

                            break;

                        case "administrative_area_level_1":
                            this._rpc({
                                route: "/sh_get_country_state_code",
                                params: {
                                    state_name: component.long_name,
                                },
                            }).then(function (data) {
                                if (data.state_code) {
                                    setTimeout(function () {
                                        $('select[name="state_id"]').val(data.state_code);
                                    }, 600);
                                }
                            });
                            break;
                        case "postal_code": {
                            postcode = `${component.long_name}${postcode}`;
                            break;
                        }

                        case "postal_code_suffix": {
                            postcode = `${postcode}-${component.long_name}`;
                            break;
                        }
                    }
                }

                $('input[name="street"]').val(street);
                $('input[name="street2"]').val(street2);
                $('input[name="city"]').val(city);
                $('input[name="zip"]').val(postcode);
            }

			if (gmapPlace.address_components !== undefined && portal_profile) {
                for (const component of gmapPlace.address_components) {
                    // @ts-ignore remove once typings fixed
                    const componentType = component.types[0];

                    switch (componentType) {
                        case "street_number": {
                            street += component.long_name;
                            break;
                        }
                        case "route": {
                            if(street){
								street += " "+component.long_name;	
							}
							else{
								street += component.long_name;
							}
                            break;
                        }
                        case "sublocality_level_3": {
                            if(street){
								street += ", " + component.long_name;	
							}
							else{
								street += component.long_name;
							}
                            break;
                        }
                        case "sublocality_level_2": {
                            if(street){
								street += ", " + component.long_name;	
							}
							else{
								street += component.long_name;
							}
                            break;
                        }

                        case "sublocality_level_1":
                            street += ", " + component.long_name;
                            break;
                        case "locality":
                            city = component.long_name;
                            break;
                        case "postal_town":
                            if(!city){
                                city = component.long_name;
                            }
                            break;
                        case "country":
                            this._rpc({
                                route: "/sh_get_country_state_code",
                                params: {
                                    country_name: component.long_name,
                                },
                            }).then(function (data) {
                                if (data.country_code) {
                                    $('select[name="country_id"]').val(data.country_code);
                                }
                                $('select[name="country_id"]').trigger("change");
                            });

                            break;

                        case "administrative_area_level_1":
                            this._rpc({
                                route: "/sh_get_country_state_code",
                                params: {
                                    state_name: component.long_name,
                                },
                            }).then(function (data) {
                                if (data.state_code) {
                                    setTimeout(function () {
                                        $('select[name="state_id"]').val(data.state_code);
                                    }, 600);
                                }
                            });
                            break;
                        case "postal_code": {
                            postcode = `${component.long_name}${postcode}`;
                            break;
                        }

                        case "postal_code_suffix": {
                            postcode = `${postcode}-${component.long_name}`;
                            break;
                        }
                    }
                }

                $('input[name="street"]').val(street);
                $('input[name="street2"]').val(street2);
                $('input[name="city"]').val(city);
                $('input[name="zip"]').val(postcode);
            }
        },
    });
});
