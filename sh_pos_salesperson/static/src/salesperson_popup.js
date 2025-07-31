import { usePos } from "@point_of_sale/app/store/pos_hook";
import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class SalespersonPopup extends Component {
    setup() {
        this.pos = usePos();
        this.popup = useService("popup");
    }

    async selectSalesperson(userId) {
        this.props.resolve({ confirmed: true, payload: userId });
        this.popup.close();
        console.log("sjfbeiergbnerklgfref==================")
    }

    cancel() {
        this.props.resolve({ confirmed: false });
        this.popup.close();
    }
}
    // console.log("calleddddd")
SalespersonPopup.template = "SalespersonPopup";

 