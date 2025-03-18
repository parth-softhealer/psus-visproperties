odoo.define('sh_wsale_address_google_place.sh_wsale_address_autofill', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    const { qweb } = require('web.core');
    const { debounce } = require("@web/core/utils/timing");

    publicWidget.registry.ShWSaleAddressAutofill = publicWidget.Widget.extend({
        selector: '.sh_js_cls_address_autofill',
        xmlDependencies: ['/sh_wsale_address_google_place/static/src/xml/sh_wsale_address_dropdown.xml'],
        events: {
            'input input[name="address"]': '_onChangeAddress',
            'click .sh_js_cls_address_dropdown_item': '_onClickAddressDropdownItem',
        },
        init: function () {
            this._super.apply(this, arguments);
            this.oldAddress = "";
            this.addressSuggestion = []
            this._onChangeAddress = debounce(this._onChangeAddress, 200);
        },
        start: function () {
            this._super.apply(this, arguments);
            var parent = this.$el.parent();
            this.viewTemplate = this.$el[0].dataset.viewTemplate !== undefined ? this.$el[0].dataset.viewTemplate : '';
            this.streetInput = parent.find('input[name="street"]');
            this.cityInput = parent.find('input[name="city"]');
            this.zipInput = this.viewTemplate === 'portal' ? parent.find('input[name="zipcode"]') : parent.find('input[name="zip"]');
            this.stateSelect = document.querySelector('select[name="state_id"]');
            this.countrySelect = document.querySelector('select[name="country_id"]');
        },
        /**
         * For Hide addresses dropdown
         * @param {Element} $el 
         */
        _hideAddressDropdown: function ($el) {
            const addressesDropdown = $el.find('.sh_js_cls_addresses_dropdown');
            if (addressesDropdown) {
                addressesDropdown.remove();
            }
        },
        /**
         * @private
         * @param {Event} ev 
         */
        async _onChangeAddress(ev) {
            var self = this;
            if (ev.currentTarget.value.length) {
                var address = ev.currentTarget.value;
                if (address.trim() != self.oldAddress.trim()) {
                    self._hideAddressDropdown(self.$el);
                    await this._rpc({ route: '/sh_wsale_address_google_place/partial_address', params: { partial_address: address } }).then(function (results) {
                        self.oldAddress = address
                        if (results.length > 0) {
                            self.addressSuggestion = results
                        }
                    });
                }
                self._showAddressDropDown();
            }
            else {
                self._hideAddressDropdown(self.$el);
            }
        },
        /**
         * Render the address drop down qweb and append it to the $el.
         * @private
         */
        async _showAddressDropDown() {
            if (this.addressSuggestion !== undefined && this.addressSuggestion.length > 0) {
                this.$el.append(qweb.render('sh_wsale_address_google_place.AddressDropDown', { addresses: this.addressSuggestion }));
            }
            else {
                this._hideAddressDropdown(this.$el);
            }
        },
        /**
         * @private
         * @param {Event} ev 
         */
        async _onClickAddressDropdownItem(ev) {
            const addressInput = this.$el.find('input[name="address"]');
            const address = ev.currentTarget.innerText.trim();
            if (addressInput !== undefined) {
                addressInput.val(address);
                this.oldAddress = address;
            }
            const address_vals = await this._rpc({ route: '/sh_wsale_address_google_place/fill_address', params: { address: address, place_id: ev.currentTarget.dataset.placeId } });
            if (address_vals) {
                this.countrySelect.value = address_vals.country !== undefined ? address_vals.country : 0;

                if(address_vals.country){
                    $(this.countrySelect).parents('.div_country').addClass('d-none')
                }
                else{
                    $(this.countrySelect).parents('.div_country').removeClass('d-none')
                }


                this.countrySelect.dispatchEvent(new Event('change', { bubbles: true }));
                if (address_vals.state) {
                    if (this.viewTemplate === 'shop') {
                        
                        new MutationObserver((entries, observer) => {
                            this.stateSelect.value = address_vals.state
                            if(address_vals.state){
                                $(this.stateSelect).parents('.div_state').addClass('d-none')
                            }
                            else{
                                $(this.stateSelect).parents('.div_state').removeClass('d-none')
                            }

                            observer.disconnect();
                        }).observe(this.stateSelect, {
                            childList: true,
                        });
                    }
                    else {
                        this.stateSelect.value = address_vals.state
                        if(address_vals.state){
                            $(this.stateSelect).parents('.div_state').addClass('d-none')
                        }
                        else{
                            $(this.stateSelect).parents('.div_state').removeClass('d-none')
                        }
                        this.stateSelect.dispatchEvent(new Event('change', { bubbles: true }));
                    }
                }
                // ZIP
                if(address_vals.zip){
                    this.zipInput.parents(".div_zip").addClass('d-none');
                    this.zipInput.val(address_vals.zip !== undefined ? address_vals.zip : '');
                }
                else{
                    this.zipInput.parents(".div_zip").removeClass('d-none');
                }
                
                // CITY
                if(address_vals.city){
                    this.zipInput.parents(".div_city").addClass('d-none');
                    this.cityInput.val(address_vals.city !== undefined ? address_vals.city : '');
                }
                else{
                    this.zipInput.parents(".div_city").removeClass('d-none');
                    this.cityInput.val('')
                }

                // STREET
                if(address_vals.formatted_street){
                    this.zipInput.parents(".div_street").addClass('d-none');
                    this.streetInput.val(address_vals.formatted_street !== undefined ? address_vals.formatted_street : address_vals.street !== undefined ? address_vals.street : '');
                }
                else{
                    this.zipInput.parents(".div_street").removeClass('d-none');
                }
                
            }
            this._hideAddressDropdown(this.$el);
        }
    })
});