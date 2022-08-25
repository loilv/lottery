odoo.define('lottery.custom_option_field', function (require) {
"use strict";
var BasicController = require('web.BasicController');


var CustomOptionField = BasicController.include({
    /**
     * Save the optional columns settings in local storage for this view
     *
     * @param {OdooEvent} ev
     * @param {Object} ev.data.keyParts see _getLocalStorageKey
     * @param {Array<string>} ev.data.optionalColumnsEnabled list of optional
     *   field names that have been enabled
     * @private
     */
    _onSaveOptionalFields: function (ev) {
        var old_data = this.call(
            'local_storage',
            'getItem',
            this._getOptionalFieldsLocalStorageKey(ev.data.keyParts)
        );
        var data = old_data.concat(ev.data.optionalColumnsEnabled)
        if (old_data.indexOf(ev.data.del_index) != -1){
            data.splice(old_data.indexOf(ev.data.del_index), 1);
        }
        this.call(
            'local_storage',
            'setItem',
            this._getOptionalFieldsLocalStorageKey(ev.data.keyParts),
            [...new Set(data)]
        );
    },
});
return CustomOptionField;
})