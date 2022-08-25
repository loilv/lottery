odoo.define('lottery.customer', function (require) {
"use strict";
var ListRenderer = require('web.ListRenderer');

var CustomOptional = ListRenderer.include({
    /**
     * We want section and note to take the whole line (except handle and trash)
     * to look better and to hide the unnecessary fields.
     *
     * @override
     */
    /**
     * When the user clicks on the checkbox in optional fields dropdown the
     * column is added to listview and displayed
     *
     * @private
     * @param {MouseEvent} ev
     */
    _onToggleOptionalColumn: function (ev) {
        var self = this;
        ev.stopPropagation();
        // when the input's label is clicked, the click event is also raised on the
        // input itself (https://developer.mozilla.org/en-US/docs/Web/HTML/Element/label),
        // so this handler is executed twice (except if the rendering is quick enough,
        // as when we render, we empty the HTML)
        ev.preventDefault();
        var input = ev.currentTarget.querySelector('input');
        var fieldIndex = this.optionalColumnsEnabled.indexOf(input.name);
        var del_index = ''
        if (fieldIndex >= 0) {
            del_index = input.name
            console.log(111111)
            this.optionalColumnsEnabled.splice(fieldIndex, 1);
        } else {
            this.optionalColumnsEnabled.push(input.name);
        }
        this.trigger_up('save_optional_fields', {
            keyParts: this._getOptionalColumnsStorageKeyParts(),
            optionalColumnsEnabled: this.optionalColumnsEnabled,
            del_index: del_index,
        });
        this._processColumns(this.columnInvisibleFields);
        this._render().then(function () {
            self._onToggleOptionalColumnDropdown(ev);
        });
    },
});
return CustomOptional;
})