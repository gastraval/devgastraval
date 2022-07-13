odoo.define("mrp_extension.ReportActionManager", function(require) {
    "use strict";

    const ActionManager = require("web.ActionManager");
    require("web.ReportActionManager");

    ActionManager.include({
        _triggerDownload: function(action, options, type) {
            const self = this;
            const reportUrls = this._makeReportUrls(action);
            if (action.post_action_to_run) {
                return this._downloadReport(reportUrls[type]).then(function() {
                    return self.doAction(action.post_action_to_run, options);
                });
            }
            return this._super.apply(this, arguments);
        },
    });
});
