// import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { patch } from "@web/core/utils/patch";
 
patch(PosOrderline.prototype, {
    getDisplayData() {
        return {
            ...super.getDisplayData(),
            sh_salesperson_id: this.sh_salesperson_id?.id || "",
            sh_salesperson_src: `/web/image/res.users/${this.sh_salesperson_id?.id}/avatar_128` || "",
            sh_salesperson_name: this.sh_salesperson_id?.name || ""
        };
    },
    remove_salesperson(){
        console.log("fghjkllllllp-",this)
        this.sh_salesperson_id = false
    }
});
