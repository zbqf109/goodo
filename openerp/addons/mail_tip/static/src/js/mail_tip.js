odoo.define('mail_tip.mail_tip', function (require) {
"use strict";

var mail = require('mail.chatter');

mail.ChatterMailThread.include({
    render_value: function() {
        var self = this;
        this._super.apply(this, arguments).done(function() {
            // event has to be triggered on form view
            self.view.trigger('chatter_messages_displayed');
        });
    }
});

});
